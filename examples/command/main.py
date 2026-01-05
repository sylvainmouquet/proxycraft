import threading
import socket
import time
from proxycraft import ProxyCraft
import logging

if __name__ == "__main__":
    # Initialize the proxy
    proxycraft: ProxyCraft = ProxyCraft(config_file="proxy.json")
    proxycraft.serve()