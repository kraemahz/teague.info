# Paper 8 Reframing: Revealed-Sacrifice Observation

*Reframing memo. Authored 2026-04-14 after Paper 7 draft completion, during
discussion of the Paper 8 direction. The existing outline at
`paper8_outline.md` remains on disk but is superseded by this reframing for
the central thesis. Machinery from the old outline (exercise indicator, gap
decomposition, wireheading detection, worked example) remains useful as
supplementary material but is no longer load-bearing for the paper's main
result.*

## The reframing

The old thesis posed $\mathrm{vol}_R$ as a measure the framework computes
directly via structural counterfactual queries on the capability poset
(`e_t(d) = 1` iff removing $d$ makes some realized output unrealizable). This
has two failures the framing did not surface:

1. **Tractability failure.** The counterfactual query is worst-case
   exponential in pathway length and requires global knowledge of every
   realized output the collective produces. Even with Paper 2's polynomial-time
   $\mathrm{vol}_P$ computation, the sheer enumeration of realized outputs
   over an observation window is not operationally feasible at scale.

2. **Privacy failure (load-bearing).** Computing realized-output sets requires
   observational access to what the collective actually does — what outputs
   each agent produces, what cooperative outputs emerge, what each capability
   contributes. This is the total-surveillance scenario. The framework's
   operational commitments elsewhere (Paper 5's cryptographic opacity, Paper
   6's cross-substrate channel discipline, Paper 7's bounded-scope testing)
   explicitly rule out panopticon-style observation. $\mathrm{vol}_R$ as
   defined in the old outline contradicts those commitments.

## The new thesis

> Direct measurement of $\mathrm{vol}_R$ requires a privacy sacrifice
> incompatible with the framework's operational commitments. Revealed-sacrifice
> observation is a privacy-minimal surrogate: agents disclose
> $\mathrm{vol}_R$-content through voluntary trades — commitments that
> surrender a benchmarkable capability in exchange for an unbenchmarked bundle.
> The framework bounds $\mathrm{vol}_R$ from below using only those events.
> Aggregate trade streams, optionally passed through commitment or
> zero-knowledge proofs, recover a constructive lower bound on the
> unbenchmarked portion of $\mathrm{vol}_R$ without additional observation
> rights beyond those the trade events already create.

This converts the B-to-C gap from "unknown divergence" (a structural hole)
into "lower-bounded divergence" (a characterized partial order).

## Formal observation model

**Definition (Revealed-Sacrifice Event).** A revealed-sacrifice event is a
tuple $(i, X, Y, t)$ where agent $i$ at time $t$ commits to surrendering
benchmarked capability $X$ with known $\Delta\mathrm{vol}_P(X)$, in exchange
for unbenchmarked bundle $Y = \{Y_1, \ldots, Y_k\}$. The channel emits the
signal
$$\mathrm{vol}_R^{\mathrm{lower}}(Y) \geq \Delta\mathrm{vol}_P(X).$$

The revealed-preference inequality is: $U_i(Y) \geq U_i(X)$ by free choice, and
under the framework's standing assumption that $\mathrm{vol}_P$ is an
operational target on the benchmarked subspace (the B-to-C precondition from
Paper 6's framing), this gives the lower bound on $\mathrm{vol}_R$ of the
unbenchmarked side of the trade.

**Proposition (Aggregate B-to-C Lower Bound).** For a sequence of
revealed-sacrifice events $\{(i_n, X_n, Y_n, t_n)\}_{n=1}^N$ with bundles
jointly covering a subset $\mathcal{U}$ of unbenchmarked capability-space,
$$\mathrm{vol}_R^{\mathcal{U}} \geq \sum_{n=1}^N \Delta\mathrm{vol}_P(X_n)
\cdot w_n,$$
where $w_n \in [0, 1]$ are bundle-disaggregation weights obtained by standard
hedonic-regression decomposition of overlapping bundles. If the $Y_n$ jointly
exhaust $\mathcal{U}$, the sum closes the B-to-C gap on $\mathcal{U}$ from
below by a characterized quantity.

## Why the two sacrifice types matter separately

The sacrifice dimension splits cleanly into two observation channels:

**Money-sacrifice channel.** Benchmarked capability $X$ is purchasing power.
The trade exchanges priced goods for unpriced bundles (buy-a-boat for
water-access-plus-social). Signal is the price. Privileges capabilities
valued by wealthier agents; market-scale aggregation handles the distributional
loading.

**Time-sacrifice channel.** Benchmarked capability $X$ is the agent's
outside-option labor hours, valued at market wage rate $r$. The trade exchanges
hours-at-wage for unpriced bundles (volunteering, parenting, craft practice,
relationship-building). Signal is $r \cdot \mathrm{hours}$. Captures
$\mathrm{vol}_R$ content that the money channel misses entirely — arguably
more important for overall $\mathrm{vol}_R$ since time is the scarcest
capability every agent shares and time-sacrifice bundles include most
identity-constitutive activity.

The residual class (see below) is the intersection of what neither channel
catches.

## Privacy discipline as load-bearing

The revealed-sacrifice channel is privacy-minimal in a formal sense that
should be the paper's structural invariant:

1. **No interior access.** The framework never observes what the agent values
   privately, only what they commit to publicly through sacrifice.

2. **Consent via participation.** Markets and labor are opt-in. Non-trading is
   honored by silence; an agent who doesn't participate emits no signal, and
   the framework draws no inference.

3. **Discretization as a feature.** Trade events are sparse by construction;
   the signal is bounded by trade frequency, not by observation intensity.

4. **Commitment-layer composability.** `lasser2026exo`'s cryptographic
   commitment protocol (Definition 13, Risk-Claim Protocol) extends: a
   revealed-sacrifice event can be committed as a proof-of-trade exposing only
   the $\mathrm{vol}_R$-category and $\Delta\mathrm{vol}_P$-magnitude, not
   counterparty, price, or specific goods. Zero-knowledge rollups over
   aggregate trade volume are feasible and preserve the lower-bound property.

5. **Third-party observability.** Unlike Paper 7's controlled relaxation
   (which requires the framework to *impose* a test on the agent) and unlike
   Paper 5's verification (which requires the agent to *participate* in a
   commitment), revealed-sacrifice events are observable from public-facing
   ledger data (market exchanges, payment rails, public commitments) with no
   agent participation required. This changes the adversarial model: the
   non-cooperative agent who refuses to commit or to be tested still has to
   buy things and spend time to operate, so still emits the signal.

## The shared discipline across Papers 7 and 8

**Resolution through frequency, not through depth.**

- Paper 7's controlled relaxation: more precision on risk claims comes from
  running more tests, not from surveilling each test more intrusively.
- Paper 8's revealed sacrifice: more precision on $\mathrm{vol}_R$ comes from
  observing more trades, not from observing each trader more intrusively.
- Paper 6's phase boundary: $\rho_{\min}^{\mathrm{cross}}$ counts channels,
  not observation depth per channel.

Both papers in the later sequence refuse the panopticon move. This is
consonant with the GFM sequence's broader position and should be stated as a
design principle in Paper 8's introduction.

## Duality with Paper 7

Paper 7 and Paper 8 form a complementary pair:

| | Paper 7 (controlled relaxation) | Paper 8 (revealed sacrifice) |
|-|---------------------------------|------------------------------|
| Question | Is the restriction still warranted? | Is the capability actually valuable? |
| Evidence source | Framework-initiated exercise | Agent-initiated sacrifice |
| Channel direction | Framework injects observation | Framework receives disclosure |
| Scope | Bounded $\scope \subset P$, bounded $\testdur$ | Bounded to the trade event itself |
| Privacy cost | Scope-limited exercise under monitoring | None beyond what the trade creates |
| Adversarial model | Agent must tolerate the test | Agent must operate (buy, work) |
| Dimension coverage | Risk dimension (restriction lattice) | Value dimension (experiential $\mathrm{vol}_R$) |

Together they cover both axes of the preemptive-restriction criterion from
Paper 3 Proposition 1: restriction cost (Paper 7 tests the risk side) and
experiential value (Paper 8 bounds the value side). Paper 7 tells us whether a
feared harm is real; Paper 8 tells us whether the forgone capability is worth
recovering. Without both, the restriction decision is undetermined.

## What to keep from the existing outline

The old outline's machinery remains useful as supplementary material even
under the new framing:

1. **Exercise indicator $e_t(d)$** (old §2): no longer the primary observation
   mechanism, but can be retained as a *secondary* indicator the framework
   computes when it has the observation access (e.g., internal cooperative
   outputs within the collective's own operational perimeter, where no
   privacy issue arises). State explicitly that the exercise indicator is
   applicable only where interior access is legitimate.

2. **Gap decomposition** (old §8, Definition 10): still the right framing for
   the alarm mechanism. Under the new framing:
   - `delta_dormant`: capabilities the framework can identify as possessed
     but not appearing in aggregate sacrifice data.
   - `delta_restricted`: capabilities under active restriction (Paper 7
     addresses these).
   - `delta_residual`: capabilities outside the reach of sacrifice observation
     AND outside the reach of interior exercise measurement.

3. **Wireheading detection** (old §8, Proposition 8–9): exercise leverage
   concentration is still the right diagnostic, but the underlying
   $\lambda_{\mathrm{ex}}$ is computed from trade-flow concentration (HHI on
   trade volume by bundle category), not from structural counterfactuals. The
   formal property carries over: concentrated sacrifice on a narrow bundle
   class is the observable signature of wireheading, regardless of what
   structural mechanism drives it.

4. **Worked example** (old §9): the automation-induces-dormancy scenario still
   illustrates the core phenomenon but should be re-staged. Instead of the
   framework computing $e_t(d) = 0$ for dormant biological capabilities, the
   framework observes that no revealed-sacrifice events exchange
   purchasing-power or time for biological-capability bundles — aggregate
   trade flow shifts toward silicon-only outputs, and the alarm fires on the
   absence of trade signal for biological-valued bundles.

5. **Axiom inheritance and M6 failure** (old §4): $\mathrm{vol}_R$ as the
   lower-bounded quantity inherits even fewer axioms than the old outline
   allowed, because the lower bound itself is not a measure (it's a bound on
   a measure). This should be stated clearly: $\mathrm{vol}_R$ remains a
   diagnostic quantity, not an objective, and the lower-bound construction
   doesn't change that. The non-self-balancing finding still applies and
   remains the structural reason to use $\mathrm{vol}_R$ as audit rather than
   objective.

## Residual class re-characterization

The old residual class was capabilities that fail benchmarkability (identity-
individuated + non-repeatable + non-communicable). The new framing has a
differently-shaped residual class:

**New residual class:** capabilities realized purely privately, with no trade
or sacrifice event that exposes them to the aggregate observation channel.

Relationship to old residual class:
- Identity-individuated capabilities often *are* in the new residual (purely
  private experiences don't trade), but some trade indirectly (e.g., an
  artistic practice that is identity-individuated still involves purchasing
  supplies, paying for studio space, foregoing labor hours). The intersection
  is non-trivial.
- Some capabilities that are benchmarkable in the old sense are in the new
  residual (e.g., purely internal cognitive capabilities that produce no
  external commitment event — thinking-about-something).
- Some capabilities that were in the old residual are NOT in the new residual
  (e.g., relational capabilities that are identity-individuated but still
  involve observable time-sacrifice).

The re-characterization is cleaner operationally: "what doesn't the framework
observe?" has a single answer (things the agent doesn't trade or sacrifice
for) rather than four different failure-of-benchmarkability conditions. Paper
8 should argue this is the *correct* carve — the old carve was an artifact of
trying to measure $\mathrm{vol}_R$ directly.

## What changes in the structure

Candidate new section ordering for Paper 8:

1. Introduction and the privacy problem with direct measurement
2. Revealed-sacrifice observation model (Definition, observation channels)
3. Aggregate lower bound theorem (the central result)
4. Two sacrifice channels: money and time
5. Commitment-layer composition with `lasser2026exo`
6. Residual class under revealed-sacrifice observation
7. Alarm mechanism and gap decomposition (retained from old §8, reframed)
8. Wireheading detection via trade-flow concentration (retained from old §8,
   reframed)
9. Worked example: the dormant-capability scenario re-staged
10. Integration: duality with Paper 7, the shared privacy discipline,
    connection to Paper 6's phase boundary
11. Discussion and open questions

Notable removals from the old outline:
- Old §2 (exercise indicator as primary object) → demoted to supplementary
- Old §4 (axiom inheritance proof) → compressed and absorbed into §3 (with
  the non-self-balancing finding retained)
- Old §5 (benchmark refinement dynamics) → retained as a supplementary
  mechanism for internal-perimeter exercise, not as the primary convergence
  driver; the primary convergence driver is trade-flow accumulation.
- Old §6 (convergence of β) → re-proved under the trade-flow observation
  model with different assumptions (trade frequency, coverage of
  $\mathcal{U}$, commitment integrity from `lasser2026exo`)

## Open questions specific to the new framing

1. **Hedonic disaggregation of bundles.** The aggregate lower bound requires
   weights $w_n$ to disaggregate trade bundles into per-capability
   contributions. Classical hedonic regression handles this for priced goods;
   the time-sacrifice channel needs an analogous framework. Is this a
   solved problem in the labor-economics literature, or does it require new
   machinery for the framework's purposes?

2. **Non-stationarity of revealed preferences.** Preferences shift over time
   (an agent may value a capability highly at 30, less at 60). The lower
   bound from past trades may overstate $\mathrm{vol}_R$ at present. How
   should the framework discount old sacrifice evidence? EWMA with a
   decay constant matching preference-shift timescales seems natural but
   requires empirical calibration.

3. **Coerced sacrifice.** Free choice is load-bearing for the revealed-
   preference inequality. Under duress (economic coercion, political pressure,
   information asymmetry at sale), the agent's trade doesn't reveal their
   preferences. How does the framework filter coerced sacrifice events? One
   candidate: require that the agent has alternatives (the trade is between
   options the agent ranked), which can be verified by observing that other
   agents in similar circumstances chose differently.

4. **Market-failure cases.** In contexts without functioning markets
   (pre-capitalist societies, closed economies, intra-family sharing), the
   revealed-sacrifice channel is quiet even though $\mathrm{vol}_R$ activity
   is real. Does the framework need a non-market revealed-sacrifice variant,
   or does the residual class just grow in market-failure contexts?

5. **Commitment at scale.** The paper's privacy guarantee depends on
   commitment-based disclosure. A fully-committed trade ledger at the scale of
   a modern economy is an infrastructure problem. The paper should be
   realistic about the commitment-layer cost and state clearly that the
   privacy guarantee is conditional on the commitment infrastructure existing
   (which is Paper 5's remit).

## Relationship to subsequent papers

If Paper 9 covers adversarial structure learning (Proposal 5 from the gap
analysis), the revealed-sacrifice channel gives it a clean empirical signal:
trade patterns reveal agent preferences under intervention (the SCM can
intervene on prices or availability and observe sacrifice responses). The
"designed-experiment observations" that Paper 9 would need correspond to
market experiments (flash sales, sudden availability changes) that generate
adversarially-robust trade signals.

---

*End of reframing memo. The canonical Paper 8 outline should be rewritten
from this reframing; the existing `paper8_outline.md` is superseded for the
central thesis but retained as a source of supplementary machinery.*
