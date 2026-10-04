import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../ui/Sidebar';
import Topbar from '../ui/Topbar';
import MobileBottomNav from '../ui/MobileBottomNav';
import ToastContainer from '../common/Toast';

export default function CandidateLayout() {
  return (
    <div className="min-h-screen flex bg-[#F5F7FB] dark:bg-slate-950 text-slate-900 dark:text-slate-100 antialiased font-sans">
      {/* Desktop/Tablet Sticky Sidebar */}
      <Sidebar role="candidate" className="hidden sm:flex" />

      {/* Main App Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto pb-24 sm:pb-8">
          <Outlet />
        </main>
      </div>

      {/* Mobile Bottom Navigation */}
      <MobileBottomNav />
      <ToastContainer />
    </div>
  );
}
