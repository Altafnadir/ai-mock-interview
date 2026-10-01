import re
import math
from typing import Dict, List, Any

# Common grammatical patterns and disfluencies to flag
GRAMMAR_PATTERNS = [
    (r"\b(i|we|they|you)\s+is\b", "Subject-verb agreement: use 'am' or 'are' instead of 'is'"),
    (r"\b(he|she|it)\s+are\b", "Subject-verb agreement: use 'is' instead of 'are'"),
    (r"\b(doesn't|don't)\s+has\b", "Use base form 'have' after auxiliary negative verbs"),
    (r"\b(could|should|would)\s+of\b", "Incorrect preposition: use 'could have', 'should have', or 'would have'"),
    (r"\bmore\s+(better|faster|easier|higher|stronger)\b", "Double comparative: remove 'more' before '-er' adjectives"),
    (r"\bvery\s+unique\b", "'Unique' is an absolute adjective; avoid intensifying with 'very'"),
    (r"\b(their|there|they're)\b", None),  # Context check
]

class GrammarAnalyzer:
    """Analyzes interview transcripts for grammatical correctness, readability, and vocabulary richness."""

    def analyze(self, transcript: str) -> Dict[str, Any]:
        if not transcript or not transcript.strip():
            return {
                "grammar_error_count": 0,
                "spelling_error_count": 0,
                "readability_score": 75.0,
                "vocabulary_richness_score": 70.0,
                "error_breakdown": [],
                "suggestions": ["No spoken transcript available for grammar evaluation."]
            }

        text = transcript.strip()
        words = re.findall(r'\b[A-Za-z]+\b', text)
        total_words = max(len(words), 1)

        # Split sentences by punctuation
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        total_sentences = max(len(sentences), 1)

        # 1. Grammar error matching
        errors = []
        for pattern, explanation in GRAMMAR_PATTERNS:
            if explanation:
                matches = re.finditer(pattern, text, re.I)
                for m in matches:
                    errors.append({
                        "error_text": m.group(0),
                        "explanation": explanation,
                        "position": m.start()
                    })

        grammar_error_count = len(errors)

        # 2. Vocabulary Richness (Type-Token Ratio adjusted for length)
        unique_words = len({w.lower() for w in words})
        raw_ttr = unique_words / total_words
        # Scale to 0-100 score (higher TTR -> higher vocabulary richness)
        vocab_score = min(round(raw_ttr * 125.0, 1), 100.0)

        # 3. Readability Index (Flesch-Kincaid Reading Ease approximation)
        # Approximate syllables by counting vowel clusters
        syllable_count = 0
        for w in words:
            vowels = len(re.findall(r'[aeiouy]+', w.lower()))
            syllable_count += max(vowels, 1)

        words_per_sentence = total_words / total_sentences
        syllables_per_word = syllable_count / total_words

        # Flesch Reading Ease = 206.835 - 1.015 * (total_words / total_sentences) - 84.6 * (total_syllables / total_words)
        flesch = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
        readability_score = max(min(round(flesch, 1), 100.0), 30.0)

        # 4. Actionable suggestions
        suggestions = []
        if words_per_sentence > 28:
            suggestions.append("Sentences are quite long; try structuring your points into shorter, punchier statements.")
        elif words_per_sentence < 8:
            suggestions.append("Sentences are relatively brief; elaborate with more technical context and connective transitions.")

        if vocab_score < 50.0:
            suggestions.append("Incorporate more domain-specific vocabulary and varied descriptors to enrich your explanations.")
        else:
            suggestions.append("Strong vocabulary variety and natural sentence structure.")

        if grammar_error_count > 0:
            suggestions.append("Pay attention to subject-verb agreement during spontaneous speech responses.")

        return {
            "grammar_error_count": grammar_error_count,
            "spelling_error_count": 0,
            "readability_score": readability_score,
            "vocabulary_richness_score": vocab_score,
            "error_breakdown": errors[:5],
            "suggestions": suggestions
        }

grammar_analyzer = GrammarAnalyzer()
