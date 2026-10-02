import json
import re
import logging
from typing import Dict, List, Any, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

class ContentEvaluator:
    """Evaluates question answers for technical depth, keyword alignment, and STAR rubric structure."""

    def evaluate_answer(
        self,
        question_text: str,
        answer_text: str,
        expected_keywords: Optional[List[str]] = None,
        job_role_name: str = "Full Stack Developer",
        category_name: str = "Technical"
    ) -> Dict[str, Any]:
        """
        Evaluates answer content.
        Uses Gemini LLM if key is configured, else falls back to robust semantic rubric analyzer.
        """
        if not answer_text or not answer_text.strip():
            return {
                "technical_accuracy_score": 0.0,
                "relevance_score": 0.0,
                "completeness_score": 0.0,
                "star_situation_score": 0.0,
                "star_task_score": 0.0,
                "star_action_score": 0.0,
                "star_result_score": 0.0,
                "keywords_matched": [],
                "keywords_missing": expected_keywords or [],
                "strengths": [],
                "improvements": ["No answer provided for this question."]
            }

        # Try Gemini API
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            try:
                gemini_eval = self._evaluate_with_gemini(
                    question_text=question_text,
                    answer_text=answer_text,
                    expected_keywords=expected_keywords or [],
                    job_role_name=job_role_name,
                    category_name=category_name
                )
                if gemini_eval:
                    return gemini_eval
            except Exception as e:
                logger.warning(f"Gemini content evaluation failed: {e}. Using rubric fallback.")

        return self._evaluate_with_rubric(
            question_text=question_text,
            answer_text=answer_text,
            expected_keywords=expected_keywords or []
        )

    def _evaluate_with_gemini(
        self,
        question_text: str,
        answer_text: str,
        expected_keywords: List[str],
        job_role_name: str,
        category_name: str
    ) -> Optional[Dict[str, Any]]:
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        prompt = (
            f"You are a strict technical and behavioral interviewer evaluating a candidate for a {job_role_name} position.\n\n"
            f"Question: \"{question_text}\"\n"
            f"Candidate Answer: \"{answer_text}\"\n"
            f"Expected Domain Keywords: {', '.join(expected_keywords) if expected_keywords else 'General engineering best practices'}\n\n"
            f"Evaluate the answer across:\n"
            f"1. technical_accuracy_score (0-100)\n"
            f"2. relevance_score (0-100)\n"
            f"3. completeness_score (0-100)\n"
            f"4. STAR Method Breakdown: star_situation_score (0-100), star_task_score (0-100), star_action_score (0-100), star_result_score (0-100)\n"
            f"5. keywords_matched (list of strings found in answer)\n"
            f"6. keywords_missing (list of expected keywords omitted)\n"
            f"7. strengths (list of 2-3 specific positive points)\n"
            f"8. improvements (list of 2-3 actionable areas to improve)\n"
            f"Return valid JSON adhering to schema."
        )

        response_schema = {
            "type": "OBJECT",
            "properties": {
                "technical_accuracy_score": {"type": "NUMBER"},
                "relevance_score": {"type": "NUMBER"},
                "completeness_score": {"type": "NUMBER"},
                "star_situation_score": {"type": "NUMBER"},
                "star_task_score": {"type": "NUMBER"},
                "star_action_score": {"type": "NUMBER"},
                "star_result_score": {"type": "NUMBER"},
                "keywords_matched": {"type": "ARRAY", "items": {"type": "STRING"}},
                "keywords_missing": {"type": "ARRAY", "items": {"type": "STRING"}},
                "strengths": {"type": "ARRAY", "items": {"type": "STRING"}},
                "improvements": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": [
                "technical_accuracy_score", "relevance_score", "completeness_score",
                "star_situation_score", "star_task_score", "star_action_score", "star_result_score",
                "keywords_matched", "keywords_missing", "strengths", "improvements"
            ]
        }

        try:
            from google.genai import types
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema
                )
            )
            output = resp.text
            if output:
                data = json.loads(output)
                data["used_fallback"] = False
                data["library"] = "Google Gemini 2.5 Flash"
                return data
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}")
        return None

    def _evaluate_with_rubric(
        self,
        question_text: str,
        answer_text: str,
        expected_keywords: List[str]
    ) -> Dict[str, Any]:
        text_lower = answer_text.lower()
        words = text_lower.split()
        word_count = len(words)

        # 1. Keyword matching
        matched = []
        missing = []
        for kw in expected_keywords:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower):
                matched.append(kw)
            else:
                missing.append(kw)

        kw_ratio = (len(matched) / max(len(expected_keywords), 1)) if expected_keywords else 0.8
        kw_score = round(kw_ratio * 100.0, 1)

        # 2. STAR Method heuristic detectors
        # Situation: mentions of problem, context, previous experience, team, client
        situation_cues = ["project", "client", "problem", "challenge", "company", "team", "scenario", "working on", "when i was"]
        has_situation = any(c in text_lower for c in situation_cues)
        sit_score = 85.0 if has_situation else 60.0

        # Task: responsibilities, requirements, goal
        task_cues = ["goal", "task", "requirement", "objective", "needed to", "had to", "responsibility", "assigned"]
        has_task = any(c in text_lower for c in task_cues)
        task_score = 82.0 if has_task else 62.0

        # Action: concrete action verbs
        action_cues = ["implemented", "built", "designed", "optimized", "created", "refactored", "migrated", "developed", "configured", "used"]
        action_count = sum(1 for c in action_cues if c in text_lower)
        act_score = min(70.0 + (action_count * 6.0), 95.0)

        # Result: metrics, outcome, impact, percentages
        has_metrics = bool(re.search(r'\b\d+%\b|\b\d+x\b|\$\d+|\b\d+\s*(users|requests|ms|seconds|fps)\b', answer_text, re.I))
        result_cues = ["improved", "reduced", "resulted in", "successfully", "achieved", "delivered", "outcome"]
        has_result = any(c in text_lower for c in result_cues) or has_metrics
        res_score = 88.0 if has_metrics else (75.0 if has_result else 58.0)

        # Length and depth scaling
        if word_count < 25:
            relevance = 55.0
            completeness = 45.0
            accuracy = 60.0
        elif word_count < 60:
            relevance = 75.0
            completeness = 70.0
            accuracy = 75.0
        else:
            relevance = min(82.0 + (kw_ratio * 15.0), 96.0)
            completeness = min(80.0 + (kw_ratio * 12.0), 94.0)
            accuracy = min(80.0 + (kw_ratio * 16.0), 95.0)

        strengths = []
        improvements = []

        if matched:
            strengths.append(f"Demonstrated domain knowledge by naturally referencing {', '.join(matched[:3])}.")
        if action_count >= 2:
            strengths.append("Articulated specific technical actions and tools used.")
        if has_metrics:
            strengths.append("Supported achievements with quantifiable impact metrics.")

        if not strengths:
            strengths.append("Clear foundational understanding of the core question subject.")

        if missing:
            improvements.append(f"Could strengthen answer by incorporating concepts like {', '.join(missing[:3])}.")
        if not has_metrics:
            improvements.append("Quantify the final outcome or performance gains using concrete metrics.")
        if not has_task:
            improvements.append("Clearly state your specific role and objective within the STAR framework.")

        return {
            "technical_accuracy_score": round(accuracy, 1),
            "relevance_score": round(relevance, 1),
            "completeness_score": round(completeness, 1),
            "star_situation_score": round(sit_score, 1),
            "star_task_score": round(task_score, 1),
            "star_action_score": round(act_score, 1),
            "star_result_score": round(res_score, 1),
            "keywords_matched": matched,
            "keywords_missing": missing,
            "strengths": strengths,
            "improvements": improvements,
            "used_fallback": True,
            "library": "STAR Rubric & Keyword Matcher"
        }

content_evaluator = ContentEvaluator()
