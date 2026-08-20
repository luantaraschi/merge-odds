# When a project says yes and behaves no

Policy files describe intent. Statistics describe a hundred past pull
requests. Neither one catches a project that accepts outside
contributions in writing and, for one reason or another, does not accept
them from you.

Five shapes, each of which has passed a policy read and a statistics read
and still been the wrong place to spend a day. Then two questions that
belong to the same step: whether there is any work to do, and where the
candidate came from in the first place.

Examples describe what was measured in August 2026. They are shapes to
recognise, not claims about any project's current state.

## 1. The door is bolted and the sign still says open

GitHub lets a project limit who may interact with it. The limit does not
appear in `CONTRIBUTING.md`, does not change the repository's
description, and does not stop anyone from opening an issue.

The direct check: `POST repos/OWNER/REPO/pulls` answers 404, not 403,
with a valid token. A 404 where a 403 belongs is the signature of a
restriction the API declines to describe.

The cheaper check, and the one to prefer, since it costs no write
attempt: list recent closed pull requests and find the newest one whose
`head.repo.owner.login` differs from the repository owner. If the last
outside fork landed weeks ago and everything since is maintainers, treat
the project as closed until something proves otherwise.

An issue usually still goes through. Where the finding is worth
publishing, the shape that works is a report with the diagnosis and the
patch offered rather than a pull request nobody can accept.

## 2. The outside authors work there

`author_association` returns `CONTRIBUTOR` for anyone with a merged pull
request behind them, which covers employees without a public
organization membership, contractors, and staff of the company that
sponsors the project. `METHODOLOGY.md` covers why the field cannot be
filtered into an answer.

What the field cannot do, reading can. Take the names behind the most
recent external merges and look at them: a handful of accounts that
appear over and over, some of them carrying the project's own name or its
employer's, is a project running its own team through the public queue.

Two tells that arrive before the profiles do. A hundred closed pull
requests covering less than two days is internal traffic, not outside
interest. And an acceptance rate computed over that sample describes the
team, not the public.

## 3. A bot did the work before you arrived

Some projects run triage automation that goes well past labelling. It
reproduces the report, links an exploration branch, writes the failing
test with its path and name, and sets a priority. A maintainer then says
that a pull request will be created once the finding is confirmed.

There is nothing wrong with the project. It is simply not a place where
an outside contributor's version of that same work has anywhere to go,
because the maintainer reviews the automation's output first and it
arrives first.

Cheap check, and it is worth making a habit: open one recent bug report
and read the last bot comment. If the bot reproduces and writes tests,
the queue is not an opening. In one project measured this way, 105 open
issues were already referenced by an open pull request against 12 that
were free, and most of those 12 were labelled as not reproducible, not
actionable, or already refused.

## 4. Everything merges and nothing is read

A very high acceptance rate paired with a very fast queue looks like the
ideal project and usually is not one. Above 90 percent acceptance with a
p90 under a day, what is being measured is a maintainer merging without
reading.

That matters for two reasons. The number inflates any table it enters,
and a merge nobody reviewed is worth little as evidence that the work was
good.

The inverse pattern is worth naming too, because it reads as welcoming
and is not: a fast p90 with a low acceptance rate is a project that
refuses quickly. A queue that moves is not the same as a queue that lets
people in.

## 5. Everything merged from outside is documentation

Read the titles of the external merges, not only their count. A project
can have a healthy acceptance rate for outside authors where half of what
lands is documentation, a registry entry, or a wording fix.

That is real contribution and it is not evidence that outside code gets
merged. If the goal is a code change, count only the code changes: in one
project measured this way, 20 casual-author merges in a sample of 190
closed pull requests broke down as 9 documentation, 10 fixes and 1
performance change.

## The third cut: is there any work here

Acceptance and queue speed are two cuts. The third one fails
independently of both, and failing it cancels the other two: a project
can merge outside work quickly and have nothing available to do.

What to measure, all of it cheap over the REST API:

Open issues that are unassigned, carry a defect label, and are not
already referenced by an open pull request. The last part is the
discount that matters, and it is one pass: fetch the open pull requests,
extract every `#\d+` from their bodies, and subtract. In one project that
turned 420 labelled issues into 301 genuinely free ones; in another it
turned 192 into 188.

Open pull requests per author, not only in total. A total that looks like
ordinary competition can be one person holding twenty-five of them, with
the clean-looking issues opened during review of their own work.

Whether the labelled queue is alive at all. Invitation labels in large
projects are frequently stale by years, and a queue whose free items are
all old is a queue that has been picked over rather than one nobody
wants.

A project that fails this cut is not a bad project. It is a project with
no door to walk through, and recognising that before the clone is the
whole point of the exercise.

## Where the candidate came from

One filter belongs at the top of any search rather than the bottom.
Sorting by what is new and popular selects against acceptance rather than
for it. In one sweep, the five newest trending projects had the worst
acceptance rates of the entire set, between 14 and 24 percent, for a
reason visible in the sample window: attention brings a crowd, one of
them collected 168 outside authors in 14 days and held more open pull
requests than open issues, and the maintainer's only available response
was to close most of them.

Prefer projects found by looking for the work rather than the attention.
