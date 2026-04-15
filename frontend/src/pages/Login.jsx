/**
 * Login page — email + password form with JWT authentication.
 */

import { useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';
import './Login.css';

export default function Login() {
  const { login, isAuthenticated, loading } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (loading) {
    return (
      <div className="loading-center" style={{ height: '100vh' }}>
        <div className="spinner" />
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error('Vui lòng nhập email và mật khẩu');
      return;
    }
    setSubmitting(true);
    try {
      await login(email, password);
      toast.success('Đăng nhập thành công!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Đăng nhập thất bại';
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-bg-pattern" />

      <div className="login-card animate-fade-in">
        <div className="login-header">
          <div className="login-logo">✦</div>
          <h1 className="login-title">SciRes</h1>
          <p className="login-subtitle">Hệ thống Quản lý Nghiên cứu Khoa học</p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder="email@university.edu.vn"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Mật khẩu</label>
            <input
              id="password"
              type="password"
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-lg login-btn"
            disabled={submitting}
          >
            {submitting ? (
              <span className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} />
            ) : (
              'Đăng nhập'
            )}
          </button>
        </form>

        <div className="login-demo-info">
          <p className="login-demo-title">Tài khoản demo</p>
          <div className="login-demo-accounts">
            <code>admin@university.edu.vn</code>
            <code>staff@university.edu.vn</code>
            <code>leader@university.edu.vn</code>
            <code>faculty1@university.edu.vn</code>
            <code>reviewer1@university.edu.vn</code>
          </div>
          <p className="login-demo-pw">Mật khẩu: <code>password123</code></p>
        </div>
      </div>
    </div>
  );
}
