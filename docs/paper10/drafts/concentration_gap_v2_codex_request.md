# Codex review request: Concentration-Gap Selection Theorem v2

## Context

This is v2 of the scoped Concentration-Gap Selection Theorem in
`drafts/concentration_gap_v2.tex`. v1 had 2 P0 + 6 P1 + 1 P2 = 9
findings; you said the algebraic kernel was unsound but Route D'
remained viable.

Progression:
- v1: 2 P0 + 6 P1 + 1 P2 = 9 findings (kernel unsound)
- v2 (this draft): targeting 0 P0 + small P1 count

## v2's structural pivot

The single biggest change: **switching from a probabilistic
deviation field to a deterministic one with explicit base
population measure $\mu$, and stating the forward bound via
$\chi^2$ divergence**.

This single change resolves multiple v1 findings simultaneously:
- **P0-1 (cross-counterparty correlation):** v1's proof needed
  cross-counterparty decorrelation that wasn't supplied. v2's
  Cauchy-Schwarz argument in $L^2(\mu; \mathcal{V})$ doesn't need
  it — cross-correlations are absorbed into $\sigma^2$
  automatically.
- **P1-1 ((NCOL) sharpness):** $\chi^2(w \| \mu)$ is a single
  scalar with a sharp definition.
- **P1-2 ($w$ random/deterministic):** v2 treats both
  deterministically.
- **P1-3 (uniform averaging on countable $\mathcal{C}$):** $\mu$
  is a fixed probability measure, well-defined.

Plus targeted fixes for the remaining v1 findings:
- **P0-2 (Lipschitz reverse):** v2's reverse claim restricted to
  $\|\Pproxy - \Ttruth\|$ level only; $g$-level lower bound
  dropped.
- **P1-4 (reverse HHI):** v2 uses $\max_c w_c \geq \HHI(w)$.
- **P1-5 (directional cancellation):** v2 uses
  $\langle u_d, \sum_{c \neq d} w_c \Delta_c\rangle \geq -\beta$.
- **P1-6 (embedding):** v2 introduces $\phi:
  \mathcal{V}_\mathrm{utility} \to \mathcal{V}$ explicitly.
- **P1-7 (coalition closure):** v2 makes coalition partitioning
  an audit precondition (COAL); latent-coalition residual is an
  explicit $\eta_\mathrm{latent}$ term.
- **P2 (terminology):** "Cauchy-Schwarz" instead of
  "parallelogram identity."

## Main results

**Theorem 1 (forward):** Under (REP) + (DISP),
$$\|\Delta(w)\| \leq \rho_\mathrm{rep} + \sigma \sqrt{\chi^2(w \| \mu)}.$$
For uniform $\mu$ on $N$, $\chi^2(w \|\mu) = N\HHI(w) - 1$, so
under low HHI ($\HHI \to 1/N$), bound $\to \rho_\mathrm{rep}$.

**Theorem 2 (reverse, norm-level only):** Under concentration
($\HHI \geq H^*$), dominant separation ($\|\Delta_d\| \geq \delta$),
and directional cancellation ($\beta$):
$$\|\Delta(w)\| \geq H^* \delta - \beta.$$

**Theorem 3 (Route-C transfer):** $|g(T) - g(P)| \leq
\Lip(g) (\rho_\mathrm{rep} + \sigma\sqrt{\chi^2} +
\eta_\mathrm{latent})$ via Microfoundation Lipschitz transfer
(forward only). No $g$-level reverse.

## Review focus

1. **Is the deterministic Cauchy-Schwarz argument rigorous?**
   Theorem 1's proof: $\|\Delta(w) - \bar\Delta\| =
   \|\mathbb{E}_\mu[(r-1)(\Delta - \bar\Delta)]\| \leq \sqrt{\mathbb{E}_\mu[(r-1)^2]}
   \cdot \sqrt{\mathbb{E}_\mu[\|\Delta-\bar\Delta\|^2]}$ via Cauchy-Schwarz in
   $L^2(\mu; \mathcal{V})$. Is the inner-product structure
   correct? Does Cauchy-Schwarz apply in this Hilbert-space-valued
   form?

2. **Is the codex counterexample resolved?** Remark 1 of v2
   argues that the v1 counterexample (identical centered
   deviations) translates to $\sigma^2 = 0$ in the deterministic
   setting, hence trivial bound. Verify.

3. **Is the latent-coalition treatment via
   $\eta_\mathrm{latent}$ residual the right move?** Or does
   coalition closure need a more structural treatment than an
   additive residual?

4. **Are the v1 findings all addressed adequately?**
   Specifically check P0-1, P0-2, and each of P1-1 through P1-7
   plus P2.

5. **Is v2 ready for integration into a companion paper?** If
   0 P0 and ≤ 2 P1, declare convergence.

## Format

For each finding:
- [P0] Critical
- [P1] Substantive
- [P2] Polish

For each: line reference, problem, suggested fix. Be specific.

If 0 P0 and ≤ 2 P1, please say "v2 is ready for integration into
the companion paper."

Output the findings list directly with no preamble.
