#!/usr/bin/env python3
"""Generate the monthly client cover emails for Renato.

    python3 tools/gen-client-emails.py <month-year> <contacts.json> [out.md]
    e.g.  python3 tools/gen-client-emails.py september-2026 ~/contacts.json drafts.md

contacts.json maps client slug -> recipient address(es). Keep it OUTSIDE this repo:
everything committed here is served publicly at reports.dentistnerds.com, and client
email addresses must not be published. The manifest holds names only, never addresses.
"""
import json, sys, os, io

month_slug = sys.argv[1]                       # e.g. september-2026
contacts   = json.load(open(sys.argv[2], encoding="utf-8"))
out_path   = sys.argv[3] if len(sys.argv) > 3 else "client-emails-%s.md" % month_slug

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man  = json.load(open(os.path.join(root, "clients/clients.json"), encoding="utf-8"))
month_name = month_slug.replace("-", " ").title().replace(" 20", " 20")
mon, yr = month_slug.split("-"); month_name = mon.capitalize(); year = yr

BODY = """Hello {greeting},

This report analyzes your organic SEO performance for {month} {year}. We evaluate keyword \
rankings, traffic, backlinks, Google Maps rankings, and activity including calls, to provide \
the key insights inside.

SEO Report: {practice} — {month} {year}
{url}

Over the coming month we will continue publishing optimized blog content to improve visibility \
across both AI-powered platforms and search engines, expanding and enhancing your treatment \
pages, and identifying and securing high-quality backlinks from reputable websites and local \
business directories to grow your referring domain count. This strategy is designed to \
strengthen your Authority Score, improve organic search rankings, and enhance visibility across \
both traditional search engines and AI-driven discovery platforms.

Thank you for your continued partnership.

Best regards,
Renato
Dentist Nerds"""

out, skipped = [], []
out.append("# Client report emails — %s %s\n" % (month_name, year))
out.append("Generated from `clients/clients.json` plus a local contacts file. "
           "Addresses are not stored in the repo.\n")
for c in sorted([c for c in man["clients"] if c.get("active")], key=lambda x: x["name"].lower()):
    slug = c["slug"]
    rel  = "clients/%s/%s.html" % (slug, month_slug)
    why  = []
    if not os.path.exists(os.path.join(root, rel)): why.append("no %s report" % month_slug)
    if not c.get("contact_greeting"):               why.append("no greeting on file")
    if slug not in contacts:                        why.append("no email address on file")
    if why:
        skipped.append((c["name"], slug, "; ".join(why))); continue
    out.append("\n---\n")
    out.append("## %s\n" % c["name"])
    out.append("**To:** %s  " % contacts[slug])
    out.append("**Subject:** SEO Report by Dentist Nerds — %s %s\n" % (month_name, year))
    out.append("```")
    out.append(BODY.format(greeting=c["contact_greeting"], month=month_name, year=year,
                           practice=c["name"],
                           url="https://reports.dentistnerds.com/" + rel))
    out.append("```")
if skipped:
    out.append("\n---\n\n## Not generated — needs attention\n")
    for n, s, w in skipped: out.append("- **%s** (`%s`) — %s" % (n, s, w))
io.open(out_path, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote %s — %d drafts, %d skipped" % (out_path, len([l for l in out if l.startswith("## ")]) - (1 if skipped else 0), len(skipped)))
for n, s, w in skipped: print("   skipped:", n, "|", w)
