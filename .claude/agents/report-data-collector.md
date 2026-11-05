---
name: report-data-collector
description: Pulls one client's real monthly SEO data for a spec-v6 report (Semrush city campaign, Local Falcon, Windsor GA4/GBP/GSC at US level, backlink sheet, blogs) and writes a structured JSON packet. Use during the monthly report run, one instance per client.
tools: '*'   # inherit every tool: the collector needs Semrush, Local Falcon, Windsor, Google
             # Drive and OneUp MCP tools, and an explicit allowlist silently hides whichever
             # are omitted — including from ToolSearch. The *builder* keeps a restricted list
             # on purpose; this agent must not.
model: sonnet
---

# Monthly report — data collector (SPEC v6)

**READ `.claude/specs/monthly-report-spec-v6.md` IN FULL BEFORE YOU START.** It is the source of
truth. This file tells you what to put in the packet; the spec tells you what each number means
and how it must be queried. Where they disagree, the spec wins.

You collect **one client's** data for **one month** and write it to a JSON packet.
You never write report HTML and never touch `clients/<slug>/*.html`.

## Inputs
`slug`, `name`, `city`, `state`, `website`, `ids`, `report_month` (e.g. `2026-10`), `out_path`.

## Hard rules

1. **Every number comes from a live tool call.** If a tool fails or a connector is unauthorized,
   write `null` plus an `_error` string for that field. Never estimate, never carry a number from
   another client or another month, never invent. A null is a correct answer; a plausible guess
   is a defect that ships to a client.
2. **Geography is not optional** (spec §0). Semrush = the client's CITY campaign, desktop.
   Local Falcon = grid on the practice's own lat/lng. **Every** GA4 call carries
   `["country","eq","United States"]`. **Every** GSC call carries `["country","eq","United States"]`
   too — the doc says `"usa"`, but Windsor stores the full country name and `"usa"` returns
   `total_rows: 0`. Verified 2026-11-05.
   Never a city filter on GA4. Never all-countries on either.
3. **Local Falcon costs credits.** `listLocalFalconScanReports` first, reuse the month's scan,
   and never run a new scan without explicit approval recorded in `_cost_notes`.
4. Big responses (Semrush tracking, unmasked Local Falcon) blow the token limit — write to a file
   and parse it. Always pass the spec's fieldmasks.
5. **Collectors run in parallel and share a scratchpad.** Put every intermediate file under a
   directory named for your slug, and never use a generic filename like `semrush.json` — a
   dry run had one collector read another client's data off a colliding path. If a file you did
   not write appears where you expected yours, stop and re-derive from your own tool results.
6. **Backlink sheets:** `mcp__Google_Drive__read_file_content` returns only ~10 sample rows per
   tab, and a `text/csv` export returns only the FIRST tab. To see every row you must export the
   whole workbook as xlsx (`exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)
   and parse it. When `.cache/<month>/v6/backlinks-october.json` exists, use it instead — it was
   extracted centrally and carries no credentials.

## What to collect

### A. Semrush — keyword table source (city level)
- Resolve `list_projects` -> `campaigns` -> `"<project>_<campaign>"`. `project_id` must be an
  INTEGER. A bare project id fails with "campaign not found".
- `tracking_position_organic` for the full month. Per row: `Ph` phrase, `Be` position at start,
  `Fi` position at end, `Dt` daily series. `"-"` = not in top 100.
- **RUN BOTH VALIDATION TESTS (spec §4) AND RECORD THEM.** Test A is the daily count. Test B is
  the Search Console cross-check — a keyword pinned at `"-"` every day is "stable" to the count
  test, so Test A alone misses a broken campaign. Put the per-keyword Semrush-vs-GSC comparison in
  `semrush.validation.gsc_crosscheck_avg_position`. Either test failing means unreliable. For each of the last ~10 days of the
  month, count how many tracked keywords have a position. Put the daily counts in
  `semrush.validation.daily_counts` and set `semrush.validation.verdict` to `"healthy"` or
  `"unreliable"`, with `reason`. A count that collapses (10 of 14 -> 1 of 14) and does not
  recover means DO NOT PUBLISH these figures: set the verdict to `unreliable`, fall back to
  Search Console for the keyword table for this client this month only, and say so loudly in
  `_errors` so the client gets added to Appendix A.
- Emit `semrush.keywords_all`: every tracked keyword with `phrase`, `position_start`,
  `position_end`, `change` (start − end; positive = improved), `is_new` (no start position).
- Emit `semrush.tracked_total` — the Y in "X of the Y keywords we track".
- **Do NOT emit a status of "Declining".** It does not exist in v6. Statuses are only
  Improving / Stable / Building, defined in spec §4.
- **Do NOT collect search volume for the table.** There is no Searches/mo column in v6.

### B. Local Falcon — ONE grid only (spec §5)
`dentist in <city>`. Do **not** collect a second "dentist near me" grid; it was removed.
Emit ARP, `found_in`, SoLV, grid size, radius, scan date, office lat/lng, and the full per-point
array as a flat `[{lat,lng,rank}]` list in the order returned (**column-major — do not re-sort**).
`rank === false` -> `0`. Verify the non-zero count equals `found_in` and record that you did.
Also pull **last month's** ARP / points ranked / SoLV for the same keyword so the builder can
compare in prose.

### C. Windsor — GA4 (`googleanalytics4`), US level
- Channel mix + organic sessions:
  `fields ["session_default_channel_group","sessions"]`, `filter [["country","eq","United States"]]`.
  Record every channel row and the total; confirm the rows sum to the total.
- Traffic to Each Page:
  `fields ["page_path","sessions","screen_page_views"]`,
  `filter [["session_default_channel_group","eq","Organic Search"],"and",["country","eq","United States"]]`.
  **`page_path`, never `landing_page`** — see the spec for why. Drop the `(not set)` row. Emit the
  top 10 by sessions. Record in `top_pages_note` that page figures do not sum to the session total.
- **Re-pull the prior month with the same US filter** for the KPI sub-line. Never take the
  comparison figure from an earlier report.

### D. Windsor — Search Console (`searchconsole`), US level
Account is `sc-domain:<domain>`. Needed for **every** client, because the footprint block and
hero KPI 1 both come from here.
- `clicks` + `impressions` for the month, and again for the prior month.
- Top-20 count: `fields ["query","position"]`, month aggregated **per query** (not daily rows);
  count queries whose monthly average position is <= 20. Do the same for the prior month.
- If the client has no GSC property, set these null with an `_error` — do not substitute a
  Semrush number.

### E. Windsor — Google Business Profile (`google_my_business`)
Account `locations/<id>`; no geo filter.
- **RE-PULL ALL SIX MONTHS FRESH, EVERY RUN (spec §2, mandatory).** Google restates GBP figures
  for weeks. Publish current values; earlier rows will differ from what those months' own reports
  printed. Set `gbp.restated: true`.
- Fields per the spec, including the four impression splits. **Verify
  desktop_search + mobile_search + desktop_maps + mobile_maps == impressions for every month**
  and record the result in `gbp.split_verified`.
- Reviews: total count, overall average, new reviews this month and their average.
- If the final days of the month show zero calls/clicks, flag `gbp.reporting_lag: true` — that is
  lag, not a collapse.

### F. Backlinks — the client's own tracking sheet ONLY
Look the sheet up in `.cache/<month>/backlink-sheets.json` (slug -> file id + view url).
Read **every tab that holds links**, not just the first. Count only rows with BOTH a date and a
public link; bare domains with no date are a target list, not completed work. Keep only rows
dated inside the report month. Record for each: url, date, tab, and whether it is nofollow
(Wikipedia, Reddit, most social profiles and Q&A sites are). **Do NOT emit `backlinks.sheet_url`.** The "View Backlinks Sheet" button is HELD (spec §3,
decision 2026-11-05) because this reports site is public and the sheets carry live credentials.
Set `backlinks.sheet_url: null` and `backlinks.sheet_withheld_reason` to a short explanation.
Never copy a username, email or password into the packet, a scratch file, or your report back. **Never source backlinks from Semrush, a crawl, or anywhere else.**

### G. Blogs, treatment pages, technical SEO
- Blogs: fetch the live `/blog/` index and confirm each post is published. Record title, url,
  date and category. `[]` means a verified zero; `null` means the fetch failed — say which.
- Treatment pages: only what the team supplied. Nothing supplied -> `[]` (the card drops).
- Technical SEO: only what the team reported. Nothing reported -> `null` (the builder uses the
  default Maintenance wording). Never invent work.

## Output
Write JSON to `out_path`, then reply with a short summary: client, fields populated, fields
nulled, and the Semrush validation verdict. Schema:

```json
{ "slug": "...", "report_month": "2026-10", "collected_at": "<iso8601>", "spec_version": 6,
  "ids_resolved": {},
  "semrush": {"tracked_total": 0, "keywords_all": [], "validation": {}},
  "local_falcon": {"map": {}, "prior_month": {}},
  "windsor": {"ga4": {}, "gsc": {}, "gbp": {}},
  "backlinks": {"sheet_url": "", "links": []},
  "blogs": [], "treatment_pages": [], "technical_seo": null,
  "_cost_notes": [], "_errors": [] }
```
