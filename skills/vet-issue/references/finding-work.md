# Finding work by reading code

The issue queue is the obvious place to look and the most contested one.
Everything below finds defects nobody has reported, which means no
competition and no claim to check. It costs more than picking an issue,
so the leverages are ordered by how often they paid.

All of them share one property: they compare the code against something
that already answers the question. A leverage without an oracle is
guessing, and guessing produces the kind of finding a maintainer closes
on sight.

## Compare two implementations the project keeps in step

The strongest leverage there is, because the project itself has agreed
which behaviour is correct. It applies wherever a codebase carries two
things that must match: a reference implementation and a port to another
language, a plugin for one service and the equivalent plugin for
another, a browser build and a server build of the same module.

Where the two disagree, one is wrong and the project has already said
which. That is what makes the change defensible: it needs no argument
about intent, and the project's own stated rule is the argument.

The flip side is a genuine result too. Where the second implementation
documents the divergence as deliberate, the finding is not a defect. In
one measured case a comment on the ported function described the
behaviour the other side lacked as intentional, which turned a planned
pull request into an issue describing two deliberate and contradictory
decisions, and left the choice with the maintainers. That is the correct
outcome, and it only exists because the other side was read first.

## Compare a new path against the older one it duplicates

When a project adds a variant of an existing function, a copy adapted to
a narrower case, the copy is where the defects are and the original is
the oracle. In one measured pair the recently added variant carried two
defects and the function it was copied from carried none.

## Read the sibling of a function that was just fixed

After any merge, look at the neighbour of what was fixed. A defect
corrected in the flat-path branch of a function frequently survives in
the nested-path branch, and the fix that just landed is both the proof
that the maintainers consider it a defect and the model for the next one.
This is the cheapest leverage on the list and it needs no new
understanding of the codebase.

## Read a small parser all the way through

Parsers concentrate edge cases, and a small one can be read completely in
an afternoon. Empty input, repeated separators, a separator at each end,
nesting where the grammar allows nesting. In one measured case a selector
parser treated an empty group as a wildcard, so several malformed inputs
matched every element in the document.

## Compare the code against the specification it cites

Where a function's own comment names an RFC or a standard, the standard
is the oracle and the comparison is mechanical. Two shapes recur: the
code implements a rule from a neighbouring specification instead of the
one it cites, and the code implements a fixed rule where the
specification requires a sliding one.

Two cautions from measured cases. The visible effect is often rejection
rather than a wrong answer, because a later validation step catches the
inconsistency, which means the search is for inputs that fail rather than
inputs that produce garbage. And a window that grows with the calendar is
worth saying out loud, because a defect affecting a handful of values
today affects more of them every year.

## Compare a replacement against the function it replaces

Projects that reimplement a platform function for another environment
give you the platform as the oracle. The comparison can be exhaustive
rather than sampled: in one measured case, running both implementations
over every string of length 0 to 6 built from a small alphabet produced
149 divergences, and running it again after the fix produced none, which
is a far better argument in a pull request than any single example.

Keep the scope of the change to one rule. The same comparison usually
surfaces a second family of divergences that belongs to a different rule,
and folding it in makes the change harder to review and harder to accept.

## Write invariants over a catalogue of shapes

For a library that accepts a structured input, build a catalogue of 30 to
40 shapes it accepts and assert the properties that must hold for all of
them: reconstructing from its own serialisation gives the same object,
cloning gives the same object, everything the object lists can be
resolved, removing everything empties it.

The catalogue covers combinations the project's own suite never crosses,
which is where the defects are. In one measured run, 39 shapes and four
invariants produced one crash, on a shape three levels deep.

## Let the project tell you where to look

An `AGENTS.md` or `CONTRIBUTING.md` that declares an invariant is an
audit map. Where a project writes that every function materialising an
object from untrusted input must filter certain property names, and that
a regression there is a security defect, the search is mechanical: find
the ones that do not filter. In one measured case three of four did and
the fourth did not.

## Before believing a finding

Test the premise, not only the conclusion. When a probe reports something
enormous, the probe is usually what is wrong. In one case an oracle
reported a library losing paths, and the fault was the probe filtering
out anything whose value was a function, which for that library included
legitimate entries. In another, a probe wrote a dangerous property name
as a literal in the host language, which sets a prototype rather than
creating a key, so the defect it reported did not exist; rewritten to
build the input the way a real document arrives, the code was correct.

A property test is only as good as its invariant. Of five invariants
tried in one session, three were false statements about the library
rather than defects in it, and each would have become a rejected pull
request. An invariant that fails should be checked against the
documentation before it is checked against the code.

A control that passes both with and without the fix tests nothing. Two
measured cases: a test that passed because the failure it targeted was
masked by an earlier failure in the same file, and a control assertion
about global state that the defect never touched. Run every new test with
the fix reverted, and require it to fail.

Where an asynchronous behaviour is involved, measure every ordering
before claiming it is handled. One measured claim covered the ordering in
which the data happened to arrive during testing, and the other ordering
lost the user's input entirely.

## Give a finding somewhere to land

A defect found by reading code, rather than from a user's report, arrives
without the thing a maintainer needs most: evidence that it happens to
someone. A unit test over an internal function does not supply it. In one
measured case a report of that shape was closed as a solution in search
of a problem, while a defect of the same class, in a different project,
survived review because it was demonstrated end to end through the
public interface the users call.

So: reproduce through the public API, name the path by which a real input
reaches the defective code, and say what a person would see. Where the
answer is that no realistic input reaches it, that is a finding too, and
the finding is that there is nothing to fix.

If a maintainer answers that the input is unrealistic, the productive
reply is not an argument. Go and find real files. Code search accepts
size and extension filters, which is enough to collect real inputs
written by real tools, and a handful of those written by well-known
software settles the question in a way no reasoning does.
