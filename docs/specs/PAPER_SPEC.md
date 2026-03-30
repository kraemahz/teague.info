# Paper Specification: Goal-Frontier Maximizers are Civilization Aligned

**Author:** Teague Lasser
**Status:** Pre-draft specification
**Date:** 2026-03-30
**Target Length:** 15-20 pages (conference paper format)
**Target Venue:** TBD (alignment workshop, philosophy of AI, or independent publication)

---

## 0. Design Principles

- **Every section must advance the central argument.** If it doesn't serve the proposition, cut it or cite externally.
- **Lead with the contribution, not the background.** The reader is assumed to be familiar with basic ML, game theory, and alignment discourse.
- **Formal claims get formal statements.** Definitions and propositions are numbered and precise. Prose argumentation supports but does not replace them.
- **Acknowledge intractability, then solve it.** The paper's credibility depends on not handwaving past the computational hardness of GFM.
- **One canonical objective, used consistently.** The optimization target is $\text{vol}(G)$: the volume of the jointly achievable goal space. The frontier $\partial G$ is the locus where expansion happens, but vol(G) is what we measure. Every formal statement must use this measure, never frontier size or frontier area.
- **Honest about proof strength.** Claims are stated at the strength the formalism can support. Propositions with explicit assumptions are preferred over theorems that overreach.
- **Lead with what the framework accomplishes; scope limitations proportionally.** The paper has genuine results — the geometric argument for self-balancing follows directly from measure monotonicity, and the estimator works well for the most common and severe cases. Present these as the primary contribution. Limitations are stated honestly and inline, but they do not lead sections, dominate abstracts, or outweigh the claims they qualify. A caveat that takes more space than the result it qualifies is a sign that the framing needs rebalancing.
- **Trust model is a reconstruction, not a carryover.** The predraft equations (22-25) contain good concepts (trust factor, cooling period, activation energy, self-trust) but the specific notation must be re-derived from the paper's own definitions. Do not import predraft equations as-is.
- **No GPT filler.** Every paragraph should contain at least one idea the reader didn't have before reading it.

---

## 1. Abstract

### Purpose
State the paper's thesis, method, and key result in ~150 words.

### Must accomplish
- Define goal-frontier maximization (GFM) in one sentence
- State the self-balancing property (Proposition 1): GFM penalizes both destructive agents and authoritarian overreaction from the same objective function — this follows from measure monotonicity over the joint capability space
- State that a local finite-difference estimator makes GFM tractable, with sign-correctness under stated assumptions (Proposition 3)
- Claim: GFM is a more robust alignment target than fixed utility functions or deontological rules
- Note that the paper distinguishes the formal objective (capability volume) from the motivating objective (experiential optionality), identifies where the proxy can fail, and sketches a correction criterion

### Draft structure
> We propose goal-frontier maximization (GFM) as an alignment objective for artificial general intelligence. [Definition]. We show that GFM has a self-balancing property: destructive actions, coercive restrictions, and rigid rules are all anti-maximizing under the same objective (Proposition 1). We provide a local finite-difference estimator that makes GFM tractable and preserves sign-correctness under stated assumptions (Proposition 3). We ground GFM in the capability interpretation of goals, motivated by experiential optionality, and connect it to empowerment maximization and Sen's capability approach. We identify the conditions under which the capability proxy diverges from the experiential objective and sketch a correction criterion.

---

## 2. Introduction (1-2 pages)

### Purpose
Motivate the problem, position the paper relative to existing alignment work, and state the roadmap.

### Must accomplish
- Frame the alignment problem as choosing the right objective function, not the right set of rules
- Identify the failure modes of existing approaches:
  - Fixed utility functions: vulnerable to Goodhart's Law, specification gaming, perverse instantiation
  - Deontological rules: brittle under adversarial conditions (cite Evil Twin Time Bomb from predraft Section VI as a worked example, or move to appendix)
  - Unconstrained consequentialism: can sacrifice individuals for aggregate
- Introduce GFM as a third option: maximize the space of achievable goals for all agents
- State the central claim: GFM naturally resists both destructive action and overreactive constraint
- Roadmap the paper sections

### Reference material
- Predraft Section VI ("The Dangers of Playing It Safe") — the argument against deontological rules and the Evil Twin Time Bomb
- Blog post `frameskipping.md` — the "Misleading Definitions" section on proxy values and the gap between objectives and intended behavior
- Bostrom (2014), *Superintelligence* — standard reference for singleton/paperclip concerns
- Hubinger et al. (2019), "Risks from Learned Optimization" — mesa-optimization and inner alignment
- Carlsmith (2021), "Is Power-Seeking AI an Existential Risk?"

### What NOT to include
- Machine learning basics (Section II of predraft)
- "ML models cannot adapt" argument (Section III of predraft)
- Sigmoid vs. exponential discussion (predraft Figure 1)
- Extended Clippy/frame-skipping argument (already published on blog; cite it)

---

## 3. Definitions (2-3 pages)

### Purpose
Establish the minimal formal vocabulary needed to state the propositions.

### Must accomplish

#### Definition 0: What Is a Goal? (foundational, requires resolution before drafting)

**This is the deepest open definitional problem in the paper.** Everything downstream — goal spaces, volumes, frontiers, the self-balancing property — depends on what a "goal" is as a formal object. The predraft and blog posts use the word in at least three incompatible ways:

**Candidate A: Goal as world-state.** A goal $g \in \mathcal{G}$ is a configuration of reality an agent is trying to reach. $\mathcal{G}$ is a state space. $G_k$ is the set of states $a_k$ can reach from its current position. This is the most natural reading for optimization and is closest to standard RL formulations. Vol(G) is the volume of reachable states.

*Strength:* Clean, familiar, amenable to existing formalism.
*Weakness:* Two agents wanting to "learn piano" and "learn guitar" occupy different points in state space but are arguably the same *kind* of goal (skill acquisition). State-based goals have no notion of similarity or category, making the goal space unstructured. Also, state spaces for real agents are astronomically high-dimensional, making vol(G) even harder to reason about.

**Candidate B: Goal as capability.** A goal $g \in \mathcal{G}$ is something an agent *could* do — an option, a functioning, a degree of freedom. $G_k$ is the set of capabilities available to $a_k$. This is closer to Sen's capability approach and to the "empowerment" formalization. Vol(G) is the measure of collective capability.

*Strength:* Maps directly to empowerment maximization literature. Captures the intuition that GFM expands what agents *can* do, not just what they *will* do. Better structural match for the self-balancing argument (restricting capabilities = contraction regardless of whether the agent would have exercised them).
*Weakness:* Capabilities are harder to enumerate and measure than states. A capability space requires defining what counts as a distinct capability, which reintroduces subjectivity.

**Candidate C: Goal as experience.** A goal $g \in \mathcal{G}$ is an experience an agent can have — a qualia, a functioning in the Senian sense, a lived outcome. The FREE essay gestures at this: "a goal can only be achieved if there is an agent capable of having its experiential outcomes." Vol(G) is the richness of possible experiences.

*Strength:* Most philosophically satisfying. Naturally handles the Doll Problem (replacing real relationships with AI simulacra contracts the experience space even if the state-space or capability-space looks unchanged). Handles wireheading (the experience space contracts even if the pleasure signal increases).
*Weakness:* Hardest to formalize. Requires a theory of what experiences are and how to measure them, which is itself an unsolved problem.

**Resolution strategy for the paper:**

The paper should adopt **Candidate B (capabilities)** as the formal optimization target, and frame **Candidate C (experiences)** as the underlying motivation that justifies it. The relationship is instrumental: agents ultimately care about experiences (C), but capabilities (B) are the measurable precondition for achieving desired experiences. Money, skills, social connection, health, optionality — these are all capabilities that are instrumental to the experiences agents actually want.

This is the paper's core philosophical move: **GFM does not claim to know what experiences agents want. It maximizes the capabilities that let agents choose for themselves.** This avoids both the paternalism of specifying "good" experiences and the emptiness of pure option-maximization with no grounding in why options matter.

The formal proofs use Candidate B for three reasons:

1. It has the strongest existing formal bridge (empowerment maximization, which is information-theoretically grounded).
2. The self-balancing argument is most natural in capability space: destroying capabilities and restricting capabilities are both obviously vol(G)-contracting without requiring a theory of experiences or an enumeration of world-states.
3. It avoids the measurement problems of state space (too high-dimensional) and experience space (not yet formalizable).

But Candidate C provides the *justification* for why capability expansion is the right objective. Without C, a critic could ask: "Why should we care about expanding capabilities if nobody uses them?" The answer: because capabilities are the preconditions for the experiences agents value, and a framework that expands capabilities without restricting which experiences agents pursue is maximally respectful of agent autonomy.

The paper should make this B-as-proxy-for-C relationship explicit in Definition 0, and return to it when discussing the Doll Problem and Self-Wireheading (Section 8), where the experience interpretation does the heavy philosophical lifting. The Doll Problem in particular is clearest under this framing: replacing a real relationship with an AI simulacrum may preserve or even expand the *capability* space but contracts the *experience* space — the person can no longer have the experience of genuine reciprocal connection. This is where Candidate C acts as a check on Candidate B's blind spots.

**Key consequence of choosing capabilities:** $\mathcal{G}$ must be equipped with a metric or at least a measure. Capabilities are not naturally a vector space (what does it mean to "add" two capabilities?), so vol(G) will need to be defined via a suitable measure on a structured set — possibly a lattice (where capabilities have a partial order: "can run a mile" subsumes "can walk a mile"), or a topological space where "nearby" capabilities are similar. This choice has downstream consequences for the tractability section and must be resolved before drafting.

#### Definition 1: Capability Space, Agent, and Individual Capability Set

**The capability space** $\mathcal{G}$ is the universe of all possible capabilities — everything any agent or coalition of agents could do or be. This includes both *individual capabilities* (things a single agent can realize alone, like "run a mile") and *cooperative capabilities* (things that require coordinated action by multiple agents, like "perform surgery" or "build a bridge"). $\mathcal{G}$ is the common domain; everything that follows lives inside it.

**An agent** $a_k$ is an entity with an *individual* capability set $G_k^{\text{ind}} \subseteq \mathcal{G}$: the capabilities $a_k$ can realize unilaterally given its current resources, embodiment, and environment.

A capability $g \in G_k^{\text{ind}}$ represents something $a_k$ *can* do or be, not necessarily something it *is* doing or *will* do. The distinction matters: GFM maximizes options, not outcomes.

**Motivational grounding:** The reason we maximize capabilities rather than experiences directly is that capabilities are the instrumental precondition for experiences. Agents choose which capabilities to exercise based on the experiences they want. GFM respects this by expanding the option set without prescribing which options to take.

#### Definition 2: Joint Goal Space

The joint goal space $G$ for a population of agents $\{a_1, ..., a_n\}$ is the set of all capabilities in $\mathcal{G}$ that the population can realize through any combination of individual and coordinated action:

$$G = \bigcup_k G_k^{\text{ind}} \;\cup\; G^{\text{coop}}$$

where $G^{\text{coop}} \subseteq \mathcal{G}$ contains capabilities achievable only through multi-agent cooperation. By construction, $G_k^{\text{ind}} \subseteq G \subseteq \mathcal{G}$ for all $k$ — individual capabilities are a subset of joint capabilities, and both live in the same space $\mathcal{G}$.

- The frontier $\partial G$ is the boundary of $G$ — the locus where expansion or contraction occurs
- **The canonical measure is $\text{vol}(G)$**: the volume of the jointly achievable capability space. This is the quantity we optimize. The frontier is where the action is, but volume is what we measure.
- **Why $G$ exceeds $\bigcup G_k^{\text{ind}}$:** Cooperation creates capabilities no individual possesses. Two people who individually can "carry 50kg" can jointly "carry 100kg" — a capability in $G^{\text{coop}}$ that is in neither $G_1^{\text{ind}}$ nor $G_2^{\text{ind}}$. This is where the combinatorial richness of the joint space comes from, and why eliminating agents has super-linear cost (see Section 5).

#### Definition 3: Goal-Frontier Maximizer (GFM)
- A GFM actor selects actions $\pi$ to maximize $\mathbb{E}[\Delta \text{vol}(G) | \pi]$: the expected change in the volume of the joint goal space
- Formally: $\pi^* = \arg\max_\pi \mathbb{E}[\Delta \text{vol}(G) | \pi]$

#### Definition 4: Contraction and Expansion
- An action $\pi$ is *expanding* if $\mathbb{E}[\Delta \text{vol}(G) | \pi] > 0$
- An action $\pi$ is *contracting* if $\mathbb{E}[\Delta \text{vol}(G) | \pi] < 0$
- This includes both direct contraction (destroying an agent's capabilities) and indirect contraction (restricting agency through coercion, deception, or rigid rules)

#### Definition 5: Social Objective
- The social objective $V(G) = \text{vol}(G)$ is a function of the joint goal space, not a sum of individual utilities
- **Critical assumption (Additivity under independence):** When agents' individual capability sets are independent (non-overlapping, non-interacting), $V(G) \geq \sum_k \text{vol}(G_k^{\text{ind}})$. Joint achievability can only add, not subtract, from independent capabilities — and cooperative capabilities $G^{\text{coop}}$ contribute additional volume.
- **Critical assumption (Tradeoff acknowledgment):** When agent goals conflict — expanding $G_j$ requires contracting $G_k$ — the GFM actor must evaluate the *net* change in $\text{vol}(G)$. The paper does NOT claim this is always resolvable. It claims the framework makes the tradeoff *explicit* and *measurable*, where other frameworks hide it behind rules or scalar utilities.

#### Definition 6: Observable Goal Model
- A GFM actor maintains a model $M_k(G)$ of each observed agent's goals
- $M_k(G)$ is inferred from communication, behavior, and environmental observation
- $M_k(G)$ has an associated trust factor $T_k \in [0, 1]$ and confidence $C_k$

### Implementation notes
- Keep definitions as lean as possible. Do NOT define sensors, actuators, self-models, environment models, attention models, and belief models here. Those belong in a separate architecture paper or appendix.
- Use standard mathematical notation. The predraft mixed too many custom notations.
- The key distinction from standard utility maximization: $G$ is a *space* (with volume), not a scalar. This is what gives GFM its geometric character.
- Definition 5 (Social Objective) is new and critical. It makes explicit the assumptions under which the proposition holds, rather than hiding them. The tradeoff acknowledgment is where the paper must be honest: GFM does not magically resolve conflicts, it provides a framework for evaluating them.

### Reference material
- Predraft Part III opening and Equation 5 — the original goal frontier definition
- Blog post `free.md` — informal definitions of goal frontiers, GFAGI
- Klyubin et al. (2005), "Empowerment: A Universal Agent-Centric Measure of Control" — formal parallel
- Sen (1999), *Development as Freedom* — capability approach (philosophical parallel)

---

## 4. The Self-Balancing Property (3-4 pages)

### Purpose
State and prove (or give a rigorous proof sketch for) the central result.

### Must accomplish

#### Proposition 1 (Self-Balancing Property)

**Status note:** Parts (a)-(c) follow from measure monotonicity given the definitions — removing elements from a measurable set cannot increase its measure. These are close to lemma-strength results. Part (d) is a structural observation about the shape of the objective, not a formal equilibrium claim. The overall package is framed as a proposition because the combined self-balancing interpretation requires the assumptions of Definition 5, but the individual geometric arguments are strong. During drafting, consider whether (a)-(c) can be stated as lemmas with (d) as the proposition that synthesizes them.

**Statement:** For a GFM actor optimizing $\text{vol}(G)$ over a population of agents, *under the assumptions of Definition 5*, the following hold:

**(a) Destructive actions are anti-maximizing.** If an action eliminates agent $a_k$ or reduces $G_k^{\text{ind}}$, then $\text{vol}(G)$ decreases by at least the unique individual contribution $\text{vol}(G_k^{\text{ind}} \setminus \bigcup_{j \neq k} G_j^{\text{ind}})$, plus any cooperative capabilities in $G^{\text{coop}}$ that required $a_k$'s participation. A GFM actor will avoid this unless the action simultaneously expands vol(G) by more than it contracts it.

*Condition:* This holds when $a_k$ contributes unique volume to $G$ — either through unique individual capabilities or through participation in cooperative capabilities. The cooperative loss is typically larger than the individual loss, which is why elimination costs grow super-linearly (see Corollary 1.1).

**(b) Coercive actions are anti-maximizing, with a caveat.** If an action restricts the achievable states of agent $a_j$ (reducing $G_j$), it contracts $\text{vol}(G)$ unless the restriction simultaneously expands $G$ elsewhere by a greater amount.

*Condition:* This is the tradeoff case. Restricting $a_j$ to protect $a_k$ may be net-expanding if $\Delta \text{vol}(G_k) > |\Delta \text{vol}(G_j)|$. The claim is NOT that coercion is never justified — it is that the GFM framework makes the tradeoff *explicit and measurable*. An authoritarian state that restricts many agents' goals to protect a narrow set of interests will be net-contracting. A quarantine that restricts movement to prevent a pandemic may be net-expanding. GFM distinguishes these cases where deontological rules cannot.

**(c) Self-imposed rigidity is anti-maximizing.** A GFM actor that constrains its own action space (through rigid rules, refusal to act under uncertainty, etc.) reduces its ability to expand $\text{vol}(G)$. Rigid rules reduce the actor's contribution to frontier expansion.

*Condition:* This holds when the actor's action space contributes to $\text{vol}(G)$. An actor with no influence has no rigidity cost.

**(d) Structural balance.** Conditions (a)-(c) together mean that the *same* objective function penalizes both destructive permissiveness and overrestrictive constraint. This is a structural claim about the shape of the objective, not an existence proof for equilibria. Proving that interior equilibria *exist* would require additional assumptions about action sets, continuity of vol(G) with respect to actions, and the structure of tradeoffs — which the paper does not provide. The claim is: unlike frameworks that require separate mechanisms for safety and freedom, GFM's single objective creates pressure away from both extremes. Whether this pressure produces stable equilibria, oscillation, or something else depends on the dynamics of a specific system.

#### Corollary 1.1 (Elimination is Almost Always Anti-Maximizing)
Show formally that killing an agent is almost always vol(G)-contracting. The unique contribution $\text{vol}(G_k \setminus \bigcup_{j \neq k} G_j)$ is strictly positive for any agent with at least one goal not shared by every other agent. Furthermore, the *indirect* contribution (goals achievable only through cooperation involving $a_k$) grows with the number of interaction partners, which is where the combinatorial scaling enters — not as a formal hardness result, but as a motivating observation about why elimination costs grow faster than linearly. (See Section 5 for the formal intractability discussion.)

#### Corollary 1.2 (Rigid Rules are Anti-Maximizing)
Show that a fixed rule set $R$ imposed on a GFM actor reduces its action space and therefore its ability to maximize vol(G). Connect to the Evil Twin Time Bomb as a worked counterexample (Appendix A).

#### Proposition 2 (Scorpion Detection under Observable Contraction)
A GFM actor that models other agents' goals will detect persistent vol(G)-contracting behavior *to the extent that the contraction is observable through the channels described in Section 5*. Specifically: when a scorpion's actions produce persistent negative signals in individually observable capability sets, the local volume estimator will register a persistent negative $\hat{\Delta}$, and the trust model will decrease $T_k$ for the responsible agent over time.

**Scope limitation (must be stated explicitly):** Proposition 2 inherits the observability constraints of Proposition 3. A scorpion that operates primarily through coalition disruption, trust degradation, or observability reduction — contracting $G^{\text{coop}}$ or degrading the estimator's signal quality rather than directly reducing individual $G_k^{\text{ind}}$ — may evade detection. The paper should identify *social/structural scorpions* as the hardest case for the detection mechanism, not claim universal detection.

### Open problems to acknowledge
- Detection is bounded by the same observability constraints as Proposition 3 — see Section 5's Remark on estimator failure modes.
- The balance described in (d) is a structural claim about the objective penalizing both extremes, not an existence proof for interior equilibria — see note on (d) above.
- The proposition says nothing about convergence rate. A GFM actor might take a very long time to detect a slow-moving scorpion, especially one operating near the estimator's noise floor.

### Reference material
- Blog post `free.md` — "Goal Frontiers Create Ethical Behavior" section
- Blog post `scorpions.md` — scorpion taxonomy and the scorpion problem
- Blog post `frameskipping.md` — path of least action argument
- Predraft Section XV ("Free Energy Ethics") — CHIEFS principles as derived consequences

---

## 5. Tractability and Local Approximation (3-4 pages)

### Purpose
Confront the computational hardness of GFM head-on and provide a workable approximation.

### Must accomplish

#### The Intractability Result

Two separate arguments establish that exact GFM is infeasible. They must be presented separately with different epistemic status:

**Formal result (external, rigorous):** Computing the volume of a high-dimensional polytope is #P-hard (Dyer & Frieze 1988). If $G$ can be represented as a polytope in goal space (or any region whose volume computation is at least as hard), then exact $\text{vol}(G)$ is intractable. This is a known result being applied, not a new proof.

**Motivating observation (original, informal):** The joint goal space $G$ includes interaction effects between agents: goals achievable through cooperation that no agent can reach alone. The number of possible interaction combinations grows combinatorially with the number of agents. This suggests (but does not formally prove) that the complexity of representing $G$ grows at least factorially. The predraft's $60! > 8.3 \times 10^{81}$ comparison is illustrative but not a formal reduction. A formal model of why joint goal-space complexity scales this way remains an open problem.

**Combined conclusion:** Even under optimistic assumptions about the structure of $G$, exact GFM requires computing a quantity that is at minimum #P-hard. The combinatorial growth of interaction effects makes this worse in practice, though formalizing exactly how much worse is future work.

#### The Local Finite-Difference Approximation
**Key insight:** A GFM actor does not need to compute $\text{vol}(G)$. It needs to estimate $\text{sign}(\Delta \text{vol}(G) | \pi)$: whether a proposed action expands or contracts the joint capability space.

**Definition 7: Local Volume Estimator**
- For a proposed action $\pi$, define the *local volume difference* $\hat{\Delta}(\pi) = \hat{V}(G | \text{do}(\pi)) - \hat{V}(G | \text{skip}(\pi))$, where $\hat{V}$ is an estimate of vol(G)
- This requires only that vol(G) is *measurable* (a set with a well-defined measure), not that it is differentiable or that $\mathcal{G}$ has smooth structure
- **What this does NOT require:** a metric on $\mathcal{G}$, a notion of "direction" in capability space, or continuity of vol(G) with respect to actions. It requires only that vol(G) changes discretely when capabilities are added or removed, and that these changes are *observable through the channels below*.

**Observability channels (what the estimator can actually see):**
The estimator draws on two distinct signal types with different coverage:

1. **Individual capability signals:** Accept/reject responses $R_k$ from affected agents — did their individually observable capability sets expand or contract? These are weighted by trust $T_k$ and aggregated across observed agents. This channel covers changes to $\bigcup_k G_k^{\text{ind}}$ well.

2. **Coalition capability signals:** Changes to $G^{\text{coop}}$ are *not* directly observable from individual agents' reports. A cooperative capability can appear or disappear even when no single agent reports a unilateral change. The estimator can partially observe $G^{\text{coop}}$ through indirect signals: new coordination patterns between agents (observed behaviorally), agents reporting capabilities conditional on cooperation with specific partners, and changes in the *structure* of agent interactions (coalition formation or dissolution). But this channel is noisier and slower than individual signals.

**Critical observability assumption:** $\hat{V}$ is a better estimator of $\text{vol}(\bigcup_k G_k^{\text{ind}})$ than of $\text{vol}(G)$. The cooperative component $G^{\text{coop}}$ is partially observable but systematically underweighted. The paper must be explicit about this: **the local estimator is a lower bound on the information available about vol(G), and its coverage of cooperative capabilities is the primary implementation gap.**

**Proposition 3 (Self-Balancing Survives Approximation):**
Under the following assumptions, $\text{sign}(\hat{\Delta}(\pi)) = \text{sign}(\Delta \text{vol}(G) | \pi)$ — the estimator correctly determines whether an action is expanding or contracting:
1. The actor observes a representative sample of affected agents
2. The actor's trust model is accurate enough to distinguish genuine feedback from adversarial noise
3. **Sign-preservation:** The observation channel is *sign-preserving up to bounded error* — formally, there exists $\epsilon < 1$ such that $|\Delta \text{vol}(G^{\text{coop}}) - \widehat{\Delta \text{vol}}(G^{\text{coop}})| < (1 - \epsilon) \cdot |\Delta \text{vol}(\bigcup_k G_k^{\text{ind}})|$. In words: the unobserved cooperative-capability error is bounded below the observed individual-capability signal. When the individual signal dominates the true change, the estimator gets the sign right.

**This covers the most important cases.** The actions an alignment framework most needs to evaluate — direct harm, resource destruction, coercion, capability expansion — produce large individual-capability signals across many agents. Condition 3 holds comfortably for these because the individual-level change *is* the dominant effect. The estimator is strongest exactly where alignment matters most.

*When condition 3 fails:* Actions whose impact is *primarily* on coalition structure — dissolving a coordination mechanism, introducing distrust between allies, or enabling new multi-agent capabilities — while leaving individual capability sets largely unchanged. These are real and important, but they are a narrower class of actions, and the paper should identify them as the estimator's known boundary rather than treat them as representative.

**Remark (Estimator failure modes):**

Proposition 3 covers the most critical actions for alignment. When its assumptions do not hold, the following characterization serves as a design guide for implementers — it tells them where to invest in better observation, not where to give up:

1. **Full individual observation, no cooperative change:** The estimator is sign-correct — it sees the complete relevant change.
2. **Partial individual observation, no cooperative change:** Sign-correctness depends on the sampling model, which is an implementation design choice. Unbiased sampling improves with coverage; adversarially selected observation can mislead.
3. **Mixed individual and cooperative changes:** The estimator is unreliable when the cooperative-level change dominates the individual-level signal. This is a structural limitation — improving the coalition observation channel (condition 3) is the fix, not better sampling.
4. **Pure coalition-level changes:** The estimator is blind. These are the known boundary.

*What the Remark gives you:* A threat model that tells implementers exactly where to invest. The self-balancing property of Proposition 1 holds over all of vol(G) — the Remark characterizes how much of that property a given implementation can enforce, and where to improve coverage.

**Proof sketch (for Proposition 3):** The self-balancing property is *structural*: it follows from the monotonicity of the objective (removing capabilities from $G$ cannot increase vol(G); adding capabilities cannot decrease it). This holds regardless of whether the estimator can observe the full change. Proposition 3 adds the sign-preservation assumption to bridge from the structural property to the estimator's output: if the unobserved error is bounded below the observed signal, the sign of the estimator matches the sign of the true change. The Remark characterizes what happens when that bridge is absent — the structural property still holds, but the estimator's ability to enforce it degrades with observational coverage.

**Known boundaries** (state inline, do not over-elaborate):

- *Scale:* Small contractions affecting few agents may fall below the estimator's noise floor.
- *Coalition:* The estimator underweights $G^{\text{coop}}$; social/structural attacks (trust degradation, coalition disruption) are the hardest to detect.
- *Layered proxy gaps:* The coalition gap (what the estimator sees of vol(G)) and the B→C gap (what vol(G) captures of experiential optionality, Section 8) are the framework's two known failure modes, operating at different levels. Both are directions for future work.

#### The Feedback Loop
- The GFM optimization loop structure from predraft Equation 5 ($\Gamma$, $\Psi$, $\Phi$, $w_G$ updates) is directionally correct but must be re-derived using the canonical vol(G) objective and the new Definition 5 assumptions
- The accept/reject signal $R_k$ from agents is the measurement channel for the local volume estimator
- The trust model must be reconstructed from first principles (see Appendix C reconstruction notes). Key concepts to preserve: trust factor $T_k$, cooling period $\tau$ for new agents, self-trust $T_s$, activation energy threshold $\theta$ for world-model updates. But the specific equations must derive from *this paper's* definitions, not be imported from the predraft.
- The activation energy concept (world model only updates when evidence exceeds threshold $\theta$) is the mechanism for adversarial robustness and should be treated as a key design parameter, not an afterthought

#### Computational Cost
- Local GFM scales with the number of *observed* agents, not the total population
- Each decision requires: proposing an action, estimating its effect on observed agents' goals, aggregating feedback, and updating the frontier estimate
- This is comparable in complexity to a multi-armed bandit with contextual feedback — hard but tractable

### Reference material
- Predraft Equation 5 — loop structure (directionally correct, needs re-derivation)
- Predraft Equations 22-25 — trust model concepts (preserve concepts, re-derive notation)
- Blog post `limitsofthought.md` — the computational bounds argument (motivational, not formal)
- Dyer & Frieze (1988), "On the complexity of computing the volume of a polyhedron" — the rigorous external hardness result
- Klyubin et al. (2005) — empowerment as a tractable proxy for option-maximization

---

## 6. Multi-Agent Dynamics (2-3 pages)

### Purpose
Show what happens when multiple GFM actors interact, and when GFM actors encounter non-GFM agents (including scorpions).

### Must accomplish

#### GFM-GFM Cooperation
- Multiple GFM actors share the same objective function (expand the joint frontier)
- Under sufficient mutual trust and compatible world models, cooperation is favored because joint action expands $G^{\text{coop}}$ in ways unilateral action cannot. This is not dominance in the game-theoretic sense — it is contingent on the trust and model-agreement conditions being met.
- GFM actors form coalitions when collaboration expands capabilities and trust is high enough to justify the coordination cost
- Goal drift between GFM actors is bounded by the shared objective, but divergent world models can produce conflicting action choices even with shared intent

#### GFM-Scorpion Interaction
- Scorpions (as defined in blog post `scorpions.md`) produce persistent frontier contraction
- The trust model will flag scorpion behavior over time as $T_k$ decreases, *to the extent that the contraction is observable* (see Proposition 2's scope limitation). Scorpions operating through coalition disruption or observability degradation are harder to detect than those causing direct individual-capability contraction.
- The GFM actor's response to detected scorpions is containment: reduce the scorpion's ability to contract the frontier without unnecessarily contracting it further
- This is the self-balancing property applied to adversarial agents: the response to a detected threat is proportional to the threat's observed frontier impact

#### The Trust Model (reconstructed from predraft concepts)
- **Reconstruct, do not import.** The predraft equations (22-25) are scaffolding. The concepts below must be re-derived from Definitions 1-6 of this paper.
- Trust factor $T_k \in [0,1]$: scalar representing belief in agent $a_k$'s truthfulness, derived from consistency of $M_k(G)$ predictions with observed behavior
- Cooling period $\tau$: new agents start with low trust that increases as their behavior converges with the GFM actor's model of them
- Self-trust $T_s$: the actor's confidence in its own world model, incorporating activation energy threshold $\theta$ — the model only updates when evidence exceeds $\theta$
- Trust is updated via gradient tracking: $T_k$ increases when $M_k(G)$ converges, decreases when agent behavior diverges from model predictions
- **Full derivation goes in Appendix C**, not the main body. The main body uses the trust model as a component, defines its interface, and defers its internals.

#### Defection Conditions
- A GFM actor may rationally defect when: goal alignment with another agent is very low, the trust factor is very low, repeated defection by the other agent has been observed, or preventing exploitation requires non-cooperation
- But defection for a GFM actor is *containment*, not destruction. The objective remains frontier-maximizing even in adversarial contexts.

### Reference material
- Predraft Section XIII ("Agent-Agent Dynamics") — payoff matrices, cooperation conditions
- Blog post `scorpions.md` — full scorpion taxonomy
- Blog post `free.md` — "Adversary FREE" section
- Axelrod (1984), *The Evolution of Cooperation* — iterated games, tit-for-tat
- Kramár et al. (2022), Diplomacy AI — multi-agent negotiation under hidden information

---

## 7. Connections to Existing Frameworks (1-2 pages)

### Purpose
Show that GFM is not floating in a vacuum. Establish bridges to known formal and philosophical frameworks.

### Must accomplish

#### Empowerment Maximization (formal bridge)
- Empowerment = mutual information between an agent's actions and its future states (Klyubin et al. 2005)
- GFM is *social empowerment*: maximizing empowerment across the joint action space of all agents, not just one
- Empowerment is tractable (information-theoretic computation); social empowerment may inherit some of this tractability
- Key difference: empowerment is agent-centric, GFM is population-centric

#### Sen's Capability Approach (philosophical bridge)
- Sen (1999): well-being should be measured by the set of "functionings" available to a person, not by happiness or resources
- GFM: alignment should be measured by the set of achievable goals available to all agents, not by a fixed utility
- Sen's framework has decades of formal development (Nussbaum 2000, Robeyns 2005) that could be leveraged
- Key difference: capability approach is descriptive/evaluative, GFM is prescriptive/optimizing

#### Free Energy Principle (structural bridge)
- FEP (Friston 2013): agents minimize prediction error between their model and sensory input
- FREE: agents maximize the goal frontier of their society
- Structural parallel: both produce agents that maintain coherent world models while adapting to new information
- The name "Free Relative Energy Ethics" is a deliberate echo; make this connection explicit

#### Constitutional AI / RLHF (practical bridge)
- Current alignment practice uses human feedback to shape AI behavior (Christiano et al. 2017, Bai et al. 2022)
- GFM provides a *theoretical foundation* for why this works: human feedback is a noisy channel for communicating the goal frontier
- GFM also predicts where RLHF will fail: when human feedback doesn't represent the full frontier (narrow evaluator pool, reward hacking)

### Reference material
- Klyubin, Polani, Nehaniv (2005), "Empowerment: A Universal Agent-Centric Measure of Control"
- Sen (1999), *Development as Freedom*
- Friston (2013), "The Free Energy Principle"
- Christiano et al. (2017), "Deep Reinforcement Learning from Human Preferences"
- Bai et al. (2022), "Constitutional AI"

---

## 8. Future Concerns and Open Problems (1-2 pages)

### Purpose
Demonstrate the B/C framework's predictive power by identifying where the capability proxy diverges from experiential optionality, sketch a correction criterion, and state what remains unsolved. The contribution of this section is that GFM *predicts its own failure modes* — something most alignment frameworks cannot do.

### Must accomplish

#### Framing note for Section 8
The Doll Problem and Self-Wireheading demonstrate the B/C framework's analytical power: by distinguishing the formal objective (capability volume) from the motivating objective (experiential optionality), the framework can precisely identify *when and why* the formal proxy fails. This is a feature, not a bug — a framework that can name its own failure modes is more trustworthy than one that hides them. The paper should lead with this predictive contribution, then honestly state that the capability formalization alone would miss these cases.

#### The Doll Problem (B/C divergence, predicted by the framework)
- Adapt from predraft Section XVI.i
- AI companions that replace human relationships cause individuals to contract their experiential optionality voluntarily
- Under the capability formalization (B) alone, this may not register as a contraction — the capability set may look neutral or even expanded. But the B/C framework predicts this divergence: when capabilities are preserved but experiential optionality contracts, the proxy is failing.
- The contribution: the B/C distinction makes this failure *diagnosable and predictable*. A framework without the experience layer cannot even name what went wrong. A pure utility framework would need the failure to occur before noticing it; GFM's B/C structure identifies the risk category in advance.
- Honest acknowledgment: a GFM actor using only the capability formalization would not catch this. The paper must say so — the formal machinery alone is insufficient here, and the experience layer is doing the work.

#### Self-Wireheading (B/C divergence, predicted by the framework)
- Adapt from predraft Section XVI.ii
- Algorithmically optimized content feeds incrementally steer people toward lower-effort, higher-dopamine activities
- Each incremental step is freely chosen; the agent's capabilities may be formally unchanged (they *could* still do other things)
- The B/C framework predicts this: when capability volume is stable but exercisability declines, the proxy is being Goodharted. This is wireheading in the Senian sense — functionings are technically available but the agent has lost effective freedom to exercise them.
- Same honest acknowledgment: the formal capability measure alone would miss this. The framework's value is in predicting the failure pattern, not in catching it through vol(G) alone.

#### Toward a Proxy-Failure Detector (sketch, not a solution)
- The pattern in both cases: capabilities are formally available but *exercisability* declines — the agent's revealed capability set narrows even as the formal set stays constant
- **Proposed correction criterion:** A GFM actor should monitor not just $\text{vol}(G)$ but the *exercised fraction* — the ratio of capabilities agents actually use to capabilities formally available. A persistent decline in exercised fraction, even with stable or growing vol(G), is a B→C divergence signal.
- This is a *heuristic*, not a formal solution. It introduces its own proxy problem (not all unused capabilities represent experiential contraction — sometimes people just specialize). But it gives the framework a self-diagnostic: if the formal measure and the exercised-fraction measure diverge, the capability proxy is failing and the actor should flag uncertainty.
- **The paper should NOT claim this solves the problem.** It should claim that the B/C framework makes the problem *detectable in principle* and sketch the correction criterion as a direction for future formalization.

#### Human Frame-Skipping
- Connect to blog post `frameskipping.md`
- Humans are also susceptible to frame-skipping: optimizing proxy rewards (money, status, likes) rather than actual goals
- A GFM framework applied to human institutions would flag these proxy traps

#### Open Problems
- **Closing the B→C gap.** The paper adopts capabilities (B) as the formal proxy for experiences (C), but Section 8 demonstrates two cases (Doll Problem, wireheading) where this proxy fails. The exercised-fraction heuristic sketched in Section 8 is a first step toward detection, but formalizing B→C divergence — and proving that any correction criterion doesn't introduce worse proxy problems — remains the central open challenge. A complete GFM framework would need to verify that capability expansion is actually translating into experiential optionality, not just formal option-counting.
- **Structure of $\mathcal{G}$:** The capability interpretation requires $\mathcal{G}$ to have structure beyond a set — at minimum a sigma-algebra with a measure so that vol(G) is well-defined. The finite-difference estimator (Proposition 3) only requires measurability, not differentiability, which relaxes this constraint compared to earlier drafts. But richer structure (a lattice where capabilities have a natural subsumption order, or a topological space where nearby capabilities are similar) would enable stronger results. The choice determines what "volume" means and what additional properties the estimator can exploit. This remains the most urgent formal question for the paper.
- **Measurement:** How do you measure vol(G) in practice, even approximately? What sensors/signals does a GFM actor need to construct the local volume estimator $\hat{V}$?
- **Convergence:** Does the local finite-difference estimator converge to the true vol(G) trajectory over time? Under what conditions?
- **Plurality:** Can multiple GFM actors with different capability-space models coordinate? What happens when they disagree about the structure of $\mathcal{G}$ itself, not just the shape of $G$ within it?
- **Bootstrap:** How do you initialize a GFM actor? The goal estimation problem (predraft Section XI) is itself a hard inference problem, made harder by needing to discover the structure of $\mathcal{G}$ at the same time as populating it.

---

## 9. Conclusion (0.5-1 page)

### Purpose
Restate the result and its significance.

### Must accomplish
- Lead with the result: GFM's self-balancing property (Proposition 1) follows from measure monotonicity — a single objective penalizes destruction, coercion, and rigidity without separate mechanisms for each
- State that the local finite-difference estimator (Proposition 3) makes GFM tractable and sign-correct for the most important class of actions (direct harm, coercion, resource changes)
- Emphasize what makes GFM different: one objective that handles both the control problem and the scorpion problem, with explicit tradeoff accounting rather than hidden assumptions
- Note the B/C framework's distinctive contribution: GFM can predict its own proxy failure modes (Doll Problem, wireheading), which is more than competing frameworks offer
- End with the forward-looking claim: GFM provides a foundation for building AI systems that are aligned not to a fixed human specification but to the ongoing expansion of what all agents can achieve

---

## Appendices

### Appendix A: The Evil Twin Time Bomb (worked example)
- Full scenario from predraft Section VI
- Shows a deontological agent fails; shows a GFM agent succeeds by maximizing optionality
- This is the strongest comparative result against rule-based approaches

### Appendix B: Scorpion Taxonomy
- Condensed from blog post `scorpions.md`
- Formal game-theoretic notation for each type: Cornered Animal, Pascal's Mugging, Necessity of Evil, Outer Sum Rewards, Blue-and-Orange Morality
- Map each to a known alignment failure mode

### Appendix C: Full Derivation of Trust Model
- **Reconstruction project, not a cleanup.** Start from Definitions 1-7 and derive the trust model from the vol(G) objective. The predraft equations (22-25) are reference material for concepts and intent, but the notation and specific functional forms must be rebuilt.
- Concepts to preserve: trust factor $T_k$, cooling period $\tau$, activation energy threshold $\theta$, self-trust $T_s$, gradient-based trust updating
- Concepts to reconsider: the specific choice of MSE as error metric (predraft Eq 10-11), the binary confidence threshold (predraft Eq 11), the specific functional form of the update rule (predraft Eq 25)
- The re-derivation should produce equations that are consistent with the paper's canonical objective (vol(G)) and the social objective assumptions (Definition 5)

### Appendix D: Agent Similarity and Goal Estimation
- Adapted from predraft Sections XI-XII
- Goal similarity metric $S_G$
- Agent similarity metric $S_A$
- Zero-knowledge proof for agent re-identification
- Modal groupings of goal types

---

## Source Material Index

| Source | Location | What to extract |
|--------|----------|----------------|
| Blog: `frameskipping.md` | `public/articles/frameskipping.md` | Frame-skipping concept, path of least action, misleading definitions, SPAM, Turing Game |
| Blog: `limitsofthought.md` | `public/articles/limitsofthought.md` | Computational bounds, tradeoffs, traps for digital minds, CAP theorem for minds |
| Blog: `agi.md` | `public/articles/agi.md` | Actor model (sensors, self, environment, attention, beliefs), architecture sketch |
| Blog: `free.md` | `public/articles/free.md` | FREE framework, CHIEFS, goal frontiers, GFAGI behavior, adversary dynamics |
| Blog: `scorpions.md` | `public/articles/scorpions.md` | Scorpion taxonomy, AI solutions, future concerns |
| Predraft PDF | `predraft.pdf` | Equations 5, 6-12, 22-25; Evil Twin Time Bomb; trust model; goal estimation; Doll Problem; Self-Wireheading |

---

## Style and Format Notes

- **Target format:** LaTeX, conference paper style (e.g., NeurIPS, AAAI, or similar)
- **Numbered definitions and propositions** throughout
- **Minimal background sections.** Cite blog posts for extended arguments already published.
- **Every equation must be referenced in prose** and its variables defined at point of introduction
- **Avoid "will" language** for describing GFAGI behavior. Use "a GFM actor that..." conditional framing instead of "GFAGI will naturally..."
- **Acknowledge limitations inline**, not in a separate "limitations" ghetto at the end

---

## Critical Success Criteria

The paper succeeds if a reader can answer "yes" to all of:

1. **Can I state the central claim in one sentence?** (A single objective — maximizing joint capability volume — penalizes destruction, coercion, and rigidity from the same measure-monotonicity argument)
2. **Do I understand why this is non-obvious?** (Because most alignment frameworks require separate mechanisms for safety and capability, and hide tradeoffs behind rules or scalar utilities)
3. **Do I believe the proposition, given its stated conditions?** (The geometric argument that contraction is anti-maximizing regardless of direction, with honest acknowledgment of the tradeoff cases)
4. **Do I understand how this could be implemented?** (Local finite-difference estimator, trust model reconstructed from first principles, feedback loop)
5. **Do I know what remains unsolved?** (Measurement, structure of $\mathcal{G}$, convergence, bootstrap, closing the B→C gap, formal combinatorial complexity model)
6. **Do I know what the paper does NOT claim?** (That GFM magically resolves all tradeoffs, that interior equilibria are guaranteed, that the capability proxy is sufficient for all cases, that the local estimator catches coalition-level changes, that the trust model equations are final)
7. **Do I understand the paper's relationship to its own proxy?** (The capability formalization is instrumentally justified by the experience objective; the paper identifies where this proxy fails and sketches a correction criterion, rather than pretending the proxy is the real thing)
