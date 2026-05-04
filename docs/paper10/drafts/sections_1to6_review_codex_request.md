# Codex review request: Paper 10 sections 1-6 checkpoint review

## Mode

**Constructive checkpoint review during drafting.** We have completed sections 1-6 of Paper 10 (~27 pages). Sections 7-10 are not yet drafted (currently stubbed in `main.tex`). Before continuing, we want a checkpoint review to surface issues before they propagate.

This is not a final adversarial review. The goal is to catch problems early — internal inconsistencies, broken cross-references, claims that the formal apparatus doesn't deliver, places where the prose drifts from what we've actually proved.

If you find issues, identify them. If §1-6 hangs together as a coherent foundation for §7-10, say so.

## What to read

Primary:
- `docs/paper10/main.pdf` — the compiled draft, 27 pages
- `docs/paper10/main.tex` — preamble, macros, section orchestration
- `docs/paper10/sections/abstract.tex`
- `docs/paper10/sections/introduction.tex`
- `docs/paper10/sections/composition_setup.tex`
- `docs/paper10/sections/invariants.tex`
- `docs/paper10/sections/lemmas.tex`
- `docs/paper10/sections/main_theorem.tex`
- `docs/paper10/sections/substrate_anchoring.tex`

Reference (for the work that shaped these sections):
- `docs/paper10/paper10_proposal.md` — the proposal these sections instantiate
- `docs/paper10/drafts/lemma_5_anti_monopolar_robustness.tex` — v5 main exploratory draft (the proposal sections distill this)
- `docs/paper10/drafts/lemma_5c_minimax_static_tightening.tex` — v4 Lemma 5c standalone derivation

Source paper sections referenced:
- `docs/paper3/sections/substitution.tex`
- `docs/paper5/sections/witnesses.tex`, `commitment.tex`, `asymmetry.tex`
- `docs/paper6/sections/lyapunov.tex`, `phase_boundary.tex`, `absorbing_state.tex`
- `docs/paper8a/sections/lower_bound.tex`
- `docs/paper8b/sections/...`
- `docs/paper9/sections/goodhart.tex`

## What we want from you

Five focus areas, in priority order:

### Q1. Internal consistency across §1-6

Does the abstract match what the theorem (§5) actually proves? Does the introduction's preview of the three-layer claim match the §5 statement? Do the lemmas referenced in §5's proof match what §4 actually establishes? Do the invariants used in §5 (eleven of them) match what §3 defines (eleven of them, with the right structural roles)?

Specific checks:
- The abstract claims "Goodhart slack between proxy and operational truth is bounded by a constant independent of the system's absolute capability magnitude." Does §5's Theorem 1 actually establish this?
- §1 previews "three-layer deployment claim." Does §5 deliver three layers, with the residuals (Layer 3) named explicitly?
- §1.5 promises a canonical tripartite substrate identification. Does §6 establish it formally? Are the failure-correlation-independence claims defensible in the proof of §6's Proposition?
- §3's eleven invariants — are all eleven actually used somewhere in §4-6? If any is dead weight, flag it.

### Q2. Title-claim alignment

The title is "Goal-Frontier Maximization: A Provably Safe Regime for Capability-Unbounded Deployment." 

Question: Does the formal apparatus deliver "provably safe" and "capability-unbounded"? Specifically:
- "Provably safe" should mean the theorem is a proof, not a heuristic. Is §5's proof actually a proof, or is it a sketch with hand-waved gaps?
- "Capability-unbounded" should mean the bound does not scale with capability magnitude. Is the intensivity argument in §5 (Layer 1, Step 6) and §4 Lemma 1 actually rigorous?
- "Regime" implies conditions under which safety holds. Are the conditions (C1)-(C5) of Theorem 1 sufficient, or are there hidden assumptions we glossed?

If the title claims more than the apparatus delivers, this is a place to surface it.

### Q3. Lemma 5c proof reference

§4.9 (Lemma 5c) references the companion exploratory draft for the full derivation rather than reproducing it inline. The §4.9 proof sketch has six steps but defers the multi-shock derivation, the high-$\lambda$ behavior, and the cooperative-vs-redundancy audit to the companion draft.

Question: Is this acceptable for a paper that cites Lemma 5c as a foundation for the main theorem? Or does §4.9 need to be expanded to be self-contained? If self-contained, what specifically must be reproduced?

### Q4. Prose-formal balance in §6

§6 has a different register from §3-5: more discursive, fewer numbered theorems, more explanatory text. The codex review rounds on §6 specifically shaped it this way (the structural finding requires explanation, not just statement).

Question: Does §6 strike the right balance between formal claims and operational interpretation? Are there places where the prose makes claims the formal apparatus doesn't support? In particular, the cooperative-anchoring proposition (§6.2) is informal — should it be tightened, or is this the right register?

### Q5. Forward references to §7-10

The drafted sections reference §7 (operationalization of Conjecture 1), §8 (deployment tooling), §9 (worked scenarios), §10 (discussion) at multiple points. None of these are yet drafted.

Question: Are the forward references well-formed? Specifically:
- §3.7 (conjecture-dependence audit) defers the empirical validation pathway to §7. Is the right content set up for §7 to deliver it?
- §6 references §10 (discussion) for residuals and basin-entry follow-up. Is the right tone established for §10's role?
- The deployment-tooling specification is referenced in many places (§3 invariants, §5 proof Step 5, §6 evasions). Does the specification need to provide concrete operational procedures, or are the references currently vague enough to be future-flexible?

If any forward reference is over-promising what §7-10 can reasonably deliver, flag it.

## What we are NOT asking

- Stylistic feedback (LaTeX, prose flow, sentence-level clarity).
- Whether the paper is well-positioned for a particular venue.
- Reviewer-style line-by-line critique. We will run a final adversarial review when §1-10 is complete.
- Re-litigation of previously-settled points (Lemma 5c v4 corrections, §6 cooperative-anchoring narrowing). Those are settled.

## Output we want

For each Q1-Q5:

- **Yes, this is solid** — brief confirmation with anything minor worth noting.
- **Issue identified** — name the issue precisely; recommend whether it requires revision before §7-10 or can be addressed later.
- **Significant problem** — explain the structural obstruction and what would be needed to resolve.

Plus: any cross-cutting issue you identify that doesn't fit Q1-Q5 (e.g., a notational inconsistency that affects multiple sections, a missing definition the lemmas implicitly assume).

The goal is to know whether §1-6 is a stable foundation or whether revisions are needed before continuing.
