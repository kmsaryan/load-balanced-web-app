# app.py
from flask import Flask
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Response from: {socket.gethostname()} (Container ID: {os.environ.get('HOSTNAME')})"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

