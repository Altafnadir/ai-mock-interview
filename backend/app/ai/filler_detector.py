import re
from typing import Dict, List, Any

COMMON_FILLERS = [
    "um", "uh", "like", "you know", "actually", "basically",
    "so", "right", "i mean", "sort of", "kind of", "literally",
    "well", "honestly", "you see", "at the end of the day"
]

class FillerDetector:
    """Analyzes transcripts for verbal fillers, disfluencies, and speech hesitation patterns."""

    def analyze(self, transcript: str, duration_seconds: float = 30.0) -> Dict[str, Any]:
        if not transcript or not transcript.strip():
            return {
                "total_fillers": 0,
                "filler_percentage": 0.0,
                "fillers_per_minute": 0.0,
                "breakdown": {},
                "snippets": [],
                "severity": "optimal",
                "coaching_tip": "No speech disfluencies detected."
            }

        words = transcript.strip().split()
        total_words = max(len(words), 1)
        text_lower = transcript.lower()

        breakdown = {}
        total_fillers = 0
        snippets = []

        for filler in COMMON_FILLERS:
            # Word boundary regex search
            pattern = r'\b' + re.escape(filler) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            count = len(matches)
            if count > 0:
                breakdown[filler] = count
                total_fillers += count

                # Capture context snippets for top 3 occurrences
                for m in matches[:3]:
                    start = max(m.start() - 25, 0)
                    end = min(m.end() + 25, len(transcript))
                    snippet = transcript[start:end].strip()
                    snippets.append(f"...{snippet}...")

        filler_pct = round((total_fillers / total_words) * 100, 1)
        mins = max(duration_seconds / 60.0, 0.1)
        fpm = round(total_fillers / mins, 1)

        # Classify severity
        if filler_pct < 2.0:
            severity = "optimal"
            tip = "Excellent vocal clarity with minimal hesitation words."
        elif filler_pct <= 5.0:
            severity = "moderate"
            tip = "Acceptable conversational filler usage. Try replacing 'um' or 'like' with brief 1-second silent pauses."
        else:
            severity = "high"
            tip = f"High filler density detected ({filler_pct}%). Frequent fillers dilute confidence. Practice intentional pauses before answering."

        return {
            "total_fillers": total_fillers,
            "filler_percentage": filler_pct,
            "fillers_per_minute": fpm,
            "breakdown": breakdown,
            "snippets": snippets[:6],
            "severity": severity,
            "coaching_tip": tip
        }

filler_detector = FillerDetector()
