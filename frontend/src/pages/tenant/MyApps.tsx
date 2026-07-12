import React, { useEffect, useState } from 'react';
import { apiClient } from '@/api/apiClient';
import { ENDPOINTS } from '@/api/endpoints';
import { HealthBadge } from '@/components/enterprise/HealthBadge';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { formatDistanceToNow } from 'date-fns';
interface Installation {
  id: string;
  application_name: string;
  version_number: string;
  status: 'RUNNING' | 'FAILED' | 'PENDING' | 'STOPPED';
  route_path: string;
  installed_at: string;
  last_health_check: string | null;
}

const mapStatusToHealth = (status: string) => {
  switch (status) {
    case 'RUNNING': return 'healthy';
    case 'FAILED': return 'critical';
    case 'PENDING': return 'degraded';
    default: return 'unknown';
  }
};

export function MyApps() {
  const [installations, setInstallations] = useState<Installation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const response = await apiClient.get(ENDPOINTS.MARKETPLACE.INSTALLATIONS);
        setInstallations(response.data.data || []);
      } catch (error) {
        console.error("Failed to fetch installations", error);
      } finally {
        setLoading(false);
      }
    };
    fetchApps();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Apps</h1>
          <p className="text-muted-foreground mt-2">Manage your organization's installed applications and their health.</p>
        </div>
      </div>

      {loading ? (
        <div className="flex h-40 items-center justify-center">
          <div className="w-8 h-8 rounded-full border-4 border-primary border-t-transparent animate-spin" />
        </div>
      ) : installations.length === 0 ? (
        <Card className="border-dashed bg-muted/20">
          <CardContent className="flex flex-col items-center justify-center py-16 text-center">
            <h3 className="mt-4 text-lg font-semibold">No applications installed</h3>
            <p className="mt-2 text-sm text-muted-foreground max-w-sm">
              Head over to the Marketplace to discover and install applications for your tenant.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {installations.map(app => (
            <Card key={app.id} className="overflow-hidden transition-all hover:shadow-md border border-border/50 bg-card">
              <CardHeader className="pb-3 border-b border-border/30 bg-muted/10">
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{app.application_name}</CardTitle>
                    <CardDescription className="font-mono text-xs mt-1 bg-muted px-2 py-0.5 rounded w-fit">
                      v{app.version_number}
                    </CardDescription>
                  </div>
                  <HealthBadge 
                    status={mapStatusToHealth(app.status)} 
                    label={app.status.toLowerCase()} 
                  />
                </div>
              </CardHeader>
              <CardContent className="pt-4 space-y-4">
                <div className="text-sm">
                  <p className="text-muted-foreground mb-1">Route Path</p>
                  <a href={app.route_path} target="_blank" rel="noreferrer" className="text-primary hover:underline font-mono text-xs break-all">
                    {app.route_path || 'Provisioning...'}
                  </a>
                </div>
                
                <div className="flex items-center justify-between text-xs text-muted-foreground pt-2 border-t border-border/30">
                  <div>
                    <span className="font-medium">Installed:</span> {formatDistanceToNow(new Date(app.installed_at))} ago
                  </div>
                  {app.last_health_check && (
                    <div className="flex items-center gap-1.5" title={new Date(app.last_health_check).toLocaleString()}>
                      <div className={`w-1.5 h-1.5 rounded-full ${app.status === 'RUNNING' ? 'bg-success animate-pulse' : 'bg-muted-foreground'}`} />
                      Checked {formatDistanceToNow(new Date(app.last_health_check))} ago
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
