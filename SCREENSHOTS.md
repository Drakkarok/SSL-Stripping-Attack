# Required Screenshots for Report

To complete your essay and presentation, please take the following screenshots during your demo:

## 1. Environment Setup
- [ ] **Docker Status**: Terminal showing `docker compose ps` with both containers running.
- [ ] **Network**: Output of `docker network inspect proiect_ssl_strip_net` showing the subnet (optional but good for technical details).

## 2. The "Before" State
- [ ] **Clean Login Page**: The banking site [localhost:5001](http://localhost:5001) looking normal.
- [ ] **Dashboard**: Successfully logged in as `admin`.

## 3. The Attack
- [ ] **Attacker Terminal**: Command `./attack.sh ...` running with the "Attack running" message.
- [ ] **Captured Credentials**: **CRITICAL**. A screenshot of the terminal clearly showing the red/green "CAPTURED CREDENTIALS" output with the username and password.

## 4. Defense (HSTS)
- [ ] **HSTS Enabled Message**: The flash message on the website saying "HSTS Protection enabled!".
- [ ] **Header Inspection**: Open Browser DevTools (F12) -> Network -> Click `localhost` request -> **Headers**. Screenshot the `Strict-Transport-Security` header being present.
