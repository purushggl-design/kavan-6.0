import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { selectCurrentUser, logout } from '@/store/authSlice';
import { apiClient } from '@/api/apiClient';
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
  const user = useSelector(selectCurrentUser);
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
    try {
      await apiClient.post('/auth/logout/');
    } catch (e) {
      // Ignore
    }
    dispatch(logout());
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
      {/* Sidebar removed to fix nested layout issue with AppLayout */}

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
