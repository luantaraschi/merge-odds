# merge-odds

merge-odds answers one question, one project at a time: does this project accept pull requests from people outside its core team, and under what rules.

Maintainers in 2026 spend real hours closing pull requests they never asked for, many of them written by an agent that never read the file explaining the project's rules. A lot of that work should not have started at all. The project already said no, or said "open an issue first," or said "not AI-written text," in a file sitting in its own repository. Nobody checked before the work began. merge-odds reads those files, once per entry, and writes down exactly what they say. Where the project's rule departs from the default of "open, no issue required, nothing said about AI" -- the entry carries a quote taken word for word and a link that pins it to a specific commit. Where nothing in the files read said otherwise, the entry records the default, which means "no restriction found," not "permission granted."

## Reading the table

Column order is deliberate. The first four columns after the project name are policy, read straight from the project's own files: whether it accepts external pull requests, whether it wants an issue opened first, and what it says about AI-assisted code and about AI-written pull request text, listed as two separate claims because a project can allow one and forbid the other. The columns after that are statistics from a sample of the 100 closed pull requests the project most recently touched, which is the closest the GitHub API can get to "most recently closed": it can sort by when a pull request was last updated, not by when it was closed. `Sample recency` reports how many days separate the newest close in the sample from the median close, so a stray old pull request that got a late comment cannot pass itself off as recent activity. `Median` and `p90` are not computed over the whole sample: they cover only the merged pull requests from casual outside authors, the same group `Casual acceptance` is drawn from, since a regular committer's merge speed says nothing about how long an outside pull request waits. Policy comes first because it is what the project asked for, in its own words. The numbers come after because they describe a sample of other people's past pull requests, not a promise, and not a forecast for yours.

Where a policy cell links to text, the link goes to the quote it was read from, pinned to the commit it was read at. A cell with no link means the entry found nothing in the project's files that departed from the default for that claim -- not that the project said yes.

<!-- merge-odds:table:start -->
| Project | External PRs | Issue first | AI code | AI PR text | Casual acceptance | Median | p90 | Sample recency | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [directus/directus](https://github.com/directus/directus) | yes | — | [conditional](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L5-L6) | [disallowed](https://github.com/directus/directus/blob/197d141ad92c659a8d89a29fe58b9618ed9863e2/ai_policy.md#L29-L30) | 0.33 | 4.09 d | 49.65 d | 51.45 d | 2026-08-07 |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | yes | [yes](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L451-L458) | [conditional](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L501) | [disallowed](https://github.com/n8n-io/n8n/blob/c0d863ec3cbad249ac6e416e0c94a500d237a4f7/CONTRIBUTING.md#L505-L506) | 0.47 | 0.57 d | 2.88 d | 0.81 d | 2026-08-07 |
| [payloadcms/payload](https://github.com/payloadcms/payload) | yes | — | — | — | — | — | — | 3.46 d | 2026-08-07 |
| [prisma/prisma](https://github.com/prisma/prisma) | yes | [yes](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L17) | [allowed](https://github.com/prisma/prisma/blob/06ea3dc3775d399a0a501d6d40ba6999a1c1346d/CONTRIBUTING.md#L118) | — | — | — | — | 6.8 d | 2026-08-07 |
| [strapi/strapi](https://github.com/strapi/strapi) | yes | — | — | — | 0.41 | 5.99 d | 67.64 d | 6.41 d | 2026-08-07 |
| [supabase/supabase](https://github.com/supabase/supabase) | yes | [yes](https://github.com/supabase/supabase/blob/6c0439ace812f134859a825e421f5f241cbf01b3/CONTRIBUTING.md#L23) | — | — | 0.9 | 0.92 d | 10.73 d | 1.78 d | 2026-08-07 |
| [twentyhq/twenty](https://github.com/twentyhq/twenty) | yes | — | — | — | — | — | — | 1.65 d | 2026-08-07 |
| [withastro/astro](https://github.com/withastro/astro) | yes | — | — | — | 0.56 | 3.26 d | 15.08 d | 9.96 d | 2026-08-07 |
<!-- merge-odds:table:end -->

## Limitations

Each entry's statistics come from a sample of 100 closed pull requests, not the project's full history. Policy is read at a specific date against a specific commit; a project can change its rules the day after an entry is measured. The weekly refresh recomputes the statistics and re-checks that each already-quoted line of policy text is still there -- it does not re-read a project's files looking for a rule that is new since the entry was written, so a `Measured` date advancing every week is not proof the policy was re-read, only that the statistics were. No number in this table predicts what will happen to any single pull request. A high acceptance rate describes a hundred people who are not you.

## Installing the `vet-repo` skill

This repository is also a Claude Code plugin, built around the `vet-repo`
skill under `skills/vet-repo/`.

- **As a plugin:** `/plugin marketplace add luantaraschi/merge-odds`, then
  `/plugin install merge-odds`.
- **By cloning:** `git clone` this repository. The skill and its data
  live entirely inside it; nothing else needs to be installed.

Either way, `skills/vet-repo/SKILL.md` explains that the paths it uses
(`data/repos/...`, `scripts/measure.py`) are relative to this repository's
own root, not to the project you happen to be working in when you invoke
the skill.

## Contributing

To add or correct an entry, see `CONTRIBUTING.md`.
