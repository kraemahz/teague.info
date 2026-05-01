#!/usr/bin/env bash
# Build the Distill HTML version of Paper 8a (Revealed Sacrifice).
# Usage: ./build-web.sh
# Output: ../../public/papers/revealed-sacrifice/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/revealed-sacrifice"

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

# Convert Pandoc citation spans to Distill d-cite tags
def convert_cite(m):
    keys = m.group(1).replace(' ', ',')
    return '<d-cite key=\"' + keys + '\"></d-cite>'

html = re.sub(
    r'<span\s+class=\"citation\"\s+data-cites=\"([^\"]+)\">\s*[^<]*</span>',
    convert_cite,
    html,
    flags=re.DOTALL
)

# Remove bare \label{...} lines
html = re.sub(r'\\\\label\{[^}]*\}\s*', '', html)
html = re.sub(r'\\\\qed\b', '', html)
html = re.sub(r'0?[□◻◼▪▫∎■◾◽△▲◇]', '', html)

# Resolve cross-references for Paper 8a (Revealed Sacrifice)
ref_map = {
    # Sections
    'sec:introduction': '1',
    'sec:not_do': '1.3',
    'sec:design_principle': '1.5',
    'sec:dependencies': '1.6',
    'sec:sacrifice_model': '2',
    'sec:assumptions': '2.1',
    'sec:sacrifice_events': '2.2',
    'sec:lower_bound': '3',
    'sec:two_channels': '4',
    'sec:channel_substitutability': '4.3',
    'sec:axiom_inheritance': '5',
    'sec:commitment': '6',
    'sec:integration': '7',
    'sec:companion_pointer': '7.4',
    'sec:discussion': '8',
    # Definitions
    'def:trade_window': '1',
    'def:sacrifice_event': '2',
    'def:volR': '3',
    'def:bundle_decomp': '4',
    'def:volRlower_subset': '5',
    'def:btoc_ratio': '6',
    'def:money_sacrifice': '7',
    'def:time_sacrifice': '8',
    'def:committed_event': '9',
    'def:category_partition': '10',
    'def:exercise_indicator': '11',
    # Lemmas / Theorems / Propositions / Corollaries
    'lem:cancellation': '1',
    'thm:privacy': '1',
    'thm:aggregate_bound': '2',
    'thm:axiom_inheritance': '3',
    'prop:privacy_institutional': '1',
    'prop:monotone': '2',
    'prop:monotone_part_a': '3',
    'prop:commit_preserves': '4',
    'prop:zk_aggregation': '5',
    'cor:joint_coverage': '1',
    'cor:not_self_balancing': '2',
    # Examples
    'ex:agent_specific_time': '1',
    'ex:capital_concentrated': '2',
    'ex:volR_removal_invariance': '3',
    'ex:m6_fail_volRlower': '4',
    # Remarks
    'rem:s5_heavy': '1',
    'rem:s0_substantive': '2',
    'rem:units': '3',
    'rem:cooperative_closure_op': '4',
    'rem:bundle_for_bundle': '5',
    'rem:s4a_status': '6',
    'rem:privacy_mixed_status': '7',
    'rem:volR_diagnostic': '8',
    'rem:within_bundle_indep': '9',
    'rem:poset_indep': '11',
    'rem:part_a_monotone_interp': '12',
    'rem:s0_time_cap': '13',
    'rem:residual_scope': '14',
    'rem:cross_channel_overlap': '15',
    'rem:zk_limits': '17',
    'rem:external_attestation': '18',
    'rem:label_collision': '19',
    'rem:commit_part_b': '20',
    'rem:boundary_cooperative_undercount': '23',
    # Open Questions
    'oq:hedonic': '1',
    'oq:mixed_polarity': '2',
    'oq:nonstationarity': '3',
    'oq:coercion': '4',
    'oq:market_failure': '5',
    'oq:commitment_infra': '6',
    'oq:calibration': '7',
    # Appendices
    'app:exercise_indicator': 'A',
    'app:proofs': 'B',
    'app:notation': 'C',
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
  "title": "An Aggregate B-to-C Lower Bound from Revealed-Sacrifice Observation",
  "description": "Constructs a privacy-respecting observation channel for the Goal-Frontier Maximization framework's exercised capability volume vol_R via revealed-sacrifice events. The Aggregate B-to-C Lower Bound theorem yields a constructive lower bound vol_R^lower from voluntary trade events under six named assumptions S0-S5 and genuine-exchange conditions. Composes with a zero-knowledge commitment layer for privacy-respecting aggregation. Establishes the structural non-self-balancing finding for vol_R: the measure is not strictly monotone under removal of unexercised capabilities, so vol_L's self-balancing property does not transfer.",
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
  <h1>An Aggregate B-to-C Lower Bound from Revealed-Sacrifice Observation</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/revealed-sacrifice/revealed-sacrifice.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
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
    cp "$PAPER_DIR/main.pdf" "$OUT_DIR/revealed-sacrifice.pdf"
    echo "PDF copied to $OUT_DIR/revealed-sacrifice.pdf"
fi

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
