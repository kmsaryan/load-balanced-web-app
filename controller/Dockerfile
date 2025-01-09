#Docekerfile for the controller
FROM python:3.9-slim

WORKDIR /app

# Copy the controller script
COPY controller.py .

# Install dependencies
RUN apt-get update --allow-releaseinfo-change && apt-get install -y curl python3 python3-pip haproxy

# Install Python dependencies
RUN pip install requests

# Set the entry point for the controller script
CMD ["python3", "/app/controller.py"]
