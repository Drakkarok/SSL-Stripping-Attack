#!/bin/bash

# Start the attack in the background using the dedicated test script
# Ensure we target Victim (30) and Server (20)
echo "[*] Starting Attack for Diagnostics..."
docker exec -d -w /root/attacker_scripts kali_attacker ./test_attack.sh

# Wait 5 seconds for arpspoof to pollute the cache
echo "[*] Waiting 5s for ARP spoofing..."
sleep 5

# Check Victim's ARP table
echo "[?] Victim's ARP Table (Should show Attacker's MAC for Server IP):"
echo "    Server IP: 172.28.0.20"
echo "    Attacker IP: 172.28.0.10"
echo "---------------------------------------------------------------"
docker exec victim_client ip neigh show
echo "---------------------------------------------------------------"

# Get Real MACs for comparison
echo "[?] Actual MAC Addresses:"
docker network inspect proiect_ssl_strip_net | grep -E "Name|IPv4Address|MacAddress" | grep -v "proiect_ssl_strip_net"
