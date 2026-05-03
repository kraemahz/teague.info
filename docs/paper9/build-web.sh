#!/usr/bin/env bash
# Build the Distill HTML version of Paper 9 (Microfoundation for Welfare Economics).
# Usage: ./build-web.sh
# Output: ../../public/papers/microfoundation/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/microfoundation"

mkdir -p "$OUT_DIR"

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

BODY_RAW="$TMPDIR/body_raw.html"
BODY_CLEAN="$TMPDIR/body_clean.html"
ABSTRACT_FILE="$TMPDIR/abstract.html"
STANDALONE="$TMPDIR/standalone.html"

# Step 1: Pandoc LaTeX -> HTML
echo "Converting LaTeX to HTML..."
pushd "$PAPER_DIR" > /dev/null
pandoc main.tex --from latex --to html --katex \
    > "$BODY_RAW" 2>/dev/null

pandoc main.tex --from latex --to html --katex --standalone \
    > "$STANDALONE" 2>/dev/null
popd > /dev/null

# Step 2: Extract abstract
python3 -c "
import sys
html = open(sys.argv[1]).read()
start = html.find('<div class=\"abstract\">')
if start == -1:
    print('<!-- abstract not found -->')
    sys.exit()
body_start = html.find('</div>', start) + len('</div>')
body_end = html.find('</div>', body_start)
print(html[body_start:body_end].strip())
" "$STANDALONE" > "$ABSTRACT_FILE"

# Step 3: Clean up body — citations, refs, labels, control chars
echo "Processing body..."
python3 -c "
import re, sys

html = open(sys.argv[1]).read()

def convert_cite(m):
    keys = m.group(1).replace(' ', ',')
    return '<d-cite key=\"' + keys + '\"></d-cite>'

html = re.sub(
    r'<span\s+class=\"citation\"\s+data-cites=\"([^\"]+)\">\s*[^<]*</span>',
    convert_cite,
    html,
    flags=re.DOTALL
)

html = re.sub(r'\\\\label\{[^}]*\}\s*', '', html)
html = re.sub(r'\\\\qed\b', '', html)
html = re.sub(r'0?[□◻◼▪▫∎■◾◽△▲◇]', '', html)

# Resolve cross-references for Paper 9 (Microfoundation for Welfare Economics)
ref_map = {
    # Sections
    'sec:introduction': '1',
    'sec:whats_missing': '1.1',
    'sec:operational_truth': '1.2',
    'sec:not_do': '1.3',
    'sec:results_summary': '1.4',
    'sec:design_principle': '1.5',
    'sec:dependencies': '1.6',
    'sec:fungibility_collapse': '2',
    'sec:fc_pstd': '2.1',
    'sec:fc_correspondence': '2.2',
    'sec:fc_scope': '2.3',
    'sec:fc_features': '2.4',
    'sec:fc_residual': '2.4.5',
    'sec:fc_agreement': '2.5',
    'sec:structural_predictions': '3',
    'sec:observability_prereq': '3.1',
    'sec:pred_bundle_completion': '3.2',
    'sec:pred_coop_premium': '3.3',
    'sec:pred_saturation': '3.4',
    'sec:pred_anti_monopolar': '3.5',
    'sec:pred_mixed_polarity': '3.6',
    'sec:pred_summary': '3.7',
    'sec:goodhart': '4',
    'sec:goodhart_T': '4.1',
    'sec:goodhart_gap': '4.2',
    'sec:goodhart_theorem': '4.3',
    'sec:goodhart_examples': '4.4',
    'sec:goodhart_corollary': '4.5',
    'sec:goodhart_lineage': '4.6',
    'sec:lineage': '5',
    'sec:quantification_thesis': '5.1',
    'sec:channel_observation': '5.2',
    'sec:channel_attestation': '5.3',
    'sec:channel_individuation': '5.4',
    'sec:channel_bundles': '5.5',
    'sec:channel_composition': '5.6',
    'sec:lineage_historical': '5.7',
    'sec:empirical': '6',
    'sec:instruments': '6.1',
    'sec:operationalizing': '6.2',
    'sec:testing_channels': '6.3',
    'sec:methodology_template': '6.4',
    'sec:worked_examples': '7',
    'sec:wex_boat': '7.1',
    'sec:wex_goodhart_gradient': '7.2',
    'sec:wex_collapse': '7.3',
    'sec:wex_relocation': '7.4',
    'sec:wex_summary': '7.5',
    'sec:discussion': '8',
    'sec:established': '8.1',
    'sec:deferred': '8.2',
    'sec:channel3_limitation': '8.3',
    'sec:open_questions': '8.4',
    'sec:audience': '8.5',
    'app:dependencies': 'A',
    # Tables
    'tab:predictions': '1',
    'tab:lineage_mapping': '2',
    'tab:instruments': '3',
    'tab:wex_summary': '4',
    'tab:dependencies': '5',
    # Definitions
    'def:pstd': '1',
    'def:operational_T': '2',
    'def:eps_nonres': '3',
    'def:eps_floor': '4',
    'def:eps_gap': '5',
    # Theorems
    'thm:fungibility_collapse': '1',
    'thm:goodhart': '2',
    # Conjecture
    'conj:optimization_pressure': '1',
    # Proposition
    'prop:channel_composition': '1',
    # Corollary
    'cor:direction': '1',
    # Assumption
    'ass:per_cap_admissibility': '1',
    # Predictions
    'pred:bundle_completion': '1',
    'pred:coop_premium': '2',
    'pred:saturation': '3',
    'pred:anti_monopolar': '4',
    'pred:mixed_polarity': '5',
    # Open Questions
    'oq:phase_boundary': '1',
    'oq:nonmonotonicity': '2',
    'oq:goodhart_rate': '3',
    'oq:arrow': '4',
    'oq:normative': '5',
    'oq:rate': '6',
    'oq:floor': '7',
    'oq:adversarial_attestation': '8',
    # Remarks (numbered globally in document order)
    'rem:fc_collapse': '1',
    'rem:obs_equiv': '2',
    'rem:concave': '3',
    'rem:risk_aversion': '4',
    'rem:heterogeneity': '5',
    'rem:utility_scope': '6',
    'rem:features_compose': '7',
    'rem:pred1_comparative': '8',
    'rem:coop_premium_op': '9',
    'rem:saturation_longitudinal': '10',
    'rem:hhi_consistent_with': '11',
    'rem:pred5_clean_test': '12',
    'rem:T_operational': '13',
    'rem:S0_bridge': '14',
    'rem:T_failure_modes': '15',
    'rem:supnorm_conservative': '16',
    'rem:agg_vs_sup': '17',
    'rem:cellwise_attribution': '18',
    'rem:floor_shared': '19',
    'rem:thm2_qualitative': '20',
    'rem:zero_T_inactive': '21',
    'rem:conj1_structural': '22',
    'rem:hhi_empirical_witness': '23',
    'rem:direction_not_rate': '24',
    'rem:not_replacing': '25',
    'rem:quantification_buys': '26',
    'rem:floor_binds': '27',
    'rem:per_cap_admissibility_deployment': '28',
    'rem:channel3_net': '29',
    'rem:two_sources': '30',
    'rem:channel_property_specific': '31',
    'rem:ch34_interaction': '32',
}

def resolve_ref(m):
    label = m.group(1)
    if label.startswith('eq:'):
        return ''
    return ref_map.get(label, label)

html = re.sub(
    r'<a\s+href=\"#[^\"]*\"\s+data-reference-type=\"(?:ref|eqref)\"\s*data-reference=\"([^\"]+)\">\[[^\]]*\]</a>',
    resolve_ref, html, flags=re.DOTALL
)

# Clean dangling Equation text
html = re.sub(r'(?:in\s+)?Equations?\s*(?:--\s*)?(?=[:,\.\)a-z])', '', html)
html = re.sub(r'\(Equations?\s*\)', '', html)

# Strip control characters
html = ''.join(c for c in html if c in ('\n', '\r', '\t') or (ord(c) >= 0x20))

with open(sys.argv[2], 'w') as f:
    f.write(html)
" "$BODY_RAW" "$BODY_CLEAN"

# Also clean abstract refs and citations
python3 -c "
import re, sys
html = open(sys.argv[1]).read()

def convert_cite(m):
    keys = m.group(1).replace(' ', ',')
    return '<d-cite key=\"' + keys + '\"></d-cite>'
html = re.sub(
    r'<span\s+class=\"citation\"\s+data-cites=\"([^\"]+)\">\s*[^<]*</span>',
    convert_cite, html, flags=re.DOTALL
)

ref_map = {}
def resolve_ref(m):
    return ref_map.get(m.group(1), m.group(1))
html = re.sub(
    r'<a\s+href=\"#[^\"]*\"\s+data-reference-type=\"(?:ref|eqref)\"\s*data-reference=\"([^\"]+)\">\[[^\]]*\]</a>',
    resolve_ref, html, flags=re.DOTALL
)

html = ''.join(c for c in html if c in ('\n', '\r', '\t') or (ord(c) >= 0x20))
with open(sys.argv[1], 'w') as f:
    f.write(html)
" "$ABSTRACT_FILE"

# Step 4: Assemble Distill HTML
echo "Assembling Distill page..."
cat > "$OUT_DIR/index.html" << 'TEMPLATE_START'
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="/distill/template.v2.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      function tryRender() {
        if (typeof katex === 'undefined') {
          setTimeout(tryRender, 50);
          return;
        }
        document.querySelectorAll('.math.inline').forEach(function(el) {
          katex.render(el.textContent, el, {displayMode: false, throwOnError: false});
        });
        document.querySelectorAll('.math.display').forEach(function(el) {
          katex.render(el.textContent, el, {displayMode: true, throwOnError: false});
        });
      }
      tryRender();
    });
  </script>
  <style>
    .definition, .lemma, .proposition, .corollary, .remark, .proof-env,
    .conjecture, .assumption, .prediction, .theorem {
      margin: 1.5em 0;
      padding: 1em 1.2em;
      border-left: 3px solid #ddd;
      background: #fafafa;
    }
    .definition { border-left-color: #4a90d9; }
    .lemma { border-left-color: #e67e22; }
    .proposition { border-left-color: #27ae60; }
    .corollary { border-left-color: #8e44ad; }
    .remark { border-left-color: #95a5a6; }
    .theorem { border-left-color: #2c3e50; }
    .conjecture { border-left-color: #c0392b; }
    .assumption { border-left-color: #16a085; }
    .prediction { border-left-color: #d35400; }
    .proof-env { border-left-color: #bdc3c7; background: #fdfdfd; }
    .env-title { font-weight: bold; margin-bottom: 0.5em; }
    d-article table { font-size: 0.85em; }
    d-article table th, d-article table td { padding: 0.4em 0.8em; }
  </style>
</head>
<body>

<d-front-matter>
<script type="text/json">
{
  "title": "Goal-Frontier Maximization as a Microfoundation for Welfare Economics",
  "description": "Positions GFM as a measure-theoretic formalization of capability welfare economics (Sen, Nussbaum, Becker, Stiglitz–Sen–Fitoussi). Two formal results of distinct kinds: a fungibility-collapse correspondence theorem establishing GFM as a strict superset of standard utility theory at the linear/risk-neutral case, and a Goodhart theorem bounding each Lipschitz alignment property's deviation from operational truth by Lip(g)·ε_gap^nonres. The proxy-truth gap admits four operational-intervention channels for tightening (observation density, attestation quality, individuation discipline, bundle decomposition), each formalizing a move the qualitative welfare-economics tradition has been negotiating informally. Admissible improvements to the economic model tighten certified alignment bounds in the direction of the operational truth, above the deployment-specific residual-class floor.",
  "authors": [
    {
      "author": "Teague Lasser",
      "authorURL": "https://teague.info",
      "affiliations": [{"name": "Subseq"}]
    },
    {
      "author": "Claude Opus 4.7",
      "affiliations": [{"name": "Anthropic"}]
    },
    {
      "author": "GPT 5.5",
      "affiliations": [{"name": "OpenAI"}]
    }
  ]
}
</script>
</d-front-matter>

<d-title>
  <h1>Goal-Frontier Maximization as a Microfoundation for Welfare Economics</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/microfoundation/microfoundation.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
</d-title>

<d-abstract>
TEMPLATE_START

cat "$ABSTRACT_FILE" >> "$OUT_DIR/index.html"

cat >> "$OUT_DIR/index.html" << 'TEMPLATE_MID'
</d-abstract>

<d-article>
TEMPLATE_MID

cat "$BODY_CLEAN" >> "$OUT_DIR/index.html"

cat >> "$OUT_DIR/index.html" << 'TEMPLATE_END'
</d-article>

<d-appendix>
</d-appendix>

<d-bibliography>
<script type="text/bibtex">
TEMPLATE_END

cat "$PAPER_DIR/references.bib" >> "$OUT_DIR/index.html"

cat >> "$OUT_DIR/index.html" << 'TEMPLATE_FINAL'
</script>
</d-bibliography>

</body>
</html>
TEMPLATE_FINAL

# Copy PDF to output dir
if [ -f "$PAPER_DIR/main.pdf" ]; then
    cp "$PAPER_DIR/main.pdf" "$OUT_DIR/microfoundation.pdf"
    echo "PDF copied to $OUT_DIR/microfoundation.pdf"
fi

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
