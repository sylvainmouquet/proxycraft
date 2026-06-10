# Virtual upstream

Resolves requests by trying multiple configured source endpoints until one returns HTTP 200 (`first-match` strategy).

**Key module:** `resolver.py` — `handle_request(...)`
