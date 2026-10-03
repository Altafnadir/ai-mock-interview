import React from 'react';
import { BrowserRouter, useLocation } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import ToastContainer from './components/common/Toast';
import SplashScreen from './components/common/SplashScreen';

function AppLayout() {
  const location = useLocation();

  return (
    <>
      <SplashScreen currentPath={location.pathname} />
      <AppRoutes />
      <ToastContainer />
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}

