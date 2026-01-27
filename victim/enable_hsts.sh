#!/bin/bash

HSTS_CACHE="/root/hsts-cache"

echo "----------------------------------------------------------------"
echo " [?] Activating HSTS Protection..."
echo "     Step 1: Poking server to Enable HSTS (Global Toggle)"
# We go directly to HTTPS (bypassing sslstrip) to toggle the switch
curl -k https://bank_server/toggle_security > /dev/null 2>&1
echo "     [+] Server HSTS Mode toggled."

echo "     Step 2: Visiting Secure Site to Learn HSTS Policy"
# We visit the site via HTTPS and save the HSTS header to our cache file
curl -k -v --hsts $HSTS_CACHE https://bank_server > /dev/null 2>&1
echo "     [+] HSTS Policy cached in: $HSTS_CACHE"
echo "----------------------------------------------------------------"
