/**
 * Authentication context — manages JWT token, current user, and login/logout.
 */

import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../api/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Load user on mount if token exists
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authApi
        .getProfile()
        .then((profile) => setUser(profile))
        .catch(() => {
          localStorage.removeItem('access_token');
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(
    async (email, password) => {
      const data = await authApi.login(email, password);
      localStorage.setItem('access_token', data.access_token);
      const profile = await authApi.getProfile();
      setUser(profile);
      navigate('/');
      return profile;
    },
    [navigate]
  );

  const logout = useCallback(() => {
    localStorage.removeItem('access_token');
    setUser(null);
    navigate('/login');
  }, [navigate]);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
