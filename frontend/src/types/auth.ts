// Platform-level roles. Matches apps.authentication.models.User.platform_role
// on the backend exactly — do not rename without updating the backend choices.
export type PlatformRole =
  | 'SUPER_ADMIN'
  | 'TENANT_ADMIN'
  | 'SECURITY_ANALYST'
  | 'DEVELOPER'
  | 'EMPLOYEE'
  | 'MANAGER'
  | null;

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  platform_role: PlatformRole;
  tenant_id: string | null;
}

export interface Tenant {
  id: string;
  tenant_name: string;
  company_name: string;
  tenant_status: string;
}

export interface AuthState {
  user: User | null;
  tenant: Tenant | null;
  permissions: string[];
  role: PlatformRole;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
