"""
demo_shop_site: a tiny, fake website for practising web scraping SAFELY (Session 8).

It runs on your own computer (127.0.0.1) in a background thread, so the scraping
examples never touch a real company's server and always give the same output.

    from demo_shop_site import start_site
    base = start_site()          # e.g. 'http://127.0.0.1:54321'
"""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PRODUCTS = [
    # id, name, category, price text (deliberately messy), rating, in stock
    (1, "Wireless Mouse", "accessories", "Rs 1,499", 4.3, True),
    (2, "Mechanical Keyboard", "accessories", "Rs 6,850", 4.7, True),
    (3, "USB-C Hub 7-in-1", "accessories", "Rs. 4,200", 4.1, False),
    (4, "27-inch Monitor", "displays", "Rs 58,999", 4.6, True),
    (5, "Laptop Stand", "accessories", "PKR 2,350", 4.0, True),
    (6, "Noise-cancelling Headphones", "audio", "Rs 18,500", 4.8, True),
    (7, "Bluetooth Speaker", "audio", "Rs 7,999", 3.9, False),
    (8, "1080p Webcam", "accessories", "Rs 5,600", 4.2, True),
    (9, "Portable SSD 1TB", "storage", "Rs 21,750", 4.9, True),
    (10, "32GB USB Drive", "storage", "Rs 1,150", 4.4, True),
    (11, "Graphics Tablet", "accessories", "Rs 12,400", 4.5, True),
    (12, "24-inch Monitor", "displays", "Rs 36,500", 4.3, False),
]
PER_PAGE = 5
JOBS = [
    {"id": "J101", "title": "Junior Data Analyst", "company": "Indus Analytics", "city": "Karachi", "posted": "2026-10-20"},
    {"id": "J102", "title": "Python Developer (Flask)", "company": "Clifton Tech", "city": "Karachi", "posted": "2026-10-21"},
    {"id": "J103", "title": "Machine Learning Intern", "company": "Margalla AI", "city": "Islamabad", "posted": "2026-10-22"},
    {"id": "J104", "title": "Lab Engineer (Computer Science)", "company": "City University", "city": "Karachi", "posted": "2026-10-23"},
    {"id": "J105", "title": "Data Entry Operator", "company": "Port Logistics", "city": "Karachi", "posted": "2026-10-24"},
]
STATE = {"jobs_visible": 3}          # the job page 'grows' when the test calls add_jobs()

def _page(title, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title></head>
<body><header><h1 class="site-title">TechBazaar Demo</h1>
<nav><a href="/">Home</a> <a href="/products?page=1">Products</a> <a href="/jobs">Jobs</a></nav></header>
<main>{body}</main><footer><p>Practice site for scraping lessons. Not a real shop.</p></footer></body></html>"""

def _product_card(p):
    pid, name, cat, price, rating, stock = p
    badge = '<span class="stock in">In stock</span>' if stock else '<span class="stock out">Out of stock</span>'
    return f"""<div class="product" data-id="{pid}" data-category="{cat}">
  <h2 class="name"><a href="/product/{pid}">{name}</a></h2>
  <p class="price">{price}</p><p class="rating" title="{rating} out of 5">★ {rating}</p>{badge}
</div>"""

def _render(path, query):
    if path == "/robots.txt":
        return "text/plain", "User-agent: *\nDisallow: /admin\nDisallow: /cart\nCrawl-delay: 1\n"
    if path == "/":
        return "text/html", _page("Home", """<p id="intro">Welcome! Today's <b>deals</b> are below.</p>
<table id="deals"><tr><th>Item</th><th>Old price</th><th>New price</th></tr>
<tr><td>Wireless Mouse</td><td>Rs 1,899</td><td>Rs 1,499</td></tr>
<tr><td>Portable SSD 1TB</td><td>Rs 24,000</td><td>Rs 21,750</td></tr>
<tr><td>32GB USB Drive</td><td>Rs 1,400</td><td>Rs 1,150</td></tr></table>
<ul class="links"><li><a href="/products?page=1">All products</a></li><li><a href="/jobs">Careers</a></li>
<li><a href="https://example.com/partner" rel="nofollow">Partner site</a></li></ul>""")
    if path == "/products":
        page = int(query.get("page", "1"))
        chunk = PRODUCTS[(page - 1) * PER_PAGE: page * PER_PAGE]
        if not chunk:
            return None
        pages = -(-len(PRODUCTS) // PER_PAGE)
        nxt = f'<a class="next" href="/products?page={page + 1}">Next &raquo;</a>' if page < pages else ""
        cards = "\n".join(_product_card(p) for p in chunk)
        return "text/html", _page(f"Products page {page}", f'<div id="catalogue">{cards}</div><p class="pager">Page {page} of {pages} {nxt}</p>')
    if path.startswith("/product/"):
        pid = int(path.rsplit("/", 1)[1])
        for p in PRODUCTS:
            if p[0] == pid:
                return "text/html", _page(p[1], _product_card(p) + f'<p class="desc">Model TB-{pid:03d}. One-year warranty.</p>')
        return None
    if path == "/api/products.json":
        return "application/json", json.dumps([{"id": p[0], "name": p[1], "category": p[2]} for p in PRODUCTS])
    if path == "/jobs":
        rows = "".join(f'<li class="job" id="{j["id"]}"><h3>{j["title"]}</h3><span class="company">{j["company"]}</span>'
                       f' - <span class="city">{j["city"]}</span> <time datetime="{j["posted"]}">{j["posted"]}</time></li>'
                       for j in JOBS[:STATE["jobs_visible"]])
        return "text/html", _page("Jobs", f'<ul id="jobs">{rows}</ul>')
    if path == "/slow":                       # used to demonstrate timeouts
        import time
        time.sleep(2)
        return "text/plain", "finally!"
    if path in ("/admin", "/cart"):
        return "text/html", _page("Private", "<p>Private area.</p>")
    return None

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlsplit, parse_qsl
        parts = urlsplit(self.path)
        result = _render(parts.path, dict(parse_qsl(parts.query)))
        if result is None:
            self.send_response(404); self.send_header("Content-Type", "text/html"); self.end_headers()
            try:
                self.wfile.write(b"<h1>404 Not Found</h1>")
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        ctype, body = result
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", f"{ctype}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass                         # the client gave up waiting (e.g. the timeout demo)
    def log_message(self, *args):        # keep the console quiet
        pass

_SERVER = {}

def start_site():
    """Start the demo site once (port chosen by the OS) and return its base URL."""
    if "url" not in _SERVER:
        # Make sure requests talks to our local server directly, even if the
        # computer is configured to send web traffic through a proxy.
        for var in ("NO_PROXY", "no_proxy"):
            current = os.environ.get(var, "")
            if "127.0.0.1" not in current:
                os.environ[var] = ",".join(x for x in (current, "127.0.0.1", "localhost") if x)
        srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        _SERVER.update(url=f"http://127.0.0.1:{srv.server_address[1]}", srv=srv)
    return _SERVER["url"]

def add_jobs(n=2):
    """Simulate new vacancies appearing on the jobs page."""
    STATE["jobs_visible"] = min(len(JOBS), STATE["jobs_visible"] + n)

def reset_jobs():
    STATE["jobs_visible"] = 3

if __name__ == "__main__":
    import time
    print("Demo site running at", start_site(), "- press Ctrl+C to stop")
    while True:
        time.sleep(1)
