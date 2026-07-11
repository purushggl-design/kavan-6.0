import { api } from './api';

export interface DashboardMetrics {
  total_tenants: number;
  active_tenants: number;
  pending_tenants: number;
  total_deployments: number;
  new_alerts: number;
  open_incidents: number;
  system_health: 'healthy' | 'degraded' | 'down';
}

const dashboardService = {
  /**
   * Aggregate dashboard metrics from multiple API calls.
   * Returns a combined summary for the platform dashboard.
   */
  getPlatformMetrics: async (): Promise<DashboardMetrics> => {
    const [tenantsRes, siemRes] = await Promise.allSettled([
      api.get('/platform/tenants/'),
      api.get('/siem/stats/'),
    ]);

    // Safe extraction from settled promises
    const tenantsData = tenantsRes.status === 'fulfilled' ? tenantsRes.value.data : null;
    const siemData = siemRes.status === 'fulfilled' ? siemRes.value.data?.data : null;

    // Count tenants by status from the list response
    const tenants: Array<{ tenant_status: string }> = tenantsData?.data ?? [];
    const total_tenants = tenantsData?.count ?? tenants.length;
    const active_tenants = tenants.filter((t) => t.tenant_status === 'ACTIVE').length;
    const pending_tenants = tenants.filter((t) => t.tenant_status === 'PENDING').length;

    return {
      total_tenants,
      active_tenants,
      pending_tenants,
      total_deployments: 0, // Layer 6 will populate this
      new_alerts: siemData?.alerts?.new ?? 0,
      open_incidents: siemData?.incidents?.open ?? 0,
      system_health: 'healthy',
    };
  },

  /** Fetch health status from the monitoring endpoint */
  getHealth: async (): Promise<{ status: string }> => {
    try {
      const res = await api.get('/monitoring/health/');
      return res.data?.data ?? { status: 'healthy' };
    } catch {
      return { status: 'unknown' };
    }
  },
};

export default dashboardService;
