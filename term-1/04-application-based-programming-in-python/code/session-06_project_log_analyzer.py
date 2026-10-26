"""
Session 6 · Mini project: web-server log analyzer
-------------------------------------------------
Web servers write one line per request in the "combined log format":
  IP - - [day/Mon/year:hh:mm:ss zone] "METHOD /path HTTP/1.1" status bytes "referrer" "agent"
This project parses access_sample.log with ONE verbose regex using named
groups, then reports traffic per hour, status codes, top pages, and flags
IPs with repeated failed logins (a simple security check).
Run:  python session-06_project_log_analyzer.py
"""
import re
from collections import Counter, defaultdict

LINE = re.compile(r"""
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})        # client IP address
    \s-\s-\s
    \[(?P<day>\d{2})/(?P<mon>\w{3})/(?P<year>\d{4}):(?P<hour>\d{2}):\d{2}:\d{2}\s[+-]\d{4}\]
    \s"(?P<method>[A-Z]+)\s(?P<path>\S+)\sHTTP/[\d.]+"
    \s(?P<status>\d{3})\s(?P<size>\d+|-)
    \s"[^"]*"\s"(?P<agent>[^"]*)"$
""", re.VERBOSE)

records, rejected = [], []
with open("access_sample.log", encoding="utf-8") as f:
    for n, line in enumerate(f, 1):
        m = LINE.match(line.strip())
        if m:
            records.append(m.groupdict())
        else:
            rejected.append(n)

print(f"parsed {len(records)} requests, could not parse line(s) {rejected}")
print("first record:", records[0])

status = Counter(r["status"] for r in records)
print("\nstatus codes:", dict(sorted(status.items())))
errors = sum(c for s, c in status.items() if s[0] in "45")
print(f"error rate: {errors / len(records):.0%}")

pages = Counter(re.sub(r"\?.*", "", r["path"]) for r in records if r["method"] == "GET")
print("top pages:", pages.most_common(3))

total_bytes = sum(int(r["size"]) for r in records if r["size"] != "-")
print(f"data served: {total_bytes / 1024:.1f} KB")

failed = defaultdict(int)
for r in records:
    if r["path"] == "/login" and r["status"] == "401":
        failed[r["ip"]] += 1
agent_of = {r["ip"]: r["agent"] for r in records}       # last agent seen per IP
for ip, count in failed.items():
    if count >= 3:
        print(f"SECURITY: {ip} had {count} failed logins (agent {agent_of[ip]})")

hours = Counter(int(r["hour"]) for r in records)
print("requests per hour:", dict(sorted(hours.items())))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
hs = list(range(9, 15))
a1.bar([f"{h}:00" for h in hs], [hours.get(h, 0) for h in hs], color="#FF6B1A")
a1.set_title("Requests per hour"); a1.tick_params(axis="x", rotation=45)
codes = sorted(status)
colours = {"2": "#FF6B1A", "3": "#FCD34D", "4": "#F43F5E", "5": "#A78BFA"}
a2.bar(codes, [status[c] for c in codes], color=[colours[c[0]] for c in codes])
a2.set_title("Responses by status code")
fig.tight_layout(); fig.savefig("session-06_project_log_analyzer.png", dpi=110)
print("Chart saved: session-06_project_log_analyzer.png")
