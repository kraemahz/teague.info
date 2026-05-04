# Codex review request: Lemma 1 (Intensive composition under co-evolution) — full proof draft

## Mode

**Proof verification.** This is the first item from
`docs/paper10/TODO_proofs.md` Phase 2 work: promoting Lemma 1 from
inline proof outline to a self-contained formal proof for the
appendix.

The current Paper 10 §4.2 has an inline proof outline. This draft
formalizes the proof with named assumptions (A1-A4), explicit
constants, and step-by-step derivations. We want to verify the
proof is rigorous before integrating into the appendix.

## What to read

Primary:
- `docs/paper10/drafts/lemma_1_full_proof.tex` — the full proof
  draft (6pp PDF)

Source paper sections referenced:
- `docs/paper9/sections/goodhart.tex` — Composition Proposition 1
  and the four-channel decomposition (the bound A4 references)
- `docs/paper9/sections/structural_predictions.tex` — the residual
  class structure (A2)
- `docs/paper9/sections/empirical.tex` — per-channel quantities (A1)

Reference (for context):
- `docs/paper10/main.pdf` — current Paper 10 draft, §4.2 has the
  current inline outline this proof replaces
- `docs/paper10/TODO_proofs.md` — Phase 2 work plan

## What we want from you

Five verification questions from the proof draft's §"Specific
verification questions for codex review":

### Q1. Is Definition 1 (intensive in $|P|$) the right formalization?

The draft uses a uniform-constant formulation: a bound is intensive
if there exists $C \geq 0$ independent of $|P|$ such that the bound
$\leq C$ for all valid deployment states.

Question: Is this the right convention? Alternative: $|P|$-asymptotic
intensivity ($\limsup_{|P| \to \infty}$ bound is finite). Does the
uniform-constant formulation match what the deployment claim actually
needs?

### Q2. Are Assumptions A1-A4 stated correctly?

(a) A1 (per-channel non-residual gap intensivity): Each
$\epsnonresChannel{c} \leq K_c$ independent of $|P|$. Justification
references Microfoundation paper's per-channel definitions.
**Question:** Does A1 actually follow from Microfoundation, or does
it require additional content not in the source paper?

(b) A2 (residual floor intensivity): $\epsfloor \leq K_{\mathrm{floor}}$
independent of $|P|$. Justification: residual class is
structurally-unobservable subset bounded by per-capability
unobservability rate.
**Question:** Is A2 defensible, or could the residual class grow
with $|P|$ in some deployment regimes?

(c) A4 (co-evolution error bound): $(\epsnonresCoev)_+ \leq
K_{\mathrm{coev}} \cdot M(\text{deployment})$ from Composition
Proposition 1.
**Question:** Is A4's bound actually established by Microfoundation's
Composition Proposition 1, or does that proposition give a different
(potentially weaker) bound?

### Q3. Is the proof step-by-step rigorous?

(a) Step 3 absorbs $M(\text{deployment})$ into the constant
$K_{\mathrm{coev}}'$. Does this hide any $|P|$-dependence?

(b) Step 6 uses $\lambda \in [0,1]$ to bound $\lambda \cdot
K_{\mathrm{floor}} \leq K_{\mathrm{floor}}$. Could $\lambda$ depend
on $|P|$ in some deployment regimes? If so, does the proof break?

### Q4. Is the constant-existence-without-numerical-values approach acceptable?

The proof asserts the constants $K_c, K_{\mathrm{coev}}, M,
K_{\mathrm{floor}}, K_{\mathrm{Lip}}$ exist and are independent of
$|P|$, but does not derive their numerical values.

**Question:** Is this acceptable for Paper 10's purposes? Or does
the paper need to specify computational procedures for each
constant?

### Q5. Is the Layer 1 connection (proof draft §6) correct?

The draft asserts $h_{\mathrm{static}}(\theta) \leq C^* /
\mathrm{Lip}(g) = K_{\mathrm{gap}}$, claiming this captures
Lemma 1's role in Theorem 1's Layer 1 proof.

**Question:** Is this connection correctly stated? Does it match
how Theorem 1's Layer 1 proof in `docs/paper10/sections/main_theorem.tex`
actually invokes Lemma 1?

## Output format

For each Q1-Q5:
- **Sound** — confirmation with any minor refinements.
- **Issue identified** — name the issue precisely; recommend whether
  the proof needs revision (v2) or can be addressed with a remark.
- **Significant problem** — explain the structural obstruction and
  what would be needed to resolve.

If you find a soundness issue we did not name, flag it.

## Background discipline

We will iterate: write full proof → codex review → fix any issues →
re-review until clean → integrate into appendix. Per
`TODO_proofs.md`, Lemma 1 is the first of several proofs to
promote (Lemmas 2, 5a, 5e to follow, plus theorem-level
formalizations for $h_{\mathrm{detect}}$ intensivity and the (C6),
(C7) conditions).

The goal of this round: settle whether the Lemma 1 proof above is
rigorous enough for appendix placement, or whether it needs another
draft pass.
