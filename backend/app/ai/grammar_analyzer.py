import os
import re
import math
import logging
import requests
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

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
                "suggestions": ["No spoken transcript available for grammar evaluation."],
                "used_fallback": True,
                "library": "Regex & Lexical Heuristic Analyzer"
            }

        text = transcript.strip()
        words = re.findall(r'\b[A-Za-z]+\b', text)
        total_words = max(len(words), 1)

        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        total_sentences = max(len(sentences), 1)

        # Attempt LanguageTool API check (local Docker service or custom URL)
        lt_url = os.getenv("LANGUAGETOOL_URL", "http://localhost:8010/v2/check")
        lt_result = self._check_languagetool(text, lt_url)
        if lt_result is not None:
            errors, spelling_count = lt_result
            used_fallback = False
            library = f"LanguageTool API ({lt_url})"
        else:
            # Fallback to local regex pattern matching
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
            spelling_count = 0
            used_fallback = True
            library = "Regex & Flesch-Kincaid Lexical Analyzer"

        grammar_error_count = len(errors)

        # Vocabulary Richness (Type-Token Ratio adjusted for length)
        unique_words = len({w.lower() for w in words})
        raw_ttr = unique_words / total_words
        vocab_score = min(round(raw_ttr * 125.0, 1), 100.0)

        # Readability Index (Flesch-Kincaid Reading Ease approximation)
        syllable_count = 0
        for w in words:
            vowels = len(re.findall(r'[aeiouy]+', w.lower()))
            syllable_count += max(vowels, 1)

        words_per_sentence = total_words / total_sentences
        syllables_per_word = syllable_count / total_words

        flesch = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
        readability_score = max(min(round(flesch, 1), 100.0), 30.0)

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
            suggestions.append("Pay attention to subject-verb agreement and preposition choices during spontaneous speech.")

        return {
            "grammar_error_count": grammar_error_count,
            "spelling_error_count": spelling_count,
            "readability_score": readability_score,
            "vocabulary_richness_score": vocab_score,
            "error_breakdown": errors[:5],
            "suggestions": suggestions,
            "used_fallback": used_fallback,
            "library": library
        }

    def _check_languagetool(self, text: str, url: str) -> Optional[Tuple[List[Dict[str, Any]], int]]:
        try:
            resp = requests.post(url, data={"text": text, "language": "en-US"}, timeout=1.5)
            if resp.status_code == 200:
                data = resp.json()
                matches = data.get("matches", [])
                errors = []
                spelling_count = 0
                for m in matches:
                    issue_type = m.get("rule", {}).get("issueType", "")
                    if issue_type == "misspelling":
                        spelling_count += 1
                    errors.append({
                        "error_text": text[m.get("offset", 0): m.get("offset", 0) + m.get("length", 1)],
                        "explanation": m.get("message", "Grammar suggestion"),
                        "position": m.get("offset", 0)
                    })
                return errors, spelling_count
        except Exception:
            pass
        return None

grammar_analyzer = GrammarAnalyzer()
