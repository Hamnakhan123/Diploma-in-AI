"""
Session 8 · Example 2: parsing HTML with BeautifulSoup
------------------------------------------------------
Run:  python session-08_bs4_parsing.py
"""
import requests
from bs4 import BeautifulSoup
from demo_shop_site import start_site

BASE = start_site()
html = requests.get(BASE + "/", timeout=10).text
soup = BeautifulSoup(html, "html.parser")        # or "lxml" (faster, needs the lxml package)

# 1. Simple access by tag name
print("title tag:", soup.title, "| text:", soup.title.string)
print("first <h1>:", soup.h1.get_text(), "| its class:", soup.h1["class"])

# 2. find (first match) and find_all (all matches), filtering by attributes
intro = soup.find("p", id="intro")
print("get_text(strip=True):     ", intro.get_text(strip=True))        # pieces glued together!
print("get_text(' ', strip=True):", intro.get_text(" ", strip=True), "| bold word:", intro.b.text)
links = soup.find_all("a")
print("number of links:", len(links))
for a in links:
    print(f"  {a.get_text():<14} -> {a['href']:<28} rel={a.get('rel')}")

# 3. CSS selectors with select / select_one (same syntax as in CSS files)
print("nav links:", [a.text for a in soup.select("nav a")])
print("external links:", [a["href"] for a in soup.select('a[href^="http"]')])
print("footer text:", soup.select_one("footer p").text)

# 4. Turning an HTML table into Python data
table = soup.find("table", id="deals")
rows = []
for tr in table.find_all("tr")[1:]:                       # skip the header row
    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
    rows.append(cells)
headers = [th.text for th in table.find_all("th")]
print("\ntable headers:", headers)
for item, old, new in rows:
    to_int = lambda t: int(t.replace("Rs", "").replace(",", "").strip())
    saving = to_int(old) - to_int(new)
    print(f"  {item:<18} saves Rs {saving:,} ({saving / to_int(old):.0%})")

# 5. Navigating the tree: parent, children, siblings
first_td = soup.find("td")
print("\nfirst <td>:", first_td.text, "| parent tag:", first_td.parent.name,
      "| next sibling:", first_td.find_next_sibling("td").text)
print("children of <nav>:", [c.name for c in soup.nav.children if c.name])

# 6. Product cards: data attributes and nested elements on another page
page = BeautifulSoup(requests.get(BASE + "/products?page=1", timeout=10).text, "html.parser")
for card in page.select("div.product")[:3]:
    print(f"  id={card['data-id']} cat={card['data-category']:<12} "
          f"{card.select_one('.name').get_text(strip=True):<22} {card.select_one('.price').text:<10} "
          f"{card.select_one('.stock').text}")

# 7. Missing elements return None: guard before using them
missing = page.select_one(".discount")
print("missing element ->", missing, "| safe text:", missing.text if missing else "n/a")
