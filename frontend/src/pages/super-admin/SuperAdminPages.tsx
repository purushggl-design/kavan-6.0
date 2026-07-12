import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { SectionHeader } from '@/components/enterprise/SectionHeader';
import { StatCard } from '@/components/enterprise/StatCard';
import { 
  Building2, 
  Shield, 
  BarChart3, 
  Cpu, 
  Activity, 
  CreditCard, 
  Key, 
  Settings, 
  Tv, 
  Lock, 
  Database, 
  Bot,
  Plus,
  Trash2,
  Edit,
  Save,
  CheckCircle,
  AlertTriangle,
  FileDown,
  Sparkles,
  Search,
  Globe
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  AreaChart, 
  Area,
  XAxis, 
  YAxis, 
  CartesianGrid,
  Tooltip
} from 'recharts';
import { toast } from 'sonner';

import rbacService from '@/services/rbacService';
import auditService, { AuditLog } from '@/services/auditService';
import monitoringService, { SystemHealth } from '@/services/monitoringService';
import dashboardService from '@/services/dashboardService';
import tenantService from '@/services/tenantService';



// 2. Roles & Permissions Page
export const RolesPermissionsPage: React.FC = () => {
  const [roles, setRoles] = useState<{ id: string; name: string; description: string; permissions: any[] }[]>([]);

  React.useEffect(() => {
    rbacService.getPlatformPermissions().then((data) => {
      // Mock grouping or mapping from the generic list since API might just return Flat permissions
      // We'll construct standard roles here or read them from real DB if available
      setRoles([
        { id: '1', name: 'SUPER_ADMIN', description: 'Full System Control access', permissions: [] },
        { id: '2', name: 'TENANT_ADMIN', description: 'Organization wide control access', permissions: [] },
        { id: '3', name: 'SECURITY_ANALYST', description: 'SOC incident operations', permissions: [] },
        { id: '4', name: 'DEVELOPER', description: 'App and platform developer', permissions: [] },
      ]);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Roles & Permissions</h1>
        <p className="text-muted-foreground">Define RBAC permission scopes globally.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Role Title</TableHead>
                <TableHead>Access Description</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {roles.map(r => (
                <TableRow key={r.id}>
                  <TableCell className="font-semibold">{r.name.replace('_', ' ')}</TableCell>
                  <TableCell>{r.description}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" onClick={() => toast.success(`Simulating permissions matrix for ${r.name}`)}>
                      Configure matrix
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

// 3. Analytics Page
export const AnalyticsPage: React.FC = () => {
  const [timeframe, setTimeframe] = useState<'today' | '7d' | '30d' | 'quarter' | 'year'>('30d');
  const [tenantCount, setTenantCount] = useState<number>(0);

  React.useEffect(() => {
    tenantService.list().then(res => setTenantCount(res.count || res.data?.length || 0)).catch(() => {});
  }, []);

  // Mock data for 24 months revenue history
  const monthlyRevenueData = [
    { month: 'Jul 24', revenue: 28000, forecast: 28000 },
    { month: 'Aug 24', revenue: 29500, forecast: 29500 },
    { month: 'Sep 24', revenue: 31000, forecast: 31000 },
    { month: 'Oct 24', revenue: 33400, forecast: 33400 },
    { month: 'Nov 24', revenue: 34000, forecast: 34000 },
    { month: 'Dec 24', revenue: 38200, forecast: 38200 },
    { month: 'Jan 25', revenue: 39000, forecast: 39000 },
    { month: 'Feb 25', revenue: 41200, forecast: 41200 },
    { month: 'Mar 25', revenue: 42000, forecast: 42000 },
    { month: 'Apr 25', revenue: 44900, forecast: 44900 },
    { month: 'May 25', revenue: 47000, forecast: 47000 },
    { month: 'Jun 25', revenue: 48290, forecast: 50500 }, // June 25 is current month
  ];

  // Daily Users Growth
  const userGrowthData = [
    { day: '06/23', active: 7800, newRegs: 120 },
    { day: '06/24', active: 7920, newRegs: 98 },
    { day: '06/25', active: 8100, newRegs: 145 },
    { day: '06/26', active: 8050, newRegs: 110 },
    { day: '06/27', active: 8300, newRegs: 160 },
    { day: '06/28', active: 8420, newRegs: 175 },
    { day: '06/29', active: 8420, newRegs: 180 },
  ];

  // Org distributions
  const orgDistributionData = [
    { name: 'Enterprise', value: 15 },
    { name: 'Startup', value: 20 },
    { name: 'Education', value: 5 },
    { name: 'Government', value: 4 },
    { name: 'Healthcare', value: 6 },
  ];
  const ORG_COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  // Subscription plan growth
  const subscriptionPlans = [
    { plan: 'Free', users: 3400, revenue: 0, growth: 5 },
    { plan: 'Basic', users: 4100, revenue: 82000, growth: 12 },
    { plan: 'Premium', users: 1900, revenue: 171000, growth: 18 },
    { plan: 'Enterprise', users: 600, revenue: 326480, growth: 22 },
  ];

  // API Requests latency logs
  const apiMonitoringLogs = [
    { hour: '00:00', requests: 120000, errors: 4, latency: 15 },
    { hour: '04:00', requests: 80000, errors: 1, latency: 12 },
    { hour: '08:00', requests: 240000, errors: 12, latency: 18 },
    { hour: '12:00', requests: 450000, errors: 28, latency: 24 },
    { hour: '16:00', requests: 380000, errors: 15, latency: 19 },
    { hour: '20:00', requests: 190000, errors: 8, latency: 14 },
  ];

  // Security incidents
  const securityAnalyticsData = [
    { category: 'Failed Logins', value: 124 },
    { category: 'MFA Violations', value: 12 },
    { category: 'Threat Blocked', value: 8 },
    { category: 'SOC Incidents', value: 0 },
  ];

  // Tenants growth
  const tenantGrowth = [
    { month: 'Jan', active: 38, churn: 1 },
    { month: 'Feb', active: 40, churn: 0 },
    { month: 'Mar', active: 42, churn: 1 },
    { month: 'Apr', active: 45, churn: 0 },
    { month: 'May', active: 48, churn: 0 },
    { month: 'Jun', active: 50, churn: 1 },
  ];

  // Region breakdown
  const regionalData = [
    { region: 'US East', active: 18 },
    { region: 'US West', active: 12 },
    { region: 'EU Central', active: 14 },
    { region: 'APAC South', active: 6 },
  ];

  const handleExport = (format: 'csv' | 'excel' | 'pdf' | 'png') => {
    toast.success(`Exporting platform analytics as ${format.toUpperCase()}...`);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500 pb-12">
      {/* Header section */}
      <SectionHeader 
        title="Super Admin Analytics" 
        description="Enterprise-grade telemetry, revenue curves, and network API audit logs."
      >
        <div className="flex flex-wrap items-center gap-2">
          {/* Timeframe Filters */}
          <div className="flex bg-muted rounded-md p-1 border">
            {[
              { id: 'today', label: 'Today' },
              { id: '7d', label: '7 Days' },
              { id: '30d', label: '30 Days' },
              { id: 'quarter', label: 'Quarter' },
              { id: 'year', label: 'Year' },
            ].map(t => (
              <button
                key={t.id}
                onClick={() => { setTimeframe(t.id as any); toast.success(`Filter set to ${t.label}`); }}
                className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                  timeframe === t.id ? 'bg-background shadow text-foreground' : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Export options */}
          <div className="flex gap-1">
            <Button size="sm" variant="outline" onClick={() => handleExport('csv')}>CSV</Button>
            <Button size="sm" variant="outline" onClick={() => handleExport('excel')}>Excel</Button>
            <Button size="sm" variant="outline" onClick={() => handleExport('pdf')}>PDF</Button>
            <Button size="sm" variant="outline" onClick={() => handleExport('png')}>PNG</Button>
          </div>
        </div>
      </SectionHeader>

      {/* AI Insights Banner */}
      <Card className="border-primary/20 bg-primary/5 shadow-inner">
        <CardContent className="p-4 flex items-center gap-3">
          <Sparkles className="w-5 h-5 text-primary animate-pulse" />
          <div className="text-sm">
            <span className="font-bold text-primary">AI Intelligence Engine:</span>{' '}
            <span className="text-foreground/90 font-medium">
              "Monthly subscription revenue increased by 18% YoY. Security threat logs indicate intrusion events reduced by 25%. Enterprise plans exhibit strongest seat expansion."
            </span>
          </div>
        </CardContent>
      </Card>

      {/* KPI Cards Grid */}
      <div className="grid gap-4 grid-cols-2 lg:grid-cols-5">
        {[
          { title: 'Total Organizations', value: `${tenantCount} Tenants`, trend: '+8.4%', sub: 'vs last month' },
          { title: 'Total Users', value: '10,000', trend: '+12.1%', sub: 'vs last month' },
          { title: 'Active Users', value: '8,420 Active', trend: '+15.2%', sub: '84.2% engagement' },
          { title: 'Monthly Revenue', value: '$48,290.00', trend: '+18.0%', sub: 'MRR target reached' },
          { title: 'Annual Forecast', value: '$579,480.00', trend: '+22.5%', sub: 'ARR run rate' },
          { title: 'Active Sessions', value: '1,492', trend: '+5.3%', sub: 'Concurrent web users' },
          { title: 'API Requests', value: '2.4M', trend: '+14.6%', sub: 'Last 30 days log' },
          { title: 'System Health', value: '99.98% uptime', trend: 'Stable', sub: 'Nodes healthy' },
          { title: 'Security Alerts', value: '0 Open', trend: '-25.0%', sub: 'SOC incidents' },
          { title: 'YoY Growth', value: '+11.8%', trend: 'Strong', sub: 'Subscription expansion' },
        ].map((kpi, idx) => {
          const isPos = kpi.trend.startsWith('+') || kpi.trend === 'Stable' || kpi.trend === 'Strong';
          const isNeg = kpi.trend.startsWith('-');
          return (
            <StatCard 
              key={idx}
              title={kpi.title}
              value={kpi.value}
              trend={{ 
                value: kpi.trend, 
                isPositive: kpi.title === 'Security Alerts' ? isNeg : isPos 
              }}
              description={kpi.sub}
            />
          );
        })}
      </div>

      {/* Main Charts Row */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Revenue Analytics Line Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Revenue Analytics</CardTitle>
            <CardDescription>MRR trend history and forecast run rate.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyRevenueData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="revenue" stroke="#3b82f6" strokeWidth={3} name="Revenue ($)" />
                <Line type="monotone" dataKey="forecast" stroke="#10b981" strokeWidth={2} name="Forecast ($)" strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* User Growth Line Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>User Activity & Growth</CardTitle>
            <CardDescription>Daily active users vs new workspace registrations.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={userGrowthData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="active" stroke="#8b5cf6" strokeWidth={3} name="Active Users" />
                <Line type="monotone" dataKey="newRegs" stroke="#f59e0b" strokeWidth={2} name="New Registrations" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Organization Distribution Pie Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Organization Distribution</CardTitle>
            <CardDescription>Tenant distribution classification.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px] flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={orgDistributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={95}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {orgDistributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={ORG_COLORS[index % ORG_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="flex flex-col gap-2 ml-4">
              {orgDistributionData.map((entry, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: ORG_COLORS[idx % ORG_COLORS.length] }} />
                  <span className="text-xs font-semibold">{entry.name} ({entry.value})</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Subscription Plan Bar Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Subscription Revenue Share</CardTitle>
            <CardDescription>Consolidated revenue generation per active billing tier.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={subscriptionPlans}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="plan" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="revenue" fill="#10b981" radius={[4, 4, 0, 0]} name="Revenue ($)" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* API Latency Area Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>API Performance logs</CardTitle>
            <CardDescription>Average API endpoint response delay and errors.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={apiMonitoringLogs}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="requests" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.1} name="Requests Count" />
                <Area type="monotone" dataKey="latency" stroke="#ec4899" fill="#ec4899" fillOpacity={0.1} name="Avg Latency (ms)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Security Analytics Bar Chart */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>SOC Incidents Log</CardTitle>
            <CardDescription>Firewall intrusion audits and login threat counts.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={securityAnalyticsData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#ef4444" radius={[4, 4, 0, 0]} name="Incidents Count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Tenant Growth & Churn */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Tenant organic expansion</CardTitle>
            <CardDescription>New tenants acquisition and active subscriptions counts.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={tenantGrowth}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="active" stroke="#10b981" strokeWidth={3} name="Active Tenants" />
                <Line type="monotone" dataKey="churn" stroke="#ef4444" strokeWidth={2} name="Churned Tenants" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Regional Distribution Fallback Map */}
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Geographic Tenants breakdown</CardTitle>
            <CardDescription>Regional network user connections.</CardDescription>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={regionalData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                <XAxis type="number" />
                <YAxis dataKey="region" type="category" />
                <Tooltip />
                <Bar dataKey="active" fill="#f59e0b" radius={[0, 4, 4, 0]} name="Active Tenants" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* System Health meters row */}
      <div className="space-y-3">
        <h3 className="font-bold text-lg">System Hardware Health Triage</h3>
        <div className="grid gap-4 md:grid-cols-5">
          {[
            { label: 'CPU Allocation', value: '42%', color: 'bg-primary' },
            { label: 'Memory Allocation', value: '68%', color: 'bg-purple-500' },
            { label: 'Disk Allocation', value: '12%', color: 'bg-green-500' },
            { label: 'Database Connections', value: '12%', color: 'bg-amber-500' },
            { label: 'Network Latency', value: '14 ms', color: 'bg-cyan-500' },
          ].map((item, idx) => (
            <Card key={idx} className="glass-card">
              <CardContent className="p-4">
                <p className="text-xs text-muted-foreground font-semibold">{item.label}</p>
                <div className="text-xl font-bold mt-1">{item.value}</div>
                <div className="w-full bg-muted rounded-full h-1.5 mt-2">
                  <div className={`h-1.5 rounded-full ${item.color}`} style={{ width: item.value.includes('ms') ? '14%' : item.value }} />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Audit Timeline Logs */}
      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Real-Time Audit Timeline</CardTitle>
          <CardDescription>Recent administrative activities and system updates logs.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {[
            { actor: 'superadmin@kavan.com', event: 'REVENUE_EXPORTS', desc: 'Triggered PDF charts generation', time: '5 mins ago' },
            { actor: 'admin@kavan.com', event: 'PLAN_UPGRADE', desc: 'Acme Corp upgraded to Enterprise plan', time: '2 hours ago' },
            { actor: 'security@kavan.com', event: 'IP_WHITELIST_SAVE', desc: 'Updated security network whitelists block', time: '4 hours ago' },
          ].map((log, idx) => (
            <div key={idx} className="flex justify-between items-center border-b pb-3 text-sm last:border-b-0 last:pb-0">
              <div className="space-y-0.5">
                <p className="font-semibold">{log.actor}</p>
                <p className="text-xs text-muted-foreground">{log.desc}</p>
              </div>
              <div className="text-right">
                <Badge variant="outline">{log.event}</Badge>
                <p className="text-[10px] text-muted-foreground mt-0.5">{log.time}</p>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};

// 4. System Monitoring Page
export const SystemMonitoringPage: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);

  React.useEffect(() => {
    monitoringService.getHealth().then(setHealth);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">System Monitoring</h1>
        <p className="text-muted-foreground">CPU, Memory, and global service health logs.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="glass-card">
          <CardHeader><CardTitle>Infrastructure Load</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1"><span>CPU Usage</span><span className="font-bold">{health?.cpu_usage || 0}%</span></div>
              <div className="w-full bg-muted rounded-full h-2"><div className="bg-primary h-2 rounded-full" style={{ width: `${health?.cpu_usage || 0}%` }} /></div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1"><span>Memory Allocation</span><span className="font-bold">{health?.memory_usage || 0}%</span></div>
              <div className="w-full bg-muted rounded-full h-2"><div className="bg-purple-500 h-2 rounded-full" style={{ width: `${health?.memory_usage || 0}%` }} /></div>
            </div>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardHeader><CardTitle>Service Node Health</CardTitle></CardHeader>
          <CardContent className="space-y-2">
            {health?.services.map((s, i) => (
              <div key={i} className="flex justify-between">
                <span>{s.name}</span>
                <Badge className={s.status === 'HEALTHY' ? "bg-green-500 text-white" : "bg-red-500 text-white"}>
                  {s.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

// 5. Audit Logs Page
export const AuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);

  React.useEffect(() => {
    auditService.getLogs().then(setLogs);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Audit Logs</h1>
        <p className="text-muted-foreground">Compliance audit events and user action trails.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Actor</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>IP</TableHead>
                <TableHead>Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {logs.map((log) => (
                <TableRow key={log.id}>
                  <TableCell>{log.actor}</TableCell>
                  <TableCell><Badge variant="outline">{log.action}</Badge></TableCell>
                  <TableCell>{log.ip_address}</TableCell>
                  <TableCell>{new Date(log.created_at).toLocaleString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

// 6. Subscriptions Page
export const SubscriptionsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Subscriptions Control</h1>
        <p className="text-muted-foreground">Manage global billing tiers and active usage levels.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-3">
        {['Starter Plan', 'Pro Business', 'Enterprise Custom'].map((plan, i) => (
          <Card key={i} className="glass-card">
            <CardHeader>
              <CardTitle>{plan}</CardTitle>
              <CardDescription>Plan description and details.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <span className="text-2xl font-bold">${(i + 1) * 99}/mo</span>
              <p className="text-xs text-muted-foreground">Active seats: {(i + 1) * 45}</p>
              <Button onClick={() => toast.success(`Configuration for ${plan} saved.`)} className="w-full">Edit Plan Info</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

// 7. Licenses Page
export const LicensesPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Licenses</h1>
        <p className="text-muted-foreground">Seat allocation details and corporate license keys.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>License Key</TableHead>
                <TableHead>Allocated Seats</TableHead>
                <TableHead>Expiry Date</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell><code className="bg-muted px-2 py-1 rounded">KV-KEY-9238-A930</code></TableCell>
                <TableCell>150 seats</TableCell>
                <TableCell>2027-12-31</TableCell>
                <TableCell className="text-right"><Button variant="ghost" size="sm" onClick={() => toast.success('Key refreshed')}>Refresh key</Button></TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};

// 8. Global Settings Page
export const GlobalSettingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Global Settings</h1>
        <p className="text-muted-foreground">SMTP configuration, base currency parameters and API access tokens.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="space-y-4 pt-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <Label>Base Localization Currency</Label>
              <Input defaultValue="USD ($)" />
            </div>
            <div className="space-y-1">
              <Label>SMTP Gateway Endpoint</Label>
              <Input defaultValue="smtp.kavan.com" />
            </div>
          </div>
          <Button onClick={() => toast.success('Global settings updated.')}><Save className="w-4 h-4 mr-2" /> Save Global Settings</Button>
        </CardContent>
      </Card>
    </div>
  );
};

// 9. Feature Toggles Page
export const FeatureTogglesPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Feature Toggles</h1>
        <p className="text-muted-foreground">Manage active workspace feature releases and module visibility rules.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="space-y-4 pt-6">
          <div className="flex justify-between items-center border-b pb-3">
            <div>
              <h4 className="font-semibold text-sm">Beta Custom Graph Builder</h4>
              <p className="text-xs text-muted-foreground">Expose new charts layout in report generator.</p>
            </div>
            <Button size="sm" onClick={() => toast.success('Feature toggled successfully.')}>Toggle module</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// 10. Maintenance Page
export const MaintenancePage: React.FC = () => {
  const [maintenance, setMaintenance] = useState(false);

  const handleToggle = () => {
    setMaintenance(!maintenance);
    toast.success(maintenance ? 'Maintenance Mode Disabled' : 'Maintenance Mode Enabled');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Maintenance Mode</h1>
        <p className="text-muted-foreground">Force-place KAVAN into maintenance mode and customize downtime messaging.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="space-y-4 pt-6">
          <div className="p-4 bg-orange-500/10 border border-orange-500/20 rounded-lg flex gap-3">
            <AlertTriangle className="w-5 h-5 text-orange-500 mt-0.5" />
            <div>
              <h4 className="font-semibold text-orange-600 dark:text-orange-400">Notice</h4>
              <p className="text-xs text-muted-foreground">Activating this mode blocks all standard tenant users from accessing directories.</p>
            </div>
          </div>
          <Button onClick={handleToggle} variant={maintenance ? 'destructive' : 'default'}>
            {maintenance ? 'Disable Maintenance' : 'Enable Maintenance'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
};

// 11. Database Monitor Page
export const DatabaseMonitorPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Database Monitor</h1>
        <p className="text-muted-foreground">Verify queries performance and snapshot status logs.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="glass-card">
          <CardHeader><CardTitle>Storage Allocation</CardTitle></CardHeader>
          <CardContent><span className="text-2xl font-bold">12.4 GB / 100 GB used</span></CardContent>
        </Card>
        <Card className="glass-card">
          <CardHeader><CardTitle>Backup Snapshot Status</CardTitle></CardHeader>
          <CardContent><Badge className="bg-green-500 text-white">UP-TO-DATE</Badge></CardContent>
        </Card>
      </div>
    </div>
  );
};

// 12. AI Assistant Page
export const AiAssistantPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Assistant Console</h1>
        <p className="text-muted-foreground">Manage KAVAN intelligence recommendations and workspace chat prompts.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-6 text-center text-muted-foreground">
          <Bot className="w-12 h-12 text-primary mx-auto mb-4" />
          <p className="font-medium text-foreground">AI Intelligence Agent is running globally.</p>
          <p className="text-xs mt-1">Chat widget can be expanded using the bubble in the bottom right corner.</p>
        </CardContent>
      </Card>
    </div>
  );
};
