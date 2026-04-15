/**
 * App root — defines routing structure with auth protection.
 * All authenticated routes use MainLayout with role-based sidebar.
 */

import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import MainLayout from './components/Layout/MainLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import ComingSoon from './pages/ComingSoon';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-center" style={{ height: '100vh' }}>
        <div className="spinner" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<Login />} />

      {/* Protected — all wrapped in MainLayout */}
      <Route
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />

        {/* Faculty */}
        <Route path="my-proposals" element={<ComingSoon />} />
        <Route path="proposals/new" element={<ComingSoon />} />
        <Route path="proposals/:id" element={<ComingSoon />} />
        <Route path="my-progress" element={<ComingSoon />} />
        <Route path="my-acceptance" element={<ComingSoon />} />

        {/* Staff */}
        <Route path="periods" element={<ComingSoon />} />
        <Route path="proposals" element={<ComingSoon />} />
        <Route path="reviews" element={<ComingSoon />} />
        <Route path="councils" element={<ComingSoon />} />
        <Route path="progress" element={<ComingSoon />} />
        <Route path="acceptance" element={<ComingSoon />} />
        <Route path="reports" element={<ComingSoon />} />

        {/* Leadership */}
        <Route path="approvals" element={<ComingSoon />} />

        {/* Reviewer */}
        <Route path="assigned" element={<ComingSoon />} />
        <Route path="assigned/:id/review" element={<ComingSoon />} />
        <Route path="councils/schedule" element={<ComingSoon />} />

        {/* Admin */}
        <Route path="users" element={<ComingSoon />} />
        <Route path="catalog" element={<ComingSoon />} />

        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
