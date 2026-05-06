#!/usr/bin/env bash
# Build the Distill HTML version of Paper 11 (Structural Foundations for GFM Deployment Safety).
# Usage: ./build-web.sh
# Output: ../../public/papers/safety-foundations/index.html

set -euo pipefail

# Ensure homebrew binaries (pandoc) are available
export PATH="/opt/homebrew/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAPER_DIR="$SCRIPT_DIR"
OUT_DIR="$SCRIPT_DIR/../../public/papers/safety-foundations"

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

# Resolve cross-references for Paper 11 (Structural Foundations for GFM Deployment Safety)
ref_map = {
    # Sections
    'sec:intro': '1',
    'sec:setup': '2',
    'sec:bounded_coev': '3',
    'sec:concgap': '4',
    'sec:concgap-algebraic': '4.1',
    'sec:concgap-counterparty': '4.2',
    'sec:concgap-transfer': '4.3',
    'sec:composition': '5',
    'sec:audits': '6',
    'sec:discussion': '7',
    # Theorems
    'thm:c7-corollary': '1',
    'thm:concgap-scoped': '2',
    # Assumptions
    'ass:c7-rate': '1',
    'ass:embedding-companion': '2',
    # Lemmas
    'lem:per-step-companion': '1',
    'lem:cumulative-companion': '2',
    'lem:forward-companion': '3',
    'lem:reverse-companion': '4',
    # Definitions
    'def:M-step': '1',
    'def:c5-ovl': '2',
    'def:chisq-companion': '3',
    'def:hhi-companion': '4',
    'def:rep-companion': '5',
    'def:disp-companion': '6',
    'def:coal-companion': '7',
    # Remarks
    'rem:cross-corr-companion': '1',
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
  "title": "Structural Foundations for Goal-Frontier Maximization Deployment Safety",
  "description": "Establishes two structural foundations for the deployment-safety theorem of Lasser 2026 (Provably Safe Deployment) in the Goal-Frontier Maximization sequence. First, bounded co-evolution is derived as a corollary of clipped-LLR SPRT machinery, an upper exposure-rate cap, and the verification protocol's channel-projection structure. Second, a scoped Concentration-Gap selection theorem proves that under four operationally auditable structural conditions — representativeness (REP), bounded dispersion (DISP), coalition closure (COAL), and Lipschitz embedding compatibility (EMB) — the proxy-truth Goodhart slack is bounded by an explicit chi-squared-divergence quantity that controls the Herfindahl-index trade-flow concentration. The selection theorem replaces the monolithic HHI surrogate-adequacy assumption with concrete checkable conditions and converts the Concentration-Gap conjecture into a scoped theorem with named structural prerequisites. Audit procedures for (C7.RATE), (REP), (DISP), (COAL), and the embedding compatibility precondition are specified.",
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
  <h1>Structural Foundations for Goal-Frontier Maximization Deployment Safety</h1>
  <p style="margin-top: 0.5em;"><a href="/papers/safety-foundations/safety-foundations.pdf" style="color: #666; text-decoration: none; border-bottom: 1px solid #ccc;">📄 Download PDF version</a></p>
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
    cp "$PAPER_DIR/main.pdf" "$OUT_DIR/safety-foundations.pdf"
    echo "PDF copied to $OUT_DIR/safety-foundations.pdf"
fi

echo "Done: $OUT_DIR/index.html"
echo "Size: $(wc -c < "$OUT_DIR/index.html") bytes, $(wc -l < "$OUT_DIR/index.html") lines"
