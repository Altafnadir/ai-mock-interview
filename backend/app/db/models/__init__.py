from app.db.models.user import (
    User,
    CandidateProfile,
    OTPCode,
    PasswordResetToken,
    RefreshToken,
    LoginHistory,
)
from app.db.models.resume import (
    Resume,
    ResumeAnalysis,
)
from app.db.models.interview import (
    JobRole,
    InterviewCategory,
    DifficultyLevel,
    Question,
    QuestionSet,
    InterviewSession,
    SessionQuestion,
    Answer,
)
from app.db.models.analysis import (
    AnalysisVoice,
    AnalysisVision,
    AnalysisEmotion,
    AnalysisGrammar,
    AnalysisContent,
)
from app.db.models.report import (
    Report,
    ReportShare,
    Recommendation,
)
from app.db.models.resource import (
    LearningResource,
    LearningProgress,
    FeedbackTemplate,
)
from app.db.models.coach import (
    CoachConversation,
    CoachMessage,
)
from app.db.models.achievement import (
    Badge,
    UserBadge,
    PointsLedger,
)
from app.db.models.goal import (
    PracticeGoal,
)
from app.db.models.preference import (
    NotificationPreference,
)
from app.db.models.system import (
    Notification,
    ActivityLog,
    SystemSetting,
    ProcessingJob,
    ErrorLog,
    Backup,
)

__all__ = [
    "User",
    "CandidateProfile",
    "OTPCode",
    "PasswordResetToken",
    "RefreshToken",
    "LoginHistory",
    "Resume",
    "ResumeAnalysis",
    "JobRole",
    "InterviewCategory",
    "DifficultyLevel",
    "Question",
    "QuestionSet",
    "InterviewSession",
    "SessionQuestion",
    "Answer",
    "AnalysisVoice",
    "AnalysisVision",
    "AnalysisEmotion",
    "AnalysisGrammar",
    "AnalysisContent",
    "Report",
    "ReportShare",
    "Recommendation",
    "LearningResource",
    "LearningProgress",
    "FeedbackTemplate",
    "CoachConversation",
    "CoachMessage",
    "Badge",
    "UserBadge",
    "PointsLedger",
    "PracticeGoal",
    "NotificationPreference",
    "Notification",
    "ActivityLog",
    "SystemSetting",
    "ProcessingJob",
    "ErrorLog",
    "Backup",
]

