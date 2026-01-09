from proxycraft import ProxyCraft

if __name__ == "__main__":
    # Initialize the proxy
    proxycraft: ProxyCraft = ProxyCraft(config_file="proxy.json")
    proxycraft.serve()
