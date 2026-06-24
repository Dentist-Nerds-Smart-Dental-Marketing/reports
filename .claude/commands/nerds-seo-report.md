---
description: Generate a Dentist Nerds SEO audit & growth report for a client from live Semrush + Local Falcon data
argument-hint: <practice name> | <website> | <city, ST> [| keyword to scan]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__Semrush_MCP_Server__*, mcp__Local_Falcon__*, mcp__Windsor_ai__*
---

# Nerds SEO Report

Generate a branded **Dentist Nerds — SEO Audit & Growth Report** for a client and publish it.

## Inputs

Parse `$ARGUMENTS` (pipe- or comma-separated). Expected fields, in order:

1. **Practice name** — e.g. `Westgrove Dental Care`
2. **Website** — e.g. `westgrovedental.com`
3. **Market** — e.g. `Pasadena, CA`
4. **Keyword to scan** *(optional)* — the term for the Google Maps / Local Falcon grid, e.g. `dentist near me`. If omitted, default to `dentist <city>`.

If any of the first three are missing, **ask the user** for them before continuing — do not guess the domain or city.

Derive the **client slug** from the practice name: lowercase, spaces → hyphens, strip punctuation (e.g. `Westgrove Dental Care` → `westgrove-dental-care`). Match an existing folder in `reports/` exactly if one already exists.

## Step 1 — Pull live data

Use the connected MCP servers. **Always call the tools — never invent numbers.** Default the Semrush database to `us`.

Pull for the client's domain:

- **Search Visibility** (Semrush organic/overview): organic monthly traffic, total ranking keywords, (note AI visibility as an estimate if not directly available).
- **Authority & Backlinks** (Semrush backlinks): total backlinks, Authority/Domain score, toxic/spam %.
- **Keyword gap** (Semrush): keywords the site has content/pages for but ranks poorly (page 2+ or unranked). Capture keyword, the page it lives on, monthly search volume, current rank. Pick the 5 highest-volume.
- **Local competition** (Semrush): 3 nearby competitors and each one's ranking-keyword count, for the comparison bars.
- **Traffic sources** (Semrush .Trends / Windsor GA4 if available): Direct / GBP / Organic / Referral / Paid mix.
- **Google Maps** (Local Falcon): run/read a grid scan for the chosen keyword; capture each cell's rank, the average rank, and % of grid where the practice is visible.

If a specific metric can't be retrieved, leave the template's placeholder and tell the user which fields need manual entry — don't fabricate.

## Step 2 — Build the report from the template

1. Read `reports/report-example/index.html` — this is the **canonical template**. Do NOT edit the template itself.
2. Copy it to `reports/<client-slug>/index.html` (create the folder).
3. Fill in the real values:
   - **Hero**: practice name (`[Practice Name]`), website, market, report date (today), and the meta-grid blocks (Prepared For, Report Date, Issues Found, Recommendation).
   - **Health Score**: overall score + the 4 pillar percentages (Content Quality, UX, AI Search/AEO, Local Search).
   - **Search Visibility** dials: Monthly Traffic, Ranking Keywords, AI Visibility — set each `data-value`/`data-max` and the flag.
   - **Authority & Backlinks** dials: Total Backlinks, Domain Authority, Toxic %.
   - **Top 3 Weaknesses** + the "other issues" list — write from the actual findings.
   - **Keyword gap** table — the 5 keywords with page, volume, rank (use `rk` red / `rk warn` amber).
   - **Local Competition** bars — set each `width:%` relative to the top competitor and the numbers.
   - **Google Maps**: the "Keyword scanned" chip, the 5×5 grid `seed`/`ranks` arrays in the script, average rank, and % visible.
   - **Traffic** stack: the channel percentages and bar widths.
   - Tailor the **Game Plan** copy (Step 01 + engines) to the client where relevant.
4. Keep all branding, fonts, and interactive JS intact.

## Step 3 — Add to the listing

Add a card for the new report near the top of `reports/index.html` grid, following the existing `<a class="card">` pattern, linking to `/reports/<client-slug>/`.

## Step 4 — Publish

- Commit on `main` with message: `Add SEO report — <Practice Name>`.
- Push with `git push -u origin main` (rebase onto `origin/main` first if it has moved).
- Report the live URL: `https://reports.dentistnerds.com/reports/<client-slug>/`.

## Notes

- The report is fully click-to-edit, so leave anything uncertain as a sensible placeholder and flag it for the user to finalize.
- The template lives at `reports/report-example/` — keep it as the master copy and always generate fresh client reports from it.
