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

## Step 1 — Intake (ALWAYS ask first)

Before pulling any data, ask the user this intake. **Start by asking which client the report is
for**, then collect the month's work so you can paste it straight into the report:

1. **Which client is this for?** (client name — map it to the exact `clients/<slug>/` folder,
   case-sensitive, from the active-clients list in `CLAUDE.md`) + confirm **city, ST**, **website**,
   and the **report month** (e.g. "May 2026").
2. **Blogs** — paste the blog post **titles + links** completed this month.
3. **Treatment pages** — paste the **links** to any treatment/service pages added this month.
4. **Backlinks** — ask the user to **paste the client's backlink sheet** (the live tracking
   spreadsheet — paste its link and/or the rows). Use it to count the backlinks built this month
   and to set the "View Backlinks Sheet" button link in the report.
5. **Technical updates** — paste any technical SEO work done this month.
6. (If not obvious) the **Semrush project** name and the **GA4 property / Google Business Profile**
   so Windsor pulls hit the right account.

Whatever the user pastes is what goes into the **"What We've Done This Month"** cards verbatim
(titles linked to the URLs they gave). Drop any card with nothing to report this month.

Confirm the client already has a folder under `clients/<slug>/`. If there's no folder, ask before
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

## Step 4 — Add the month card to the client's folder index

Each client has their **own folder** with a landing page (`clients/<slug>/index.html`) that
**lists every month as a card** (newest first) — e.g. https://reports.dentistnerds.com/clients/smile-tustin/.
The dated report file lives **in that same folder**, and you add a new card linking to it.

1. The report file is already at `clients/<slug>/<month>-<year>.html` (from Step 3).
2. Open `clients/<slug>/index.html` and **prepend** a new card to the top of `<div class="grid">`
   (newest month first), using the existing card markup in that file. Pattern:

   ```html
   <a target="_blank" href="<month>-<year>.html" class="card">
     <div class="card-icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18"/><path d="M8 4v4"/><path d="M16 4v4"/></svg></div>
     <div><div class="card-name"><Month Year></div><div class="card-tag">Monthly Report</div></div>
   </a>
   ```

   (e.g. `href="june-2026.html"` and `card-name` = `June 2026`.) Don't touch the other cards or
   the rest of the page.

3. The clients hub `clients/index.html` lists clients (not individual months) — only edit it if
   this client has no card there yet.

---

## Step 5 — Publish (the report MUST go live)

The report is not done until it's **live on the site under the correct client**. Push to `main`
(GitHub Pages serves `main`):

```
git add -A
git fetch origin main && git rebase origin/main   # remote moves often — always rebase first
git commit -m "Add <Month Year> monthly report — <Client Name>"
git push -u origin main
```

After pushing, confirm both URLs resolve to the new month and give them to the user:
- Report: `https://reports.dentistnerds.com/clients/<slug>/<month>-<year>.html`
- Latest:  `https://reports.dentistnerds.com/clients/<slug>/`
- Hub:     `https://reports.dentistnerds.com/clients/` (the client's card links the new report)

---

## Guardrails
- Real data only — no placeholder/sample numbers, no map reused across clients.
- Final report has zero `contenteditable`.
- Confirm before spending Local Falcon scan credits; reuse a recent scan when one exists.
- "Building" status = dropped >12 positions OR not ranking well.
- Keep the blue/Anton Dentist Nerds branding from `reports/report-example/index.html`.
