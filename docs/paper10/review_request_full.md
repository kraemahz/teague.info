# Codex full review request: Paper 10 (deployment-safety theorem)

## Mode

**Comprehensive structural and technical review** of Paper 10
("Goal-Frontier Maximization: A Provably Safe Regime for
Capability-Unbounded Deployment").  This is the post-Phase-2 paper
after all lemma promotions and conditions integration.  Six
internal review cycles have been completed on individual lemmas
(Lemmas 1, 2, 5a, 5e via 2 rounds each; Lemma 6 via 6 rounds).
This is the first full-paper review.

## What to read

Primary (the paper itself):
- `docs/paper10/main.tex` — main file with macros + structure
- `docs/paper10/sections/*.tex` — all 11 body sections
- `docs/paper10/appendices/proofs.tex` — appendix A: detailed proofs
  (Lemmas 1, 2, 4, 5a, 5b, 5c, 5e, 6)
- `docs/paper10/appendices/notation_table.tex` — appendix B:
  notation reconciliation
- The compiled PDF: `docs/paper10/main.pdf` (67 pages)

Reference (source-paper machinery the composition rests on):
- `docs/paper3/` — Horizon Aware (anti-monopolar property,
  cross-substrate cooperative novelty rate)
- `docs/paper5/` — Exogenous Verification (substrate-exclusivity
  witnesses, SPRT detection, Pedersen commitments)
- `docs/paper6/` — Phase Redundancy (Lyapunov phase boundary,
  metastable lifetime, redundancy floor)
- `docs/paper8a/` — Revealed Sacrifice (B-to-C lower bound)
- `docs/paper8b/` — Need Sufficiency (HHI as concentration
  surrogate)
- `docs/paper9/` — Microfoundation (Lipschitz transfer Goodhart
  bound, four-channel decomposition, Conjecture 1)

**Skip these (working artifacts, not paper content):**
- `docs/paper10/drafts/` — v1→vN lemma proof drafts and prior
  codex review requests
- `docs/paper10/TODO_proofs.md` — internal progress tracker

## What we want from you

A holistic review.  Specifically, we are looking for findings in
the following categories.  Use the severity tagging below; not all
categories need to fire.

### A. Theorem statement and proof

- Is Theorem 1's statement complete and unambiguous?  All twelve
  conditions (C1)--(C12) plus sub-clauses (C5.SPRT.HOEFF/MULT/IID/
  SUPP), (C11.CLK), (C12.ENV-WIT.PUB/PART/TRUST-WRITE/TRUST-CORR/
  SETUP/CAL).
- Are the three layers (static safe region / detection-and-
  correction / acknowledged residuals) correctly composed?
- Are the proof steps in §5.2--§5.3 (Layer 1, Layer 2) sound and
  do they correctly invoke the appendix proofs?
- Does Lemma 6 (h_detect intensivity) correctly drive Layer 2's
  bound, with the $\Tbeta$/$\tau_{\mathrm{meta}}$ separation?
- Is the typology in §5.4 ("What the theorem does not establish")
  --- conjectural / scope / operational --- correctly applied?

### B. Lemma soundness and composition

The nine lemmas (1, 2, 3, 4, 5a, 5b, 5c, 5d, 5e, 6) compose into
the three-layer claim.  Are the compositions correct?

- Lemma 1: intensive composition under co-evolution (appendix §A.1)
- Lemma 2: Lyapunov-Goodhart bridge (appendix §A.2)
- Lemma 3: HHI surrogate forward implication (inline, §4.3)
- Lemma 4: SPRT lead-time tail bound (appendix §A.4)
- Lemma 5a: substrate floor (appendix §A.3)
- Lemma 5b: channel-restricted detection KL floor (appendix §A.5)
- Lemma 5c: minimax static tightening (appendix §A.6)
- Lemma 5d: lead-time tail composition union-class (inline, §4.10)
- Lemma 5e: environment-side witness extension (appendix §A.8)
- Lemma 6: $h_{\mathrm{detect}}$ intensivity (appendix §A.7)

The 5-family numbering uses sub-letters; if any rendering issue
remains, flag it.

### C. Invariants and conditions

- Are the eleven invariants $I_1$--$I_{11}$ well-defined?  In
  particular: does $I_8$'s enumeration (in §3) match Lemma 5e's
  $V_{\mathrm{env}}$ usage in §4.11?
- Is the (C5.SPRT) bundling clean?  Same for (C12.ENV-WIT) sub-
  clauses.
- Do (C6)--(C12) cover what the proofs need?  Any remaining hidden
  assumption?
- Is SA1 (HHI surrogate adequacy) clearly presented as the one
  conjectural condition the deployment claim conditions on?

### D. Substrate anchoring (§6)

- Is the canonical tripartite identification (Human + AI +
  Formal-Operational) defensible?  Is its connection to
  $\mindep \geq 3$ rigorous?
- Is (C4) (causally-grounded inner-alignment) presented with the
  right scope?  Is the distinction from substrate-aware
  $V^\gamma$-optimization clear?
- Does the destabilizing-cascade mirror failure mode receive the
  right treatment (it's named but not bounded)?

### E. Conjecture-1 dependency (§7)

- Is the §7 typology (operational / conjectural / scope) correctly
  applied?
- Is SA1's status as an empirical assumption (not derived) clear,
  with a defensible empirical-validation pathway?
- Is the channel-mediation conjecture deferred to follow-up work
  appropriately?

### F. Deployment tooling (§8)

- Do Audits 1--8 cover all the calibration the theorem requires?
- Is each audit's procedure operationally implementable from
  ledger state?
- Are the trade-offs (tighter audits vs.\ residual coverage) named
  honestly without being defensive?

### G. Worked scenarios (§9)

- Do the scenarios correctly instantiate the theorem and exercise
  the conditions?
- Are the scenario constants chosen plausibly (or are they
  obviously hand-tuned)?

### H. Discussion / scope / what the theorem does not say (§10)

- Are the limitations correctly categorized into the three-category
  typology?
- Are the deferred-indefinitely items (welfare-truth bridge,
  monolithic-agent partition, trusted-setup details, empirical
  threshold calibration) properly named and not treated as gaps the
  paper closes?

### I. Notation, prose, and presentation

- Is the notation in Appendix B consistent with usage throughout
  the body?  Any symbols used but not in the table?
- Are the cross-references correctly resolved?  Any dangling
  $\ref{}$?
- Is the prose free of defensive phrasing (we removed 8
  "honest"/"honesty" usages; flag any remaining issues)?
- Are tables 1 and 2 (notation in Appendix B; invariants in §3)
  legible and not box-breaking?
- Is the introduction (§1) appropriately framed?  Does it
  oversell or undersell the result?

### J. Anything we did not name

If you find a load-bearing issue we did not name above, flag it.
This is the highest-priority category.

## Output format

Use severity tagging:

- **P0 (must-fix before publication)**: load-bearing flaw in the
  theorem, proof, or main lemmas.  Either an error or a gap in
  load-bearing argument.
- **P1 (should-fix before publication)**: significant issue with
  presentation, completeness, or one of the conditional conditions.
  Could be addressed without restructuring.
- **P2 (nice-to-fix)**: cosmetic, stylistic, or readability issues.
- **P3 (out of scope / acknowledged)**: items the paper already
  treats as deferred work or out of scope; no action needed.

For each finding:
1. Severity tag.
2. Location (`file.tex:line` or `§X.Y`).
3. The issue.
4. Recommended fix (if applicable).

Group findings by category (A--J).  Provide a rollup at the top
("verdict: ready / minor revisions / structural revisions").

## Goal

Determine whether Paper 10 is ready for adversarial external review
or whether further internal revisions are needed.
