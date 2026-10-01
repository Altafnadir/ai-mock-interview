import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Layouts
import CandidateLayout from '../components/layout/CandidateLayout';
import AdminLayout from '../components/layout/AdminLayout';

// Route Guards
import ProtectedRoute from './ProtectedRoute';
import RoleRoute from './RoleRoute';

// Public & Auth Pages
import LandingPage from '../pages/public/LandingPage';
import LoginPage from '../pages/auth/LoginPage';
import RegisterPage from '../pages/auth/RegisterPage';
import OTPVerificationPage from '../pages/auth/OTPVerificationPage';
import ForgotPasswordPage from '../pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '../pages/auth/ResetPasswordPage';
import AdminLoginPage from '../pages/auth/AdminLoginPage';
import PublicSharedReport from '../pages/shared/PublicSharedReport';

// Candidate Pages
import DashboardPage from '../pages/candidate/DashboardPage';
import ProfilePage from '../pages/candidate/ProfilePage';
import ResumePage from '../pages/candidate/ResumePage';
import InterviewSetupPage from '../pages/candidate/InterviewSetupPage';
import InterviewRoomPage from '../pages/candidate/InterviewRoomPage';
import ProcessingPage from '../pages/candidate/ProcessingPage';
import ReportPage from '../pages/candidate/ReportPage';
import HistoryPage from '../pages/candidate/HistoryPage';
import ResourcesPage from '../pages/candidate/ResourcesPage';
import PracticePage from '../pages/candidate/PracticePage';
import NotificationsPage from '../pages/candidate/NotificationsPage';

// Admin Pages
import AdminDashboardPage from '../pages/admin/AdminDashboardPage';
import UserManagementPage from '../pages/admin/UserManagementPage';
import QuestionManagementPage from '../pages/admin/QuestionManagementPage';
import ContentManagementPage from '../pages/admin/ContentManagementPage';
import ResourcesAdminPage from '../pages/admin/ResourcesAdminPage';
import SessionManagementPage from '../pages/admin/SessionManagementPage';
import ReportManagementPage from '../pages/admin/ReportManagementPage';
import AnalyticsPage from '../pages/admin/AnalyticsPage';
import AdminNotificationsPage from '../pages/admin/AdminNotificationsPage';
import MonitoringPage from '../pages/admin/MonitoringPage';
import SecurityBackupPage from '../pages/admin/SecurityBackupPage';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public Pages */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/verify-otp" element={<OTPVerificationPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route path="/admin/login" element={<AdminLoginPage />} />
      <Route path="/shared/:token" element={<PublicSharedReport />} />

      {/* Immersive Fullscreen Interview Room & Processing (Protected Candidate) */}
      <Route
        path="/interview/:id/room"
        element={
          <RoleRoute allowedRoles={['candidate', 'admin']}>
            <InterviewRoomPage />
          </RoleRoute>
        }
      />
      <Route
        path="/interview/:id/processing"
        element={
          <RoleRoute allowedRoles={['candidate', 'admin']}>
            <ProcessingPage />
          </RoleRoute>
        }
      />

      {/* Candidate Portal Routes (Shared CandidateLayout) */}
      <Route
        element={
          <RoleRoute allowedRoles={['candidate', 'admin']}>
            <CandidateLayout />
          </RoleRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/resume" element={<ResumePage />} />
        <Route path="/resumes" element={<ResumePage />} />

        <Route path="/interview/setup" element={<InterviewSetupPage />} />
        <Route path="/reports/:sessionId" element={<ReportPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/resources" element={<ResourcesPage />} />
        <Route path="/practice" element={<PracticePage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
      </Route>

      {/* Admin Portal Routes (Shared AdminLayout) */}
      <Route
        element={
          <RoleRoute allowedRoles={['admin']}>
            <AdminLayout />
          </RoleRoute>
        }
      >
        <Route path="/admin" element={<AdminDashboardPage />} />
        <Route path="/admin/users" element={<UserManagementPage />} />
        <Route path="/admin/questions" element={<QuestionManagementPage />} />
        <Route path="/admin/content" element={<ContentManagementPage />} />
        <Route path="/admin/resources" element={<ResourcesAdminPage />} />
        <Route path="/admin/sessions" element={<SessionManagementPage />} />
        <Route path="/admin/reports" element={<ReportManagementPage />} />
        <Route path="/admin/analytics" element={<AnalyticsPage />} />
        <Route path="/admin/notifications" element={<AdminNotificationsPage />} />
        <Route path="/admin/monitoring" element={<MonitoringPage />} />
        <Route path="/admin/security" element={<SecurityBackupPage />} />
      </Route>

      {/* Catch-all */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
