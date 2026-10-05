# Ride Domestique site

Single-page static site. Edit `index.html` and commit; GitHub Pages redeploys automatically.

- Ride and race details: edit the cards in `index.html`
- Calendar: rides come from the public Google Calendar (`CAL_ID` in `index.html`, `ICS_URL` in `.github/workflows/deploy.yml`); the workflow rebuilds `events.json` hourly
- Domain: the `CNAME` file holds `ridedomestique.com`
