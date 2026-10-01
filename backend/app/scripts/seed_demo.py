import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models.user import User, CandidateProfile
from app.db.models.resume import Resume, ResumeAnalysis
from app.db.models.interview import JobRole, InterviewCategory, DifficultyLevel, InterviewSession, SessionQuestion, Answer
from app.db.models.analysis import AnalysisVoice, AnalysisVision, AnalysisEmotion, AnalysisGrammar, AnalysisContent
from app.db.models.report import Report, Recommendation
from app.db.models.resource import LearningResource
from app.db.models.system import Notification
from app.core.security import get_password_hash

def seed_demo(db: Session = None):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        demo_email = "candidate@gims.edu.pk"
        candidate = db.query(User).filter(User.email == demo_email).first()
        if not candidate:
            candidate = User(
                full_name="Hamza Ali (Demo Candidate)",
                email=demo_email,
                password_hash=get_password_hash("CandidatePassword123!"),
                role="candidate",
                is_active=True,
                is_email_verified=True,
                auth_provider="local"
            )
            db.add(candidate)
            db.flush()

            # Profile
            profile = CandidateProfile(
                user_id=candidate.id,
                phone="+92 300 1234567",
                education=[
                    {"degree": "BS Software Engineering", "institution": "PMAS-Arid Agriculture University (GIMS)", "year": "2024", "gpa": "3.75"}
                ],
                skills=["React.js", "JavaScript", "Python", "FastAPI", "SQL", "Tailwind CSS", "Git", "Docker"],
                work_experience=[
                    {"role": "Frontend Intern", "company": "TechSolutions Islamabad", "duration": "6 months", "highlights": "Built responsive React dashboards and optimized web performance."}
                ],
                certifications=[
                    {"title": "Meta Frontend Developer Professional Certificate", "issuer": "Coursera", "year": "2023"}
                ],
                preferred_job_roles=["Frontend Developer", "Full Stack Developer", "Software Engineer"],
                experience_level="beginner"
            )
            db.add(profile)

            # Resume
            resume = Resume(
                user_id=candidate.id,
                file_path="./storage/resumes/sample_resume_hamza.pdf",
                original_filename="Hamza_Ali_Software_Engineer_Resume.pdf",
                file_type="pdf",
                is_active=True
            )
            db.add(resume)
            db.flush()

            analysis = ResumeAnalysis(
                resume_id=resume.id,
                extracted_education=profile.education,
                extracted_skills=profile.skills,
                extracted_projects=[
                    {"title": "AI Mock Interview System", "tech_stack": "React, FastAPI, MediaPipe", "description": "Built AI preparation web application with automated performance scoring."}
                ],
                extracted_certifications=profile.certifications,
                extracted_experience=profile.work_experience,
                missing_skills=["TypeScript", "Kubernetes", "AWS Cloud Architecture", "GraphQL"],
                weak_sections=["Quantifiable project metrics in experience descriptions", "Cloud deployment specifics"],
                improvement_suggestions=[
                    "Add measurable outcome metrics (e.g. 'improved page load times by 35%').",
                    "Highlight TypeScript experience alongside React.",
                    "Include a dedicated section for distributed systems and API design."
                ],
                status="analyzed",
                raw_text="Hamza Ali - BS Software Engineering candidate with experience in React, Python, and FastAPI."
            )
            db.add(analysis)

            # Look up metadata
            frontend_role = db.query(JobRole).filter(JobRole.name == "Frontend Developer").first()
            fullstack_role = db.query(JobRole).filter(JobRole.name == "Full Stack Developer").first()
            swe_role = db.query(JobRole).filter(JobRole.name == "Software Engineer").first()

            tech_cat = db.query(InterviewCategory).filter(InterviewCategory.name == "Technical").first()
            mixed_cat = db.query(InterviewCategory).filter(InterviewCategory.name == "Mixed").first()
            behav_cat = db.query(InterviewCategory).filter(InterviewCategory.name == "Behavioral").first()

            beg_diff = db.query(DifficultyLevel).filter(DifficultyLevel.name == "Beginner").first()
            int_diff = db.query(DifficultyLevel).filter(DifficultyLevel.name == "Intermediate").first()

            # Session 1: Frontend Developer (Technical, Beginner) - Excellent Score (88.5)
            s1_time = datetime.utcnow() - timedelta(days=5)
            s1 = InterviewSession(
                user_id=candidate.id,
                resume_id=resume.id,
                job_role_id=frontend_role.id,
                category_id=tech_cat.id,
                difficulty_id=beg_diff.id,
                status="analyzed",
                started_at=s1_time,
                ended_at=s1_time + timedelta(minutes=15),
                total_questions=3,
                duration_seconds=900,
                video_path="./storage/recordings/demo_session_1.webm",
                audio_path="./storage/recordings/demo_session_1.wav",
                created_at=s1_time
            )
            db.add(s1)
            db.flush()

            # Questions & Answers for S1
            sq1 = SessionQuestion(
                session_id=s1.id,
                order_index=1,
                question_text="What is the difference between let, const, and var in modern JavaScript?",
                source="bank",
                time_limit_seconds=120,
                status="answered",
                started_at=s1_time,
                ended_at=s1_time + timedelta(seconds=90)
            )
            db.add(sq1)
            db.flush()

            ans1 = Answer(
                session_question_id=sq1.id,
                transcript="In modern JavaScript, var is function-scoped and hoisted with an undefined value. In contrast, let and const are block-scoped and remain in the temporal dead zone until declared. const prevents reassignment while let allows mutating the reference.",
                word_count=41,
                duration_seconds=35.0,
                filler_word_count=1,
                filler_words_breakdown={"um": 1},
                speaking_rate_wpm=145.0
            )
            db.add(ans1)

            c_eval1 = AnalysisContent(
                session_question_id=sq1.id,
                relevance_score=92.0,
                completeness_score=88.0,
                technical_accuracy_score=95.0,
                star_score=75.0,
                star_breakdown={"S": "Demonstrated technical foundation", "T": "Defined scope differences", "A": "Detailed TDZ and hoisting", "R": "Accurate summary"},
                keyword_match_score=90.0,
                matched_keywords=["scope", "hoisting", "temporal dead zone", "reassignment"],
                logical_flow_score=90.0,
                llm_comment="Concise, highly articulate explanation with accurate technical terminology."
            )
            db.add(c_eval1)

            # Analyses for S1
            v_ana1 = AnalysisVoice(
                session_id=s1.id,
                speaking_speed_wpm=142.5,
                avg_pitch_hz=165.2,
                pitch_variance=24.5,
                tone_score=88.0,
                clarity_score=90.0,
                fluency_score=86.0,
                confidence_score=89.0,
                pause_count=4,
                avg_pause_duration=0.8,
                total_pause_duration=3.2,
                voice_stability_score=88.5
            )
            db.add(v_ana1)

            vis_ana1 = AnalysisVision(
                session_id=s1.id,
                eye_contact_percentage=86.5,
                looking_away_count=3,
                posture_score=91.0,
                slouch_percentage=4.5,
                head_movement_score=88.0,
                body_stability_score=90.0,
                sitting_position_score=92.0,
                frames_analyzed=450,
                timeline=[
                    {"time": 0, "eye_contact": 88, "posture": 92},
                    {"time": 30, "eye_contact": 85, "posture": 90},
                    {"time": 60, "eye_contact": 87, "posture": 91}
                ]
            )
            db.add(vis_ana1)

            emo_ana1 = AnalysisEmotion(
                session_id=s1.id,
                distribution={"confident": 68.0, "happy": 15.0, "neutral": 12.0, "nervous": 5.0, "smile_pct": 22.0},
                dominant_emotion="confident",
                timeline=[
                    {"time": 0, "emotion": "neutral", "confidence": 75},
                    {"time": 30, "emotion": "confident", "confidence": 88},
                    {"time": 60, "emotion": "confident", "confidence": 91}
                ]
            )
            db.add(emo_ana1)

            gram_ana1 = AnalysisGrammar(
                session_id=s1.id,
                grammar_score=92.0,
                vocabulary_score=88.0,
                sentence_structure_score=90.0,
                pronunciation_score=91.0,
                language_quality_score=91.0,
                communication_effectiveness_score=90.0,
                errors=[]
            )
            db.add(gram_ana1)

            rep1 = Report(
                session_id=s1.id,
                overall_score=88.5,
                confidence_score=89.0,
                voice_score=88.0,
                eye_contact_score=86.5,
                communication_score=90.0,
                content_score=92.0,
                body_language_score=91.0,
                grammar_score=92.0,
                strengths=[
                    "Precise explanation of technical JavaScript concepts.",
                    "Superb eye contact and upright posture throughout.",
                    "Virtually zero filler words; fluid pacing."
                ],
                weaknesses=[
                    "Could elaborate slightly more on practical browser debugging examples."
                ],
                confidence_analysis="You maintained commanding composure with calm breathing and steady eye contact.",
                communication_feedback="Structured, concise sentences with accurate technical vocabulary.",
                improvement_tips=[
                    "Continue reinforcing concepts with short production anecdotes.",
                    "Practice answering advanced React Fiber reconciliation questions."
                ],
                final_verdict="Excellent",
                generated_at=s1_time + timedelta(minutes=16)
            )
            db.add(rep1)

            # Session 2: Full Stack Developer (Mixed, Intermediate) - Good Score (76.2)
            s2_time = datetime.utcnow() - timedelta(days=2)
            s2 = InterviewSession(
                user_id=candidate.id,
                resume_id=resume.id,
                job_role_id=fullstack_role.id,
                category_id=mixed_cat.id,
                difficulty_id=int_diff.id,
                status="analyzed",
                started_at=s2_time,
                ended_at=s2_time + timedelta(minutes=18),
                total_questions=4,
                duration_seconds=1080,
                created_at=s2_time
            )
            db.add(s2)
            db.flush()

            v_ana2 = AnalysisVoice(
                session_id=s2.id,
                speaking_speed_wpm=132.0,
                avg_pitch_hz=158.0,
                pitch_variance=18.0,
                tone_score=75.0,
                clarity_score=78.0,
                fluency_score=74.0,
                confidence_score=76.0,
                pause_count=12,
                avg_pause_duration=1.2,
                total_pause_duration=14.4,
                voice_stability_score=76.0
            )
            db.add(v_ana2)

            vis_ana2 = AnalysisVision(
                session_id=s2.id,
                eye_contact_percentage=72.0,
                looking_away_count=8,
                posture_score=78.0,
                slouch_percentage=12.0,
                head_movement_score=76.0,
                body_stability_score=75.0,
                sitting_position_score=80.0,
                frames_analyzed=540,
                timeline=[]
            )
            db.add(vis_ana2)

            emo_ana2 = AnalysisEmotion(
                session_id=s2.id,
                distribution={"confident": 52.0, "nervous": 18.0, "neutral": 25.0, "happy": 5.0, "smile_pct": 12.0},
                dominant_emotion="confident",
                timeline=[]
            )
            db.add(emo_ana2)

            gram_ana2 = AnalysisGrammar(
                session_id=s2.id,
                grammar_score=78.0,
                vocabulary_score=76.0,
                sentence_structure_score=77.0,
                pronunciation_score=80.0,
                language_quality_score=78.0,
                communication_effectiveness_score=75.0,
                errors=[
                    {"message": "Possible agreement error", "offset": 12, "suggestion": "were"}
                ]
            )
            db.add(gram_ana2)

            rep2 = Report(
                session_id=s2.id,
                overall_score=76.2,
                confidence_score=76.0,
                voice_score=75.0,
                eye_contact_score=72.0,
                communication_score=75.0,
                content_score=79.0,
                body_language_score=78.0,
                grammar_score=78.0,
                strengths=[
                    "Sound conceptual knowledge of full-stack API integration.",
                    "Handled database indexing queries with good clarity."
                ],
                weaknesses=[
                    "Occasional hesitations and downward glances during complex explanations.",
                    "Slight reliance on filler words ('um', 'like')."
                ],
                confidence_analysis="Confidence remained steady overall, but dipped during deeper system design questions.",
                communication_feedback="Solid communication that can be enhanced by pausing before speaking instead of using fillers.",
                improvement_tips=[
                    "Practice silent pauses instead of verbal crutches.",
                    "Maintain eye level with the camera lens."
                ],
                final_verdict="Good",
                generated_at=s2_time + timedelta(minutes=19)
            )
            db.add(rep2)

            # Recommendations for S2
            rec_res = db.query(LearningResource).filter(LearningResource.weak_area_tag == "filler_words").first()
            if rec_res:
                rec1 = Recommendation(
                    user_id=candidate.id,
                    session_id=s2.id,
                    weak_area_tag="filler_words",
                    resource_id=rec_res.id,
                    practice_suggestion="Watch 'How to Stop Saying Um and Uh' and practice 2-minute timed drill answers without fillers."
                )
                db.add(rec1)

            # Notifications
            n1 = Notification(
                user_id=candidate.id,
                title="Interview Report Ready!",
                message="Your Full Stack Developer mock interview report has been analyzed and is ready to view.",
                type="report_ready",
                is_read=False
            )
            n2 = Notification(
                user_id=candidate.id,
                title="Weekly Practice Reminder",
                message="Keep your momentum going! Schedule a 15-minute mock interview session this week.",
                type="practice",
                is_read=True
            )
            db.add(n1)
            db.add(n2)

            db.commit()
            print(f"Demo candidate ({demo_email}) and 2 sample analyzed sessions created successfully!")
        else:
            print(f"Demo candidate ({demo_email}) already exists.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding demo candidate: {e}")
        raise
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_demo()
