# Reiterhof Georg — Website

A responsive website for a family-run equestrian centre in Hofheim am Taunus, Germany.

**Live website:** https://reiterhof-georg.de/

The site presents the boarding stable, riding school, horse and rider training,
and the people and countryside around the farm. Its visual design uses cream,
beige and brown tones, original photography, and a responsive six-page navigation.

## Implementation

- A small static-site generator written in Python, using only the standard library.
- Shared page templates, navigation and footer maintained in one place.
- HTML and CSS with a small JavaScript mobile menu.
- A local development server with automatic rebuilding and browser reload.
- Locally served assets; no frontend framework, analytics scripts or embedded widgets.

## Run locally

Requires Python 3.10 or newer. No package installation is needed.

```sh
python3 dev.py
```

Open http://127.0.0.1:8080. To generate the static files without starting a server:

```sh
python3 build.py
```

The generated site is written to `dist/` (ignored by Git). Local builds contain
`noindex` metadata and a restrictive robots.txt, and are intended for development.

## Source layout

| File | Purpose |
| --- | --- |
| `build.py` | Page content, shared templates and static build |
| `dev.py` | Local preview with automatic reload |
| `src/site.css` | Responsive styling and image crops |
| `src/site.js` | Mobile navigation |
| `src/datenschutz.html` | Website privacy notice |
| `src/images/` | Photography used by the site |

This repository is a periodically updated portfolio snapshot. Hosting credentials,
production deployment configuration and internal project documents are not included.
It does not deploy the live website.

## Content and photographs

This repository is published for inspection as a portfolio project. No open-source
license is granted by this publication. Photographs, branding and website copy are
not offered for reuse; obtain permission from the relevant rights holders.
