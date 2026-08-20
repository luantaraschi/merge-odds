# Merge Odds site inventory

This file records the product facts and design constraints that the public site may use. Site copy must stay inside this inventory.

## Product

- Name: Merge Odds
- Repository: `luantaraschi/merge-odds`
- Public artifact: an open dataset and a Claude Code plugin containing the `vet-repo` skill
- Primary question: does a project accept pull requests from outside its core team, and under what rules?
- Primary action: check policy before opening the editor, forking, filing an issue, or writing code
- Source order: pull request template, dataset entry, then current policy files
- Policy questions: external pull requests, issue required first, AI assisted code, AI written pull request text
- Evidence model: a policy claim that differs from the default carries a verbatim quote and a URL pinned to the commit where it was read
- Default meaning: no restriction found in the files read, not permission granted
- Statistics: a sample of 100 recently touched closed pull requests, filtered to casual outside authors for acceptance and merge time
- Statistics are context, not a prediction for a new pull request
- Dataset size at launch: eight measured projects
- Install command: `/plugin marketplace add luantaraschi/merge-odds`, then `/plugin install merge-odds`
- Clone command: `git clone https://github.com/luantaraschi/merge-odds.git`
- Runtime for scripts: Python 3.11 or later and `pip install -e .`
- License: MIT

## Site jobs

1. Explain why policy comes before statistics.
2. Let a visitor inspect the current dataset without reading a Markdown table.
3. Show the quote and pinned source behind any nondefault policy claim.
4. Make installing `vet-repo` easy to copy.
5. State the limits without hiding them below promotional copy.

## Audience

- People considering a first contribution to an open source project
- Agent users who want a repository policy check before work begins
- Maintainers who need a published entry corrected
- Contributors who want to add another project to the dataset

## Voice

- Direct, calm, specific, and slightly skeptical of forecasts
- Policy first, numbers second
- Short labels paired with complete explanations
- No promotional superlatives
- No personification of the product
- No claims that a pull request will be merged
- No em dash or en dash punctuation
- No ASCII hyphen used as sentence punctuation

## Visual temperature

- Editorial evidence desk, not analytics software
- Warm paper against near black ink
- Deep green for verified routes and acid yellow for current focus
- Fine rules, commit references, and compact labels
- One strong serif statement paired with practical sans and mono text
- Square and slightly rounded surfaces, with no pill shaped card collection
- One signature motif: two independent paths converge, cross a policy gate, and leave as one line

## Density

- The hero is spacious enough to state the thesis in one look
- The repository reader is intentionally dense because every field carries evidence or meaning
- The method section is compact and sequential
- The complete dataset remains available as a table on wide screens and stacked records on small screens
- Controls keep at least a 44 pixel target

## Required states

- Search with results
- Search with no result
- Repository with a cited restriction
- Repository with no restriction found for a claim
- Repository with insufficient statistics
- Copy command idle and copied
- JavaScript unavailable, with the full dataset still readable
- Reduced motion
- Narrow phone at 320 pixels
- Wide desktop at 1440 pixels

## Intentionally generic comparison site

The generic page is a fictional visual demonstration, not a description of Merge Odds. It may use these deliberate faults:

- Purple to blue gradient hero
- Rocket, target, sparkle, shield, and chart emojis used as icons
- Generic headline and generic calls to action
- Interchangeable feature cards
- Large rounded panels
- Empty product promises without invented statistics, customers, or testimonials

It must link back to the real site and identify itself in accessible metadata as a generic demonstration.

## Exclusions

- No merge probability calculator
- No score claiming to predict a visitor's chance of acceptance
- No fake customer logos, metrics, activity feeds, or testimonials
- No casino, betting, coin, crystal ball, or AI sparkle imagery in the real site
- No emoji icons in the real site
- No fabricated repository policy
- No quote edited for brevity or tone
