import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useAuth } from '../../context/AuthContext';
import { setCredentials } from '../../store/authSlice';
import './LoginPage.css';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const { login } = useAuth();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login({ email, password });
      
      // Sync user into Redux store for PermissionGuard
      const storedUser = localStorage.getItem('user');
      const token = localStorage.getItem('access_token');
      if (storedUser && token) {
        const userData = JSON.parse(storedUser);
        dispatch(setCredentials({
          user: userData,
          accessToken: token,
          permissions: [],
        }));
      }

      navigate(from, { replace: true });
    } catch (err: any) {
      const message =
        err?.response?.data?.message ||
        err?.response?.data?.detail ||
        err?.response?.data?.non_field_errors?.[0] ||
        'Login failed. Please check your credentials.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Animated background */}
      <div className="login-bg">
        <div className="login-bg-orb login-bg-orb--1" />
        <div className="login-bg-orb login-bg-orb--2" />
        <div className="login-bg-orb login-bg-orb--3" />
        <div className="login-grid-overlay" />
      </div>

      <div className="login-container">
        {/* Left panel – branding */}
        <div className="login-brand-panel">
          <div className="login-brand-content">
            <div className="login-logo">
              <div className="login-logo-icon">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 20L20 8L32 20L20 32L8 20Z" fill="url(#logoGrad)" />
                  <path d="M14 20L20 14L26 20L20 26L14 20Z" fill="rgba(255,255,255,0.3)" />
                  <defs>
                    <linearGradient id="logoGrad" x1="8" y1="8" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                      <stop stopColor="#7C3AED" />
                      <stop offset="1" stopColor="#06B6D4" />
                    </linearGradient>
                  </defs>
                </svg>
              </div>
              <span className="login-logo-text">KAVAN</span>
            </div>
            <h1 className="login-brand-title">
              Enterprise Security<br />
              <span className="login-brand-highlight">Orchestration Platform</span>
            </h1>
            <p className="login-brand-subtitle">
              Unified platform for multi-tenant security operations,
              deployment management, and real-time threat intelligence.
            </p>
            <div className="login-stats">
              <div className="login-stat">
                <span className="login-stat-value">7</span>
                <span className="login-stat-label">Security Layers</span>
              </div>
              <div className="login-stat-divider" />
              <div className="login-stat">
                <span className="login-stat-value">∞</span>
                <span className="login-stat-label">Tenants</span>
              </div>
              <div className="login-stat-divider" />
              <div className="login-stat">
                <span className="login-stat-value">24/7</span>
                <span className="login-stat-label">SIEM</span>
              </div>
            </div>
            <div className="login-features">
              {['JWT Authentication', 'RBAC Permissions', 'Multi-Tenant Isolation', 'Real-time Monitoring'].map((f) => (
                <div key={f} className="login-feature-badge">
                  <svg viewBox="0 0 16 16" fill="none" width="14" height="14">
                    <circle cx="8" cy="8" r="8" fill="rgba(124,58,237,0.2)" />
                    <path d="M5 8l2 2 4-4" stroke="#7C3AED" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  {f}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right panel – form */}
        <div className="login-form-panel">
          <div className="login-card">
            <div className="login-card-header">
              <h2 className="login-card-title">Sign In</h2>
              <p className="login-card-subtitle">Access the KAVAN Platform</p>
            </div>

            {error && (
              <div className="login-error" role="alert">
                <svg viewBox="0 0 20 20" fill="none" width="18" height="18">
                  <circle cx="10" cy="10" r="9" stroke="#f87171" strokeWidth="1.5"/>
                  <path d="M10 6v4M10 14h.01" stroke="#f87171" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
                {error}
              </div>
            )}

            <form className="login-form" onSubmit={handleSubmit} noValidate>
              <div className="login-field">
                <label htmlFor="login-email" className="login-label">Email Address</label>
                <div className="login-input-wrapper">
                  <svg className="login-input-icon" viewBox="0 0 20 20" fill="none" width="18" height="18">
                    <path d="M3 5h14l-7 7-7-7z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
                    <rect x="3" y="5" width="14" height="11" rx="1" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                  <input
                    id="login-email"
                    type="email"
                    className="login-input"
                    placeholder="admin@kavan.local"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    autoFocus
                    autoComplete="email"
                  />
                </div>
              </div>

              <div className="login-field">
                <label htmlFor="login-password" className="login-label">Password</label>
                <div className="login-input-wrapper">
                  <svg className="login-input-icon" viewBox="0 0 20 20" fill="none" width="18" height="18">
                    <rect x="4" y="9" width="12" height="9" rx="2" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M7 9V6a3 3 0 016 0v3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <input
                    id="login-password"
                    type={showPassword ? 'text' : 'password'}
                    className="login-input login-input--password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    className="login-toggle-password"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? (
                      <svg viewBox="0 0 20 20" fill="none" width="18" height="18">
                        <path d="M3 3l14 14M8.7 8.7a3 3 0 004.2 4.2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        <path d="M10 5c4 0 7 3.5 7 5 0 .7-.3 1.4-.7 2.1M4.7 7.9C3.7 8.8 3 9.8 3 10c0 1.5 3 5 7 5a7 7 0 002.1-.3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      </svg>
                    ) : (
                      <svg viewBox="0 0 20 20" fill="none" width="18" height="18">
                        <path d="M10 4C5.5 4 2 8 2 10s3.5 6 8 6 8-4 8-6-3.5-6-8-6z" stroke="currentColor" strokeWidth="1.5"/>
                        <circle cx="10" cy="10" r="2.5" stroke="currentColor" strokeWidth="1.5"/>
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              <button
                id="login-submit-btn"
                type="submit"
                className="login-btn"
                disabled={isLoading || !email || !password}
              >
                {isLoading ? (
                  <>
                    <div className="login-btn-spinner" />
                    Authenticating...
                  </>
                ) : (
                  <>
                    Sign In
                    <svg viewBox="0 0 20 20" fill="none" width="18" height="18">
                      <path d="M5 10h10M11 6l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </>
                )}
              </button>
            </form>

            <div className="login-hint">
              <span>Default admin:</span>
              <code>admin@kavan.local / Admin123!</code>
            </div>

            <p className="login-footer">
              KAVAN v6.0 — Enterprise Security Platform
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
