---
description: Run the automated monthly client report cycle to SPEC v6 — collect, build, QA, publish, notify.
---

# Monthly client report run (SPEC v6)

**The spec is `.claude/specs/monthly-report-spec-v6.md`. Read it before anything else.**
It is transcribed from the Google Doc "Monthly Organic SEO Report — Generation Spec v6
(ALL CLIENTS)". If the doc has moved on, re-sync the file first — the doc wins.

Manifest: `clients/clients.json` (`active: true` only). Packets: `.cache/<YYYY-MM>/<slug>.json`.
Everything under `.cache/` is gitignored and never published.

> **READ THE PERMANENT RULES AT THE END OF THE SPEC FIRST.** They were added 2026-11-05 and
> override anything that conflicts. In short: the page is a client deliverable and carries no
> caveats, no methodology and no apologies (R1); GBP figures publish exactly as pulled with no
> restatement note (R2); the Backlinks card has fixed body text and a visible button to the
> client's real sheet, and the logins in those sheets are intentional and never a reason to
> withhold it (R3); never edit a report already sent (R4); build to
> `<month>-<year>-staging.html` and promote only on approval (R5); and curl every live page
> before reporting done (R6).

## 0. Pre-flight — do these before spending any agent time
- **Local Falcon credits.** Call `viewLocalFalconAccountInformation`. An 11×11 grid costs 121
  credits and a 15×15 costs 225. If the balance cannot cover the clients that need a fresh scan,
  say so now and get it topped up — do not discover it halfway through. Scans are reused within
  the month either way; never run one without explicit approval.
- **Backlink sheets.** Every report must carry a Backlinks card sourced only from the client's own
  tracking sheet. Confirm `.cache/<month>/backlink-sheets.json` exists and covers the active
  clients. Without it the run cannot produce a compliant report.
- **Connectors.** Semrush, Windsor, Local Falcon and Google Drive must all answer. Two of the three
  OneUp servers hold invalid keys; only `mcp__One_up_5_22_206__*` works.

## 1. Collect — one collector per client
Follow `.claude/agents/report-data-collector.md`.

> **Known environment trap.** A dry run on 2026-10-22 found subagents receiving only the Semrush
> MCP server, which silently nulls the maps, GA4, GBP and Search Console — most of the report.
> `tools: '*'` in the agent frontmatter fixes it, but only takes effect in a **fresh session**,
> because agent definitions load at session start. Before trusting a batch, have one collector
> call `listLocalFalconScanReports` and confirm it answers. If it does not, run collection inline
> in the main session instead.

Record the Semrush §4 validation verdict for every client. An `unreliable` verdict means the
keyword table falls back to Search Console for that client that month, and the client gets added
to Appendix A of the spec.

## 2. Build — batches of 5
Follow `.claude/agents/report-builder.md`. Builders have no data tools on purpose: if a figure
is not in the packet, it cannot reach the page. Hand each builder its slug, packet path and the
template, plus any Appendix A exception that applies to that client.

## 3. QA — once, over the whole batch
Follow `.claude/agents/report-reviewer.md`. Fix every FAIL and re-run it. Do not publish a batch
with an open FAIL, and do not report a verdict the reviewer did not give.

## 4. Publish — staging first (R5)

Builders write `clients/<slug>/<month>-<year>-staging.html`. The official
`<month>-<year>.html` is replaced only after the team approves, and never for a client whose
report has already been sent (R4). Promote with a plain copy, then commit both files.

## 4b. Publish — per client, two files at a time
Per spec §9. **Never `git add -A`** — it sweeps up unrelated work. Never a bare `git commit` —
it opens an editor. Never rebase with files still staged.

```
git add clients/<slug>/<month>-<year>.html clients/<slug>/index.html
git commit -m "<slug>: <Month> <Year> report"
git pull --rebase origin main
git push origin main
```

Then confirm the live URL returns 200 **and** that the published file matches the local one.

## 4c. R6 final check — before you tell anyone the run is done
`curl` every live page. Confirm none of the R1 wording appears, the Backlinks body text matches
R3 word for word, and a visible button links to a `docs.google.com/spreadsheets` URL. List any
page that fails. A run is not done until this has been run and passed.

## 5. Notify
Post the run summary to Slack `#organic-search`, and email Amin and Renato the hub link plus a
per-client list of individual report links. Say plainly what needs a human: connector failures,
sheets that ask for a sign-in, campaigns that failed validation, clients held back and why.
Internal problems go here — never onto a client's page.
