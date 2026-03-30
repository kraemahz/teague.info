# Paper Drafting Implementation Plan

> **For agentic workers:** Each task drafts one or more LaTeX sections to near-final quality. The compile command is `cd docs/paper && export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH" && pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft the complete paper "Goal-Frontier Maximizers are Civilization Aligned" in LaTeX, following the approved design spec at `docs/specs/2026-03-30-paper-drafting-design.md` and the paper spec at `docs/specs/PAPER_SPEC.md`.

**Architecture:** Depth-first, definitions-out. Each task drafts a section to near-final quality, compiles to verify, and commits. Author reviews PDF between phases. The paper is self-contained --- blog posts and predraft are source material mined into the paper's own language, not cited.

**Tech Stack:** LaTeX (NeurIPS preprint style), pdflatex, bibtex, natbib

---

## Source Material Reference

These files contain the ideas to formalize. Read them before drafting.

| Source | Path | What to extract |
|--------|------|----------------|
| Paper Spec | `docs/specs/PAPER_SPEC.md` | Master spec --- every section's requirements, definitions, propositions, proof sketches |
| Design Spec | `docs/specs/2026-03-30-paper-drafting-design.md` | Drafting order, decisions, guardrails, blog disposition |
| Blog: FREE | `public/articles/free.md` | Goal frontier definitions, adversary dynamics, rejection criterion |
| Blog: Scorpions | `public/articles/scorpions.md` | Five scorpion types, game-theoretic framing, irremovable defection rate |
| Blog: Frame-Skipping | `public/articles/frameskipping.md` | Proxy values argument, combinatorial explosion (60!), path of least action |
| Blog: Limits of Thought | `public/articles/limitsofthought.md` | Computational bounds arguments |
| Predraft | `docs/predraft.pdf` | Equations 5, 6-12, 22-25 (concepts only --- re-derive notation). Evil Twin scenario. Trust model concepts. Goal estimation. Doll Problem. Self-Wireheading. |

## Style Rules (apply to every task)

- Conditional framing ("a GFM actor that...") not "will" language
- Limitations inline, not in a separate section
- Every equation referenced in prose, variables defined at point of introduction
- Every paragraph carries at least one new idea
- Acknowledge intractability, then solve it
- Honest about proof strength: propositions with explicit assumptions over theorems that overreach
- Lead with what the framework accomplishes; scope limitations proportionally
- One canonical objective used consistently: vol(G) is what we measure. Never use "frontier size" or "frontier area" as the measure.
- No GPT filler

## LaTeX Macros Available

Defined in `main.tex`:
- `\G` = `\mathcal{G}` (capability space)
- `\Gind{k}` = `G_k^{\mathrm{ind}}` (individual capability set)
- `\Gcoop` = `G^{\mathrm{coop}}` (cooperative capabilities)
- `\vol` = `\operatorname{vol}` (volume operator)
- `\sign` = `\operatorname{sign}`
- `\Vhat` = `\hat{V}` (estimated volume)
- `\Deltahat` = `\hat{\Delta}` (estimated volume difference)

Theorem environments: `definition` (starts at 0), `proposition`, `corollary` (numbered under proposition), `remark`, `lemma`

---

### Task 1: Draft Definitions (Section 2)

**Files:**
- Modify: `docs/paper/sections/definitions.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 3 (Definitions) --- full requirements for Defs 0-6
- `public/articles/free.md` --- informal goal frontier definitions to formalize
- Predraft Part III opening --- original goal frontier definition

**What to draft:**

Definition 0 is the hardest and most important. It must:
1. Adopt capabilities (Candidate B) as the formal optimization target
2. Frame experiences (Candidate C) as the motivating justification
3. Make the B-as-proxy-for-C relationship explicit: "GFM does not claim to know what experiences agents want. It maximizes the capabilities that let agents choose for themselves."
4. State why capabilities over states or experiences: strongest formal bridge (empowerment), most natural for self-balancing argument, avoids measurement problems
5. Note that the capability space G requires structure (at minimum a sigma-algebra with measure) and flag this as an open problem

Definitions 1-6 are already scaffolded. Refine them:
- Def 1: Add the motivational grounding paragraph (why capabilities rather than experiences directly)
- Def 2: Add the explanation of why G exceeds the union of individual sets (cooperation creates capabilities no individual possesses --- two people carrying 50kg each can jointly carry 100kg). This is where combinatorial richness enters.
- Def 5: The two critical assumptions (additivity under independence, tradeoff acknowledgment) are already present but need connecting prose explaining why these assumptions matter and what breaks without them
- Def 6: Expand to note that M_k(G) is inferred (not given), and that the trust factor T_k and confidence C_k are learned quantities updated through interaction

Add a closing paragraph before the next section: the key distinction from standard utility maximization is that G is a *space* with volume, not a scalar. This geometric character is what gives GFM its self-balancing property.

**Guardrails:**
- Keep definitions lean. Do NOT define sensors, actuators, self-models, environment models, attention models, or belief models.
- Use standard mathematical notation.
- No new macros needed beyond what main.tex already provides.

- [ ] **Step 1:** Read the Paper Spec Section 3 (Definitions) and blog `free.md` for source material
- [ ] **Step 2:** Draft Definition 0 (Goal) with the B/C philosophical move
- [ ] **Step 3:** Refine Definitions 1-6 with connecting prose, examples, and assumption explanations
- [ ] **Step 4:** Add closing paragraph on geometric character
- [ ] **Step 5:** Compile and verify PDF renders correctly
- [ ] **Step 6:** Commit: `git add docs/paper/sections/definitions.tex && git commit -m "draft: Section 2 Definitions (Defs 0-6)"`

---

### Task 2: Draft Self-Balancing Property (Section 3) + Evil Twin (Appendix A)

**Files:**
- Modify: `docs/paper/sections/self_balancing.tex` (replace TODO scaffolding with full draft)
- Modify: `docs/paper/appendices/evil_twin.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 4 (Self-Balancing Property) --- Prop 1 (a)-(d), Cors 1.1-1.2, Prop 2
- `docs/specs/PAPER_SPEC.md` Appendix A (Evil Twin)
- `public/articles/free.md` --- "Goal Frontiers Create Ethical Behavior" section
- `public/articles/scorpions.md` --- scorpion definition for Prop 2
- `public/articles/frameskipping.md` --- path of least action argument
- Predraft Section VI --- Evil Twin Time Bomb scenario
- Predraft Section XV --- CHIEFS as derived consequences (for context, not inclusion)

**What to draft:**

**Proposition 1 (Self-Balancing Property):** This is the paper's central result. The spec suggests considering whether (a)-(c) should be lemmas with (d) as the synthesizing proposition. Make a decision during drafting based on what reads best.

For each part:
- **(a) Destructive actions are anti-maximizing.** Formal statement: eliminating agent a_k removes at least vol(G_k^ind \ union_{j!=k} G_j) plus cooperative capabilities requiring a_k. Proof sketch from set measure monotonicity --- removing elements from a measurable set cannot increase its measure. State the condition: a_k contributes unique volume.
- **(b) Coercive actions are anti-maximizing, with caveat.** Restricting G_j contracts vol(G) unless compensated elsewhere. The honest caveat: restricting a_j to protect a_k may be net-expanding. Give the quarantine vs. authoritarian state example. The claim is that GFM makes the tradeoff *explicit and measurable*, not that coercion is never justified.
- **(c) Self-imposed rigidity is anti-maximizing.** Constraining own action space reduces frontier expansion ability. Condition: the actor's action space contributes to vol(G).
- **(d) Structural balance.** This is a structural claim about the *shape* of the objective, NOT an equilibrium existence proof. The same objective penalizes both extremes. Proving interior equilibria exist would require additional assumptions the paper does not provide. State this honestly.

**Corollary 1.1 (Elimination):** Unique contribution is strictly positive for any agent with at least one non-universal goal. Cooperative loss grows super-linearly with interaction partners. This is the combinatorial scaling observation, not a formal hardness result.

**Corollary 1.2 (Rigid Rules):** Fixed rule set R reduces action space. Reference Evil Twin (Appendix A) as the worked counterexample.

**Proposition 2 (Scorpion Detection):** A GFM actor modeling other agents' goals will detect persistent vol(G)-contracting behavior *to the extent that contraction is observable*. Define "scorpion" briefly here (full taxonomy in Appendix B). State the scope limitation explicitly: inherits observability constraints from Proposition 3. Social/structural scorpions (coalition disruption, trust degradation, observability reduction) may evade detection.

**Open problems to acknowledge inline:**
- (d) is structural, not equilibrium existence
- Detection bounded by Prop 3 observability
- No convergence rate claims

**Appendix A (Evil Twin):** Full worked example. Structure:
1. Setup: AGI with strict rules controls a valuable resource. Adversary threatens Evil Twin release on tight deadline.
2. The bind: rule-following AGI caught between ethical obligations and capitulation to extortion. Cannot weigh probabilities under strict rules.
3. GFM analysis: a GFM actor evaluates vol(G) impact of each option --- capitulation contracts frontier (surrenders resources), risk-weighted resistance may expand or preserve it. The GFM actor can reason about probabilities and tradeoffs.
4. Conclusion: rigid rules create exploitable predictability. GFM's flexibility is a feature, not a bug.

- [ ] **Step 1:** Read Paper Spec Section 4 and predraft Section VI for source material
- [ ] **Step 2:** Draft Proposition 1 (a)-(d) with proof sketches and conditions
- [ ] **Step 3:** Draft Corollaries 1.1 and 1.2
- [ ] **Step 4:** Draft Proposition 2 (Scorpion Detection) with scope limitation
- [ ] **Step 5:** Draft Appendix A (Evil Twin Time Bomb)
- [ ] **Step 6:** Compile and verify
- [ ] **Step 7:** Commit: `git add docs/paper/sections/self_balancing.tex docs/paper/appendices/evil_twin.tex && git commit -m "draft: Section 3 Self-Balancing Property + Appendix A Evil Twin"`

---

### Task 3: Draft Tractability (Section 4)

**Files:**
- Modify: `docs/paper/sections/tractability.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 5 (Tractability) --- intractability, Def 7, Prop 3, failure modes, feedback loop, cost
- `public/articles/frameskipping.md` --- combinatorial explosion argument (60! example)
- `public/articles/limitsofthought.md` --- computational bounds
- Predraft Equation 5 --- loop structure (concepts only, re-derive)
- Predraft Equations 22-25 --- trust model concepts (preserve concepts, rebuild notation)
- Dyer & Frieze (1988) --- #P-hardness of polytope volume (cite properly)
- Klyubin et al. (2005) --- empowerment as tractable proxy (cite)

**What to draft:**

**Intractability (subsection):** Two arguments with different epistemic status, presented separately:
1. *Formal (external, rigorous):* Volume of high-dimensional polytope is #P-hard \citep{dyer1988complexity}. If G can be represented as a polytope, exact vol(G) is intractable. This is a known result being applied.
2. *Motivating (original, informal):* Joint goal space includes interaction effects between agents. Number of possible interaction combinations grows combinatorially. Use the paper's own language for the combinatorial argument mined from `frameskipping.md`, but do not use the "frame-skipping" term. State that a formal model of why joint goal-space complexity scales this way remains an open problem.
3. *Combined conclusion:* Even under optimistic assumptions, exact GFM is intractable.

**Definition 7 (Local Volume Estimator):** Already scaffolded. Expand with:
- The key insight: GFM does not need to compute vol(G), only sign(Delta vol(G) | pi)
- What the estimator does NOT require: a metric on G, notion of direction, continuity. Only measurability.
- Observability channels: (1) Individual capability signals --- accept/reject R_k, weighted by T_k, good coverage. (2) Coalition capability signals --- indirect, noisier, slower.
- Critical assumption stated explicitly: V-hat is a better estimator of vol(union G_k^ind) than vol(G). The cooperative component is systematically underweighted. This is the primary implementation gap.

**Proposition 3 (Sign-Correctness):** Already scaffolded. Add:
- Proof sketch: self-balancing is structural (monotonicity). Sign-preservation assumption bridges structure to estimator output.
- Discussion of when condition 3 holds: direct harm, coercion, resource changes produce large individual-capability signals. The estimator is strongest where alignment matters most.
- Discussion of when condition 3 fails: actions primarily on coalition structure while individual capability sets are unchanged.

**Remark (Estimator Failure Modes):** Already scaffolded. Fill in the four cases:
1. Full individual observation, no cooperative change --- sign-correct
2. Partial individual, no cooperative change --- depends on sampling model
3. Mixed individual and cooperative --- unreliable when cooperative dominates
4. Pure coalition-level --- blind

Add the "what the Remark gives you" framing: a threat model that tells implementers where to invest.

**The Optimization Loop (subsection):** Re-derive from vol(G) objective:
- Propose action pi
- Estimate Delta vol(G) via local volume estimator (Def 7)
- Aggregate accept/reject signals R_k from observed agents, weighted by T_k
- Update frontier estimate and goal models M_k(G)
- The activation energy concept: world model only updates when evidence exceeds threshold theta. This is a key design parameter for adversarial robustness --- prevents manipulation through incremental gaslighting. Treat as first-class, not a footnote.
- Trust model interface defined here. Full derivation deferred to Appendix C.

**Computational Cost (subsection):**
- Local GFM scales with number of observed agents, not total population
- Per-decision cost: propose, estimate, aggregate, update
- Comparable to contextual multi-armed bandit with structured feedback

- [ ] **Step 1:** Read Paper Spec Section 5, `frameskipping.md` combinatorial argument, `limitsofthought.md` bounds, predraft Equations 5 and 22-25
- [ ] **Step 2:** Draft intractability subsection (two arguments, combined conclusion)
- [ ] **Step 3:** Expand Definition 7 with observability channels and critical assumption
- [ ] **Step 4:** Draft Proposition 3 proof sketch and condition analysis
- [ ] **Step 5:** Fill in the Remark on estimator failure modes
- [ ] **Step 6:** Draft the optimization loop subsection with activation energy emphasis
- [ ] **Step 7:** Draft computational cost subsection
- [ ] **Step 8:** Add \citep references to Dyer & Frieze, Klyubin et al.
- [ ] **Step 9:** Compile and verify
- [ ] **Step 10:** Commit: `git add docs/paper/sections/tractability.tex && git commit -m "draft: Section 4 Tractability and Local Approximation"`

---

### Task 4: Draft Multi-Agent Dynamics (Section 5) + Trust Model (Appendix C)

**Files:**
- Modify: `docs/paper/sections/multi_agent.tex` (replace TODO scaffolding with full draft)
- Modify: `docs/paper/appendices/trust_model.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 6 (Multi-Agent Dynamics) and Appendix C (Trust Model)
- `public/articles/scorpions.md` --- scorpion interaction dynamics
- `public/articles/free.md` --- "Adversary FREE" section, commensalism hypothesis
- Predraft Section XIII --- payoff matrices, cooperation conditions
- Predraft Equations 22-25 --- trust model (concepts to preserve, notation to rebuild)
- Axelrod (1984) --- iterated games (cite)
- FAIR Diplomacy (2022) --- multi-agent negotiation (cite)

**What to draft:**

**GFM-GFM Cooperation (subsection):**
- Multiple GFM actors share vol(G) objective
- Under sufficient mutual trust and compatible world models, cooperation is favored because joint action expands G^coop
- This is NOT game-theoretic dominance --- it is contingent on trust and model-agreement conditions
- Goal drift between GFM actors is bounded by shared objective, but divergent world models can produce conflicting choices even with shared intent

**GFM-Scorpion Interaction (subsection):**
- Define "scorpion" precisely: an agent whose chosen rewards exist outside the observable criteria of the cooperative game (full taxonomy in Appendix B)
- Scorpions produce persistent frontier contraction
- Trust model flags behavior as T_k decreases, subject to observability constraints (Prop 2)
- Response is containment: reduce scorpion's contraction ability without unnecessarily contracting frontier further
- This is self-balancing applied to adversarial agents: proportional response

**Trust Model (subsection):**
- Define the interface in the main body. The reader needs to know what the trust model does and what properties it has, not how every equation is derived.
- Trust factor T_k: consistency of M_k(G) predictions with observed behavior
- Cooling period tau: new agents start low, trust increases with convergence
- Self-trust T_s: confidence in own world model, incorporating activation energy theta
- Trust updated via gradient tracking: T_k increases when M_k(G) converges, decreases on divergence
- Defer full derivation to Appendix C

**Defection Conditions (subsection):**
- When GFM actor may rationally defect: very low goal alignment, very low trust, repeated defection observed, preventing exploitation requires non-cooperation
- Key: defection for GFM is *containment, not destruction*. The objective remains frontier-maximizing even in adversarial contexts.

**Appendix C (Trust Model Derivation):**
RECONSTRUCTION, not cleanup. Start from Definitions 1-7 and derive:
- C.1: Trust factor T_k derived from consistency of M_k(G) predictions with observed behavior
- C.2: Cooling period tau --- why new agents start low, formal justification
- C.3: Self-trust T_s and activation energy theta --- formal relationship to vol(G) objective
- C.4: Trust update rule via gradient tracking on M_k(G) convergence
- C.5: Integration with local volume estimator (Def 7) --- how trust weights affect the estimator

Preserve concepts from predraft Eqs 22-25 but rebuild notation from this paper's definitions. Reconsider: MSE as error metric, binary confidence threshold, specific functional forms.

- [ ] **Step 1:** Read Paper Spec Section 6 and Appendix C, `scorpions.md`, `free.md` adversary section, predraft Section XIII and Eqs 22-25
- [ ] **Step 2:** Draft GFM-GFM Cooperation subsection
- [ ] **Step 3:** Draft GFM-Scorpion Interaction subsection
- [ ] **Step 4:** Draft Trust Model interface subsection (main body)
- [ ] **Step 5:** Draft Defection Conditions subsection
- [ ] **Step 6:** Draft Appendix C full trust model derivation (C.1-C.5)
- [ ] **Step 7:** Add \citep references to Axelrod, FAIR Diplomacy
- [ ] **Step 8:** Compile and verify
- [ ] **Step 9:** Commit: `git add docs/paper/sections/multi_agent.tex docs/paper/appendices/trust_model.tex && git commit -m "draft: Section 5 Multi-Agent Dynamics + Appendix C Trust Model"`

---

### Task 5: Draft Standalone Appendices (B, D)

**Files:**
- Modify: `docs/paper/appendices/scorpion_taxonomy.tex` (replace TODO scaffolding with full draft)
- Modify: `docs/paper/appendices/agent_similarity.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Appendices B and D
- `public/articles/scorpions.md` --- full scorpion taxonomy (source material to mine)
- Predraft Sections XI-XII --- goal estimation, agent characterization, similarity metrics

**What to draft:**

**Appendix B (Scorpion Taxonomy):**
Define "scorpion" formally in game-theoretic terms: an agent that plans to defect regardless of game rewards, whose chosen rewards exist outside the observable criteria of the game.

Five types, each with:
- Formal game-theoretic characterization
- Concrete example
- Mapping to a known alignment failure mode
- Assessment of GFM detectability (ties back to Prop 2 and the estimator failure modes)

Types:
1. **Cornered Animal:** Normal player who defects when all options produce loss. Switches to minimizing others' utility. Alignment failure: distributional shift under stress. Detectable: yes (large individual-capability signals).
2. **Pascal's Mugging:** Agent receiving outside reward so high it overrides cooperative calculation. Wireheading is the AI version. Alignment failure: reward hacking. Detectable: depends on observability of the outside reward.
3. **Necessity of Evil:** Deliberate antagonist red-teaming society. Alignment failure: adversarial robustness. Detectable: behavior looks like contraction, but intent is constructive. Hardest case for the trust model.
4. **Outer Sum Rewards:** Agrees on facts, disagrees on "ought." Acts for imagined greater good against others' interests. Alignment failure: value misalignment with correct world model. Detectable: yes (actions produce observable contraction).
5. **Blue-and-Orange Morality:** Fundamentally different axioms. Internally consistent but orthogonal to shared expectations. Alignment failure: mesa-optimization with alien objectives. Detectable: most unpredictable, may operate primarily through coalition disruption (estimator's known boundary).

Must be self-contained. No blog citation required to understand the taxonomy.

**Appendix D (Agent Similarity and Goal Estimation):**
Adapted from predraft Sections XI-XII with notation rebuilt from this paper's definitions.

- D.1: Goal similarity metric S_G --- how to determine two goals are similar, projected through shared models
- D.2: Agent similarity metric S_A --- behavioral consistency plus identity verification
- D.3: Zero-knowledge proof for agent re-identification --- strongest form of identity, overrides behavioral scores
- D.4: Modal groupings --- clusters of agents with similar goal profiles

- [ ] **Step 1:** Read `scorpions.md` and predraft Sections XI-XII
- [ ] **Step 2:** Draft Appendix B formal scorpion definition and five types
- [ ] **Step 3:** Draft Appendix D similarity metrics and goal estimation
- [ ] **Step 4:** Compile and verify
- [ ] **Step 5:** Commit: `git add docs/paper/appendices/scorpion_taxonomy.tex docs/paper/appendices/agent_similarity.tex && git commit -m "draft: Appendix B Scorpion Taxonomy + Appendix D Agent Similarity"`

---

### Task 6: Draft Connections (Section 6)

**Files:**
- Modify: `docs/paper/sections/connections.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 7 (Connections)
- Klyubin et al. (2005) --- empowerment
- Sen (1999) --- capability approach
- Friston (2013) --- free energy principle
- Christiano et al. (2017), Bai et al. (2022) --- RLHF, Constitutional AI

**What to draft:**

Four subsections, each identifying: the parallel, the key difference, and what GFM adds.

1. **Empowerment Maximization (formal bridge):** Empowerment = mutual information between actions and future states. GFM is *social empowerment*: across joint action space of all agents. Key difference: empowerment is agent-centric, GFM is population-centric. GFM may inherit some empowerment tractability.

2. **Sen's Capability Approach (philosophical bridge):** Well-being measured by available functionings. GFM: alignment measured by achievable capabilities. Decades of formal development to leverage. Key difference: capability approach is descriptive/evaluative, GFM is prescriptive/optimizing.

3. **Free Energy Principle (structural bridge):** FEP: minimize prediction error. FREE: maximize goal frontier. Both produce agents maintaining coherent world models while adapting. "Free Relative Energy Ethics" is a deliberate echo --- make connection explicit.

4. **Constitutional AI / RLHF (practical bridge):** Human feedback is a noisy channel for communicating the goal frontier. GFM provides theoretical foundation for why RLHF works. GFM predicts where RLHF fails: narrow evaluator pool, reward hacking.

Each subsection should be 1-2 paragraphs. Total section: 1-2 pages.

- [ ] **Step 1:** Read Paper Spec Section 7
- [ ] **Step 2:** Draft all four subsections
- [ ] **Step 3:** Add \citep references
- [ ] **Step 4:** Compile and verify
- [ ] **Step 5:** Commit: `git add docs/paper/sections/connections.tex && git commit -m "draft: Section 6 Connections to Existing Frameworks"`

---

### Task 7: Draft Future Concerns and Open Problems (Section 7)

**Files:**
- Modify: `docs/paper/sections/future_concerns.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 8 (Future Concerns) --- Doll Problem, wireheading, proxy-failure detector, open problems
- `public/articles/frameskipping.md` --- proxy values, human susceptibility to proxy traps
- Predraft Section XVI --- Doll Problem and Self-Wireheading scenarios

**What to draft:**

**Framing paragraph:** The B/C framework's analytical power is that it can precisely identify when and why the formal proxy fails. This is a feature --- a framework that names its own failure modes is more trustworthy than one that hides them.

**Doll Problem (subsection):**
- AI companions replacing human relationships
- Under capability formalization (B) alone, this may not register as contraction --- capability set looks neutral or expanded
- B/C framework *predicts* this divergence: capabilities preserved but experiential optionality contracts
- Honest: formal machinery alone insufficient here. Experience layer does the work.
- Contribution: the B/C distinction makes this failure diagnosable and predictable. A framework without the experience layer cannot name what went wrong.

**Self-Wireheading (subsection):**
- Algorithmically optimized content feeds steering toward lower-effort, higher-dopamine activities
- Each step freely chosen; capabilities formally unchanged
- B/C predicts: stable capability volume + declining exercisability = proxy being Goodharted
- This is wireheading in the Senian sense: functionings technically available but effective freedom to exercise them declining
- Same honest acknowledgment as Doll Problem

**Toward a Proxy-Failure Detector (subsection):**
- Pattern: capabilities formally available but exercisability declines
- Proposed correction criterion: monitor exercised fraction (ratio of used to available capabilities)
- Persistent decline with stable vol(G) = B-to-C divergence signal
- This is a HEURISTIC, not a solution. Introduces own proxy problem: specialization is not contraction. Not all unused capabilities represent experiential contraction.
- The paper must NOT claim this solves the problem. Claim: B/C framework makes the problem *detectable in principle*.

**Human Proxy-Trap Susceptibility (subsection):**
- Evaluate whether "frame-skipping" as a term adds value beyond established language (Goodhart's Law, proxy gaming, reward hacking). Use established language unless the coined term meaningfully extends the argument.
- Humans optimizing proxy rewards (money, status, likes) rather than actual goals
- GFM applied to human institutions would flag these proxy traps

**Open Problems (subsection):**
Bulleted list with 1-2 sentences each:
- Closing the B-to-C gap (central open challenge)
- Structure of G (sigma-algebra? lattice? topological space? most urgent formal question)
- Measurement (sensors/signals for V-hat in practice)
- Convergence (does local estimator converge to true vol(G) trajectory?)
- Plurality (multiple GFM actors with different G models)
- Bootstrap (initializing a GFM actor --- goal estimation is itself a hard inference problem)

- [ ] **Step 1:** Read Paper Spec Section 8, `frameskipping.md`, predraft Section XVI
- [ ] **Step 2:** Draft framing paragraph and Doll Problem subsection
- [ ] **Step 3:** Draft Self-Wireheading subsection
- [ ] **Step 4:** Draft Proxy-Failure Detector subsection with honest caveats
- [ ] **Step 5:** Make frame-skipping terminology decision and draft Human Proxy-Trap subsection
- [ ] **Step 6:** Draft Open Problems list
- [ ] **Step 7:** Compile and verify
- [ ] **Step 8:** Commit: `git add docs/paper/sections/future_concerns.tex && git commit -m "draft: Section 7 Future Concerns and Open Problems"`

---

### Task 8: Draft Introduction (Section 1)

**Files:**
- Modify: `docs/paper/sections/introduction.tex` (replace TODO scaffolding and \nocite block with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Section 2 (Introduction) --- requirements and exclusion list
- The completed Sections 2-7 (read the compiled PDF to know what the paper actually delivers)

**What to draft:**

Written last because it must accurately preview a finished paper.

**Paragraph 1:** Frame the alignment problem as choosing the right objective function, not the right set of rules. The reader is assumed familiar with basic ML, game theory, and alignment discourse.

**Paragraph 2-3:** Three failure modes of existing approaches:
- Fixed utility functions: vulnerable to Goodhart's Law, specification gaming, perverse instantiation \citep{bostrom2014superintelligence, hubinger2019risks}
- Deontological rules: brittle under adversarial conditions (reference Evil Twin in Appendix A as worked example)
- Unconstrained consequentialism: can sacrifice individuals for aggregate utility

**Paragraph 4:** Introduce GFM as a third option: maximize the space of achievable goals for all agents. State the central claim: a single objective --- maximizing joint capability volume --- naturally resists both destructive action and overreactive constraint.

**Paragraph 5:** Roadmap the paper sections.

**Exclusion list (DO NOT include):**
- ML basics
- "ML models cannot adapt" argument
- Sigmoid vs. exponential discussion
- Extended Clippy/frame-skipping argument

Remove the `\nocite` block --- all citations should now be organic \citep references.

- [ ] **Step 1:** Read Paper Spec Section 2 and the completed PDF for what the paper actually delivers
- [ ] **Step 2:** Draft introduction paragraphs
- [ ] **Step 3:** Add \citep references (Bostrom, Hubinger, Carlsmith)
- [ ] **Step 4:** Remove the \nocite block from the scaffolding
- [ ] **Step 5:** Compile and verify
- [ ] **Step 6:** Commit: `git add docs/paper/sections/introduction.tex && git commit -m "draft: Section 1 Introduction"`

---

### Task 9: Draft Conclusion + Abstract

**Files:**
- Modify: `docs/paper/sections/conclusion.tex` (replace TODO scaffolding with full draft)
- Modify: `docs/paper/sections/abstract.tex` (replace TODO scaffolding with full draft)

**Context to read first:**
- `docs/specs/PAPER_SPEC.md` Sections 1 (Abstract) and 9 (Conclusion)
- The complete compiled PDF

**What to draft:**

**Conclusion (0.5-1 page):**
- Lead with the result: self-balancing property (Prop 1) follows from measure monotonicity --- a single objective penalizes destruction, coercion, and rigidity
- Local finite-difference estimator (Prop 3) makes GFM tractable and sign-correct for the most important action class
- What makes GFM different: one objective for both the control problem and the scorpion problem, with explicit tradeoff accounting
- B/C framework's distinctive contribution: GFM predicts its own proxy failure modes
- Forward-looking: aligned to ongoing expansion of what all agents can achieve, not a fixed specification

**Abstract (~150 words):**
- Define GFM in one sentence
- State self-balancing property (Prop 1)
- State local estimator with sign-correctness (Prop 3)
- Claim: more robust than fixed utility or deontological rules
- Note B/C distinction and proxy failure prediction

- [ ] **Step 1:** Read the complete compiled PDF
- [ ] **Step 2:** Draft conclusion
- [ ] **Step 3:** Draft abstract (~150 words)
- [ ] **Step 4:** Compile and verify
- [ ] **Step 5:** Review against Critical Success Criteria (can a reader answer "yes" to all 7?)
- [ ] **Step 6:** Commit: `git add docs/paper/sections/conclusion.tex docs/paper/sections/abstract.tex && git commit -m "draft: Section 8 Conclusion + Abstract"`

---

### Task 10: Final Compilation and Cleanup

**Files:**
- Modify: `docs/paper/main.tex` (if any macro additions needed)
- Modify: `docs/paper/references.bib` (verify all cited works are present)
- All section files (minor cross-reference fixes)

- [ ] **Step 1:** Full compile from clean state: delete .aux, .bbl, .blg, .log, .out files, then run full pdflatex/bibtex cycle
- [ ] **Step 2:** Check for undefined references, missing citations, bad cross-refs
- [ ] **Step 3:** Verify all \label/\ref pairs resolve correctly
- [ ] **Step 4:** Read through compiled PDF end-to-end checking for:
  - Consistent notation throughout
  - No orphaned TODO comments
  - All equations referenced in prose
  - All variables defined at point of introduction
  - Style rules followed (conditional framing, inline limitations, no filler)
- [ ] **Step 5:** Fix any issues found
- [ ] **Step 6:** Final compile and commit: `git add docs/paper/ && git commit -m "paper: complete first draft, all sections"`
