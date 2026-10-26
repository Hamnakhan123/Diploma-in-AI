"""
Session 8 · Real-life problem: scraping a paginated product catalogue
---------------------------------------------------------------------
PROBLEM
A small business wants to track a competitor's catalogue (here: the local
practice site). Write a scraper that
  1. starts at page 1 and follows the "Next" link until there is none,
  2. extracts id, name, category, price, rating and stock status from each card,
  3. CLEANS the messy prices ("Rs 1,499", "Rs. 4,200", "PKR 2,350") into integers,
  4. saves everything to products.csv,
  5. prints category statistics and draws a chart.
It must respect robots.txt and wait between requests.
Run:  python session-08_problem_catalogue_scraper.py
"""
import csv
import re
import time
from urllib import robotparser
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from demo_shop_site import start_site

BASE = start_site()
session = requests.Session()
session.headers["User-Agent"] = "DiplomaAI-StudentBot/1.0"

rp = robotparser.RobotFileParser()
rp.parse(session.get(BASE + "/robots.txt", timeout=10).text.splitlines())

def clean_price(text):
    """'Rs. 4,200' -> 4200. Raises ValueError if no number is present."""
    digits = re.sub(r"[^\d]", "", text)
    if not digits:
        raise ValueError(f"no price in {text!r}")
    return int(digits)

def parse_card(card):
    """Extract one product dict from a <div class="product">."""
    return {
        "id": int(card["data-id"]),
        "name": card.select_one(".name").get_text(strip=True),
        "category": card["data-category"],
        "price": clean_price(card.select_one(".price").text),
        "rating": float(card.select_one(".rating")["title"].split()[0]),
        "in_stock": "in" in card.select_one(".stock")["class"],
        "url": urljoin(BASE, card.select_one(".name a")["href"]).replace(BASE, ""),
    }

products, url, pages = [], BASE + "/products?page=1", 0
while url:
    if not rp.can_fetch(session.headers["User-Agent"], url):
        print("robots.txt blocks", url); break
    soup = BeautifulSoup(session.get(url, timeout=10).text, "html.parser")
    pages += 1
    for card in soup.select("div.product"):
        try:
            products.append(parse_card(card))
        except (ValueError, KeyError, AttributeError) as e:      # one bad card never stops the crawl
            print("  skipped a card:", e)
    nxt = soup.select_one("a.next")
    url = urljoin(url, nxt["href"]) if nxt else None              # relative -> absolute link
    time.sleep(0.2)                                               # be polite (shortened for the demo)

print(f"scraped {len(products)} products from {pages} pages")
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(products[0]))
    w.writeheader(); w.writerows(products)
print("saved products.csv; first rows:")
for p in products[:3]:
    print("  ", p)

print(f"\n{'Category':<12} {'Items':>5} {'Avg price':>10} {'Cheapest':>9} {'In stock':>8}")
cats = sorted({p["category"] for p in products})
avg = {}
for c in cats:
    group = [p for p in products if p["category"] == c]
    avg[c] = sum(p["price"] for p in group) / len(group)
    print(f"{c:<12} {len(group):>5} {avg[c]:>10,.0f} {min(p['price'] for p in group):>9,} "
          f"{sum(p['in_stock'] for p in group):>4}/{len(group)}")
best = max(products, key=lambda p: (p["rating"], -p["price"]))
print(f"\nBest rated: {best['name']} ({best['rating']}★, Rs {best['price']:,})")
print("Out of stock:", [p["name"] for p in products if not p["in_stock"]])

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7, 3.6))
colours = {"accessories": "#FF6B1A", "displays": "#A78BFA", "audio": "#F43F5E", "storage": "#FCD34D"}
for p in products:
    ax.scatter(p["price"], p["rating"], color=colours[p["category"]], s=60,
               marker="o" if p["in_stock"] else "x")
for c, col in colours.items():
    ax.scatter([], [], color=col, label=c)
ax.set_xscale("log"); ax.set_xlabel("Price (Rs, log scale)"); ax.set_ylabel("Rating")
ax.set_title("Scraped catalogue: price vs rating (x = out of stock)"); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig("session-08_problem_catalogue_scraper.png", dpi=110)
print("Chart saved: session-08_problem_catalogue_scraper.png")
