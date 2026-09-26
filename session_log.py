"""
Local storage for completed focus sessions, plus a helper to roll them up
into per-day totals for the chart. Stored as JSON next to this file.
"""

import datetime
import json
import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "sessions.json")


def _load():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH) as f:
            return json.load(f)
    return []


def _save(sessions):
    with open(LOG_PATH, "w") as f:
        json.dump(sessions, f, indent=2)


def record_session(minutes):
    sessions = _load()
    sessions.append({
        "date": datetime.date.today().isoformat(),
        "minutes": minutes,
    })
    _save(sessions)


def last_n_days(n):
    sessions = _load()
    today = datetime.date.today()
    totals = {}
    for i in range(n):
        day = today - datetime.timedelta(days=n - 1 - i)
        totals[day.isoformat()] = 0

    for s in sessions:
        if s["date"] in totals:
            totals[s["date"]] += s["minutes"]

    return [
        (datetime.date.fromisoformat(d).strftime("%a"), minutes)
        for d, minutes in totals.items()
    ]
