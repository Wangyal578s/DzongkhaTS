import re
from collections import Counter

# POS weights (new version)
POS_WEIGHTS = {
    "PROPN": 2.0,
    "NOUN": 2.0,
    "VERB": 1.6,
    "PRON": 1.0,
    "ADJ": 1.5,
    "ADV": 1.2,
    "ADP": 0.4,
    "PART": 0.4,
    "CCONJ": 0.4,
    "SCONJ": 0.4,
    "DET": 0.5,
    "NUM": 0.6,
    "AUX": 1.0,
    "PUNCT": 0.1,
    "UNK": 1.0
}

def load_tagged_text(path="data/tagged_essay.txt"):
    """Load tagged text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def split_sentences(text):
    """Split Dzongkha text into sentences based on punctuation."""
    raw = re.split(r"[།༎\n]+", text.strip())
    return [s.strip() for s in raw if s.strip()]

def parse_pos_tokens(sentence):
    """Extract (word, POS) pairs from a tagged sentence."""
    tokens = []
    for token in sentence.split():
        if "/" in token:
            word, tag = token.rsplit("/", 1)
            tokens.append((word, tag.upper()))
    return tokens

def compute_word_frequencies(sentences_tokens):
    """Count how often each word occurs."""
    freq = Counter()
    for sent in sentences_tokens:
        for w, _ in sent:
            freq[w] += 1
    return freq

def score_sentence(tokens, word_freq):
    """Weight sentence score by POS and frequency."""
    score = 0.0
    for word, tag in tokens:
        score += word_freq[word] * POS_WEIGHTS.get(tag, POS_WEIGHTS["UNK"])
    return score

def summarize_text(pos_tagged_text, top_k=3):
    sents = split_sentences(pos_tagged_text)
    parsed = [parse_pos_tokens(s) for s in sents]
    freq = compute_word_frequencies(parsed)

    scored = []
    for i, tokens in enumerate(parsed):
        scored.append((i, score_sentence(tokens, freq), sents[i]))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)[:top_k]
    ranked_sorted = sorted(ranked, key=lambda x: x[0])

    # ───── CLEAN POS TAGS FROM SELECTED SENTENCES ─────
    def remove_pos_tags(sentence):
        return re.sub(r"/[A-Z]+", "", sentence)

    clean_sentences = [remove_pos_tags(s[2]) for s in ranked_sorted]

    return " ".join(clean_sentences)

