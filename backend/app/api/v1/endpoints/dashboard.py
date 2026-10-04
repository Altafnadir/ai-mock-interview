from datetime import datetime, timedelta
from typing import Any, List, Dict, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_current_user
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.interview import InterviewSession
from app.db.models.resume import Resume
from app.db.models.report import Report, Recommendation
from app.db.models.resource import LearningResource
from app.schemas.dashboard import (
    CandidateDashboardResponse,
    RecentSessionSummary,
    DashboardOverviewResponse,
    DashboardMetrics,
    CompetencyRadarItem,
    RecentSessionItem,
    WeakAreaAlert,
)

router = APIRouter()

@router.get("/candidate", response_model=CandidateDashboardResponse)
def get_candidate_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Fetch aggregated performance telemetry, readiness index, and recommendation feed for candidate."""
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

    total_interviews = len(sessions)
    session_ids = [s.id for s in sessions]
    reports = db.query(Report).filter(Report.session_id.in_(session_ids)).all() if session_ids else []

    scores = [r.overall_score for r in reports]
    avg_score = round(sum(scores) / max(len(scores), 1), 1) if scores else 0.0
    best_score = max(scores) if scores else 0.0

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    month_sessions = [s for s in sessions if s.created_at >= thirty_days_ago]
    interviews_this_month = len(month_sessions)

    readiness = min(round((avg_score * 0.7) + (min(total_interviews * 5, 30)), 1), 98.0) if total_interviews > 0 else 0.0

    dim_averages = {
        "content": round(sum(r.content_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
        "communication": round(sum(r.communication_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
        "voice": round(sum(r.voice_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
        "vision": round(sum(r.eye_contact_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
        "confidence": round(sum(r.confidence_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
        "grammar": round(sum(r.grammar_score for r in reports) / max(len(reports), 1), 1) if reports else 0.0,
    }

    score_trend = []
    for r in sorted(reports, key=lambda x: x.generated_at):
        score_trend.append({
            "date": r.generated_at.strftime("%b %d"),
            "score": r.overall_score
        })

    recent_summaries = []
    report_map = {r.session_id: r for r in reports}
    for s in sessions[:5]:
        rep = report_map.get(s.id)
        recent_summaries.append(RecentSessionSummary(
            id=s.id,
            job_role_name=s.job_role.name if s.job_role else "Software Engineer",
            category_name=s.category.name if s.category else "Technical",
            difficulty_name=s.difficulty.name if s.difficulty else "Intermediate",
            status=s.status,
            overall_score=rep.overall_score if rep else None,
            final_verdict=rep.final_verdict if rep else None,
            created_at=s.created_at
        ))

    recs = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).all() if current_user else []

    tag_counts = {}
    for r in recs:
        tag_counts[r.weak_area_tag] = tag_counts.get(r.weak_area_tag, 0) + 1

    weak_areas = [{"tag": tag.replace("_", " ").title(), "count": cnt} for tag, cnt in tag_counts.items()]
    if not weak_areas:
        weak_areas = [
            {"tag": "STAR Method", "count": 1},
            {"tag": "Filler Words", "count": 1}
        ]

    rec_resources = []
    db_resources = db.query(LearningResource).filter(LearningResource.is_active == True).limit(4).all()
    for res in db_resources:
        rec_resources.append({
            "id": res.id,
            "title": res.title,
            "url": res.url,
            "platform": res.platform,
            "weak_area_tag": res.weak_area_tag,
            "difficulty": res.difficulty
        })

    return CandidateDashboardResponse(
        total_interviews=total_interviews,
        average_score=avg_score,
        best_score=best_score,
        interviews_this_month=interviews_this_month,
        readiness_percentage=readiness,
        dimension_averages=dim_averages,
        score_trend=score_trend,
        recent_sessions=recent_summaries,
        weak_areas=weak_areas,
        recommended_resources=rec_resources
    )

def score_to_label(score: float) -> str:
    if score >= 88: return "Excellent"
    if score >= 83: return "Very Good"
    if score >= 70: return "Good"
    if score >= 55: return "Needs Improvement"
    return "Needs Practice"

@router.get("/overview", response_model=DashboardOverviewResponse)
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Provides high-level dashboard data for candidates (KPIs, Radar, Trend, Recent, Weak Area Alert, Recommendation)."""
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.desc()).all()

    total_interviews = len(sessions)
    session_ids = [s.id for s in sessions]
    reports = db.query(Report).filter(Report.session_id.in_(session_ids)).all() if session_ids else []

    scores = [r.overall_score for r in reports]
    avg_score = round(sum(scores) / max(len(scores), 1), 1) if scores else 0.0
    highest_score = max(scores) if scores else 0.0

    # Calculate streak (consecutive days with sessions)
    session_dates = sorted(list({s.created_at.date() for s in sessions}), reverse=True)
    streak = 0
    today = datetime.utcnow().date()
    current_check = today
    if session_dates and (session_dates[0] == today or session_dates[0] == today - timedelta(days=1)):
        for d in session_dates:
            if d == current_check or d == current_check - timedelta(days=1):
                streak += 1
                current_check = d
            else:
                break
    else:
        streak = 1 if total_interviews > 0 else 0

    # Deltas
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    two_weeks_ago = datetime.utcnow() - timedelta(days=14)
    this_week_sessions = [s for s in sessions if s.created_at >= one_week_ago]
    last_week_sessions = [s for s in sessions if two_weeks_ago <= s.created_at < one_week_ago]
    interviews_delta_week = len(this_week_sessions) or (2 if total_interviews > 0 else 0)

    this_week_scores = [r.overall_score for r in reports if r.generated_at >= one_week_ago]
    last_week_scores = [r.overall_score for r in reports if two_weeks_ago <= r.generated_at < one_week_ago]
    if this_week_scores and last_week_scores:
        score_delta_week = round((sum(this_week_scores) / len(this_week_scores)) - (sum(last_week_scores) / len(last_week_scores)), 1)
    else:
        score_delta_week = 4.0 if total_interviews > 0 else 0.0

    # Dimension scores
    dim_content = round(sum(r.content_score for r in reports) / max(len(reports), 1), 1) if reports else 75.0
    dim_voice = round(sum(r.voice_score for r in reports) / max(len(reports), 1), 1) if reports else 75.0
    dim_vision = round(sum(r.eye_contact_score for r in reports) / max(len(reports), 1), 1) if reports else 75.0
    dim_body = round(sum(r.body_language_score for r in reports) / max(len(reports), 1), 1) if reports else 75.0
    dim_grammar = round(sum(r.grammar_score for r in reports) / max(len(reports), 1), 1) if reports else (88.0 if total_interviews > 0 else 75.0)
    dim_conf = round(sum(r.confidence_score for r in reports) / max(len(reports), 1), 1) if reports else (82.0 if total_interviews > 0 else 75.0)
    dim_comm = round(sum(r.communication_score for r in reports) / max(len(reports), 1), 1) if reports else (75.0 if total_interviews > 0 else 70.0)

    # Resume Score
    resume = db.query(Resume).filter(Resume.user_id == current_user.id, Resume.is_active == True).first()
    resume_score = resume.analysis.resume_score if (resume and resume.analysis and resume.analysis.resume_score) else (85.0 if total_interviews > 0 else 80.0)

    score_trend = []
    for idx, r in enumerate(sorted(reports, key=lambda x: x.generated_at)):
        score_trend.append({
            "date": f"Session {idx + 1}" if len(reports) <= 5 else r.generated_at.strftime("%b %d"),
            "score": round(r.overall_score, 1)
        })

    # Performance overview (Mon-Sun)
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    performance_overview = []
    for i in range(6, -1, -1):
        day_date = (datetime.utcnow() - timedelta(days=i)).date()
        day_name = day_names[day_date.weekday()]
        day_reports = [r for r in reports if r.generated_at.date() == day_date]
        day_score = round(sum(r.overall_score for r in day_reports) / len(day_reports), 1) if day_reports else None
        performance_overview.append({
            "day": day_name,
            "date": day_date.strftime("%Y-%m-%d"),
            "score": day_score if day_score is not None else (avg_score if total_interviews > 0 else 70.0)
        })

    competency_radar = [
        CompetencyRadarItem(subject="Technical Content", value=dim_content),
        CompetencyRadarItem(subject="Voice & Tone", value=dim_voice),
        CompetencyRadarItem(subject="Eye Contact", value=dim_vision),
        CompetencyRadarItem(subject="Body Language", value=dim_body),
        CompetencyRadarItem(subject="Grammar", value=dim_grammar),
        CompetencyRadarItem(subject="Confidence", value=dim_conf),
    ]

    report_map = {r.session_id: r for r in reports}
    recent_sessions = []
    for s in sessions[:5]:
        rep = report_map.get(s.id)
        recent_sessions.append(RecentSessionItem(
            id=s.id,
            role_name=s.job_role.name if s.job_role else "Software Engineer",
            category_name=s.category.name if s.category else "Technical",
            difficulty_name=s.difficulty.name if s.difficulty else "Intermediate",
            score=round(rep.overall_score, 1) if rep else None,
            verdict=rep.final_verdict if rep else None,
            date=s.created_at.strftime("%Y-%m-%d")
        ))

    # Weak area alert
    recs = db.query(Recommendation).filter(Recommendation.user_id == current_user.id).all()
    weak_alert = None
    if recs:
        tag_counts = {}
        for r in recs:
            tag_counts[r.weak_area_tag] = tag_counts.get(r.weak_area_tag, 0) + 1
        top_tag = max(tag_counts.items(), key=lambda x: x[1])[0]
        latest_rec = [r for r in recs if r.weak_area_tag == top_tag][-1]
        weak_alert = WeakAreaAlert(
            tag=top_tag,
            title=top_tag.replace("_", " ").title(),
            suggestion=latest_rec.practice_suggestion
        )
    else:
        weak_alert = WeakAreaAlert(
            tag="filler_words",
            title="Verbal Crutches & Filler Words",
            suggestion="Focus on improving your eye contact and reducing filler words. Practice more behavioral questions."
        )

    ai_recommendation = {
        "text": weak_alert.suggestion,
        "tag": weak_alert.tag,
        "title": weak_alert.title,
        "action_text": "Start Recommended Practice"
    }

    return DashboardOverviewResponse(
        metrics=DashboardMetrics(
            total_interviews=total_interviews,
            average_score=avg_score,
            highest_score=highest_score,
            practice_streak_days=streak,
            confidence_score=dim_conf,
            communication_score=dim_comm,
            grammar_score=dim_grammar,
            resume_score=resume_score,
            interviews_delta_week=interviews_delta_week,
            score_delta_week=score_delta_week,
            confidence_label=score_to_label(dim_conf),
            communication_label=score_to_label(dim_comm),
            grammar_label=score_to_label(dim_grammar),
            resume_label=score_to_label(resume_score),
            average_score_label=score_to_label(avg_score if avg_score > 0 else 75.0),
            practice_streak=f"{max(1, streak)} Days" if total_interviews > 0 else "0 Days",
            next_goal={"text": "Complete 3 interviews this week", "current": min(3, total_interviews), "target": 3}
        ),
        score_trend=score_trend,
        competency_radar=competency_radar,
        recent_sessions=recent_sessions,
        weak_area_alert=weak_alert,
        ai_recommendation=ai_recommendation,
        performance_overview=performance_overview
    )

@router.get("/performance")
def get_dashboard_performance(
    range_type: str = Query("week", alias="range", pattern="^(week|month)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retrieve time series data for the Performance Overview chart."""
    days = 7 if range_type == "week" else 30
    cutoff = datetime.utcnow() - timedelta(days=days)
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id,
        InterviewSession.created_at >= cutoff
    ).all()
    s_ids = [s.id for s in sessions]
    reports = db.query(Report).filter(Report.session_id.in_(s_ids)).all() if s_ids else []

    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    series = []
    for i in range(days - 1, -1, -1):
        d = (datetime.utcnow() - timedelta(days=i)).date()
        d_name = day_names[d.weekday()] if days == 7 else d.strftime("%b %d")
        matched = [r for r in reports if r.generated_at.date() == d]
        sc = round(sum(r.overall_score for r in matched) / len(matched), 1) if matched else None
        series.append({
            "label": d_name,
            "date": d.strftime("%Y-%m-%d"),
            "score": sc
        })
    return {"range": range_type, "data": series}

@router.get("/recommendation")
def get_dashboard_recommendation(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """AI recommendation generated from candidate's weakest metrics."""
    recs = db.query(Recommendation).filter(Recommendation.user_id == current_user.id).all()
    if recs:
        latest = recs[-1]
        return {
            "title": latest.weak_area_tag.replace("_", " ").title(),
            "tag": latest.weak_area_tag,
            "text": latest.practice_suggestion,
            "action_text": "Start Recommended Practice"
        }
    return {
        "title": "Verbal Crutches & Fluency",
        "tag": "filler_words",
        "text": "Focus on improving your eye contact and reducing filler words. Practice more behavioral questions.",
        "action_text": "Start Recommended Practice"
    }


@router.get("/trends")
def get_dashboard_trends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Historical progression of scores and dimensions across candidate sessions."""
    sessions = db.query(InterviewSession).filter(
        InterviewSession.user_id == current_user.id
    ).order_by(InterviewSession.created_at.asc()).all()

    session_ids = [s.id for s in sessions]
    reports = db.query(Report).filter(Report.session_id.in_(session_ids)).all() if session_ids else []
    report_map = {r.session_id: r for r in reports}

    trend_items = []
    for idx, s in enumerate(sessions):
        rep = report_map.get(s.id)
        if rep:
            trend_items.append({
                "session_index": idx + 1,
                "session_id": s.id,
                "date": s.created_at.strftime("%Y-%m-%d"),
                "overall_score": rep.overall_score,
                "content_score": rep.content_score,
                "communication_score": rep.communication_score,
                "voice_score": rep.voice_score,
                "vision_score": rep.eye_contact_score,
                "confidence_score": rep.confidence_score,
                "grammar_score": rep.grammar_score,
            })

    return {"trends": trend_items}

@router.get("/compare")
def compare_sessions(
    ids: str = Query(..., description="Comma-separated session IDs to compare"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Side-by-side comparison of 2 or more interview sessions."""
    session_id_list = [sid.strip() for sid in ids.split(",") if sid.strip()]
    if not session_id_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No session IDs provided")

    sessions = db.query(InterviewSession).filter(
        InterviewSession.id.in_(session_id_list),
        InterviewSession.user_id == current_user.id
    ).all()

    reports = db.query(Report).filter(Report.session_id.in_(session_id_list)).all()
    rep_map = {r.session_id: r for r in reports}

    comparison = []
    for s in sessions:
        r = rep_map.get(s.id)
        comparison.append({
            "session_id": s.id,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "job_role": s.job_role.name if s.job_role else "Unknown",
            "category": s.category.name if s.category else "Unknown",
            "difficulty": s.difficulty.name if s.difficulty else "Unknown",
            "status": s.status,
            "overall_score": r.overall_score if r else None,
            "content_score": r.content_score if r else None,
            "communication_score": r.communication_score if r else None,
            "voice_score": r.voice_score if r else None,
            "vision_score": r.eye_contact_score if r else None,
            "confidence_score": r.confidence_score if r else None,
            "grammar_score": r.grammar_score if r else None,
            "final_verdict": r.final_verdict if r else None,
        })

    return {"comparison": comparison}

