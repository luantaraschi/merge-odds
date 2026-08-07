# Methodology

## What is measured

Every entry has two layers. The first is policy: whether the project accepts external pull requests, whether it wants an issue opened before one, what it says about AI-assisted code, and what it says, separately, about AI-written pull request text. Every policy claim carries a quote copied verbatim from a file in the project's own repository, pinned to the commit it was read at. The second layer is statistics, computed from a sample of the project's 100 most recently closed pull requests: acceptance for casual outside authors, and how long a merge took at the median and at the 90th percentile.

Policy is listed first because it is what the project asked for, in its own words, and reading a quote takes less trust than reading a number. Statistics come second because they describe what happened to a sample of other people in the past. They are not a commitment from the project and not a forecast for the next pull request.

## Casual-author acceptance

Casual-author acceptance counts only pull requests from authors who appear at most twice in the 100-pull-request sample: someone who shows up, sends one or two changes, and is not seen again in that window. That is the profile of a person who found a bug or a rough edge, fixed it, and left, which is closer to the situation of most people reading this dataset than the situation of a regular committer with dozens of merged pull requests behind them. Authors above that threshold are left out of the acceptance number, because by that point they are part of the project in every way that matters, whatever GitHub's association field happens to say.

`casual_sample_size` is the denominator behind that rate: how many casual pull requests the acceptance figure was computed from. Below 20, the entry reports an insufficient sample and omits the acceptance figure entirely, the same guard applied to the human sample as a whole, because a rate computed from a handful of people is not a rate.

`distinct_merged_casual_authors` is a headcount, not the denominator: it counts the distinct casual authors whose pull requests were merged, so it is always at most `casual_sample_size` and usually smaller. Reading it beside the acceptance percentage as if it were "how many people this rate is based on" overstates the rate's foundation; `casual_sample_size` is the number to read for that.

## Two traps in `author_association`

GitHub's `author_association` field returns `CONTRIBUTOR` for anyone who has had a pull request merged into the repository before. It does not mean "works there," and it does not mean "outside." It covers a maintainer's own employer, a company's engineers filing pull requests through the same process as everyone else, and contractors paid to work on the project without holding a formal seat on the team. None of those people are outside contributors in the sense this dataset cares about, and an acceptance rate that folds them in reads far more welcoming than the project actually is to someone who has never touched the code. The sign that a sample is contaminated this way is traffic, not the field itself: if a hundred closed pull requests cover less than two days, the repository is not fielding outside interest at that pace. It is running its own team's work through the same queue as everyone else's.

Filtering to `FIRST_TIME_CONTRIBUTOR` looks like the fix, and it inverts the bias instead. GitHub computes `author_association` at the moment it serves the API response, from the repository's state at that moment, not from the repository's state when the pull request was opened. Someone whose first pull request just got merged now shows up as `CONTRIBUTOR` on that same pull request, because the merge already happened and the field reflects the repository as it stands now. What is left under `FIRST_TIME_CONTRIBUTOR` is close to the set of people whose first pull request was closed without merging. It still reads as first-time only because there was never a second event to update it. Filtering to it does not isolate newcomers. It isolates the people who were turned away.

## Why bots are removed first

Dependabot and Renovate open pull requests and merge them on a schedule, in minutes, without the review a human contribution gets. Left in a sample, they pull the median toward zero and make a project look far faster to merge into than it is for a person. Bots are identified and removed before any statistic in this dataset is computed, not filtered out afterward from numbers that already include them.

## Why the window matters

`window_days` records how many days the 100-pull-request sample actually spans. A short window means the project is busy: a hundred pull requests closed quickly, recently. A long window means the opposite. The project is quiet, and a high acceptance rate over a long window is not evidence that the project is easy to get a pull request into. It is evidence that few pull requests arrive at all. Read acceptance and window together. Acceptance on its own can describe either a welcoming project or an empty one.

## What is not measured

This dataset does not estimate the chance that any individual pull request will be merged. It does not measure code quality, project health, or how a maintainer will respond to a particular person. A casual-author acceptance rate describes a hundred past pull requests from a hundred different people. It says nothing about the next one.

Only files inside the repository itself are read. A rule published on a project's website, wiki, or a linked external guide is out of scope, even when a file in the repository points to it, because there is no commit to pin the quote to.
