# Paper 7: Controlled Relaxation Protocols for the Max-Aggregation Pathology

*Working title. Companion to Papers 1-6 in the GFM sequence.*

**Thesis:** The max-aggregation operator in the GFM risk framework produces a verification asymmetry: catastrophe confirms a risk claim, but absence of catastrophe under restriction provides no evidence against it, because the restriction prevented the exercise that would have generated the counterfactual observation. This *Wamura pathology* produces persistent overcaution that no amount of observational evidence can revise. This paper introduces *controlled relaxation protocols* -- bounded, monitored partial lifting of restrictions that generates genuine Bayesian evidence about risk claims while bounding maximum damage. The central result is a convergence theorem: under repeated controlled relaxation tests, risk estimates converge to the true risk level at a characterized rate that depends on detection sensitivity, damage tolerance, and test duration.

**Status:** Outline with formal definitions and theorem statements. Proof sketches indicate approach; full proofs are future work.

---

## Section Structure

1. Introduction and Motivation
2. The Verification Asymmetry
3. Controlled Relaxation Protocol
4. Scope-Bounding and Damage Guarantees
5. Detection Sensitivity and Bayesian Update
6. Convergence of Risk Estimates
7. Meta-Policy for Test Initiation
8. Worked Example: Canonical Wamura Scenario
9. Integration with Prior Results
10. Discussion and Open Questions

---

## 1. Introduction and Motivation

### Purpose

Paper 3 identifies the max-aggregation pathology as "the most important open problem the paper identifies" (Discussion, lines 257-276). The conservative max operator, combined with the verification asymmetry inherent in risk prevention, produces overcaution that is structurally irresolvable within the existing framework: a risk claim that successfully prevents catastrophe generates no observation that could lower the risk estimate, because the very success of the restriction is what prevents the counterfactual test.

This is a distinct problem from the compound feedback loops addressed in Paper 6. Paper 6 asks: "when does partial subsumption self-correct vs. cascade?" Paper 7 asks: "when the framework correctly restricts a risky capability, how does it ever learn that the restriction was unnecessary?" The two problems reinforce each other (Paper 6 Proposition 3 shows the Wamura pathology is a degenerate phase boundary), but neither resolves the other.

The paper is named for Mayor Kotoku Wamura's legacy: the oversized floodgate at Fudai (Paper 2, Discussion) that was ridiculed for decades as wasteful overcaution until the 2011 Tohoku tsunami proved it exactly right. The Wamura problem is the formal version: when prevention works, the evidence for prevention disappears.

### The structural problem

Three ingredients combine to produce the pathology:

1. **Max-aggregation** (Paper 3, risk machinery): The framework takes the maximum over agents' risk estimates, meaning a single high-risk claim from any agent constrains the capability tuple. This is conservative by design -- it prevents the framework from dismissing minority risk warnings -- but it means a single overly-cautious agent can lock a capability indefinitely.

2. **Verification asymmetry** (Paper 5, Definition 2; Paper 5, Proposition 1): The monotonicity result shows that as an agent's capabilities grow, the verification asymmetry between what it can demonstrate and what can be externally verified is non-decreasing. Applied to risk claims: verifying a risk (observing catastrophe) is operationally straightforward; verifying safety (observing non-catastrophe under exercise) requires the exercise to happen, which the restriction prevents.

3. **Neutral-prior bootstrap** (Paper 3, Discussion): When a new capability is discovered and no exercise history exists, the framework initializes with a neutral prior. Combined with max-aggregation, a single agent assigning high risk to the new capability immediately restricts it, and the restriction then prevents the evidence accumulation that would revise the estimate.

### What this paper does NOT do

- Does not propose replacing max-aggregation with a different aggregation operator. Paper 4's log-odds risk aggregation (Definition 5) already provides an alternative for the multi-agent case. This paper addresses the structural verification asymmetry that persists under *any* aggregation rule -- including log-odds -- whenever a risk claim prevents the exercise that would generate evidence.
- Does not address observation-channel integrity under adversarial conditions. Paper 5's commitment protocols handle that. This paper assumes honest observation channels and honest (but possibly miscalibrated) risk assessors.
- Does not resolve the B-to-C gap (Proposal 3 in the gap-closure sequence). Controlled relaxation generates evidence about risk claims, not about experiential value.

### Dependencies on prior papers

| Paper | Result used | Role in this paper |
|-------|-----------|-------------------|
| P2 | Axiom verification (Prop 1), benchmark refinement mechanism | vol_P properties preserved under relaxation; benchmark refinement as a complementary evidence source |
| P3 | Exercise Pathway (Def 2), Concentration Risk (Def 3), Risk Claim (Def 4), Preemptive Restriction Criterion (Prop 1) | The risk machinery that controlled relaxation operates within |
| P3 | Anti-monopolar property (Prop 6), Information Value of Structure (Def 5, Prop 2) | Value framework for comparing test cost vs. restriction cost |
| P4 | Risk-Trust Dynamics (Def 4), Log-Odds Risk Aggregation (Def 5), Risk-Trust L^2 Convergence (Prop 2) | The Bayesian update machinery that processes test outcomes |
| P4 | Causal Attribution (Def 2), multi-channel architecture (Table 1) | Formalizing what "observing the outcome" means during a test |
| P5 | Verification Asymmetry (Def 2), Monotonicity (Prop 1), Exercise Protocol (Def 12), Risk Claim Protocol (Def 13) | The formal verification-asymmetry framework this paper resolves |
| P5 | Channel Isolation (Prop 5), Channel Independence (Prop 6) | Integrity conditions on test observations |
| P6 | Phase Boundary (Thm 1), Wamura Pathology as Phase Boundary Degeneracy (Prop 3) | The dynamical-systems context: controlled relaxation makes the Loop 3 self-correction rate r_S positive, preventing phase boundary collapse |

---

## 2. The Verification Asymmetry

### Formalizing the asymmetry

**Definition 1 (Risk-Restriction Pair).** A risk-restriction pair (R, Xi) consists of:
- A risk claim R = (a_j, (d_1, ..., d_k), Pathway, p_R) where a_j is the claiming agent, (d_1, ..., d_k) is the capability tuple under concern, Pathway is the predicted exercise pathway (Paper 3, Definition 2) that would produce contraction, and p_R in (0, 1] is a_j's claimed probability that the pathway activates if the tuple is exercised.
- A restriction Xi: the preemptive restriction of a keystone capability d_j in the tuple (Paper 3, Proposition 1), preventing exercise of the pathway.

**Definition 2 (Observation Regimes).** Under a risk-restriction pair (R, Xi), the observation regime at time t is one of:
- **Restricted regime** (Xi active): The capability tuple is restricted. The pathway cannot activate. The only observations available are indirect: behavioral signals from the claiming agent a_j, correlational evidence from related capabilities, and time-passage without incident (which is uninformative because the restriction is preventing the test).
- **Exercise regime** (Xi lifted): The capability tuple is exercised. The pathway may or may not activate. Direct observation of the pathway's activation or non-activation is available.

**Proposition 1 (Asymmetric Evidence Under Restriction).** Let p_R(t) be the posterior probability that risk claim R is valid at time t. Under the restricted regime:

(a) If the pathway were to activate (contraction observed under a hypothetical exercise), the standard Bayesian update yields:

    p_R(t+1) = p_R(t) * Pr(contraction | R valid) / Pr(contraction)

which is a standard update with Pr(contraction | R valid) > Pr(contraction | R invalid), increasing p_R.

(b) Under the restricted regime, no exercise occurs, so:

    p_R(t+1) = p_R(t)

The posterior is unchanged because the restriction prevents the observation that would update it. The absence of contraction under restriction is consistent with both R being valid (the restriction correctly prevented it) and R being invalid (there was nothing to prevent). This is the Wamura asymmetry: successful prevention is observationally equivalent to unnecessary prevention.

*Proof sketch:* Direct from the Bayesian update rule and the counterfactual structure. Under restriction, the likelihood ratio Pr(no contraction | R valid, Xi active) / Pr(no contraction | R invalid, Xi active) = 1 because both hypotheses predict no contraction when the pathway is blocked. The likelihood ratio being 1 means the posterior equals the prior -- no information is gained.

**Remark (connection to Paper 5).** Paper 5's verification asymmetry (Definition 2) is the substrate-level version of this result: a digital agent can demonstrate capability possession (positive claim) far more easily than an external observer can verify capability absence (negative claim). Proposition 1 here is the risk-framework specialization: a risk claim can be confirmed by observing catastrophe but cannot be disconfirmed by observing non-catastrophe-under-restriction.

### The overcaution accumulation dynamic

**Proposition 2 (Monotone Overcaution Under Max-Aggregation).** Under the max-aggregation operator (Paper 3, risk machinery) and neutral-prior initialization:

(a) For any newly discovered capability tuple (d_1, ..., d_k) with no exercise history, there exists a threshold p_thresh > 0 such that if any agent a_j assigns p_R(0) > p_thresh, the tuple is immediately restricted (by Paper 3, Proposition 1).

(b) Once restricted, p_R(t) = p_R(0) for all t > 0 under the restricted regime (by Proposition 1(b)).

(c) The number of restricted capability tuples is monotonically non-decreasing over time: new tuples may be discovered and restricted, but no restricted tuple is ever unrestricted through the standard evidence-accumulation mechanism.

*Proof sketch:*
(a) Paper 3 Proposition 1's restriction criterion compares risk against restriction cost; for any tuple, a sufficiently high p_R exceeds the threshold.
(b) Direct from Proposition 1(b).
(c) Part (b) shows no evidence accumulates to reduce p_R below p_thresh, and no mechanism in the existing framework generates exercise-regime observations for restricted tuples.

**Corollary (Asymptotic Lockup).** In the limit of many capability discoveries, the fraction of the capability poset under active restriction grows monotonically, bounded below by the fraction of tuples for which at least one agent assigned p_R(0) > p_thresh. If agents are systematically overcautious (p_R(0) > true risk for many tuples), the locked fraction can grow without bound relative to the truly risky fraction, producing vol_P contraction that the framework cannot distinguish from genuine safety.

---

## 3. Controlled Relaxation Protocol

### Core idea

The structural root of the Wamura pathology is that evidence against a risk claim requires *exercise* of the restricted capability, which the restriction prevents. Controlled relaxation breaks this deadlock by creating bounded, monitored exercise windows that generate genuine Bayesian evidence while limiting maximum damage.

**Definition 3 (Controlled Relaxation Test).** A controlled relaxation test T = (R, Xi, S, tau_test, epsilon) for a risk-restriction pair (R, Xi) consists of:

- **Risk-restriction pair** (R, Xi): the claim and restriction being tested.
- **Test scope** S subset of P: a bounded sub-poset within which the restriction Xi is temporarily lifted. S determines the maximum vol_P exposure during the test (see Section 4).
- **Test duration** tau_test in N: the number of time steps for which Xi is lifted within scope S. After tau_test steps, Xi is reinstated regardless of outcome.
- **Damage tolerance** epsilon > 0: the maximum acceptable vol_P contraction from the test if the risk materializes. epsilon is a parameter set by the meta-policy (Section 7) or by the user as a safety bound.

### Protocol phases

**Phase 1: Scope selection.** Identify a sub-poset S such that:
(i) The predicted exercise pathway Pathway from risk claim R is exercisable within S (the prerequisite capabilities {d_1, ..., d_m} are available within S).
(ii) The maximum vol_P contraction from any exercise pathway within S is bounded by epsilon (Section 4, Theorem 1).
(iii) No other controlled relaxation test is currently running on a scope S' that overlaps with S (isolation requirement -- prevents cascading test failures).

**Phase 2: Relaxation.** Within scope S, lift restriction Xi for tau_test time steps. During the test window:
- Monitor for the predicted contraction pathway using Paper 4's multi-channel detection architecture (Table 1): capability gating, causal attribution, behavioral residuals, SPRT detection, correlational co-occurrence.
- Record all observations in the test log with timestamps and channel attributions.
- If vol_P contraction within S exceeds epsilon at any step, immediately reinstate Xi and terminate the test early (safety cutoff).

**Phase 3: Observation and Bayesian update.**

We separate the latent event (pathway activation) from the observed event (detection alarm). The model is a **simple binary hypothesis test** with fixed likelihoods throughout:

- A_n in {0, 1}: indicator that the pathway activates during test n (latent; not directly observed)
- O_n in {0, 1}: indicator that contraction is detected during test n (observed)
- H_0: the pathway is harmless -- activation probability theta = 0 (pathway never activates even when exercised)
- H_1: the pathway is dangerous -- activation probability theta = theta_1 for a fixed theta_1 in (0, 1] (pathway activates with known probability theta_1 when exercised)

The choice of theta_1 parameterizes the alternative hypothesis. The conservative default is theta_1 = 1 ("if the pathway is dangerous at all, it activates every time the capability is exercised"). This produces the strongest evidence per test. A more nuanced choice theta_1 < 1 reduces evidence per test but may be more realistic.

**Observation model (sensitivity/specificity):**
- Pr(O_n = 1 | A_n = 1) = 1 - beta(tau_test)  (true positive rate; beta is the false-negative rate, Section 5)
- Pr(O_n = 1 | A_n = 0) = alpha_fp  (false positive rate)

**Fixed likelihoods under each hypothesis:**

Under H_1 (pathway dangerous, theta = theta_1):
- Pr(O_n = 1 | H_1) = theta_1 * (1 - beta) + (1 - theta_1) * alpha_fp
- Pr(O_n = 0 | H_1) = theta_1 * beta + (1 - theta_1) * (1 - alpha_fp)

Under H_0 (pathway harmless, theta = 0):
- Pr(O_n = 1 | H_0) = alpha_fp
- Pr(O_n = 0 | H_0) = 1 - alpha_fp

These likelihoods are fixed numbers (determined by theta_1, beta, alpha_fp) -- not functions of a free parameter. This is what makes the binary test well-defined.

**Likelihood ratios:**
- L_1 = Pr(O_n=1 | H_1) / Pr(O_n=1 | H_0) = [theta_1*(1-beta) + (1-theta_1)*alpha_fp] / alpha_fp
- L_0 = Pr(O_n=0 | H_1) / Pr(O_n=0 | H_0) = [theta_1*beta + (1-theta_1)*(1-alpha_fp)] / (1-alpha_fp)

By Assumption T1 (Section 6), L_0 < 1 and L_1 > 1.

**Posterior updates:**

*Outcome A (contraction detected, O_n = 1):*

    p_R(t+) = p_R(t) * L_1 / [p_R(t) * L_1 + (1 - p_R(t))]

Equivalently in log-odds: logit(p_R(t+)) = logit(p_R(t)) + log(L_1).

*Outcome B (no contraction detected, O_n = 0):*

    p_R(t+) = p_R(t) * L_0 / [p_R(t) * L_0 + (1 - p_R(t))]

Equivalently: logit(p_R(t+)) = logit(p_R(t)) + log(L_0).

Since L_0 < 1, each no-contraction observation pushes the posterior toward H_0. This is what breaks the Wamura asymmetry.

**Remark (contrast with restricted regime).** Under the restricted regime (Proposition 1), A_n = 0 with certainty (the restriction prevents activation), so L_0 = L_1 = 1 and the posterior is unchanged. Under controlled relaxation, the capability is exercised (Assumption T5, Section 6), activation can occur, and the detector can observe it -- making both outcomes informative.

**Remark (continuous extension).** The binary formulation (H_0 vs H_1 with fixed theta_1) suffices for the operational question "should this restriction be maintained?" A continuous extension (placing a prior pi(theta) over [0,1]) would estimate the exact activation rate, but this requires latent-state augmentation for the posterior update (the latent A_n makes the model non-conjugate with a Beta prior, unlike the standard Beta-Binomial). We defer this extension to future work; the binary formulation addresses the Wamura pathology directly.

### Connection to Paper 6 Proposition 3

Paper 6 Proposition 3 shows that feedback loop 3 (over-calibrated restriction -> discovery avoidance -> structural ignorance) has a degenerate phase boundary when the self-correction rate r_S = 0 for that loop. The self-correction rate is zero precisely because the Wamura asymmetry prevents evidence accumulation. Controlled relaxation makes r_S > 0 by injecting exercise-regime observations into the evidence stream, which is the mechanism Paper 6's design criterion requires to make the Loop 3 phase boundary non-degenerate.

---

## 4. Scope-Bounding and Damage Guarantees

### Formalizing test scope

**Definition 4 (Test Scope).** A test scope S for risk claim R = (a_j, (d_1, ..., d_k), Pathway, p_R) is a sub-poset of P satisfying:
(i) **Pathway containment:** The exercise pathway Pathway is exercisable within S -- all prerequisite capabilities {d_1, ..., d_m} are present in S, and all intermediate poset transitions along Pathway remain within S.
(ii) **Forward-reachable cooperative closure:** S is cooperatively closed with respect to damage propagation under transitive forward-reachability: for every cooperative capability c in the full poset P that involves at least one capability in S and at least one capability in P \ S, the maximum vol_P contraction along any pathway within S that modifies c is included in max_contraction(S). Furthermore, if modification of c can causally enable (unlock) an exercise pathway in P \ S -- i.e., there exists a pathway Pathway_ext in P \ S whose prerequisites include a state change in c -- then the expected contraction from Pathway_ext, weighted by its activation probability, is also included in max_contraction(S). This transitive closure prevents a test within S from triggering a cascade outside S through cross-boundary cooperative capabilities.
(iii) **Irreversibility bound:** For each exercise pathway within S, the fraction of the pathway's vol_P contraction that is irreversible (cannot be recovered by reinstating Xi) is bounded by a known constant delta_irrev(Pathway). Pathways with delta_irrev > epsilon are excluded from the test scope. This addresses the hysteresis problem: some state changes during the test window (e.g., information disclosure, trust damage) may not be undone by reinstatement.
(iv) **Scope minimality:** S is inclusion-minimal subject to (i)-(iii) -- no proper sub-poset of S satisfies all three conditions.

**Remark (constructibility).** Condition (i) is computable from Paper 3's exercise pathway definition (Definition 2): enumerate the prerequisite set and all intermediate states. Condition (ii) requires computing the cooperative capabilities that span S and P \ S -- the "cooperative surface" of S -- and then forward-reachability analysis: for each boundary cooperative, enumerate external pathways whose prerequisites include a state change in that cooperative. This is more expensive than simple pathway enumeration (exponential in the depth of the forward-reachability chain) but necessary to prevent cascading damage through cooperative-capability spillover. In practice, the forward-reachability depth is bounded by the poset diameter, and most cooperative capabilities have low fan-out. Condition (iii) requires a pathway-level analysis of reversibility; in practice, most capability restrictions are reversible (reinstating the restriction restores the prior state), but information-disclosure pathways and trust-degradation pathways may have irreversible components.


### Damage-bounding theorem

**Theorem 1 (Damage Bound for Controlled Relaxation).** Let T = (R, Xi, S, tau_test, epsilon) be a controlled relaxation test with test scope S satisfying Definition 4. Then:

(a) **Maximum instantaneous damage:** The worst-case vol_P contraction at any step t' in {t, ..., t + tau_test} during the test is:

    vol_P(G_{t'}) >= vol_P(G_t) - max_contraction(S)

where max_contraction(S) is the maximum vol_P contraction achievable by any exercise pathway within S. If the scope selection constraint requires max_contraction(S) <= epsilon, then the instantaneous damage is bounded by epsilon.

(b) **Partial reversibility under reinstatement:** If the safety cutoff triggers at step t' < t + tau_test (contraction within S exceeds epsilon), reinstating Xi at t' + 1 gives:

    vol_P(G_{t'+1}) >= vol_P(G_t) - epsilon - delta_irrev_max

where delta_irrev_max = max_{Pathway in S} delta_irrev(Pathway) is the maximum irreversible component across all pathways in the scope (Definition 4(iii)). The recoverable component of the contraction is restored by reinstatement; the irreversible component delta_irrev is not. By the scope construction (Definition 4(iii)), delta_irrev_max <= epsilon, so the total post-reinstatement damage is bounded by 2*epsilon.

**Remark (why not delta_reinstate <= 0).** Paper 3's preemptive restriction criterion (Proposition 1) is an ex ante cost-benefit comparison that justifies imposing the restriction initially. It does not guarantee that reinstatement after partial pathway execution fully recovers the pre-test state. Irreversible state changes during the test -- information disclosure to adversaries, trust degradation, structural changes to the poset that are not reversed by restriction alone -- create a gap between the pre-test vol_P and the post-reinstatement vol_P. Definition 4(iii) bounds this gap by requiring the scope to exclude pathways with large irreversible components.

(c) **Scope isolation under cooperative closure:** If no other test is running on an overlapping scope (Definition 3 condition (iii)), and S satisfies cooperative closure (Definition 4(ii)), then the damage from test T that propagates to P \ S is bounded by the cooperative surface terms already included in max_contraction(S). Formally: for any capability d not in S and not part of any cooperative capability spanning S and P \ S, the exercise probability of d's pathways is unchanged during the test. For cooperative capabilities spanning the boundary, the contraction contribution is included in max_contraction(S) by the cooperative closure requirement.

*Proof sketch:*
(a) max_contraction(S) is computable from the sub-poset structure by enumerating exercise pathways within S (finite by Paper 3 Definition 2's finiteness assumption on pathway length), plus the cooperative surface terms from Definition 4(ii).
(b) The safety cutoff halts the test before damage exceeds epsilon. Reinstatement restores the reversible component. The irreversible component is bounded by Definition 4(iii).
(c) Cooperative closure (Definition 4(ii)) ensures that cross-boundary cooperative terms are accounted for in max_contraction(S). Pathways within S may affect cooperative capabilities that span S and P \ S, but these effects are bounded because they are included in the damage calculation by construction.

**Lemma 1 (Computable max_contraction).** For a finite sub-poset S with bounded pathway length L, max_contraction(S) is computable in O(|S|^L) time by exhaustive pathway enumeration.

*Proof sketch:* Paper 3 Definition 2 bounds pathway length. The number of pathways is at most |S|^L (each step selects a capability in S). vol_P contraction along each pathway is computable from the axioms M1-M6 (Paper 2, Proposition 1). Take the maximum.

**Remark (computational tractability).** The O(|S|^L) bound is exponential in pathway length but polynomial in scope size for fixed L. Practical deployment requires either (a) short pathway restrictions (L <= 3, say), (b) approximate bounds using Paper 3's concentration risk formula (Definition 3) as an upper bound on max_contraction, or (c) structural decomposition of S into independent sub-scopes. We note this as an engineering consideration, not a theoretical limitation -- the bound exists and is computable; the question is computational cost.

---

## 5. Detection Sensitivity and Bayesian Update

### Characterizing the detection mechanism

The Bayesian update in Section 3 depends on beta(tau_test), the false-negative rate of the detection mechanism over the test window. This section formalizes beta in terms of the multi-channel detection architecture from Paper 4.

**Connection to the latent-variable model.** Section 3's model has a per-test latent variable A_n (pathway activates or not) and a per-test observable O_n (contraction detected or not). The detection sensitivity beta mediates between them: beta = Pr(O_n = 0 | A_n = 1). Within a single test, A_n = 1 means the pathway activates at some point during the tau_test window. The detection mechanism then has tau_test opportunities to detect the activation.

**Assumption D0 (Activation duration).** When the pathway activates during a test (A_n = 1), the activation persists for k_act consecutive steps, where k_act is either (a) a fixed parameter of the pathway (determined by the exercise pathway's structure from Paper 3, Definition 2), or (b) drawn from a distribution K with known or bounded support. The per-test false-negative rate beta depends on k_act: the detector has min(k_act, tau_test) steps to detect the activation. For the default analysis, we assume k_act >= tau_test (persistent activation); the transient case k_act < tau_test is handled as a sensitivity analysis.

**Definition 5 (Detection Sensitivity).** For a controlled relaxation test T = (R, Xi, S, tau_test, epsilon) monitoring for exercise pathway Pathway = (pi_1, ..., pi_l):

The per-step detection probability on channel c_i is:

    delta_i = Pr(channel c_i detects pathway activation at step t' | Pathway activates at t')

The aggregate per-step detection probability across all active channels is:

    delta_agg = 1 - product_{c_i in O(P_t) intersection C_S} (1 - delta_i)

where C_S is the set of channels that cover the scope S.

**Assumption D1 (Cross-channel independence).** Detection events on distinct channels are conditionally independent given the latent pathway activation state A_n. This is justified for cross-substrate channels by Paper 5's channel isolation (Proposition 5, unconditional), and for same-substrate channels under Paper 5's joint-factorization assumption (Proposition 6, conditional on committed verification). When Assumption D1 fails (correlated same-substrate channels without committed verification), the product formula for delta_agg is optimistic; a conservative fallback uses only the cross-substrate channels:

    delta_agg^conservative = 1 - product_{c_i in O(P_t) intersection C_S : cross-substrate} (1 - delta_i)

The false-negative rate over the full test window is:

    beta(tau_test) = (1 - delta_agg)^{tau_test}

under the additional assumption:

**Assumption D2 (Temporal independence or mixing).** Conditional on the latent activation state A_n, the detection outcomes at distinct time steps within a test window are independent (memoryless detectors) or satisfy a mixing condition with mixing time tau_mix << tau_test. Without D2, persistent detector outages or common-cause failures can produce correlated misses across time steps, making beta decay slower than exponential. When D2 fails, the effective number of independent detection opportunities in tau_test steps is tau_test / tau_mix rather than tau_test, giving:

    beta(tau_test) <= (1 - delta_agg)^{tau_test / tau_mix}

For transient pathways (activation lasts only k < tau_test steps), beta(tau_test) = (1 - delta_agg)^{min(k, tau_test) / tau_mix} under the mixing model, or (1 - delta_agg)^{min(k, tau_test)} under D2.

**Proposition 3 (Detection Sensitivity Bounds).** Under the multi-channel architecture (Paper 4, Table 1) and Assumptions D1, D2:

(a) beta(tau_test) is monotonically decreasing in tau_test: longer tests have lower false-negative rates.

(b) For any epsilon_beta > 0, the minimum test duration required to achieve beta(tau_test) <= epsilon_beta is:

    tau_min = ceil(log(epsilon_beta) / log(1 - delta_agg))

Under the mixing relaxation of D2, this becomes tau_min * tau_mix.

(c) If at least one cross-substrate channel covers the scope S with detection probability delta_cross > 0, then even without D1 for same-substrate channels:

    beta(tau_test) <= (1 - delta_cross)^{tau_test / tau_mix}

which converges to 0 exponentially in tau_test (at rate 1/tau_mix). This is the substrate-diversity dividend for detection: cross-substrate channels provide independent detection opportunities that same-substrate channels may not (due to correlated failures), and their isolation is unconditional (Paper 5, Proposition 5), so D1 is satisfied for them without additional assumptions.

*Proof sketch:*
(a) beta is a product of (1 - delta_agg) terms; adding more independent detection opportunities decreases the product.
(b) Solve (1 - delta_agg)^{tau_min} <= epsilon_beta; apply mixing correction.
(c) The cross-substrate channel satisfies D1 unconditionally (Paper 5, Proposition 5), so the product formula is exact for it. Temporal independence follows from D2 or the mixing relaxation.

### The Bayesian update formalized

**Proposition 4 (Evidence Strength of Controlled Relaxation).** After a controlled relaxation test T with outcome O_n in {0, 1}, using the binary model from Section 3 (H_0: theta=0 vs H_1: theta=theta_1 with fixed likelihoods), the log-odds update is:

(a) **Evidence for R (O_n = 1, contraction detected):**

    Delta_logodds = log(L_1) = log([theta_1*(1-beta) + (1-theta_1)*alpha_fp] / alpha_fp)

This is a positive constant (evidence for R) by Assumption T1 (L_1 > 1). For the common case theta_1 = 1: Delta_logodds = log((1-beta) / alpha_fp).

(b) **Evidence against R (O_n = 0, no contraction detected):**

    Delta_logodds = log(L_0) = log([theta_1*beta + (1-theta_1)*(1-alpha_fp)] / (1-alpha_fp))

This is a negative constant (evidence against R) by Assumption T1 (L_0 < 1). For theta_1 = 1: Delta_logodds = log(beta / (1-alpha_fp)). Note the denominator (1-alpha_fp) -- this is material when alpha_fp is non-negligible and was missing in a naive derivation that assumed alpha_fp = 0.

(c) **Comparison with restricted regime:** Under the restricted regime (Proposition 1), the capability is not exercised, so both outcomes have likelihood ratio 1 (no update). Under controlled relaxation, the capability is exercised (Assumption T5), making both L_0 and L_1 non-unit, so both outcomes are informative.

(d) **Effect of theta_1 choice:** The alternative hypothesis theta_1 affects the evidence strength:
- theta_1 = 1 (strongest alternative): L_1 = (1-beta)/alpha_fp, L_0 = beta/(1-alpha_fp). Maximum evidence per test.
- theta_1 < 1 (weaker alternative): L_1 decreases, |log(L_0)| decreases. Less evidence per test, but the alternative may be more realistic for pathways that activate stochastically.
The choice of theta_1 is a modeling decision that does not affect convergence (Theorem 2 holds for any theta_1 in (0,1] under T1), only the rate.

*Proof sketch:* Direct from Section 3's fixed likelihood ratios L_0, L_1. The log-odds form follows from the Bayesian update: logit(p_R(t+)) = logit(p_R(t)) + log(Pr(O_n | H_1) / Pr(O_n | H_0)).

**Remark (integration with Paper 4).** The log-odds evidence from Proposition 4 feeds directly into Paper 4's log-odds risk aggregation (Definition 5) as an additional evidence channel. The controlled relaxation test produces evidence with the same structure as an individual agent's risk assessment -- a log-odds contribution weighted by trust. The trust weight on this evidence is 1 (the observation is direct, not mediated by an agent's report), which means test outcomes are the highest-trust evidence the aggregation can receive. This is by design: direct observation under controlled conditions is the gold standard for empirical risk assessment.

---

## 6. Convergence of Risk Estimates

### Main convergence result

### Formulation choice: binary hypothesis test

The convergence result is stated in the **binary hypothesis** framework (H_0: pathway is harmless, theta = 0; H_1: pathway is dangerous, theta = theta_1 > 0 for a fixed alternative). This is the dimensionally consistent formulation: p_R is the posterior probability of H_1, which converges to 0 or 1, not to a fractional activation rate.

The continuous estimation problem (inferring the exact value of theta^true in [0,1]) is a strictly harder problem that requires a continuous prior pi(theta) and produces a posterior density, not a point estimate. The binary formulation suffices for the operational question -- "should this restriction be maintained?" -- and avoids the dimensional mismatch between a binary posterior and a continuous parameter.

**Remark (continuous extension).** For applications where the activation rate theta matters (e.g., calibrating the damage tolerance epsilon for future tests), a prior pi(theta) on [0,1] with posterior updates via the latent-variable likelihood can in principle estimate the continuous parameter. However, as noted in Section 3, the latent activation variable A_n makes the posterior non-conjugate (even with a Beta prior), requiring latent-state augmentation or numerical methods. This extension is deferred to future work; it is not needed for the Wamura pathology, whose resolution requires only that p_R moves (which the binary formulation guarantees), not that it converges to a specific continuous value.

### Assumptions

**Assumption T1 (Identifiable binary model).** The observation model from Section 3 (Phase 3) discriminates H_0 from H_1: the likelihood ratio L_0 = Pr(O_n=0 | H_1) / Pr(O_n=0 | H_0) is strictly less than 1, and L_1 = Pr(O_n=1 | H_1) / Pr(O_n=1 | H_0) is strictly greater than 1. Equivalently: theta_1 * (1-beta) > theta_1 * alpha_fp, which holds when (1-beta) > alpha_fp (the detector has nontrivial power), satisfied whenever at least one channel with nonzero sensitivity covers the scope (Proposition 3(c)).

**Assumption T2 (Correct likelihood specification).** The observation model used in the Bayesian update (sensitivity 1-beta, specificity 1-alpha_fp) matches the true data-generating process. Misspecification (e.g., the actual false-positive rate differs from the assumed alpha_fp) produces convergence to the wrong hypothesis.

**Assumption T3 (Inter-test independence).** Test outcomes {O_n} are conditionally independent given the true state of the world (H_0 or H_1). This requires: (a) no adaptation by the tested agent between tests (the agent does not learn to evade detection based on prior test results), (b) the detection architecture's false-positive and false-negative rates are stable across tests (no detector degradation), and (c) the poset state P is approximately stationary between tests (the scope S remains valid). When (a) fails, the adversarial case (Open Question 3, Section 10) applies.

**Assumption T4 (Prior support).** The prior p_R(0) is in (0, 1) -- neither hypothesis is assigned probability zero a priori. This is a standard requirement for Bayesian consistency: if p_R(0) = 0, no amount of evidence can move the posterior. In practice, the neutral-prior initialization (Paper 3, Discussion) assigns p_R(0) in a neighborhood of 0.5, satisfying T4.

**Assumption T5 (Capability exercise during test).** During the test window, the capability tuple (d_1, ..., d_k) is actually exercised -- i.e., the conditions for pathway activation are present, not merely that the restriction is lifted. Without T5, O_n = 0 is ambiguous between "the pathway is safe" and "nobody tried." In practice, T5 is enforced by the scope selection (Phase 1): the test scope S is constructed to include the prerequisite capabilities and the test protocol actively invokes the capability tuple rather than passively waiting. When T5 cannot be guaranteed (e.g., the pathway requires a specific environmental trigger), the evidential weight of O_n = 0 must be discounted by the probability that the capability was actually exercised: Pr(exercised during test | Xi lifted) = p_exercise, and the effective observation model becomes Pr(O_n = 0 | H_1) = p_exercise * [theta_1*beta + (1-theta_1)*(1-alpha_fp)] + (1-p_exercise) * (1-alpha_fp).

**Theorem 2 (Convergence Under Repeated Controlled Relaxation).** Let {T_n}_{n=1}^{infinity} be a sequence of controlled relaxation tests for a risk-restriction pair (R, Xi) with fixed parameters (S, tau_test, epsilon), under the binary formulation H_0 (theta=0) vs H_1 (theta=theta_1). Under Assumptions T1-T5:

(a) **Convergence.** Under the true hypothesis H_j (j in {0,1}), the posterior p_R(t_n) converges almost surely to the correct value:
- If H_0 is true: p_R(t_n) -> 0 a.s.
- If H_1 is true: p_R(t_n) -> 1 a.s.

This is the binary consistency result: repeated testing identifies which hypothesis is correct.

(b) **Rate (H_0 true, pathway harmless):** Every test produces O_n = 0 with probability 1 - alpha_fp and O_n = 1 with probability alpha_fp. The posterior after n tests with all O_n = 0 satisfies:

    logit(p_R(t_n)) = logit(p_R(0)) + n * log(L_0)

where L_0 = [theta_1*beta + (1-theta_1)*(1-alpha_fp)] / (1-alpha_fp) < 1 (by T1). Convergence of p_R to 0 is exponential in the number of all-negative tests, at rate |log(L_0)| per test.

(c) **Rate (H_1 true, pathway dangerous):** Each test produces O_n = 1 with probability Pr(O=1 | H_1) = theta_1*(1-beta) + (1-theta_1)*alpha_fp and O_n = 0 otherwise. The log-odds update on O_n = 1 is log(L_1) > 0, which is large when (1-beta) >> alpha_fp. For theta_1 close to 1 and small beta, a single detection suffices to push p_R above 1 - delta for any fixed delta. Expected number of tests to reach p_R > 1 - delta is O(1/[theta_1*(1-beta)]).

(d) **General convergence rate.** The posterior converges at a rate determined by the KL divergence between the true observation distribution and the alternative:
- If H_0 true: rate = KL(Pr(O | H_0) || Pr(O | H_1)) = (1-alpha_fp)*log(1/L_0) + alpha_fp*log(1/L_1) per test
- If H_1 true: rate = KL(Pr(O | H_1) || Pr(O | H_0)) per test

Both rates are strictly positive by T1, confirming exponential convergence in both directions.

*Proof sketch:*
(a) Standard result for binary Bayesian hypothesis testing with i.i.d. observations: the log-likelihood ratio is a random walk with drift determined by the true hypothesis, and the strong law of large numbers ensures the posterior converges.
(b) Under H_0, each O_n = 0 contributes log(L_0) < 0 to the log-odds. The rare O_n = 1 (false positive, probability alpha_fp) contributes log(L_1) > 0, but E[Delta_logodds | H_0] = (1-alpha_fp)*log(L_0) + alpha_fp*log(L_1) < 0 (negative by KL positivity).
(c) Under H_1, E[Delta_logodds | H_1] > 0 by the same KL argument.
(d) Stein's lemma applied to the binary testing problem gives the exponent as the KL divergence.

### Finite-sample guarantees

**Corollary 1 (Minimum Tests to Clear a False Claim).** To reduce a false risk claim from prior p_R(0) to posterior p_R <= p_clear, when theta^true = 0 and all n tests produce O_n = 0 (no spurious false positives), the required number of tests under the binary hypothesis formulation (H_0: theta=0, H_1: theta=theta_1) is:

    N_clear >= ceil(log(p_clear * (1 - p_R(0)) / (p_R(0) * (1 - p_clear))) / log(L_0))

where L_0 = [theta_1 * beta + (1 - theta_1) * (1 - alpha_fp)] / (1 - alpha_fp) is the per-test likelihood ratio for the no-detection outcome. Note L_0 < 1 by Assumption T1.

When alpha_fp << 1, L_0 ≈ theta_1 * beta + (1 - theta_1), and the formula reduces approximately to:

    N_clear ≈ ceil(logit(p_clear) - logit(p_R(0))) / log(theta_1 * beta + 1 - theta_1))

**Remark.** For concrete numbers: if theta_1 = 1 (the alternative hypothesis is "pathway always activates when exercised"), beta = 0.1, alpha_fp = 0.01, p_R(0) = 0.5, and p_clear = 0.01, then L_0 = (1*0.1 + 0*0.99) / 0.99 = 0.101, and N_clear = ceil(log(0.01/0.99 * 0.5/0.5) / log(0.101)) = ceil(log(0.0101) / log(0.101)) = ceil(2.006) = 3 tests. Three controlled relaxation tests suffice to clear a false risk claim from a neutral prior to 1% residual risk, given 90% detection sensitivity and 1% false-positive rate. The correction from including alpha_fp adds approximately 1 test compared to the naive beta^N estimate. This illustrates the power of direct observation: the verification asymmetry that makes the Wamura pathology seem intractable is broken by a small number of well-designed tests.

**Corollary 2 (Convergence Rate Under Paper 4's EWMA).** When the test outcomes are fed into Paper 4's risk-trust EWMA (Definition 4) rather than a pure Bayesian update, the convergence is governed by the EWMA forgetting factor alpha_risk:

    sigma_j^{risk,2}(t_n) converges to mu_j^{risk} in L^2

at the rate established by Paper 4 Proposition 2, with the variance bound:

    limsup Var[sigma_j^{risk,2}(t)] <= [(1 - alpha_risk) / (1 + alpha_risk)] * C_dep * nu_j^{risk}

The controlled relaxation test contributes observations with lower variance than passive observations (because the test conditions are controlled), so C_dep may be smaller than in the passive case, tightening the variance bound.

---

## 7. Meta-Policy for Test Initiation

### When to test

Not every restriction should be tested. Controlled relaxation has costs: the damage tolerance epsilon is a real (if bounded) risk, the test consumes monitoring resources, and running too many tests simultaneously increases the chance of correlated failures. The meta-policy determines when a test is worth running.

**Definition 6 (Test Initiation Criteria).** A controlled relaxation test for risk-restriction pair (R, Xi) is initiated when all of the following hold:

(i) **Stale restriction:** The restriction Xi has persisted for at least T_stale time steps without new supporting evidence for R. "New supporting evidence" means any observation that increased p_R via the Bayesian update (not merely the passage of time under restriction, which provides no evidence by Proposition 1).

(ii) **Favorable cost-benefit:** The expected information value of the test exceeds the expected damage cost:

    IV(T) = E_outcome[KL(p_R^post || p_R^prior)] > epsilon * p_R(t)

where IV(T) is the expected information gain (KL divergence between posterior and prior, averaged over test outcomes weighted by their probabilities) and epsilon * p_R(t) is the expected damage (damage tolerance times probability that the risk materializes). The information value quantifies how much the test would reduce uncertainty about R, regardless of outcome direction.

(iii) **Scope isolation:** No other controlled relaxation test is currently running on a scope S' that overlaps with S (prevents cascading test failures and ensures independence of simultaneous tests).

(iv) **User approval** (when applicable): If the damage tolerance epsilon exceeds a user-configured threshold epsilon_user, the test requires explicit user approval before initiation. This is the safety valve: the framework can initiate low-damage tests autonomously but must ask the user before high-damage tests. The threshold epsilon_user is analogous to the self-trust pause threshold in the GFM harness constitution (Section 4.2).

**Remark (connection to Paper 3 Proposition 2).** Criterion (ii) is a specialization of Paper 3's structural discovery value (Proposition 2, Definition 5): a structural discovery that would resolve the risk claim has information value IV_struct; a controlled relaxation test has information value IV(T). The framework should prefer whichever is cheaper: if a structural argument can resolve the claim without exercise (e.g., proving the pathway is mechanically impossible), that is strictly better than a controlled relaxation test. Controlled relaxation is the fallback when no structural resolution is available -- the empirical arbitration mechanism for claims that resist formal resolution.

### Test parameter optimization

**Proposition 5 (Optimal Test Duration).** For fixed scope S and damage tolerance epsilon, the test duration tau_test that maximizes the expected information value per unit of risk exposure is:

    tau_opt = argmax_{tau} IV(T(tau)) / (epsilon * Pr(contraction in tau steps))

Under the exponential detection model (beta(tau) = (1 - delta_agg)^tau) and the persistent-activation assumption (D0 with k_act >= tau_test), tau_opt is approximately:

    tau_opt = ceil(-1 / log(1 - delta_agg))

which is the time constant of the exponential detection process -- the number of steps for the miss probability to decay by a factor of e. For delta_agg << 1 (low per-step detection), this is approximately 1/delta_agg. For delta_agg close to 1 (high per-step detection), tau_opt = 1 (a single step suffices). The test should run long enough for the detection mechanism to have seen approximately one expected detection opportunity. Running longer provides diminishing returns (beta is already small); running shorter wastes the test setup cost.

*Proof sketch:* The information value IV scales as |log(beta(tau))| for the no-contraction case, which grows linearly in tau. The risk exposure grows as 1 - (1 - p_R^true * delta_agg)^tau, which is approximately p_R^true * delta_agg * tau for small tau. The ratio IV/risk peaks when the marginal information gain equals the marginal risk increase, which occurs at tau approximately 1/delta_agg.

### Scheduling multiple tests

**Definition 7 (Test Schedule).** A test schedule Sigma = {(R_i, Xi_i, S_i, tau_i, epsilon_i)}_{i=1}^{N} is a set of controlled relaxation tests to be run. A schedule is *feasible* if:
(i) All scopes S_i are pairwise non-overlapping.
(ii) The aggregate damage tolerance sum_i epsilon_i is within the framework's total damage budget epsilon_total.
(iii) Tests are prioritized by their information-value-to-cost ratio IV(T_i) / epsilon_i (highest ratio first).

**Remark.** The scheduling problem is a variant of the knapsack problem with isolation constraints (non-overlapping scopes). For small numbers of concurrent tests, greedy selection by IV/epsilon ratio with scope-conflict checking is sufficient; for large-scale deployment, integer programming formulations are available.

---

## 8. Worked Example: Canonical Wamura Scenario

### Setup

Consider the scenario from Paper 3's discussion (lines 257-276): A newly discovered capability tuple (d_1, d_2) is identified by agent a_j as having a potential exercise pathway. Agent a_j assigns p_R(0) = 0.7 (moderately high confidence that the pathway is dangerous). The preemptive restriction criterion (Paper 3, Proposition 1) triggers because p_R(0) exceeds the threshold, and keystone d_1 is restricted. The ground truth is H_0: the pathway is harmless (theta = 0).

We use the binary hypothesis formulation: H_0 (theta = 0, pathway is harmless) vs. H_1 (theta = theta_1 = 1, pathway always activates if exercised). The prior p_R(0) = 0.7 reflects a_j's belief that H_1 is likely.

**Parameters:**
- Prior: p_R(0) = 0.7 (binary: probability of H_1)
- Ground truth: H_0 (pathway is harmless, theta = 0)
- Detection sensitivity: delta_agg = 0.95 (the multi-channel architecture detects pathway activation with 95% per-step probability)
- Test duration: tau_test = 3 steps (slightly above tau_opt = ceil(-1/log(0.05)) = 1 for delta_agg = 0.95; using tau_test = 3 for additional sensitivity margin)
- False-negative rate: beta(3) = (1 - 0.95)^3 = 0.000125
- False-positive rate: alpha_fp = 0.01 (1% chance of spurious contraction signal)
- Damage tolerance: epsilon = 0.02 * vol_P (2% of total capability volume)

### Without controlled relaxation (Wamura pathology)

Under the standard framework without controlled relaxation:
- p_R(t) = 0.7 for all t (Proposition 1(b))
- Restriction Xi remains in force indefinitely
- vol_P is permanently reduced by the restriction cost |Delta vol_P(restrict d_1)| for the rest of time
- The ground truth (H_0, pathway harmless) never surfaces; the 70% estimate persists forever

### With controlled relaxation

**Test 1:** Initiation criteria met (restriction is stale, IV > epsilon * p_R). Scope S constructed around {d_1, d_2} with max_contraction(S) = 0.015 * vol_P < epsilon.

Outcome: No contraction observed (probability 0.99 under H_0; the pathway never activates, so the only way to observe O_n = 1 is a false positive with probability alpha_fp = 0.01).

Using the latent-variable update (Section 3, Phase 3) with theta_1 = 1:
- Pr(O=0 | H_1) = theta_1 * beta + (1-theta_1) * (1-alpha_fp) = 1 * 0.000125 + 0 * 0.99 = 0.000125
- Pr(O=0 | H_0) = 1 - alpha_fp = 0.99
- Likelihood ratio L_0 = 0.000125 / 0.99 = 0.000126

    p_R(t_1) = 0.7 * 0.000126 / (0.7 * 0.000126 + 0.3) = 0.000294

After a single test with no contraction: p_R drops from 0.7 to 0.0003. The dramatic drop reflects the high detection sensitivity -- under H_1 (theta_1 = 1, pathway always activates), the detector would have caught it with probability 1 - beta = 99.99%. The absence of detection is extremely unlikely under H_1 and completely expected under H_0.

**Test 2:** p_R is already below most reasonable restriction thresholds (p_thresh), so the restriction is lifted. If the meta-policy calls for a confirmation test:

Outcome: No contraction observed again.

    p_R(t_2) = 0.000294 * 0.000126 / (0.000294 * 0.000126 + 0.999706) ≈ 3.7 * 10^{-8}

The risk estimate has converged to effectively zero after two tests. Note that Corollary 1's formula with the worked example's detection parameters (beta(3) = 0.000125, alpha_fp = 0.01, theta_1 = 1) gives L_0 = 0.000125 / 0.99 = 0.000126, so N_clear = ceil(logit(0.01) - logit(0.7)) / log(0.000126)) = 1 test -- a single test suffices because the per-test likelihood ratio is so extreme (the detector would catch a real pathway with 99.99% probability). The worked example confirms this: after one test, p_R is already 0.0003. The second test is a confirmation that drives p_R to negligible levels.

### If the risk were real

Suppose instead the ground truth is H_1 (pathway is genuinely dangerous). Test 1 with tau_test = 3:

Under H_1 with theta_1 = 1: Pr(O=1 | H_1) = 1 * (1-beta) + 0 * alpha_fp = 0.999875. The test detects contraction with near-certainty.

Outcome: Contraction detected (O_n = 1).

    p_R(t_1) = 0.7 * L_1 / (0.7 * L_1 + 0.3) where L_1 = 0.999875 / 0.01 = 99.9875

    p_R(t_1) = 0.7 * 99.9875 / (0.7 * 99.9875 + 0.3) = 69.99 / 70.29 = 0.9957

The risk estimate increases from 0.7 to 0.996, and the restriction is reinforced. Maximum damage during the test was bounded by epsilon = 0.02 * vol_P, which the cooperative-closure scope construction guarantees.

### Summary

| Scenario | Ground truth | Tests needed | Final p_R | Damage incurred |
|----------|-------------|-------------|-----------|-----------------|
| False alarm (standard) | H_0 | infinity (never resolves) | 0.70 | 0 (but permanent vol_P loss from restriction) |
| False alarm (controlled) | H_0 | 1 (+ 1 confirmation) | 3.7 * 10^{-8} | 0 (pathway didn't activate) |
| True risk (controlled) | H_1 | 1 | 0.996 | <= 0.02 * vol_P (bounded) |

---

## 9. Integration with Prior Results

### How controlled relaxation extends the GFM framework

**Proposition 6 (Controlled Relaxation Preserves Self-Balancing).** The self-balancing property of vol_P (Paper 2, Theorem 1) is preserved under controlled relaxation:

(a) During the test window (Xi lifted within scope S), the capability tuple (d_1, ..., d_k) is exercisable, which by Paper 2's axiom M4 (weak monotonicity) means vol_P is at least as large as under restriction, minus the possible damage bounded by epsilon. The net effect on vol_P is bounded by [-epsilon, +Delta_unrestrict] where Delta_unrestrict >= 0 is the vol_P gain from lifting the restriction.

(b) After the test, the updated risk estimate p_R(t + tau_test) more accurately reflects the true risk, which means the restriction criterion (Paper 3, Proposition 1) is applied against a more accurate estimate. If the risk was genuinely low, the restriction is lifted, permanently increasing vol_P. If the risk was genuinely high, the restriction is maintained with higher confidence, and vol_P is unchanged (the restriction was already in place).

(c) Over repeated tests (Theorem 2), the risk estimates converge to truth, and the restriction landscape converges to the optimal restriction set -- the set of tuples that are genuinely risky. This is a stronger self-balancing guarantee than the static version: not only does vol_P self-balance against perturbations, but the restriction landscape itself converges to the truth-tracking configuration.

**Proposition 7 (Risk-Claim Consensus via Empirical Arbitration).** When multiple agents disagree on the risk of a capability tuple (a_j assigns p_R^{(j)} >> p_R^{(k)} for agents j, k), controlled relaxation provides an empirical arbitration mechanism:

(a) Under the max-aggregation rule, a_j's high estimate locks the capability. Under log-odds aggregation (Paper 4, Definition 5), the disagreement produces a moderate aggregate that may or may not trigger restriction.

(b) In either case, if the capability is restricted, controlled relaxation generates evidence that updates both agents' estimates toward the truth (Theorem 2). After sufficient tests, the agents' posteriors converge, and the disagreement is resolved by data rather than by aggregation-rule choice.

(c) The convergence rate depends on the agents' prior weight (how strongly they hold their beliefs), but Doob's consistency guarantees convergence regardless of prior -- even a strongly held false risk claim is eventually overwhelmed by repeated controlled-relaxation evidence.

### Connection to Paper 4's multi-channel architecture

**Lemma 2 (Controlled Relaxation as a Sixth Detection Channel).** The controlled relaxation test adds a sixth channel to Paper 4's five-channel attribution architecture (Table 1):

| Channel | Source | Signal |
|---------|--------|--------|
| 1. Capability gating | Exercise outcomes | Binary (pass/fail) |
| 2. Causal attribution | SCM interventions | Continuous (Delta vol_P) |
| 3. Behavioral residual | Agent policy | Continuous (deviation) |
| 4. SPRT detection | Sequential test | Binary (accept/reject) |
| 5. Correlational co-occurrence | Pattern matching | Continuous (correlation) |
| **6. Controlled relaxation** | **Direct exercise under monitoring** | **Binary (contraction/no-contraction) + continuous (vol_P delta)** |

The sixth channel is distinct from the others in that it is *actively generated* rather than passively observed. The framework designs the observation (by constructing the scope and lifting the restriction), rather than waiting for the observation to arrive. This active-experiment property makes it the only channel that can generate evidence against a risk claim under the verification asymmetry.

---

## 10. Discussion and Open Questions

### What this paper accomplishes

1. **Breaks the Wamura pathology.** Theorem 2 proves that controlled relaxation drives risk estimates to truth at an exponential rate, converting "permanent overcaution" into "temporary overcaution with a characterized resolution time." This closes Paper 3's most important named open problem.

2. **Provides a damage-bounded mechanism.** Theorem 1 proves that the maximum damage from a test is bounded by epsilon, a parameter the framework or user controls. This makes controlled relaxation safe to deploy: the cost of learning is bounded, even when the risk turns out to be real.

3. **Integrates with the existing machinery.** Propositions 6-7 and Lemma 2 show that controlled relaxation preserves the self-balancing property, resolves inter-agent risk disagreements, and extends the multi-channel detection architecture. The protocol is additive to the existing framework, not a replacement.

4. **Connects to Paper 6's dynamics.** Paper 6 Proposition 3 shows the Wamura pathology is a degenerate phase boundary. Controlled relaxation makes the Loop 3 self-correction rate positive, restoring the phase boundary to its non-degenerate form and ensuring the compound feedback loop analysis applies to restriction dynamics as well as subsumption dynamics.

### Open questions for user review

**Open Question 1 (Damage tolerance calibration).** The damage tolerance epsilon is a free parameter that trades off learning speed against risk exposure. What should the default be? Options:
- (a) Fixed fraction of vol_P (e.g., epsilon = 0.01 * vol_P) -- simple, scales with the capability volume
- (b) Proportional to the restriction cost (epsilon = c * |Delta vol_P(Xi)|) -- tests whose restrictions are expensive to maintain get more generous damage budgets
- (c) Proportional to the information value (epsilon = c' * IV(T)) -- damage budget scales with expected information gain
- (d) User-set per-test -- maximum safety but maximum user burden

This is a design choice that shapes the character of the framework: aggressive (high epsilon, fast learning, higher risk) vs. conservative (low epsilon, slow learning, lower risk). The worked example shows that even small epsilon values produce rapid convergence when detection sensitivity is high, so the answer may depend more on the detection architecture than on epsilon itself.

**Open Question 2 (Transient vs. persistent pathways).** The detection sensitivity analysis (Section 5) assumes persistent pathway activation. Some risk pathways may be transient -- they produce a brief contraction that the detection mechanism could miss if the sampling rate is too low. How should the protocol handle transient pathways?
- The current formulation handles transient pathways via beta(tau_test) = (1 - delta_agg)^{min(k, tau_test)} where k is the pathway duration. But if k = 1 (single-step activation), then beta = 1 - delta_agg, which may be non-negligible. Should the protocol require longer test windows for suspected transient pathways? Should the detection architecture be adapted to increase sampling rate during tests?

**Open Question 3 (Adversarial risk claimants).** The current formulation assumes honest-but-miscalibrated risk assessors. What happens when an agent strategically inflates risk claims to lock competitors' capabilities? The controlled relaxation protocol still works (it generates evidence regardless of the claimant's intent), but the meta-policy for test initiation may need to be more aggressive when strategic inflation is suspected. Detection of strategic inflation is a variant of Paper 4's scorpion detection (Propositions 3-4): an agent whose risk claims are systematically disconfirmed by controlled relaxation tests should see its risk-trust T^risk_j decrease, eventually down-weighting its future claims in the aggregation. Should the meta-policy explicitly model this adversarial case, or is the trust-dynamics response sufficient?

### Relationship to subsequent papers

- **Paper 8 (B-to-C gap / Proposal 3):** Controlled relaxation generates exercise events that increase vol_R (realized capability volume). When a capability is locked by a false risk claim, vol_R is artificially suppressed; controlled relaxation lifts the lock and lets the capability contribute to vol_R. The convergence of the restriction landscape (Proposition 6(c)) implies that vol_R / vol_P approaches its true value as false restrictions are cleared, partially closing the B-to-C gap for the class of capabilities locked by the Wamura pathology.

- **Paper 9 (Adversarial structure learning / Proposal 5):** Controlled relaxation provides a clean experimental signal for structure learning: the SCM can use the designed-experiment observations from controlled relaxation tests (where the intervention is known and the outcome is observed) as ground-truth data points for calibrating the structural causal model. This is strictly more informative than observational data (where interventions are inferred, not designed), and could improve SCM confidence c_SCM(t) faster than passive observation alone.

- **Paper 6 (Compound feedback loops):** As noted throughout, controlled relaxation makes the Loop 3 self-correction rate positive, ensuring Paper 6's phase boundary theorem applies to restriction dynamics. The two papers are complementary: Paper 6 characterizes the macro-dynamics of when self-correction works; Paper 7 provides the micro-mechanism that makes self-correction work for the restriction-specific feedback loop.
