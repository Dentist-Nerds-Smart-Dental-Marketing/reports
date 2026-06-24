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

- **Search Visibility** (Semrush organic/overview): organic monthly traffic, total ranking keywords.
- **Authority & Backlinks** (Semrush backlinks): total backlinks, Authority/Domain score, toxic/spam %.
- **Keyword gap** (Semrush): keywords the site has pages for but ranks poorly (page 2+ or unranked). Capture keyword, the page it lives on, monthly search volume, current rank. Pick the 5 highest-volume.
- **Local competition** (Semrush): 3 nearby competitors and each one's ranking-keyword count, for the comparison bars.
- **Traffic sources** (Semrush .Trends / Windsor GA4 if available): Direct / GBP / Organic / Referral / Paid mix.
- **Google Maps** (Local Falcon): run/read a grid scan for the chosen keyword; capture each cell's rank, the average rank, and % of grid where the practice is visible.

If a metric can't be retrieved, leave the template placeholder and tell the user which fields need manual entry — don't fabricate.

### Data interpretation rules (apply automatically)

- **Ranking keywords below 80** → flag the Ranking Keywords dial as low and call out that **there isn't enough content / no keyword strategy** (a top weakness, and a driver for the Content Engine).
- **Many backlinks but low Domain Authority** → call out that the profile is **probably spammy / toxic backlinks dragging authority down**; recommend a disavow + cleanup (make it a Top 3 Weakness when the gap is severe).
- Reflect these in both the dial flags/notes and the Top 3 Weaknesses.
- **Google Maps grid & Traffic mix must be REAL or marked pending — never placeholder.** The 5×5 map grid must come from an actual Local Falcon scan, and the Traffic channel mix from real analytics (GA4 / Windsor). **Never reuse the template's default grid or default traffic percentages** — that ships identical, fake data across every client. If Local Falcon or analytics data is not available in the session, set that section to a clear "Pending — from your latest Local Falcon scan / GA4" state and tell the user which sections need real data, rather than filling placeholders.

---

## Step 3 — Build the report from the template

1. Read `reports/report-example/index.html` — the **canonical template**. Do NOT edit the template itself.
2. Copy it to `reports/<client-slug>/index.html` (create the folder).
3. Fill in the real values:
   - **Hero**: practice name, website, market, report date (today), and the meta-grid blocks.
   - **Health Score**: overall score + the 4 pillar percentages — derived from the **Step 1 review**.
   - **Search Visibility** dials: Monthly Traffic, Ranking Keywords, AI Visibility — set each `data-value`/`data-max` and the flag.
   - **Authority & Backlinks** dials: Total Backlinks, Domain Authority, Toxic %.
   - **Top 3 Weaknesses** + the "other issues" list — written from the **Step 1 findings** and the interpretation rules.
   - **Keyword gap** table — the 5 keywords with page, volume, rank (use `rk` red / `rk warn` amber).
   - **Local Competition** bars — set each `width:%` relative to the top competitor and the numbers.
   - **Google Maps**: the "Keyword scanned" chip, the 5×5 grid `seed`/`ranks` arrays in the script, average rank, % visible.
   - **Traffic** stack: the channel percentages and bar widths.
   - Tailor the **Game Plan** copy (Step 01 + engines) to the client where relevant.
4. Keep all branding, fonts, and interactive JS intact.
5. **Reports are final deliverables — keep them non-editable.** The template has no `contenteditable` anywhere; never add it. Just replace the placeholder values directly in the HTML.

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

- The report is fully click-to-edit, so leave anything uncertain as a sensible placeholder and flag it for the user to finalize.
- The template lives at `reports/report-example/` — keep it as the master copy and always generate fresh client reports from it.
