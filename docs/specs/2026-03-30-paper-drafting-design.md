# Paper Drafting Design: Goal-Frontier Maximizers are Civilization Aligned

**Date:** 2026-03-30
**Author:** Teague Lasser
**Status:** Approved design

---

## Overview

Full drafting plan for the paper specified in `docs/specs/PAPER_SPEC.md`. The paper argues that goal-frontier maximization (GFM) --- maximizing the volume of the jointly achievable capability space --- is a more robust alignment objective than fixed utility functions or deontological rules, because a single measure-monotonicity argument penalizes destruction, coercion, and rigidity from the same objective function.

## Decisions

### Drafting Process

- **I draft everything, you revise.** All sections drafted to near-final quality from the spec and source material. Author reviews PDF, marks revisions, drafter revises. Repeat per phase.
- **Depth-first, definitions-out.** Formal backbone (Definitions, Propositions, Proofs) drafted first. Prose sections (Introduction, Connections, Future Concerns) drafted after the formal claims are solid. Abstract and Conclusion drafted last, since they summarize a finished paper.

### Self-Contained Paper

The paper must be self-contained. No reader should need to consult external blog posts to follow the argument or evaluate the claims. Blog posts are source material to mine, not references to cite.

### Blog Material Disposition

| Source | Disposition |
|--------|------------|
| `free.md` | Mined for Definitions and Propositions. CHIEFS dropped (aspirational, not provable). Adversary dynamics folded into Section 5. No blog citation. |
| `scorpions.md` | Full taxonomy with formal game-theoretic notation goes into Appendix B as specific examples of behavior GFM defends against. Self-contained. |
| `frameskipping.md` | Evaluate during drafting: if "frame-skipping" as a coined term meaningfully extends the argument beyond established language (Goodhart's Law, proxy gaming, reward hacking), define it properly in the paper. If it is just rebranding, use established terminology. Proxy-values argument and combinatorial explosion go into Sections 4 and 7 in the paper's own language. |
| `limitsofthought.md` | Computational bounds arguments extracted into Section 4 (Tractability) or a supporting appendix, depending on space needs. |

### Predraft Reference

Dropped entirely. The predraft was a summary of a body of work; only the final section is relevant, and that material is being wholly rewritten here. Predraft equations (5, 6-12, 22-25) are reference scaffolding for concepts and intent --- the notation and functional forms are rebuilt from this paper's definitions.

## Drafting Order

### Phase 1: Definitions (Section 2)

**Goal:** Establish the minimal formal vocabulary the entire paper depends on.

**Content:** Definitions 0-6.
- Definition 0 (Goal): Adopt Candidate B (capabilities) as formal target. Frame Candidate C (experiences) as the motivating justification. Make the B-as-proxy-for-C relationship explicit. This is the paper's core philosophical move.
- Definition 1 (Capability Space, Agent, Individual Capability Set): Already scaffolded in LaTeX.
- Definition 2 (Joint Goal Space): G = union of individual sets plus cooperative capabilities. Canonical measure is vol(G).
- Definition 3 (Goal-Frontier Maximizer): The optimization objective.
- Definition 4 (Contraction and Expansion): Direct and indirect contraction.
- Definition 5 (Social Objective): Additivity under independence, tradeoff acknowledgment. Critical assumptions stated explicitly.
- Definition 6 (Observable Goal Model): Trust factor T_k and confidence C_k.

**Key decision for drafting:** The capability space G needs structure beyond a set (at minimum a sigma-algebra with a measure). The paper should state this requirement and identify it as an open problem (Section 7) rather than resolving it.

**Drafting guardrails:**
- Keep definitions lean. Do NOT define sensors, actuators, self-models, environment models, attention models, or belief models here --- those belong in a separate architecture paper or appendix.
- Use standard mathematical notation. The predraft mixed too many custom notations.
- The key distinction from standard utility maximization: G is a *space* (with volume), not a scalar. This is what gives GFM its geometric character. Make this explicit.

### Phase 2: Self-Balancing Property (Section 3) + Appendix A (Evil Twin)

**Goal:** State and prove/sketch the central contribution.

**Content:**
- Proposition 1 (a)-(d): Destructive, coercive, and rigid actions are anti-maximizing; structural balance follows. Consider whether (a)-(c) should be lemmas with (d) as the synthesizing proposition.
- Corollary 1.1: Elimination is almost always anti-maximizing. Cooperative loss grows super-linearly.
- Corollary 1.2: Rigid rules are anti-maximizing. Connect to Evil Twin (Appendix A).
- Proposition 2: Scorpion detection under observable contraction, with explicit scope limitation (inherits observability constraints from Proposition 3; social/structural scorpions may evade detection).
- Appendix A: Full Evil Twin Time Bomb worked example. Deontological agent fails; GFM agent succeeds by evaluating vol(G) impact of each option.

**Open problems to acknowledge inline:**
- (d) is structural, not an equilibrium existence proof.
- Detection bounded by Proposition 3 observability.
- No convergence rate claims.

### Phase 3: Tractability (Section 4)

**Goal:** Confront computational hardness head-on and provide a workable approximation.

**Content:**
- Intractability result: Two arguments with different epistemic status. Formal (#P-hard, Dyer & Frieze 1988, applied result). Motivating (combinatorial interaction effects, original, informal).
- Definition 7 (Local Volume Estimator): Finite-difference on vol(G). Requires measurability, not differentiability.
- Observability channels: Individual capability signals (good coverage) vs. coalition capability signals (noisier, slower). Critical assumption: estimator is better for individual capabilities than cooperative ones.
- Proposition 3: Sign-correctness under three assumptions. Proof sketch from measure monotonicity + sign-preservation bound.
- Remark on estimator failure modes: Four cases from full observation to pure coalition blindness.
- The feedback loop: Re-derive from vol(G) objective using Definitions 1-6. The predraft loop structure (Gamma, Psi, Phi, w_G updates from Equation 5) is directionally correct but must be rebuilt. The accept/reject signal R_k from agents is the measurement channel for the local volume estimator. The activation energy concept (world model only updates when evidence exceeds threshold theta) is a *key design parameter* for adversarial robustness --- treat it as a first-class concern, not a trust model footnote.
- Trust model interface defined here (details in Appendix C).
- Computational cost: Scales with observed agents, not total population. Each decision requires proposing an action, estimating effect on observed agents' goals, aggregating feedback, updating frontier estimate. Comparable to contextual multi-armed bandit.

**Source material to mine:** `frameskipping.md` combinatorial explosion argument, `limitsofthought.md` computational bounds. Rewrite in the paper's own language.

### Phase 4: Multi-Agent Dynamics (Section 5) + Appendix C (Trust Model)

**Goal:** Show what happens when GFM actors interact with each other and with adversaries.

**Content:**
- GFM-GFM cooperation: Shared objective, coalition formation, bounded goal drift.
- GFM-Scorpion interaction: Detection, containment, proportional response. Source material from `scorpions.md` and `free.md` adversary dynamics.
- Trust model interface in main body. Full re-derivation in Appendix C starting from Definitions 1-7. Preserve concepts (T_k, tau, theta, T_s, gradient tracking). Reconsider specific functional forms.
- Defection conditions: Containment, not destruction.

### Phase 5: Standalone Appendices (B, D)

**Appendix B (Scorpion Taxonomy):** Five types with formal game-theoretic notation, each mapped to a known alignment failure mode. Written to be self-contained --- the reader gets the full argument without needing the blog post.

**Appendix D (Agent Similarity and Goal Estimation):** Goal similarity S_G, agent similarity S_A, ZK re-identification, modal groupings. Adapted from predraft Sections XI-XII with notation rebuilt from this paper's definitions.

### Phase 6: Connections (Section 6)

**Goal:** Position GFM relative to four existing frameworks.

**Content:** Empowerment maximization (formal bridge), Sen's capability approach (philosophical bridge), Free Energy Principle (structural bridge), Constitutional AI/RLHF (practical bridge). Each gets a subsection identifying the parallel, the key difference, and what GFM adds.

### Phase 7: Future Concerns and Open Problems (Section 7)

**Goal:** Demonstrate the B/C framework's predictive power and state what remains unsolved.

**Content:**
- Doll Problem: B/C divergence. Capability set looks neutral but experiential optionality contracts. Framework predicts the failure; formal machinery alone would miss it.
- Self-Wireheading: Stable capability volume + declining exercisability = proxy being Goodharted.
- Proxy-failure detector sketch: Exercised fraction heuristic --- ratio of capabilities agents actually use to capabilities formally available. A persistent decline with stable vol(G) is a B-to-C divergence signal. This is a *heuristic, not a solution*. It introduces its own proxy problem (specialization is not contraction). The paper must NOT claim this solves the problem --- it claims the B/C framework makes the problem *detectable in principle*.
- Human proxy-trap susceptibility (from `frameskipping.md`, using established language unless the coined term adds value).
- Open problems: B-to-C gap, structure of G, measurement, convergence, plurality, bootstrap.

### Phase 8: Introduction (Section 1)

**Goal:** Motivate the problem and roadmap the paper. Written last so it accurately previews what the paper actually delivers.

**Content:** Frame alignment as objective choice, not rule choice. Three failure modes (fixed utility, deontological, unconstrained consequentialism). GFM as third option. Central claim. Roadmap.

**Exclusion list (from spec --- guardrails against scope creep):**
- Do NOT include ML basics (predraft Section II)
- Do NOT include "ML models cannot adapt" argument (predraft Section III)
- Do NOT include sigmoid vs. exponential discussion (predraft Figure 1)
- Do NOT re-argue the extended Clippy/frame-skipping argument --- the material is either in the paper's own sections or dropped

### Phase 9: Conclusion + Abstract

**Goal:** Summarize the finished paper.

**Content:** Conclusion restates result, estimator, what makes GFM different, B/C predictive power, forward-looking claim. Abstract is ~150 words covering definition, self-balancing, tractability, robustness claim, B/C distinction.

## Appendix Structure

| Appendix | Content | Role |
|----------|---------|------|
| A | Evil Twin Time Bomb | Worked comparative example against rule-based approaches |
| B | Scorpion Taxonomy | Five adversary types grounding detection/containment claims |
| C | Trust Model Derivation | Full re-derivation from Defs 1-7 for Section 5's interface |
| D | Agent Similarity and Goal Estimation | Technical details for estimator and goal modeling |

## Style Rules

From the spec:
- Conditional framing ("a GFM actor that...") not "will" language
- Limitations inline, not in a separate section
- Every equation referenced in prose, variables defined at point of introduction
- Every paragraph carries at least one new idea
- Acknowledge intractability, then solve it
- Honest about proof strength: propositions with explicit assumptions over theorems that overreach
- Lead with what the framework accomplishes; scope limitations proportionally

## Bibliography

Academic references retained: Bostrom (2014), Hubinger et al. (2019), Carlsmith (2022), Christiano et al. (2017), Bai et al. (2022), Klyubin et al. (2005), Sen (1999), Nussbaum (2000), Robeyns (2005), Friston (2013), Dyer & Frieze (1988), Axelrod (1984), FAIR/Diplomacy (2022).

Blog post and predraft references removed from bibliography. Material is in the paper itself.

## Review Cycle

Per phase:
1. Draft section(s) in LaTeX
2. Compile to PDF
3. Author reads and marks revisions
4. Revise
5. Next phase

## LaTeX Structure

```
docs/paper/
  main.tex                    # Master document
  neurips_2023.sty            # NeurIPS preprint style
  references.bib              # Academic references only
  sections/
    abstract.tex              # Phase 9
    introduction.tex          # Phase 8
    definitions.tex           # Phase 1
    self_balancing.tex        # Phase 2
    tractability.tex          # Phase 3
    multi_agent.tex           # Phase 4
    connections.tex           # Phase 6
    future_concerns.tex       # Phase 7
    conclusion.tex            # Phase 9
  appendices/
    evil_twin.tex             # Phase 2
    scorpion_taxonomy.tex     # Phase 5
    trust_model.tex           # Phase 4
    agent_similarity.tex      # Phase 5
```

## Critical Success Criteria (from spec --- review checklist for finished paper)

The paper succeeds if a reader can answer "yes" to all of:

1. Can I state the central claim in one sentence?
2. Do I understand why this is non-obvious?
3. Do I believe the proposition, given its stated conditions?
4. Do I understand how this could be implemented?
5. Do I know what remains unsolved?
6. Do I know what the paper does NOT claim?
7. Do I understand the paper's relationship to its own proxy?
