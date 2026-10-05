# /// script
# requires-python = ">=3.12"
# dependencies = ["icalendar==7.3.0", "recurring-ical-events==3.8.2"]
# ///
"""Print the upcoming events from an iCal feed as JSON for index.html."""

import html
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

LOCAL_TZ = ZoneInfo("America/Denver")
LOOKAHEAD = timedelta(days=365)
MAX_EVENTS = 200


def load_calendar(source):
    if source.startswith("http"):
        with urllib.request.urlopen(source, timeout=30) as resp:
            return icalendar.Calendar.from_ical(resp.read())
    with open(source, "rb") as f:
        return icalendar.Calendar.from_ical(f.read())


def plain_text(description):
    """Google Calendar stores descriptions edited on the web as HTML."""
    def anchor(m):
        href, label = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        return href if label in ("", href) else f"{label} {href}"

    text = re.sub(r'<a\b[^>]*href="([^"]*)"[^>]*>(.*?)</a>', anchor, description, flags=re.I | re.S)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</li>", "\n", text, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def iso_start(start):
    if not isinstance(start, datetime):
        return start.isoformat()
    # Floating times carry no zone; the team calendar is in Utah.
    return (start if start.tzinfo else start.replace(tzinfo=LOCAL_TZ)).isoformat()


def to_event(component):
    start = component.decoded("DTSTART")
    return {
        "summary": str(component.get("SUMMARY", "")),
        "location": str(component.get("LOCATION", "")),
        "description": plain_text(str(component.get("DESCRIPTION", ""))),
        "start": iso_start(start),
        "allDay": not isinstance(start, datetime),
    }


def upcoming(calendar, now):
    occurrences = recurring_ical_events.of(calendar).between(now, now + LOOKAHEAD)
    return sorted(map(to_event, occurrences), key=lambda e: e["start"])[:MAX_EVENTS]


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else os.environ["ICS_URL"]
    json.dump(upcoming(load_calendar(source), datetime.now(LOCAL_TZ)), sys.stdout, indent=1)
