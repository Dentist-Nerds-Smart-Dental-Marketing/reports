# SEO Client Review — August 2026

**Date:** 28 Aug 2026 · **Scope:** all 32 active SEO clients
**Sources:** Local Falcon (118 trend reports, 39 campaigns, scans through 8/25) · Semrush (domain overview + 12-month rank history, US db) · repo audit

Movement convention: Local Falcon reports moves as *improvement-positive* — a negative
`arp_move` / `solv_move` means the client got worse.

---

## 1. Critical — act this week

### 1.1 The Smile Spa (Agoura Hills) — organic traffic −91%
| | Apr | May | Jun | Jul | **Aug** |
|---|---|---|---|---|---|
| Keywords | 499 | 490 | 542 | 623 | **629** |
| Traffic | 614 | 540 | 1,458 | 1,455 | **136** |

Keyword count is flat while traffic collapsed — this is positional loss, not deindexing.
The Jun–Jul run at ~1,455 was roughly 2.4× the client's ~600 baseline; August fell *below*
the baseline too, so both the spike and part of the floor are gone.

Traffic is now concentrated in the homepage (65 visits, 48% of all organic). The pages that
carried the spike have lost their positions — most tellingly
`/my-tooth-is-turning-black-how-can-a-dentist-help/` holds **87 keywords but returns only 12
visits**, and `/things-to-do-in-agoura-hills-outdoor-adventures-and-small-town-charm/` is
down to 18.

**Do:** pull GSC for the two URLs above, confirm whether this is a core-update hit or a
SERP-layout change; refresh and re-internally-link both posts; re-check in 2 weeks.
Local is healthy (SoLV 44.01, "emergency dentist near me" +4.13) — do not touch GBP.

### 1.2 Pearl Dental Group — largest absolute loss in the portfolio
| | Apr | May | Jun | Jul | **Aug** |
|---|---|---|---|---|---|
| Keywords | 6,780 | 7,779 | 7,158 | 6,777 | **6,715** |
| Traffic | 15,044 | 12,911 | 8,323 | 5,843 | **4,143** |

**−72% since April — about 11,000 visits/month gone.** A steady four-month bleed, not a
single event. This is by far the biggest account by volume in the roster.

Money pages are commercial-intent cost guides: `/zirconia-bridge-price-guide/` (1,119),
`/zirconia-full-arch-cost/` (606), `/dental-implants/dental-implant-cost-calculator/` (515).

It is also the **least managed** account: no Local Falcon campaign, no `clients/` folder,
no monthly report ever published, 0 blogs assigned, still flagged `newLaunch` in the tracker.

**Do:** treat as an escalation. Onboard properly (LF campaign + Semrush project + monthly
report), then diagnose the four-month decline against the cost-guide cluster.

### 1.3 AV Dental Wellness Group — −82% and unreported for four months
| | Apr | May | Jun | Jul | **Aug** |
|---|---|---|---|---|---|
| Traffic | 2,149 | 1,275 | 649 | 1,251 | **389** |

August alone is −69%. Meanwhile `clients/av-dental-wellness-group/` contains only
`april-2026.html` — **May, June and July were never published.** The client has been
bleeding through the exact window in which we stopped reporting.

Local is also weak: SoLV 5.79, "dentist in lancaster" 2.48 (−0.83), "emergency dentist in
lancaster" **SoLV 0.00 across all 9 scans**.

**Do:** diagnose the decline, then publish May–August together with an honest note.

### 1.4 Beverly Hills Cosmetic Dentistry — map presence gone, site is fine
Campaign: **ARP 21.00 · ATRP 21.00 · SoLV 0.00** — invisible across the grid.

| Keyword | ARP | SoLV | SoLV move |
|---|---|---|---|
| cosmetic dentist beverly hills | 5.23 | 11.57 | **−54.55** |
| dentist in beverly hills | 20+ | 0.00 | 0.00 |
| emergency dentist in beverly hills | 20+ | 0.00 | 0.00 |
| dentist near me | 20+ | 0.00 | 0.00 |
| emergency dentist near me | 20+ | 0.00 | 0.00 |

The one keyword where they ranked at all lost 54 points of share this month.

The GBP itself is **live and healthy** — verified, linked, 5.0★. And organic is the portfolio's
best improvement: **60 → 116 visits (+93%)**, 413 → 523 keywords. So the website is winning
and the profile is losing.

The likely lever is review volume: **73 reviews** in the most competitive cosmetic-dentistry
market in the country, where grid leaders carry several hundred.

**Do:** review-generation campaign as first priority; audit categories/services against the
top-3 grid holders for "cosmetic dentist beverly hills". Do not spend content hours here.

### 1.5 Confidential client reports are publicly indexable
**156 of 209 report pages carry no `noindex`.** `robots.txt` contains only a `Crawl-delay` —
no `Disallow`.

```
User-agent: *
Crawl-delay: 3
```

Only the two hub pages (`index.html`, `clients/index.html`) and a partial set of recent
monthly reports are protected. The tag was added to the template at some point but never
backfilled — so most April/May/June reports and all 50+ audit reports under `reports/` are
crawlable at `dentist-nerds-smart-dental-marketing.github.io`, exposing client names,
traffic figures, revenue estimates and competitor analysis.

**Do:** add `Disallow: /` to `robots.txt` and backfill the `noindex` meta across all 156 files.
Mechanical fix, ~10 minutes.

---

## 2. High priority

| # | Client | Problem |
|---|---|---|
| 2.1 | **Seren Advanced Dentistry Oxnard** | Worst combined position. Organic **48 → 15 (−69%)** in Aug; 421 keywords producing 15 visits. Local: SoLV 0.42, ARP 15.33, all four keywords at 20+ ATRP. No visibility on either channel. |
| 2.2 | **Pennsylvania Perio & Implants** | Organic collapsed in June (37–41 → 3–4 visits) and never recovered: 221 kw / **4 visits**. Yet Hanover owns the map (SoLV 94.22–100). Total channel disconnect. York is at SoLV 0.42 vs Hanover 94.22 — the second location is unworked. |
| 2.3 | **Westwood Oralux** | 98 keywords, **0 organic traffic**, Semrush rank 14.3M. "dentist in westwood" ARP fell to 20.00 (**−8.00**), SoLV 0.00. New site, but foundationally invisible. |
| 2.4 | **Woodland Hills Family Dentistry** | Steady organic bleed **888 → 282 (−68%)** since April. Maps are excellent (SoLV 100 / 96.69), so this is purely organic. Its Local Falcon campaign is **paused**. |
| 2.5 | **Fullerton Smile Dentistry** | Weakest local presence among established accounts: SoLV 1.24, ARP 15.14. "emergency dentist in fullerton" and "emergency dentist near me" both SoLV 0.00. Organic 262 kw / 35 visits. |
| 2.6 | **Smile Tustin** | "emergency dentist in tustin" **SoLV −31.40** (95 → 63.64), ARP −1.17. Sharp single-keyword local loss. Organic is fine (+62%) — this is a GBP/proximity issue. |
| 2.7 | **Cameron Park Family Dentistry** | Organic **1,562 (May) → 425 (−73%)**. Maps excellent (SoLV 85.74). Organic-only problem. |
| 2.8 | **San Juan Family Dentistry** | **269 → 128 (−52%)** since April. SoLV 99.17 on the city term but **0.00 on both emergency terms** — a whole intent category unclaimed. |

---

## 3. Slow decliners — watch

| Client | Organic (Apr → Aug) | Note |
|---|---|---|
| Malibu Dentistry | 781 → 328 (−58%) | Perfect 100% SoLV on all 3 keywords — local is maxed, organic is the gap |
| Torrance Dental Spa | 405 → 167 (−59%) | Recovering: +18% in Aug, "dentist in torrance" SoLV **+17.35** |
| West Hollywood Dental Studio | 433 → 190 (−56%) | +28% in Aug, but all local SoLV 0.00–1.65 |
| Canyon Country Dental Care | 1,223 (May) → 587 (−52%) | SoLV 99.17 on "emergency dentist in canyon country" |
| Smile Spa Camarillo | 542 → 306 (−44% in Aug) | Local weak: SoLV 3.72 |
| Orthodontics in Woodland Hills | 483 → 450 (−7%) | Maps dominant (SoLV 93–100). Low concern |

---

## 4. Winners — use these in reporting

| Client | Result |
|---|---|
| **AZ Dental Laguna Hills** | "emergency dentist in laguna hills" **SoLV +45.45** (26.45 → 71.90), ARP +2.33 — best local gain of the month |
| **Beverly Hills Cosmetic** | Organic **+93%** (60 → 116 visits) |
| **OC Perio & Implants** | 1,577 visits (+78%); SoLV 83.47; "periodontics in mission viejo" SoLV 100 |
| **Gardena Dental Group** | **1,744 visits** — best organic in the portfolio; SoLV 60.95 |
| **Foothill Ranch Dentistry** | 156 → 330 organic; SoLV 100 on "dentist in foothill ranch" |
| **Torrance Dental Spa** | "dentist in torrance" SoLV **+17.35**, ATRP +3.97 |
| **Woodland Hills Family** | "emergency dentist near me" SoLV **+14.05** |
| **Malibu Dentistry** | ARP 1.00 / SoLV 100.00 on all three keywords — total map dominance |
| **Smile Tustin** | Organic +62% (251 → 406) |
| **Valencia Aesthetic** | 1,332 visits |

---

## 5. Operational gaps

**5.1 — 21 of 32 SEO clients have no Semrush project.** Only 17 projects exist, and five of
those are not current SEO clients (Saddleback Valley Endodontics, Marconi Dental Group,
Rod Gleave DMD, Rancho Cucamonga Dentistry, Tustin Aesthetic Dentistry). Everyone without a
project has no Site Audit, no Position Tracking and no Backlink Audit — including Gardena,
OC Perio, Perio Implant Health, Woodland Hills, Exceptional, Malibu, Smile Tustin, Valencia,
The Smile Spa, Pennsylvania Perio, San Juan, Elite, Torrance, West Hollywood, Camarillo,
Canyon Country, Cameron Park, Seren Oxnard, Orthodontics WH, All Smiles, Fullerton.

**5.2 — 3 Local Falcon campaigns are paused:** Woodland Hills Family Dentistry,
Exceptional Dentistry (last run ~3 Jun), All Smile Dental Studio (last run ~2 Jul).

**5.3 — 2 SEO clients have no local rank tracking at all:** Pearl Dental Group and
Smile Santa Maria. Both have one-time audits under `reports/` but were never onboarded to
Local Falcon or monthly reporting.

**5.4 — Four wrong domains in `internal-clients.html`.** Anyone pulling data from the
tracker for these gets zeros:

| Client | Tracker says | Semrush result | Actual domain (GBP + reports) |
|---|---|---|---|
| All Smile Dental Studio | `allsmilesds.com` | 4 kw, 0 traffic | `encinitasallsmilesdental.com` (881 kw, 147) |
| Camarillo Dental Spa | `camarillosmiledentistry.com` | **NOTHING FOUND** | `camarillocosmeticdentistry.com` (226 kw, 306) |
| 2C Dentistry | `2cdentistry.com` | 5 kw, 0 traffic | `dentistoflagunaniguel.com` (28 kw, 41) |
| Lava Dental | `lava.dental` | 40 kw, 0 traffic | `lavadentalhouston.com` (81 kw, 76) |

**5.5 — Reporting gaps:** `av-dental-wellness-group` missing May/June/July;
`seattle-biomimetic-dentistry` missing July.

**5.6 — `clients/test/` is live in production.** Contains a real Pennsylvania Perio report
(`april-2026.html`) and a third-party page titled "Monterey Dental Contours — Website Quality
Audit | WEBRIS". Not linked from the index, but publicly crawlable. Delete.

**5.7 — August reports are due.** 33 client reports to generate; the month closes in 3 days.

---

## 6. Suggested order of work

1. Add `Disallow: /` + backfill `noindex` across 156 files, delete `clients/test/` — §1.5, §5.6
2. Fix the four wrong domains in `internal-clients.html` — §5.4
3. Escalate Pearl Dental Group; onboard it properly — §1.2
4. Diagnose The Smile Spa and AV Dental; publish AV's May–July backlog — §1.1, §1.3
5. Launch review generation for Beverly Hills — §1.4
6. Un-pause the three Local Falcon campaigns; add campaigns for Pearl and Smile Santa Maria — §5.2, §5.3
7. Create Semrush projects for the 21 clients without one — §5.1
8. Work the §2 list: Seren Oxnard, Pennsylvania Perio, Westwood Oralux, Woodland Hills, Fullerton, Smile Tustin, Cameron Park, San Juan
9. Generate the 33 August reports — §5.7
