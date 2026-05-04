# Codex review request: Lemma 6 v6 — re-review after Round E revisions

## Mode

**v6 confirmation review.** Round E returned "v6 needed but
narrow": Q1 (rigorous Hoeffding inversion) was confirmed Sound, but
four narrow issues remained (Q2 $R$ range-width mismatch, Q3
(C5.IID) contradictory phrasing, Q4 empirical $\Ncasc$ sign error,
Q5 bundling under (C5.SPRT) + integration list expansion).

V6 fixes:

- **Q2 $R$ range-width disambiguation.** Renamed clip radius to
  $\Bclip$ (symmetric clip $[-\Bclip, \Bclip]$) and Hoeffding
  range to $\Rh = 2\Bclip$ (Lemma 4's $R = b - a$ convention). Step 5
  now uses $\Rh$ throughout: $\Tbeta = \max\{2A/\delta_*, 2\Rh^2
  \log(1/\beta)/\delta_*^2\}$. Plus added "monitored partition
  fixed before deployment" clause to (C5.MULT).

- **Q3 (C5.IID) reformulation.** Now: adapted increments with
  conditional mean $\geq \delta_n \geq \delta_*$; centered increments
  $\tilde\ell_n := \ell_n - \mathbb{E}[\ell_n | \mathcal{F}_{n-1}]$
  form the martingale-difference sequence. Plus explicit note that
  $\delta_*$ is **post-clipping** drift floor. (C5.SUPP) simplified
  (clipping makes finiteness automatic).

- **Q4 empirical sign fix.** $\Ncasc$ now certified **lower** bound,
  $\Bclip$ upper, $\delta_*$ lower. Total Layer 2 failure $\beta +
  \beta_\mathrm{clk} + \beta_\mathrm{cal}$ with sign-direction
  discipline.

- **Q5 bundle into (C5.SPRT).** HOEFF/MULT/IID/SUPP bundled under
  single (C5.SPRT) "SPRT-applicability" condition with sub-clauses,
  matching (C9.*) and (C10.*) patterns. Plus expanded integration
  prerequisites: §2 notation, §4.10/§4 statements, §3 invariants
  ($I_{11}$ connection), §8 Audit 7, §6 noted as no-update.

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof_v6.tex` — v6 (17pp PDF)

Reference:
- Round E findings: `brqs6pu5s.output` lines 5599-5697
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — exact
  Hoeffding form using $R = b - a$ convention

## What we want from you

Five v6 verification questions:

### Q1. Is the range-width discipline now consistent end-to-end?

V6 separates clip radius $\Bclip$ from Hoeffding range $\Rh =
2\Bclip$, matching Lemma 4's $R = b - a$ convention.

**Question:** Is the range-width discipline now consistent? In
particular: does the appendix Lemma 4 statement (referenced as
$R = b - a$) need to be updated to use the $\Rh$ symbol explicitly,
or is the convention sufficiently anchored by v6's prose?

### Q2. Is (C5.SPRT) bundling correct, and is (C5.MULT) adversarial-channel clause sufficient?

V6 bundles HOEFF/MULT/IID/SUPP under (C5.SPRT) with sub-clauses.
(C5.MULT) now includes "monitored partition fixed before deployment;
adaptive channel creation falls into residual class."

**Question:** Is the bundling clean, and is the adversarial-channel
clause sufficient? Does adversarial **selection among already-
monitored channels** (not creation of new ones) need additional
treatment, or is it already covered by the per-channel KL floor
structure of Lemmas 5b/5e?

### Q3. Is (C5.IID) reformulation right, and is the post-clipping drift verification sufficient?

V6 reformulates (C5.IID) to avoid v5's contradiction: now adapted
increments with conditional mean $\geq \delta_n \geq \delta_*$,
centered increments form martingale differences. $\delta_*$ is the
post-clipping drift floor.

**Question:** Is this the right framing for Hoeffding-Azuma to
apply? Does the post-clipping drift verification need its own audit
sub-item (Audit 7 expansion) or is it implicit in the (C5.SPRT)
bundle?

### Q4. Is the empirical-calibration sign-direction discipline correct end-to-end?

V6 corrects v5's sign error: $\Ncasc$ certified **lower**, $\Bclip$
**upper**, $\delta_*$ **lower**. All conservative.

**Question:** Is the sign-direction discipline correct end-to-end?
Are there other places in the proof where sign-direction issues
could lurk (e.g., in the post-clipping drift verification, or in
the relationship between raw KL floor from Lemmas 5b/5e and the
clipped drift floor)?

### Q5. Is the integration-prerequisite list complete enough to drive the integration patch?

V6's integration-prerequisite section now covers: §2 notation,
§4.10 Lemma 5d, §4 Lemma 4, §A.4 prose nit, Theorem 1 Layer 2 proof,
$\beta'$ legacy drop, (C5.SPRT)/(C11)/(C11.CLK) additions, §3
invariants/$I_{11}$ connection, expanded Audit 7, §6 explicitly
noted as no-update.

**Question:** Is the list complete? Or are there integration items
still missing — e.g., interaction with §7 (philosophical and
ethical considerations), §9 (related work), or front-matter
abstract / introduction that mention $\beta'$ or other legacy
constants?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v7 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v6 is ready for appendix integration.
Round D was "v5 needed", Round E was "v6 needed but narrow"; if v6
is clean, proceed to integration. If v7 needed, revise — but at
this point we expect at most editorial polish, not structural
issues.
