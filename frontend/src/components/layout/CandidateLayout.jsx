import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import CandidateSidebar from './CandidateSidebar';
import ToastContainer from '../common/Toast';

export default function CandidateLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <Navbar />
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <CandidateSidebar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
      <ToastContainer />
    </div>
  );
}
