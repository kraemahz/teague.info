# Codex review request: Paper 11 (Structural Foundations)

## Context

Paper 11 (`Structural Foundations for Goal-Frontier Maximization
Deployment Safety`) is a companion paper to paper 10
(`Deployment Safety`), located at
`/Users/teague/Code/kraemahz/teague.info/docs/paper11/`. The
companion paper formalizes two structural derivations that
paper 10 forward-references:

1. **Theorem 1 (Bounded co-evolution corollary)** in
   `sections/bounded_coevolution.tex`: bounded co-evolution
   derived from (C5.HOEFF), (C7.RATE), and channel-projection
   structure, instead of being asserted as a free-floating
   deployment-class assumption.
2. **Theorem 3 (Concentration-Gap selection theorem, scoped)**
   in `sections/concentration_gap.tex`: the Concentration-Gap
   conjecture from
   \citep[Microfoundation]{lasser2026micro} discharged in scoped
   form under three operationally auditable structural
   conditions (REP, DISP, COAL).

Both theorems were individually codex-reviewed across multiple
iterations before being integrated into this paper:
- C7 closed-form: 5 codex review cycles, converged at v5
  (`drafts/c7_closed_form_v5.tex`)
- Concentration-Gap selection theorem: 2 codex review cycles,
  converged at v2 (`drafts/concentration_gap_v2.tex`)

The companion paper integrates the v5/v2 final drafts into a
unified document, with these additional sections beyond the
proofs:
- `sections/setup.tex`: shared notation
- `sections/composition.tex` (\S 5): how each theorem enters
  paper 10's deployment-claim hypothesis set
- `sections/audits.tex`: audit procedures for the four new
  structural conditions
- `sections/discussion.tex`: limitations and connection to
  Goodhart literature

The companion paper has also undergone a meta-narrative cleanup
pass: discussion-level naming has been replaced by direct cites
using the topical tag `[Deployment Safety]` for paper 10
(matching GFM-sequence cite conventions like `[Microfoundation]`,
`[Phase Redundancy]`).

## Recent revision history

- Paper 10 has been integrated to forward-reference paper 11's
  theorems: paper 10's Assumption 1 (bounded co-evolution) and
  Assumption SA1 (HHI surrogate adequacy) now point to paper 11's
  Theorem 1 and Theorem 3, respectively. Paper 10's (C7.RATE) is
  added as a sub-clause of (C7), and Audit 4 in paper 10's
  deployment-tooling spec now has a dual-mode (structural
  certification primary, empirical fallback) procedure.
- Paper 11's introduction was restructured to drop "What this
  paper does / does not do / Reader path / Roadmap" meta-narrative
  subsections, replaced by a single section with results
  statements + a brief Organization paragraph.
- Paper 11's discussion dropped a "Companion-paper status as
  integration target for paper 10" subsection (pure meta).

## Review focus

Please review paper 11 (located at
`/Users/teague/Code/kraemahz/teague.info/docs/paper11/`,
`main.tex` builds via `pdflatex`) for:

1. **End-to-end consistency.** The proofs in §3 (bounded
   co-evolution) and §4 (Concentration-Gap) were
   individually codex-reviewed in their final forms; verify they
   integrated cleanly into the companion paper without
   degradation. Specifically:
   - §3's Lemma 1, Lemma 2, Theorem 1 statements/proofs match
     the v5 final draft.
   - §4's Theorem 1 (forward), Theorem 2 (reverse), Theorem 3
     (transfer) statements/proofs match the v2 final draft (with
     the four cleanup fixes applied: H_j operator-norm scoping,
     normalized conditional baseline, atomic-C scope for
     reverse, embedding-compatibility assumption).

2. **Cross-section consistency.** Notation introduced in §2
   (setup) is used consistently in §3 and §4. The structural
   conditions (REP, DISP, COAL, C7.RATE) are defined consistently
   across §2/§3/§4 and §6 audits.

3. **Section 5 (composition).** This section was significantly
   rewritten to drop meta-narrative. Verify:
   - The hypothesis-set-removed/added accounting is correct.
   - The "where each theorem enters Deployment Safety's proof"
     subsection accurately describes the integration points.
   - The "what stays unchanged" subsection captures all the
     structural elements that remain invariant.

4. **Forward references to paper 10 are accurate.** Specifically:
   - `\citep[Assumption~1]{lasser2026paper10}` refers to paper
     10's bounded-co-evolution assumption (which now references
     this paper's Theorem 1).
   - `\citep[\S 6, SA1]{lasser2026paper10}` refers to paper 10's
     SA1 assumption (now meaning the structural conditions of
     this paper).
   - Specific section references like `\citep[\S 5,
     Layer~1 proof, Step~4]{lasser2026paper10}` should be
     accurate.

5. **Meta-narrative cleanup quality.** After the cleanup pass,
   the paper should read as direct mathematical exposition rather
   than discussion-level meta-references. Identify any remaining
   places where the prose still has unnecessary
   "this paper / this section" references that could be
   simplified to direct statements.

6. **Audit specifications (§6).** The audit procedures for
   (C7.RATE), (REP), (DISP), (COAL) should be operationally
   meaningful (not just formal restatements). Each should specify
   procedure, cadence, failure mode, and connection to existing
   paper 10 audits.

## Format

For each finding:
- [P0] Critical: must-fix before submission
- [P1] Substantive: should-fix
- [P2] Polish: minor improvements

For each: file:line, problem description, suggested fix. Be
specific. Aim for 5-15 findings. Focus on integration quality
(does the unified paper hang together as a single document) and
cleanup quality (is the meta-narrative actually gone, or are
there residual artifacts).

If the paper has 0 P0 and ≤ 3 P1 findings, please say
"paper 11 is ready for publication."

Output the findings list directly with no preamble.
