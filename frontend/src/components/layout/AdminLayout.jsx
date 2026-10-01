import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import AdminSidebar from './AdminSidebar';
import ToastContainer from '../common/Toast';

export default function AdminLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100">
      <Navbar />
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <AdminSidebar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
      <ToastContainer />
    </div>
  );
}
