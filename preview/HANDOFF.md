# Stephie's World — Handoff

## Structure
- `World_A.html` — landing constellation. 9 orbs link to chapter pages.
- Chapter pages (each with its own unique layout):
  - `About.html` — editorial diary
  - `Reading.html` — book spines + open-book spreads + library card catalogue
  - `Art.html` — gallery wall + dark film strip + museum feature
  - `Cities.html` — horizontal postcard scroll
    - `Paris_Guide.html` — field-guide (museums / cafés / walks / address)
    - `NewYork_Guide.html` — field-guide with stylized SVG map
  - `Ideas.html` — centered essay with pull-quotes
  - `Projects.html` — alternating case files with status chips + side meta
  - `Career.html` — CV timeline (year column, connecting line)
  - `Tennis.html` — court diagram + scorecard + kit specs
  - `Curiosities.html` — cabinet of curiosities + Substack feature
  - `Music.html` — React/Babel mini-app (source in `src/App.jsx`)
- Shared styles: `src/site.css`
- Music app: `src/App.jsx`

## Aesthetic (do not change)
- `--paper` `#faf4ee`, `--paper-warm` `#f5ead8`, `--blush` `#e8c5bd`
- `--ember` `#c2453a` (accent), `--ink` `#2a1a18`, `--ink-soft` `#4a3834`, `--ink-mute` `#8a6e66`
- Serif: Cormorant Garamond, italic-forward
- Mono: JetBrains Mono, uppercase-spaced for labels
- Centerpiece: heart (❦). Cycle options live in Tweaks panel — can be removed in production.

## TODO for Claude Code
1. **Copy:** replace placeholder prose on all pages with Stephie's real content. Pull from her existing site where possible.
2. **Favorites (Reading):** expand Favorites grid — currently only 3 cards; she has more.
3. **Cities copy:** verbatim from original site, not my rewrites.
4. **Maps:** NYC and Paris guides have stylized SVG maps. Improve by tracing real OSM coastlines/rivers, or swap in a Leaflet map with a paper-toned tile style. Keep the numbered-pin concept tied to list entries.
5. **Images:** placeholder gradients in Art gallery wall + film strip. Replace with real art / film stills.
6. **Curiosities cabinet:** 9 placeholder entries. Replace with her real curiosities.
7. **Deploy:** static site, `vercel --prod` from project root.
8. **Cleanup:** remove the Tweaks panel from World_A.html for production (search for `#tweaks` and `__edit_mode_available`).

## Known quirks
- File links use capitalized names (e.g. `About.html`). Make sure server is case-sensitive-safe.
- `localStorage` key `sw-crest` stores the chosen centerpiece — can ignore / reset.
- Music.html uses inline React + Babel Standalone (dev build, pinned).
