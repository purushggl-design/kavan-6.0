import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Terminal, Hash, Server, CheckCircle2 } from 'lucide-react';

export const DeveloperDashboard: React.FC = () => {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-blue-500 dark:text-blue-400">Developer Console</h2>
        <p className="text-muted-foreground mt-1">API Health, deployments, and integration logs.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {[
          { title: 'API Uptime', value: '99.99%', icon: Server, color: 'text-green-500', bg: 'bg-green-500/10' },
          { title: 'Open PRs', value: '12', icon: Hash, color: 'text-foreground', bg: 'bg-muted' },
          { title: 'Last Deploy', value: '2h ago', icon: Terminal, color: 'text-blue-500', bg: 'bg-blue-500/10' },
          { title: 'Build Status', value: 'Passing', icon: CheckCircle2, color: 'text-green-500', bg: 'bg-green-500/10' },
        ].map((stat, i) => (
          <Card key={i} className="glass-card font-mono">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-xs text-muted-foreground uppercase">{stat.title}</CardTitle>
              <div className={`p-2 rounded-lg ${stat.bg}`}>
                <stat.icon className={`w-4 h-4 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="glass-card bg-black text-green-400 border-none shadow-2xl">
        <CardHeader className="border-b border-green-900/50 pb-4">
          <CardTitle className="text-sm font-mono text-green-500 flex items-center gap-2">
            <Terminal className="w-4 h-4" />
            System Logs
          </CardTitle>
        </CardHeader>
        <CardContent className="font-mono text-xs pt-4 h-64 overflow-y-auto">
          <div className="space-y-2 opacity-80">
            <p>[INFO] 10:24:01 - Deployment pipeline triggered for kavan-core-v6</p>
            <p>[INFO] 10:24:45 - Building Docker image...</p>
            <p>[INFO] 10:26:12 - Pushing to registry...</p>
            <p>[SUCCESS] 10:28:00 - Rollout successful across 3 regions.</p>
            <p className="text-blue-400">[DEBUG] 10:30:15 - Auth service cache hit ratio: 94.2%</p>
            <p className="text-yellow-400">[WARN] 10:45:02 - High latency detected on database replica set 2</p>
            <p className="animate-pulse">_</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
