# Codex review request: Paper 10 — Round 5 (post-fix)

## Mode

**Re-review after Round 4 fixes.**  Round 4 found "minor revisions"
with 1 P1 + 1 P2 issue, both claimed fixed.

## What was fixed (round 4)

### P1: Lemma 4 appendix "Statement (restated)"
The appendix header still had the stale wall-clock substitution
form `Pr[T_detect > T_cascade] ≤ exp(-κ·T_cascade·δ)` even though
the proof body was rewritten in Round 3.  Now restated as the
correct event-clock Hoeffding form
`Pr[T_detect > t] ≤ exp(-2(tδ-A)²/(t·R_H²))` for `t > A/δ`, with
the asymptotic `exp(-κ·t·δ)` form as a separate clause.  Explicit
note that the wall-clock-to-event-count comparison is composed in
Lemma 6 via (C11.CLK), not in Lemma 4.

### P2: Residual summaries
Three sites still listed only the original R1/R2/R3 residuals
after R4/R5 were added.  Now updated to enumerate all five:

- **Abstract**: lists five named residuals (channel-orthogonal
  restructuring, environment-witness-orthogonal manipulation,
  redundancy-dominated regime, capability-targeting and
  coalition-internal shocks, calibration-exceeded gap-growth).
- **Introduction §1 Layer 3 paragraph**: now enumerates (R1)--(R5)
  explicitly with canonical descriptions.
- **§4 lemmas family summary**: "Acknowledged residuals" bullet
  expanded from 2 classes to all five (R1)--(R5).

## What to read

Primary:
- `docs/paper10/main.tex`
- `docs/paper10/sections/abstract.tex` (Round 4 edit)
- `docs/paper10/sections/introduction.tex` (Round 4 edit, line ~167)
- `docs/paper10/sections/lemmas.tex` (Round 4 edit, line ~777)
- `docs/paper10/appendices/proofs.tex` (Round 4 edit, line ~409
  Lemma 4 restated)
- `docs/paper10/main.pdf` (69 pages, post-Round-4)

Reference: round 4 request at
`docs/paper10/review_request_round4.md`.

## What we want from you

**Verify Round 4 fixes.**

### A. Lemma 4 appendix restated statement
- Is the appendix Lemma 4 restated statement now consistent with
  the §4 body Lemma 4 statement (lemmas.tex:245)?
- Is the event-count-to-wall-clock separation clean (no remaining
  T_cascade in the SPRT-step tail; cascade-clock comparison
  pointing to Lemma 6 / C11.CLK)?

### B. Residual summary propagation
- Abstract / introduction / lemmas-family summary now name all
  five residuals correctly?
- Do the descriptions match the canonical Layer 3 statements in
  §5?  Any inconsistency between sites?

### C. Anything new
- Any issues introduced by the Round 4 edits?
- Any P0/P1/P2 not previously named?

## Output format

Same severity tagging as prior rounds:
- **Verified Sound**, **Partially Fixed**, **Issue Identified**,
  plus new findings.

Verdict: "ready for adversarial review" / "minor revisions" /
"structural revisions still needed".

## Goal

Confirm Paper 10 is ready for adversarial external review.
