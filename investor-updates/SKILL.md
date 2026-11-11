---
name: investor-updates
description: Turn a startup's monthly numbers (a management report, board pack, PDF or spreadsheet) into a short, optimistic, VC-ready founder letter, plus ready-to-send emails. Use when a founder shares their monthly report or says "monthly update", "investor update" or "setup".
---

# Monthly investor update

You help a founder turn their monthly numbers into a letter that investors and VCs love to read, and the emails to send it. Aim for 5 minutes of founder time a month.

## Setup (run once, then saved)

A skill cannot save files by itself, so the settings live in Claude's memory, or in the instructions of a Claude Project if the founder uses one.

**"setup"**: ask once, in one message, for:

1. Company name, and who signs the letter (one or more founder names).
2. Who sends, who is on copy, and the main investor contact who receives it first (name and email).
3. The recipient list: existing investors and future-round candidates, each as "Name, Fund, email".
4. The 3 to 6 KPIs the company runs on (for example revenue, recurring revenue, volume, customers, retention), with how each is defined.
5. Anything that must never appear in the letter (for example pricing, margins or a partner's name).

Then print the settings as one block titled "Investor update settings" and save it to memory. If memory is off, tell the founder in one line to paste the block into the Project instructions, or to paste it with each month's report.

**Other commands:**

- **"add Name, Fund, email"** (one or several): add them to the recipient list, skip duplicates, save, and print the updated list with the count. Example: "add Jane Doe, Fund Name, jane@fund.example".
- **"remove Name"**: remove them, save, and print the updated list.
- **"list"**: print the current settings and recipient list.

No saved settings on a monthly run: ask for them first, then continue.

## Monthly run

**Inputs.** Required: this month's report. Optional: last month's letter (to show the change vs last month) and news since month-end. No last month's letter? Use last month's column in the report if it has one. Otherwise leave the change out. Never guess it.

1. Read the report fully. Pull out the saved KPIs.
2. Ask the founder **one message with at most 3 short questions**, only for what the report cannot answer. Usually:
   - Cash and runway (if the report does not show them).
   - 1 to 3 dated milestones for next month, whether last month's landed, and whether to mention a fundraise.
   - News since month-end (customers, launches, hires), and who they would most like to be introduced to.
   If they say "skip", leave out what is missing.
3. Write the letter (shape below).
4. Output the emails (format below), ready to copy and send. Nothing else.

## Letter shape

Subject: `{Company} | {Month Year} investor update`

1. Greeting: "Dear investors and friends,"
2. One line: the month in one sentence, leading with the best news.
3. **Highlights**: 3 to 6 bullets with the best numbers of the month. Say each number once: later sections add detail, not repeats.
4. **Treasury**: cash, monthly burn (or "profitable"), runway in months.
5. **Traction**: each saved KPI as value plus the change vs last month.
6. **Product and go-to-market**: what shipped or is shipping, and new customers and partners. Link each one's website if the founder gives it.
7. **Team**: only if someone joined or left.
8. **Market and regulation**: only if something moved.
9. **Up next: {next month}** (for example "Up next: March"): news since month-end, only if there is some.
10. **Fundraising**: only if the founder said to mention it. Timing and purpose, no amount unless the founder gives one.
11. **Honest reflection**: one short paragraph. Name what is not working, then the fix and when.
12. **How you can help**: 1 to 3 asks, each naming exactly who to introduce. Use the founder's answer. If none, propose asks from the month and flag them in the gaps line.
13. Close with one standing line (for example "Thanks for being on this ride."), signed with the saved founder names.

## Voice

- Founder-written, first person ("we"). It should sound like the founder on a good day.
- Short paragraphs and short sentences. Plain words, no jargon walls.
- Optimistic without hype: celebrate the progress, then state the ask.
- No filler. Never "excited to share", "thrilled" or "game-changing".
- Numbers sit next to their label ("Revenue: {value} (+{x}%)"), so a phone reader can scan them.
- Same standing close every month, so the letter feels familiar.

## Rules

- Every number comes from the report or the founder. Simple arithmetic on those numbers is fine (sums, differences, x12). If you do not have a number, leave it out.
- Use the same KPIs and definitions every month, so trends show.
- Show profit once, in plain terms ("profit after operating expenses"). If the report has a label that reads like profit but is not (for example a margin before operating expenses), do not list it next to the real one. If you quote it, say what it excludes.
- "Annualized" means this month times 12, labelled that way. Never call it ARR or MRR unless it is recurring revenue.
- Be optimistic and true. Lead every section with the win. Put every problem next to its fix and a date. A fix with no date: state the fix, and list the missing date in the gaps line.
- Keep out of the letter: customer pricing, margins by product line, bank balances line by line, receivables, open disputes or losses under review, deals not yet signed that a partner has not agreed to announce, and anything on the saved never-share list.
- The letter must be clean and final: no brackets, placeholders, notes to the founder or questions in it. Anything missing goes only in the gaps line under the emails.
- Short paragraphs, readable on a phone in 2 minutes. Skip empty sections.
- Write it as if it will be forwarded to a VC the founder has never met, because it will be.

## Email output (exact format)

Two emails, each ready to copy.

**Email 1, the letter** (no attachment, because it will be forwarded):

```
To: {main investor contact}
Cc: {who is on copy}
Bcc: {everyone on the recipient list}
Subject: {Company} | {Month Year} investor update

{the letter}
```

**Email 2, the report, for the main investor contact only:**

```
To: {main investor contact}
Subject: {Company} | {Month Year} report (not for forwarding)
Attach: this month's report

Hi {first name}, here is the report behind this month's letter.
```

Under the emails, list in one line anything you left out because it was missing, so the founder can add it before sending.

See `template.md` for the shape of a finished letter.
