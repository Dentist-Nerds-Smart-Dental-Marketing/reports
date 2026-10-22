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

## Step 1 — Collect (fan out)

One `report-data-collector` per client, **in batches of 5** so connector rate limits and
Local Falcon don't get hammered. Each writes `.cache/<report_month>/<slug>.json`.

Pass the client's manifest row and `out_path`. As packets land, write any `ids_resolved` back
into `clients/clients.json` so later runs are deterministic.

If a collector fails entirely, record it and carry on — one broken client must not sink the run.

---

## Step 2 — Build (fan out)

One `report-builder` per client **that has a packet**, again in batches of 5. Builders have no
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
