## Entry or problem

Which project are you adding, or what problem are you fixing?

## Evidence

For a dataset entry, link every quote to the pinned commit and explain any value that differs from its default. For code changes, include the smallest reproduction.

## Checks

- [ ] `python -m pytest -q` passes
- [ ] Changed entries pass `python scripts/validate_data.py`
- [ ] `python scripts/render.py --check` passes
- [ ] `python scripts/build_site.py --check` passes
- [ ] `python scripts/validate_content.py` passes
- [ ] The pull request contains one project or one code problem
