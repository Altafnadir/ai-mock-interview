from typing import Dict, Any, List

class ScoringEngine:
    """Computes weighted multi-dimensional interview scores and hiring verdicts."""

    # Weights configured per project specification
    WEIGHT_CONTENT = 0.35
    WEIGHT_COMMUNICATION = 0.20
    WEIGHT_VOICE = 0.15
    WEIGHT_VISION = 0.15
    WEIGHT_CONFIDENCE = 0.15

    def calculate_scores(
        self,
        content_scores: List[float],
        communication_score: float,
        voice_score: float,
        eye_contact_score: float,
        body_language_score: float,
        confidence_score: float,
        grammar_score: float
    ) -> Dict[str, Any]:
        avg_content = round(sum(content_scores) / max(len(content_scores), 1), 1) if content_scores else 75.0

        # Aggregate weighted score
        overall = (
            (avg_content * self.WEIGHT_CONTENT) +
            (communication_score * self.WEIGHT_COMMUNICATION) +
            (voice_score * self.WEIGHT_VOICE) +
            (eye_contact_score * self.WEIGHT_VISION) +
            (confidence_score * self.WEIGHT_CONFIDENCE)
        )
        overall_score = round(max(min(overall, 100.0), 0.0), 1)

        # Determine verdict
        if overall_score >= 85.0:
            verdict = "Strong Hire / Recommended"
        elif overall_score >= 70.0:
            verdict = "Hire / Qualified"
        elif overall_score >= 55.0:
            verdict = "Borderline / Needs Practice"
        else:
            verdict = "Needs Significant Improvement"

        return {
            "overall_score": overall_score,
            "content_score": avg_content,
            "communication_score": round(communication_score, 1),
            "voice_score": round(voice_score, 1),
            "eye_contact_score": round(eye_contact_score, 1),
            "body_language_score": round(body_language_score, 1),
            "confidence_score": round(confidence_score, 1),
            "grammar_score": round(grammar_score, 1),
            "final_verdict": verdict
        }

scoring_engine = ScoringEngine()
