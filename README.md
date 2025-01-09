# load-balanced-web-app
Implementation and Demonstration of Load Balancer for HTTP Requests in MS Azure using Virtualization Techniques  
Load Balancing and Proxy Server Architecture with Docker, NGINX, and HAProxy
## Introduction
This project demonstrates a scalable system architecture that includes a reverse proxy (NGINX) and a load balancer (HAProxy) to distribute traffic across two web servers. The goal is to provide high availability and efficient load distribution using Docker containers in a virtual machine hosted on Microsoft Azure.
## Architecture Overview
The project consists of the following components each component has been deployed in its own container 
myproject/
├── Dockerfile           # Web server Dockerfile
├── app.py               # Web server application code
├── proxy/
│   ├── Dockerfile       # Proxy server Dockerfile
│   └── nginx.conf       # Proxy server NGINX configuration
├── loadbalancer/
│   ├── Dockerfile       # Load balancer Dockerfile
│   └── haproxy.cfg      # Load balancer HAProxy configuration
└── docker-compose.yml   # Docker Compose configuration
### Components:
1.	Proxy Server (NGINX): Acts as the ingress point for client requests and forwards them to the load balancer.
2.	Load Balancer (HAProxy): Distributes traffic to three backend web servers using the Round Robin algorithm.
3.	Web Servers (Flask): Serve HTTP responses, identifying themselves by name (WebServer1 and WebServer2, Webserver3).
How does it work!
•	Client: Sends an HTTP request to the system’s public IP (e.g., via curl or browser).
•	Proxy Server (NGINX): Receives the request and forwards it to the load balancer.
•	Load Balancer (HAProxy): Distributes the incoming request to one of the available web servers (web1, web2, or web3) based on the configured load balancing algorithm.
•	Web Servers: Process the request and return a response (e.g., "Response from web1") to the client via the same path.
In this project we implemented two virtualizations namely OS level and network virtualization.
### OS Level virtualization
We used Docker containers to Virtualize the web servers, load balancer and proxy server. Each service is in its own container isolated, but they share the host OS kernel since they are isolated, they use minimal resources 
### Network Virtualization
Docker’s bridge network was used to connect all the containers in this project this enables seamless communication between webservers, load balancer, proxy.
The following describes the parallels to SDN technology
•	The traditional VM virtualize the hardware layer, but Docker containers provide light weight virtualization at the application level. They share the host OS kernel which makes them more efficient.
•	Docker bridge network used here acts a virtual switch enabling isolated communication between containers. Containers in the same network can communicate via assigned IP or Container names.
•	Containers consume fewer resources compared to Vms because they share the host kernel 
•	Docker's bridge networking enables logical separation of containerized workloads while maintaining physical network infrastructure.
## Implementation:
We have created a network for the project using docker network command 
We utilized one flask app and docker file in project root directory, and a directory for load balancer and proxy along with respective configuration files and Docker files the following  we used docker compose  instead of relying on manual building and starting of container.
The docker compose build will build the containers defined in the ‘docker-compose.yml file’
` docker-compose build `
To start the containers in detached mode:
` docker-compose up -d 
To Start all containers without recreating them: 
` docker-compose start `
To Stop running containers: 
` docker-compose stop `
To restart all containers:
` docker-compose restart `
To stop and remove all containers, networks, and volumes:
` docker-compose down `
### Load balancer configuration used: 
Weighted round robin Algorithm: 
this also a static load balancing approach which is quite similar to the round robin technique the difference is it allocates requests based on the preconfigured weights. Which are present in the snipped provided here.
•	Weights influence traffic distribution:
o	web1 will handle 1 request per round.
o	web2 will handle 3 requests per round.
o	web3 will handle 2 requests per round.
This means Out of every 6 requests (sum of weights), traffic will be distributed as follows:
o	web1: 16.7% (1/6 of the traffic).
o	web2: 50% (3/6 of the traffic).
o	web3: 33.3% (2/6 of the traffic).
### Controller Script:
•	Fetches CPU metrics from /metrics endpoint exposed by the web servers.
•	Uses the CPU metrics to calculate weights for each server (higher CPU -> lower weight).
•	Dynamically updates the HAProxy configuration file (haproxy.cfg) with the new weights.
•	Reloads HAProxy to apply the updated configuration.
### Docker Compose Setup:
•	The controller service is introduced as a separate container.
•	The haproxy.cfg file is managed as a shared volume (haproxy-config) between the controller and loadbalancer containers.
•	The controller dynamically updates this configuration file, and HAProxy picks up the changes upon reload.
Controller Functionality:
•	The controller dynamically updates the load balancing configuration based on real-time metrics.
•	It ensures efficient utilization of resources by reducing the load on highly stressed servers.
### Adaptive Load Balancing:
•	HAProxy weights adjust dynamically to reflect server health and workload.
•	Load balancing adapts to changing conditions, ensuring better response times and availability.
Behavior During Load:
•	Servers under high CPU load were assigned lower weights.
•	Requests were distributed proportionally, favoring less loaded servers.
## Results
•	Imposed CPU load on the web servers using the stress tool:
docker exec -it web1 stress --cpu 2 --timeout 60s
docker exec -it web2 stress --cpu 4 --timeout 60s
docker exec -it web3 stress --cpu 1 --timeout 60s
This simulates high CPU usage on web1 and web2, while web3 remains relatively less loaded.
Step 3: Inspecting the Updated Configuration
•	The controller dynamically adjusts server weights in haproxy.cfg based on the CPU metrics.
•	View the updated HAProxy configuration:
 ` docker exec -it loadbalancer cat /usr/local/etc/haproxy/haproxy.cfg `
o	The weights reflect the CPU load: higher CPU -> lower weight.
after the stress test the updated haproxy configuration
the metric return into a file and can be accessed using the following command.
`docker exec -it controller cat /app/metrics_log.txt`
## Summary
The servers are alternating and responding to requests sent directly from the proxy and directly from the load balancer. Indicating the configuration is working as expected 
The servers are responding to requests send from local machine and responses are cycling between the available servers in the configuration 
