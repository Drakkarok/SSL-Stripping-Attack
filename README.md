# SSL Stripping Attack - Proof of Concept
**University Project: SINF - Securitatea Informatică**

This repository contains a complete Docker-based environment to demonstrate an **SSL Stripping (HTTPS Downgrade)** Man-in-the-Middle attack.

## 🏗 Project Architecture

| Component | Technology | Description |
|-----------|------------|-------------|
| **Attacker** | Kali Linux Docker | Runs `sslstrip`, `arpspoof`, `tcpdump`, and `iptables`. |
| **Simulated Bank** | Python Flask | A vulnerable banking application running on port 5000 (mapped to host 5001). |
| **Victim** | Host Machine | Your web browser interacting with the "Bank". |

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Terminal (support for ANSI colors recommended)

### Installation & Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Drakkarok/SSL-Stripping-Attack.git
    cd SSL-Stripping-Attack
    ```
2.  **Start the Environment**:
    ```bash
    docker compose up --build -d
    ```
3.  **Verify Access**:
    -   Open Browser: [http://localhost:5001](http://localhost:5001)

## ⚔️ Running the Attack Demo

Detailed step-by-step instructions are in [DEMO_SCRIPT.md](./DEMO_SCRIPT.md).

**Quick Reference:**
1.  **Enter Attacker Container**:
    ```bash
    docker exec -it kali_attacker /bin/bash
    ```
2.  **Execute Attack**:
    ```bash
    cd /root/attacker_scripts
    ./attack.sh 172.28.0.20 172.28.0.1
    ```
3.  **Perform Action**:
    -   Login on the website.
    -   Watch the terminal for captured credentials.

## 🛡 Mitigation: HSTS
The application includes a demonstration of **HTTP Strict Transport Security (HSTS)**.
1.  Click **"Toggle HSTS Protection"** on the homepage.
2.  The server will now send the `Strict-Transport-Security` header.
3.  **Effect**: In a real HTTPS scenario, this header instructs the browser to **refuse** any unencrypted (HTTP) connections, effectively blocking the SSL Stripping attack.
    *   *Note: In this specific HTTP-only lab environment, browsers will ignore this header because it is not delivered over a secure channel (RFC 6797). This allows us to inspect the header without locking ourselves out.*

## 📁 Project Structure
- `attacker/`: Setup scripts (`iptables`, `sysctl`) and attack automation.
- `web_server/`: Flask application source code.
- `docker-compose.yml`: Network layout and container definitions.

## ⚠️ Disclaimer
This project is for **educational purposes only**. It demonstrates a vulnerability to understand how to defend against it. Do not use these tools on networks you do not own or have permission to test.
