# Implementation Details & Simulation Scope

## 1. Overview: The "Post-Downgrade" Simulation
This Proof of Concept (PoC) focuses on the critical **Credential Harvesting** phase of a Man-in-the-Middle (MiTM) attack. 

In a fully wild SSL Stripping attack, the attacker must intercept the initial 301 Redirect from HTTP to HTTPS. However, to maintain a portable and reproducible lab environment without requiring valid global SSL certificates or complex DNS spoofing, this project simulates the **"Post-Downgrade" state**.

### What we simulate
*   **The Victim's State**: The user is already communicating over an insecure HTTP channel (simulating a successful strip or a phishing link).
*   **The Attack**: The traffic flows through the attacker's machine, where it is inspected and logged.
*   **The Consequence**: Plaintext credentials are captured in real-time.

---

## 2. Technical Limitations & Constraints

### A. HTTP-Only Environment (The HSTS Paradox)
The biggest limitation of a local lab vs. a production environment is the lack of valid, trusted SSL Certificates.
*   **Production**: A server has a valid certificate. The browser trusts it. The browser accepts the HSTS header and blocks future HTTP connections.
*   **Lab (This Project)**: The server runs on HTTP. It sends the valid HSTS header.
*   **The Result**: Modern browsers (Chrome, Safari, etc.) strictly follow **RFC 6797**, which states that **HSTS headers received over insecure HTTP must be ignored**.
    *   *Why?* To prevent attackers from injecting fake security rules that break connectivity.
    *   *Demo Impact*: This is why enabling HSTS in our lab does not immediately "Red Screen" the browser. We demonstrate the **Presence** of the defense (the header) rather than the **Enforcement** (the block).

### B. Docker for Mac Network Isolation
Use of Docker Desktop on macOS introduces a virtualization layer that handles networking differently than native Linux.
*   **Limitation**: Standard ARP Spoofing (poisoning the cache of the host machine) is often blocked or ignored by the virtualization bridge.
*   **Workaround**: We utilized `tcpdump` directly on the Attacker's container interface. Since all traffic in the Docker subnet must pass through the bridge, the attacker (positioned as the gateway/neighbor) can successfully sniff the packets even if the host machine's ARP table fights back.

---

## 3. Architecture Summary
| Component      | Role        | Simulation Status                                                |
| -------------- | ----------- | ---------------------------------------------------------------- |
| **Attacker**   | Interceptor | **Active**: Uses `iptables` and packet sniffing.                 |
| **Web Server** | Bank        | **Simulated**: Vulnerable HTTP endpoint with HSTS logic enabled. |
| **Session**    | Traffic     | **Downgraded**: Traffic is forced to HTTP for visibility.        |

## 4. Conclusion
While we do not perform the initial "Strip" of the HTTPS handshake (due to the lack of an HTTPS upstream), we successfully demonstrate the **integrity loss** and **confidentiality breach** that occurs when that strip is successful. The project validates that **if** a user is on HTTP, **all** data is compromised.
