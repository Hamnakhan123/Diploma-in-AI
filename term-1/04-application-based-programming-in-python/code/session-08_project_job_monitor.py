"""
Session 8 · Mini project: a job-vacancy monitor with change detection
---------------------------------------------------------------------
Every day a graduate checks a careers page for new jobs. This tool automates it:
  1. scrape the jobs page (title, company, city, posted date, job id),
  2. keep only jobs matching keywords and a city,
  3. compare with the previous run's snapshot (jobs_snapshot.json),
  4. report NEW and REMOVED vacancies, then save the new snapshot.
The demo runs the monitor twice; between the runs the practice site
publishes two more vacancies, just like a real site would over a day.
Run:  python session-08_project_job_monitor.py
"""
import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import demo_shop_site as site

SNAPSHOT = "jobs_snapshot.json"
KEYWORDS = ["data", "python", "machine learning", "lab engineer"]
CITY = "Karachi"

def scrape_jobs(base):
    """Return a list of job dicts from the /jobs page."""
    html = requests.get(base + "/jobs", headers={"User-Agent": "DiplomaAI-StudentBot/1.0"}, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for li in soup.select("ul#jobs li.job"):
        jobs.append({
            "id": li["id"],
            "title": li.h3.get_text(strip=True),
            "company": li.select_one(".company").text,
            "city": li.select_one(".city").text,
            "posted": li.time["datetime"],
        })
    return jobs

def matches(job):
    title = job["title"].lower()
    return job["city"] == CITY and any(k in title for k in KEYWORDS)

def load_snapshot():
    try:
        with open(SNAPSHOT, encoding="utf-8") as f:
            return {j["id"]: j for j in json.load(f)["jobs"]}
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return {}

def save_snapshot(jobs, when):
    with open(SNAPSHOT, "w", encoding="utf-8") as f:
        json.dump({"checked_at": when, "jobs": jobs}, f, indent=2)

def run_monitor(base, when):
    print(f"--- check at {when} ---")
    all_jobs = scrape_jobs(base)
    relevant = [j for j in all_jobs if matches(j)]
    old = load_snapshot()
    new_ids = {j["id"] for j in relevant} - set(old)
    gone_ids = set(old) - {j["id"] for j in relevant}
    print(f"page lists {len(all_jobs)} jobs, {len(relevant)} match {KEYWORDS} in {CITY}")
    if not old:
        print("first run: saving a baseline snapshot")
    for j in relevant:
        if j["id"] in new_ids and old:
            print(f"  NEW   {j['id']} {j['title']} @ {j['company']} (posted {j['posted']})")
    for jid in sorted(gone_ids):
        print(f"  GONE  {jid} {old[jid]['title']}")
    if old and not new_ids and not gone_ids:
        print("  no changes")
    save_snapshot(relevant, when)
    return relevant

if os.path.exists(SNAPSHOT):
    os.remove(SNAPSHOT)                       # start fresh for a reproducible demo
site.reset_jobs()
BASE = site.start_site()

first = run_monitor(BASE, "2026-10-22 09:00")
for j in first:
    print(f"  baseline {j['id']} {j['title']}")
site.add_jobs(2)                              # the site publishes two more vacancies
second = run_monitor(BASE, "2026-10-24 09:00")
third = run_monitor(BASE, "2026-10-25 09:00")

print("\nSnapshot file now holds:", [j["id"] for j in json.load(open(SNAPSHOT, encoding="utf-8"))["jobs"]])
os.remove(SNAPSHOT)
