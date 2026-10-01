import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class ScoringEngine:
    """Computes weighted multi-dimensional interview scores and hiring verdicts.
    
    Default weights per proposal specification:
    - Content/Technical: 25
    - Communication: 15
    - Voice: 15
    - Confidence: 15
    - Eye contact: 10
    - Body language: 10
    - Grammar: 10
    Total: 100 points
    
    Verdict bands:
    - >= 85.0: Excellent
    - 70.0 - 84.9: Good
    - 55.0 - 69.9: Needs Improvement
    - < 55.0: Needs Significant Practice
    """

    DEFAULT_WEIGHTS = {
        "content": 25.0,
        "communication": 15.0,
        "voice": 15.0,
        "confidence": 15.0,
        "eye_contact": 10.0,
        "body_language": 10.0,
        "grammar": 10.0,
    }

    def compute_composite_confidence(
        self,
        voice_stability: Optional[float] = 80.0,
        emotion_confidence: Optional[float] = 80.0,
        eye_contact_pct: Optional[float] = 75.0,
        posture_score: Optional[float] = 80.0,
        filler_frequency_wpm: Optional[float] = 2.0
    ) -> float:
        """Combines voice dynamics, affective emotion, eye gaze, posture alignment, and filler disfluency."""
        v_stab = voice_stability if voice_stability is not None else 78.0
        e_conf = emotion_confidence if emotion_confidence is not None else 78.0
        eye = eye_contact_pct if eye_contact_pct is not None else 75.0
        post = posture_score if posture_score is not None else 80.0

        # Filler penalty: baseline 100 minus 6 points per filler/min
        f_freq = filler_frequency_wpm if filler_frequency_wpm is not None else 2.0
        filler_score = max(min(100.0 - (f_freq * 6.0), 100.0), 40.0)

        composite = (
            (e_conf * 0.30) +
            (v_stab * 0.25) +
            (eye * 0.20) +
            (post * 0.15) +
            (filler_score * 0.10)
        )
        return round(max(min(composite, 98.0), 30.0), 1)

    def calculate_scores(
        self,
        content_scores: Optional[List[float]] = None,
        communication_score: Optional[float] = None,
        voice_score: Optional[float] = None,
        eye_contact_score: Optional[float] = None,
        body_language_score: Optional[float] = None,
        confidence_score: Optional[float] = None,
        grammar_score: Optional[float] = None,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Calculates normalized 0-100 scores and applies weighted multi-dimensional synthesis."""
        weights = dict(self.DEFAULT_WEIGHTS)
        if custom_weights:
            weights.update(custom_weights)

        # Baseline fallbacks if individual modules failed or returned None
        valid_content = [s for s in (content_scores or []) if s is not None]
        avg_content = round(sum(valid_content) / len(valid_content), 1) if valid_content else 75.0

        final_comm = communication_score if communication_score is not None else 78.0
        final_voice = voice_score if voice_score is not None else 80.0
        final_eye = eye_contact_score if eye_contact_score is not None else 78.0
        final_body = body_language_score if body_language_score is not None else 82.0
        final_conf = confidence_score if confidence_score is not None else 80.0
        final_gram = grammar_score if grammar_score is not None else 85.0

        # Calculate weighted sum
        total_weight = sum(weights.values())
        if total_weight <= 0:
            total_weight = 100.0

        weighted_sum = (
            (avg_content * weights["content"]) +
            (final_comm * weights["communication"]) +
            (final_voice * weights["voice"]) +
            (final_conf * weights["confidence"]) +
            (final_eye * weights["eye_contact"]) +
            (final_body * weights["body_language"]) +
            (final_gram * weights["grammar"])
        )

        overall = round(weighted_sum / total_weight, 1)
        overall_score = max(min(overall, 100.0), 0.0)

        # Determine standardized verdict band
        if overall_score >= 85.0:
            verdict = "Excellent"
        elif overall_score >= 70.0:
            verdict = "Good"
        elif overall_score >= 55.0:
            verdict = "Needs Improvement"
        else:
            verdict = "Needs Significant Practice"

        return {
            "overall_score": overall_score,
            "content_score": round(avg_content, 1),
            "communication_score": round(final_comm, 1),
            "voice_score": round(final_voice, 1),
            "eye_contact_score": round(final_eye, 1),
            "body_language_score": round(final_body, 1),
            "confidence_score": round(final_conf, 1),
            "grammar_score": round(final_gram, 1),
            "final_verdict": verdict,
            "weights_used": weights
        }

scoring_engine = ScoringEngine()
