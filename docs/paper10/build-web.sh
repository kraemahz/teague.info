#!/usr/bin/env bash
# Build the Distill HTML version of Paper 10 (GFM Provably Safe Deployment).
# Usage: ./build-web.sh
# Output: ../../public/papers/provably-safe/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/provably-safe"

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

# Resolve cross-references for Paper 10 (Provably Safe Deployment)
ref_map = {
    # Sections
    'sec:introduction': '1',
    'sec:setting': '1.1',
    'sec:problem': '1.2',
    'sec:wrong_frame': '1.3',
    'sec:composition': '1.4',
    'sec:claim_preview': '1.5',
    'sec:substrate_preview': '1.6',
    'sec:scope': '1.7',
    'sec:roadmap': '1.8',
    'sec:composition_setup': '2',
    'sec:source_blocks': '2.1',
    'sec:intensive_extensive': '2.2',
    'sec:notation': '2.3',
    'sec:composition_challenges': '2.4',
    'sec:paper10_new': '2.5',
    'sec:invariants': '3',
    'sec:dynamical_invariants': '3.1',
    'sec:empirical_invariants': '3.2',
    'sec:substrate_invariants': '3.3',
    'sec:anchoring_invariants': '3.4',
    'sec:invariants_table': '3.5',
    'sec:conjecture_audit': '3.6',
    'sec:lemmas': '4',
    'sec:lem1': '4.1',
    'sec:lem2': '4.2',
    'sec:lem3': '4.3',
    'sec:lem4': '4.4',
    'sec:lem5_family': '4.5',
    'sec:lem5a': '4.6',
    'sec:lem5b': '4.7',
    'sec:lem5c': '4.8',
    'sec:lem5d': '4.9',
    'sec:lem5e': '4.10',
    'sec:lem6': '4.11',
    'sec:lem_composition': '4.12',
    'sec:main_theorem': '5',
    'sec:theorem_statement': '5.1',
    'sec:proof_layer1': '5.2',
    'sec:proof_layer2': '5.3',
    'sec:proof_layer3': '5.4',
    'sec:theorem_establishes': '5.5',
    'sec:theorem_does_not': '5.6',
    'sec:substrate_anchoring': '6',
    'sec:tripartite': '6.1',
    'sec:cooperative_anchoring': '6.2',
    'sec:evasions': '6.3',
    'sec:asymmetric_capture': '6.3.1',
    'sec:cooperative_forking': '6.3.2',
    'sec:time_asymmetry': '6.3.3',
    'sec:weaker_c4': '6.4',
    'sec:destabilizing_cascade': '6.5',
    'sec:section_scope': '6.6',
    'sec:conjecture_op': '7',
    'sec:conditional_structure': '7.4',
    'sec:deployment_tooling': '8',
    'sec:tooling_verification': '8.1',
    'sec:tooling_substrate_audits': '8.2',
    'sec:tooling_concgap_structural': '8.3',
    'sec:tooling_channels': '8.4',
    'sec:tooling_anchoring': '8.5',
    'sec:tooling_training': '8.6',
    'sec:tooling_correction': '8.7',
    'sec:tooling_workflow': '8.8',
    'sec:worked_scenarios': '9',
    'sec:scenario_clean': '9.1',
    'sec:scenario_violations': '9.2',
    'sec:scenario_coalition': '9.3',
    'sec:scenario_audit': '9.4',
    'sec:scenarios_establish': '9.5',
    'sec:discussion': '10',
    'sec:disc_establishes': '10.1',
    'sec:disc_sensitivity': '10.2',
    'sec:disc_alignment': '10.3',
    'sec:disc_related': '10.4',
    'sec:disc_companion': '10.5',
    'sec:disc_indefinite': '10.6',
    'sec:disc_significance': '10.7',
    # Appendices
    'app:proofs': 'A',
    'app:proof_lem1': 'A.1',
    'app:proof_lem2': 'A.2',
    'app:proof_lem4': 'A.3',
    'app:proof_lem5a': 'A.4',
    'app:proof_lem5b': 'A.5',
    'app:proof_lem5c': 'A.6',
    'app:proof_lem5e': 'A.7',
    'app:proof_lem6': 'A.8',
    'app:notation': 'B',
    # Tables
    'tab:invariants': '1',
    # Theorem
    'thm:deployment_safety': '1',
    # Assumption
    'ass:concgap_conditions': '1',
    # Lemmas (numbered globally)
    'lem:1': '1',
    'lem:2': '2',
    'lem:3_forward': '3',
    'lem:4': '4',
    'lem:5a': '5a',
    'lem:5b': '5b',
    'lem:5c': '5c',
    'lem:5d': '5d',
    'lem:5e': '5e',
    'lem:6': '6',
    # Propositions
    'prop:tripartite_indep': '1',
    'prop:cooperative_anchoring': '2',
    # Definitions (numbered globally)
    'def:joint_indep': '7',
    'def:intensive_paper10': '13',
    'def:loss_fraction': '14',
    'def:coop_overlap': '15',
    'def:tripartite': '16',
    'def:cross_sub_coop': '17',
    # Invariants (each is a definition; numbers below are their definition counter)
    'inv:I1': '1',
    'inv:I2': '2',
    'inv:I3': '3',
    'inv:I4': '4',
    'inv:I5': '5',
    'inv:I6': '6',
    'inv:I7': '8',
    'inv:I8': '9',
    'inv:I9': '10',
    'inv:I10': '11',
    'inv:I11': '12',
    # Remarks (numbered globally)
    'rem:mechanism_campaign': '1',
    'rem:multishock': '2',
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
  "title": "Goal-Frontier Maximization: A Provably Safe Regime for Capability-Unbounded Deployment",
  "description": "Characterizes a provably safe regime for deployments of capability-unbounded systems within the Goal-Frontier Maximization framework, defined by eleven operational invariants, twelve operational conditions (C1)-(C12), and four Concentration-Gap structural conditions (representativeness, bounded dispersion, coalition closure, Lipschitz embedding compatibility). Under these conditions, the Goodhart slack between proxy and operational truth is bounded by a constant independent of the system's absolute capability magnitude, with tail-bounded detection of substrate-targeting evasions in a four-channel observable class. The regime is delimited by three layers (static safe region, detection-and-correction with lead-time guarantee, five explicitly named residuals), requires a canonical tripartite substrate identification (Human + AI + Formal-Operational) with failure-correlation-independent failure modes, and uses cooperative anchoring to make optimization pressure on cooperative outputs locally rational toward preserving the substrate-exclusive verification layer.",
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
  <h1>Goal-Frontier Maximization: A Provably Safe Regime for Capability-Unbounded Deployment</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/provably-safe/provably-safe.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
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
    cp "$PAPER_DIR/main.pdf" "$OUT_DIR/provably-safe.pdf"
    echo "PDF copied to $OUT_DIR/provably-safe.pdf"
fi

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
