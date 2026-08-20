# Contributing

merge-odds grows one project at a time, added by people who read that project's own files and write down what they say.

## Before starting

Claim an open measurement issue before working on it. For a schema, methodology, or site change, start in [Ideas](https://github.com/luantaraschi/merge-odds/discussions/categories/ideas) so the decision is recorded before the code.

Questions about an entry or the measurement process belong in [Q&A](https://github.com/luantaraschi/merge-odds/discussions/categories/q-a). A published claim that is wrong or stale belongs in the dispute issue form.

## Set up the repository

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
```

Measuring a project also needs a GitHub token in `GITHUB_TOKEN`.

## Adding a project

1. Pick a project nobody has measured yet.
2. Run: `python scripts/measure.py owner/repo --write`
3. Open the generated file. It has a `_review` block with three keys. `candidates` are the quotes the scanner found; read each one in its source file, not just the quote in the JSON, since a sentence can reverse meaning two lines later. Then decide the four policy values and move the quotes you actually used into `evidence`. `unmatched_claims` lists claims the scanner found nothing for. That silence is not evidence of a permissive policy, so go read the relevant files yourself before accepting the default. `files_read` is what the scanner already fetched, a starting point if you need to look further. When you are done, delete `_review`. CI rejects any file that still has it.
4. Open a pull request. One project per pull request.

## Check the change

Run the checks that match the files you touched. A new entry needs all of them.

```sh
python -m pytest -q
python scripts/validate_data.py data/repos/owner__repo.json
python scripts/render.py --check
python scripts/build_site.py --check
python scripts/validate_content.py
```

If the render checks report a difference, run the same command without `--check`, inspect the generated change, then run the check again.

## Review

Expect a first response within 72 hours.

## One project per pull request

Keep each pull request to one project. Two people adding different projects will not conflict with each other if they never touch the same file, and one file per pull request is what keeps that true.

For code or documentation changes, keep one problem per pull request and explain how you verified it. Do not combine a dataset entry with an unrelated refactor.
