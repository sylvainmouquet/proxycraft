from proxycraft import ProxyCraft

if __name__ == "__main__":
    proxycraft: ProxyCraft = ProxyCraft(config_file="proxy.json")
    proxycraft.serve(host="0.0.0.0")
