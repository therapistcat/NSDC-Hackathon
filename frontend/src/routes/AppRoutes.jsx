import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Import components (we'll create them as needed)
import LoginPage from '../pages/Auth/LoginPage';

const AppRoutes = () => {
  const { isAuthenticated, isStudent, isRecruiter, isMentor, loading } = useAuth();

  // Show loading spinner while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-background via-surface to-background flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-4"></div>
          <p className="text-textSecondary">Loading GenZ CareerHub...</p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      {/* Public Routes */}
      <Route
        path="/login"
        element={!isAuthenticated() ? <LoginPage /> : <Navigate to="/" replace />}
      />

      {/* Protected Routes */}
      <Route
        path="/student-dashboard"
        element={
          isAuthenticated() && isStudent() ? (
            <div className="min-h-screen bg-background p-4">
              <div className="max-w-6xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  Student Dashboard
                </h1>
                <div className="card">
                  <p className="text-center text-textSecondary">
                    Student dashboard implementation coming soon!
                  </p>
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-primary/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">🎮</div>
                      <p className="font-medium">Take Quizzes</p>
                    </div>
                    <div className="bg-secondary-pink/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">🧠</div>
                      <p className="font-medium">AI Learning</p>
                    </div>
                    <div className="bg-accent/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">👥</div>
                      <p className="font-medium">Community</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      <Route
        path="/recruiter-dashboard"
        element={
          isAuthenticated() && isRecruiter() ? (
            <div className="min-h-screen bg-background p-4">
              <div className="max-w-6xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  Recruiter Dashboard
                </h1>
                <div className="card">
                  <p className="text-center text-textSecondary">
                    Recruiter dashboard implementation coming soon!
                  </p>
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-primary/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">📊</div>
                      <p className="font-medium">View Talent Pool</p>
                    </div>
                    <div className="bg-secondary-pink/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">🔍</div>
                      <p className="font-medium">Search Profiles</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      <Route
        path="/mentor-dashboard"
        element={
          isAuthenticated() && isMentor() ? (
            <div className="min-h-screen bg-background p-4">
              <div className="max-w-6xl mx-auto">
                <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  Mentor Dashboard
                </h1>
                <div className="card">
                  <p className="text-center text-textSecondary">
                    Mentor dashboard implementation coming soon!
                  </p>
                  <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-primary/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">👨‍🏫</div>
                      <p className="font-medium">Mentor Sessions</p>
                    </div>
                    <div className="bg-accent/10 p-4 rounded-lg text-center">
                      <div className="text-3xl mb-2">📈</div>
                      <p className="font-medium">Student Progress</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* Default redirects */}
      <Route
        path="/"
        element={
          isAuthenticated() ? (
            isStudent() ? <Navigate to="/student-dashboard" replace /> :
            isRecruiter() ? <Navigate to="/recruiter-dashboard" replace /> :
            isMentor() ? <Navigate to="/mentor-dashboard" replace /> :
            <Navigate to="/login" replace />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />

      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;
