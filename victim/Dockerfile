FROM alpine:latest

# Install curl and bash for interaction
RUN apk add --no-cache curl bash

WORKDIR /root

# Copy scripts
COPY login.sh .
COPY enable_hsts.sh .
RUN chmod +x login.sh enable_hsts.sh

# Keep container running
CMD ["tail", "-f", "/dev/null"]
