# SOP — Pre-Audit Report (Website Quality & AI Visibility Audit)

**Purpose:** Produce a polished, data-backed, single-page HTML audit report for a prospective dental client, publish it live on the Dentist Nerds reports hub, and list it on the hub index.

**Output:** A self-contained `index.html` at `reports.dentistnerds.com/reports/<slug>/`, plus a card on `reports.dentistnerds.com/reports/`.

**Time:** ~20–40 min per report once set up.

**At a glance:** Collect inputs → pull Semrush + live-site data → **verify every claim** → pick the honest narrative → build the single-file `index.html` from the template → preview/render check → add hub card → commit *only the two paths* + push → confirm live (200 + card present).

> 📋 **For daily use, follow the [Pre-Audit Run Sheet](Pre-Audit-Run-Sheet.md)** — a one-page, tick-the-box checklist per report. This document is the reference manual behind it; open it when a run-sheet step needs the "why."

---

## 0. Before you start — inputs to collect from the requester

1. **Practice website URL** (e.g. `https://www.example.com/`)
2. **Doctor name(s)** — optional but improves credibility (verify against the live site anyway)
3. **Notes / findings to mention** — the requester's manual observations (UX issues, backlinks, FAQ, missing pages, etc.)
4. **"How we help" closing notes** — the standard services paragraph (foundation + treatment pages/schema, backlinks + NAP + listings, 4 AI blogs/mo, GBP/Maps, monthly reporting)
5. **Template to match** — always the William Wong reference: `https://reports.dentistnerds.com/reports/william-wong-dds/`

---

## 1. Access & tools required

| Need | What it is |
|---|---|
| **Semrush MCP** (server `fd709d83…`) | Live SEO data — the factual backbone of the report |
| **`gh` CLI** (logged in as `sheena-dentalnerds`) | Has admin/push to the production repo |
| **Production repo** | `Dentist-Nerds-Smart-Dental-Marketing/reports` (public). **This** is what Netlify deploys — NOT `sheena-dentalnerds/dentist-nerds-reports` |
| **Netlify** | Auto-deploys the production repo's `main` to `reports.dentistnerds.com` (~15–60s after push). No CLI/token here — deploy by pushing to GitHub. |
| **curl** | On Windows, always add `--ssl-no-revoke`; use `dangerouslyDisableSandbox` for network calls |
| **Preview server** | `.claude/serve.ps1` on port 8099 (Python is NOT installed; use the PowerShell server) |

> The local working folder `C:\Users\Sheena\Desktop\Dentist Nerds Report` has `origin` → the production repo, so `git push` from here publishes live. `personal` remote = the old `dentist-nerds-reports` repo (backup only, not connected to the live site).

---

## 2. Gather the data (Semrush + live site)

Run these Semrush reports (toolkit → `get_report_schema` → `execute_report`, database `us`):

| Report | Gives you |
|---|---|
| `domain_rank` | **Current** snapshot: keywords, organic traffic, (for KPIs) |
| `domain_rank_history` (sort `dt_desc`, limit 40) | Monthly trend → the traffic chart + the growth/decline story |
| `domain_organic` (sort `tr_desc`, limit ~35) | Top keywords, positions, volumes, which URL ranks → findings & tables |
| `domain_organic_unique` (limit ~20) | Top pages by traffic → site-architecture table |
| `backlinks_overview` (target_type `root_domain`) | Authority Score, referring domains, follow vs nofollow → backlink finding |

**KPI definitions (hero block):**
- **Authority Score** = `score` from `backlinks_overview`
- **Visits / mo** = `Organic Traffic` from `domain_rank` (current)
- **Ranking Keywords** = `Organic Keywords` from `domain_rank`
- **Referring Domains** = `domains_num` from `backlinks_overview`

**Verify the practice profile** with WebFetch on the homepage: practice name, city/state, doctors, services, phone/address, whether a hero CTA / booking widget / FAQ exists.

---

## 3. ⚠️ VERIFY every claim before writing it (critical)

The requester's notes are **observations, not verified facts**. A client can open their own page and check, so the report must be true. **Always confirm against the live site** before stating a finding.

- **FAQ content / schema** — fetch the raw HTML of 4–6 treatment pages and grep:
  ```bash
  curl -s --ssl-no-revoke "<treatment-url>" | grep -ic 'FAQPage'      # FAQ schema?
  curl -s --ssl-no-revoke "<treatment-url>" | grep -ioE 'frequently asked questions'  # visible FAQ?
  curl -s --ssl-no-revoke "<treatment-url>" | grep -oiE '"@type"\s*:\s*"?[A-Za-z]+'    # what schema exists
  ```
  - Real example: on **Spectrum**, FAQ *content existed* but had **no FAQPage schema** → reworded to "FAQs aren't schema-marked," not "no FAQ content."
  - On **Williamsburg**, there was genuinely **no FAQ content and no FAQ schema** → the note was accurate, stated as-is.
- **Hero CTA / booking widget / footer issues** — confirm via WebFetch or by loading the page. State precisely what's true.
- Use the correct URL form (some sites 404 on trailing slashes — check both).

**Rule: if the data contradicts a note, report the data and tell the requester what you found.**

---

## 4. Decide the narrative (don't force one template story)

Read the trend + keyword data and pick the honest story:

| Data pattern | Narrative angle | Banner |
|---|---|---|
| Low traffic, few keywords (e.g. Next Smile: 38 kw) | "Branded trap, missing pages, 400+ keyword potential" | Keep "100+ pages" banner |
| Strong & growing (e.g. Spectrum: 1,308 kw) | "Strong foundation, but conversion leaks + money pages stuck + AI gap" | **Drop** the 100+ banner |
| Solid but declining (e.g. Williamsburg: 846 kw, slipping) | "Momentum slipped — reverse the decline" | **Drop** the banner |

> Don't claim "only X keywords, should be 400+" for a site that already ranks for hundreds. Don't claim "thin site / 100+ pages" for a site that isn't thin.

---

## 5. Build the report HTML

1. **Pick a slug** — practice-name based, kebab-case (e.g. `williamsburg-dental-arts`, `spectrum-dental-group`). Confirm with requester if ambiguous.
2. **Copy the template head/CSS** from the most recent report (identical across all reports):
   ```bash
   hl=$(grep -n "</head>" reports/<recent-slug>/index.html | head -1 | cut -d: -f1)
   mkdir -p reports/<new-slug>
   sed -n "1,${hl}p" reports/<recent-slug>/index.html > reports/<new-slug>/index.html
   ```
3. **Set the `<title>`** to `<Practice> — Website Quality & AI Visibility Audit`.
4. **Write the body** (append after `</head>`), in this section order:
   1. **Hero** — eyebrow, H1 (practice name), description, 4 KPI cards, prepared-line (`domain · City, State · Live Semrush Data · <Month Year>`)
   2. **3 Focus Areas** — the three biggest priorities (red/amber/purple cards with mini-charts/gauges)
   3. **Key Findings** — 5–6 findings, each grounded in a real number
   4. **Site Architecture** — triple-stat + top-pages table + note
   5. **Triage Center** — technical/UX issues (one row per issue; map the requester's UX notes here)
   6. **Traffic Trend** — SVG line chart from `domain_rank_history` + delta row
   7. **Where Traffic Comes From** — conv cards + top-pages table + top-keywords table
   8. **Process 01: Organic Search Optimization** — 6 steps
   9. **Process 02: AI Search Visibility** — 6 steps
   10. **Priority Action Plan** ("How We Help", dark section) — 8 numbered actions mapping the closing notes
   11. **Footer** — brand + meta line

**Mapping the requester's notes → sections:**
- Backlink evaluation → a Key Finding + a Triage row + Action #6
- FAQ / AI visibility → Focus 03 + a Key Finding + Triage row + an AI action
- Missing/disorganized pages → Site Architecture note + Key Finding
- Each UX issue (no CTA, contrast, footer, broken images, booking widget, etc.) → its own Triage row, and the headline ones also become Focus 01 + Action #1
- "How we help" notes → the 8 action rows (foundation, treatment pages+schema, FAQ, keyword growth, backlinks+NAP+listings, 4 blogs/mo, GBP+reporting)

**Trend chart tip:** plot one point per month from `domain_rank_history`. Map value→y with `y = 440 − (value/axisMax)*380`; space x evenly from 110→1045. Mark the peak and the current point.

---

## 6. Verify rendering (before publishing)

```
preview_start (name: static)  → navigate to http://localhost:8099/reports/<slug>/
```
- `preview_console_logs` (level error) → expect none
- DOM check via `preview_eval`: confirm H1, the 4 KPI numbers, 3 focus titles, all 10 content sections (Hero → Priority Action Plan) + footer, 8 action rows, 2 trend paths, and **no leftover "100+" banner** if you dropped it.
- Screenshots are nice-to-have but the renderer sometimes times out — the DOM check is sufficient.

---

## 7. Publish (to the production repo → Netlify)

Working in `C:\Users\Sheena\Desktop\Dentist Nerds Report` (origin = production repo):

1. **Sync first** to avoid conflicts (the hub `index.html` is regenerated/edited upstream often). **Your new report lives only in the working tree until committed — never `git reset --hard` before saving it.** Safe order:
   ```bash
   git add reports/<slug>/index.html          # stage the new report so reset can't wipe it
   git stash --keep-index                      # park any other uncommitted changes
   git fetch origin main && git rebase origin/main   # replay your staged work on top of latest
   git stash pop                                # restore parked changes (if any)
   ```
   Only use `git reset --hard origin/main` when the working tree is genuinely clean (nothing of yours to lose).
2. **Add the hub card** — append after the last card in `reports/index.html` (newest goes last). Match the existing markup exactly:
   ```html
   <a target="_blank" href="/reports/<slug>/" class="card">
     <div class="card-icon">
       <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M7 14l4-4 4 4 5-6"/></svg>
     </div>
     <div><div class="card-name"><Practice Name></div><div class="card-tag">SEO Audit</div></div>
   </a>
   ```
3. **Commit only the two specific paths** (NEVER `git add .` — the org repo has no `.gitignore`, so `.claude/` would get committed):
   ```bash
   git add reports/<slug>/index.html reports/index.html
   git commit -m "Add <Practice> SEO audit + hub listing card"
   git push origin main
   ```
4. If the push is **rejected** (someone pushed meanwhile): `git fetch origin main`, then rebase or re-apply your card onto the latest `reports/index.html` (its structure may have changed), and push again.

> Note: the hub `reports/index.html` is technically auto-generated by a separate `seo-skill-set` tool not on this machine. Hand-editing the card works and deploys immediately; a future regeneration that scans `reports/` folders will keep it. Flag this to the requester.

---

## 8. Verify it's live

```bash
# report returns 200
curl -s -o /dev/null -w "%{http_code}" --ssl-no-revoke "https://reports.dentistnerds.com/reports/<slug>/"
# card present on hub
curl -s --ssl-no-revoke "https://reports.dentistnerds.com/reports/" | grep -c "<slug>"
```
Both should be `200` and `≥1` within ~1 minute of pushing. Report the live URL to the requester.

---

## 9. Quality checklist (before declaring done)

- [ ] Every number in the report traces to Semrush or a verified live-site check
- [ ] FAQ/schema/UX claims were **verified**, not copied blindly from notes
- [ ] Narrative matches the data (no "low keywords" story on a strong site; banner dropped when not thin)
- [ ] All requester notes are represented somewhere in the report
- [ ] "How we help" action plan includes all standard commitments
- [ ] Hero KPIs, footer meta, and account line show the right practice/city/doctors
- [ ] Renders with no console errors; no leftover template text from the copied report
- [ ] Report URL returns 200 and the hub card is visible
- [ ] Slug is practice-based and confirmed

---

## Reference — worked examples

The `reports/` folder holds 35+ live audits; copy the **most recent** one for the current template/CSS (don't assume an old slug is up to date). The clearest narrative examples built with this SOP:

| Practice | Slug | Data shape | Narrative |
|---|---|---|---|
| Next Smile + Implant | `next-smile-implant` | 38 kw, 32 visits | Branded trap, missing pages (kept 100+ banner) |
| Spectrum Dental Group | `spectrum-dental-group` | 1,308 kw, 656 visits | Strong but leaking; money pages stuck on page 2 |
| Williamsburg Dental Arts | `williamsburg-dental-arts` | 846 kw, declining | Momentum slipped; reverse the decline |

> Slugs are case-sensitive and inconsistent across the repo (some kebab-case, some capitalized). Always confirm the exact folder name before committing.
