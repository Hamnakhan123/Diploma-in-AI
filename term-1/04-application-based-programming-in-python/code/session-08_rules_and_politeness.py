"""
Session 8 · Example 3: the rules of scraping - robots.txt, rate limits, caching
-------------------------------------------------------------------------------
Run:  python session-08_rules_and_politeness.py
"""
import time
from urllib import robotparser
import requests
from demo_shop_site import start_site

BASE = start_site()
AGENT = "DiplomaAI-StudentBot/1.0"

# 1. Read robots.txt: the site's instructions for automated visitors
robots_txt = requests.get(BASE + "/robots.txt", timeout=10).text
print("robots.txt says:\n" + robots_txt)
rp = robotparser.RobotFileParser()
rp.parse(robots_txt.splitlines())
for path in ["/products?page=1", "/jobs", "/admin", "/cart"]:
    print(f"  may fetch {path:<18}? {rp.can_fetch(AGENT, BASE + path)}")
delay = rp.crawl_delay(AGENT) or 1
print("requested crawl delay:", delay, "second(s)")

# 2. A polite fetcher: checks robots.txt, waits between requests, caches pages
class PoliteFetcher:
    def __init__(self, robots, delay, agent):
        self.robots, self.delay, self.last = robots, delay, 0.0
        self.session = requests.Session()
        self.session.headers["User-Agent"] = agent
        self.cache, self.requests_made = {}, 0

    def get(self, url):
        if not self.robots.can_fetch(self.session.headers["User-Agent"], url):
            raise PermissionError(f"robots.txt disallows {url}")
        if url in self.cache:                       # never download the same page twice
            return self.cache[url]
        wait = self.delay - (time.monotonic() - self.last)
        if wait > 0:
            time.sleep(wait)                        # rate limiting
        resp = self.session.get(url, timeout=10)
        self.last = time.monotonic()
        self.requests_made += 1
        resp.raise_for_status()
        self.cache[url] = resp.text
        return resp.text

fetcher = PoliteFetcher(rp, delay=0.5, agent=AGENT)    # 0.5 s here to keep the demo short
start = time.monotonic()
for url in [BASE + "/products?page=1", BASE + "/products?page=2", BASE + "/products?page=1", BASE + "/admin"]:
    try:
        fetcher.get(url)
        print(f"  fetched {url.replace(BASE, ''):<18} (network requests so far: {fetcher.requests_made})")
    except PermissionError as e:
        print("  refused:", str(e).replace(BASE, ""))
elapsed = time.monotonic() - start
print(f"3 page loads, {fetcher.requests_made} real requests, spaced out: {'yes' if elapsed >= 0.5 else 'no'}")

# 3. A checklist to run before every scraping project
checklist = [
    "Is there an official API or a downloadable dataset? Use it instead.",
    "Do the Terms of Service allow automated access?",
    "Does robots.txt allow the pages you need?",
    "Are you collecting personal data? (names, phones, emails -> privacy law applies)",
    "Is the data copyrighted? Store facts, not whole articles or images.",
    "Identify yourself (User-Agent), rate-limit, cache, and scrape off-peak.",
]
print("\nBefore you scrape:")
for i, item in enumerate(checklist, 1):
    print(f"  {i}. {item}")
