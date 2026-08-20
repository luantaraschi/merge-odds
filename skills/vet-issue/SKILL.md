---
name: vet-issue
description: Use after a repository passes vetting and before writing code for one of its issues. Checks that the defect still exists, that nobody already owns the work, and that the project still maintains the area, which are three separate ways an open and unassigned issue can be worth nothing.
---

# Vetting an issue before you write code for it

`vet-repo` answers whether a project accepts outside work. This skill
answers whether one particular piece of work is still available, and it
is a different question with different failure modes.

An issue can be open, unlabelled by any claim, unassigned, and referenced
by no pull request, and still be worthless for all three of these
reasons: the bug is already fixed, someone else already owns the work, or
the project no longer maintains that code. Each check below costs a few
minutes. Skipping any of them costs the whole change.

Answer the three questions in order and stop at the first no.

## Question 1: is the defect still in the code

The strongest signal that an issue is worth working on is not its label,
its age, or the absence of a linked pull request. It is that the code the
issue describes is still wrong.

Open the file and the line the issue names, on the current default
branch, and confirm the defect. Where the issue names no file, find the
function it describes and read it. Where the claim is about behaviour,
reproduce it.

Measured on 20 August 2026: four issues passed a filter of open,
unassigned, and no cross-referenced pull request. Three were already
fixed. Two projects had shipped the fix and left the public issue open,
and in the third the function the issue named no longer existed.

This is structural rather than accidental in a project that works from an
internal tracker and mirrors to GitHub in batches. In one of those, every
one of the seven free issues had a merged fix behind it; the owner runs
agents against the internal queue, merges dozens of pull requests a
month, and the public issue is only a mirror. A line in the issue body
naming an internal identifier is the tell. Search the history for it
before anything else:

    git log --grep=<internal-id>

## Question 2: does someone already own it

Absence of an assignee means nothing. Ownership arrives through at least
four channels and a quick sweep misses three of them.

An open pull request naming the issue number in its body. A cross
reference sweep finds these.

An open pull request that never names the number. Only the issue's own
timeline shows it, as a `cross-referenced` event. Filter that timeline by
`.source.issue.repository.full_name` against the repository being
checked, because the timeline returns cross references from any
repository, including forks and unrelated projects, and an unfiltered
read reports a vacancy as taken and the reverse.

A comment claiming the work. "I would like to take this on" is a claim.
So is the issue's own author proposing a design and waiting on a
maintainer to answer, which is the expensive one to miss because it
appears in neither the assignee field nor any linked pull request.

A patch written into the issue body. Someone who diagnosed the bug,
pointed at the two functions and pasted the corrected code owns that
work, whether or not a pull request exists. "Happy to open a PR" at the
end of that comment is a claim, and days of silence afterwards do not
release it.

Two habits make this cheap. List the project's open pull requests once,
in full, rather than searching per issue: one call replaces nine
searches, and it catches the contributor whose titles never mention issue
numbers. And count open pull requests per author, not only in total,
because a queue that looks like ordinary competition can belong to one
person.

Freshness inverts in a project whose queue moves. A new issue with no
comments is a sign of competition rather than a vacancy: in one fast
project, three issues listed as available during a sweep had all been
taken within roughly five days of being opened, two of them before the
sweep ran. In the same direction, sorting a labelled queue by recently
updated selects the disputed items, because recent activity on an old
issue is usually another contributor working rather than a maintainer
triaging. Sort by creation date and prefer the issue nobody has touched.

There is a version of this that no filter catches, so measure it when the
project has a label meaning accepted work: how long an issue survives
after the label is applied. In one project the median was 8.1 hours, and
seven issues labelled over two days went between 0.6 and 17.5 hours. A
daily sweep arrives after everything is gone. What is left over is
usually left for a reason, with one honourable exception: an accepted
issue whose earlier pull request was abandoned by its author is a genuine
opening.

## Question 3: does the project still want work in that area

An issue can be real, unclaimed, and still refused, because the code it
touches receives no more investment or because the maintainer has already
answered this class of question elsewhere.

Read the history of the file. A compatibility path for a major version
released years ago is a scope refusal waiting to happen. A recent commit
from another outside contributor in the same file is not proof the area
is open: in one measured case that exact signal gave false confidence,
and the maintainer who had accepted that commit closed the next change to
the same file with one sentence about how long the migration had been
available. The diagnosis was never contested. Scope belongs to the
maintainer, and arguing after that answer spends the channel rather than
the point.

Read the maintainer's answer on a similar issue. Where they have refused
this class before with a reason that generalises, the reason covers the
new case too. One project treats a whole category of import behaviour as
a deliberate design decision rather than a defect, which invalidates
every issue in that category at once, and reading one closed issue was
enough to learn it.

Read what the project's labels mean in its own vocabulary. A label
saying a workaround exists often means the project has decided not to
prioritise the fix, which is different from an open invitation.

## When the free queue is dry

In a large and active project the labelled queues are usually empty of
real work, and the checks above will keep returning no. That is not a
reason to lower the bar or to write something cosmetic to have written
something.

It is a reason to stop competing for the queue and read the code instead.
`references/finding-work.md` describes the leverages that produced
defects nobody had reported, what to do before believing one of them, and
the rule that keeps such a finding from being closed on sight.
