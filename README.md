
<h1 align="center">
ProxyCraft
</h1>


<p align="center"><i>ProxyCraft is the easiest and quickest way to deploy a web proxy.</i></p>

****

<!-- Project Status Badges -->
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

<!-- Technology Badges 
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Asyncio](https://img.shields.io/badge/Asyncio-FFD43B?style=flat&logo=python&logoColor=blue)
-->
<!-- Protocol Support Badges -->
![HTTP](https://img.shields.io/badge/HTTP-✅-green)
![HTTPS](https://img.shields.io/badge/HTTPS-✅-green)
![WebSocket](https://img.shields.io/badge/WebSocket-✅-green)
![SOCKS5](https://img.shields.io/badge/SOCKS5-✅-green)
![TCP/UDP](https://img.shields.io/badge/TCP%2FUDP-✅-green)

<!-- Installation Badge 
![PyPI](https://img.shields.io/pypi/v/idum-proxy?logo=pypi&logoColor=white)
![Downloads](https://img.shields.io/pypi/dm/idum-proxy?logo=pypi&logoColor=white)
-->
<!-- Social Badges
![GitHub stars](https://img.shields.io/github/stars/idumhq/idum-proxy?style=social)
![GitHub forks](https://img.shields.io/github/forks/idumhq/idum-proxy?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/idumhq/idum-proxy?style=social)
 -->
<!-- Custom Style Badges 
![Proxy](https://img.shields.io/badge/🌐_Proxy-Server-4F46E5?style=for-the-badge)
![Performance](https://img.shields.io/badge/⚡_High-Performance-10B981?style=for-the-badge)
![Security](https://img.shields.io/badge/🔒_Secure-Authentication-DC2626?style=for-the-badge)
-->

****

## ✨ Features

ProxyCraft offers many features:

- 🔒 Protocol Support: Handle HTTP, HTTPS, WebSockets, TCP/UDP, and SOCKS proxies
- 🔐 Authentication: Support for various auth methods (Basic, Digest, NTLM, Kerberos)
- 🔄 Connection Pooling: Efficient reuse of connections to improve performance
- ⚖️ Load Balancing: Distribute traffic across multiple proxies
- 🏥 Health Checking: Automatic detection and recovery from failed proxies
- 💾 Caching: Store and reuse responses for identical requests
- 🔄 Retry Mechanisms: Automatically retry failed requests
- 🔧 Circuit Breaking: Prevent cascading failures
- 📊 Metrics Collection: Track proxy performance, latency, error rates
- 🔐 TLS/SSL Termination: Handle encryption/decryption
- 🌍 IP Rotation: Change public IP addresses for scraping
- 🎯 Geo-targeting: Route requests through proxies in specific locations



## 🚀 Quick Start

## Installation

```bash
pip install proxycraft
```

Or with uv:

```bash
uv add proxycraft
```

### Basic Usage

```python
from proxycraft import ProxyCraft

if __name__ == "__main__":
    proxycraft: ProxyCraft = ProxyCraft(config_file='proxy.json')
    proxycraft.serve(host='0.0.0.0', port=8091)
```

📋 Configuration Example

```json

{
  "version": "1.0",
  "name": "Simple example",
  "endpoints": [
    {
      "prefix": "/",
      "match": "**/*",
      "backends": {
        "https": {
          "url": "https://jsonplaceholder.typicode.com/posts"
        }
      },
      "upstream": {
        "proxy": {
          "enabled": true
        }
      }
    }
  ]
}
```




## 🐳 Docker Usage


```bash
docker build -t proxycraft -f dockerfiles/proxycraft.Dockerfile .
docker run  -p 8080:8080 proxycraft
```

## Project structure

```text
proxycraft/
├── app/              # ASGI application composition root
├── features/         # Capability-owned modules (routing, backends, middleware, …)
└── shared/           # Cross-cutting infrastructure (logging, connection pooling)
```

See [docs/architecture.md](docs/architecture.md) and [SPECS.md](SPECS.md) for details.

## Development

Install [just](https://github.com/casey/just) and [uv](https://docs.astral.sh/uv/), then:

```bash
just install
just test
just lint
```

Build a release (requires `VERSION`):

```bash
VERSION=1.0.0 just build
```

Run a subset of tests:

```bash
just test tests/path/to/test_file.py
```

List all available commands:

```bash
just
```

## 📄 License

[MIT](LICENSE)
