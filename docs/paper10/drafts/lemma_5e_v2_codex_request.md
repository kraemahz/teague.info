# Codex review request: Lemma 5e v2 — re-review after Round A revisions

## Mode

**v2 confirmation review.** Round A returned "v2 needed" with five
issues, all addressable. Q1 (trust model not transferring), Q2 (KL
derivation gaps: missing DPI step, support conventions, two-sided),
Q3 ($\Vem$ enumeration policy + $I_8$ vs deployment-tooling
mismatch), Q4 (R2 connection refinement), Q5 (theorem-level
conditions needed).

V2 fixes:

- **Q1 trust model**: Added (C12.ENV-WIT) with four sub-clauses:
  - (C12.PUB) Published fixed $\Vem$
  - (C12.PART) Source/witness substrate partition
  - (C12.TRUST) Witness substrate outside adversary write-access /
    failure-correlation domain
  - (C12.SETUP) Trusted-setup honesty (Paper 5's at-least-one-honest
    participant)

- **Q2 KL derivations**: Added marginal-to-joint KL via DPI;
  Bernoulli baseline restricted to $(\eenv, 1-\eenv') \subset (0,1)$
  open; Poisson baseline $\lambda_0 \geq \eenv > 0$ regularized;
  non-overlapping support fallback via (C5.HOEFF) clipping inherited
  through Lemma 6; two-sided floor option for any-direction shifts.

- **Q3 $\Vem$**: Made deployment-policy-derived per (C12.PUB), with
  four canonical variables as illustrative minimum. Reconciled $I_8$
  vs deployment-tooling: dropped $\Delta r_K$ (strategy-dependent,
  not exogenous), added trusted-setup status flag.

- **Q4 R2 refinement**: R2 covers manipulations targeting only
  unmonitored exogenous variables AND producing no threshold-
  exceeding monitored shift. Manipulations of unmonitored variables
  that causally shift monitored $v \in \Vem$ are detected via
  monitored projection.

- **Q5 theorem-level conditions**: Introduced (C12.ENV-WIT) bundle
  matching (C5.SPRT)/(C9.*)/(C10.*) pattern. Plus expansion of
  (C5.SPRT) sub-clauses to explicitly cover environment-side LLR.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5e_full_proof_v2.tex` — v2 (11pp PDF)

Reference:
- Round A findings: `b51wlvm15.output` lines 3098-3196
- `docs/paper10/sections/lemmas.tex` §4.11 — current inline sketch
- `docs/paper10/appendices/proofs.tex` §A.5 (Lemma 5b) — template

## What we want from you

Five v2 verification questions:

### Q1. Is (C12.ENV-WIT)'s four sub-clause factoring right?

V2's bundle: PUB / PART / TRUST / SETUP. Is the factoring tight, or
should (TRUST) be split (write-access vs failure-correlation are
distinct)? Is (SETUP) sufficient as a cross-reference to Paper 5's
honesty assumption, or should it repeat the assumption explicitly?

### Q2. Is the DPI step rigorous?

V2 adds: $D_{KL}(q \| p_0^{\mathrm{env}}) \geq D_{KL}(q_{v_i} \|
p_{0,v_i}) \geq \delta_i^{\mathrm{env}}$ via DPI on the
marginalization map. Is this tight? In particular: the DPI requires
the witness-recorded $v_i$ is a deterministic function of the joint
state — does the proof need to verify this precondition for each
canonical variable, or is the determinism implicit in the
witness-recording machinery?

### Q3. Is the $\Vem$ reconciliation right?

V2 drops $\Delta r_K$ from $\Vem$ (strategy-dependent, agent-side),
adds trusted-setup status flag. Is $\Delta r_K$ correctly classified
as agent-side? Does any other Paper 10 proof rely on $\Delta r_K$
being witnessed by $I_8$ specifically (rather than agent-side
mechanism)?

### Q4. Is the R2 refinement consistent with Theorem 1?

V2 refines R2: "manipulations targeting only unmonitored exogenous
variables AND producing no threshold-exceeding monitored shift." Is
this consistent with the Theorem 1 R2 statement at
`main_theorem.tex` line 218 ("Environment manipulations targeting
exogenous variables outside $V_{\mathrm{env}}$ are outside
$\Aadv^{\mathrm{env}}$ and not detected by Lemma 5e")? Should the
integration update Theorem 1's R2 wording?

### Q5. Are (C12.ENV-WIT) sub-clauses the right framing?

V2 introduces (C12.ENV-WIT) parallel to (C5.SPRT)/(C9.*)/(C10.*).
Is the bundle's structure right? Should:
- (C5.SPRT) be expanded to explicitly cover both agent-side and
  environment-side LLR (currently (C5.IID) references $\delta_*$
  union but other sub-clauses don't explicitly mention environment)?
- $\eenv$ surface as a separate (C5.SUPP) sub-clause for support
  conventions, or fold into Audit 7?
- The (C12.ENV-WIT) sub-clauses live as expanded $I_8$ instead?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v3 needed
  or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 5e v2 is ready for appendix integration (§A.8).
After 5e is integrated, all Phase 2 proof-promotion work in
TODO_proofs.md is complete.
