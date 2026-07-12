import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ShieldAlert, Activity, Lock, Search } from 'lucide-react';

export const SecurityDashboard: React.FC = () => {
  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-red-500 dark:text-red-400">Security Operations Center</h2>
        <p className="text-muted-foreground mt-1">Real-time threat detection and access monitoring.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {[
          { title: 'Active Threats', value: '0', icon: ShieldAlert, color: 'text-green-500', bg: 'bg-green-500/10' },
          { title: 'Failed Logins (24h)', value: '1,204', icon: Lock, color: 'text-orange-500', bg: 'bg-orange-500/10' },
          { title: 'Anomaly Score', value: 'Low', icon: Activity, color: 'text-blue-500', bg: 'bg-blue-500/10' },
          { title: 'Open Investigations', value: '2', icon: Search, color: 'text-purple-500', bg: 'bg-purple-500/10' },
        ].map((stat, i) => (
          <Card key={i} className="glass-card border-red-500/20">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
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

      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Recent Security Events</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
              <div className="flex items-center gap-4">
                <ShieldAlert className="w-6 h-6 text-orange-500" />
                <div>
                  <h4 className="font-semibold text-orange-600 dark:text-orange-400">Multiple Failed Logins</h4>
                  <p className="text-sm text-muted-foreground">IP 192.168.1.104 attempted login 15 times.</p>
                </div>
              </div>
              <span className="text-xs text-muted-foreground">10 mins ago</span>
            </div>
            <div className="flex items-center justify-between p-4 bg-background/50 rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <Lock className="w-6 h-6 text-muted-foreground" />
                <div>
                  <h4 className="font-semibold">New MFA Device Registered</h4>
                  <p className="text-sm text-muted-foreground">User admin@tenant.com added YubiKey.</p>
                </div>
              </div>
              <span className="text-xs text-muted-foreground">2 hours ago</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
