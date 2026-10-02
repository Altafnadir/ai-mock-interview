import json
import logging
import random
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.interview import Question, JobRole, InterviewCategory, DifficultyLevel

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """Generates tailored interview questions via Gemini API or the seeded database question bank."""

    def generate_session_questions(
        self,
        db: Session,
        job_role: JobRole,
        category: InterviewCategory,
        difficulty: DifficultyLevel,
        total_questions: int = 5,
        resume_context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Produces an ordered list of questions for an interview session.
        Attempts LLM personalization via Gemini API first; gracefully falls back to DB question bank.
        """
        # Try Gemini API if key is set
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            try:
                ai_questions = self._generate_with_gemini(
                    job_role_name=job_role.name,
                    category_name=category.name,
                    difficulty_name=difficulty.name,
                    total_count=total_questions,
                    resume_context=resume_context
                )
                if ai_questions and len(ai_questions) >= total_questions:
                    return ai_questions[:total_questions]
            except Exception as e:
                logger.warning(f"Gemini Question Generation failed: {e}. Falling back to DB question bank.")

        # Fallback to DB Question Bank
        return self._generate_from_db(
            db=db,
            job_role_id=job_role.id,
            category_id=category.id,
            difficulty_id=difficulty.id,
            total_count=total_questions
        )

    def _generate_with_gemini(
        self,
        job_role_name: str,
        category_name: str,
        difficulty_name: str,
        total_count: int,
        resume_context: Optional[Dict[str, Any]] = None
    ) -> Optional[List[Dict[str, Any]]]:
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        resume_summary = "No resume provided."
        if resume_context:
            skills = ", ".join(resume_context.get("extracted_skills", [])[:10])
            projects = [p.get("name") if isinstance(p, dict) else str(p) for p in resume_context.get("extracted_projects", [])[:3]]
            resume_summary = f"Skills: {skills}. Projects: {', '.join(projects)}."

        prompt = (
            f"Generate exactly {total_count} realistic, professional mock interview questions for:\n"
            f"- Role: {job_role_name}\n"
            f"- Category: {category_name}\n"
            f"- Difficulty: {difficulty_name}\n"
            f"- Candidate Resume Context: {resume_summary}\n\n"
            f"Questions should test practical depth, architecture, problem-solving, and communication. "
            f"If category is HR or Behavioral, use the STAR format framework. "
            f"Return JSON adhering strictly to schema."
        )

        response_schema = {
            "type": "OBJECT",
            "properties": {
                "questions": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "question_text": {"type": "STRING"},
                            "time_limit_seconds": {"type": "INTEGER"},
                            "expected_keywords": {"type": "ARRAY", "items": {"type": "STRING"}}
                        },
                        "required": ["question_text", "time_limit_seconds"]
                    }
                }
            },
            "required": ["questions"]
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
                q_list = data.get("questions", [])
                formatted = []
                for idx, q in enumerate(q_list):
                    formatted.append({
                        "order_index": idx + 1,
                        "question_text": q.get("question_text"),
                        "source": "ai",
                        "time_limit_seconds": q.get("time_limit_seconds", 120),
                        "expected_keywords": q.get("expected_keywords", [])
                    })
                return formatted
        except Exception as e:
            logger.warning(f"Gemini question generation error: {e}")
        return None

    def _generate_from_db(
        self,
        db: Session,
        job_role_id: str,
        category_id: str,
        difficulty_id: str,
        total_count: int
    ) -> List[Dict[str, Any]]:
        # 1. Exact match query
        exact_query = db.query(Question).filter(
            Question.job_role_id == job_role_id,
            Question.category_id == category_id,
            Question.difficulty_id == difficulty_id,
            Question.is_active == True
        ).all()

        selected_questions = list(exact_query)

        # 2. Relax difficulty if needed
        if len(selected_questions) < total_count:
            role_cat_query = db.query(Question).filter(
                Question.job_role_id == job_role_id,
                Question.category_id == category_id,
                Question.is_active == True
            ).all()
            for q in role_cat_query:
                if q not in selected_questions:
                    selected_questions.append(q)
                if len(selected_questions) >= total_count:
                    break

        # 3. Relax role if needed
        if len(selected_questions) < total_count:
            cat_query = db.query(Question).filter(
                Question.category_id == category_id,
                Question.is_active == True
            ).all()
            for q in cat_query:
                if q not in selected_questions:
                    selected_questions.append(q)
                if len(selected_questions) >= total_count:
                    break

        # 4. Fill from any active questions
        if len(selected_questions) < total_count:
            all_q = db.query(Question).filter(Question.is_active == True).all()
            for q in all_q:
                if q not in selected_questions:
                    selected_questions.append(q)
                if len(selected_questions) >= total_count:
                    break

        # Shuffle selection if more than needed
        if len(selected_questions) > total_count:
            selected_questions = random.sample(selected_questions, total_count)

        result = []
        for idx, q in enumerate(selected_questions):
            result.append({
                "order_index": idx + 1,
                "question_text": q.text,
                "source": "bank",
                "time_limit_seconds": 120,
                "expected_keywords": q.expected_keywords or []
            })

        return result

    def generate_followup_question(
        self,
        parent_question_text: str,
        candidate_answer_text: str,
        job_role_name: str
    ) -> Optional[str]:
        """Generates dynamic follow-up question probing deeper into candidate's response."""
        if not candidate_answer_text or len(candidate_answer_text.split()) < 5:
            return None

        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                prompt = (
                    f"You are conducting a technical interview for a {job_role_name}.\n"
                    f"Interviewer asked: \"{parent_question_text}\"\n"
                    f"Candidate answered: \"{candidate_answer_text}\"\n\n"
                    f"Ask one concise, targeted follow-up question (under 25 words) that tests the candidate's depth, "
                    f"trade-off awareness, or specific design decision."
                )
                interaction = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )
                output = interaction.output_text
                if output and len(output.strip()) > 10:
                    return output.strip().strip('"')
            except Exception as e:
                logger.warning(f"Followup question generation with Gemini failed: {e}")

        # Intelligent template fallbacks
        templates = [
            f"What was the most challenging technical trade-off you had to consider while working through that scenario?",
            f"How did you measure or validate the performance and reliability of your solution?",
            f"If you had to scale that solution to support 100x traffic or data volume, what architectural bottlenecks would you tackle first?",
            f"Could you share a specific edge case or failure scenario you encountered with that approach and how you resolved it?"
        ]
        return random.choice(templates)

question_generator = QuestionGenerator()
