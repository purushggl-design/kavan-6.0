import { apiClient as api } from '@/api/apiClient';

export interface Deployment {
  id: string;
  name: string;
  environment: 'PRODUCTION' | 'STAGING' | 'DEVELOPMENT';
  status: 'SUCCESS' | 'FAILED' | 'PENDING' | 'IN_PROGRESS';
  deployed_at: string;
  version: string;
  url?: string;
  logs?: string[];
}

export const deploymentService = {
  getDeployments: async (): Promise<Deployment[]> => {
    try {
      const response = await api.get('/deployments/');
      return response.data;
    } catch {
      // Fallback for UI
      return [
        { id: '1', name: 'Frontend v6', environment: 'PRODUCTION', status: 'SUCCESS', deployed_at: new Date().toISOString(), version: 'v6.0.0', url: 'https://kavan.com' },
        { id: '2', name: 'API Services', environment: 'PRODUCTION', status: 'SUCCESS', deployed_at: new Date(Date.now() - 86400000).toISOString(), version: 'v6.0.0', url: 'https://api.kavan.com' },
        { id: '3', name: 'Worker Nodes', environment: 'STAGING', status: 'IN_PROGRESS', deployed_at: new Date().toISOString(), version: 'v6.1.0-rc1' }
      ];
    }
  }
};

export default deploymentService;
