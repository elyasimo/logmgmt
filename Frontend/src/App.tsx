import React, { useState, useEffect } from 'react';
import { createBrowserRouter, RouterProvider, Route, Navigate, RouteObject } from 'react-router-dom';
import { LogSearch } from './components/LogSearch';
import { Login } from './components/Login';
import { Layout } from './components/Layout';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLoginSuccess = (token: string) => {
    localStorage.setItem('token', token);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
  };

  const handleApiError = (message: string) => {
    setError(message);
  };

  const routes: RouteObject[] = [
    {
      path: "/",
      element: (
        <Layout onLogout={handleLogout} isLoggedIn={isLoggedIn}>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
              <strong className="font-bold">Error:</strong>
              <span className="block sm:inline"> {error}</span>
            </div>
          )}
          {isLoggedIn ? <LogSearch onError={handleApiError} /> : <Navigate to="/login" />}
        </Layout>
      ),
    },
    {
      path: "/login",
      element: (
        <Layout onLogout={handleLogout} isLoggedIn={isLoggedIn}>
          {isLoggedIn ? (
            <Navigate to="/" />
          ) : (
            <Login onLoginSuccess={handleLoginSuccess} onError={handleApiError} />
          )}
        </Layout>
      ),
    },
  ];

  const router = createBrowserRouter(routes, {
    future: {
      v7_relativeSplatPath: true,
    },
  });

  return <RouterProvider router={router} />;
}

export default App;

