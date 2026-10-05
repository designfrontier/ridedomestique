# Ride Domestique site

Single-page static site. Edit `index.html` and commit; GitHub Pages redeploys automatically.

- Ride card descriptions and tags: edit the cards in `index.html`
- Calendar: rides come from the public Google Calendar (`CAL_ID` in `index.html`, `ICS_URL` in `.github/workflows/deploy.yml`); the workflow rebuilds `events.json` hourly
  - The next 4 timed events show as ride cards, soonest first; "zwift" in the title or location marks a ride Virtual
  - Events with "race", "crit" or "criterium" in the title appear under Upcoming races (all-day is fine)
  - The event's Location is shown as the start address, linked to Google Maps
  - Pills come from a `Tags: No-drop, Social pace` line in the description; virtual rides also get a Virtual pill
  - The first URL in the event description becomes the card's button or the race's Details link
  - The rest of a ride's description (lines without links) is shown on its card, e.g. "Lights required: front and rear"
- Domain: the `CNAME` file holds `ridedomestique.com`
