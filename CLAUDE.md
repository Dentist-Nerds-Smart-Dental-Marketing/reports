# Dentist Nerds — Reports Repository
# Connected to: Dentist-Nerds-Smart-Dental-Marketing/reports

## What This Repo Is

Published SEO reports for all Dentist Nerds clients. Two report types:

- **`clients/`** — Monthly performance reports (`april-2026.html`, `may-2026.html`)
  - One folder per active client (e.g. `clients/westgrove-dental-care/`)
  - Each folder has an `index.html` (latest) + monthly snapshots
- **`reports/`** — One-time SEO audit reports (older format)
  - One folder per client, typically one `index.html` inside

## File Structure

```
reports/                                 ← repo root
├── clients/                             ← monthly performance reports
│   ├── index.html                       ← client listing page
│   └── <client-slug>/
│       ├── index.html                   ← latest report (symlink or copy)
│       ├── april-2026.html
│       └── may-2026.html
├── reports/                             ← SEO audit reports (legacy)
│   ├── index.html
│   └── <client-slug>/
│       └── index.html
├── index.html                           ← site root
└── robots.txt
```

## Active Clients (clients/ folder)

all-smiles-dental-studio, av-dental-wellness-group, beverly-hIlls-cosmetic-dentistry,
cameron-park-family-dentistry, canyon-country-dental-care, elite-dentistry,
exceptional-dentistry, foothill-ranch-dentistry, fullerton-smile-dentistry,
gardena-dental-group, malibu-dentistry, oc-perio-implants-dental-group,
pennsylvania-perio--implants, perio-implants-health-pro, san-juan-family-dentistry,
seren-advanced-dentistry-oxnard, smile-spa-camarillo, smile-tustin,
the-smile-spa, Torrance-Dental-Spa, valencia-aesthetic-dentistry,
west-hollywood-dental-studio, westgrove-dental-care, woodland-hills-family-dentistry

## Workflow

### Adding a New Monthly Report
1. Generate report in `seo-skill-set` project (see `C:\Users\renat\seo-skill-set`)
2. Copy finished HTML to `clients/<client-slug>/may-2026.html`
3. Update `clients/<client-slug>/index.html` to point to new month
4. Commit and push

### Pushing Changes
```powershell
cd C:\Users\renat\reports
git add .
git commit -m "Add May 2026 report — <client-name>"
git push
```

## Preview

Reports are served at: https://dentist-nerds-smart-dental-marketing.github.io/reports/

Local preview (optional):
```powershell
npx serve -l 3333 "C:\Users\renat\reports"
```

## Key Rules

- Never edit `index.html` files manually — they are auto-generated listing pages
- Monthly report filenames: `<month>-<year>.html` (e.g. `may-2026.html`)
- Client slug must match existing folder name exactly (case-sensitive)
- Always push to `main` branch

## Related Project

Report generation lives in `C:\Users\renat\seo-skill-set` — see that project's CLAUDE.md
for the full report-generator skill and workflow.

## Git Remote

```
origin  https://github.com/Dentist-Nerds-Smart-Dental-Marketing/reports.git
```
