# Codex review request: Paper 10 — Round 2 (post-fix)

## Mode

**Re-review after Round 1 fixes.**  Round 1 found:
- 1 P0: (C11) didn't state what Lemma 6 needed; tied gap-growth to
  $\delta_*$ (a drift floor) rather than uniform per-step bound.
- 8 P1: Lemma 5d clock, Lemma 4 sufficient/necessary, "nine
  lemmas" → ten, Lemma 5b multinomial conditions, "contrapositive"
  wording, stale (C1)–(C5), Audit 7 backwards remediation, worked
  scenarios checklist + KL constants.
- 2 P2: notation table overfull float; hyperref bookmark math
  warnings.

## What was fixed (round 1)

### P0
- **(C11) reformulated** as uniform worst-case per-SPRT-step bound
  on $(\Delta\epsgap)_n$ over the entire $\Aadv \cup \Aadv^{\mathrm{env}}$
  class; $\rhogap$ no longer indexed by $\delta_*$ (verified
  globally swept).  Audit 7 reframed: calibration must be conservative
  (from rate limits / action bounds), not measured against
  "representative strategies."  Anything outside $\rhogap$ falls
  into residual (R3).

### P1
1. **Lemma 5d**: replaced $\Tbeta \leq \tau_\mathrm{meta}$ with
   $\Tbeta \leq \Nev(\tau_\mathrm{meta})$ (event-count clock
   throughout).
2. **Lemma 4 appendix**: "sufficient condition" → "necessary
   condition" for $\Lambda_t < A$, with explicit inequality-
   direction justification.
3. **"nine lemmas" → "ten lemmas"** in §4 intro, §4 closing, §5
   main_theorem intro.
4. **Lemma 5b multinomial**: added fixed-cardinality + baseline-
   mass floor conditions; (C5.SUPP) extended to agent-side
   multinomials.
5. **"contrapositive"** → "separate reverse-threshold adequacy
   condition" with explanation in both `conjecture_op.tex` and
   `lemmas.tex`.
6. **Stale (C1)--(C5)** → **(C1)--(C12)** swept across 12 sites
   (conjecture_op, discussion, main_theorem, deployment_tooling,
   worked_scenarios).
7. **Audit 7 remediation** fixed: now correctly recommends
   increasing $\delta_*$, decreasing $\Bclip$, loosening $\beta$,
   increasing $\alpha$, increasing $\Ncasc$.  Explicit note that
   tightening $\beta$ / raising $\Bclip$ go the wrong way.
8. **Worked scenarios**: full (C5.SPRT)/(C6)--(C12) checklist for
   Scenario 1; SPRT KL constants relabeled as illustrative with
   corrected values per the Lemma 5b formulas.

### P2
- **Notation table**: converted to `longtable` (no more
  Float-too-large overfull).
- **Hyperref bookmarks**: wrapped subsection titles with
  `\texorpdfstring` (Lemma 6, $I_X$ subsection groups in
  invariants/deployment_tooling, Proof of Lemma 6) and Violation
  paragraph titles in worked_scenarios.  9 cosmetic warnings remain
  on `\paragraph{...}` titles with math; PDF body is unaffected.

## What to read

Primary:
- `docs/paper10/main.tex` — main file
- `docs/paper10/sections/*.tex` — body sections
- `docs/paper10/appendices/proofs.tex` — appendix A
- `docs/paper10/appendices/notation_table.tex` — appendix B
- `docs/paper10/main.pdf` (69 pages, post-fix)

Reference (round 1 review): `docs/paper10/review_request_full.md`
already in repo with the original questions.

## What we want from you

**Verify the fixes are sound.**  For each of the round 1 findings,
check whether the fix is correct, complete, and didn't introduce
new issues.

**Look for new issues.**  The (C11) rewrite, Lemma 5b multinomial
extension, and (C1)--(C12) sweep were substantial edits; new
inconsistencies or undefined behavior may have crept in.

**In particular, check:**

### A. (C11) reformulation soundness

The new (C11) says $\rhogap$ is a uniform worst-case bound over
the union class $\Aadv \cup \Aadv^{\mathrm{env}}$ during the
detection window, with anything outside falling into (R3).

- Does the proof of Lemma 6 (in §A.7) still go through with the
  new (C11)?  Is there any place that implicitly relied on the
  old `\rhogap(\delta_*)` form that we missed?
- Is the (R3) residual now correctly defined to absorb $q$'s
  whose per-step gap-growth exceeds $\rhogap$?  Or does this
  conflict with (R3)'s prior definition (redundancy-dominated
  regime)?
- Does Audit 7's "uniform worst-case from rate limits / action
  bounds" calibration give operators something concrete to do?

### B. Lemma 5b multinomial conditions

We added fixed-cardinality + baseline-mass-floor conditions for
Channels 3/4.  Does this leak into (C5.MULT) or (C5.SPRT) bundling
in a way that requires further integration?

### C. Lemma 5d event-clock fix

Now uses $\Nev(\tau_\mathrm{meta})$ instead of $\tau_\mathrm{meta}$
directly.  Does the chain $\Tbeta \leq \Ncasc \leq
\Nev(\tau_\mathrm{meta})$ still hold rigorously, and is the
event-count form consistent with how Theorem 1 Layer 2 invokes
the lead-time guarantee?

### D. (C1)--(C12) sweep completeness

We replaced 12 sites globally.  Did this miss any?  Are there
any places where "(C1)--(C5)" was correct shorthand (e.g.,
referring to the original pre-Phase-2 condition list) that
should not have been rewritten?

### E. Worked scenarios constants

The relabeled illustrative KL constants ($\delta_1 \approx 0.274$,
$\delta_2 \approx 0.070$) — verify the formulas from Lemma 5b
yield these values for the parameters given.

### F. Anything else

Flag any new issues, P0/P1/P2 as before.  Use the same severity
tagging.

## Output format

For each round 1 finding (A through E above plus any new):
- **Verified Sound** — fix is correct and complete.
- **Partially Fixed** — fix is correct but incomplete; name what
  remains.
- **Issue Identified** — fix introduces a new problem, name it.

Plus any new findings in the same severity scheme as round 1
(P0/P1/P2/P3).

Verdict at the top: "ready for adversarial review" / "minor
revisions" / "structural revisions still needed".

## Goal

Confirm whether Paper 10 is now ready for adversarial external
review.
