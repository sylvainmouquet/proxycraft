from pyprox import PyProx

if __name__ == "__main__":
    pyprox: PyProx = PyProx(config_file="proxy.json")
    pyprox.serve(host="0.0.0.0", port=8091)
