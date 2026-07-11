import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './modules/authentication/LoginPage';
import { PlatformDashboard } from './modules/dashboard/PlatformDashboard';
import { TenantListPage } from './modules/platform/tenants/TenantListPage';
import { MarketplacePage } from './modules/platform/marketplace/MarketplacePage';
import { store } from './store';

function App() {
  return (
    <Provider store={store}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />

            {/* Platform Admin protected routes */}
            <Route
              path="/platform/dashboard"
              element={
                <ProtectedRoute>
                  <PlatformDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/platform/tenants"
              element={
                <ProtectedRoute>
                  <TenantListPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/platform/marketplace"
              element={
                <ProtectedRoute>
                  <MarketplacePage />
                </ProtectedRoute>
              }
            />

            {/* Legacy dashboard redirect */}
            <Route path="/dashboard" element={<Navigate to="/platform/dashboard" replace />} />

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
        </BrowserRouter>
      </AuthProvider>
    </Provider>
  );
}

export default App;
