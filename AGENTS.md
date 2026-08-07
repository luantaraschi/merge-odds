# AGENTS.md

This file is for an agent reading this repository, not for an agent deciding whether to work on some other project. For that, see the `vet-repo` skill under `skills/`.

## Where the data lives

Each measured project has one file at `data/repos/<owner>__<repo>.json`, matching `schema/repo.schema.json`. Read a project's policy from that file, not from the table in `README.md`. The table is a rendered summary and drops detail the JSON keeps.

## What each field means

- `repo`: the `owner/name` GitHub slug this entry describes.
- `measured_at`: the date policy and pull requests were read, `YYYY-MM-DD`.
- `default_branch_sha`: the commit every quote and every `url` in `evidence` is pinned to.
- `archived`: present and `true` only for a repository GitHub has archived. Entries like this carry no `merge_stats`, because there is no ongoing pull request activity to sample.
- `insufficient_sample`: present and `true` when the pull request sample was too small or too skewed to support a statistic. On these entries, `merge_stats` omits `casual_author_acceptance`, `median_days_to_merge`, and `p90_days_to_merge` rather than showing a number computed from too little.
- `policy_stale`: present and `true` when the weekly refresh could not confirm the quoted text is still on the pinned commit's file, most often because the file moved or the wording changed since it was quoted.
- `policy.accepts_external_prs`, `policy.requires_issue_first`: booleans, each backed by at least one item in `policy.evidence`.
- `policy.ai_assisted_code`, `policy.ai_authored_pr_text`: one of `allowed`, `allowed_with_conditions`, `not_stated`, `disallowed`. These are two separate claims on purpose. A project can welcome AI-assisted code and still require that the pull request description be written by a person.
- `policy.evidence`: the quotes backing the four claims above. Each item names the `claim` it supports, a `source` file, a `url` pointing at that file on the pinned commit with a line anchor, and the `quote` itself, copied verbatim from the source.
- `merge_stats.sample_size`, `merge_stats.window_days`: how many closed pull requests were sampled, and how many days that sample spans.
- `merge_stats.casual_author_acceptance`, `merge_stats.distinct_casual_authors`: the acceptance rate and headcount for authors appearing at most twice in the sample. See `METHODOLOGY.md` for why the threshold sits at two.
- `merge_stats.median_days_to_merge`, `merge_stats.p90_days_to_merge`: time to merge for the merged pull requests in the sample, with bots already removed.
- `merge_stats.bots_excluded`: `true` when present. It records that bot removal happened, not how many were removed.

## How to read an entry

Check `policy.accepts_external_prs` and `policy.requires_issue_first` before anything else in the file. Everything past those two fields, including every statistic, is secondary to whether the project wants outside pull requests at all and whether it wants an issue opened first.

Never state a policy claim without the `url` that pins its quote to a commit. The quote is the entire basis for the claim. A claim without its link is an assertion this repository cannot back up.
