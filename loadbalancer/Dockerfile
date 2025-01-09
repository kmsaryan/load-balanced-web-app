FROM haproxy:2.6

USER root

# Install curl and Python for controller interaction
RUN apt-get update --allow-releaseinfo-change && apt-get install -y curl python3 python3-pip

COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
