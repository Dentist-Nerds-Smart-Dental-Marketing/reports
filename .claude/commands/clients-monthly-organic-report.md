---
description: Generate a monthly organic SEO performance report for a Dentist Nerds client (Semrush + Local Falcon + Windsor), build from the template, and publish to the clients hub.
---

# Clients Monthly Organic Report

You generate a **monthly performance report** for an existing Dentist Nerds client and
publish it to the `clients/` section of this repo. This is the recurring "here's what we did
and how you're doing this month" report — **different from** the one-time SEO audit
(`/nerds-seo-report`).

- **Theme/style:** matches `reports/report-example/index.html` (Dentist Nerds blue `#0a6bff` +
  black + white, Anton + DM Sans, white logo). DO NOT use the old navy/gold Playfair design.
- **Master template:** `clients/report-template.html` — copy it, fill it, never edit the master.
- **Final deliverable:** non-editable HTML (no `contenteditable` anywhere).
- **Data is always real.** Never ship placeholder numbers or a map copied from another client.
  Every figure comes from a live tool call below.

---

## Step 1 — Get the client basics

Ask the user (one short prompt) for:
1. **Client name** + **city, ST** + **website**
2. **Report month** (e.g. "May 2026")
3. The **Semrush project** name (for position tracking) and the **Google Business Profile /
   GA4 property** if not obvious — needed for Windsor pulls.
4. The month's **work done**: blogs (titles + URLs), backlinks added (#), treatment pages added
   (titles + URLs), technical SEO summary, and the backlinks tracking-sheet link.

Confirm the client already has a folder under `clients/<slug>/`. The slug must match exactly
(case-sensitive) — see the active-clients list in `CLAUDE.md`. If there's no folder, ask before
creating one.

---

## Step 2 — Pull the real data

Call the tools — do not answer from memory. Default Semrush database to `us`.

### A. Semrush — keyword position tracking (the keyword table + "Keywords Ranking" KPI)
- Use `mcp__Semrush_MCP_Server__tracking_research` / `projects_research` to get the client's
  tracked keywords with **current position, previous position, and search volume**.
- Also get domain-wide **organic keyword count** (`organic_research` / `overview_research`) for
  the hero "Keywords Ranking" KPI.
- **Status rule (important):** mark a keyword **"Building"** if it **dropped more than 12
  positions** month-over-month **OR** it isn't ranking well (not in the top ~20 / no position).
  Otherwise: **"Improving"** if it moved up meaningfully, else **"Stable"**.
- Rank pill color: `good` = #1–3, `warn` = #4–10, `bad` = #11+/none.

### B. Local Falcon — local map grids (TWO maps)
Run a scan for **`dentist in <city>`** AND **`dentist near me`**.
- `searchForLocalFalconBusinessLocation` → `saveLocalFalconBusinessLocationToAccount`
  (required before a scan or you'll get "location not saved").
- `runLocalFalconScan` — **scans cost credits; confirm with the user before running.** If a
  recent scan for this keyword already exists, reuse it via `listLocalFalconScanReports` +
  `getLocalFalconReport` instead of paying again.
- Pull each report's **ARP, points ranked, SoLV, grid size**, and the **per-point grid**
  (`data_points` with rank + lat + lng). Remember data_points are **column-major**; build the
  `{lat,lng,rank}` array for the template's `renderMap(...)` calls. Capture the **office
  lat/lng** for the blue pin.

### C. Windsor — GA4, Google Business Profile, Search Console
Use `mcp__Windsor_ai__get_data` (connectors: `googleanalytics4`, `googlemybusiness`,
`googlesearchconsole`).
- **GA4:** organic **sessions this month** (hero "Website Traffic" KPI), **top pages by organic
  sessions** (Traffic to Each Page), and **sessions by default channel group** (Traffic Sources —
  Organic Search / Direct / Referral / Organic Social / Paid, with % and counts).
- **Google Business Profile:** **phone calls, website clicks, direction requests, searches/
  impressions (Search + Maps)** for this month **and the prior 5 months** (the 6-month trend
  table), plus **review count + average rating** and **new reviews this month**.

If a specific Windsor connector isn't authorized, tell the user which one to connect rather than
inventing numbers.

---

## Step 3 — Build the report

1. Copy `clients/report-template.html` → `clients/<slug>/<month>-<year>.html`
   (e.g. `clients/smile-tustin/may-2026.html`, lowercase month-year).
2. Fill every `[bracketed placeholder]`:
   - Hero: month/year, practice name, city/ST, website, and the 4 KPIs
     (Keywords Ranking, Website Traffic/mo, GBP Phone Calls, Review rating + count).
   - **What We've Done This Month:** blogs (titles + links), backlinks added (#) + sheet link,
     treatment pages added (titles + links), technical SEO summary, tracking. Drop any work
     card that doesn't apply this month.
   - **Keyword Rankings table:** one row per tracked keyword — phrase, position pill (color by
     rank), month-over-month change (▲/▼), searches/mo, and status (Stable / Improving /
     **Building** per the rule above).
   - **Local Map Rankings:** fill both `map-stats` blocks and paste the real `{lat,lng,rank}`
     arrays + office lat/lng into the two `renderMap(...)` calls. Map 1 = `dentist in <city>`,
     Map 2 = `dentist near me`.
   - **Traffic to Each Page:** top organic pages with visit counts; bar widths relative to the
     top page.
   - **Where Traffic Comes From:** stacked-bar widths + legend (% and session counts) from GA4
     channel groups; total sessions.
   - **GBP Performance:** the 4 at-a-glance stat cards + the 6-month trend table (last row =
     this month, bolded).
   - Footer: reporting period.
3. **Verify:** no `[` placeholders left, no `contenteditable`, both maps have real data points,
   every number traces to a Step-2 tool call. The two maps MUST differ (different keyword data).

---

## Step 4 — Update the client's index + the hub

1. Point `clients/<slug>/index.html` at the new month (it's the "latest" pointer — copy the new
   file's contents over it, or update its redirect, matching how that folder already works).
2. Add/refresh the client's card on the clients hub `clients/index.html` so the latest month is
   linked. (Don't hand-edit unrelated auto-generated listing markup — just the one card.)

---

## Step 5 — Publish

```
git add -A
git fetch origin main && git rebase origin/main   # remote moves often — always rebase first
git commit -m "Add <Month Year> monthly report — <Client Name>"
git push -u origin main
```

Then give the user the live link:
`https://reports.dentistnerds.com/clients/<slug>/<month>-<year>.html`

---

## Guardrails
- Real data only — no placeholder/sample numbers, no map reused across clients.
- Final report has zero `contenteditable`.
- Confirm before spending Local Falcon scan credits; reuse a recent scan when one exists.
- "Building" status = dropped >12 positions OR not ranking well.
- Keep the blue/Anton Dentist Nerds branding from `reports/report-example/index.html`.
