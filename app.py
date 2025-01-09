# app.py
import socket
from flask import Flask, jsonify
import os
import psutil

app = Flask(__name__)

@app.route("/")
def home():
    return f"Response from: {socket.gethostname()} (Container ID: {os.environ.get('HOSTNAME')})"
    
@app.route("/metrics")
def metrics():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

