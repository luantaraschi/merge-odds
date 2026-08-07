# merge-odds

merge-odds answers one question, one project at a time: does this project accept pull requests from people outside its core team, and under what rules.

Maintainers in 2026 spend real hours closing pull requests they never asked for, many of them written by an agent that never read the file explaining the project's rules. A lot of that work should not have started at all. The project already said no, or said "open an issue first," or said "not AI-written text," in a file sitting in its own repository. Nobody checked before the work began. merge-odds reads those files, once per entry, and writes down exactly what they say, with a quote taken word for word and a link that pins the quote to a specific commit.

## Reading the table

Column order is deliberate. The first four columns after the project name are policy, read straight from the project's own files: whether it accepts external pull requests, whether it wants an issue opened first, and what it says about AI-assisted code and about AI-written pull request text, listed as two separate claims because a project can allow one and forbid the other. The columns after that are statistics from a sample of the project's 100 most recently closed pull requests. Policy comes first because it is what the project asked for, in its own words. The numbers come after because they describe a sample of other people's past pull requests, not a promise, and not a forecast for yours.

<!-- merge-odds:table:start -->
| Project | External PRs | Issue first | AI code | AI PR text | Casual acceptance | Median | p90 | Measured |
|---|---|---|---|---|---|---|---|---|
<!-- merge-odds:table:end -->

## Limitations

Each entry's statistics come from a sample of 100 closed pull requests, not the project's full history. Policy is read at a specific date against a specific commit; a project can change its rules the day after an entry is measured, and the weekly refresh exists to catch that, not to guarantee it never happens. No number in this table predicts what will happen to any single pull request. A high acceptance rate describes a hundred people who are not you.

## Contributing

To add or correct an entry, see `CONTRIBUTING.md`.
