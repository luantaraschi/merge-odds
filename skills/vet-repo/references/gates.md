# Gates that reject finished work

A project can accept outside pull requests, allow assistance, and still
refuse a correct change because of a rule that appeared in none of the
files read so far. Every gate below has the same shape: invisible while
the work is written, expensive once it exists.

Check all of them in one pass, before the fork. Each check is a file read
or a single API call.

Examples name the shape a rule took in a real project during August 2026.
They are illustrations of what to look for, not claims about what any
project requires today. Read the current file.

## Which branch the change targets

`main` is a default, not a rule. Projects that ship from a development
branch want the pull request there. Projects with a live maintenance line
may want the fix in both places. A project in the middle of a major
migration can move its default branch under an open pull request.

Cheap check: the repository's default branch, plus the base branch of the
last five merged pull requests. When those two disagree, the template
usually says which one is intended.

Cost when found late: the pull request opens against the wrong base, so
the diff carries every commit that separates the two branches, and
correcting it is a rebase and a retarget in public.

Shapes seen: a development branch instead of the default (`dev`); an
older name kept as the default (`master`); a maintenance line as the base
for fixes while `main` carries the next major; a template that requires
deciding between "this major only" and a backport pull request, which
means checking whether the touched file even exists on the older branch
before answering.

## A contributor license agreement

Cheap check: look at any recent pull request from an outside author for a
`cla-assistant`, `EasyCLA` or vendor-named check.

Cost when found late: nothing merges, and the check stays red until a
person signs. The agreement is signed by the human whose name is on the
account. It is never an agent's to accept, and no wording in a task
description changes that.

Two properties that surprise people. An agreement can be per
organization, so one signature covers every repository that organization
owns. It can also be per repository, so a signature on the flagship
project covers nothing else in the same organization. Both arrangements
exist, sometimes inside the same company.

## A Developer Certificate of Origin

Cheap check: `CONTRIBUTING.md` or the pull request template mentioning
DCO, or a `dco` check on recent pull requests.

Mechanically it is a `Signed-off-by` trailer, produced by
`git commit -s`. It is not a formality. The trailer asserts that the
person named has the right to submit the code under the project's
license, which makes it a statement by that person and not by the tool
that typed it. Ask once, record the answer, and use it after that.

## A verified commit signature

Some projects reject unsigned commits by rule, and a `Signed-off-by`
trailer does not satisfy that rule. A bot often comments on the pull
request listing each commit that fails.

Where the account has no signing key, a commit created through the GitHub
API is signed by GitHub's own web flow key and shows as verified. The
GraphQL mutation `createCommitOnBranch` accepts several files in one
commit, where the REST contents API creates one commit per file. Verify
afterwards that the new commit's tree matches the tree you meant to push,
by comparing the base against your branch before considering it done.

Creating a cryptographic identity in someone else's name is not an
agent's decision to make. The API route avoids the question rather than
answering it.

## The disclosure the project requires

Step 2 of the skill treats this as a policy question, because it is one.
It belongs here too, because it is also a gate, and it fails silently: a
missing footer, a missing marker in the title, a missing emoji in the
body. Copy the format from the file that demands it, character for
character, and put it where that file says to put it.

Where a project requires disclosure, provide it. Where a project's own
agent instructions name a specific tool and model, and a different tool
and model did the work, the honest disclosure names what actually wrote
the code. A wrong declaration is worse than a missing one.

## Declarations only a person can make

A template checkbox can assert something about a human being: that a
human reviewed the full diff, that AI-generated content was checked, that
the author certifies the origin of the code. Those belong to the person,
not to the agent. Surface them, explain what each one claims, and let
them answer.

This is the one gate where being wrong does not cost a round trip. It
puts a false statement inside the contribution, which is worse than no
contribution.

## Thresholds a correct patch can still fail

The change is right, the tests pass locally, and CI refuses it anyway.
Read the project's CI workflow and its linter configuration looking for
numbers.

Coverage measured on the patch rather than on the project. A floor
applied to the diff means every branch the change introduces needs a
test, including the error branches that only exist to fail.

Numeric limits in linter configuration. A `clippy.toml` capping function
arguments at three rejects a four-parameter helper, and the fix is a
struct, not an argument.

A spell checker reading source and tests. A third-party package name
inside a new test can fail it, and choosing a neutral name in the test
costs less than editing the project's dictionary.

A bundle size ratchet. Where one exists, its `--update` flag usually
rewrites every ceiling to whatever it just measured, including ceilings
the change never touched. Raise the one that moved, leave the rest at
their old and lower values, and say why.

One caution before assuming a red gate belongs to the change: run the
same command on the base commit. A project's own lint can fail on a clean
checkout, and a suite can have failures that predate the branch.

## How the project wants work claimed

Some projects run an assignment bot, usually a comment command at the
start of a line, and usually with a cap on how many issues one person can
hold at once. The bot refuses in public when the cap is exceeded, and a
bot comment cannot be deleted without write access, so a duplicate
command leaves a permanent refusal in the thread.

Two things to check before commenting: how the command must be written,
and how many issues are already assigned to the account. Where a command
seems to have been ignored, the usual cause is the Actions queue rather
than the syntax.

A related rule that costs a first pull request: in many projects the
workflows of a first-time contributor sit in `action_required` until a
maintainer approves them. No CI means no review, so the silence looks
like rejection and is not. Say so plainly rather than pushing commits to
force a re-run, which in some projects spends a maintainer's approval on
every attempt.
