---
name: vet-repo
description: Use before doing any work on a repository you do not own - checks whether it accepts external pull requests, whether it requires an issue first, and what its policy on AI-assisted contribution says.
---

# Vetting a repository before you work on it

Run this before reading the code, before forking, before opening an issue.
Work done on a project that does not accept it is work thrown away.

## Step 1: read the pull request template first

Not `CONTRIBUTING.md`. The template.

Restrictions get buried there, sometimes inside an HTML comment that renders
as nothing. Fetch and read all of these, in this order, and stop at the first
that says the project is closed to outside pull requests:

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE.md`

If the project is closed, say so and stop. Do not fork. Do not read the code.
Report what the project asks for instead, which is usually an issue.

## Step 2: check the dataset

Every path in this skill (`data/repos/...`, `scripts/measure.py`, ...) is
relative to this plugin's own directory, not to whatever project you are
currently working in. Once this skill is installed as a plugin, your
working directory is the user's project, and those paths resolve to
nothing there. Find the plugin's root first: this file lives at
`skills/vet-repo/SKILL.md` inside it, so the root is two directories up
from wherever you read this file. Resolve every relative path below, and
run every command below, from that root -- `cd` there first, or prefix
each path with it.

Look for `data/repos/<owner>__<name>.json` there.

A recent `measured_at` only means the statistics were recomputed recently
-- the weekly refresh re-checks that already-quoted text is still present
and recomputes statistics, but it does not re-read a project's files
looking for a rule that is new since the entry was written (see
`METHODOLOGY.md`). Treat the dataset entry, if present, as a starting
point and a set of quotes to check, not a substitute for Step 3. If
anything in this vetting matters to you -- it usually does -- read the
policy files yourself rather than trusting the date.

If there is no entry yet, measure one:

    python scripts/measure.py owner/repo

This needs `GITHUB_TOKEN` set in the environment. Unauthenticated requests
are capped at 60 an hour, and a single measurement uses several of them.

## Step 3: read the policy files

- `ai_policy.md`
- `AGENTS.md`, `CLAUDE.md`
- `CONTRIBUTING.md`

Answer four questions, and quote the line you answered from:

1. Does it accept external pull requests?
2. Does it require an issue to be opened, or claimed, before a pull request?
3. What does it say about AI-assisted code?
4. What does it say about AI-written pull request text?

Question 4 is separate from question 3 on purpose. A project can welcome
AI-assisted code and still require that the pull request description be
written by a person.

## Step 4: report, in this order

1. Whether external pull requests are accepted, with the quote.
2. Whether an issue is required first, with the quote.
3. The two AI positions, with the quotes.
4. The statistics, last: casual-author acceptance, median and p90 days to
   merge, and `median_close_age_days` -- how many days separate the
   newest closed pull request in the sample from the median one, which is
   how stale or fresh the sample actually is.

The statistics go last because they are the least useful part. A project with
a 90 percent acceptance rate that bans agent-authored pull requests is a
project you should not open one on.

## What this skill will not do

It will not tell you whether your change is likely to be merged. Nobody can.
It tells you what the project asks for, so you can decide.
