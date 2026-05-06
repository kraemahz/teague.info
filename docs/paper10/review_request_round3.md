# Codex review request: Paper 10 — Round 3 (post-fix)

## Mode

**Re-review after Round 2 fixes.**  Round 2 found minor revisions
needed:

- **A (C11) Partially Fixed** → P1: residual routing put $q$
  exceeding $\rhogap$ into (R3) but (R3) is "Redundancy-dominated
  regime."
- **B Lemma 5b multinomial Partially Fixed** → P1: appendix
  introduces $\Kchmulti$ but theorem/audit/notation table didn't
  surface it.
- **C Lemma 5d event-clock Partially Fixed** → P1: stale
  $\{\Tbeta > \tau_\mathrm{meta}\}$ in proof's union-bound
  sentence (should be $\{\Tbeta > \Nev(\tau_\mathrm{meta})\}$).
- **D (C1)--(C12) sweep Verified Sound**.
- **E Scenario constants Verified Sound**.
- New P2: Lemma 6 appendix says "post-clipping per-step
  gap-growth" but clipping applies to LLR, not $\epsgap$.

## What was fixed (round 2)

### P1-A: (C11) residual routing
- Added new residual class **(R5) Calibration-exceeded
  gap-growth** in Theorem 1's Layer 3 enumeration.  $q$ exceeding
  $\rhogap$ now routes to (R5) (in (C11) text and Audit 7).
- Layer 3 proof discussion gets a new (R5) paragraph.
- "four residuals" → "five residuals" updated in main_theorem and
  discussion.
- Found and fixed a similar misroute in (C5.MULT): "adaptive
  channel creation falls into (R3)" → "violates (C5.MULT) and
  takes the deployment outside Theorem 1's conditions" (since
  condition violation isn't a residual class).

### P1-B: Multinomial cardinality
- New `\Kchmulti` macro defined in main.tex.
- (C5.MULT) explicitly bounds $K_3, K_4 \leq \Kchmulti$ as a
  deployment-class constant fixed before deployment.
- Audit 7 procedure now certifies both $\Kch$ (channel count) and
  $\Kchmulti$ (multinomial cardinality), with explicit per-channel
  documentation.
- Audit 7 "constants involved" list and notation table both
  updated with $\Kchmulti$.
- Lemma 5b appendix uses the macro.

### P1-C: Lemma 5d wall-clock leak
- Step 4 union bound now reads
  $\{\Tbeta > \Nev(\tau_\mathrm{meta})\}$ (was
  $\{\Tbeta > \tau_\mathrm{meta}\}$).

### P2: Lemma 6 appendix wording
- "post-clipping per-step gap-growth satisfies ..." rephrased to
  "per-SPRT-exposure-step gap growth ... uniformly over the
  admissible adversarial class" (clipping applies to LLR, not
  $\epsgap$).

## What to read

Primary:
- `docs/paper10/main.tex` (now imports `\longtable`, has `\Kchmulti`)
- `docs/paper10/sections/*.tex` — body sections
- `docs/paper10/appendices/proofs.tex` — appendix A
- `docs/paper10/appendices/notation_table.tex` — appendix B (now
  with `$\Kchmulti$` row)
- `docs/paper10/main.pdf` (69 pages, post-Round-2)

Reference: `docs/paper10/review_request_round2.md` (Round 2
request) and `docs/paper10/review_request_full.md` (Round 1
request) are present in the repo for traceability.

## What we want from you

**Verify Round 2 fixes.**  For each of A–E plus the new P2, check
whether the fix is correct, complete, and didn't introduce new
issues.

**Specifically:**

### A. (R5) introduction
- Is the new (R5) "Calibration-exceeded gap-growth" residual class
  well-defined?  Does it cleanly separate from the other residuals
  (no overlap, no gap)?
- Does the Layer 3 (R5) discussion correctly explain why this is a
  residual the theorem cannot close?
- Is the (C5.MULT) "adaptive channel creation" rewrite (now a
  condition violation, not residual) consistent with how the rest
  of the paper treats condition violations?

### B. $\Kchmulti$ surfacing
- Is the new $\Kchmulti$ used consistently?  Audit 7, (C5.MULT),
  Lemma 5b appendix, notation table.
- Are the multinomial-cardinality conditions integrated with
  (C5.SUPP)'s baseline mass floor and (C5.MULT) consistently?
- Any missed sites where the multinomial cardinality should be
  named?

### C. Lemma 5d clock
- All references to the cascade-clock event in Lemma 5d's proof
  are now event-count form?
- Does the rest of the paper still have any wall-clock-vs-event-
  count confusion?

### D / E
- Were there any (C1)--(C12) or scenario-constant regressions
  introduced by the Round 2 edits?

### F. New issues
- Any issues introduced by (R5)'s addition (residual count change,
  cross-references missed)?
- Any issues from $\Kchmulti$ propagation?
- Any other findings?

## Output format

Same as Round 2:
- **Verified Sound** — fix is correct and complete.
- **Partially Fixed** — name what remains.
- **Issue Identified** — name the new problem.

Plus any new findings (P0/P1/P2/P3).

Verdict: "ready for adversarial review" / "minor revisions" /
"structural revisions still needed".

## Goal

Confirm Paper 10 is now ready for adversarial external review.
