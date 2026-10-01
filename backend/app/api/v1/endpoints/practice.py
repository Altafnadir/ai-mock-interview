from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.interview import Question, JobRole, InterviewCategory, DifficultyLevel, InterviewSession
from app.db.models.report import Report, Recommendation
from app.schemas.resource import QuestionPracticeResponse

router = APIRouter()

GENERAL_DRILLS = [
    {
        "id": "drill-filler-pause",
        "title": "Silent Pause Drill",
        "tag": "filler_words",
        "duration": "5 Mins",
        "desc": 'Answer a complex technical query without using "um", "uh", or "like". Replace every verbal hesitation with a calm 1-second silent breath.',
        "category": "Vocal Discipline",
        "is_personalized": False,
        "suggested_topic": "Communication & Vocal Discipline",
        "suggested_category": "Behavioral",
        "suggested_questions": [
            "Tell me about a time you had to explain a complex technical problem to a non-technical stakeholder.",
            "Describe a difficult bug you tracked down in production."
        ],
        "suggested_session_type": "Communication Mock Session"
    },
    {
        "id": "drill-star-story",
        "title": "STAR Method Storytelling Drill",
        "tag": "star_method",
        "duration": "8 Mins",
        "desc": "Structure a past bug resolution strictly dividing your answer into 15s Situation, 15s Task, 45s Action, and 15s quantifiable Result.",
        "category": "Behavioral",
        "is_personalized": False,
        "suggested_topic": "STAR Method Behavioral Stories",
        "suggested_category": "Behavioral",
        "suggested_questions": [
            "Tell me about a disagreement you had with a teammate and how you resolved it.",
            "Describe an instance where you took initiative outside your job description."
        ],
        "suggested_session_type": "Behavioral STAR Deep Dive"
    },
    {
        "id": "drill-eye-contact",
        "title": "Webcam Eye-Level Gaze Lock",
        "tag": "eye_contact",
        "duration": "4 Mins",
        "desc": "Focus continuously on the camera lens while answering technical questions to build unconscious gaze endurance.",
        "category": "Body Language",
        "is_personalized": False,
        "suggested_topic": "Eye Contact & Confidence Presence",
        "suggested_category": "HR",
        "suggested_questions": [
            "Why do you want to join our organization?",
            "Where do you see yourself technically in three years?"
        ],
        "suggested_session_type": "HR Confidence Screening"
    },
    {
        "id": "drill-pitch",
        "title": "60-Second System Design Elevator Pitch",
        "tag": "technical",
        "duration": "6 Mins",
        "desc": "Explain how you would design a high-throughput URL shortener or rate limiter in under 60 seconds with clear trade-offs.",
        "category": "Technical Architecture",
        "is_personalized": False,
        "suggested_topic": "Technical System Design",
        "suggested_category": "Technical",
        "suggested_questions": [
            "How would you design a distributed cache invalidation strategy?",
            "What are the differences between optimistic and pessimistic locking?"
        ],
        "suggested_session_type": "Technical Architecture Review"
    },
]

@router.get("/drills")
def get_practice_drills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Return catalog of interactive candidate micro-drills, personalized if candidate has reports."""
    # Find candidate's latest completed interview report
    latest_report = (
        db.query(Report)
        .join(InterviewSession, Report.session_id == InterviewSession.id)
        .filter(InterviewSession.user_id == current_user.id)
        .order_by(Report.generated_at.desc())
        .first()
    )

    if not latest_report:
        return GENERAL_DRILLS

    # Candidate has a completed interview report: build personalized recommendations
    session = latest_report.session
    role_name = session.job_role.name if session and session.job_role else "Software Engineer"
    category_name = session.category.name if session and session.category else "Technical"

    # Query relevant questions from DB
    sample_questions = (
        db.query(Question)
        .filter(Question.is_active == True)
        .filter(
            (Question.job_role_id == session.job_role_id) if session and session.job_role_id else True
        )
        .limit(4)
        .all()
    )
    q_texts = [q.text for q in sample_questions] if sample_questions else [
        f"Explain key architectural challenges you faced as a {role_name}.",
        "How do you approach debugging under production pressure?"
    ]

    drills = []

    # 1. Communication & Vocal Discipline Drill
    comm_score = round(latest_report.communication_score or latest_report.voice_score or 65.0)
    has_comm_weakness = any("fill" in str(w).lower() or "voice" in str(w).lower() or "speech" in str(w).lower() for w in (latest_report.weaknesses or []))
    drills.append({
        "id": "drill-filler-pause",
        "title": "Vocal Clarity & Deliberate Pause Drill" if (comm_score < 75 or has_comm_weakness) else "Silent Pause Drill",
        "tag": "filler_words",
        "duration": "5 Mins",
        "desc": (
            f"Your latest communication score was {comm_score}%. Practice answering questions with controlled pacing, using 1-second silent pauses instead of filler words."
            if (comm_score < 75 or has_comm_weakness)
            else 'Answer a complex technical query without using "um", "uh", or "like". Replace every verbal hesitation with a calm 1-second silent breath.'
        ),
        "category": "Communication Exercise",
        "is_personalized": True,
        "score_context": f"Communication Score: {comm_score}%",
        "suggested_topic": "Communication & Vocal Delivery",
        "suggested_category": "Behavioral",
        "suggested_role": role_name,
        "suggested_questions": q_texts[:2],
        "suggested_session_type": "Communication & Articulation Mock"
    })

    # 2. Confidence & Body Language Drill
    conf_score = round(latest_report.confidence_score or latest_report.eye_contact_score or 65.0)
    drills.append({
        "id": "drill-confidence-gaze",
        "title": "Camera Eye-Level Gaze Lock & Confidence Stance",
        "tag": "eye_contact",
        "duration": "4 Mins",
        "desc": f"Your latest confidence metric registered at {conf_score}%. Lock steady eye gaze on the lens to project executive presence and reduce nervous head movements.",
        "category": "Confidence Activity",
        "is_personalized": True,
        "score_context": f"Confidence Score: {conf_score}%",
        "suggested_topic": "Confidence & Gaze Lock",
        "suggested_category": "HR",
        "suggested_role": role_name,
        "suggested_questions": [
            f"What makes you uniquely qualified for this {role_name} position?",
            "How do you maintain confidence when you encounter a problem you don't know the answer to?"
        ],
        "suggested_session_type": "Confidence Building Mock"
    })

    # 3. Weak Topics & Technical Mastery Drill
    weak_items = latest_report.weaknesses if isinstance(latest_report.weaknesses, list) else []
    weak_summary = ", ".join([w if isinstance(w, str) else str(w.get("area", "")) for w in weak_items[:2]]) if weak_items else "Technical Depth & System Architecture"
    drills.append({
        "id": "drill-targeted-weakness",
        "title": f"{role_name} Core Competency Remediation",
        "tag": "technical",
        "duration": "8 Mins",
        "desc": f"Target your latest flagged growth areas: {weak_summary}. Deliver a structured 2-minute architectural solution emphasizing scalability and clean trade-offs.",
        "category": "Weak Topic Remediation",
        "is_personalized": True,
        "score_context": f"Content Score: {round(latest_report.content_score or 60)}%",
        "suggested_topic": f"{role_name} - {weak_summary}",
        "suggested_category": "Technical",
        "suggested_role": role_name,
        "suggested_questions": q_texts[1:3] if len(q_texts) > 2 else q_texts,
        "suggested_session_type": f"Targeted {role_name} Technical Mock"
    })

    # 4. Behavioral & STAR Method Storytelling Drill
    drills.append({
        "id": "drill-star-story",
        "title": "STAR Method Behavioral Storytelling Drill",
        "tag": "star_method",
        "duration": "8 Mins",
        "desc": "Structure your behavioral answers strictly dividing your response into 15s Situation, 15s Task, 45s Action, and 15s quantifiable Result.",
        "category": "Behavioral",
        "is_personalized": True,
        "score_context": "Framework Discipline",
        "suggested_topic": "STAR Method Behavioral Stories",
        "suggested_category": "Behavioral",
        "suggested_role": role_name,
        "suggested_questions": [
            "Tell me about a time you resolved a critical production incident under severe time pressure.",
            "Describe a situation where you convinced senior team members to adopt a new technical standard."
        ],
        "suggested_session_type": "Behavioral STAR Deep Dive"
    })

    return drills

@router.get("/questions", response_model=List[QuestionPracticeResponse])
def get_practice_questions(
    category_id: Optional[str] = Query(None, description="Category ID filter"),
    job_role_id: Optional[str] = Query(None, description="Job role ID filter"),
    difficulty_id: Optional[str] = Query(None, description="Difficulty ID filter"),
    search: Optional[str] = Query(None, description="Search keyword in question text"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve practice questions from question bank with sample answers and expected keywords."""
    query = db.query(Question).filter(Question.is_active == True)

    if category_id:
        query = query.filter(Question.category_id == category_id)
    if job_role_id:
        query = query.filter(Question.job_role_id == job_role_id)
    if difficulty_id:
        query = query.filter(Question.difficulty_id == difficulty_id)
    if search:
        query = query.filter(Question.text.ilike(f"%{search.strip()}%"))

    questions = query.limit(limit).all()

    result = []
    for q in questions:
        result.append(QuestionPracticeResponse(
            id=q.id,
            text=q.text,
            category_name=q.category.name if q.category else "General",
            job_role_name=q.job_role.name if q.job_role else "All Roles",
            difficulty_name=q.difficulty.name if q.difficulty else "Intermediate",
            expected_keywords=q.expected_keywords or [],
            sample_answer=q.sample_answer
        ))
    return result

@router.get("/questions/{question_id}", response_model=QuestionPracticeResponse)
def get_practice_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Get single question drill details with sample answer."""
    q = db.query(Question).filter(
        Question.id == question_id,
        Question.is_active == True
    ).first()

    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    return QuestionPracticeResponse(
        id=q.id,
        text=q.text,
        category_name=q.category.name if q.category else "General",
        job_role_name=q.job_role.name if q.job_role else "All Roles",
        difficulty_name=q.difficulty.name if q.difficulty else "Intermediate",
        expected_keywords=q.expected_keywords or [],
        sample_answer=q.sample_answer
    )
