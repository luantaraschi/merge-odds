---
name: vet-repo
description: Use before doing any work on a repository you do not own. Checks whether it accepts external pull requests, whether it requires an issue first, what its policy on AI-assisted contribution says, and which of its gates would reject the work after it is already written.
---

# Vetting a repository before you work on it

Run this before reading the code, before forking, before opening an issue.
Work done on a project that does not accept it is work thrown away. So is
work on a project you cannot build, and work that a rule nobody read
rejects after it is finished.

Every step below can end the vetting. Stop at the first closed gate,
report it, and do not open the next one. The statistics come last, and
that is deliberate.

Two references sit beside this file, in the `references/` directory next
to it. `references/gates.md` lists the requirements that reject correct
work after it exists, with the cheap check for each.
`references/open-in-practice.md` lists the ways a project can accept
outside pull requests in writing and refuse them in practice. Those two
paths are the only ones here relative to this file. Everything naming the
dataset or a script is relative to the plugin root, which step 5
explains.

## Step 0: can you build it and run its tests

This is the only gate about your own machine rather than the project's
rules, and it is the cheapest, because the answer sits in one file and
reading it needs no clone.

Read whichever the project has: `packageManager` and `engines` in
`package.json`, `requires-python` in `pyproject.toml`, `go.mod`,
`rust-toolchain.toml`, `.tool-versions`.

Then answer one question. Can this be built, and its tests run, here,
today, without installing something the user has not agreed to install? A
toolchain you do not have rejects a project that would have welcomed you,
and saying so before the fork is worth more than finding out after it.

Two shapes are worth naming, both measured in August 2026 on a Windows
machine without administrator rights. pnpm 9 and 10 install, because they
fall back to junctions when symlinks are denied; pnpm 11 and 12 fail with
`os error 1314`, because the newer store needs real symlinks. One field
in `package.json` settles that before the clone. And a missing language
toolchain rejects a whole class at once: no Go on the machine removed
five projects in one afternoon, every one of which had passed every other
gate.

Where a container runtime is available this gate softens rather than
closes. A suite whose CI declares `TZ` or `LANG` is usually cheaper to
run inside the project's own image than to argue with the host operating
system.

## Step 1: read the pull request template first

Not `CONTRIBUTING.md`. The template.

Restrictions get buried there, sometimes inside an HTML comment that
renders as nothing. Fetch and read all of these, in this order, and stop
at the first that says the project is closed to outside pull requests:

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/pull_request_template.md`
- `PULL_REQUEST_TEMPLATE.md`

If the project is closed, say so and stop. Do not fork. Do not read the
code. Report what the project asks for instead, which is usually an
issue.

The template earns its place at the front for a second reason. It is
where a project puts the decisions it wants made before the work exists:
which branch a change targets, whether a fix needs a backport to a
maintenance line, which declarations the author has to sign. Reading it
after the branch is pushed means rewriting the pull request body, or
discovering that the change belongs on a different base.

Some of those declarations cannot be answered by an agent at all. A
checkbox asserting that a human read the full diff, a Developer
Certificate of Origin sign-off, a confirmation that AI-generated content
was reviewed: each is a statement about a person, and only that person
can make it truthfully. Surface them and let them answer. Ticking one on
their behalf puts a false statement inside the contribution itself.

## Step 2: read the policy files

- `ai_policy.md`
- `AGENTS.md`, `CLAUDE.md`
- `CONTRIBUTING.md`

Answer five questions, and quote the line each answer came from:

1. Does it accept external pull requests?
2. Does it require an issue to be opened, or claimed, before a pull request?
3. What does it say about AI-assisted code?
4. What does it say about AI-written pull request text?
5. If assistance is allowed, what disclosure does it require, in what exact form?

Question 4 is separate from question 3 on purpose. A project can welcome
AI-assisted code and still require that the pull request description be
written by a person.

Question 5 is about form rather than permission, and it is the one that
fails by accident. Projects that welcome assistance often specify how it
must be declared, precisely enough that a near miss does not count. Read
the current file for the exact wording rather than trusting any example,
including these three, read in August 2026: one project asked in
`CONTRIBUTING.md` for a commit footer naming the agent and the model, and
gave the literal string to copy; one asked in `AGENTS.md` for an emoji in
the body of every issue, pull request and comment written by an agent;
one asked in its template for a marker in the pull request title. Three
shapes, all mandatory, none of them guessable.

Two answers end the vetting here rather than shaping the work. A project
can forbid AI-assisted contribution outright, and some address the agent
directly, asking it to stop and to remove the project from its list of
targets. When that is what the file says, comply, report the project as
closed to this kind of contribution, and write it down somewhere durable,
so that a later pass over the same numbers does not recommend it again.
Both projects found this way while writing this skill were excellent by
every other measure, which is exactly why they come back.

## Step 3: find the gates that reject finished work

A project can accept outside pull requests, allow assistance, and still
refuse a correct change because of a rule that was not in anything read
so far. Each of these costs a round trip with a maintainer when it is
found late, and some cost the branch.

Read `references/gates.md` for the cheap check on each and what each one
costs when it is found late. The list:

- Which branch a change targets, and whether a maintenance line needs it too
- A contributor license agreement, which can be per organization or per repository
- A Developer Certificate of Origin sign-off
- A verified commit signature, which a sign-off does not satisfy
- Thresholds a correct patch can fail: coverage on the patch, a numeric limit in a linter, a spell checker over tests, a bundle size ratchet
- How the project wants work claimed, where it wants that at all

The first four are signed or decided by the human, not by the agent.

## Step 4: is the door open in practice

Everything so far reads what the project wrote. This step reads what it
does, and it is the one that most often reverses a promising vetting. A
project can accept external pull requests in its own words and still be
closed to you.

Read `references/open-in-practice.md` before answering. The five shapes:

- An interaction limit, which answers `POST repos/OWNER/REPO/pulls` with 404 rather than 403. Cheaper to check by the date of the last pull request from an outside fork
- Outside authors who work there, which no association field will tell you and reading the profiles will
- A triage bot that reproduces the report and writes the failing test, so the work is queued before you arrive
- A rubber stamp, which is acceptance above 90 percent with a p90 under a day
- External merges that are all documentation, which is what the project accepts

The same reference covers the cut that fails independently of acceptance
and queue speed: whether the project has any work available at all.

## Step 5: check the dataset

The dataset and script paths in this skill (`data/repos/...`,
`scripts/measure.py`, ...) are relative to this plugin's own directory,
not to whatever project you are currently working in. Once this skill is
installed as a plugin, your working directory is the user's project, and
those paths resolve to nothing there. Find the plugin's root first: this file lives at
`skills/vet-repo/SKILL.md` inside it, so the root is two directories up
from wherever you read this file. Resolve every relative path below, and
run every command below, from that root. Change into it first, or prefix
each path with it.

Look for `data/repos/<owner>__<name>.json` there.

A recent `measured_at` only means the statistics were recomputed
recently. The weekly refresh re-checks that already-quoted text is still
present and recomputes statistics, but it does not re-read a project's
files looking for a rule that is new since the entry was written (see
`METHODOLOGY.md`). Treat the dataset entry, if present, as a starting
point and a set of quotes to check, not a substitute for steps 1 through
4. If anything in this vetting matters to you, and it usually does, read
the policy files yourself rather than trusting the date.

If there is no entry yet, measure one:

    python scripts/measure.py owner/repo

This needs `GITHUB_TOKEN` set in the environment, and `pip install -e .`
run from this plugin's root first. Unauthenticated requests are capped at
60 an hour, and a single measurement uses several of them.

## Step 6: report, in this order

1. Whether the project can be built and tested here, when the answer is no.
2. Whether external pull requests are accepted, with the quote.
3. Whether an issue is required first, with the quote.
4. The two AI positions, with the quotes, and the disclosure format where one is required.
5. The gates that reject finished work, naming which of them need a decision from the user.
6. Whether the door is open in practice, and what you checked in order to say so.
7. The statistics, last: casual-author acceptance, median and p90 days to merge, and `median_close_age_days`, which is how many days separate the newest closed pull request in the sample from the median one, and therefore how stale or fresh the sample actually is.

The statistics go last because they are the least useful part. A project
with a 90 percent acceptance rate that bans agent-authored pull requests
is a project you should not open one on. A project at 40 percent with a
fast queue and no gate you cannot pass is a better place to spend an
afternoon than a project at 70 percent whose open queue is held by four
people.

## What this skill will not do

It will not tell you whether your change is likely to be merged. Nobody
can. It tells you what the project asks for, so you can decide.

It also will not tell you what to work on once a project passes. That is
a separate decision, with its own ways of wasting a day, and it has its
own skill: `vet-issue`.
