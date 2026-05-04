# Codex review request: Lemma 5a v2 — re-review after Round A revisions

## Mode

**v2 confirmation review.** Round A returned "v2 needed" with Q2 (Step 4 additivity) as significant problem plus minor refinements on Q1, Q3, Q5 and a caveat fix.

V2 fixes:

- **Q1:** Heterogeneous rates $\rho_{ij}$ over audited subset $\Saudit$, with $\rho_0 = \min_{i<j \in \Saudit} \rho_{ij}$.
- **Q2 (the big fix):** Replaced incorrect "joint independence implies additivity" with new explicit Assumption SU (Pairwise cooperative channel superposition), comprising disjoint attribution + non-rivalrous production + joint-deployment intensities.
- **Q3:** Pairwise channels redefined as exact-two-substrate support (not "at least one from each"), eliminating double-counting of higher-order cooperatives.
- **Q5:** CN+SU surfaced as theorem-level condition (C10).
- **Caveat fix:** Removed v1's incorrect claim that failure-correlation independence excludes correlated-channel sub-additivity. Added Remark 3 distinguishing $I_6'$ (shock independence) from SU (cooperative-production superposition).

## What to read

Primary:
- `docs/paper10/drafts/lemma_5a_full_proof_v2.tex` — v2 (6pp PDF)

Reference:
- Round A findings: `b39ep4z5a.output`
- `docs/paper10/sections/main_theorem.tex` C1-C9 — where (C10) gets added
- `docs/paper10/sections/invariants.tex` — $I_6'$ definition codex pointed to

## What we want from you

Five v2 verification questions:

### Q1. Is SU's three-part formulation right?

SU has three sub-conditions:
1. Disjoint attribution (channels are disjoint event classes)
2. Non-rivalrous production (rates not reduced by simultaneous production in other channels)
3. Joint-deployment intensities (rates measured in joint deployment, not isolation)

**Question:** Are all three necessary, or can some be derived from others? In particular, does (3) follow from the way audit calibration is performed, making it implicit rather than a separate sub-condition?

### Q2. Is the audited-subset $\Saudit$ formulation correctly scoped?

V2 introduces $\Saudit$ as an audited subset of $m^*$ substrates. The deployment may have $\mindep > m^*$ substrates total, but only the audited subset is used for the bound.

**Question:** Is $\Saudit$ an audit-time construct (chosen once) or a deployment-state construct (could change as substrates evolve)? The proof treats it as fixed; should the deployment-tooling specification allow re-auditing as substrates change?

### Q3. Is exact-two-substrate-support correctly preventing double-counting?

Definition: $\mathcal{C}^{(s_i, s_j)} = \{c : \mathrm{participants}(c) \subseteq s_i \cup s_j\}$ (exact two-substrate support).

**Question:** What about cooperatives with two-substrate primary participants but optional third-substrate auxiliary participants (e.g., a Human-AI cooperative that occasionally invokes a Formal-Operational verifier)? Are these:
- Pairwise (counted in $\mathcal{C}^{(\mathrm{Human}, \mathrm{AI})}$)?
- Three-way (counted in $\mathcal{C}^{(\mathrm{Human}, \mathrm{AI}, \mathrm{Formal})}$)?
- Mixed (sometimes pair, sometimes three-way)?

The classification matters for the rate bookkeeping.

### Q4. Is Step 4's additivity argument now rigorous under SU?

V1's mistake was using $I_6'$ (failure-correlation independence) when cooperative-channel additivity actually requires SU. V2 explicitly invokes SU's three sub-conditions in Step 4.

**Question:** Is the argument now watertight? Specifically, do SU(1)+SU(2)+SU(3) together imply the additive sum in Step 4, or are there still hidden conditions (e.g., measurability of per-pair rates, finiteness of the substrate population)?

### Q5. Is (C10) framing for Theorem 1 correct?

V2 surfaces CN+SU as a single condition (C10). 

**Question:** Should this be one condition or two? Arguments for separation: CN is a coercivity claim (per-pair rates positive); SU is a structural claim (channels superpose). Arguments for unification: both are deployment-class conditions on cooperative-production structure, and both are required jointly for the bound.

## Output format

For each Q1-Q5:
- **Sound** — confirmation, ready for appendix integration.
- **Issue identified** — name precisely; recommend whether v3 needed or addressable at integration.
- **Significant problem** — explain the obstruction.

If you find an issue we did not name, flag it.

## Goal

Settle whether Lemma 5a v2 is ready for appendix integration. If yes, proceed to next TODO item. If v3 needed, revise.
