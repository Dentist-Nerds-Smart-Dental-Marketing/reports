---
description: Run the automated monthly client report cycle — collect data, build every active client's report, QA the batch, publish, and post the summary to Slack.
---

# Monthly client reports — automated run

Produces the monthly organic report for **every active client** in `clients/clients.json`,
publishes them, and reports back. Fired by a Routine on the 4th; also runnable by hand.

`$ARGUMENTS` may name a report month (`2026-09`) and/or a comma-separated slug list to limit
the run. With no arguments: **the month that just ended**, all active clients.

---

## Step 0 — Set up

1. `git fetch origin main && git checkout main && git reset --hard origin/main`
2. Read `clients/clients.json`. Work list = `active: true` clients (minus any slug filter).
3. Resolve the report month and `month-year` slug (e.g. `2026-09` → `september-2026`).
4. `mkdir -p .cache/<report_month>` for the data packets. **`.cache/` is never committed.**
5. Announce: month, client count, and anything already present (a client who already has that
   month's file is **skipped**, not overwritten — say so).

### Preflight — check the dependencies before burning any work
- **Windsor** — if the connector is unauthorized, GA4/GBP/GSC are unavailable, which is most of
  the report. **Stop and report** rather than producing 36 hollow reports. The fix is for a human
  to reauthorise Windsor in claude.ai connector settings.
- **Semrush** and **Local Falcon** — one cheap call each to confirm they answer.
- **Client websites** — these are often blocked by the environment's network policy. If so, blog
  lists can't be scraped; continue, mark blogs null, and ask for them in the Slack summary.

---

## Step 1 — Collect (INLINE, not delegated)

Work through the clients **one at a time in this session**, following
`.claude/agents/report-data-collector.md` as the procedure. Write each client's packet to
`.cache/<report_month>/<slug>.json` and then **drop the detail from your working context** —
the packet on disk is the handoff, so collecting 34 clients does not mean holding 34 clients'
data at once.

**Do not delegate this step to a `report-data-collector` subagent.** A dry run on 2026-10-22
showed subagents here receive only the Semrush MCP server; Local Falcon, Windsor and OneUp are
absent, so a delegated collector returns Semrush plus blogs and silently nulls the map grids,
GA4, GBP and Search Console. If you want to re-test that, have a subagent call
`listLocalFalconScanReports` first — if it cannot, collect inline.

Per client: resolve any null `ids` by name and write them back into `clients/clients.json`.
If one client's collection fails, record it and move on — one failure must not sink the run.

## Step 2 — Build (fan out)

One `report-builder` per client **that has a packet**, in batches of 5. Builders need only
Read/Write/Edit/Bash — no MCP servers — so delegation is safe and verified here. They have no
data tools, so anything they write traces to a packet.

Never run a builder for a client whose packet is missing — that is how blank reports happen.

---

## Step 3 — Review (the gate)

Run `report-reviewer` **once** over the whole batch. It checks coverage against the manifest and
correctness per report, including the cross-client duplicate check.

Take its verdict at face value:
- **PASS** → Step 4.
- **FAIL** → fix what is fixable (rebuild a client, rerun a collector), then **re-run the
  reviewer**. Only publish once it passes, or once the remaining failures are genuinely
  unfixable (e.g. a dead connector) — and then name them explicitly in the Slack summary.

Never report a run as clean when the reviewer said otherwise.

---

## Step 4 — Publish

```
git add -A
git fetch origin main && git rebase origin/main
git commit -m "Add <Month Year> monthly reports — <n> clients"
git push -u origin main
```
`main` is what GitHub Pages serves, so this puts the reports live. Confirm `clients/clients.json`
is included and `.cache/` is not.

---

## Step 4b — Generate Renato's client cover emails

Once the reports are live, produce the per-client cover emails:

```
python3 tools/gen-client-emails.py <month>-<year> <contacts.json> <out.md>
```

`contacts.json` maps client slug to recipient address. **It is NOT in this repo and must never
be committed.** This repository is PUBLIC on GitHub and the site serves its files without
authentication, so any address added here is published — in the manifest, in a skill, in an
agent definition, anywhere. `clients/clients.json` holds `contact_greeting` (names only, which
are already public on the practices' own sites); addresses live in the CRM or a private sheet
and are supplied at generation time.

If no contacts file is available, still generate the drafts with the To: line left blank and
say so in the Slack post — the body, subject and report link are the slow part, not the address.

Attach or link the generated markdown in the Slack summary so Renato can work straight from it.

## Step 5 — Tell Amin and Renato

Post to the Slack channel in `notify.slack_channel` (if null, say so and ask which channel):

- Month, clients published, hub link `https://reports.dentistnerds.com/clients/`
- The reviewer's verdict line
- **Needs a human**: any client with nulled sections, what's missing, and why — especially blogs
  and backlinks, which the old interactive skill collected from a person
- Any client skipped, paused, or failed, and the reason
- A reminder that these are live and awaiting their review before going to clients

Be accurate about what did not work. A run that half-failed and is reported as a success is
worse than one that failed loudly.

---

## Guardrails
- Real data only. A null with an explanation beats a plausible number.
- Never overwrite an existing month's report unless explicitly asked.
- Never edit `clients/report-template.html`.
- Final reports carry no `contenteditable`.
- Reuse Local Falcon scans within 30 days; only scan the gaps.
