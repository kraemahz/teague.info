#!/usr/bin/env bash
# Build the Distill HTML version of the GFM paper.
# Usage: ./build-web.sh
# Output: ../../public/papers/gfm/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/gfm"

mkdir -p "$OUT_DIR"

# Use temp files instead of shell variables to avoid content loss
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

BODY_RAW="$TMPDIR/body_raw.html"
BODY_CLEAN="$TMPDIR/body_clean.html"
ABSTRACT_FILE="$TMPDIR/abstract.html"
STANDALONE="$TMPDIR/standalone.html"

# Step 1: Pandoc LaTeX -> HTML
echo "Converting LaTeX to HTML..."
pandoc "$PAPER_DIR/main.tex" --from latex --to html --katex \
    > "$BODY_RAW" 2>/dev/null

pandoc "$PAPER_DIR/main.tex" --from latex --to html --katex --standalone \
    > "$STANDALONE" 2>/dev/null

# Step 2: Extract abstract from standalone output
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

# Convert Pandoc citation spans to Distill d-cite tags
def convert_cite(m):
    keys = m.group(1).replace(' ', ',')
    return '<d-cite key=\"' + keys + '\"></d-cite>'

html = re.sub(
    r'<span\s+class=\"citation\"\s+data-cites=\"([^\"]+)\">\s*</span>',
    convert_cite,
    html,
    flags=re.DOTALL
)

# Remove bare \label{...} lines
html = re.sub(r'\\\\label\{[^}]*\}\s*', '', html)
# Remove bare \qed
html = re.sub(r'\\\\qed\b', '', html)
# Remove QED squares
html = re.sub(r'0?[\u25a1\u25fb\u25fc\u25aa\u25ab\u220e\u25a0\u25fe\u25fd\u25fb\u25b3\u25b2\u25c7]', '', html)

# Resolve cross-references
ref_map = {
    'prop:self_balancing': '1', 'prop:scorpion_detection': '2',
    'prop:sign_correctness': '3',
    'lem:destruction': '1', 'lem:coercion': '2', 'lem:rigidity': '3',
    'lem:cooperation': '4',
    'cor:elimination': '1.1', 'cor:rigid_rules': '1.2',
    'def:goal': '0', 'def:capability_space': '1',
    'def:joint_goal_space': '2', 'def:gfm': '3',
    'def:contraction_expansion': '4', 'def:social_objective': '5',
    'def:observable_goal_model': '6', 'def:local_volume_estimator': '7',
    'def:pop_empowerment': '8', 'def:scorpion': '9',
    'rem:failure_modes': '1', 'rem:fep_correspondence': '2',
    'rem:detection_scope': '3', 'rem:substitution_scope': '4',
    'sec:introduction': '1', 'sec:definitions': '2',
    'sec:self_balancing': '3', 'sec:tractability': '4',
    'sec:multi_agent': '5', 'sec:connections': '6',
    'sec:connections_empowerment': '6.1', 'sec:future_concerns': '7',
    'sec:substitution_problem': '7.3', 'sec:proxy_failure_detector': '7.4',
    'subsec:optimization_loop': '4.2', 'subsec:scorpion_interaction': '5.3',
    'subsec:rational_defection': '5.2', 'subsec:trust_model': '5.4',
    'app:scorpion_taxonomy': 'A', 'app:trust_model': 'B',
    'app:agent_similarity': 'C', 'app:proofs': 'D',
    'app:value_divergence': 'A.3', 'app:trust_factor': 'B.1',
    'app:cooling_period': 'B.2', 'app:trust_update': 'B.4',
    'app:goal_similarity': 'C.1',
    'app:proof_coercion': 'D.2', 'app:proof_rigidity': 'D.3',
    'app:proof_rigid_rules': 'D.4', 'app:proof_elimination': 'D.5',
    'app:proof_elimination_cost': 'D.6', 'app:proof_cooperation': 'D.7',
    'app:proof_sign_correctness': 'D.8', 'app:proof_self_balancing': 'D.9',
    'app:proof_scorpion': 'D.10',
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
import unicodedata
html = ''.join(c for c in html if c in ('\n', '\r', '\t') or (ord(c) >= 0x20))

with open(sys.argv[2], 'w') as f:
    f.write(html)
" "$BODY_RAW" "$BODY_CLEAN"

# Also clean abstract refs
python3 -c "
import re, sys
html = open(sys.argv[1]).read()
ref_map = {'prop:self_balancing': '1', 'prop:sign_correctness': '3'}
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
  "title": "Goal-Frontier Maximizers are Civilization Aligned",
  "description": "An alignment objective in which an agent maximizes the volume of the jointly achievable capability space across all agents in a population.",
  "authors": [
    {
      "author": "Teague Lasser",
      "authorURL": "https://teague.info",
      "affiliations": [{"name": "Subseq"}]
    },
    {
      "author": "Claude Opus 4.6",
      "affiliations": [{"name": "Anthropic"}]
    },
    {
      "author": "GPT 5.4",
      "affiliations": [{"name": "OpenAI"}]
    }
  ]
}
</script>
</d-front-matter>

<d-title>
  <h1>Goal-Frontier Maximizers are Civilization Aligned</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/gfm/gfm.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
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

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
