# Monthly report — client email template

What Renato sends once a month's report is live and reviewed. Keep it short: the report
does the talking, this just gets them to it.

Placeholders: `{greeting}` `{practice}` `{month}` `{year}` `{report_url}` `{sender}`

---

**Subject:** SEO Report by Dentist Nerds — {month} {year}

> Hello {greeting},
>
> This report analyzes your organic SEO performance for {month} {year}. We evaluate keyword
> rankings, traffic, backlinks, Google Maps rankings, and activity including calls, to provide
> the key insights inside.
>
> **SEO Report:** [{practice} — {month} {year}]({report_url})
>
> Over the coming month we will continue publishing optimized blog content to improve visibility
> across both AI-powered platforms and search engines, expanding and enhancing your treatment
> pages, and identifying and securing high-quality backlinks from reputable websites and local
> business directories to grow your referring domain count. This strategy is designed to
> strengthen your Authority Score, improve organic search rankings, and enhance visibility
> across both traditional search engines and AI-driven discovery platforms.
>
> Thank you for your continued partnership.
>
> Best regards,
> {sender}
> Dentist Nerds

---

## Worked example — Smile Tustin

**Subject:** SEO Report by Dentist Nerds — September 2026

> Hello Dr. Ezzy,
>
> This report analyzes your organic SEO performance for September 2026. We evaluate keyword
> rankings, traffic, backlinks, Google Maps rankings, and activity including calls, to provide
> the key insights inside.
>
> **SEO Report:** [Smile Tustin — September 2026](https://reports.dentistnerds.com/clients/smile-tustin/september-2026.html)
>
> Over the coming month we will continue publishing optimized blog content to improve visibility
> across both AI-powered platforms and search engines, expanding and enhancing your treatment
> pages, and identifying and securing high-quality backlinks from reputable websites and local
> business directories to grow your referring domain count. This strategy is designed to
> strengthen your Authority Score, improve organic search rankings, and enhance visibility
> across both traditional search engines and AI-driven discovery platforms.
>
> Thank you for your continued partnership.
>
> Best regards,
> Renato
> Dentist Nerds

---

## Notes

- **"your" not "our".** The treatment pages, referring domains and Authority Score belong to the
  practice. "our" reads as though the agency owns them.
- **One link only.** Link the dated report (`september-2026.html`), not the folder index — the
  client should land on the month being discussed, not the newest one.
- **Greeting is per-contact.** `{greeting}` is whoever signs off at that practice, usually
  "Dr. <surname>". It is NOT derivable from the practice name, so it lives in
  `clients/clients.json` as `contact_greeting` and has to be filled in once per client.
- Say nothing here that the report contradicts. If a client's month was weak, the report shows
  it; this email should not imply otherwise.
