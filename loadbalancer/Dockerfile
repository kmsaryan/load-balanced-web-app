FROM haproxy:2.6

# Fix for permission issues with apt
USER root
RUN apt-get update --allow-releaseinfo-change && apt-get install -y curl

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

