# Codex review request: Lemma 6 v5 — re-review after Round D revisions

## Mode

**v5 confirmation review.** Round D returned "v5 needed" with one
significant problem (Q1 factor-of-4 in Hoeffding inversion: v4's
$\Tbeta = R^2\log(1/\beta)/(2\delta_*^2)$ doesn't rigorously imply
$\Pr[T_\mathrm{detect} > T_\beta] \leq \beta$ when $A > 0$) plus
four issues (Q2 multiplicity policy too weak, Q3 audit-vs-empirical
distinction, Q4 integration-text leakage of $\beta'$, Q5 missing
martingale/support assumptions).

V5 fixes:

- **Q1 factor-of-4 fix.** Replaced $R^2\log(1/\beta)/(2\delta_*^2)$
  with $2R^2\log(1/\beta)/\delta_*^2$ via the rigorous chain
  (Substeps 5a-5e): $T \geq 2A/\delta_* \Rightarrow (T\delta_* -
  A)^2 \geq T^2\delta_*^2/4 \Rightarrow$ exponent $\geq
  T\delta_*^2/(2R^2)$. Solved for exponent $\geq \log(1/\beta)$.

- **Q2 split: (C5.HOEFF) + (C5.MULT).** Range bound (C5.HOEFF)
  now enforced by uniform LLR clipping. Channel multiplicity
  promoted to its own clause (C5.MULT) with fixed-cardinality
  monitored partition $K_\mathrm{ch}$.

- **Q3 audit-vs-empirical: (C11.CLK) extended.** Added optional
  $\beta_\mathrm{cal}$ parameter for empirical-calibration variant;
  $\beta_\mathrm{cal} = 0$ in certified case. Total Layer 2 failure
  becomes $\beta + \beta_\mathrm{clk} + \beta_\mathrm{cal}$.

- **Q4 integration-prerequisite list.** Spelled out the required
  edits to §4.10 Lemma 5d, §5 Theorem 1 Layer 2 proof, §A.4 prose,
  Theorem 1 condition list, and §8 Audit 7.

- **Q5 missing assumptions: (C5.IID) + (C5.SUPP).** Added:
  - (C5.IID): adapted/i.i.d. LLR with conditional drift
  - (C5.SUPP): LLR finiteness via support overlap or clipping

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof_v5.tex` — v5 (14pp PDF)

Reference:
- Round D findings: `b24yjx0wd.output` lines 1822-1916
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — exact
  Hoeffding form
- `docs/paper5/sections/commitment.tex` line 319 — Paper 5 SPRT
  threshold

## What we want from you

Five v5 verification questions:

### Q1. Is the rigorous Hoeffding inversion correct and tight?

V5 Step 5 chain:
1. $T \geq 2A/\delta_*$
2. $\Rightarrow T\delta_* - A \geq T\delta_*/2$
3. $\Rightarrow (T\delta_* - A)^2 \geq T^2\delta_*^2/4$
4. $\Rightarrow$ exponent $2(T\delta_* - A)^2/(TR^2) \geq T\delta_*^2/(2R^2)$
5. $\Rightarrow$ Exponent $\geq \log(1/\beta) \Leftrightarrow T \geq 2R^2\log(1/\beta)/\delta_*^2$

Conservative form: $T_\beta = \max\{2A/\delta_*, 2R^2\log(1/\beta)/\delta_*^2\}$.

**Question:** Is this chain rigorous? Are there any sign issues
(e.g., when $A$ is large enough that step 2 doesn't apply)? Is the
conservative form tight enough operationally, or should we use the
exact root form $T_\beta = (2A\delta_* + c + \sqrt{c^2 + 4A\delta_* c})/(2\delta_*^2)$
with $c = R^2\log(1/\beta)/2$?

### Q2. Is the (C5.HOEFF) + (C5.MULT) split clean and necessary?

V5 splits range bound from multiplicity policy:
- (C5.HOEFF): uniform LLR clip to $[-R, R]$ with deployment-class $R$
- (C5.MULT): $K_\mathrm{ch}$ deployment-class with fixed-cardinality

**Question:** Is the split clean? Could (C5.MULT) be absorbed into
(C5.HOEFF) since clipping handles unbounded LLR even with large
multiplicity? Conversely, do we need additional clauses to handle
adversarial channel selection (the adversary picking which channel
to push hardest, potentially driving up effective $K_\mathrm{ch}$)?

### Q3. Are (C5.IID) and (C5.SUPP) the right structural assumptions?

V5 adds:
- (C5.IID): adapted/i.i.d. LLR with conditional drift
  $\mathbb{E}[\ell_n | \mathcal{F}_{n-1}] \geq \delta_n \geq \delta_*$
- (C5.SUPP): $p_0(x), p_1(x) \geq \epsilon > 0$ or LLR clipped

**Question:** Are these the right structural assumptions for
Hoeffding-Azuma to apply? Specifically:
- Does (C5.IID) need to specify conditional-variance proxy bounds
  (sub-Gaussian or sub-exponential)?
- Does (C5.SUPP) need an explicit value of $\epsilon$ or is the
  existence sufficient?
- Should the martingale-difference structure be a separate clause
  (C5.MART) distinct from i.i.d.?

### Q4. Is (C11.CLK)'s certified-vs-empirical split sufficient?

V5 introduces $\beta_\mathrm{cal}$ for empirical-calibration variant,
$\beta_\mathrm{cal} = 0$ certified. Total Layer 2 failure
$\beta + \beta_\mathrm{clk} + \beta_\mathrm{cal}$.

**Question:** Is the split clean enough? In the certified case, the
operator audits $\Ncasc \geq T_\beta$ as a hard inequality at
calibration time; $T_\beta$ is computed from $\alpha, \beta, R,
\delta_*$, all deployment-class. Is this enough, or do we need the
operator to certify each input constant independently (e.g., certify
$\delta_*$ via Lemma 5b/5e empirical floor), with separate failure
probabilities for each certification step?

### Q5. Is the integration-prerequisite list complete?

V5's "Integration prerequisites" paragraph lists:
- §4.10 Lemma 5d $\beta'$ drop
- §5 Theorem 1 Layer 2 proof rewrite
- §A.4 Lemma 4 prose nit
- Condition-list amendments (C5.HOEFF, C5.MULT, C5.IID, C5.SUPP, C11, C11.CLK)
- §8 Audit 7

**Question:** Are there other integration items we've missed?
- Does §2 notation table need $T_\beta, \Ncasc, \beta_\mathrm{clk},
  \beta_\mathrm{cal}, R, K_\mathrm{ch}$ surfaced?
- Does §3 invariants need updating to reflect (C11.CLK)'s event-
  throughput floor?
- Are there §6 cooperative-anchoring implications of the Layer 2
  failure decomposition?
- Does this v5 introduce so many new clauses ((C5.HOEFF), (C5.MULT),
  (C5.IID), (C5.SUPP)) that they should be bundled into a single
  "(C5.SPRT) SPRT-applicability" clause with sub-clauses, like
  (C9) BD/CL/WB/TF and (C10) CN/SU?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v6 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v5 is ready for appendix integration. The
v5 changes from v4 are: factor-of-4 algebra correction, split of
(C5) into multiple sub-clauses, certified-vs-empirical (C11.CLK),
integration-prerequisite list. If clean, proceed to integration. If
v6 needed, revise.
