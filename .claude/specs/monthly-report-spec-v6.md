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
| GSC | Filter EVERY call to country = United States. GSC has NO city dimension. Windsor field id: `country` |

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

> **CORRECTION TO THE DOC (verified 2026-11-05).** The doc says to filter GSC with
> `["country","eq","usa"]`. Windsor's Search Console connector stores the country as the full
> name, so `"usa"` matches nothing and the call returns `total_rows: 0` — checked directly
> against `sc-domain:westgrovedentalcare.com` for October 2026. Use
> `["country","eq","United States"]`, the same value GA4 takes. The intent of the doc is
> unchanged: US-only, never all countries. Fix the source doc and delete this note.

Footprint block (every client):

```
total clicks + impressions:
  fields ["clicks","impressions"]
  filter [["country","eq","United States"]]

top-20 keyword count:
  fields ["query","position"]
  filter [["country","eq","United States"]]
  date range = full month, aggregated per query (NOT daily rows)
```

Count queries whose monthly average position is 20 or better. A position filter on daily
rows counts any query that touched the top 20 on a single day and inflates the number.

Keyword table (fallback clients only — see section 4):

```
fields ["query","impressions","clicks","position"]
filter [["query","in","[\"kw1\",\"kw2\"]"],"and",["country","eq","United States"]]
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
- A month often holds MORE THAN ONE scan for the same keyword (e.g. 6 Oct and 20 Oct). The doc
  does not say which to take: **use the latest scan inside the report month**, and show its real
  date. Use the latest scan inside the prior month for the comparison. `listLocalFalconScanReports`
  is paginated, so a prior-month lookup may need the `next_token` page.
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

> **BUTTON HELD — decision by Amin, 2026-11-05. Overrides the "MANDATORY" wording below until
> lifted.** The doc assumes the sheet being readable without a sign-in is the desired state. It is
> not safe here: reports.dentistnerds.com is public and unauthenticated, and the backlink sheets
> carry Username / Email / Password columns beside the links. A sample of 10 of the 33 active
> clients found credentials in **all 10**, and 8 of those 10 are already shared
> `{"type":"anyone","role":"reader"}` — so linking them from a client report publishes working
> logins. The passwords also repeat across clients, so one exposed sheet reaches several
> practices. Malibu, Woodland Hills, All Smiles and The Smile Spa carry password values across
> 4–5 tabs each.
>
> Until the credential columns are stripped from the sheets and the reused passwords rotated:
> **render the Backlinks Added card in full — every October link, date and status — but DO NOT
> render the "View Backlinks Sheet" button and do not put the sheet URL anywhere in the HTML.**
> The card still never drops. Flag the held button in the internal run summary, never on the
> client's page. Restore the button in a follow-up pass once the sheets are clean.

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

- Count stable (e.g. 11–12 of 14 every day) -> campaign passes TEST A.
- Count collapses (e.g. 10 of 14 -> 1 of 14) and does not fully recover -> campaign
  unreliable. DO NOT PUBLISH.

### TEST B — THE COUNT TEST IS NOT ENOUGH (added 2026-11-05, from evidence)

A campaign can hold a perfectly steady count and still be wrong, because a keyword stuck at
`"-"` every single day is *stable*. California Coast Dental Arts passed Test A in October 2026
(10–11 of 14 every day) while reporting "dentist in oceanside", "dentist oceanside",
"oceanside dentist" and "dentist near me" as never reaching the top 100 all month — at the same
time Search Console put them at average positions 18.9, 15.4, 18.1 and 6.2, and Local Falcon had
"dentist in oceanside" ranked at 103 of 121 grid points. Three more terms were 20–30 places off.
That is the same failure as 2C Wellness, and the count test did not catch it.

So also run Test B, every client, every month: **cross-check the tracked terms against Search
Console for the same month**, and record the per-keyword comparison in the packet.

Weigh the evidence — do not trigger on a position gap alone. Search Console is an all-device,
US-wide average and Semrush is a desktop check at city level, so the two legitimately differ, and
the same caveat that makes the fallback imperfect makes a raw gap weak evidence.

**The decisive signal is a keyword Semrush reports as `"-"` for the WHOLE month while Search
Console shows it with a monthly average position of 20 or better.** Semrush is claiming the term
is not in the top 100 anywhere, which a national all-device average of, say, 18 contradicts
outright; geography cannot explain it away. Treat the campaign as unreliable when:

- two or more tracked keywords show that pattern, **or**
- one does and several further keywords sit 20+ places apart in the same direction, **or**
- **Local Falcon's own grid contradicts Semrush on the same head term.** This is the strongest
  evidence there is, because Local Falcon is already city-level and local, so the geography
  caveat cannot explain the gap away. Exceptional Dentistry in October 2026: Semrush put
  "dentist in palmdale" at #48 while Local Falcon had the practice ranked at all 121 grid
  points with an ARP of 3.59 and Search Console had "dentist palmdale" at an average of 3.1.
  Two independent sources, both disagreeing with Semrush in the same direction.

A single `"-"` keyword with everything else in reasonable agreement is worth a note in `_errors`,
not a fallback.

**"Near me" terms do not count toward the trigger.** Google personalises a "near me" result to
each searcher's location, so Search Console reports an average across many different local result
sets while a rank tracker checks from one fixed point. The two can disagree completely without
anything being wrong. Foothill Ranch in October 2026 failed the literal rule on exactly this —
"dentist near me" and "dental implants near me" read `"-"` all month against Search Console
averages of 9.5 and 7.8 — while every one of its other twelve keywords agreed with Search Console
to within about 14 places, Semrush was *better* than Search Console on the local terms
("dentist foothill ranch" 6 vs 15.4), and Local Falcon independently had the practice at ARP 2.43
across 121 of 121 points. That campaign is working. Judge Test B on terms that name a place. When the test does trigger, fall back to Search Console for that client that
month and add the client to Appendix A.

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
- [ ] Every GA4 call carries country = United States (no city filter); every GSC call carries country = United States
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

### CALIFORNIA COAST DENTAL ARTS (californiacoastdentalarts.com)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `30456032_5146101` passed
  the count test but failed Test B: four head terms read `"-"` all month while Search Console had
  them on page 1–2, and Local Falcon had "dentist in oceanside" on 103 of 121 points. Remove this
  entry once the campaign agrees with Google again.
- Open question for the team: Local Falcon's place record links GBP `locations/1402003271736985932`
  while the manifest carries `locations/7231815729630229678`. Confirm they are the same profile.

### LITTLETON DENTAL COLLECTIVE (littletondentalcollective.com)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `30604390_5208423` passed the
  count test but failed Test B: "root canal littleton" read `"-"` all month against a Search
  Console average of 18.9, and four more terms sat 20–35 places apart in the same direction
  ("dentist littleton" 40 vs 19.9, "littleton dentist" 49 vs 21.9, "dental implants near me" 41 vs
  6.8, "emergency dentist littleton" 52 vs 17.1). Remove once the campaign agrees with Google again.
- Local Falcon holds only three scans for this place, all dated 29 Oct, so there is no September
  grid and the map section has no month-over-month comparison this month.

### FULLERTON SMILE DENTISTRY (fullertonsmiledentistry.com)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `24384973_2931703` failed BOTH
  tests — the count fell from 13 of 14 to 8 and recovered only to 11, and "dentist near me" read
  `"-"` all month against a Search Console average of 9.15 while "dentist fullerton" read 66
  against 28.4. One keyword returned 115, outside the valid 1–100 range.
- SoLV here is 1.65, which rounds to 1.7 at one decimal. JavaScript `toFixed(1)` on 1.65 returns
  1.6, which is how an earlier report printed 1.6% in one place and 1.7% in another. Round once,
  server-side, and use the single value everywhere.

### LAVA DENTAL (Houston)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `30349785_5101386` holds a
  steady but tiny count — 2 to 4 of 23 keywords all month — and "dental implants houston",
  "houston dentist" and "dentist near me" read `"-"` all month against Search Console averages of
  9.4, 9.0 and 10.3. Note two of those three name a place, so the "near me" carve-out does not
  rescue it. One keyword returned 117, outside the valid range.
- Local Falcon holds only three scans for this place, all dated 29 Oct, so there is no September
  grid and the map section has no month-over-month comparison.

### MUSE DENTAL STUDIO (Houston)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign tracks 20 keywords of which
  12 read `"-"` on all 31 days. Three of those — "dentist houston", "dentist in houston" and
  "dentist near me" — have Search Console averages of 11.1, 1.0 and 8.4. The Search Console
  impressions behind those three are thin (9, 2 and 13), which weakens the signal without clearing
  the rule.
- Local Falcon holds only scans dated 29 Oct, so there is no September comparison.
- October's 5 new reviews average 3.4 against an overall 4.8. The overall rating is being dragged
  down and the report should say so plainly rather than quoting only the 4.8.

### ROD GLEAVE, DMD (slcsmiles.com)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Only 4 to 5 of 14 keywords held a
  position at any point, and 9 of 14 read `"-"` at month end while Search Console has 8 of those 9
  ranking (e.g. "dentist salt lake city" 29.1, "dental implants salt lake city" 25.5). Where both
  sources have a number they differ by 20+ places.
- Its backlink sheet is NOT shared by link — owner plus three named writers only.

### ORTHODONTICS IN WOODLAND HILLS
- **No Search Console property exists** for the domain in Windsor, under either `sc-domain:` or a
  URL-prefix form. That breaks three things the spec assumes: hero KPI 1, the footprint block, and
  Test B. All three are nulled with an `_error` and no Semrush figure is substituted. Someone needs
  to connect the property.
- Map keyword is "orthodontics in woodland hills", not "dentist in <city>" — no "dentist in" scan
  exists for this orthodontic practice.
- "invisalign near me" was #1 on 1 Oct and `"-"` on 23 of 31 days. That is the pattern Test B
  exists to catch and it cannot be checked here.

### OC PERIO & IMPLANTS DENTAL GROUP
- **No "dentist in mission viejo" scan exists** — this is a periodontics and implants practice and
  the account has never scanned that term. The four keywords it does scan (periodontics in/near me,
  dental implants in/near me) are recorded in the packet. The team must choose which stands in as
  the map, or approve a scan. The map is null until then.
- `page_path` splits the same article across two paths (`/blog/<slug>/` and `/<slug>/`) — e.g. gum
  recession reads 423 and 108. Merge them or note it.

### SADDLEBACK VALLEY ENDODONTICS
- Map keyword is "endodontics in laguna hills", not "dentist in <city>" — it is the one phrase both
  tracked in the campaign and scanned in Local Falcon in both months. Label the map accordingly.

### PERIO IMPLANT HEALTH PROFESSIONALS
- Hero location reads **Downtown Los Angeles, CA**, not Los Angeles — corrected by hand on an
  earlier report, so keep it.
- **Probably the wrong campaign in the manifest.** Project `27517640` holds two: the Los Angeles
  city campaign `27517640_3794715` that the manifest points at, and a Downtown Los Angeles
  neighbourhood campaign `27517640_4905046` tracking terms like "periodontist in downtown los
  angeles". Given the hero location, the Downtown one is likely correct. Someone should confirm.
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Both campaigns fail Test B — on the
  Downtown campaign "dental implants near me" and "dental implants specialist near me" read `"-"`
  all 31 days against Search Console averages of 8.1 and 1.0; on the city campaign the same term
  is `"-"` on 29 of 31 days while Local Falcon has it at ARP 2.88 / SoLV 69%.
- **No valid map.** No scan exists for "dentist in downtown los angeles" or "dentist in los
  angeles". October scans cover only "dental implants near me", "dental implants in los angeles",
  "periodontist in los angeles" and "periodontist near me". The map is null until the team picks a
  keyword or approves a scan; the candidates are listed in the packet with their report keys.
- No October blog posts — newest is 24 Sep, confirmed against the sitemap. A verified zero, and
  the team should know nothing went out.

### THE "dentist in <city>" ASSUMPTION
Three clients so far are not general dentists, so §5's default map keyword does not fit them. The
map keyword belongs in the manifest per client, not hard-coded in the spec. Until it is, check
Appendix A before assuming the default.

### DELICATE SMILES (delicatesmiles.net)
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `30530984_5177401` failed the
  count test outright — 10 of 14 keywords through 18 Oct, down to 3 on 19 Oct, recovering only to
  7 of 14 for the rest of the month. Remove once it holds a steady count again.
- Its September Search Console pull returns zero rows for `sc-domain:delicatesmiles.net`, with and
  without the country filter, so the fallback table has no month-over-month Change values and the
  footprint block has no comparison. Needs a look at the property.

### EXCEPTIONAL DENTISTRY
- Traffic to Each Page: keep the hostname filter for `palmdaleexceptionaldentistry.com`
- Keyword source: SEARCH CONSOLE FALLBACK for October 2026. Campaign `24862249_3027046` passed the
  count test but failed Test B on 9 of 20 keywords, and Local Falcon corroborated against it:
  Semrush read "dentist in palmdale" at #48 while the grid had all 121 points ranked at ARP 3.59
  and Search Console had the term at 3.1. Other gaps: "dental implants palmdale" 53 vs 1.9,
  "emergency dentist near me" 44 vs 1.4, "root canal palmdale" 64 vs 9.4. Remove once the campaign
  agrees with Google again.
- Second listing "Palmdale Emergency Dental Care" (`locations/17327590917246830856`) is still
  rejected by Windsor as unavailable. Its calls and clicks must be filled in by hand, as in August.
- Local Falcon holds no September scan for this place (all four scans are dated 6 Oct), so the map
  section has no month-over-month comparison this month.
- The backlink sheet's "NAP & Infos" tab lists the website as `exceptionaldentistryca.com` while
  the manifest has `palmdaleexceptionaldentistry.com`. Someone should confirm which is current.
