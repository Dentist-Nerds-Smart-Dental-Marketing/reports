---
description: Generate a Dentist Nerds SEO audit & growth report for a client — team website review, then Semrush + Local Falcon data, build from the template, and publish to the hub
argument-hint: <practice name> | <website> | <city, ST> [| keyword to scan]
---

# Nerds SEO Report

Generate a branded **Dentist Nerds — SEO Audit & Growth Report** for a client and publish it.

## Inputs

Parse `$ARGUMENTS` (pipe- or comma-separated). Expected fields, in order (ask for any of the first three that are missing — never guess the domain or city):

1. **Practice name** — e.g. `Westgrove Dental Care`
2. **Website** — e.g. `westgrovedental.com`
3. **Market** — e.g. `Pasadena, CA`
4. **Keyword to scan** *(optional)* — the term for the Google Maps / Local Falcon grid, e.g. `dentist near me`. If omitted, default to `dentist <city>`.

Derive the **client slug** from the practice name: lowercase, spaces → hyphens, strip punctuation. Match an existing folder in `reports/` exactly if one already exists.

---

## Step 1 — Ask the team the review questions (ALWAYS do this first)

**Before pulling any data tools**, ask the **team** to do a quick eyes-on review of the client's website and answer the questions below. Present the questions, then **wait for their answers** — do not judge these yourself or fetch the site. Their answers drive the Health Score pillars and the Top 3 Weaknesses; the automated data comes *after*.

Ask the team:

1. **Usability** — How is the usability? Open the website: is it easy to navigate, clear menu, obvious "book/call" CTAs, mobile-friendly, fast?
2. **ADA & color scheme** — How is the ADA compliance and color scheme? Readable contrast, alt text, labeled forms, accessible navigation?
3. **Stock imagery** — Does it include a lot of stock imagery (vs. real photos of the doctors, team, and office)?
4. **Treatment-page FAQs (AI / AEO)** — Do the treatment pages include FAQs for AI visibility (ideally with FAQ schema, in patient language)?

Invite any other notes (thin content, broken links, missing schema, weak internal linking, outdated design, etc.).

Use those answers to populate the **Health Score** pillars and the **Top 3 Weaknesses** + "other issues we found" list.

---

## Step 2 — Pull live data

Now run the connected MCP servers. **Always call the tools — never invent numbers.** Default the Semrush database to `us`.

Pull for the client's domain:

- **Search Visibility** (Semrush `domain_rank` overview): organic monthly traffic, total ranking keywords. (AI Visibility dial is an estimate informed by the Step 1 AEO answer.)
- **Authority & Backlinks** (Semrush `backlink_research`): total backlinks, Authority/Domain score, toxic/spam %.
- **Local Keyword Rankings** (Semrush `domain_organic` with `display_filter` = `+|Ph|Co|<city>`, `display_sort` = `po_asc`): the client's Google organic position for the core local terms — **dentist in [city], dentist near me, dental implants in [city], emergency dentist in [city], dental veneers in [city], dental cleaning in [city], invisalign in [city], all-on-4 in [city], root canal in [city]**. Take the best (lowest) position found per term; if a term isn't in the domain's organic results, mark it **"Not on page 1"**. (For "dentist near me", note it's a geo term best confirmed by the Local Falcon scan.)
  - **Target the practice's OWN city/neighborhood only.** Every keyword in this table must be for the market the office actually sits in (the city — and where relevant the neighborhood, e.g. San Carlos / Del Cerro for a Del Cerro office). **Never list a keyword for a different town just because Semrush shows the domain ranking for it** — Semrush surfaces stray out-of-area terms (a town 15–20 miles away, a same-name city in another state) that are NOT valid targets. If the domain only ranks for far-off or brand-name terms, that's the story: show the real in-city targets as **"Not on page 1"** rather than padding the table with irrelevant geos.
  - To get in-city target terms + real search volumes, use Semrush `phrase_these` on `<service> <city>` variants (e.g. `dentist <city>;dental implants <city>;cosmetic dentist <city>;emergency dentist <city>;invisalign <city>;<neighborhood> dentist`). Use those volumes in the tables.
- **Keyword gap** (Semrush `domain_organic`, page 2+ / poorly-ranked): keywords the site has pages for but ranks poorly. Capture keyword, the page it lives on, monthly search volume, current rank. Pick the 5 highest-volume. **In-city terms only** (same rule as above) — for a thin site with no pages, the gap is the high-value in-city terms it has **no page** for (mark "No dedicated page" / "Not ranking").
- **Local competition** (Semrush `domain_organic_organic` or per-competitor `domain_rank`): 3 nearby competitors and each one's ranking-keyword count, for the comparison bars.
  - **Competitors must be within ~5 miles of the practice office** (get the office address from the Local Falcon business search / scan). Verify each competitor's location before using it. **Ignore Semrush's suggested "competitors" that are out-of-area or name-twins** (e.g. same-surname practices or same-named towns in other states/regions) — they are not real local rivals. The Local Falcon scan's own competitor list (businesses ranking inside the grid) is the most reliable source of genuinely-nearby competitors; pull each one's keyword count with `domain_rank`.
- **Google Maps** (Local Falcon): run/read a grid scan for the chosen keyword; capture each cell's rank, the average rank, and % of grid where the practice is visible.

If a metric can't be retrieved, leave the template placeholder and tell the user which fields need manual entry — don't fabricate.

### Data interpretation rules (apply automatically)

- **Geographic scope is strict.** Keyword targets = the practice's own city/neighborhood; competitors = within ~5 miles of the office. Drop anything outside that radius even if Semrush returns it. A town ~15–20 miles away (e.g. San Ysidro for a Del Cerro/San Diego office) or a same-name city in another state is **never** a valid target or competitor. When in doubt, verify the office address and the competitor's location first.
- **Ranking keywords below 80** → flag the Ranking Keywords dial as low and call out that **there isn't enough content / no keyword strategy** (a top weakness, and a driver for the Content Engine).
- **Many backlinks but low Domain Authority** → call out that the profile is **probably spammy / toxic backlinks dragging authority down**; recommend a disavow + cleanup (make it a Top 3 Weakness when the gap is severe).
- Reflect these in both the dial flags/notes and the Top 3 Weaknesses.
- **The Google Maps grid must be REAL — never placeholder.** It must come from an actual Local Falcon scan (run this from a session where Local Falcon is connected — it is NOT available in headless/cloud runs). **Never reuse the template's default `seed`/`ranks` arrays** — that ships an identical, fake grid across every client. If Local Falcon isn't available, set the Maps section to a clear "Pending — from your latest Local Falcon scan" state and tell the user, rather than filling placeholders.
- Local Keyword Rankings come from real Semrush positions (US desktop). Footnote the source + month.

---

## Step 3 — Build the report from the template

1. Read `reports/report-example/index.html` — the **canonical template**. Do NOT edit the template itself.
2. Copy it to `reports/<client-slug>/index.html` (create the folder).
3. Fill in the real values, section by section (this is the exact section order in the template):
   - **Hero**: practice name, website (`Audited: <domain>`), market, report date (today), and the 4 meta-grid blocks (Prepared For, Report Date, Issues Found, Recommendation).
   - **Health Score**: the gauge number + status, and the 4 pillar percentages (Content Quality & Accuracy, User Experience & Navigation, AI Search Visibility / AEO, Local Search & Maps) — derived from the **Step 1 review**.
   - **Search Visibility** dials: Monthly Traffic, Ranking Keywords, AI Visibility — set each `data-value`/`data-max` and the flag.
   - **Authority & Backlinks** dials: Total Backlinks, Domain Authority, Toxic %.
   - **Top 3 Weaknesses** + the "other issues we found" list — written from the **Step 1 findings** and the interpretation rules.
   - **Local Keyword Rankings** table: each core local keyword + its real Google organic rank, color-coded (`rk good` = 1–3, `rk warn` = 4–10, `rk` = 11+ / "Not on page 1").
   - **Keyword gap** table — the 5 keywords with page, volume, rank (`rk` red / `rk warn` amber).
   - **Local Competition** bars — set each `width:%` relative to the top competitor and the numbers.
   - **Google Maps**: the "Keyword scanned" chip, the 5×5 `seed`/`ranks` arrays in the script (real Local Falcon data), average rank, % visible.
   - **Game Plan**: tailor the Step 01 "Rebuild" copy + the ongoing engines (02–06) to the client where relevant.
4. Keep all branding, fonts, the Local-Falcon-style map, and interactive JS intact.
5. **Reports are final, non-editable deliverables.** The template has NO `contenteditable` anywhere — never add it. Replace the placeholder values directly in the HTML.

## Step 4 — Drop it on the hub page

Add the finished report to the **hub / listing page** — `reports/index.html`, served at **https://reports.dentistnerds.com/reports/** (the password-gated team hub).

- Add a card near the **top** of the `<div class="grid" id="grid">`, following the existing `<a target="_blank" class="card">…</a>` pattern.
- Link `href="/reports/<client-slug>/"`, set the card name to the practice name, and the tag to `SEO Report`.
- Confirm the card appears in the grid before publishing.

## Step 5 — Publish

- Commit on `main` with message: `Add SEO report — <Practice Name>`.
- Push with `git push -u origin main` (rebase onto `origin/main` first if it has moved).
- Report the live URL: `https://reports.dentistnerds.com/reports/<client-slug>/`.

## Notes

- The template lives at `reports/report-example/` — it's the master copy. Always generate fresh client reports from it, and keep it non-editable.
- Anything you genuinely can't source, leave as a clearly-labeled "pending" state and tell the user — never ship fabricated or identical placeholder data across clients.
