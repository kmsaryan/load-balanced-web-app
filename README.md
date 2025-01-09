# Load-Balanced Web App

**Implementation and Demonstration of Adaptive Load Balancing in MS Azure**

This project demonstrates a scalable architecture employing NGINX as a reverse proxy, HAProxy as a load balancer, and Flask-based web servers. It integrates dynamic load balancing and resource-aware traffic distribution, leveraging Docker for containerization in Microsoft Azure.

---

## **System Overview**

### **Components**

1. **Proxy Server (NGINX)**: Entry point for client requests, forwarding traffic to the load balancer.
2. **Load Balancer (HAProxy)**: Distributes traffic using weighted round-robin and dynamically adjusts based on server health.
3. **Web Servers (Flask)**: Serve responses while exposing a `/metrics` endpoint for real-time workload statistics.
4. **Controller (Python)**: Fetches metrics, calculates dynamic weights, and updates HAProxy configuration for adaptive load balancing.

---

## **Virtualization Techniques**

1. **OS-Level Virtualization**:
   - Services are isolated in Docker containers, sharing the host OS kernel.
2. **Network Virtualization**:
   - Docker’s bridge network enables seamless container communication.

---

## **Dynamic Load Balancing Workflow**

1. **Traffic Flow**:
   - Client → Proxy → Load Balancer → Web Servers → Response to Client.
2. **Dynamic Weight Adjustments**:
   - Controller polls `/metrics` from web servers and adjusts HAProxy weights based on CPU usage.

---

## **Setup Instructions**

1. **Clone Repository**:
   ```bash
   git clone https://github.com/<your-repo>/load-balanced-web-app.git
   cd load-balanced-web-app
   ```

2. **Build and Start Services**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. **Impose Load**:
   ```bash
   docker exec -it web1 stress --cpu 2 --timeout 60s
   docker exec -it web2 stress --cpu 4 --timeout 60s
   docker exec -it web3 stress --cpu 1 --timeout 60s
   ```

4. **Verify Configuration**:
   - Inspect dynamic HAProxy configuration:
     ```bash
     docker exec -it loadbalancer cat /usr/local/etc/haproxy/haproxy.cfg
     ```
   - View controller logs:
     ```bash
     docker logs -f controller
     ```

---

## **Key Features**

1. **Dynamic Resource Awareness**:
   - HAProxy adjusts weights to offload stressed servers.
2. **Scalable and Modular**:
   - Docker Compose manages services with ease.
3. **Adaptive Behavior**:
   - Real-time metrics influence traffic distribution.

---

## **Results**

- Adaptive load balancing efficiently handles varying server workloads.
- Stress tests demonstrated proper redistribution of traffic based on real-time metrics.

---

## **Project Directory Structure**

```plaintext
myproject/
├── Dockerfile           # Web server Dockerfile
├── app.py               # Web server application code
├── proxy/
│   ├── Dockerfile       # Proxy server Dockerfile
│   └── nginx.conf       # Proxy server NGINX configuration
├── loadbalancer/
│   ├── Dockerfile       # Load balancer Dockerfile
│   └── haproxy.cfg      # Load balancer HAProxy configuration
├── controller/
│   ├── Dockerfile       # Controller Dockerfile
│   └── controller.py    # Controller Python script
└── docker-compose.yml   # Docker Compose configuration
```

---

## **Behavior During Load**

1. Servers under high CPU load are dynamically assigned lower weights.
2. Load balancer distributes requests proportionally to favor less loaded servers.
3. Real-time monitoring of weights and traffic adjustments ensures optimal performance.

---

## **Metrics Logging**

The controller logs collected metrics to a file for inspection:
```bash
docker exec -it controller cat /app/metrics_log.txt
```
![image](https://github.com/user-attachments/assets/639b7582-0270-4081-804c-f5e2647e42a7)
![image](https://github.com/user-attachments/assets/898d3fa8-71af-4a39-979d-89ed0b02fa39)
![image](https://github.com/user-attachments/assets/585787db-d039-4b42-8ead-5b5a8f8b6145)

---

## **Summary**

The project demonstrates dynamic and adaptive load balancing using HAProxy and Python. Docker containers provide scalability, and real-time metrics ensure efficient traffic distribution. The setup is ideal for environments requiring high availability and resource optimization.
