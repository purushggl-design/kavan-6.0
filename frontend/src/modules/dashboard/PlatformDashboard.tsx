import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useDispatch } from 'react-redux';
import { logout as reduxLogout } from '../../store/authSlice';
import dashboardService, { DashboardMetrics } from '../../services/dashboardService';
import './PlatformDashboard.css';

const NAV_ITEMS = [
  { label: 'Dashboard',   icon: '⊡', path: '/platform/dashboard' },
  { label: 'Tenants',     icon: '🏢', path: '/platform/tenants' },
  { label: 'Marketplace', icon: '🛒', path: '/platform/marketplace' },
  { label: 'Deployments', icon: '🚀', path: '/platform/deployments', disabled: true },
  { label: 'Monitoring',  icon: '📊', path: '/platform/monitoring', disabled: true },
  { label: 'SIEM',        icon: '🛡️', path: '/platform/siem', disabled: true },
  { label: 'Settings',    icon: '⚙️', path: '/platform/settings', disabled: true },
];

export const PlatformDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [metricsLoading, setMetricsLoading] = useState(true);

  useEffect(() => {
    dashboardService.getPlatformMetrics()
      .then(setMetrics)
      .catch(() => setMetrics(null))
      .finally(() => setMetricsLoading(false));
  }, []);

  const handleLogout = async () => {
    dispatch(reduxLogout());
    await logout();
    navigate('/login', { replace: true });
  };

  const metricCards = [
    {
      label: 'Total Tenants',
      value: metricsLoading ? '…' : String(metrics?.total_tenants ?? '—'),
      sub: metricsLoading ? '' : `${metrics?.active_tenants ?? 0} active · ${metrics?.pending_tenants ?? 0} pending`,
      icon: '🏢',
      color: '#7c3aed',
      onClick: () => navigate('/platform/tenants'),
    },
    {
      label: 'Deployments',
      value: metricsLoading ? '…' : String(metrics?.total_deployments ?? '—'),
      sub: 'Sprint 2',
      icon: '🚀',
      color: '#0891b2',
      onClick: undefined,
    },
    {
      label: 'Open Alerts',
      value: metricsLoading ? '…' : String(metrics?.new_alerts ?? '—'),
      sub: `${metrics?.open_incidents ?? 0} open incidents`,
      icon: '🔔',
      color: metrics?.new_alerts ? '#dc2626' : '#22c55e',
      onClick: undefined,
    },
    {
      label: 'System Health',
      value: metricsLoading ? '…' : (metrics?.system_health === 'healthy' ? 'Online' : 'Degraded'),
      sub: 'All services',
      icon: metrics?.system_health === 'healthy' ? '💚' : '🔴',
      color: '#16a34a',
      onClick: undefined,
    },
  ];

  return (
    <div className="platform-dashboard">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">
            <svg viewBox="0 0 40 40" fill="none">
              <path d="M8 20L20 8L32 20L20 32L8 20Z" fill="url(#sidebarGrad)" />
              <path d="M14 20L20 14L26 20L20 26L14 20Z" fill="rgba(255,255,255,0.2)" />
              <defs>
                <linearGradient id="sidebarGrad" x1="8" y1="8" x2="32" y2="32">
                  <stop stopColor="#7C3AED" />
                  <stop offset="1" stopColor="#06B6D4" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span className="sidebar-logo-text">KAVAN</span>
        </div>

        <nav className="sidebar-nav">
          {NAV_ITEMS.map((item) => {
            const isActive = location.pathname === item.path ||
              (item.path !== '/platform/dashboard' && location.pathname.startsWith(item.path));
            return (
              <div
                key={item.label}
                className={`sidebar-nav-item ${isActive ? 'sidebar-nav-item--active' : ''} ${item.disabled ? 'sidebar-nav-item--disabled' : ''}`}
                onClick={() => !item.disabled && navigate(item.path)}
                title={item.disabled ? 'Coming in Sprint 2' : undefined}
              >
                <span className="sidebar-nav-icon">{item.icon}</span>
                <span className="sidebar-nav-label">{item.label}</span>
                {isActive && <div className="sidebar-nav-indicator" />}
                {item.disabled && <span className="sidebar-nav-soon">soon</span>}
              </div>
            );
          })}
        </nav>

        <div className="sidebar-user">
          <div className="sidebar-user-avatar">
            {user?.first_name?.[0]}{user?.last_name?.[0]}
          </div>
          <div className="sidebar-user-info">
            <div className="sidebar-user-name">{user?.first_name} {user?.last_name}</div>
            <div className="sidebar-user-role">{user?.platform_role?.replace('_', ' ')}</div>
          </div>
          <button className="sidebar-logout-btn" onClick={handleLogout} title="Sign out">
            <svg viewBox="0 0 20 20" fill="none" width="18" height="18">
              <path d="M13 7l3 3-3 3M7 10h9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 3H5a2 2 0 00-2 2v10a2 2 0 002 2h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="dashboard-main">
        <header className="dashboard-header">
          <div>
            <h1 className="dashboard-title">Platform Dashboard</h1>
            <p className="dashboard-subtitle">Welcome back, {user?.first_name || 'Admin'}</p>
          </div>
          <div className="dashboard-header-badges">
            <span className="status-badge status-badge--online">● System Online</span>
          </div>
        </header>

        {/* Metrics */}
        <div className="dashboard-metrics">
          {metricCards.map((m) => (
            <div
              key={m.label}
              className={`metric-card ${m.onClick ? 'metric-card--clickable' : ''}`}
              onClick={m.onClick}
            >
              <div className="metric-icon" style={{ background: `${m.color}20`, color: m.color }}>
                {m.icon}
              </div>
              <div className="metric-info">
                <div className="metric-value">{m.value}</div>
                <div className="metric-label">{m.label}</div>
                {m.sub && <div className="metric-sub">{m.sub}</div>}
              </div>
              {m.onClick && <div className="metric-arrow">→</div>}
            </div>
          ))}
        </div>

        {/* Quick actions */}
        <div className="dashboard-section">
          <h2 className="section-title">Quick Actions</h2>
          <div className="quick-actions-grid">
            <div className="quick-action-card" onClick={() => navigate('/platform/tenants')}>
              <span className="quick-action-icon">🏢</span>
              <div>
                <div className="quick-action-title">Manage Tenants</div>
                <div className="quick-action-desc">Create, approve, and configure tenant organizations</div>
              </div>
              <span className="quick-action-arrow">→</span>
            </div>
            <div className="quick-action-card" onClick={() => navigate('/platform/marketplace')}>
              <span className="quick-action-icon">🛒</span>
              <div>
                <div className="quick-action-title">Marketplace</div>
                <div className="quick-action-desc">Browse and publish products for tenants</div>
              </div>
              <span className="quick-action-arrow">→</span>
            </div>
            <div className="quick-action-card quick-action-card--disabled">
              <span className="quick-action-icon">🚀</span>
              <div>
                <div className="quick-action-title">Deployments</div>
                <div className="quick-action-desc">Coming in Sprint 2</div>
              </div>
              <span className="quick-action-badge">Soon</span>
            </div>
            <div className="quick-action-card quick-action-card--disabled">
              <span className="quick-action-icon">🛡️</span>
              <div>
                <div className="quick-action-title">SIEM</div>
                <div className="quick-action-desc">Coming in Sprint 2</div>
              </div>
              <span className="quick-action-badge">Soon</span>
            </div>
          </div>
        </div>

        {/* API docs shortcut */}
        <div className="dashboard-section">
          <h2 className="section-title">Developer Links</h2>
          <div className="quick-links-grid">
            <a href="http://127.0.0.1:8000/api/docs/" target="_blank" rel="noreferrer" className="quick-link-card">
              <span className="quick-link-icon">📖</span>
              <span className="quick-link-label">API Documentation</span>
              <span className="quick-link-arrow">→</span>
            </a>
            <a href="http://127.0.0.1:8000/api/redoc/" target="_blank" rel="noreferrer" className="quick-link-card">
              <span className="quick-link-icon">📋</span>
              <span className="quick-link-label">ReDoc Reference</span>
              <span className="quick-link-arrow">→</span>
            </a>
          </div>
        </div>
      </main>
    </div>
  );
};
