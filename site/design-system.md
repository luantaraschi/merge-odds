# Merge Odds design system

The interface is a public policy reader presented as an editorial case file.

## Design roots

- Concrete product: evidence backed repository policy reader with secondary historical statistics
- Voice: precise, skeptical, and useful before work starts
- Visual temperature: warm editorial paper with technical notation
- Density: spacious thesis followed by compact evidence

## Tokens

| Token | Value | Reason |
|---|---|---|
| Paper | `#f1efe7` | Judgment: warmer than product dashboard white and suited to long reading |
| Paper raised | `#fbfaf5` | Derivation: a four point lightness step above Paper for controls and records |
| Ink | `#111713` | Judgment: green black carries less harshness than neutral black |
| Ink quiet | `#566159` | Derivation: secondary copy stays readable without competing with evidence |
| Gate | `#174c3c` | Judgment: policy approval uses deep institutional green, not success green |
| Signal | `#d7ff59` | Accepted cost: a sharp focus color makes the current decision obvious and is reserved for small areas |
| Stop | `#b8432f` | Platform fact: restrictions need a second cue beyond text and icon shape |
| Rule | `#c7cbc1` | Derivation: visible against both paper surfaces without turning every record into a card |
| Maximum content width | `1240px` | Judgment: enough room for evidence and explanation while preserving readable text measure |
| Reading measure | `66ch` | Platform fact: long paragraphs need a constrained line length |
| Radius small | `4px` | Subtraction: removes generic rounded SaaS styling while keeping inputs legible |
| Radius medium | `12px` | Abstention: reserved for the live reader and generic comparison frame only |
| Motion quick | `140ms` | Platform fact: direct hover and pressed feedback |
| Motion state | `240ms` | Platform fact: repository state change remains legible without delaying reading |

## Type roles

- Display: `Newsreader`, with Georgia as fallback. Used only for the thesis and large section statements.
- Interface: `IBM Plex Sans`, with system sans as fallback. Used for navigation, body, and controls.
- Evidence: `IBM Plex Mono`, with system mono as fallback. Used for repository names, commit references, quotes, and policy values.

Departure: three families are justified because the product has three distinct layers, editorial thesis, usable interface, and source evidence. No component may mix all three in one line.

## Layout

- Header: wordmark, section links, and GitHub action
- Hero: thesis at left, live repository case file at right
- Explorer: repository search followed by four policy questions and secondary statistics
- Method: source order and limits presented as a numbered reading path
- Dataset: complete rendered records with links to pinned evidence
- Install: two commands, plugin first and clone second
- Footer: repository, methodology, contribute, dispute

Judgment: the hero starts with the decision surface rather than a product illustration. Visitors can test the thesis immediately.

## Signature mark

Two paths enter from the left at different heights. They curve toward a shared center, cross a short vertical gate, and leave as one path. The upper and lower routes represent policy and observed history. Their merge only occurs after the gate.

Departure: the line leaving the mark is intentionally longer than the entering lines. It makes the object read as a decision that enables work, not a knot or decorative monogram.

## Interaction

- Repository search updates the case file and URL hash.
- Arrow keys move through repository suggestions.
- Evidence links stay visible on every claim that has a source.
- Dataset records can expand to show the exact quote.
- Copy controls announce success in a live region and return to idle without moving layout.
- Motion uses opacity and transform only.
- Reduced motion removes transitions and smooth scrolling.

## Reduction pass

- No ambient gradient, glow, glass, decorative grid, or floating orb
- No icon if a text label is clearer
- No separate card for a sentence that belongs in the page flow
- No statistic in the hero
- No repeated claim between hero, method, and install
- No entrance animation that hides content on load

## Generic page separation

The generic page uses its own stylesheet and no token from the real product except the destination link. Its excess is evidence for the comparison and must not leak into the main site.
