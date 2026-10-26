"""
Session 8 · Example 1: fetching pages with the requests library
---------------------------------------------------------------
Uses the local practice site from demo_shop_site.py, so nothing real is hit.
Run:  python session-08_requests_basics.py
"""
import requests
from demo_shop_site import start_site

BASE = start_site()
HEADERS = {"User-Agent": "DiplomaAI-StudentBot/1.0 (learning project; contact: lecturer@example.edu)"}

# 1. A basic GET request
r = requests.get(BASE + "/", headers=HEADERS, timeout=10)    # ALWAYS set a timeout
print("status:", r.status_code, r.reason, "| ok:", r.ok)
print("content type:", r.headers["Content-Type"], "| encoding:", r.encoding)
print("bytes:", len(r.content), "| first 60 chars of text:", r.text[:60].replace("\n", " "))

# 2. Query parameters: requests builds and encodes the query string
r = requests.get(BASE + "/products", params={"page": 2}, headers=HEADERS, timeout=10)
print("\nfinal URL:", r.url.replace(BASE, "BASE"), "| status:", r.status_code)

# 3. JSON endpoints: .json() parses the body for you
items = requests.get(BASE + "/api/products.json", headers=HEADERS, timeout=10).json()
print("API returned", len(items), "products; first:", items[0])

# 4. Handling errors: check status, catch network exceptions
for path in ["/products?page=9", "/no-such-page"]:
    r = requests.get(BASE + path, headers=HEADERS, timeout=10)
    try:
        r.raise_for_status()                 # raises HTTPError for 4xx/5xx
    except requests.HTTPError as e:
        print(f"HTTPError for {path}: {e.response.status_code}")

try:
    requests.get("http://127.0.0.1:1/", timeout=2)       # nothing listens on port 1
except requests.ConnectionError:
    print("ConnectionError: server unreachable (handled, no crash)")
try:
    requests.get(BASE + "/slow", timeout=0.5)            # this page needs 2 s to answer
except requests.Timeout:
    print("Timeout: the server took too long (handled)")

# 5. A Session reuses the connection and default headers (faster, politer)
with requests.Session() as s:
    s.headers.update(HEADERS)
    sizes = [len(s.get(f"{BASE}/products", params={"page": p}, timeout=10).text) for p in (1, 2, 3)]
print("\npage sizes with one Session:", sizes)

# 6. What the server saw as our identity
print("our User-Agent:", HEADERS["User-Agent"])
