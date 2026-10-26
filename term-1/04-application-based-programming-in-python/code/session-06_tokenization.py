"""
Session 6 · Example 3: tokenizing text with regular expressions
---------------------------------------------------------------
Tokenization = splitting text into units (sentences, words, symbols) that a
program or an NLP model can count and analyse. No external library needed.
Run:  python session-06_tokenization.py
"""
import re
from collections import Counter

review = ("Loved the new campus café!!! The chai is great, but Wi-Fi isn't. "
          "Prices went up 15% since Sept... Dr. Khan's AI lab opens at 9:30 a.m. "
          "#KarachiEats @campus_cafe https://example.com/menu :)")

# 1. Naive split breaks on punctuation
print("str.split():", review.split()[:8])

# 2. Sentence tokenization: split after . ! ? followed by space + capital,
#    but protect common abbreviations first
protected = re.sub(r"\b(Dr|Mr|Ms|Mrs|a\.m|p\.m)\.", lambda m: m.group(0).replace(".", "<DOT>"), review)
sentences = [s.replace("<DOT>", ".") for s in re.split(r"(?<=[.!?])\s+(?=[A-Z#@])", protected)]
print("\nSentences:")
for i, s in enumerate(sentences, 1):
    print(f"  {i}. {s}")

# 3. Word tokenization with a pattern that knows about real-world tokens
TOKEN = re.compile(r"""
    https?://\S+              # URLs
  | [#@]\w+                   # hashtags and mentions
  | (?:Dr|Mr|Ms|Mrs)\.        # titles keep their dot
  | (?:[A-Za-z]\.){2,}        # abbreviations like a.m.
  | \.{3}                     # an ellipsis is one token
  | \d+(?::\d+)?%?            # numbers, times like 9:30, percentages
  | \w+(?:[-']\w+)*           # words, incl. Wi-Fi and isn't
  | [:;]-?[)(DP]              # simple emoticons
  | [^\w\s]                   # any other single symbol
""", re.VERBOSE)
tokens = TOKEN.findall(review)
print("\nTokens:", tokens)
print("token count:", len(tokens))

# 4. Classify tokens by type
def kind(tok):
    if tok.startswith("http"): return "url"
    if tok[0] in "#@": return "tag"
    if tok.endswith(".") and tok[0].isalpha(): return "abbreviation"
    if tok[0].isdigit(): return "number"
    if re.fullmatch(r"\w+(?:[-']\w+)*", tok): return "word"
    return "symbol"
print("types:", dict(Counter(kind(t) for t in tokens)))

# 5. Normalise words: lower-case, drop stop words, count
STOP = {"the", "is", "but", "at", "since", "s", "a", "m", "up"}
words = [t.lower() for t in tokens if kind(t) == "word"]
content = [w for w in words if w not in STOP]
print("content words:", content)

# 6. Word frequencies across several reviews + a chart
reviews = [review,
           "The chai is cheap and the samosa is great. Great service!",
           "Wi-Fi is slow, chai is cold, prices are high.",
           "Great lab, great teachers, great chai."]
freq = Counter(w.lower() for r in reviews for w in re.findall(r"\w+(?:[-']\w+)*", r)
               if w.lower() not in STOP | {"and", "are", "isn't", "new", "went", "opens"})
top = freq.most_common(8)
print("\nTop words in 4 reviews:", top)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
labels, counts = zip(*top)
fig, ax = plt.subplots(figsize=(7, 3.4))
ax.bar(labels, counts, color="#FF6B1A")
ax.set_ylabel("count"); ax.set_title("Most frequent content words after regex tokenization")
fig.tight_layout(); fig.savefig("session-06_tokenization.png", dpi=110)
print("Chart saved: session-06_tokenization.png")
