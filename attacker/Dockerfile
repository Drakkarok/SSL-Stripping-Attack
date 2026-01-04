FROM kalilinux/kali-rolling

# Install necessary tools
# sslstrip: HTTPS downgrade
# dsniff: Contains arpspoof
# iptables: For redirection
# net-tools, iproute2: Networking utilities
# python3-scapy: Packet manipulation
RUN apt-get update && apt-get install -y \
    sslstrip \
    dsniff \
    iptables \
    net-tools \
    iproute2 \
    python3-scapy \
    tcpdump \
    procps \
    nano \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
