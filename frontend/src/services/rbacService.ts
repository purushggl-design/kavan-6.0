import { api } from './api';

export interface EffectivePermissions {
  user_id: string;
  platform_role: string | null;
  platform_permissions: string[];
  tenant_id: string | null;
  tenant_permissions: string[];
}

const rbacService = {
  /** Call right after login (and on app hydration) to populate authSlice.permissions */
  getMyPermissions: async (): Promise<EffectivePermissions> => {
    const res = await api.get('/rbac/my-permissions/');
    return res.data.data;
  },

  /** Get all platform permissions */
  getPlatformPermissions: async (): Promise<any> => {
    const res = await api.get('/rbac/platform-permissions/');
    return res.data;
  },
};

export default rbacService;
