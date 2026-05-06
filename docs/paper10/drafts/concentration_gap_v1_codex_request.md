# Codex review request: Concentration-Gap Selection Theorem v1

## Context

We're attempting to discharge (a scoped version of) the
Microfoundation paper's Concentration-Gap Conjecture, taking codex's
recommended Route D$'$:

1. Algebraic weighted-selection theorem first (algebraic kernel).
2. Counterparty-selection interpretation second.
3. Route-C transfer to GFM Goodhart slack third.

You evaluated this route in the prior consultation
(`drafts/concentration_gap_route_codex_request.md`) and assessed
it as the most tractable route, with explicit pitfalls flagged
around representativeness and non-collusion.

This draft (`drafts/concentration_gap_v1.tex`) is the v1 attempt.

## Main results

**Theorem 1 (Algebraic weighted-selection):** Let $\Delta_c \in
\mathcal{V}$ be a deviation field on counterparties $c \in
\mathcal{C}$, with $\HHI(w) = \|w\|_2^2$. Under representativeness
$\rho_{\mathrm{rep}}$, dispersion $\sigma$, non-collusion $\eta$:

- Forward: $\mathbb{E}\|\Delta(w)\|^2 \leq \rho_{\mathrm{rep}}^2 +
  \sigma^2 \HHI(w) + 2\eta$
- Reverse: if dominant counterparty $d$ has share $\alpha$ and
  $\|\Delta_d\| \geq \delta$, with cancellation bound $\beta$,
  then $\|\Delta(w)\| \geq \alpha\delta - \beta$, with $\HHI \geq
  \alpha^2$.

**Theorem 2 (Concentration-Gap Selection Theorem, scoped):**
Combining Theorem 1 with Microfoundation's Lipschitz transfer:
$\mathbb{E}|g(T) - g(P)|^2 \leq \mathrm{Lip}(g)^2 \cdot
(\rho_{\mathrm{rep}}^2 + \sigma^2 \HHI + 2\eta)$.

This replaces SA1 (a single opaque conjecture) with the conjunction
(REP) + (DISP) + (NCOL) (three operationally auditable structural
conditions).

## Review focus

Please review `drafts/concentration_gap_v1.tex` and check:

1. **Is the forward proof of Theorem 1 correct?**
   - Specifically, the cross-counterparty correlation step
     ($\mathbb{E}\langle \Delta_c - \bar\Delta, \Delta_{c'} -
     \bar\Delta\rangle = 0$ or bounded by $\eta$) is the
     load-bearing piece. Is the bound stated correctly? Are the
     covariance/cross-term arguments cleanly structured?

2. **Is the reverse proof of Theorem 1 correct?**
   - Triangle inequality + $\HHI \geq \alpha^2$ is the structure.
     Is anything missing? Is the cancellation $\beta$ definition
     too vague to be useful?

3. **Is the counterparty-selection interpretation faithful to the
   GFM trade-flow setting?**
   - Is the deviation $\Delta_c = U_c - W$ the right
     identification? Does the trade-flow weighting $w_c$ match
     paper 10's invariant $I_5$ semantics?

4. **Does the Route-C transfer (Theorem 2) carry over the bound
   intact?**
   - The Microfoundation Lipschitz transfer is forward-only:
     $\|P - T\|$-level bounds carry to $|g(T) - g(P)|$ via
     $\mathrm{Lip}(g)$. The reverse direction is asymmetric (no
     $g$-level lower bound from $\|P - T\|$-level lower bound).
     Is this asymmetry correctly handled?

5. **Are the structural conditions (REP), (DISP), (NCOL)
   operationally meaningful?**
   - You flagged in the prior consultation that "representative
     non-collusion" would be the load-bearing assumption. Is the
     formalization in v1 sharp enough? Are the audit hooks
     (counterparty independence, dispersion estimation, coalition
     detection) realistic?

6. **Did v1 miss any structural conditions you flagged?**
   - Cross-counterparty deviation correlations (industry,
     governance bloc) — are these absorbed by (NCOL) cleanly, or
     do they need a separate condition?
   - Hidden-coalition behavior of many small counterparties — is
     this captured in the current formalization?

7. **Is this v1 close to convergent, or are there structural
   issues that would require a v2 framework rebuild?**
   - We want to know early if the algebraic kernel needs a
     fundamentally different structure (e.g., the cross-correlation
     handling is wrong) vs. if it's converging and just needs
     tightening.

## Format

For each finding:
- [P0] Critical: proof is wrong, or the theorem doesn't deliver
  what's claimed
- [P1] Substantive: gaps in proof or definitions
- [P2] Polish: presentation could be clearer

For each: line reference into `concentration_gap_v1.tex`, problem
description, suggested fix. Be specific. Aim for 5-12 findings.

If v1 has 0 P0 findings, please say "the algebraic kernel is
sound; iterating to v2 is worthwhile." If v1 has any P0 findings
that imply a framework rebuild, say so explicitly.

Output the findings list directly with no preamble.
