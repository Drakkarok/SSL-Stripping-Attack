#!/bin/bash

# Start the Main Banking App (HTTPS) in the background
echo "[*] Starting Banking App (HTTPS)..."
python3 app.py &

# Start the Redirector (HTTP) in the background
echo "[*] Starting HTTP Redirector..."
python3 redirector.py &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
