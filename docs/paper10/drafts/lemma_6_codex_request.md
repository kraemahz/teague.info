# Codex review request: Lemma 6 ($h_{\mathrm{detect}}$ intensivity) — full proof draft

## Mode

**Proof verification.** Fourth item from `docs/paper10/TODO_proofs.md` Phase 2 work: formalizing the $h_{\mathrm{detect}}$ intensivity claim that Theorem 1's Layer 2 currently asserts informally.

V1 of the theorem proof referenced Microfoundation's "T failure modes" remark for the per-step gap-growth rate but didn't formalize it. This draft promotes the assertion to formal Lemma 6 with explicit (C11) bounded gap-growth rate condition.

Same review pattern: write full proof → codex review → cycle until clean → integrate.

## What to read

Primary:
- `docs/paper10/drafts/lemma_6_full_proof.tex` — full proof draft (5pp PDF)

Source paper sections:
- `docs/paper9/sections/goodhart.tex` — Microfoundation's "T failure modes" remark
- `docs/paper6/sections/absorbing_state.tex` — Phase Redundancy's metastable lifetime $\tau_{\mathrm{meta}}$

Reference:
- `docs/paper10/sections/main_theorem.tex` Layer 2 — where Lemma 6 plugs in
- `docs/paper10/appendices/proofs.tex` §A.4 (Lemma 4) — SPRT tail bound that Lemma 6 composes with
- `docs/paper10/sections/lemmas.tex` §4.10 (Lemma 5d) — tail composition

## What we want from you

Five verification questions:

### Q1. Is continuous-time (C11) the right formalization?

The proof uses $d\epsgap/dt \leq \rho_g(\deltaadv)$ in continuous time. The theorem's actual application context could be either:
- Continuous monitoring (PRT runs continuously; rates are continuous)
- Discrete event ledger (PRT updates per-event; rates are per-step)

**Question:** Which formulation is more appropriate, and does the equivalence-under-step-time-normalization argument hold rigorously?

### Q2. Is $h_{\mathrm{detect}}$'s definition correct?

The proof defines $h_{\mathrm{detect}}$ as the time-integrated gap during the detection window:
$h_{\mathrm{detect}} = \int (d\epsgap/dt) dt \leq T_{\mathrm{detect}} \cdot \rho_g$

**Question:** Should $h_{\mathrm{detect}}$ be:
- (a) the integrated gap accumulated during detection window (current draft), or
- (b) the supremum instantaneous gap during the window?

Theorem 1's Layer 2 applies $h_{\mathrm{detect}}$ as a bound on $|g(T) - g(P)|$, which is point-in-time. Should we use (b) instead?

### Q3. Is (C11) correctly distinguished from (C6) bounded-Lipschitz?

The discussion notes (C6) is alignment-property-side (Lipschitz of $g$) and (C11) is gap-dynamics-side (rate of $\epsgap$ growth).

**Question:** Is this distinction watertight, or does (C11) reduce to a consequence of (C6) plus channel-dynamics structure under some additional conditions?

### Q4. Is the Lemma 5d tail-bound translation rigorous?

The proof argues: with probability $1 - \beta'$, $T_{\mathrm{detect}} \leq T_{\mathrm{cascade}}$, so $h_{\mathrm{detect}} \leq \rho_g \cdot T_{\mathrm{cascade}}$.

**Question:** Does this correctly translate the tail bound into an integrated gap bound, or does it lose information about the per-trajectory gap evolution?

### Q5. Should (C11) be promoted to theorem-level condition?

Following the pattern of (C6)-(C10) added in earlier lemmas: (C11) bounded gap-growth rate as a theorem condition, analogous to (C7) bounded co-evolution.

**Question:** Should (C11) be a theorem-level condition? Or can it remain a Lemma 6-internal assumption without theorem-level surfacing?

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration with any minor refinements.
- **Issue identified** — name precisely; recommend whether v2 needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 6 v1 is ready for appendix integration, or whether v2 is needed before integration.
