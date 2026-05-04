# Paper 10 — Outstanding proof work

Items flagged during the §1-6 checkpoint review (codex Round D, 2026-05-03)
that need formal-proof treatment before final publication. Each lemma is
currently in either ``inline outline'' (proof sketch in §4) or ``inline
outline + appendix proof'' (full proof in `appendices/proofs.tex`).

This document is the working list for the post-§7-10 proof-tightening pass.

## Items already at full-proof level

These have detailed proofs in the appendix:

- **Lemma 1** (Intensive composition under co-evolution) — `appendices/proofs.tex` §A.1
  - Status: full proof via two codex review rounds (v1 → v2 → integrated)
  - New conditions added to Theorem 1: (C6) bounded-Lipschitz alignment, (C7) bounded co-evolution (Assumption~\ref{ass:bounded_coev}), (C8) per-capability admissibility
  - New Audit 4 in §8 deployment-tooling: bounded co-evolution calibration with explicit $\bar{M}$ and $K_{\mathrm{coev}}$ procedures

- **Lemma 2** (Lyapunov-to-Goodhart bridge) — `appendices/proofs.tex` §A.2
  - Status: full proof via two codex review rounds (v1 → v2 → integrated)
  - Round A caught Paper 9's $\epsnonres$ as relative sup-norm (vs. v1's absolute); v2 added truth-floor assumption (TF) with $1/T_{\min}$ factor
  - New condition added to Theorem 1: (C9) world-model parameterization regularity, comprising sub-conditions BD/CL/WB/TF
  - New Audit 5 in §8 deployment-tooling: world-model parameterization regularity calibration with $N_{\max}, L_{\max}, w_{\min}, T_{\min}$ procedures
  - Tighter heterogeneous form provided for deployment-specific calibration

- **Lemma 5a** (Substrate floor) — `appendices/proofs.tex` §A.3
  - Status: full proof via two codex review rounds (v1 → v2 → integrated)
  - Round A caught Step 4 additivity error: joint failure-correlation independence ($I_6'$) does NOT imply cooperative-production additivity; v2 added explicit superposition assumption (SU)
  - New condition added to Theorem 1: (C10) Pairwise cooperative-production floor, with sub-clauses (C10.CN) heterogeneous per-pair rate floors and (C10.SU) channel superposition
  - New Audit 6 in §8 deployment-tooling: pairwise cooperative-production floor calibration with audited subset $\Saudit$, per-pair $\rho_{ij}$ measurement, auxiliary-participant bookkeeping (causally-necessary participation rule), and superposition verification
  - Pairwise-only floor is conservative; higher-order cooperatives contribute additionally

- **Lemma 4** (SPRT lead-time tail bound) — `appendices/proofs.tex` §A.4
  - Status: full Wald + Hoeffding derivation with explicit constants
  - Caveat present: Paper 6 metastable-lifetime scaling-law qualification

- **Lemma 5b** (Channel-restricted detection KL floor) — `appendices/proofs.tex` §A.5
  - Status: full per-channel derivations (Poisson, Bernoulli, multinomial)

- **Lemma 5c** (Minimax static tightening, single-shock) — `appendices/proofs.tex` §A.6
  - Status: full single-shock derivation; multi-shock extension as Remark in body
  - Caveat present: cooperative-overlap regime conservativeness (sequential counterfactual case is Lemma 5c-prime open work)

- **Lemma 5e** (Environment-side witness extension) — `appendices/proofs.tex` §A.8
  - Status: full proof via two codex review rounds (v1 → v2 → integrated)
  - Round A → v2 fixed: trust model not auto-transferring (added (C12.ENV-WIT) with sub-clauses); missing data-processing inequality step; Bernoulli/Poisson support conventions; $V_\mathrm{env}$ deployment-policy-derived (not theorem-fixed); reconciled $I_8$ vs deployment-tooling enumeration mismatch (dropped $\Delta r_K$ as strategy-dependent, added trusted-setup status)
  - Round B → integration-time edits applied: split (C12.TRUST) into TRUST-WRITE/TRUST-CORR; refined R2 to "and-condition" (only outside $V_\mathrm{env}$ AND no monitored shift); added (C12.CAL) for deployment-added variables; expanded (C5.SPRT) to cover environment-side LLR; added (C5.SUPP) environment-support clause
  - New conditions added to Theorem 1: (C12) environment-side witness instantiation [with sub-clauses (C12.PUB) published $V_\mathrm{env}$, (C12.PART) substrate partition, (C12.TRUST-WRITE) write-access exclusion, (C12.TRUST-CORR) failure-correlation exclusion, (C12.SETUP) trusted-setup honesty, (C12.CAL) per-variable calibration]
  - New Audit 8 in §8 deployment tooling: environment-side witness instantiation calibration (8-step procedure)
  - Lemma 5e inline statement promoted to use $V_\mathrm{env}$, with proof referencing §A.8

- **Lemma 6** ($h_{\mathrm{detect}}$ intensivity) — `appendices/proofs.tex` §A.7
  - Status: full proof via six codex review rounds (v1 → v6 → integrated)
  - Round A → v2 fixed integrated-vs-supremum $h_{\mathrm{detect}}$ definition (significant problem)
  - Round B → v3 fixed $T_{\mathrm{cascade}}$ as upper bound (it's a lower bound; introduced $\Tbeta$ SPRT detection quantile)
  - Round C → v4 fixed $\kappa$ scaling error ($\kappa \delta$ scales as $\delta^2$, not $\delta$)
  - Round D → v5 fixed factor-of-4 error in Hoeffding inversion (rigorous chain via squared lower bound)
  - Round E → v6 fixed $R$ vs $B$ range-width mismatch, (C5.IID) phrasing contradiction, empirical $\Ncasc$ sign error, bundled (C5.SPRT) sub-clauses
  - New conditions added to Theorem 1: (C5.SPRT) [with sub-clauses (C5.HOEFF) clipped LLR, (C5.MULT) channel multiplicity, (C5.IID) adapted increments, (C5.SUPP) finiteness], (C11) bounded gap-growth rate, (C11.CLK) clock comparability with calibrated probability
  - New Audit 7 in §8 deployment tooling: SPRT-applicability + gap-growth + clock calibration
  - Lemma 5d updated to union-class form (drops legacy $\beta'$); Lemma 4 updated with explicit $\Rh = b - a$ convention note
  - $I_{11}$ connection to (C11.CLK) noted in invariants section

## Items needing promotion to full proofs

### Lemma 2 (Lyapunov-Goodhart bridge)

- **Current state:** Inline outline in §4.3 with explicit $N_{\max}$ and $w_{\min}$ conditions added (Phase 1 fix).
- **Needs:** Formal Cauchy-Schwarz derivation with step-by-step bounds:
  - The per-dimension error decomposition
  - The application of Cauchy-Schwarz in the dual $w^{-1}$-weighted norm
  - Tight constant tracking
- **Recommended location:** Could stay inline if tightened; otherwise appendix.
- **Priority:** Medium — short proof, but it's the bridge between Paper 6 and Paper 9 machinery.

### Lemma 5a (Substrate floor)

- **Current state:** Inline sketch in §4.7. Asserts coercivity-style assumption ``each independent channel contributes a non-zero rate $\rho_0$ of cooperative novelty'' without formal derivation.
- **Needs:**
  - Formal statement of the coercivity assumption as an explicit named assumption (analogous to Paper 6's C1/C2 assumptions)
  - Proof of the $\binom{m^*}{2}$ scaling under additivity
  - Caveat treatment of sub-additivity in correlated-channel cases
- **Recommended location:** Body (with assumption named in §3 invariants section?).
- **Priority:** Medium-high — substrate-floor is invoked in Layer 1 proof Step 1.

### Lemma 5d (Lead-time tail composition)

- **Current state:** Inline sketch in §4.10. Composition of 5b + 4 is trivial.
- **Needs:** None substantive — the composition is direct.
- **Recommended location:** Stay inline.
- **Priority:** Low.

### ~~Lemma 5e (Environment-side witness extension)~~ DONE (2026-05-04)

- **Resolved:** Full proof in §A.8 (two-round codex review cycle).
  Theorem-level condition (C12.ENV-WIT) added with six sub-clauses
  (PUB / PART / TRUST-WRITE / TRUST-CORR / SETUP / CAL).
  Audit 8 added covering all calibration. (C5.SPRT) expanded for
  environment-side LLR. R2 refined to "and-condition" (manipulation
  outside $V_\mathrm{env}$ AND no monitored shift). $I_8$ enumeration
  reconciled (dropped $\Delta r_K$, added trusted-setup status).

## Theorem-level items needing formalization

### ~~$h_{\mathrm{detect}}$ in Layer 2~~ DONE (2026-05-04)

- **Resolved:** Lemma 6 (full proof in §A.7) supplies the formal
  intensivity argument.  (C5.SPRT), (C11), (C11.CLK) added to
  Theorem 1.  Audit 7 covers calibration.  Theorem 1 Layer 2 proof
  rewritten to use $\Tbeta$ instead of $T_{\mathrm{cascade}}$ as the
  integration horizon (the latter is a lower bound on cascade time,
  not an upper bound on $T_{\mathrm{detect}}$).  Six codex review
  rounds; final verdict integration-ready with two minor cleanups
  applied at integration time.

### Lipschitz-of-$g$ intensive condition

- **Current state:** Theorem 1 statement says $g$ has Lipschitz constant $\mathrm{Lip}(g)$; Lemma 1 proof notes ``the Lipschitz constant $\mathrm{Lip}(g)$ depends on the welfare functional $g$ and not on $|P|$ for any $g$ that is bounded in single-capability perturbations.'' This is an in-text assumption, not a theorem condition.
- **Needs:** Promote to explicit theorem condition (e.g., (C6) ``Bounded-Lipschitz alignment property'') so that the intensivity of the bound is conditional on $g$'s class.
- **Recommended location:** Theorem 1 statement.
- **Priority:** High — codex Q2 flagged this as the second hidden assumption.

### Paper 6 metastable-lifetime scaling-law qualification

- **Current state:** Lemma 4 appendix proof has a caveat noting that Paper 6 states $\tau_{\mathrm{meta}}$ as a scaling law, not a theorem-level bound. Theorem 1 Layer 2 uses it as a tail-bound floor.
- **Needs:** Either:
  - Promote Paper 6's scaling law to a theorem in a paired update, or
  - Explicit assumption in Theorem 1 (e.g., (C7) ``Cascade-time floor'': $\tau_{\mathrm{meta}} \geq C/I_k$ holds with operationally calibrated constants)
- **Recommended location:** Theorem 1 conditions.
- **Priority:** Medium-high.

## Cross-cutting items

### Definition gathering

The body has many definitions scattered across sections. Consider gathering them in a single ``Definitions'' subsection at the start of §4 or in an appendix definitions block, especially:
- Definition of $\Aadv$, $\Aadv^{\mathrm{env}}$ (currently in Lemma 5b/5e statements)
- Definition of cooperative-overlap regime (currently in Lemma 5c)
- Definition of joint/event-class failure-correlation independence (currently in §3 in $I_6'$)
- Definition of counterfactual shock-loss fraction (currently in Lemma 5c)

### Notation reconciliation drift

§2's notation table is comprehensive at the time of writing, but as Paper 10 evolves through Phase 2, new symbols may be introduced (e.g., $h_{\mathrm{static}}$, $h_{\mathrm{detect}}$, $\beta'$, $\Aadv^{\mathrm{env}}$). A pre-publication notation pass should ensure every symbol is either in the table or defined inline at first use.

## Phase-2 plan summary (post Lemma 1 integration, 2026-05-04)

In priority order:

1. ~~Promote Lemma 1 to full appendix proof~~ **DONE (2026-05-04).**
   Two codex review rounds: v1 → v2 → integrated.  Added (C6),
   (C7) (with explicit Assumption~\ref{ass:bounded_coev}), (C8) to
   Theorem 1.  New Audit 4 in §8 deployment-tooling for the
   bounded-co-evolution calibration hook.
2. ~~Add (C6) Bounded-Lipschitz alignment property and (C7)
   Cascade-time floor to Theorem 1.~~ **DONE.**  (C6) added with
   Lemma 1's integration.  (C7) was renamed during integration to
   "bounded co-evolution" since the cascade-time floor is now
   covered by Lemma 4's appendix caveat on Paper 6's metastable
   lifetime as scaling law.
3. ~~Tighten Lemma 2 inline proof~~ **DONE (2026-05-04).**  Two
   codex review rounds: v1 → v2 → integrated.  Round A caught
   Paper 9's relative-sup-norm definition mismatch; v2 added
   TF (truth floor) assumption.  (C9) added to Theorem 1 with
   sub-conditions BD/CL/WB/TF.  Audit 5 added to deployment tooling.
4. ~~Add Lemma 6 ($h_{\mathrm{detect}}$ intensivity)~~
   **DONE (2026-05-04).**  Six codex review rounds: v1 → v6 →
   integrated.  Each round caught a finer-grain error: definitional
   (Round A), structural (Round B), scaling (Round C), coefficient
   (Round D), range-width / phrasing (Round E).  V6 is integration-
   ready with sign-direction discipline, post-clipping drift floor,
   and bundled (C5.SPRT) sub-clauses.  Added (C5.SPRT) [HOEFF/MULT/
   IID/SUPP], (C11), (C11.CLK) to Theorem 1.  Audit 7 added to §8
   covering all SPRT-applicability + gap-growth + clock-calibration
   constants.  Lemma 5d generalized to union-class form; Lemma 4
   updated with $\Rh = b - a$ convention.
5. ~~Tighten Lemma 5a coercivity assumption + inline proof~~
   **DONE (2026-05-04).**  Two codex review rounds: v1 → v2 →
   integrated.  Round A caught Step 4's additivity error
   (conflated joint failure-correlation independence with
   cooperative-production independence); v2 added explicit
   superposition assumption (SU).  (C10) added to Theorem 1 with
   sub-clauses (C10.CN) and (C10.SU).  Audit 6 added to deployment
   tooling.
6. ~~Promote Lemma 5e environment-side KL floor derivation to
   appendix.~~ **DONE (2026-05-04).**  Two codex review rounds:
   v1 → v2 → integrated.  Added (C12.ENV-WIT) with six sub-clauses,
   Audit 8, expanded (C5.SPRT) for env-side coverage, refined R2.
7. Definition gathering / notation pass.
8. Re-run codex review on the tightened §1--6 before final publication.

Estimated remaining effort: 1.5--2 hours of focused work.

---

*Authored 2026-05-03 during the Phase 1 remediation pass following
codex's §1-6 checkpoint review. Items captured here should be
addressed in the Phase 2 pass before §1-10 is submitted for
adversarial review.*
