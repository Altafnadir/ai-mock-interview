from fastapi import APIRouter
from app.api.v1.endpoints import auth, profile, resumes, meta, interviews, reports, dashboard, resources, practice, notifications, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(meta.router, prefix="/meta", tags=["Metadata"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(resources.router, prefix="/resources", tags=["Learning Resources"])
api_router.include_router(practice.router, prefix="/practice", tags=["Practice Drills"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Console"])

# Public / shortcut routes
api_router.add_api_route("/public/reports/{token}", reports.get_public_report, methods=["GET"], response_model=reports.ReportResponse, tags=["Reports"])
api_router.add_api_route("/public/reports/{token}/pdf", reports.download_public_report_pdf, methods=["GET"], tags=["Reports"])
api_router.add_api_route("/recommendations", resources.get_user_recommendations, methods=["GET"], response_model=list[resources.RecommendationResponse], tags=["Learning Resources"])

