# /// script
# requires-python = ">=3.12"
# dependencies = ["icalendar==7.3.0", "recurring-ical-events==3.8.2"]
# ///
"""Print the upcoming timed events from an iCal feed as JSON for index.html."""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

LOCAL_TZ = ZoneInfo("America/Denver")
LOOKAHEAD = timedelta(days=60)
MAX_EVENTS = 30


def load_calendar(source):
    if source.startswith("http"):
        with urllib.request.urlopen(source, timeout=30) as resp:
            return icalendar.Calendar.from_ical(resp.read())
    with open(source, "rb") as f:
        return icalendar.Calendar.from_ical(f.read())


def to_event(component):
    start = component.decoded("DTSTART")
    return {
        "summary": str(component.get("SUMMARY", "")),
        "location": str(component.get("LOCATION", "")),
        "description": str(component.get("DESCRIPTION", "")),
        # Floating times carry no zone; the team calendar is in Utah.
        "start": (start if start.tzinfo else start.replace(tzinfo=LOCAL_TZ)).isoformat(),
    }


def upcoming(calendar, now):
    occurrences = recurring_ical_events.of(calendar).between(now, now + LOOKAHEAD)
    timed = [c for c in occurrences if isinstance(c.decoded("DTSTART"), datetime)]
    return sorted(map(to_event, timed), key=lambda e: e["start"])[:MAX_EVENTS]


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else os.environ["ICS_URL"]
    json.dump(upcoming(load_calendar(source), datetime.now(LOCAL_TZ)), sys.stdout, indent=1)
