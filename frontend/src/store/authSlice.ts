import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import type { AuthState, User, Tenant, PlatformRole } from '../types/auth';

const STORAGE_KEY = 'kavan_auth';

function loadPersistedState(): AuthState {
  const empty: AuthState = {
    user: null,
    tenant: null,
    permissions: [],
    role: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    isLoading: true, // true until the app finishes hydrating on mount
  };

  if (typeof window === 'undefined') return empty;

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return empty;
    const parsed = JSON.parse(raw);
    return { ...empty, ...parsed, isLoading: true };
  } catch {
    return empty;
  }
}

const initialState: AuthState = loadPersistedState();

function persist(state: AuthState) {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      user: state.user,
      tenant: state.tenant,
      permissions: state.permissions,
      role: state.role,
      accessToken: state.accessToken,
      refreshToken: state.refreshToken,
      isAuthenticated: state.isAuthenticated,
    })
  );
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Called once on app mount after reading tokens from localStorage,
    // to end the loading/hydration phase without re-authenticating.
    hydrationComplete: (state) => {
      state.isLoading = false;
    },

    // Called after a real login response from POST /api/v1/auth/login/
    setCredentials: (
      state,
      action: PayloadAction<{
        user: User;
        tenant?: Tenant | null;
        permissions?: string[];
        accessToken: string;
        refreshToken?: string;
      }>
    ) => {
      state.user = action.payload.user;
      state.tenant = action.payload.tenant ?? null;
      state.permissions = action.payload.permissions ?? [];
      state.role = action.payload.user.platform_role;
      state.accessToken = action.payload.accessToken;
      state.refreshToken = action.payload.refreshToken ?? null;
      state.isAuthenticated = true;
      state.isLoading = false;
      persist(state);
    },

    // Called when the axios interceptor refreshes the access token
    setAccessToken: (state, action: PayloadAction<string>) => {
      state.accessToken = action.payload;
      persist(state);
    },

    // Called when the backend returns a fuller permission list
    // (e.g. from a dedicated /rbac/my-permissions/ endpoint once it exists)
    setPermissions: (state, action: PayloadAction<string[]>) => {
      state.permissions = action.payload;
      persist(state);
    },

    logout: (state) => {
      state.user = null;
      state.tenant = null;
      state.permissions = [];
      state.role = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    },
  },
});

export const {
  hydrationComplete,
  setCredentials,
  setAccessToken,
  setPermissions,
  logout,
} = authSlice.actions;

export const selectCurrentUser = (state: { auth: AuthState }) => state.auth.user;
export const selectCurrentTenant = (state: { auth: AuthState }) => state.auth.tenant;
export const selectCurrentRole = (state: { auth: AuthState }): PlatformRole => state.auth.role;
export const selectPermissions = (state: { auth: AuthState }) => state.auth.permissions;
export const selectIsAuthenticated = (state: { auth: AuthState }) => state.auth.isAuthenticated;
export const selectAuthLoading = (state: { auth: AuthState }) => state.auth.isLoading;

// Role-first gating: SUPER_ADMIN always passes. Everyone else needs the
// explicit permission code in their list, fetched from
// GET /api/v1/rbac/my-permissions/ after login (see services/rbacService.ts).
export const selectCanAccess = (permission: string) => (state: { auth: AuthState }) => {
  if (state.auth.role === 'SUPER_ADMIN') return true;
  return state.auth.permissions.includes(permission);
};

export default authSlice.reducer;
