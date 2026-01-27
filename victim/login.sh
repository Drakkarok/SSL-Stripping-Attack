#!/bin/bash

HSTS_CACHE="/root/hsts-cache"
HSTS_FLAG=""

if [ -f "$HSTS_CACHE" ]; then
    echo " [!] HSTS Cache Found! Using Protection."
    HSTS_FLAG="--hsts $HSTS_CACHE"
fi

echo "----------------------------------------------------------------"
echo " [?] Simulating User Login Attempt..."
echo "     Target: http://bank_server/"
echo "     Params: username=admin, password=password123"
echo "----------------------------------------------------------------"

# We request HTTP.
# If HSTS is cached, curl should internally upgrade to HTTPS before sending the request.
# If attack is running:
# - WITHOUT HSTS: curl sends HTTP -> Attacker intercepts.
# - WITH HSTS: curl upgrades to HTTPS locally -> Attacker sees HTTPS (cannot strip) or connection bypasses attacker.
curl -L -k -v $HSTS_FLAG -d "username=admin&password=password123" http://bank_server/login

echo ""
echo "----------------------------------------------------------------"
