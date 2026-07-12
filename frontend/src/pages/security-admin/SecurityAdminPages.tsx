import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  ShieldAlert, 
  Terminal, 
  Lock, 
  Clock, 
  Globe, 
  CheckCircle, 
  FileText 
} from 'lucide-react';
import { toast } from 'sonner';

import auditService, { AuditLog } from '@/services/auditService';
import incidentsService, { SecurityAlert } from '@/services/incidentsService';

// 1. Audit Logs Page
export const SecurityAuditLogsPage: React.FC = () => {
  const [logs, setLogs] = useState<AuditLog[]>([]);

  React.useEffect(() => {
    auditService.getLogs().then(setLogs);
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Security Audit Logs</h1>
        <p className="text-muted-foreground mt-1">Audit active system login events and configuration adjustments.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Actor</TableHead>
                <TableHead>Event Type</TableHead>
                <TableHead>IP Address</TableHead>
                <TableHead>Timestamp</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {logs.map(log => (
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

// 2. Threats Page
export const ThreatsPage: React.FC = () => {
  const [threats, setThreats] = useState<SecurityAlert[]>([]);

  React.useEffect(() => {
    incidentsService.getAlerts().then(setThreats);
  }, []);

  const handleResolve = (id: string) => {
    setThreats(threats.map(t => t.id === id ? { ...t, status: 'RESOLVED' } : t));
    toast.success('Incident resolved successfully.');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Threat Monitoring</h1>
        <p className="text-muted-foreground">SOC firewall intrusion alerts and abnormal activity detection logs.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Threat Title</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>IP Source</TableHead>
                <TableHead>Detected</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {threats.map(t => (
                <TableRow key={t.id}>
                  <TableCell className="font-semibold">{t.rule_name}</TableCell>
                  <TableCell><Badge className="bg-red-500 text-white">{t.severity}</Badge></TableCell>
                  <TableCell>{t.source_ip}</TableCell>
                  <TableCell>{new Date(t.timestamp).toLocaleString()}</TableCell>
                  <TableCell className="text-right">
                    {t.status === 'OPEN' || t.status === 'INVESTIGATING' ? (
                      <Button variant="outline" size="sm" onClick={() => handleResolve(t.id)}>Resolve</Button>
                    ) : (
                      <Badge className="bg-green-500 text-white">RESOLVED</Badge>
                    )}
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

// 3. MFA Policies
export const MfaPage: React.FC = () => {
  const [mfaAdmin, setMfaAdmin] = useState(true);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">MFA Policies</h1>
        <p className="text-muted-foreground">Force multi-factor device authentication across specific roles.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="space-y-4 pt-6 max-w-lg">
          <div className="flex justify-between items-center border-b pb-3">
            <div>
              <p className="font-semibold text-sm">Strict MFA for Admins</p>
              <p className="text-xs text-muted-foreground">Require YubiKey/Authenticator verification code on login.</p>
            </div>
            <input type="checkbox" checked={mfaAdmin} onChange={e => { setMfaAdmin(e.target.checked); toast.success('MFA Admin policy updated.'); }} className="rounded" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// 4. Sessions Page
export const SessionsPage: React.FC = () => {
  const [sessions, setSessions] = useState([
    { id: '1', device: 'Chrome on macOS', location: 'New York, US', ip: '192.168.1.1', status: 'ACTIVE' }
  ]);

  const handleRevoke = (id: string) => {
    setSessions(sessions.filter(s => s.id !== id));
    toast.success('Session terminated.');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Sessions Control</h1>
        <p className="text-muted-foreground">Monitor and terminate active user login states.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Browser / Device</TableHead>
                <TableHead>Location</TableHead>
                <TableHead>IP Address</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sessions.map(s => (
                <TableRow key={s.id}>
                  <TableCell className="font-semibold">{s.device}</TableCell>
                  <TableCell>{s.location}</TableCell>
                  <TableCell>{s.ip}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" onClick={() => handleRevoke(s.id)}>Revoke</Button>
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

// 5. IP Management Page
export const IpManagementPage: React.FC = () => {
  const [ip, setIp] = useState('192.168.1.1');

  const handleSave = () => {
    toast.success(`Whitelisted network IPs saved: ${ip}`);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">IP Management</h1>
        <p className="text-muted-foreground">Limit panel authentication to whitelisted IP blocks.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="space-y-4 pt-6 max-w-lg">
          <div className="space-y-1">
            <Label>IP Whitelists</Label>
            <div className="flex gap-2">
              <Input value={ip} onChange={e => setIp(e.target.value)} />
              <Button onClick={handleSave}>Save</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// 6. Permissions Page
export const PermissionsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">SOC Permissions Audit</h1>
        <p className="text-muted-foreground">Audit security credentials and assigned access levels.</p>
      </div>
      <Card className="glass-card">
        <CardContent className="p-6 text-center text-muted-foreground">
          <ShieldAlert className="w-12 h-12 text-primary mx-auto mb-4" />
          <p className="font-medium text-foreground">Access controls and permission matrix are running globally.</p>
        </CardContent>
      </Card>
    </div>
  );
};

// 7. Compliance Page
export const CompliancePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Compliance Reports</h1>
        <p className="text-muted-foreground">Download SOC2, HIPAA, and GDPR verification logs.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="glass-card">
          <CardHeader><CardTitle>SOC2 Compliance Audit</CardTitle></CardHeader>
          <CardContent>
            <Button variant="outline" onClick={() => toast.success('Downloading SOC2 Compliance audit report')}><FileText className="w-4 h-4 mr-2" /> Download Report</Button>
          </CardContent>
        </Card>
        <Card className="glass-card">
          <CardHeader><CardTitle>HIPAA Compliance Check</CardTitle></CardHeader>
          <CardContent>
            <Button variant="outline" onClick={() => toast.success('Downloading HIPAA Audit Log')}><FileText className="w-4 h-4 mr-2" /> Download Report</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
