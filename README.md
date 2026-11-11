# Investor updates: a Claude skill for founders

Turn your monthly numbers into a short founder letter that investors and VCs actually read, in about 5 minutes a month.

You drop in your monthly report (PDF or spreadsheet). Claude asks at most 3 quick questions, then writes:

1. **The letter**, ready to send and to forward: highlights, treasury, traction month on month, product, team, an honest reflection, and 1 to 3 concrete asks.
2. **A short second email** that sends your full report only to your main investor contact, so the detailed numbers are never forwarded.

## What a skill is

A Claude skill is a small instruction pack you add to your Claude account once. After that, Claude knows how to do this task in a fixed format and tone, every time you ask.

## Install (once)

1. Download `investor-updates.zip` from this repo (or zip the `investor-updates` folder yourself).
2. In Claude, open Settings, then Capabilities, then Skills, and upload the zip.
3. Open a new chat and type **setup**. Claude asks for your company name, who signs, who receives the letter, your recipient list and the KPIs you track, and saves them.

## Use (every month)

1. Open a new chat, attach this month's report and type **monthly update**. If you have last month's letter, paste it too, so the letter shows the change vs last month.
2. Answer Claude's questions (at most 3). Type **skip** for any you don't have. Claude never guesses a number.
3. Copy the two emails it writes, check the one line of gaps under them, and send.

## Commands

- **setup**: set or change your settings.
- **add Name, Fund, email**: add people to the recipient list (several at once is fine).
- **remove Name**: take someone off the list.
- **list**: show your settings and recipient list.

## Principles

- Every number comes from your report or from you. Missing means left out, never guessed.
- Same KPIs and definitions every month, so trends show.
- Optimistic and true: lead with the win, and put every problem next to its fix and a date.
- Readable on a phone in 2 minutes, and written to be forwarded.
- Pricing, margins by line, bank balances, disputes and anything on your never-share list stay out of the letter.

## Privacy

The skill contains instructions only, with no company data. Your settings and recipient list live in your own Claude account (memory or Project instructions), not in this repo.

## License

MIT. See `LICENSE`.
