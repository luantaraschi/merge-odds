<p align="center">
  <img src="site/wordmark.svg" width="560" alt="Merge Odds">
</p>

<p align="center"><strong>Read the rules before you touch the repo.</strong></p>

<p align="center">
  <a href="https://luantaraschi.github.io/merge-odds/">Website</a> ·
  <a href="https://github.com/luantaraschi/merge-odds/discussions">Discussions</a> ·
  <a href="#install-the-skills">Install</a> ·
  <a href="METHODOLOGY.md">Methodology</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

<p align="center">
  <img alt="version 0.2.0" src="https://img.shields.io/badge/version-0.2.0-174c3c">
  <img alt="8 measured projects" src="https://img.shields.io/badge/catalog-8_projects-d7ff59?labelColor=111713&color=d7ff59">
  <img alt="Python 3.11 or later" src="https://img.shields.io/badge/python-%3E%3D3.11-174c3c">
  <img alt="MIT license" src="https://img.shields.io/badge/license-MIT-174c3c">
</p>

Merge Odds answers one question, one project at a time: does this project accept pull requests from people outside its core team, and under what rules?

Many repositories have already answered that question in a pull request template, an AI policy, or a contribution guide. Merge Odds reads those files and records what they say. When a rule differs from the dataset default, the entry carries a verbatim quote and a link pinned to the commit where it was read.

The default means that no restriction was found in the files read. It does not mean the project granted permission.

## Read policy before statistics

The first four fields describe the project's published policy:

1. Does it accept external pull requests?
2. Does it require an issue or discussion first?
3. What does it say about AI assisted code?
4. What does it say about AI written pull request text?

The remaining fields describe a sample of recently touched closed pull requests. Acceptance and merge time cover casual outside authors, not regular contributors. These numbers describe other people's past pull requests. They do not forecast yours.

Where a policy cell is linked, the link opens the source text pinned to the commit where it was read. A claim with no link stayed at its default because the files read did not state a restriction.

<!-- merge-odds:table:start -->
| Project | External PRs | Issue first | AI code | AI PR text | Casual acceptance | Median | p90 | Sample recency | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [codeceptjs/CodeceptJS](https://github.com/codeceptjs/CodeceptJS) | yes | [yes](https://github.com/codeceptjs/CodeceptJS/blob/eb1bcdc533b79ae75e21a6ede19afd45f9b06631/.github/CONTRIBUTING.md#L110) | not stated | not stated | not available | not available | not available | 66.42 d | 2026-08-21 |
| [directus/directus](https://github.com/directus/directus) | yes | not required | [conditional](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L21-L22) | [disallowed](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L29-L30) | 0.33 | 4.09 d | 49.65 d | 51.45 d | 2026-08-07 |
| [isomorphic-git/isomorphic-git](https://github.com/isomorphic-git/isomorphic-git) | yes | not required | not stated | not stated | not available | not available | not available | 28.89 d | 2026-08-21 |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | yes | [yes](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L451-L458) | [conditional](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L503-L504) | [disallowed](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L505-L506) | 0.47 | 0.57 d | 2.88 d | 0.81 d | 2026-08-07 |
| [payloadcms/payload](https://github.com/payloadcms/payload) | yes | not required | not stated | not stated | not available | not available | not available | 3.46 d | 2026-08-07 |
| [prisma/prisma](https://github.com/prisma/prisma) | yes | [yes](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L17) | [allowed](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L118) | not stated | not available | not available | not available | 6.8 d | 2026-08-07 |
| [strapi/strapi](https://github.com/strapi/strapi) | yes | not required | not stated | not stated | 0.41 | 5.99 d | 67.64 d | 6.41 d | 2026-08-07 |
| [supabase/supabase](https://github.com/supabase/supabase) | yes | [yes](https://github.com/supabase/supabase/blob/6c0439ace812f134859a825e421f5f241cbf01b3/CONTRIBUTING.md#L23) | not stated | not stated | 0.9 | 0.92 d | 10.73 d | 1.78 d | 2026-08-07 |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | yes | not required | not stated | not stated | not available | not available | not available | 1.65 d | 2026-08-07 |
| [withastro/astro](https://github.com/withastro/astro) | yes | not required | not stated | not stated | 0.56 | 3.26 d | 15.08 d | 9.96 d | 2026-08-07 |
<!-- merge-odds:table:end -->

## How an entry is built

```text
scripts/measure.py <owner/repo>
        |
   github.py ........ the only module that touches the network
        |              repository metadata and default branch commit
        |              100 recently updated closed pull requests
        |              raw contents of candidate policy files
        |
        +--> policy.py ...... proposes candidate quotes and decides nothing
        +--> prs.py ......... computes statistics over the sample
        |
   entry.py ......... assembles JSON and pins evidence to the commit
        |
   data/repos/<owner>__<repo>.json
        |
   scripts/render.py  regenerates the table above
```

The README table is generated. `render.py` replaces only the content between its two markers, and CI fails when the committed table disagrees with the dataset.

## Engineering notes

### The regex proposes; a person decides

Reading a contribution policy requires judgment. A broad invitation near a narrow restriction does not cancel the restriction. Automating that interpretation would create a dataset that sounds certain and gets the rule wrong.

`policy.py` searches a fixed set of candidate files and returns passages with line ranges. It does not decide what those passages mean. The person adding an entry chooses the relevant quote and sets the four policy fields. Quotes are capped at 600 characters and 8 lines so the evidence stays readable without summary.

### Evidence is pinned and checked again

Each quote is stored with the repository's `default_branch_sha`. `entry.py` turns that location into a link to the exact source lines at that commit.

`validate_data.py` fetches the pinned range and verifies the stored text verbatim. A typo in the quote or an incorrect line range fails validation instead of entering the dataset.

### Thin samples do not produce a score

`prs.py` sets floors for the human sample and the casual author sample. Below either floor, acceptance and merge time remain unavailable. The result is less complete and more honest.

An author who appears more than twice in the sample counts as a regular contributor for this measurement. Their work is excluded from the statistic intended to describe people passing through. A frozen login list and GitHub's bot flag remove bot pull requests.

### One module owns network access

Every HTTP request is confined to `github.py`. It retries transient failures up to 4 attempts, caps secondary rate limit waits at 900 seconds, and distinguishes a missing repository from an unavailable API.

### Weekly refresh never rewrites a quote

`refresh.py` recomputes statistics and confirms that already quoted lines still exist. It does not search for policy language added after the entry was first read. The workflow pins actions to commit hashes and declares only the permissions each job needs.

## Stack

| Layer | Choice | Role |
|---|---|---|
| Language | Python 3.11 or later | Measurement, validation, and rendering |
| HTTP | requests | GitHub REST and raw content APIs |
| Validation | jsonschema, Draft 2020-12 | Entry shape enforced in CI |
| Tests | pytest | 114 deterministic cases against fixtures |
| CI | GitHub Actions | Validate changes, refresh data, publish Pages |
| Data | One JSON file per project | Diffable and reviewable without a database |

## Testing

Run the complete suite with:

```sh
python -m pytest -q
```

The 114 tests cover policy matching, sample floors, GitHub retries, error branches, serialization, rendering, the schema, dataset validation, static site generation, and public copy rules. They use recorded fixtures and do not call the network.

CI also checks that the README and site output match the dataset. When the workflow cannot determine a diff base, it validates every entry instead of skipping validation.

## Run locally

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
```

Reading the dataset requires no installation. Measuring or validating a repository also needs `GITHUB_TOKEN` for a usable API rate limit.

```sh
python scripts/measure.py owner/repo
python scripts/validate_data.py
python scripts/render.py
python scripts/build_site.py
```

## Limits

Each entry uses a sample of 100 closed pull requests, not the full project history. GitHub can sort that sample by recent activity, not by close time. The sample recency field reports the distance between its newest close and median close so an old pull request with a new comment cannot look current.

Policy is read at one date and pinned to one commit. The weekly refresh checks that already quoted text is still present and recomputes statistics. It does not search for new policy language. No number in this dataset predicts what will happen to one pull request.

## Install the skills

The plugin carries two skills, for two decisions that arrive in order.
`vet-repo` answers whether a project accepts outside work and under what
rules, and it is the one that reads this dataset. `vet-issue` answers
whether one particular piece of work in that project is still available,
which is a different question: an issue can be open, unassigned and
referenced by no pull request while the defect it describes has already
been fixed.

As a Claude Code plugin:

```text
/plugin marketplace add luantaraschi/merge-odds
/plugin install merge-odds
```

Or clone the repository:

```sh
git clone https://github.com/luantaraschi/merge-odds.git
```

The dataset needs no runtime. Running the measurement and validation scripts needs Python 3.11 or later and this setup command from the repository root:

```sh
pip install -e .
```

`vet-repo` resolves `data/repos/` and `scripts/measure.py` from its own plugin root, not from the project being checked. Read [skills/vet-repo/SKILL.md](skills/vet-repo/SKILL.md) for the complete sequence, and [skills/vet-issue/SKILL.md](skills/vet-issue/SKILL.md) for the checks that come after a project passes.

## Contributing

To add or correct an entry, read [CONTRIBUTING.md](CONTRIBUTING.md). The full measurement method is in [METHODOLOGY.md](METHODOLOGY.md).

## License

Code is licensed under MIT. The dataset has its own terms in [data/LICENSE](data/LICENSE).
