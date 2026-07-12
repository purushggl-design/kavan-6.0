import { apiClient as api } from '@/api/apiClient';

export interface Tenant {
  id: string;
  tenant_code: string;
  tenant_name: string;
  company_name: string;
  company_domain: string;
  company_email: string;
  company_phone: string;
  company_logo: string;
  timezone: string;
  language: string;
  currency: string;
  tenant_status: 'PENDING' | 'APPROVED' | 'ACTIVE' | 'WARNING' | 'READ_ONLY' | 'SUSPENDED' | 'ARCHIVED' | 'DELETED';
  owner: string;
  member_count?: number;
  created_at: string;
  updated_at: string;
}

export interface CreateTenantPayload {
  tenant_code: string;
  tenant_name: string;
  company_name: string;
  company_domain: string;
  company_email?: string;
  company_phone?: string;
  timezone?: string;
  language?: string;
  currency?: string;
}

export interface CreateAdminPayload {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
}

const tenantService = {
  /** List all tenants, optionally filtered by status */
  list: async (statusFilter?: string): Promise<{ data: Tenant[]; count: number }> => {
    const params = statusFilter ? { status: statusFilter } : {};
    const res = await api.get('/platform/tenants/', { params });
    return res.data;
  },

  /** Get a single tenant by ID */
  get: async (id: string): Promise<{ data: Tenant }> => {
    const res = await api.get(`/platform/tenants/${id}/`);
    return res.data;
  },

  /** Create a new tenant (starts in PENDING state) */
  create: async (payload: CreateTenantPayload): Promise<{ data: Tenant }> => {
    const res = await api.post('/platform/tenants/', payload);
    return res.data;
  },

  /** Edit tenant details */
  update: async (id: string, payload: Partial<CreateTenantPayload>): Promise<{ data: Tenant }> => {
    const res = await api.patch(`/platform/tenants/${id}/`, payload);
    return res.data;
  },

  /** Approve a PENDING tenant → activates it */
  approve: async (id: string): Promise<{ data: Tenant; message: string }> => {
    const res = await api.post(`/platform/tenants/${id}/approve/`);
    return res.data;
  },

  /** Suspend an ACTIVE tenant */
  suspend: async (id: string, reason?: string): Promise<{ data: Tenant; message: string }> => {
    const res = await api.post(`/platform/tenants/${id}/suspend/`, { reason: reason || '' });
    return res.data;
  },

  /** Delete a tenant */
  delete: async (id: string): Promise<void> => {
    await api.delete(`/platform/tenants/${id}/`);
  },

  /** Create a Tenant Admin user for an ACTIVE tenant */
  createAdmin: async (tenantId: string, payload: CreateAdminPayload): Promise<{ data: object; message: string }> => {
    const res = await api.post(`/platform/tenants/${tenantId}/create-admin/`, payload);
    return res.data;
  },
};

export default tenantService;
