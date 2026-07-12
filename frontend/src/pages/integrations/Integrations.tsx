import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogFooter,
  DialogDescription
} from '@/components/ui/dialog';
import { 
  Link, 
  Unlink, 
  Key, 
  RefreshCw, 
  Copy,
  Hash,
  Globe,
  Settings,
  Plus
} from 'lucide-react';
import { toast } from 'sonner';

interface Integration {
  id: string;
  name: string;
  type: string;
  status: 'CONNECTED' | 'DISCONNECTED';
  lastSync: string;
}

interface ApiKey {
  id: string;
  name: string;
  token: string;
  created: string;
}

export const Integrations: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'services' | 'apikeys'>('services');

  // Integrations State
  const [integrations, setIntegrations] = useState<Integration[]>([
    { id: '1', name: 'Google Workspace', type: 'HR & Directory Sync', status: 'CONNECTED', lastSync: '2 hours ago' },
    { id: '2', name: 'Hash Integration', type: 'Notifications Delivery', status: 'CONNECTED', lastSync: '10 mins ago' },
    { id: '3', name: 'Microsoft 365', type: 'Authentication SSO', status: 'DISCONNECTED', lastSync: 'Never' },
  ]);

  // API Keys State
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([
    { id: 'k1', name: 'Production Dashboard Sync', token: 'kv_live_••••••••••••••••3a90', created: '2026-05-12' },
  ]);
  const [newKeyName, setNewKeyName] = useState('');
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);

  const handleToggleConnect = (id: string, currentStatus: string) => {
    const nextStatus = currentStatus === 'CONNECTED' ? 'DISCONNECTED' : 'CONNECTED';
    setIntegrations(integrations.map(item => {
      if (item.id === id) {
        return {
          ...item,
          status: nextStatus,
          lastSync: nextStatus === 'CONNECTED' ? 'Just now' : 'Never'
        };
      }
      return item;
    }));
    toast.success(nextStatus === 'CONNECTED' ? `Connected successfully!` : `Disconnected successfully.`);
  };

  const handleCreateApiKey = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newKeyName) {
      toast.error('Please enter a key name.');
      return;
    }
    const newKey: ApiKey = {
      id: Math.random().toString(36).substr(2, 9),
      name: newKeyName,
      token: `kv_live_${Math.random().toString(36).substr(2, 16)}`,
      created: new Date().toISOString().split('T')[0]
    };
    setApiKeys([...apiKeys, newKey]);
    setNewKeyName('');
    setIsKeyModalOpen(false);
    toast.success('API Key created successfully!');
  };

  const handleCopyKey = (token: string) => {
    navigator.clipboard.writeText(token);
    toast.success('API Key copied to clipboard.');
  };

  const handleDeleteKey = (id: string) => {
    setApiKeys(apiKeys.filter(k => k.id !== id));
    toast.success('API Key revoked.');
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Integrations</h1>
          <p className="text-muted-foreground mt-1">Connect third-party enterprise tools and manage developer API keys.</p>
        </div>
        <div className="flex gap-2">
          {activeTab === 'apikeys' && (
            <Button onClick={() => setIsKeyModalOpen(true)} size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Generate API Key
            </Button>
          )}
        </div>
      </div>

      <div className="flex border-b">
        {[
          { id: 'services', label: 'Third-Party Services', icon: Link },
          { id: 'apikeys', label: 'Developer API Keys', icon: Key },
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

      {activeTab === 'services' && (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Connected Integrations</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Integration Service</TableHead>
                  <TableHead>Scope / Purpose</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Last Synchronized</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {integrations.map(item => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        {item.name.includes('Hash') ? (
                          <div className="w-8 h-8 rounded-lg bg-orange-500/10 flex items-center justify-center text-orange-500">
                            <Hash className="w-5 h-5" />
                          </div>
                        ) : (
                          <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                            <Globe className="w-5 h-5" />
                          </div>
                        )}
                        <span className="font-semibold text-foreground">{item.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>{item.type}</TableCell>
                    <TableCell>
                      <Badge variant={item.status === 'CONNECTED' ? 'default' : 'secondary'} className={item.status === 'CONNECTED' ? 'bg-green-500 hover:bg-green-600 text-white' : ''}>
                        {item.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-muted-foreground text-xs">{item.lastSync}</TableCell>
                    <TableCell className="text-right">
                      <Button 
                        variant={item.status === 'CONNECTED' ? 'destructive' : 'default'} 
                        size="sm"
                        onClick={() => handleToggleConnect(item.id, item.status)}
                      >
                        {item.status === 'CONNECTED' ? (
                          <>
                            <Unlink className="w-4 h-4 mr-2" />
                            Disconnect
                          </>
                        ) : (
                          <>
                            <Link className="w-4 h-4 mr-2" />
                            Connect
                          </>
                        )}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {activeTab === 'apikeys' && (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Active Developer Keys</CardTitle>
            <CardDescription>Verify request authenticity using these keys for REST API integrations.</CardDescription>
          </CardHeader>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Key Name</TableHead>
                  <TableHead>API Token</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {apiKeys.map(k => (
                  <TableRow key={k.id}>
                    <TableCell className="font-semibold">{k.name}</TableCell>
                    <TableCell>
                      <code className="text-xs bg-muted px-2 py-1 rounded font-mono select-all">{k.token}</code>
                    </TableCell>
                    <TableCell>{k.created}</TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-1">
                        <Button variant="ghost" size="icon" onClick={() => handleCopyKey(k.token)} title="Copy Key">
                          <Copy className="w-4 h-4 text-blue-500" />
                        </Button>
                        <Button variant="ghost" size="icon" onClick={() => handleDeleteKey(k.id)} title="Revoke Key">
                          <Unlink className="w-4 h-4 text-destructive" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {/* Generate API Key Modal */}
      <Dialog open={isKeyModalOpen} onOpenChange={setIsKeyModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Generate Developer API Key</DialogTitle>
            <DialogDescription>Generate a new token for REST endpoint verification.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleCreateApiKey} className="space-y-4">
            <div className="space-y-1">
              <Label htmlFor="key-name">API Key Name</Label>
              <Input 
                id="key-name"
                value={newKeyName} 
                onChange={e => setNewKeyName(e.target.value)} 
                placeholder="E.g., staging-analytics-sync" 
              />
            </div>
            
            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => setIsKeyModalOpen(false)}>
                Cancel
              </Button>
              <Button type="submit">
                Generate Token
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};
