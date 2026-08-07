# Contributing

merge-odds grows one project at a time, added by people who read that project's own files and write down what they say.

## Adding a project

1. Pick a project nobody has measured yet.
2. Run: `python scripts/measure.py owner/repo --write`
3. Open the generated file. It has a `_review` block with three keys. `candidates` are the quotes the scanner found; read each one in its source file, not just the quote in the JSON, since a sentence can reverse meaning two lines later. Then decide the four policy values and move the quotes you actually used into `evidence`. `unmatched_claims` lists claims the scanner found nothing for. That silence is not evidence of a permissive policy, so go read the relevant files yourself before accepting the default. `files_read` is what the scanner already fetched, a starting point if you need to look further. When you are done, delete `_review`. CI rejects any file that still has it.
4. Open a pull request. One project per pull request.

## Review

Expect a first response within 72 hours.

## One project per pull request

Keep each pull request to one project. Two people adding different projects will not conflict with each other if they never touch the same file, and one file per pull request is what keeps that true.
