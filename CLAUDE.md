# CLAUDE.md

## Project structure

Single-page static site. Edit `index.html` and commit; GitHub Pages redeploys automatically.

### Key directories

None — the site is flat, with everything at the repo root.

### Key files
- `index.html` — the whole site: inline CSS, ride/race cards, and an inline script that pulls upcoming events from a public Google Calendar (`CAL_ID` / `API_KEY`) to fill the "Next rides" cards and subscribe links
- `CNAME` — GitHub Pages custom domain (`ridedomestique.com`)
- `README.md` — short editing guide for ride/race content, calendar setup, and domain
