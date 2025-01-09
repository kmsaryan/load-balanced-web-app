import requests
import time
import os

# List of web servers
servers = {
    "web1": "http://web1:5000/metrics",
    "web2": "http://web2:5000/metrics",
    "web3": "http://web3:5000/metrics",
}

# Get the base directory where the controller is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set the correct path to the haproxy.cfg file
haproxy_cfg_path = os.environ.get("HAPROXY_CFG_PATH", "/usr/local/etc/haproxy/haproxy.cfg")


if not haproxy_cfg_path:
    raise ValueError("Environment variable HAPROXY_CFG_PATH is not set.")

def fetch_metrics():
    server_metrics = {}
    for name, url in servers.items():
        try:
            response = requests.get(url, timeout=2)
            metrics = response.json()
            server_metrics[name] = metrics
        except Exception as e:
            print(f"Error fetching metrics from {name}: {e}")

    # Write metrics to a file for debugging
    with open("metrics_log.txt", "a") as f:
        f.write(str(server_metrics) + "\n")

    return server_metrics

def generate_haproxy_config(server_metrics):
    config = """
global
    #log stdout format raw

defaults
    log global
    mode http
    option httplog
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:8080
    default_backend http_back

backend http_back
    balance roundrobin
"""
    for name, metrics in server_metrics.items():
        weight = int((100 - metrics['cpu']) / 10)  # Example: Higher CPU -> Lower weight
        config += f"    server {name} {name}:5000 weight {weight} check\n"

    return config

def main():
    while True:
        server_metrics = fetch_metrics()
        haproxy_config = generate_haproxy_config(server_metrics)
        with open(haproxy_cfg_path, "w") as f:
            f.write(haproxy_config)
        
        # Reload HAProxy
        os.system("haproxy -f /usr/local/etc/haproxy/haproxy.cfg -D -sf $(pidof haproxy)")
        time.sleep(10)  # Poll every 10 seconds

if __name__ == "__main__":
    main()
