---
description: Generate a Dentist Nerds SEO audit & growth report for a client from a manual site review + live Semrush & Local Falcon data
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

Derive the **client slug** from the practice name: lowercase, spaces → hyphens, strip punctuation. Match an existing folder in `reports/` exactly if one already exists.

---

## Step 1 — Ask the team the review questions (ALWAYS do this first)

**Before pulling any data tools**, ask the **team** to do a quick eyes-on review of the client's website and answer the questions below. Present the questions, then **wait for their answers** — do not judge these yourself or fetch the site. Their answers are what drive the Health Score pillars and the Top 3 Weaknesses; the automated data comes *after*.

Ask the team:

1. **Usability** — How is the usability? Open the website: is it easy to navigate, clear menu, obvious "book/call" CTAs, mobile-friendly, fast?
2. **ADA & color scheme** — How is the ADA compliance and color scheme? Readable contrast, alt text, labeled forms, accessible navigation?
3. **Stock imagery** — Does it include a lot of stock imagery (vs. real photos of the doctors, team, and office)?
4. **Treatment-page FAQs (AI / AEO)** — Do the treatment pages include FAQs for AI visibility (ideally with FAQ schema, in patient language)?

Invite any other notes (thin content, broken links, missing schema, weak internal linking, outdated design, etc.).

Once the team has answered, use those answers to populate:
- the **Health Score** pillars (Content Quality & Accuracy, User Experience & Navigation, AI Search Visibility / AEO, Local Search & Maps),
- the **Top 3 Weaknesses** + the "other issues we found" list.

---

## Step 2 — Pull live data

Now run the connected MCP servers. **Always call the tools — never invent numbers.** Default the Semrush database to `us`.

Pull for the client's domain:

- **Search Visibility** (Semrush organic/overview): organic monthly traffic, total ranking keywords.
- **Authority & Backlinks** (Semrush backlinks): total backlinks, Authority/Domain score, toxic/spam %.
- **Keyword gap** (Semrush): keywords the site has content/pages for but ranks poorly (page 2+ or unranked). Capture keyword, the page it lives on, monthly search volume, current rank. Pick the 5 highest-volume.
- **Local competition** (Semrush): 3 nearby competitors and each one's ranking-keyword count, for the comparison bars.
- **Traffic sources** (Semrush .Trends / Windsor GA4 if available): Direct / GBP / Organic / Referral / Paid mix.
- **Google Maps** (Local Falcon): run/read a grid scan for the chosen keyword; capture each cell's rank, the average rank, and % of grid where the practice is visible.

If a specific metric can't be retrieved, leave the template's placeholder and tell the user which fields need manual entry — don't fabricate.

### Data interpretation rules (apply automatically)

- **Ranking keywords below 80** → flag the Ranking Keywords dial as low and call out in the report that **there isn't enough content / no keyword strategy** (a top weakness, and a driver for the Content Engine in the Game Plan).
- **Many backlinks but low Domain Authority** (high backlink count paired with a low authority score) → call out that the profile is **probably spammy / toxic backlinks dragging authority down**, and recommend a disavow + cleanup (make it a Top 3 Weakness when the gap is severe).
- Reflect these calls in both the relevant dial flags/notes and the Top 3 Weaknesses.

---

## Step 3 — Build the report from the template

1. Read `reports/report-example/index.html` — the **canonical template**. Do NOT edit the template itself.
2. Copy it to `reports/<client-slug>/index.html` (create the folder).
3. Fill in the real values:
   - **Hero**: practice name, website, market, report date (today), and the meta-grid blocks (Prepared For, Report Date, Issues Found, Recommendation).
   - **Health Score**: overall score + the 4 pillar percentages — derived from the **Step 1 review**.
   - **Search Visibility** dials: Monthly Traffic, Ranking Keywords, AI Visibility — set each `data-value`/`data-max` and the flag.
   - **Authority & Backlinks** dials: Total Backlinks, Domain Authority, Toxic %.
   - **Top 3 Weaknesses** + the "other issues" list — written from the **Step 1 findings**.
   - **Keyword gap** table — the 5 keywords with page, volume, rank (use `rk` red / `rk warn` amber).
   - **Local Competition** bars — set each `width:%` relative to the top competitor and the numbers.
   - **Google Maps**: the "Keyword scanned" chip, the 5×5 grid `seed`/`ranks` arrays in the script, average rank, and % visible.
   - **Traffic** stack: the channel percentages and bar widths.
   - Tailor the **Game Plan** copy (Step 01 + engines) to the client where relevant.
4. Keep all branding, fonts, and interactive JS intact.

## Step 4 — Add to the listing

Add a card for the new report near the top of `reports/index.html` grid, following the existing `<a class="card">` pattern, linking to `/reports/<client-slug>/`.

## Step 5 — Publish

- Commit on `main` with message: `Add SEO report — <Practice Name>`.
- Push with `git push -u origin main` (rebase onto `origin/main` first if it has moved).
- Report the live URL: `https://reports.dentistnerds.com/reports/<client-slug>/`.

## Notes

- The report is fully click-to-edit, so leave anything uncertain as a sensible placeholder and flag it for the user to finalize.
- The template lives at `reports/report-example/` — keep it as the master copy and always generate fresh client reports from it.
