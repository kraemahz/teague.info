# Codex review request: Paper 10 — Round 4 (post-fix)

## Mode

**Re-review after Round 3 fixes.**  Round 3 found "minor revisions"
with 2 P1 + 4 P2 issues, all of which are claimed fixed.

## What was fixed (round 3)

### P1
- **deployment_tooling.tex Audit 7 failure-mode routing**:
  "Channel multiplicity grows during deployment ... falls into
  residual class (R3)" → "violates (C5.MULT) and takes the
  deployment outside Theorem 1's conditions (no longer covered,
  not a residual)".  Also added an explicit (R5) failure-mode
  entry for adversarial gap-growth exceeding $\rhogap$.
- **conjecture_op.tex R-label**: "Capability-targeting,
  coalition-internal-corruption, and environment-witness-orthogonal
  manipulations fall into residuals (R3) and (R4)" → split into
  correct categories: capability/coalition → (R4);
  environment-witness-orthogonal → (R2); calibration-exceeded
  gap-growth → (R5).

### P2
- **lemmas.tex body Lemma 6 proof outline**: "(C11) bounds the
  per-step post-clipping increment" → "per-SPRT-exposure-step
  gap increment ... uniformly over the admissible adversarial
  class".
- **proofs.tex Lemma 4 wall-clock substitution**: removed the
  entire "Substituting $T_\mathrm{cascade}$" block; Lemma 4 now
  states the asymptotic form in event-count clock $t$ only, with
  an explicit note that the wall-clock-to-event-count comparison
  is composed in Lemma 6 / (C11.CLK), not in Lemma 4.
- **$\Kchmulti$ in explanatory sites**: added to §7
  conjecture_op typology and §9 worked_scenarios Scenario 1
  Audit 7 checklist.

## What to read

Primary:
- `docs/paper10/main.tex`
- `docs/paper10/sections/*.tex`
- `docs/paper10/appendices/proofs.tex` (Lemma 4 substantively
  rewritten in this round)
- `docs/paper10/appendices/notation_table.tex`
- `docs/paper10/main.pdf` (69 pages, post-Round-3)

Reference: `docs/paper10/review_request_round3.md` and prior
rounds in `review_request_round{2,full}.md` for traceability.

## What we want from you

**Verify Round 3 fixes.**  For each finding, check whether the fix
is correct, complete, and didn't introduce new issues.

**Specifically:**

### A. Residual routing (R5 / R3 / R4 / R2 cleanup)

- All R-references throughout the paper now match the residual
  taxonomy?  Verify (R3) is reserved for "Redundancy-dominated
  regime"; (C5.MULT) violations and (C11) gap-growth exceedance
  are routed correctly.
- Audit 7's failure-mode list is now consistent with the theorem
  text?
- §7 conjecture_op's scope-restriction list correctly maps each
  manipulation class to its correct residual?

### B. Lemma 6 body wording

- Both body Lemma 6 outline (lemmas.tex) and appendix Lemma 6
  proof (proofs.tex) now use "per-SPRT-exposure-step gap" framing
  uniformly, without "post-clipping" applied to gap-growth?

### C. Lemma 4 appendix rewrite

- The Lemma 4 statement and proof are now event-clock-clean: no
  remaining $T_\mathrm{cascade}$ or $\tau_\mathrm{meta}$
  substitution into the SPRT-step tail.
- The "Note on cascade-clock composition" cleanly points readers
  to Lemma 6 / (C11.CLK) without leaving an open question about
  where the wall-clock comparison happens.
- The Caveat-on-scaling-form paragraph is consistent with the
  rest of the appendix.

### D. $\Kchmulti$ surfacing

- All sites that name (C5.SPRT)'s calibrated constants list
  $\Kchmulti$ now name it consistently (Audit 7, §7 typology,
  Scenario 1, notation table)?

### E. Anything new

- Any new issues introduced by the Round 3 edits?
- Any P0/P1/P2 findings not previously named?

## Output format

Same severity tagging as prior rounds:
- **Verified Sound**, **Partially Fixed**, **Issue Identified**,
  plus new findings (P0/P1/P2/P3).

Verdict: "ready for adversarial review" / "minor revisions" /
"structural revisions still needed".

## Goal

Confirm Paper 10 is ready for adversarial external review.
