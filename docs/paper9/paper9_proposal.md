# Paper 9 Proposal: GFM as a Microfoundation for Capability Economics

*Proposal-level document. Full outline to follow after Paper 8 rewrite (per
the reframing memo at `docs/paper8/paper8_reframing_revealed_sacrifice.md`)
and Paper 7 codex review clear. Scheduled for the Paper 9 slot; displaces the
earlier Proposal 5 (adversarial structure learning) to a later slot.*

## Working title

**Goal-Frontier Maximization as a Microfoundation for Capability Economics**

Alternatives under consideration:
- *Capability-Theoretic Microfoundations: A Formal Framework*
- *From Utility to Capabilities: GFM as an Economic Microfoundation*

## Thesis

Goal-Frontier Maximization provides a formal microfoundation for the Sen–
Nussbaum capability approach to welfare economics. Standard microeconomic
utility theory is underspecified: it accepts any revealed preference ordering
as the utility function and imposes no structure on what counts as a good,
making it unfalsifiable in practice. GFM imposes structural commitments
(poset, axioms M1–M6, cooperative capabilities, leverage) that generate
testable predictions utility theory cannot.

Standard economics emerges as a special case of GFM under a *fungibility
collapse* — when the capability poset reduces to a single-dimension money
axis, cooperative capabilities vanish, and individuation becomes irrelevant.
At the macro scale with liquid markets, this approximation is adequate and
standard economics predicts well. At the micro scale where non-fungibility
and cooperative structure dominate, GFM diverges from utility theory in ways
that match observed behavior (the voluntary purchase of depreciating assets,
time-for-relationship trades, bundle-completion purchasing patterns) without
needing ad hoc utility-function shapes to rationalize them.

## Why this paper sits where it does in the sequence

Papers 1–6 establish the formal apparatus: poset structure, $\mathrm{vol}_P$,
axioms, anti-monopolar property, phase boundary, cooperative capabilities,
leverage. Paper 7 closes the max-aggregation pathology (controlled
relaxation). Paper 8 (under the reframing memo's revealed-sacrifice thesis)
closes the B-to-C gap with a privacy-minimal observation channel that
bounds $\mathrm{vol}_R$ from below using voluntary trades.

Paper 9 makes explicit what Paper 8's observation channel already implies:
the framework's empirical entry point is economic data. Every revealed-
sacrifice event is an economic event. The paper argues that this is not
coincidental — GFM is, among other things, a formal theory of rational
economic behavior, and the revealed-sacrifice channel is how that content
becomes testable.

## Dependencies on prior papers

| Paper | Result used | Role in Paper 9 |
|-------|-------------|-----------------|
| P1 | vol_P as operational target, B-to-C framing | Scope precondition |
| P2 | Poset axioms M1–M6, vol_P self-balancing, leverage, cooperative capabilities | The structural apparatus GFM imposes that utility theory doesn't |
| P3 | Anti-monopolar property (Prop 6), γ* threshold | Structural prediction utility theory has no analog for |
| P4 | Multi-channel attribution, risk-trust aggregation | Distributional robustness of the observation apparatus |
| P5 | Cryptographic commitment, verification asymmetry | Privacy-preserving empirical apparatus |
| P6 | Cross-substrate channel redundancy, phase boundary | Resolution-through-frequency discipline carries into economic observation |
| P7 | Controlled relaxation, dual to revealed sacrifice | Risk-side complement of the value-side channel used here |
| P8 | Revealed-sacrifice channel, aggregate B-to-C lower bound | The empirical bridge — this paper's testability apparatus |

## Section structure (candidate)

1. **Introduction.** The positive content of GFM beyond AI alignment. Why
   standard utility theory is underspecified. The Sen–Nussbaum capability
   approach and what's missing from it (formal machinery). GFM as the
   bridge.

2. **Utility theory as a special case of GFM.** The fungibility-collapse
   theorem: on $\mathcal{P}_{\mathrm{std}}$ (single-dimension fungible poset,
   no cooperative capabilities), vol_P-maximization is observationally
   equivalent to money-maximizing expected-utility maximization. Standard
   microeconomics is the macro-limit of GFM.

3. **Where GFM diverges.** The four structural features utility theory
   lacks: native non-fungibility, native cooperative capabilities, native
   anti-monopolar reasoning, individuation without interpersonal
   comparison. For each, the specific class of decisions where GFM
   predicts differently from utility theory.

4. **The capability-economics lineage.** Positioning against Sen 1985,
   Nussbaum 2000, Becker 1965/1981, Stiglitz–Sen–Fitoussi 2009. What GFM
   contributes that these traditions asked for but didn't formalize;
   what GFM doesn't contribute (normative content — which capabilities
   should count as central).

5. **The empirical bridge.** The revealed-sacrifice channel from
   [Lasser, 2026h] as the empirical entry point. Four classes of
   testable predictions: bundle-completion, saturation-transition,
   cooperative premium, anti-monopolar at population scale.

6. **Worked examples.** (a) The canonical boat purchase —
   depreciating-asset acquisition explained via cooperative-capability
   bundle completion. (b) Time-for-relationship trades — unpriced
   activity revealed via wage-rate sacrifice. (c) A bundle-completion
   empirical test using existing consumer-expenditure survey data. (d) A
   counter-example where GFM and utility theory agree and why.

7. **Residual class under economic observation.** Capabilities realized
   purely privately with no trade or sacrifice event — the same residual
   as Paper 8 but viewed from the economic side. Honest statement of
   what the framework does not reach.

8. **Discussion and open questions.** Non-stationarity of preferences and
   its economic analog (life-cycle consumption theory). Coerced sacrifice
   filtering and its analog (discrimination in labor markets). Market-
   failure cases and the framework's honest silence there. The
   unfalsifiability critique of utility theory re-examined in GFM light.

9. **What this paper does not do.** Not replacing economics (macro
   reduction holds). Not providing a normative capability list. Not
   solving the subjectivity problem. Not unifying alignment with welfare
   economics.

## What needs to exist before drafting this paper

1. Paper 7 shipped and clean (in progress; draft complete at 679980e,
   codex review pending).

2. Paper 8 rewritten against the revealed-sacrifice reframing memo
   (deferred in the TODO queue; will be done after Paper 7 clears).

3. Literature review: Sen's *Commodities and Capabilities* (1985),
   Nussbaum's *Women and Human Development* (2000), Becker's *Theory of
   the Allocation of Time* (1965) and *A Treatise on the Family* (1981),
   Stiglitz–Sen–Fitoussi report (2009), Acemoglu-Robinson on capabilities
   and development. The paper will cite these as the lineage; initial
   drafting can proceed with citations-as-placeholder, but the final
   draft needs the literature read so the positioning is not parochial.

4. A decision about whether to include formal proofs or present the
   correspondence theorem informally. Paper 6's and Paper 7's proofs are
   dynamical-systems heavy; this paper's main theorem (the fungibility-
   collapse reduction) is more of a definitional theorem than a deep
   mathematical result. The paper may be more of a positioning paper
   than a theorem-driven paper, which is fine given where it sits in the
   sequence.

## Scope and tone

This is a positioning paper, not a safety-gap closure paper. Its job is
to situate GFM's positive content within an existing intellectual
lineage and identify testable predictions. It should be written in a
tone that economists will read — less alignment-specific vocabulary,
more reference to the welfare-economics literature, and explicit
acknowledgment that the paper is making a claim that should be engaged
on its own intellectual merits outside the alignment context.

The previous papers in the sequence can remain as cited dependencies
without requiring the reader to have accepted their alignment
implications. The reduction claim in §2 works whether or not you agree
that GFM is useful for AI alignment — the claim is that GFM is a useful
formal framework for rational economic agency, and the alignment
applications are downstream consequences.

## Testable-predictions commitment

The paper commits to naming at least two empirically testable predictions
that GFM makes and utility theory does not. Candidates (subject to
refinement during drafting):

1. **Bundle-completion magnitude.** Agents purchasing a bundle $Y$ whose
   cooperative capabilities complete a previously-missing region of
   their capability poset should pay more (in revealed-sacrifice units)
   than agents purchasing the same priced bundle whose capability poset
   already contains substitutes. Testable via longitudinal panel data
   on consumer expenditure conditional on prior household composition
   and asset holdings.

2. **Cooperative-premium dispersion.** Across agents with similar
   priced-endowment levels, variance in revealed-sacrifice for bundles
   with strong cooperative-capability structure should be larger than
   variance for bundles without (because cooperative structure's value
   depends on poset-specific context, unlike priced-component value
   which is interpersonally comparable). Testable via cross-sectional
   surveys on bundle valuation.

3. **Anti-monopolar at population scale.** Populations with higher
   capability diversity (measured via revealed-sacrifice dispersion
   across categories) should exhibit higher long-run welfare correlates
   than populations with equivalent total capability magnitude but
   lower diversity. Testable via cross-national comparison with
   existing welfare indices. This is the γ* threshold observed
   empirically.

## Notable risks

1. **Over-reach.** The "GFM is a theory of economic behavior" claim is
   large. The paper should be careful to state it as "GFM provides a
   microfoundation for capability economics" — a specific, defensible
   positioning — rather than "GFM replaces neoclassical economics,"
   which is both overstated and would invite dismissal.

2. **Under-engagement with the literature.** Positioning papers that
   don't read the lineage they're positioning against get correctly
   dismissed. The Sen–Nussbaum reading is non-negotiable; the Becker
   and Stiglitz–Sen–Fitoussi readings are strongly advised.

3. **Testability claims that don't hold up.** Any empirical prediction
   the paper commits to should be one that GFM actually makes and that
   utility theory actually doesn't make (not one that utility theory
   can be twisted to make post-hoc). The proposal's candidate list is
   tentative and should be tightened during drafting.

4. **Audience split.** The paper is written partly for economists (who
   need the capability-approach lineage) and partly for alignment
   readers (who come from the prior papers in the sequence). Some
   duplication of background is unavoidable; the paper should be
   upfront about its dual audience.

## Status

- Proposal-level only.
- No draft.
- No outline beyond the section-structure sketch above.
- Literature review not yet started.
- Paper 9 slot in the sequence claimed; Proposal 5 (adversarial
  structure learning) bumped to Paper 10+.

---

*Authored 2026-04-14 after research discussion of GFM's relationship to
standard economic theory. Source memo: `docs/gfm_paper_proposals.md`
Proposal 6.*
