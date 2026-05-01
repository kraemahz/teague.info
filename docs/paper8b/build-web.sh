#!/usr/bin/env bash
# Build the Distill HTML version of Paper 8b (Need Sufficiency).
# Usage: ./build-web.sh
# Output: ../../public/papers/need-sufficiency/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/need-sufficiency"

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

# Resolve cross-references for Paper 8b (Need Sufficiency)
ref_map = {
    # Sections
    'sec:introduction': '1',
    'sec:companion_relationship': '1.2',
    'sec:dependencies': '1.3',
    'sec:need_sufficiency': '2',
    'sec:capability_stuffing': '2.4',
    'sec:threshold_setting': '2.5',
    'sec:gap_decomposition': '3',
    'sec:need_diagnostic': '3.3',
    'sec:wireheading': '4',
    'sec:residual_class': '5',
    'sec:worked_example': '6',
    'sec:integration': '7',
    'sec:discussion': '8',
    # Definitions
    'def:need_bundle': '1',
    'def:downstream_safe': '2',
    'def:polarity_boundary': '3',
    'def:polarity_benchmark': '4',
    'def:downstream_gate': '5',
    'def:s1_sufficiency': '6',
    'def:alarm': '7',
    'def:gap_decomp': '8',
    'def:nac': '9',
    'def:nse': '10',
    'def:trade_leverage': '11',
    'def:residual_class': '12',
    'def:oi_exercise_bridge': '13',
    # Propositions
    'prop:near_total_collapse': '1',
    'prop:need_dominance': '2',
    'prop:below_suff_saturation': '3',
    'prop:gap_computable': '4',
    'prop:combined_diagnostic': '5',
    'prop:wireheading_hhi': '6',
    'prop:third_party_wireheading': '7',
    'prop:residual_intersection': '8',
    'prop:oi_floor': '9',
    # Remarks
    'rem:reference_pathway': '1',
    'rem:exercise_pathway': '2',
    'rem:gate_candidates': '3',
    'rem:nondownstream_floor': '4',
    'rem:dominance_scale': '5',
    'rem:gate_comparison': '6',
    'rem:s1_sufficiency_failure': '7',
    'rem:s1_above': '8',
    'rem:s1_sufficiency_sourcing': '9',
    'rem:pointwise_not_aggregate': '10',
    'rem:alarm_interpretation': '11',
    'rem:residual_cell_irreducibility': '12',
    'rem:cell_cooperative_closure': '13',
    'rem:admissibility_external': '14',
    'rem:nac_upper_bound': '16',
    'rem:hhi_alarm_governance': '19',
    'rem:wireheading_part_b_obs': '21',
    'rem:residual_conservatism': '23',
    'rem:oi_bridge_scope': '25',
    # Open Questions
    'oq:threshold_governance': '1',
    'oq:need_identification': '2',
    'oq:capability_stuffing': '3',
    'oq:gap_decomp_closure': '4',
    'oq:oi_bridge': '5',
    'oq:attestation_protocol': '6',
    # Appendices
    'app:proofs': 'A',
    'app:notation': 'B',
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

html = re.sub(r'(?:in\s+)?Equations?\s*(?:--\s*)?(?=[:,\.\)a-z])', '', html)
html = re.sub(r'\(Equations?\s*\)', '', html)

html = ''.join(c for c in html if c in ('\n', '\r', '\t') or (ord(c) >= 0x20))

with open(sys.argv[2], 'w') as f:
    f.write(html)
" "$BODY_RAW" "$BODY_CLEAN"

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
    .definition, .lemma, .proposition, .corollary, .remark, .proof-env {
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
  "title": "Need-Sufficiency Architecture and Gap Diagnostics for the B-to-C Gap",
  "description": "Companion architecture to the Aggregate B-to-C Lower Bound. Supplies the structural condition that makes S1's below-sufficiency failure mode diagnosable: multi-dimensional need bundles with sufficiency thresholds, downstream-safe gates, and polarity-correct benchmarks. Decomposes the B-to-C gap into five cells (restricted, covered, dormant, residual, boundary-residual) under default literal-partition semantics, with a wireheading-consistent HHI concentration signal and a residual-class characterization re-cast from a measurement-apparatus question to a channel-reach question. A worked example traces the architecture end-to-end across four phases.",
  "authors": [
    {
      "author": "Teague Lasser",
      "authorURL": "https://teague.info",
      "affiliations": [{"name": "Subseq"}]
    },
    {
      "author": "Claude Opus 4.7 (1M context)",
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
  <h1>Need-Sufficiency Architecture and Gap Diagnostics for the B-to-C Gap</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/need-sufficiency/need-sufficiency.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
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
    cp "$PAPER_DIR/main.pdf" "$OUT_DIR/need-sufficiency.pdf"
    echo "PDF copied to $OUT_DIR/need-sufficiency.pdf"
fi

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
