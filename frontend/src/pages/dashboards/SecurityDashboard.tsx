import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldAlert, Activity, Lock, Search } from 'lucide-react';
import { SectionHeader } from '@/components/enterprise/SectionHeader';
import { StatCard } from '@/components/enterprise/StatCard';
import { HealthBadge } from '@/components/enterprise/HealthBadge';

interface SecurityEvent {
  id: string;
  title: string;
  description: string;
  severity: string;
  time_ago: string;
}

interface SecurityDashboardData {
  active_threats: number;
  failed_logins_24h: number;
  anomaly_score: string;
  open_investigations: number;
  recent_events: SecurityEvent[];
}

export const SecurityDashboard: React.FC = () => {
  const [data, setData] = useState<SecurityDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const res = await fetch('http://127.0.0.1:8000/api/v1/monitoring/dashboards/soc/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch security dashboard');
        const json = await res.json();
        setData(json.data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) return <div className="text-white">Loading security dashboard...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;
  if (!data) return null;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <SectionHeader 
        title="Security Operations Center" 
        description="Real-time threat detection and access monitoring." 
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="Active Threats" 
          value={data.active_threats.toString()} 
          icon={<ShieldAlert className="w-4 h-4" />} 
          trend={{ value: "Secure", isPositive: true }}
        />
        <StatCard 
          title="Failed Logins (24h)" 
          value={data.failed_logins_24h.toLocaleString()} 
          icon={<Lock className="w-4 h-4" />} 
          trend={{ value: "+12%", isPositive: false }}
        />
        <StatCard 
          title="Anomaly Score" 
          value={data.anomaly_score} 
          icon={<Activity className="w-4 h-4" />} 
        />
        <StatCard 
          title="Open Investigations" 
          value={data.open_investigations.toString()} 
          icon={<Search className="w-4 h-4" />} 
        />
      </div>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Recent Security Events</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {data.recent_events.map((event) => (
              <div key={event.id} className={`flex items-center justify-between p-4 rounded-lg border ${event.severity === 'warning' ? 'bg-orange-500/10 border-orange-500/20' : 'bg-background/50 border-border'}`}>
                <div className="flex items-center gap-4">
                  {event.severity === 'warning' ? <ShieldAlert className="w-6 h-6 text-orange-500" /> : <Lock className="w-6 h-6 text-muted-foreground" />}
                  <div>
                    <h4 className={`font-semibold ${event.severity === 'warning' ? 'text-orange-600 dark:text-orange-400' : ''}`}>{event.title}</h4>
                    <p className="text-sm text-muted-foreground">{event.description}</p>
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  {event.severity === 'warning' && <HealthBadge status="degraded" label="Investigating" />}
                  <span className="text-xs text-muted-foreground">{event.time_ago}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
