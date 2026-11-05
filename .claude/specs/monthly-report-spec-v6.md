# Monthly Organic SEO Report — Generation Spec v6

Source of truth: Google Doc "Monthly Organic SEO Report — Generation Spec v6 (ALL CLIENTS)"
<https://docs.google.com/document/d/1ib9wZKEN-MH-zI8E8YUj79qxKOjoGwGWncka1jyKTBY/edit>
Transcribed into the repo 2026-11-05 so the agents can read it without a Drive call.
If the doc and this file disagree, the doc wins — re-sync this file.

THIS SPEC APPLIES TO EVERY ACTIVE CLIENT. Nothing in sections 0–9 is specific to one
client. Client-specific handling lives in APPENDIX A and only there.

Build one HTML report per client per month and publish it to
`clients/<slug>/<month>-<year>.html`.

Every figure comes from a live tool call. Never ship a placeholder, an estimate, a number
carried from last month, or a map copied from another client. If a source cannot be
reached, say so internally — do not invent, and do not silently drop a section from the
client's page.

---

## 0. TARGETING — CITY FOR RANKINGS, US FOR TRAFFIC

City level ONLY for the Semrush keyword table and the Local Falcon grid. GA4 and GSC are
scoped to the United States. NEVER report all countries.

| Source | Scope |
|---|---|
| Semrush | City campaign: "<City>, <State>, United States", city level, device desktop, engine Google |
| Local Falcon | Grid centred on the practice's own lat/lng |
| GA4 | Filter EVERY call to country = United States. NEVER a city filter. Windsor field id: `country` |
| GSC | Filter EVERY call to country = usa. GSC has NO city dimension. Windsor field id: `country` |

Name the level in each section's source line. e.g. "Source: Windsor / GA4 — organic
sessions, United States" or "Source: Windsor / Google Search Console — United States".

Keyword phrases are the local set: "<service> <city>", "<service> in <city>",
"<service> near me".

---

## 1. REPORT STRUCTURE — these sections, this order

1. Hero — month/year, practice name, city/ST, website, 4 KPIs
2. What We've Done This Month — the work cards that apply this month
3. Keyword Rankings — table + Search Console footprint block
4. Local Map Rankings — ONE Local Falcon grid
5. Traffic to Each Page — GA4 pages
6. Where Traffic Comes From — GA4 channel mix
7. Google Business Profile Performance — 4 stat cards + 6-month trend table
8. Footer — reporting period + data sources

Branding: Dentist Nerds blue `#0a6bff` + black + white, Anton + DM Sans, white logo.
The final file must contain ZERO `contenteditable` attributes.

---

## 2. WHERE EVERY NUMBER COMES FROM

### SEMRUSH — primary source for the keyword table (city level)

```
execute_report("list_projects")                    -> project_id (integer)
execute_report("campaigns", {project_id: <int>})   -> "<project>_<campaign>"
execute_report("tracking_position_organic", {campaign_id, url, date_begin, date_end})
```

- `project_id` must be an INTEGER; a string is refused.
- The campaign id is `"<project>_<campaign>"`. A bare project id fails with "campaign not found".
- Dates are YYYY-MM-DD. URL mask is `*.<domain>/*`
- Response shape: `data.data` keyed "0".."n". Per row: `Ph` = phrase, `Nq` = volume,
  `Be` = position at start date, `Fi` = position at end date, `Dt` = daily series.
  `"-"` means not in the top 100.
- Responses exceed the token limit — write to a file and parse it, do not read inline.

### GOOGLE ANALYTICS 4 — Windsor connector `googleanalytics4` (US level)

Account = the client's GA4 property ID. Call `get_fields` first; field IDs are snake_case.
EVERY GA4 call carries country = United States.

Any month-over-month or 6-month GA4 comparison RE-PULLS the earlier months with the same
country = United States filter. Reason: GA4 city is guessed from the visitor's IP, a large
share of sessions have no city, and nearby cities are real patients, so a city filter
undercounts local traffic. Earlier reports used US, so US keeps the series consistent.

Organic sessions (hero KPI) and channel mix:

```
fields  ["session_default_channel_group","sessions"]
filter  [["country","eq","United States"]]
```

Read the Organic Search row for the KPI; use all rows for the channel mix. Verify the
channel counts sum to the stated total before publishing.

Traffic to Each Page:

```
fields  ["page_path","sessions","screen_page_views"]
filter  [["session_default_channel_group","eq","Organic Search"],"and",["country","eq","United States"]]
```

**USE `page_path`. NEVER USE `landing_page`.** `landing_page` credits a session only to the
FIRST page of that session, so any page reached by navigation reads as zero. It makes the
homepage look like roughly 60% of all traffic and hides Contact Us, About Us and the
appointment page entirely. The section is titled "Traffic to Each Page", so it must count
traffic to each page.

Three more rules for this section:
- DROP the "(not set)" row. It means nothing to a client.
- Show the TOP 10 pages by sessions.
- If the client has a hostname filter listed in Appendix A, keep it.

Because one session can touch several pages, `page_path` figures DO NOT SUM to the monthly
session total. Say so in the source line under the list.

### GOOGLE SEARCH CONSOLE — Windsor connector `searchconsole` (US level)

Account = `sc-domain:<client-domain>`. EVERY GSC call carries the country filter.

Footprint block (every client):

```
total clicks + impressions:
  fields ["clicks","impressions"]
  filter [["country","eq","usa"]]

top-20 keyword count:
  fields ["query","position"]
  filter [["country","eq","usa"]]
  date range = full month, aggregated per query (NOT daily rows)
```

Count queries whose monthly average position is 20 or better. A position filter on daily
rows counts any query that touched the top 20 on a single day and inflates the number.

Keyword table (fallback clients only — see section 4):

```
fields ["query","impressions","clicks","position"]
filter [["query","in","[\"kw1\",\"kw2\"]"],"and",["country","eq","usa"]]
```

One call PER MONTH. Do not add `year_month_name` to a multi-month call — it returns per-day
rows instead of monthly aggregates. `position` is the impression-weighted average, so it
lands between whole numbers; render to one decimal.

Device split (the `device` field) is for diagnostics only — never on the client page.

### GOOGLE BUSINESS PROFILE — Windsor connector `google_my_business`

Account = `locations/<id>`. The profile is the location, so no geo filter applies.

```
fields ["year_month_name","impressions","impressions_desktop_search","impressions_mobile_search","impressions_desktop_maps","impressions_mobile_maps","website_clicks","call_clicks","direction_requests"]
```

- Search column = desktop_search + mobile_search
- Maps column = desktop_maps + mobile_maps
- VERIFY the split sums to `impressions` for every month before publishing.

Reviews:

```
fields ["review_total_count","review_average_rating_total","review_count","review_average_rating"]
```

`review_count` = new reviews in the period. `review_average_rating` = average OF THOSE NEW
REVIEWS, which can sit below the overall rating — if it does, the overall rating is dropping
and that should be reported.

**GBP RESTATEMENT — MANDATORY, EVERY CLIENT.** Google revises GBP figures for WEEKS after
month end. Always re-pull all six months fresh and publish the CURRENT values. Earlier rows
WILL differ from what those months' own reports printed. Observed example: one month first
read 442 impressions / 2 calls / 21 clicks / 82 directions, and six weeks later the same
month read 505 / 3 / 25 / 91.

Add a note under the table saying earlier months have been restated, and expect the current
month to rise too.

If the current month shows zero calls and clicks across its final days, that is reporting
lag, not a collapse. Say so rather than publishing a false decline.

### LOCAL FALCON (grid on the practice lat/lng)

```
listAllLocalFalconLocations(query)   -> place_id, lat, lng, rating, reviews
listLocalFalconScanReports(placeId, startDate, endDate, fieldmask)
getLocalFalconReport(reportKey, fieldmask)
```

Fieldmask for `listLocalFalconScanReports` — ONE unbroken line:

```
report_key,date,keyword,location.name,arp,atrp,solv,grid_size,platform
```

Fieldmask for `getLocalFalconReport` — ONE unbroken line:

```
report_key,date,keyword,lat,lng,grid_size,radius,measurement,arp,atrp,solv,found_in,data_points.*.lat,data_points.*.lng,data_points.*.rank
```

- ALWAYS pass the fieldmask — an unmasked report is 100–300KB and will blow the token limit.
- SCANS COST CREDITS. Reuse the month's existing scan. Never run a new one without explicit approval.
- `data_points` are COLUMN-MAJOR: all latitudes for the first longitude, then the next
  longitude. Build the {lat,lng,rank} array in that order or the heat map is wrong.
- `rank === false` means not ranking -> emit 0.
- Verify: an 11x11 grid is 121 points, and the count of non-zero ranks equals `found_in`.

### BLOGS

Fetch the client's live `/blog/` index and confirm each post is published.

### TREATMENT PAGES

Treatment and service pages added this month come from the team, with links. Confirm each
page is live on the site before listing it.

### BACKLINKS

The ONLY source is the client's backlink tracking sheet in Google Drive. Never take
backlinks from the OS, from a crawl, or from any other tool.

Before publishing, open the sheet link in a signed-out browser and confirm it loads WITHOUT
a sign-in (anyone with the link can view). If it asks for a login, keep the button in the
report and flag it internally so the sharing gets fixed. Do this for every client, every month.

### CHECKING THAT A LINK IS LIVE

Verify URLs return HTTP 200 before linking them, with one exception that matters: some sites
return 403 to scripts while working fine for real people. Reddit and Vitals both do this.
Open those in a browser before treating them as broken. Do not drop a real link because a
script got a 403.

---

## 3. WORK CARDS

The grid is two columns: `grid-template-columns: 1fr 1fr`. NO CARD SPANS TWO COLUMNS. Cards
in a row share equal height — do not add `align-items:start`.

THE CARD COUNT IS NOT FIXED. Show the cards that apply this month and DROP any card with
nothing to report. A month with no blogs and no technical work runs with two cards; a full
month runs with four or five. Four is common, not a rule.

| Card | Contents |
|---|---|
| Blog Content | every blog post published IN the report month, each linked, with date and category |
| Treatment Pages | treatment/service pages added this month, each linked — ITS OWN CARD, never merged into Blog Content |
| Backlinks Added | every link built in the month, linked, plus the "View Backlinks Sheet" button (MANDATORY) |
| Technical SEO | default label is "Maintenance" |
| Tracking & Reporting | which tools produced this report |

**BLOG CONTENT CARD.** Blogs only. Never fold treatment pages, backlinks or anything else
into it. If posts were written but are not live on the site, mark the card "On hold" with an
amber pill and explain why. Do not claim them as published.

**TREATMENT PAGES CARD.** Its own card, separate from Blog Content. List each page added
this month with its link. If no treatment pages were added, DROP THE CARD — do not show an
empty one, and do not merge it into another card.

**BACKLINKS CARD — THE ONE CARD THAT NEVER DROPS.** The most common failure is omitting this
card. Do not omit it.

- Source is the client's tracking sheet ONLY.
- The "View Backlinks Sheet" button is MANDATORY on every report.
- If genuinely zero links were built, keep the card and say so. This is the one card that
  stays even when empty.
- Filter rows to dates INSIDE the report month. A row dated the 3rd of the following month
  belongs to next month's report.
- Read EVERY TAB that holds links — Business Profile, Contextual Backlink, Local, Social
  Sharing, Image Sharing, Referencial Backlinks. Links are spread across tabs, not just the first.
- Count only rows with BOTH a date and a public link. Bare domain names with no date are the
  target list, not completed work.
- Check each URL is live (see the 403 note above).
- State status honestly: "Live", or "Submitted <date> · pending review" when the sheet shows none.
- NEVER present a nofollow link as ranking authority. Wikipedia, Reddit, most social profiles
  and most Q&A sites are nofollow. Label them: "builds visibility and referral traffic rather
  than ranking authority."

**TECHNICAL SEO CARD.** Default: show "Technical SEO — Maintenance" with the standard
maintenance wording. Change it ONLY when the team reports specific work worth telling the
client. NEVER invent work. If nobody told you what was done, the default stands.

**CARDS THAT MUST NOT APPEAR.** Do not invent a card for a metric you could not retrieve.
Specifically, do not add a "Google Business Profile Posts — Not available" card. A card whose
only content is a missing-data apology does not belong in a client deliverable. Report
connector failures to the internal team, not on the client's page.

---

## 4. KEYWORD RANKINGS

DEFAULT SOURCE FOR EVERY CLIENT: Semrush position tracking, that client's city campaign.
This is the correct source because it is the only one that can be scoped to the client's
CITY and to desktop. Search Console cannot be filtered below country level.

### MANDATORY VALIDATION BEFORE PUBLISHING SEMRUSH FIGURES

Run this for every client, every month. Count, for each of the last roughly ten days of the
month, how many tracked keywords have a recorded position. `"-"` means not in the top 100.

- Count stable (e.g. 11–12 of 14 every day) -> campaign healthy. PUBLISH IT.
- Count collapses (e.g. 10 of 14 -> 1 of 14) and does not fully recover -> campaign
  unreliable. DO NOT PUBLISH.

Keywords sitting at healthy positions do not all leave the top 100 on the same day. When a
campaign fails this check:

1. Cross-check the affected keywords against Search Console for the same month.
2. If Search Console shows them ranking while Semrush shows nothing, fall back to Search
   Console FOR THAT CLIENT, THAT MONTH ONLY.
3. Flag the campaign internally for repair, and add the client to Appendix A. Do not let a
   fallback become permanent without someone fixing Semrush.

### SEARCH CONSOLE FALLBACK — CAVEAT TO CARRY

Search Console blends all devices and, even filtered to usa, all US locations, so it is not
strictly comparable to a desktop/city Semrush campaign, and it breaks comparability with
prior months sourced from Semrush. Label the column "Avg. Position" rather than "Position".

### THE TABLE — EXACTLY FOUR COLUMNS

```
Search Phrase | Position (or Avg. Position on the fallback) | Change | Status
```

THERE IS NO "Searches/mo" COLUMN. It was removed deliberately. Do not reintroduce it.

### WHICH ROWS TO INCLUDE

- Sort by position, BEST FIRST. Never alphabetical.
- REMOVE a keyword if it dropped 1.0 position or more. (A keyword that slipped 0.2 stays —
  that is noise, not a decline.)
- Remove any keyword with no position at all.
- Mention material losses by name in the section intro prose if they matter — but keep them
  out of the table.

### NEW KEYWORDS (no position at the start of the month)

A keyword that was not ranking at the start of the month has no change to calculate. Semrush
shows `"-"` for the start date; Search Console simply has no earlier row. Do not guess and do
not leave the cell blank.

- Change = "New"
- Status = by its END position: top 20 -> Improving; outside the top 20 -> Building

### SAY HOW MANY OF HOW MANY

The section intro MUST state the count both ways: "X of the Y keywords we track". The table
shows X rows; the campaign tracks Y. Never write a sentence that implies the table holds all
tracked keywords when rows have been removed.

### STATUS AND COLOUR (no overlap)

- **Improving** — moved up 1.0 or more AND inside the top 20, or New and in top 20
- **Stable** — inside the top 20 AND moved less than 1.0 either way
- **Building** — outside the top 20

There is NO "Declining" status — those rows are removed, not labelled.

Rank pill colour: good = #1–3 · warn = #4–10 · bad = #11+

### FOOTPRINT BLOCK

Below the table, three Search Console stat cards, each with the month-over-month change:
Keywords in Google's Top 20 · Search Impressions · Clicks from Search. This block is Search
Console (US level) for EVERY client regardless of which source feeds the table above — it
measures the long tail a 14-keyword campaign cannot see.

---

## 5. LOCAL MAP RANKINGS — ONE MAP

- ONE GRID ONLY: "dentist in <city>". Do NOT publish a second "dentist near me" map — it was
  removed deliberately.
- Report ARP, Points Ranked (found_in / total), SoLV, grid size and scan date.
- Compare each figure to last month in the intro prose.
- Use the practice's real lat/lng for the blue office pin.

---

## 6. HERO KPIs

Four KPIs. Each covers the FULL report month, and each carries a sub-line stating the
comparison and the geographic level.

1. **Keywords in Google Top 20** — Search Console, UNITED STATES level
2. **Website Traffic / mo** — GA4 organic sessions, UNITED STATES level
3. **GBP Phone Calls** — the profile itself (or New Reviews when calls are unreliable that month)
4. **Review Rating** — average plus total review count

Any month-over-month figure in a KPI sub-line is RE-PULLED with the same filter as the
current month. For the GA4 traffic KPI that means re-pulling the prior month with
country = United States. Never take the comparison number from an earlier report.

Never use a domain-wide Semrush organic keyword total, and never a figure dated mid-month.
If the number does not cover the full report month, it is the wrong number.

---

## 7. TONE AND HONESTY

- REPORT DECLINES AS PLAINLY AS GAINS IN THE PROSE. Curating the keyword table is the
  standing instruction; misrepresenting the month is not. A month where the map coverage fell
  is a month where the map coverage fell.
- NEVER SAY "best month on record". The report shows six months, so the most you can claim is
  "best in the last six months". You do not have the record.
- NEVER PRESENT A DATA GAP AS A RESULT. Missing data is disclosed as missing data.
- DO NOT PUT INTERNAL DATA PROBLEMS ON THE CLIENT'S PAGE. No callouts explaining that a tool
  was wrong or that a source was swapped. Fix it, source it correctly, and name the source in
  the footer. Internal issues go to the team.
- Every narrative claim must trace to a number in the report.
- Do not invent "what we did" detail. If the team did not say what work happened, use the
  default wording and flag internally that specifics are needed.

---

## 8. PRE-PUBLISH CHECKLIST — run all of these, every client

- [ ] Zero `contenteditable` in the file
- [ ] Zero `[bracketed placeholders]` left
- [ ] HTML parses with no unclosed or mismatched tags
- [ ] Every card shown has something to report; empty cards dropped, EXCEPT Backlinks, which always stays
- [ ] No card spans two columns
- [ ] Blog Content holds blogs only; Treatment Pages is its own card
- [ ] Backlinks card present, sheet button present, sheet opens without sign-in
- [ ] Every blog and treatment page URL live (403 checked in a browser)
- [ ] Every GA4 call carries country = United States (no city filter); every GSC call carries country=usa
- [ ] GA4 comparison months re-pulled with country = United States, not copied from an earlier report
- [ ] Top-20 count uses monthly per-query average position, not daily rows
- [ ] Traffic to Each Page uses `page_path`, drops "(not set)", shows top 10
- [ ] Semrush daily-count validation run before any Semrush figure is published
- [ ] Keyword table has 4 columns, no Searches/mo, nothing that dropped 1.0+
- [ ] New keywords show Change "New" and Status by end position
- [ ] Keyword intro states "X of the Y keywords we track"
- [ ] Exactly 1 map card and 1 `renderMap(...)` call; 121 points for an 11x11 grid; non-zero rank count equals found_in
- [ ] GBP trend is 6 rows, and search + maps split sums to the total every month
- [ ] Channel-mix counts sum to the stated session total, percentages near 100
- [ ] No "best month on record" anywhere
- [ ] Appendix A checked for this client
- [ ] Renders at 1280px and 600px with no horizontal overflow and no JS errors
- [ ] No stale month name anywhere in the file
- [ ] Published file is byte-identical to the local file after deploy

---

## 9. PUBLISH

1. Write `clients/<slug>/<month>-<year>.html` — lowercase, e.g. `october-2026.html`
2. Prepend a card to the top of `<div class="grid">` in `clients/<slug>/index.html`, newest
   month first. Touch nothing else on that page.
3. Stage ONLY the two files you changed, commit with a message on the command line, then
   rebase and push. Never use `git add -A` — it sweeps up unrelated work. Never run a bare
   `git commit` — it opens an editor. Never rebase with files still staged — it refuses to run.

```
git add clients/<slug>/<month>-<year>.html clients/<slug>/index.html
git commit -m "<slug>: <Month> <Year> report"
git pull --rebase origin main
git push origin main
```

4. Confirm the URL returns 200 AND that the live file matches the local file before reporting
   the report as published.

---

## APPENDIX A — CLIENT-SPECIFIC EXCEPTIONS

Everything above applies to every client. These are the only exceptions. Check this list
before building any client's report. Remove an entry once the underlying issue is fixed.

### 2C WELLNESS DENTISTRY (dentistoflagunaniguel.com)
- Keyword source: SEARCH CONSOLE FALLBACK, not Semrush. Campaign `30348376_5100790` failed
  the section 4 validation in October 2026: it reported three of fourteen keywords, including
  "dentist in laguna niguel", as never reaching the top 100 all month, while Google showed
  them on page one. It agreed with Google on three keywords and diverged on eight, by as much
  as 46 positions, and was still returning only 5 of 14 keywords on 4 November. Remove this
  entry once the campaign passes validation again.
- Backlink sheet currently asks for a sign-in. Keep the button, flag it until the sharing is fixed.

### EXCEPTIONAL DENTISTRY
- Traffic to Each Page: keep the hostname filter for `palmdaleexceptionaldentistry.com`
