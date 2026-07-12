import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Terminal, Hash, Server, CheckCircle2 } from 'lucide-react';
import { SectionHeader } from '@/components/enterprise/SectionHeader';
import { StatCard } from '@/components/enterprise/StatCard';
import { HealthBadge } from '@/components/enterprise/HealthBadge';

interface DeveloperDashboardData {
  api_uptime: string;
  open_prs: number;
  last_deploy: string;
  build_status: string;
  system_logs: string[];
}

export const DeveloperDashboard: React.FC = () => {
  const [data, setData] = useState<DeveloperDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const res = await fetch('http://127.0.0.1:8000/api/v1/monitoring/dashboards/developer/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) throw new Error('Failed to fetch developer dashboard');
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

  if (loading) return <div className="text-white">Loading developer dashboard...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;
  if (!data) return null;

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <SectionHeader 
        title="Developer Console" 
        description="API Health, deployments, and integration logs." 
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="API Uptime" 
          value={data.api_uptime} 
          icon={<Server className="w-4 h-4" />} 
          trend={{ value: "Operational", isPositive: true }}
          className="font-mono"
        />
        <StatCard 
          title="Open PRs" 
          value={data.open_prs.toString()} 
          icon={<Hash className="w-4 h-4" />} 
          className="font-mono"
        />
        <StatCard 
          title="Last Deploy" 
          value={data.last_deploy} 
          icon={<Terminal className="w-4 h-4" />} 
          className="font-mono"
        />
        <StatCard 
          title="Build Status" 
          value={data.build_status} 
          icon={<CheckCircle2 className="w-4 h-4" />} 
          trend={{ value: "Stable", isPositive: true }}
          className="font-mono"
        />
      </div>

      <Card className="glass-card bg-black text-green-400 border-none shadow-2xl">
        <CardHeader className="border-b border-green-900/50 pb-4">
          <CardTitle className="text-sm font-mono text-green-500 flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4" />
              System Logs
            </div>
            <HealthBadge status="healthy" label="System Online" className="bg-green-900/30 text-green-400 border-green-800" />
          </CardTitle>
        </CardHeader>
        <CardContent className="font-mono text-xs pt-4 h-64 overflow-y-auto">
          <div className="space-y-2 opacity-80">
            {data.system_logs.map((log, index) => {
              let colorClass = "text-white";
              if (log.includes("[INFO]")) colorClass = "text-gray-300";
              if (log.includes("[SUCCESS]")) colorClass = "text-green-400";
              if (log.includes("[DEBUG]")) colorClass = "text-blue-400";
              if (log.includes("[WARN]")) colorClass = "text-yellow-400";
              if (log.includes("[ERROR]")) colorClass = "text-red-400";
              return <p key={index} className={colorClass}>{log}</p>;
            })}
            <p className="animate-pulse">_</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
