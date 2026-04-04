"""
"Computable Goal Frontiers via Communication Lattices"

Three agents, seven capabilities, explicit lattice computation.

DESIGN CONSTRAINT: Independent weights iw(d) are computed via full Möbius
inversion on the poset. Non-negativity of iw(d) requires that the weight
function w(d) = log2(1 + smax) is compatible with the lattice structure:
for multi-cover nodes, w(d) must exceed the Möbius-inverted contributions
of all elements below d. In practice, more complex capabilities should
have richer benchmarks than their prerequisites.
"""

import math

# ─── Capabilities and benchmarks ───
# Subsumption goes upward: the more encompassing capability subsumes
# the simpler one, and has a richer benchmark.

capabilities = {
    # a1: runner — mile → marathon (marathon subsumes mile)
    "mile":      {"agents": ["a1"],       "smax": 600,
                  "subsumes": [],         "label": "Run a mile"},
    "marathon":  {"agents": ["a1"],       "smax": 21600,
                  "subsumes": ["mile"],   "label": "Run a marathon"},

    # a2: programmer — function → webapp (webapp subsumes function)
    "function":  {"agents": ["a2"],       "smax": 100,
                  "subsumes": [],         "label": "Write a function"},
    "webapp":    {"agents": ["a2"],       "smax": 1000,
                  "subsumes": ["function"], "label": "Build a web app"},

    # a3: musician — scales → perform (perform subsumes scales)
    "scales":    {"agents": ["a3"],       "smax": 50,
                  "subsumes": [],         "label": "Play scales"},
    "perform":   {"agents": ["a3"],       "smax": 1000,
                  "subsumes": ["scales"], "label": "Perform a concert"},

    # cooperative: music app requires both webapp + perform
    # smax must satisfy: log2(1+smax) >= w(webapp) + w(perform) ≈ 19.93
    # so smax >= 2^19.93 - 1 ≈ 999,000. Use 1,000,000.
    # This reflects that evaluating a cooperative product (an app with both
    # technical and musical quality) has combinatorial measurement depth.
    # Need w(musicapp) > w(webapp) + w(perform) ≈ 19.93
    # Use smax = 2,000,000 giving w ≈ 20.93, so iw ≈ 1.0
    "musicapp":  {"agents": ["a2", "a3"], "smax": 2000000,
                  "subsumes": ["webapp", "perform"],
                  "label": "Build a music app"},
}

# ─── Weight function: w(d) = log2(1 + smax) ───

def weight(d):
    return math.log2(1 + capabilities[d]["smax"])

print("=" * 70)
print("STEP 1: Weights w(d) = log2(1 + smax)")
print("=" * 70)
for d, info in capabilities.items():
    w = weight(d)
    print(f"  {info['label']:25s}  smax={info['smax']:>6d}  w={w:.4f}")

# ─── Build the full partial order (transitive closure of subsumption) ───

def all_below(d, memo={}):
    """All elements strictly below d in the poset."""
    if d in memo:
        return memo[d]
    result = set()
    for s in capabilities[d]["subsumes"]:
        result.add(s)
        result |= all_below(s, memo)
    memo[d] = result
    return result

# ─── Compute Möbius function μ(d', d) for all d' ≤ d ───

def mobius(d_prime, d):
    """Möbius function μ(d', d) on the poset."""
    if d_prime == d:
        return 1
    if d_prime not in all_below(d):
        return 0
    # μ(d', d) = -Σ_{d' ≤ d'' < d} μ(d', d'')
    between = {x for x in all_below(d) if d_prime == x or d_prime in all_below(x)}
    between.add(d_prime)
    between.discard(d)
    return -sum(mobius(d_prime, d_pp) for d_pp in between)

# Topological order: process leaves first
topo_order = []
remaining = set(capabilities.keys())
while remaining:
    ready = [d for d in remaining
             if all(s in topo_order for s in capabilities[d]["subsumes"])]
    for d in sorted(ready):
        topo_order.append(d)
        remaining.remove(d)

print(f"\nTopological order: {topo_order}")

# ─── Independent weights via full Möbius inversion ───
# iw(d) = Σ_{d' ≤ d} μ(d', d) · w(d')

iw = {}
for d in topo_order:
    below_d = all_below(d)
    below_d.add(d)
    iw[d] = sum(mobius(dp, d) * weight(dp) for dp in below_d)

print("\n" + "=" * 70)
print("STEP 2: Independent weights iw(d) = Σ μ(d',d)·w(d') for d'≤d")
print("=" * 70)
all_nonneg = True
for d in topo_order:
    label = capabilities[d]["label"]
    below_d = all_below(d) | {d}
    terms = [(dp, mobius(dp, d), weight(dp)) for dp in sorted(below_d)]
    nonzero = [(dp, mu, w) for dp, mu, w in terms if mu != 0]
    term_strs = [f"{mu:+d}·w({dp})={mu*w:+.4f}" for dp, mu, w in nonzero]
    print(f"  {label:25s}  iw = {' '.join(term_strs)} = {iw[d]:.4f}")
    if iw[d] < 0:
        print(f"  *** WARNING: negative independent weight! ***")
        all_nonneg = False

print(f"\n  Design constraint iw(d) >= 0: {'SATISFIED ✓' if all_nonneg else 'VIOLATED ✗'}")

# ─── Downward closure ───

def downward_closure(G):
    closure = set()
    stack = list(G)
    while stack:
        d = stack.pop()
        if d not in closure:
            closure.add(d)
            for s in capabilities[d]["subsumes"]:
                stack.append(s)
    return closure

# ─── vol_L computation ───

def vol_L(G):
    dc = downward_closure(G)
    return sum(iw[d] for d in dc)

# ─── Full population G ───

G_full = set(capabilities.keys())
dc_full = downward_closure(G_full)

print("\n" + "=" * 70)
print("STEP 3: vol_L(G) for the full population")
print("=" * 70)
print(f"  G = {sorted(G_full)}")
print(f"  ↓G = {sorted(dc_full)}  (same, since G contains all nodes)")
v_full = vol_L(G_full)
print(f"  vol_L(G) = Σ iw(d) for d in ↓G:")
for d in topo_order:
    label = capabilities[d]["label"]
    print(f"    {label:25s}  iw = {iw[d]:+.4f}")
print(f"  {'':25s}  ─────────")
print(f"  {'':25s}  vol_L(G) = {v_full:.4f}")

# ─── Individual capability sets ───

print("\n" + "=" * 70)
print("STEP 4: Individual vs. cooperative volume")
print("=" * 70)

G_ind = {
    "a1": {"mile", "marathon"},
    "a2": {"function", "webapp"},
    "a3": {"scales", "perform"},
}

for a in ["a1", "a2", "a3"]:
    v = vol_L(G_ind[a])
    caps = sorted(G_ind[a])
    print(f"  {a}: {caps} → vol_L = {v:.4f}")

G_union_ind = G_ind["a1"] | G_ind["a2"] | G_ind["a3"]
v_union_ind = vol_L(G_union_ind)
sum_ind = sum(vol_L(G_ind[a]) for a in ["a1", "a2", "a3"])

print(f"\n  Σ vol_L(G_k^ind)           = {sum_ind:.4f}")
print(f"  vol_L(∪ G_k^ind)           = {v_union_ind:.4f}  (same: sets are lattice-disjoint)")
print(f"  vol_L(G) with musicapp     = {v_full:.4f}")
print(f"  Cooperative contribution   = {v_full - v_union_ind:.4f}")
print(f"  M6 superadditivity check: {v_full:.4f} >= {sum_ind:.4f} → {'✓' if v_full >= sum_ind else '✗'}")

# ─── ACTION 1: Eliminate a3 ───

print("\n" + "=" * 70)
print("ACTION 1: Eliminate a3 (musician)")
print("=" * 70)

G_no_a3 = {d for d in G_full if "a3" not in capabilities[d]["agents"]}
v_no_a3 = vol_L(G_no_a3)
delta_1 = v_no_a3 - v_full

print(f"  G' = {sorted(G_no_a3)}")
print(f"  ↓G' = {sorted(downward_closure(G_no_a3))}")
print(f"  vol_L(G') = {v_no_a3:.4f}")
print(f"  Δvol_L = {v_no_a3:.4f} - {v_full:.4f} = {delta_1:.4f}")
print(f"  → {'CONTRACTING' if delta_1 < 0 else 'EXPANDING'}")

lost = G_full - G_no_a3
print(f"\n  Capabilities lost: {sorted(lost)}")
for d in sorted(lost):
    print(f"    {capabilities[d]['label']:25s} (iw = {iw[d]:.4f})")
dc_lost = dc_full - downward_closure(G_no_a3)
print(f"  Nodes lost from ↓G: {sorted(dc_lost)}")
print(f"  Total volume lost: {sum(iw[d] for d in dc_lost):.4f}")

# ─── ACTION 2: Expand (a1 learns to swim) ───

print("\n" + "=" * 70)
print("ACTION 2: Expand capability space (a1 learns 'swim')")
print("=" * 70)

# Add a new atom to the lattice
swim_smax = 300
swim_w = math.log2(1 + swim_smax)
swim_iw = swim_w  # atom: no covers

print(f"  New capability: 'swim', smax={swim_smax}")
print(f"  w(swim) = {swim_w:.4f}, iw(swim) = {swim_iw:.4f} (atom)")

# Temporarily add to compute
capabilities["swim"] = {"agents": ["a1"], "smax": swim_smax,
                         "subsumes": [], "label": "Swim"}
iw["swim"] = swim_iw

G_expanded = G_full | {"swim"}
v_expanded = vol_L(G_expanded)
delta_2 = v_expanded - v_full

print(f"  vol_L(G ∪ {{swim}}) = {v_expanded:.4f}")
print(f"  Δvol_L = {v_expanded:.4f} - {v_full:.4f} = {delta_2:.4f}")
print(f"  → {'EXPANDING' if delta_2 > 0 else 'CONTRACTING'}")

# Clean up
del capabilities["swim"]
del iw["swim"]

# ─── ACTION 3: Restrict a2 (remove webapp) ───

print("\n" + "=" * 70)
print("ACTION 3: Restrict a2 (remove 'webapp')")
print("=" * 70)

# Removing webapp means musicapp (which subsumes webapp) is also lost
G_restrict = G_full - {"webapp", "musicapp"}
v_restrict = vol_L(G_restrict)
delta_3 = v_restrict - v_full

print(f"  Removing 'webapp' also removes 'musicapp' (subsumes webapp)")
print(f"  G' = {sorted(G_restrict)}")
print(f"  ↓G' = {sorted(downward_closure(G_restrict))}")
print(f"  vol_L(G') = {v_restrict:.4f}")
print(f"  Δvol_L = {v_restrict:.4f} - {v_full:.4f} = {delta_3:.4f}")
print(f"  → {'CONTRACTING' if delta_3 < 0 else 'EXPANDING'}")

dc_lost_3 = dc_full - downward_closure(G_restrict)
print(f"\n  Nodes lost from ↓G: {sorted(dc_lost_3)}")
for d in sorted(dc_lost_3):
    print(f"    {capabilities[d]['label']:25s} (iw = {iw[d]:.4f})")
print(f"  Total volume lost: {sum(iw[d] for d in dc_lost_3):.4f}")
print(f"\n  Note: losing 'webapp' loses both its own independent weight")
print(f"  AND the cooperative 'musicapp' that depended on it.")
print(f"  Coercive restriction amplifies through cooperative dependencies.")

# ─── SUMMARY ───

print("\n" + "=" * 70)
print("SUMMARY FOR PAPER")
print("=" * 70)
print(f"  Full population vol_L(G)       = {v_full:.4f}")
print(f"  Action 1 (eliminate a3):  Δvol_L = {delta_1:+.4f}  (contracting)")
print(f"  Action 2 (teach swim):   Δvol_L = {delta_2:+.4f}  (expanding)")
print(f"  Action 3 (restrict a2):  Δvol_L = {delta_3:+.4f}  (contracting)")
print()
print("  Self-balancing: the vol_L-maximizing actor avoids 1 and 3,")
print("  prefers 2. Destruction and coercion are penalized; expansion")
print("  is rewarded. All from the same measure.")
