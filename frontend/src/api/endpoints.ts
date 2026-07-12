export const ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login/',
    LOGOUT: '/auth/logout/',
    REFRESH: '/auth/refresh/',
  },
  TENANTS: {
    LIST: '/platform/tenants/',
    DETAIL: (id: string) => `/platform/tenants/${id}/`,
  },
  USERS: {
    LIST: '/accounts/users/',
    ME: '/accounts/users/me/',
  },
  RBAC: {
    MY_PERMISSIONS: '/rbac/my-permissions/',
    PLATFORM_PERMISSIONS: '/rbac/platform-permissions/',
  },
  MARKETPLACE: {
    PRODUCTS: '/marketplace/products/',
    INSTALLATIONS: '/installations/',
  },
  MONITORING: {
    HEALTH: '/monitoring/health/',
    METRICS: '/monitoring/metrics/',
  },
  SIEM: {
    INCIDENTS: '/siem/incidents/',
    STATS: '/siem/stats/',
  },
  DEPLOYMENTS: {
    LIST: '/deployments/',
  },
  AUDIT: {
    EVENTS: '/audit/events/',
  }
} as const;
