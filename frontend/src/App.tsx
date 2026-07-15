import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { Provider } from 'react-redux';
import { Toaster } from 'sonner';

import { ProtectedRoute } from './components/ProtectedRoute';
import { store } from './store';

// Layout
import { AppLayout } from './layouts/AppLayout';

// Auth Pages
import { LoginPage } from './modules/authentication/LoginPage';

// Main Dashboard (Sprint 1)
import { PlatformDashboard } from './modules/dashboard/PlatformDashboard';
import { MarketplacePage } from './modules/platform/marketplace/MarketplacePage';
import { TenantListPage } from './modules/platform/tenants/TenantListPage';

// Super Admin Pages
import { 
  RolesPermissionsPage, 
  AnalyticsPage, 
  SystemMonitoringPage, 
  AuditLogsPage, 
  SubscriptionsPage, 
  LicensesPage, 
  GlobalSettingsPage, 
  FeatureTogglesPage, 
  MaintenancePage, 
  DatabaseMonitorPage 
} from './pages/super-admin/SuperAdminPages';

// Developer Pages
import { 
  ApiKeysPage, 
  WebhooksPage, 
  DeploymentsPage, 
  MonitoringPage 
} from './pages/developer/DeveloperPages';

// Security Admin Pages
import { 
  SecurityAuditLogsPage, 
  ThreatsPage, 
  MfaPage as SecurityMfaPage, 
  SessionsPage, 
  IpManagementPage, 
  PermissionsPage, 
  CompliancePage 
} from './pages/security-admin/SecurityAdminPages';

// Shared Pages
import { UserManagement } from './pages/users/UserManagement';
import { OrganizationManagement } from './pages/organizations/OrganizationManagement';
import { MyApps } from './pages/tenant/MyApps';
import { ProfileSettings } from './pages/profile/ProfileSettings';
import { Notifications } from './pages/notifications/Notifications';
import { PermissionMatrix } from './pages/permissions/PermissionMatrix';

// Dashboards
import { SecurityDashboard } from './pages/dashboards/SecurityDashboard';
import { DeveloperDashboard } from './pages/dashboards/DeveloperDashboard';

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />

            {/* Protected Routes inside AppLayout */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              {/* Default to Dashboard */}
              <Route index element={<Navigate to="/platform/dashboard" replace />} />
              <Route path="dashboard" element={<Navigate to="/platform/dashboard" replace />} />
              
              {/* Core Dashboards */}
              <Route path="platform/dashboard" element={<PlatformDashboard />} />
              <Route path="security/dashboard" element={<SecurityDashboard />} />
              <Route path="developer/dashboard" element={<DeveloperDashboard />} />
              
              {/* Shared Settings */}
              <Route path="platform/marketplace" element={<MarketplacePage />} />
              <Route path="users" element={<UserManagement />} />
              <Route path="organizations" element={<OrganizationManagement />} />
              <Route path="my-apps" element={<MyApps />} />
              <Route path="profile" element={<ProfileSettings />} />
              <Route path="notifications" element={<Notifications />} />
              <Route path="permissions" element={<PermissionMatrix />} />

              {/* Super Admin Routes */}
              <Route path="super-admin/tenants" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><TenantListPage /></ProtectedRoute>} />
              <Route path="super-admin/roles" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><RolesPermissionsPage /></ProtectedRoute>} />
              <Route path="super-admin/analytics" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><AnalyticsPage /></ProtectedRoute>} />
              <Route path="super-admin/system-monitoring" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><SystemMonitoringPage /></ProtectedRoute>} />
              <Route path="super-admin/audit-logs" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><AuditLogsPage /></ProtectedRoute>} />
              <Route path="super-admin/subscriptions" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><SubscriptionsPage /></ProtectedRoute>} />
              <Route path="super-admin/licenses" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><LicensesPage /></ProtectedRoute>} />
              <Route path="super-admin/settings" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><GlobalSettingsPage /></ProtectedRoute>} />
              <Route path="super-admin/feature-toggles" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><FeatureTogglesPage /></ProtectedRoute>} />
              <Route path="super-admin/maintenance" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><MaintenancePage /></ProtectedRoute>} />
              <Route path="super-admin/database-monitor" element={<ProtectedRoute requiredRole="SUPER_ADMIN"><DatabaseMonitorPage /></ProtectedRoute>} />

              {/* Security Admin Routes */}
              <Route path="security/audit-logs" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><SecurityAuditLogsPage /></ProtectedRoute>} />
              <Route path="security/threats" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><ThreatsPage /></ProtectedRoute>} />
              <Route path="security/mfa" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><SecurityMfaPage /></ProtectedRoute>} />
              <Route path="security/sessions" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><SessionsPage /></ProtectedRoute>} />
              <Route path="security/ip-management" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><IpManagementPage /></ProtectedRoute>} />
              <Route path="security/permissions" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><PermissionsPage /></ProtectedRoute>} />
              <Route path="security/compliance" element={<ProtectedRoute requiredRole="SECURITY_ANALYST"><CompliancePage /></ProtectedRoute>} />

              {/* Developer Routes */}
              <Route path="developer/api-keys" element={<ProtectedRoute requiredRole="DEVELOPER"><ApiKeysPage /></ProtectedRoute>} />
              <Route path="developer/webhooks" element={<ProtectedRoute requiredRole="DEVELOPER"><WebhooksPage /></ProtectedRoute>} />
              <Route path="developer/deployments" element={<ProtectedRoute requiredRole="DEVELOPER"><DeploymentsPage /></ProtectedRoute>} />
              <Route path="developer/monitoring" element={<ProtectedRoute requiredRole="DEVELOPER"><MonitoringPage /></ProtectedRoute>} />

            </Route>

            {/* 403 Forbidden */}
            <Route
              path="/403"
              element={
                <div style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  minHeight: '100vh', background: '#080b14', color: '#f1f5f9',
                  flexDirection: 'column', gap: 12, fontFamily: 'Inter, sans-serif'
                }}>
                  <h1 style={{ fontSize: 64, margin: 0, color: '#ef4444' }}>403</h1>
                  <p style={{ color: '#64748b' }}>You don't have permission to access this page.</p>
                </div>
              }
            />

            {/* Default redirect */}
            <Route path="*" element={<Navigate to="/platform/dashboard" replace />} />
          </Routes>
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </Provider>
  );
}

export default App;
