**Credentials**:
admin
password123

# SSL Stripping Attack Demo Script

## 1. Setup (Preparation)
**Goal**: Start the environment.

1.  **Open Terminal** (in project folder):
    ```bash
    docker compose up --build -d
    ```
2.  **Verify Status**:
    *   Open Browser: [http://localhost:5001](http://localhost:5001)
    *   You should see the "Bank of Simulation" login page.

---

## 2. Launch Attack (The "Hacker" View)
**Goal**: Start interception.

1.  **Enter Attacker Container**:
    ```bash
    docker exec -it kali_attacker /bin/bash
    ```
2.  **Start Attack Script**:
    ```bash
    cd /root/attacker_scripts
    ./attack.sh 172.28.0.20 172.28.0.1
    ```
    *   *You will see: "Attack running..."*

---

## 3. Victim Action (The "User" View)
**Goal**: Generate traffic to be stolen.

1.  **Go to Browser**: [http://localhost:5001/login](http://localhost:5001/login)
2.  **Enter Credentials**:
    *   Username: `admin`
    *   Password: `password123`
3.  **Click Login**:
    *   You are redirected to the Dashboard normally.
    *   *Visuals: Nothing looks wrong.*

---

## 4. The Reveal
**Goal**: Show stolen data.

1.  **Check Attacker Terminal**:
    *   Look at the output of the running script.
    *   **SUCCESS**: You should see the captured `username=admin` and `password=password123` in plain text.

---

## 5. Defense (HSTS)
**Goal**: Show how to stop it.

1.  **Go to Browser**: [http://localhost:5001](http://localhost:5001)
2.  **Click**: "Toggle HSTS Protection" (Bottom link).
    *   *Message: "HSTS Protection enabled!"*
3.  **Try Login Again**:
    *   In this simulated environment, the browser will likely now refuse to load HTTP resources or the attack script (sslstrip) will fail to downgrade properly because the server is demanding security headers. (strict-transport-security max-age=31536000; includeSubDomains)
    *   *Note: Real HSTS requires valid HTTPS certificates. In this lab, we demonstrate the header presence.*

---

## 6. Cleanup
**Goal**: Stop everything.

1.  **Stop Attack**: `Ctrl+C` in attacker terminal.
2.  **Stop Containers**:
    ```bash
    docker compose down
    ```
