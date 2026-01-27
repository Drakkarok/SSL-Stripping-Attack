# SSL Stripping Attack - Demo Script

**Credentials**:
*   Username: `admin`
*   Password: `password123`

---

## 1. Setup & Launch
**Goal**: Start the environment with a clean slate.

1.  **Open Terminal** (Host):
    ```bash
    # Ensure fresh start (clears HSTS state)
    docker compose down
    docker compose up --build -d
    ```

---

## 2. Launch The Attack (The Hacker)
**Goal**: Intercept traffic between Victim and Bank.

1.  **Open Terminal A** (Attacker View):
    ```bash
    docker exec -it kali_attacker /bin/bash
    ```
2.  **Start the Attack**:
    *   This script enables ARP Spoofing and `sslstrip` interception.
    *   Targets: Victim (172.28.0.30) <-> Bank (172.28.0.20)
    ```bash
    cd /root/attacker_scripts
    ./attack.sh 172.28.0.30 172.28.0.20
    ```
    *   *Output: "Disabling Reverse Path Filtering...", "Disabling ICMP Redirects...", "Attack running..."*

---

## 3. The Vulnerable Victim (No HSTS)
**Goal**: Demonstrate successful SSL Stripping.

1.  **Open Terminal B** (Victim View):
    ```bash
    docker exec -it victim_client /bin/bash
    ```
2.  **Simulate Login**:
    *   The victim types `http://bank_server` (HTTP).
    *   Without attack, this forces a redirect to HTTPS.
    *   **With attack**, the redirect is stripped.
    ```bash
    ./login.sh
    ```
3.  **Observation**:
    *   **Victim**: You see `HTTP/1.1 200 OK` (Success) instead of a Redirect.
    *   **Attacker (Terminal A)**: You see **CAPTURED CREDENTIALS** in red found in the logs.

---

## 4. The Defense (HSTS Protection)
**Goal**: Show how HSTS prevents this attack.

1.  **Enable HSTS (Victim Terminal)**:
    *   This script visits the bank securely once to learn the HSTS policy and caches it.
    ```bash
    ./enable_hsts.sh
    ```
2.  **Retry Login**:
    ```bash
    ./login.sh
    ```
3.  **Observation**:
    *   **Victim**: You see `Switched from HTTP to HTTPS due to HSTS`.
    *   The connection upgrades to **HTTPS (Port 443)** immediately.
    *   **Attacker**: Sees nothing (or encrypted garbage), because `sslstrip` cannot downgrade an internally forced HTTPS request.

---

## 5. Resetting for New Demo
**Goal**: Clear HSTS to demonstrate the vulnerability again.

To go back to Step 3 (Vulnerable state), you must clear the server's memory and the victim's cache.

1.  **Host Terminal**:
    ```bash
    # Restarts server (clears server-side HSTS flag) AND victim (clears client cache)
    docker compose restart
    ```
    *Or for a full reset:*
    ```bash
    docker compose down && docker compose up -d
    ```

---

## Troubleshooting
*   **No Credentials Captured?**
    *   Ensure `attack.sh` says "Disabling Reverse Path Filtering". If not, rebuild: `docker compose up --build -d`.
*   **Victim sees 405 Method Not Allowed?**
    *   Update `victim/login.sh` to ensure it doesn't use `-X POST` (already fixed in latest version).
*   **Attack not intercepting?**
    *   Check if ICMP redirects are disabled on the attacker: `cat /proc/sys/net/ipv4/conf/eth0/send_redirects` (should be 0).
*   **SSLStrip crashing?**
    *   Ensure the Python 3 patches in `setup.sh` have been applied.
