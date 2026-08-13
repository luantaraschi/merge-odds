# merge-odds

merge-odds answers one question, one project at a time: does this project accept pull requests from people outside its core team, and under what rules.

Maintainers in 2026 spend real hours closing pull requests they never asked for, many of them written by an agent that never read the file explaining the project's rules. A lot of that work should not have started at all. The project already said no, or said "open an issue first," or said "not AI-written text," in a file sitting in its own repository. Nobody checked before the work began. merge-odds reads those files, once per entry, and writes down exactly what they say. Where the project's rule departs from the default of "open, no issue required, nothing said about AI" -- the entry carries a quote taken word for word and a link that pins it to a specific commit. Where nothing in the files read said otherwise, the entry records the default, which means "no restriction found," not "permission granted."

## Reading the table

Column order is deliberate. The first four columns after the project name are policy, read straight from the project's own files: whether it accepts external pull requests, whether it wants an issue opened first, and what it says about AI-assisted code and about AI-written pull request text, listed as two separate claims because a project can allow one and forbid the other. The columns after that are statistics from a sample of the 100 closed pull requests the project most recently touched, which is the closest the GitHub API can get to "most recently closed": it can sort by when a pull request was last updated, not by when it was closed. `Sample recency` reports how many days separate the newest close in the sample from the median close, so a stray old pull request that got a late comment cannot pass itself off as recent activity. `Median` and `p90` are not computed over the whole sample: they cover only the merged pull requests from casual outside authors, the same group `Casual acceptance` is drawn from, since a regular committer's merge speed says nothing about how long an outside pull request waits. Policy comes first because it is what the project asked for, in its own words. The numbers come after because they describe a sample of other people's past pull requests, not a promise, and not a forecast for yours.

Where a policy cell links to text, the link goes to a quote it was read from, pinned to the commit it was read at. Where a claim rests on more than one quote, the link goes to the last one, since that is the one carrying any condition that qualifies an earlier-stated permission. A cell with no link means the entry found nothing in the project's files that departed from the default for that claim -- not that the project said yes.

<!-- merge-odds:table:start -->
| Project | External PRs | Issue first | AI code | AI PR text | Casual acceptance | Median | p90 | Sample recency | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [directus/directus](https://github.com/directus/directus) | yes | — | [conditional](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L21-L22) | [disallowed](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L29-L30) | 0.33 | 4.09 d | 49.65 d | 51.45 d | 2026-08-07 |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | yes | [yes](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L451-L458) | [conditional](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L503-L504) | [disallowed](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L505-L506) | 0.47 | 0.57 d | 2.88 d | 0.81 d | 2026-08-07 |
| [payloadcms/payload](https://github.com/payloadcms/payload) | yes | — | — | — | — | — | — | 3.46 d | 2026-08-07 |
| [prisma/prisma](https://github.com/prisma/prisma) | yes | [yes](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L17) | [allowed](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L118) | — | — | — | — | 6.8 d | 2026-08-07 |
| [strapi/strapi](https://github.com/strapi/strapi) | yes | — | — | — | 0.41 | 5.99 d | 67.64 d | 6.41 d | 2026-08-07 |
| [supabase/supabase](https://github.com/supabase/supabase) | yes | [yes](https://github.com/supabase/supabase/blob/6c0439ace812f134859a825e421f5f241cbf01b3/CONTRIBUTING.md#L23) | — | — | 0.9 | 0.92 d | 10.73 d | 1.78 d | 2026-08-07 |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | yes | — | — | — | — | — | — | 1.65 d | 2026-08-07 |
| [withastro/astro](https://github.com/withastro/astro) | yes | — | — | — | 0.56 | 3.26 d | 15.08 d | 9.96 d | 2026-08-07 |
<!-- merge-odds:table:end -->

## How an entry is built

```
scripts/measure.py <owner/repo>
        |
   github.py ........ the only module that touches the network
        |              repo metadata, default branch sha,
        |              100 most recently updated closed PRs,
        |              raw contents of each candidate policy file
        |
        +--> policy.py ...... regex sweep over the files, returns
        |                     candidate quotes and decides nothing
        +--> prs.py ......... pure statistics over the sample
        |
   entry.py ......... assembles JSON, pins every quote to the sha
        |
   data/repos/<owner>__<repo>.json
        |
   scripts/render.py  regenerates the table above, in place
```

The table in this README is generated. `render.py` splices it between the two
HTML comment markers, and CI fails if a committed README disagrees with the
data it claims to display, so the table cannot silently drift from
`data/repos/`.

## Engineering Highlights

### The regex proposes; a person decides

Reading a project's contributing policy is a judgement call. "We welcome
contributions" three paragraphs above "we are not accepting new features"
means the second one. Automating that judgement produces a dataset that is
confidently wrong.

So the split is enforced in the code. `policy.py` opens with the line
`"Finds candidate policy statements. Decides nothing."` and it means it: it
sweeps a fixed list of candidate files, `ai_policy.md`, `AGENTS.md`,
`CLAUDE.md`, `CONTRIBUTING.md`, pull request templates, `README.md`, against
per claim regex patterns, and returns the passages it found with their line
ranges. What each passage *means* is decided by the person adding the entry,
and the quote they pick is stored word for word.

Quotes are capped at 600 characters and 8 lines. A quote long enough to need
summarizing is not evidence any more.

### Evidence pinned to a commit, and re-verified rather than trusted

Every quote is stored with the repository's `default_branch_sha` at the moment
it was read, and `entry.py` builds a permalink to `blob/<sha>/<path>#L21-L22`.
A reader can click a claim and land on the exact lines it came from, as they
were, even if the file has since been rewritten.

`validate_data.py` then re-fetches each quoted range at its pinned sha and
checks the text is still there verbatim. This runs in CI on every changed
entry, so a typo in a quote or a hand edited line range fails the pull request
rather than becoming part of the dataset.

### Numbers refuse to appear when the sample is too thin

The temptation with a scraped statistic is to publish whatever the arithmetic
produced. `prs.py` sets explicit floors instead: `MIN_HUMAN_SAMPLE = 20` and
`MIN_CASUAL_SAMPLE = 20`, below which a percentage is documented as noise and
withheld. That is why several rows in the table above have a policy but no
acceptance rate: the sample did not support one, and the honest output is a
blank cell.

Defining an outsider is the other half of it. `CASUAL_MAX_APPEARANCES = 2`
means an author appearing more than twice in the sample of 100 is a regular,
not someone passing through, and their merges are excluded from a statistic
meant to describe outsiders. Bots are excluded by a frozen login list plus
GitHub's own bot flag, so `dependabot` does not inflate anyone's acceptance
rate.

`prs.py` is documented as "pure functions, no network", which is what lets all
of this be tested against fixtures rather than against GitHub.

### One module owns the network, and it retries

Every HTTP call is confined to `github.py`. It retries up to 4 attempts, waits
out secondary rate limits with a 900 second ceiling so a job cannot hang
indefinitely, and distinguishes a clean 404 (`RepoNotFound`, meaning the
repository is gone) from any other failure (`GitHubUnavailable`, meaning try
later). That distinction matters at refresh time: a project that disappeared
should be marked, a project behind a flaky API should not be.

### A weekly refresh that will not touch a quote

`refresh.py` opens with `"Re-measure every entry weekly. Never rewrites a
quote."` The scheduled workflow recomputes the statistics and re-checks that
the already quoted lines are still present. It does not re-read a project's
files hunting for a rule that appeared since the entry was written.

This is a deliberate limit, and it is stated in the table's own Limitations
section rather than buried here: a `Measured` date advancing every week proves
the numbers were recomputed, not that the policy was re-read.

The workflow pins every action to a full commit sha rather than a tag, and
declares least privilege `permissions:` per job. `validate.yml` gets
`contents: read` and nothing else.

## Tech Stack

| Layer | Choice | Role in this project |
|---|---|---|
| Language | Python 3.11+ | Two runtime dependencies total |
| HTTP | requests | The GitHub REST and raw content APIs |
| Validation | jsonschema, Draft 2020-12 | Entry shape enforced in CI |
| Tests | pytest | 109 cases against recorded fixtures |
| CI | GitHub Actions | Validate on PR, refresh weekly |
| Data | One JSON file per project | Diffable, reviewable, no database |

## Testing & Reliability

`python -m pytest -q` runs 109 tests, all passing, across 10 files covering
every module: policy pattern matching, the statistics and their sample floors,
the GitHub client's retry and error branches, entry serialization, the
renderer, the schema itself and the validator.

None of them touch the network. `tests/fixtures/` holds recorded API payloads
and sample entries, so the suite is deterministic and runs in well under a
second.

Beyond unit tests, `validate.yml` enforces three things on every pull request:
the entries changed in that PR pass schema and live quote verification, the
README table matches the data (`render.py --check`), and the whole suite
passes. When it cannot determine a diff base, it falls back to validating
every entry rather than none, which is the safe direction.

## Running Locally

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Reading the dataset needs nothing installed. Measuring or validating needs the
package plus a `GITHUB_TOKEN` in the environment for a usable API rate limit:

```bash
python scripts/measure.py owner/repo    # writes data/repos/owner__repo.json
python scripts/validate_data.py         # schema, pairing, verbatim quotes
python scripts/render.py                # regenerate the table in this README
```

## Limitations

Each entry's statistics come from a sample of 100 closed pull requests, not the project's full history. Policy is read at a specific date against a specific commit; a project can change its rules the day after an entry is measured. The weekly refresh recomputes the statistics and re-checks that each already-quoted line of policy text is still there -- it does not re-read a project's files looking for a rule that is new since the entry was written, so a `Measured` date advancing every week is not proof the policy was re-read, only that the statistics were. No number in this table predicts what will happen to any single pull request. A high acceptance rate describes a hundred people who are not you.

## Installing the `vet-repo` skill

This repository is also a Claude Code plugin, built around the `vet-repo`
skill under `skills/vet-repo/`.

- **As a plugin:** `/plugin marketplace add luantaraschi/merge-odds`, then
  `/plugin install merge-odds`.
- **By cloning:** `git clone` this repository. The skill and its data
  live entirely inside it.

Either way, reading the dataset itself needs nothing extra. Running
`scripts/measure.py` or `scripts/validate_data.py` needs Python 3.11 or
later and `pip install -e .` from this repository's root first; neither
the plugin install nor a bare clone installs those dependencies for you.

`skills/vet-repo/SKILL.md` explains that the paths it uses
(`data/repos/...`, `scripts/measure.py`) are relative to this repository's
own root, not to the project you happen to be working in when you invoke
the skill.

## Contributing

To add or correct an entry, see [`CONTRIBUTING.md`](CONTRIBUTING.md). The
method behind the measurements is written up in
[`METHODOLOGY.md`](METHODOLOGY.md).

## License

Code under MIT, see [`LICENSE`](LICENSE). The dataset in `data/` carries its
own licence in [`data/LICENSE`](data/LICENSE).
