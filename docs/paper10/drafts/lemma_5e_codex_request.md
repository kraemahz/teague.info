# Codex review request: Lemma 5e (environment-side witness extension) — full proof draft

## Mode

**Proof verification.** Final substantive item from
`docs/paper10/TODO_proofs.md` Phase 2 work: promoting Lemma 5e
(environment-side KL floor derivation) from inline sketch to full
appendix proof, mirroring Lemma 5b's appendix proof structure
(four per-channel KL derivations).

V1 of the inline statement asserts the SPRT machinery applies
symmetrically to environment-side observables under $I_8$. This
draft promotes the assertion to an explicit per-variable
derivation parallel to Lemma 5b's appendix: Poisson + Bernoulli +
Bernoulli + Poisson for the four canonical environment-side
observables.

Same review pattern as Lemmas 1, 2, 5a, 6: write full proof →
codex review → cycle until clean → integrate.

## What to read

Primary:
- `docs/paper10/drafts/lemma_5e_full_proof.tex` — full proof draft (7pp PDF)

Reference:
- `docs/paper10/sections/lemmas.tex` §4.11 — current inline sketch
  for Lemma 5e
- `docs/paper10/appendices/proofs.tex` §A.5 (Lemma 5b) — the
  template this proof mirrors (Poisson + Bernoulli + multinomial
  per-channel derivations)
- `docs/paper10/sections/invariants.tex` $I_8$ definition (line 266)
- `docs/paper10/sections/deployment_tooling.tex` §8.1 lines 53-65 —
  $V_{\mathrm{env}}$ enumeration in deployment-tooling spec
- `docs/paper5/` (Exogenous Verification) — substrate-exclusivity
  construction that this proof argues is symmetrically extensible

## What we want from you

Five verification questions:

### Q1. Is the symmetric-construction argument rigorous?

The proof argues that Paper 5's substrate-exclusivity construction
(cryptographic commitment + ledger publication + cross-substrate
verification) extends symmetrically to environment-side witnesses
by swapping $s_{\mathrm{env}}$ for $s'$ and $v$ for agent
observables.

**Question:** Is the "mirror of Paper 5" framing rigorous, or does
it leave operational gaps? Specifically:
- Are the trust-model assumptions for environment-side ledger
  commitments transferable from agent-side without modification?
- Does the substrate-distinctness property
  ($s_{\mathrm{env}} \neq s(\mathrm{agent})$) require additional
  operational machinery beyond Paper 5's substrate partition?
- Is the trusted-setup ceremony for environment-side witnesses
  (mentioned in deployment tooling) sufficient, or does it need a
  named assumption analogous to Paper 5's at-least-one-honest
  participant?

### Q2. Are the per-variable KL floor derivations complete?

V1 has four derivations:
- $V_1$ (Poisson cooperative rate): $\delta_1^{\mathrm{env}} =
  (\lambda_0 - \eta_1) \log\frac{\lambda_0 - \eta_1}{\lambda_0} -
  (\lambda_0 - \eta_1) + \lambda_0$
- $V_2$ (Bernoulli distinctness): standard Bernoulli KL
- $V_3$ (Poisson arrival rate, with $\eta_3 > 0$ shift):
  same Poisson form but with positive shift
- $V_4$ (Bernoulli trusted-setup flag): standard Bernoulli KL

**Question:** Is each derivation complete? In particular:
- $V_3$ has the edge case $\lambda_0^{(3)} = 0$ (no baseline
  adversarial events) where the Poisson KL formally diverges;
  the draft addresses this with a regularization note ("use
  $\lambda_0^{(3)} > 0$ as a regularized baseline"). Is the
  regularization sufficient, or does it warrant a separate
  named clause / assumption?
- Are the Bernoulli derivations (V_2, V_4) symmetric in
  $\eta_v \to -\eta_v$ when adversarial alternatives could shift
  in either direction? The draft assumes downward shifts; is this
  the operationally relevant case, or should both directions be
  covered?

### Q3. Is $V_{\mathrm{env}}$ enumeration canonical?

V1 takes $V_{\mathrm{env}} = \{V_1, V_2, V_3, V_4\}$ from
deployment-tooling §8.1's enumeration. The proof mentions
"deployment-specific variables" can be added.

**Question:** Should the proof state $V_{\mathrm{env}}$ as a
deployment-policy-derived enumeration (with the four named
variables as the canonical minimum), or fix it as the canonical
four? The Paper 10 introduction and theorem statement reference
$\Aadv^{\mathrm{env}}$ without specifying $V_{\mathrm{env}}$
cardinality; should the lemma constrain it?

### Q4. Is the named residual (R2) connection correct?

The proof asserts that environment manipulations targeting
variables outside $V_{\mathrm{env}}$ fall into Theorem 1 residual
(R2).

**Question:** Is this consistent with Theorem 1's residual (R2)
statement? Currently (R2) says "Environment manipulations targeting
exogenous variables outside $V_{\mathrm{env}}$ are outside
$\Aadv^{\mathrm{env}}$ and not detected by Lemma 5e." The proof's
reverse direction (variables outside $V_{\mathrm{env}}$ fall into
(R2)) is asserted. Is the equivalence tight, or is there slippage?

### Q5. Does the proof need new theorem-level conditions?

Following the pattern of Lemmas 1, 2, 5a, 6 (each surfaced new
(C\*) conditions): does Lemma 5e require new conditions?

**Question:** Possible candidates:
- (C5.SPRT) sub-clauses (HOEFF/MULT/IID/SUPP) currently apply to
  agent-side LLR; should they explicitly cover environment-side
  LLR too? Or is the symmetry implicit?
- A new (C12) "environment-side coverage" condition stating that
  $V_{\mathrm{env}}$ exhaustively enumerates exogenous variables
  the deployment's threat model considers material? Or is this
  already implicit in $I_8$'s threshold semantics?
- A trusted-setup honesty assumption analogous to Paper 5's?

If new conditions are warranted, name them and recommend whether
they bundle under existing conditions or stand alone.

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any
  minor refinements.
- **Issue identified** — name precisely; recommend whether v2
  needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 5e v1 is ready for appendix integration
(§A.8), or whether v2 is needed. After Lemma 5e is integrated,
all Phase 2 proof-promotion work in TODO_proofs.md is complete.
