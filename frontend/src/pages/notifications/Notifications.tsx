import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Label } from '@/components/ui/label';
import { 
  Bell, 
  Mail, 
  Smartphone, 
  CheckCheck, 
  Trash2, 
  SlidersHorizontal,
  Settings,
  Flame
} from 'lucide-react';
import { toast } from 'sonner';

interface NotificationItem {
  id: string;
  title: string;
  body: string;
  category: 'SECURITY' | 'BILLING' | 'SYSTEM' | 'USER';
  unread: boolean;
  time: string;
}

export const Notifications: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'inbox' | 'preferences'>('inbox');
  const [filterType, setFilterType] = useState('ALL');
  
  // Preference States
  const [emailNotif, setEmailNotif] = useState(true);
  const [pushNotif, setPushNotif] = useState(true);
  const [smsNotif, setSmsNotif] = useState(false);

  const [notifs, setNotifs] = useState<NotificationItem[]>([
    { id: '1', title: 'New Device Login Detected', body: 'Super Admin logged in from Windows Chrome - IP 192.168.1.1', category: 'SECURITY', unread: true, time: '10 mins ago' },
    { id: '2', title: 'Monthly Invoice Available', body: 'Your renewal invoice for Acme Corp has been generated.', category: 'BILLING', unread: true, time: '2 hours ago' },
    { id: '3', title: 'User Account Provisioned', body: 'Employee account employee@kavan.com was created successfully.', category: 'USER', unread: false, time: '1 day ago' },
  ]);

  const handleMarkAllRead = () => {
    setNotifs(notifs.map(n => ({ ...n, unread: false })));
    toast.success('All notifications marked as read.');
  };

  const handleMarkSingleRead = (id: string) => {
    setNotifs(notifs.map(n => n.id === id ? { ...n, unread: false } : n));
    toast.success('Notification marked as read.');
  };

  const handleDeleteNotif = (id: string) => {
    setNotifs(notifs.filter(n => n.id !== id));
    toast.success('Notification removed.');
  };

  const handleSavePreferences = () => {
    toast.success('Notification delivery channels updated.');
  };

  const filteredNotifs = notifs.filter(n => {
    if (filterType === 'ALL') return true;
    return n.category === filterType;
  });

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Notification Center</h1>
          <p className="text-muted-foreground mt-1">Manage system notifications, priority alerts, and messaging delivery preferences.</p>
        </div>
        <div className="flex gap-2">
          {activeTab === 'inbox' && (
            <Button onClick={handleMarkAllRead} variant="outline" size="sm">
              <CheckCheck className="w-4 h-4 mr-2" />
              Mark All Read
            </Button>
          )}
        </div>
      </div>

      <div className="flex border-b">
        {[
          { id: 'inbox', label: 'Inbox Alerts', icon: Bell },
          { id: 'preferences', label: 'Preferences & Templates', icon: Settings },
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center gap-2 px-6 py-3 text-sm font-medium border-b-2 transition-all ${
              activeTab === tab.id 
                ? 'border-primary text-primary' 
                : 'border-transparent text-muted-foreground hover:text-foreground'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'inbox' && (
        <div className="space-y-4">
          <Card className="glass-card">
            <CardContent className="p-4 flex gap-4 items-center justify-between">
              <div className="flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-muted-foreground" />
                <span className="text-sm font-medium text-muted-foreground">Category Filter:</span>
              </div>
              <select
                value={filterType}
                onChange={e => setFilterType(e.target.value)}
                className="bg-background border rounded-md px-3 py-1.5 text-sm outline-none"
              >
                <option value="ALL">All Notifications</option>
                <option value="SECURITY">Security</option>
                <option value="BILLING">Billing</option>
                <option value="USER">Users</option>
              </select>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-8"></TableHead>
                    <TableHead>Notification Details</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Received</TableHead>
                    <TableHead className="text-right">Action</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredNotifs.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="h-64 text-center text-muted-foreground">
                        No alerts in notification log.
                      </TableCell>
                    </TableRow>
                  ) : (
                    filteredNotifs.map(n => (
                      <TableRow key={n.id} className={n.unread ? 'bg-primary/5 font-medium' : ''}>
                        <TableCell>
                          {n.unread && <div className="w-2 h-2 rounded-full bg-primary" />}
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-col">
                            <span className="text-foreground">{n.title}</span>
                            <span className="text-xs text-muted-foreground">{n.body}</span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">{n.category}</Badge>
                        </TableCell>
                        <TableCell className="text-muted-foreground text-xs">{n.time}</TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-1">
                            {n.unread && (
                              <Button variant="ghost" size="icon" onClick={() => handleMarkSingleRead(n.id)} title="Mark Read">
                                <CheckCheck className="w-4 h-4 text-green-500" />
                              </Button>
                            )}
                            <Button variant="ghost" size="icon" onClick={() => handleDeleteNotif(n.id)} title="Delete Notif">
                              <Trash2 className="w-4 h-4 text-destructive" />
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'preferences' && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Delivery Channels</CardTitle>
              <CardDescription>Toggle how you receive alert logs.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between border-b pb-3">
                <div className="flex items-center gap-3">
                  <Mail className="w-5 h-5 text-primary" />
                  <div>
                    <p className="font-semibold text-sm">Email Delivery</p>
                    <p className="text-xs text-muted-foreground">Receive copies of critical alerts in inbox.</p>
                  </div>
                </div>
                <input type="checkbox" checked={emailNotif} onChange={e => setEmailNotif(e.target.checked)} className="rounded" />
              </div>

              <div className="flex items-center justify-between border-b pb-3">
                <div className="flex items-center gap-3">
                  <Bell className="w-5 h-5 text-primary" />
                  <div>
                    <p className="font-semibold text-sm">In-App Push</p>
                    <p className="text-xs text-muted-foreground">Show temporary banners inside KAVAN workspace.</p>
                  </div>
                </div>
                <input type="checkbox" checked={pushNotif} onChange={e => setPushNotif(e.target.checked)} className="rounded" />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Smartphone className="w-5 h-5 text-primary" />
                  <div>
                    <p className="font-semibold text-sm">SMS Text Dispatch</p>
                    <p className="text-xs text-muted-foreground">Send brief text code for security violations.</p>
                  </div>
                </div>
                <input type="checkbox" checked={smsNotif} onChange={e => setSmsNotif(e.target.checked)} className="rounded" />
              </div>

              <Button onClick={handleSavePreferences} className="w-full mt-4">
                Save Preferences
              </Button>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle>Priority System Alerts</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg flex items-start gap-3">
                <Flame className="w-5 h-5 text-red-500 mt-0.5" />
                <div>
                  <p className="font-semibold text-sm text-red-600 dark:text-red-400">SMTP Notification Failures</p>
                  <p className="text-xs text-muted-foreground">Ensure SMTP settings are authenticated in System Settings to prevent dispatch blockages.</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
