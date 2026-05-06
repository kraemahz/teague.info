# Codex consultation: Choosing a proof route for the Concentration-Gap Conjecture

## Context

The Goal-Frontier Maximization (GFM) sequence's Microfoundation
paper (`lasser2026micro`) introduces the **Concentration-Gap
Conjecture**: optimization pressure on the proxy correlates with
proxy-truth gap exploitation. The conjecture is currently
**deferred** in Microfoundation as open work.

Paper 10 (deployment-safety theorem) currently inherits this
conjecture as a non-derived premise via Assumption SA1 (HHI
surrogate adequacy: $\HHI < H^* \Rightarrow$ deployment is outside
the optimization-pressure regime). We've now done a closed-form
derivation of the bounded-co-evolution assumption (C7) — that loose
thread is closed.

The remaining loose threads in paper 10 are:
1. **The Concentration-Gap Conjecture itself** (Microfoundation's
   conjecture, inherited).
2. **SA1** (HHI as a surrogate for the optimization-pressure
   regime).

If we can **prove the Concentration-Gap Conjecture**, paper 10
collapses to depending on at most SA1 (and possibly nothing if SA1
follows from a proven Concentration-Gap as a structural corollary).
This would let us:
- Strengthen paper 10's formal closing.
- Factor the C7 closed-form + Concentration-Gap proof into a
  companion paper.
- Reduce paper 10's content dramatically.

## The conjecture's content (informal)

> Optimization pressure on the proxy correlates with proxy-truth
> gap exploitation.

Operationalization in Microfoundation (paper 9): trade-flow
concentration (HHI) is the surrogate for "optimization pressure";
gap exploitation is operationalized via the proxy-truth divergence
$\epsilon_\mathrm{nonres}$ on the active subspace.

The conjecture is hard precisely because:
- "Optimization pressure" doesn't have a unique formal definition
  in the GFM apparatus.
- "Gap exploitation" mixes formal proxy-truth divergence with
  behavioral (adversarial selection) content.

So the first move is **choosing which formalization to attempt**.

## Four candidate proof routes

### Route A — Information-theoretic / data-processing

**Setup.** $P$ = proxy random variable, $T$ = truth random variable.
Optimization pressure operates as a Markov kernel on $P$ that may
or may not preserve mutual information $I(P; T)$.

**Claim.** Under selection that doesn't preserve $I(P; T)$, the gap
grows by a data-processing inequality bound. Concentrated pressure
$\equiv$ degenerate kernel that pushes mass toward low-entropy
configurations.

**Connections to existing literature:** El-Mhamdi & Hoang 2024 ("On
Goodhart's law"), Majka & El-Mhamdi 2025 ("Strong, Weak, and Benign
Goodhart's Law").

### Route B — Game-theoretic / market-power

**Setup.** Counterparties bid for capability access via trade flows;
trade-flow distribution is an equilibrium; HHI measures market
concentration.

**Claim.** Under perfect competition (HHI $\to 0$), first welfare
theorem gives Pareto efficiency, hence proxy ≈ truth. Under monopoly
(HHI $\to 1$), the dominant counterparty extracts rents, and
proxy-truth divergence equals the deadweight loss.

**Connections to existing literature:** Arrow 1951, Mas-Colell,
Whinston & Green 1995, Adler 2012 (welfare economics chain that the
GFM sequence already cites).

### Route C — Structural / Lipschitz-with-distortion

**Setup.** Microfoundation Theorem 2 gives Lipschitz transfer
$|g(T) - g(P)| \leq L \cdot \|P - T\|$. Optimization pressure is a
specific perturbation class (e.g., gradient ascent on $P$); bound
$\|P - T\|$ growth in terms of pressure magnitude.

**Claim.** Under per-counterparty bounded-Lipschitz dynamics,
$\|P - T\|$ grows at rate proportional to the dominant counterparty's
effective gradient, which is bounded above by HHI-derived market
share.

**Connections:** This is internal extension of GFM's existing
Lipschitz-transfer machinery; minimal new framework.

### Route D — Selection theorem (Manheim-Garrabrant style)

**Setup.** Each counterparty $c$ has utility $U_c$, possibly
differing from the welfare-relevant truth $W$. Each $c$ selects
trade flows to maximize $\mathbb{E}[U_c]$. HHI measures how much the
equilibrium reflects any single $c$'s utility vs. an average across
many counterparties.

**Claim.** Under low HHI (many counterparties, no dominant one),
the equilibrium approximates the population-average utility, which
approximates $W$ (under structural representativeness assumptions).
Under high HHI, the dominant counterparty's $U_c$ — which differs
from $W$ — drives the equilibrium, and the proxy-truth gap is
bounded below by the divergence $\|U_c - W\|$.

**Connections to existing literature:** Manheim & Garrabrant 2019
("Categorizing Variants of Goodhart's Law" — Adversarial Goodhart),
Hubinger et al. 2019 (mesa-optimization terminology), El-Mhamdi &
Hoang 2024.

## Author's preliminary ranking

The author (Teague) leans toward Route D as the first attempt, with
Route C as fallback:

| Route | Tractability | Coverage | Literature support | New framework needed |
|---|---|---|---|---|
| A (info-theoretic) | medium | partial | medium | medium |
| B (market-power) | low-medium | full | high | high |
| C (Lipschitz extension) | high | partial (upper-bound only) | medium | low |
| D (selection theorem) | medium-high | full | high | medium |

Reasoning for D:
- Captures the conjecture's bidirectional correlation directly.
- Existing literature support strong (Manheim & Garrabrant + El-Mhamdi
  & Hoang already cited in paper 10).
- Maps onto the GFM vocabulary (counterparties, trade flows, market
  structure).
- The "representativeness" assumption it needs is itself a meaningful
  structural condition that operators can audit.

## What we want from codex

Please weigh in on the route choice. Specifically:

1. **Which route do you assess as most tractable for an actual
   formal proof?** Consider both:
   (a) the technical difficulty of the proof itself, and
   (b) the connection to existing literature that we can leverage.

2. **Which route most directly addresses what the conjecture
   claims?** "Optimization pressure correlates with gap
   exploitation" — does any of A/B/C/D capture this content
   *better* than the others, or are they all partial captures of
   different facets?

3. **Are there proof routes we missed?** Other formalizations of
   "optimization pressure" or "gap exploitation" that admit cleaner
   proofs.

4. **What pitfalls should we anticipate for our preferred route
   (Route D)?** Where might the proof get stuck? What structural
   assumption is the proof most likely to depend on, and is that
   assumption itself reasonable to verify?

5. **If you had to bet, which route is most likely to converge in
   3-5 codex review iterations (matching our C7 cycle), vs. which
   is likely to expand into a multi-paper research program?** We
   want a route that can plausibly close in a focused effort, not
   one that opens into an indefinite agenda.

## Output

Direct evaluation of each route's prospects, then a recommendation.
If you recommend a route different from Route D, explain why. If
you think the conjecture is structurally not provable without
significant new framework (i.e., Microfoundation deferred it for
good reason), say so explicitly — we'd rather know that up-front
than discover it after several drafts.

Output format: assessment of each route, then a final ranking with
reasoning. No preamble.
