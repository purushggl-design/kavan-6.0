import React, { useState, useEffect } from 'react';
import { 
  Table, 
  TableHeader, 
  TableBody, 
  TableRow, 
  TableHead, 
  TableCell 
} from '@/components/ui/table';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle, 
  DialogFooter,
  DialogDescription
} from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { useAppSelector } from '@/hooks/redux';
import { selectCurrentRole, selectCurrentTenant } from '@/store/authSlice';
import { 
  Search, 
  Plus, 
  Edit, 
  Trash2, 
  Building2, 
  Network,
  Settings,
  SlidersHorizontal,
  FolderTree
} from 'lucide-react';
import { toast } from 'sonner';
import { mockOrganizations as initialMockOrgs } from '@/services/mockData';
import tenantService from '@/services/tenantService';

interface Organization {
  id: string;
  name: string;
  tenantId: string;
  plan: string;
  users: number;
  status: string;
}

export const OrganizationManagement: React.FC = () => {
  const currentRole = useAppSelector(selectCurrentRole);
  const currentTenant = useAppSelector(selectCurrentTenant);
  const isSuperAdmin = currentRole === 'SUPER_ADMIN';

  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  
  // Modal states
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isHierarchyOpen, setIsHierarchyOpen] = useState(false);
  const [currentOrg, setCurrentOrg] = useState<Organization | null>(null);

  // Form states
  const [formName, setFormName] = useState('');
  const [formTenantId, setFormTenantId] = useState('');
  const [formPlan, setFormPlan] = useState('Enterprise');
  const [formUsers, setFormUsers] = useState(1);

  // Load and save logic
  useEffect(() => {
    tenantService.list().then(res => {
      if (res.data && res.data.length > 0) {
        const mapped = res.data.map(t => ({
          id: String(t.id),
          name: t.company_name || t.tenant_name,
          tenantId: t.tenant_code,
          plan: 'Enterprise',
          users: t.member_count || 1,
          status: t.tenant_status
        }));
        setOrgs(mapped);
      } else {
        const stored = localStorage.getItem('kavan_orgs');
        if (stored) {
          setOrgs(JSON.parse(stored));
        } else {
          setOrgs(initialMockOrgs);
        }
      }
    }).catch(() => {
      setOrgs(initialMockOrgs);
    });
  }, []);

  const saveOrgs = (updatedOrgs: Organization[]) => {
    setOrgs(updatedOrgs);
    localStorage.setItem('kavan_orgs', JSON.stringify(updatedOrgs));
  };

  const handleAddOrg = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName || !formTenantId) {
      toast.error('Please fill in all fields.');
      return;
    }

    const newOrg: Organization = {
      id: Math.random().toString(36).substr(2, 9),
      name: formName,
      tenantId: formTenantId,
      plan: formPlan,
      users: formUsers,
      status: 'ACTIVE'
    };

    const updated = [newOrg, ...orgs];
    saveOrgs(updated);
    setIsAddOpen(false);
    clearForm();
    toast.success('Organization created successfully!');
  };

  const handleEditOrg = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentOrg || !formName || !formTenantId) {
      toast.error('Please fill in all fields.');
      return;
    }

    const updated = orgs.map(o => {
      if (o.id === currentOrg.id) {
        return {
          ...o,
          name: formName,
          tenantId: formTenantId,
          plan: formPlan,
          users: formUsers
        };
      }
      return o;
    });

    saveOrgs(updated);
    setIsEditOpen(false);
    setCurrentOrg(null);
    clearForm();
    toast.success('Organization updated successfully!');
  };

  const handleDeleteOrg = (id: string) => {
    if (confirm('Are you sure you want to delete this organization?')) {
      const updated = orgs.filter(o => o.id !== id);
      saveOrgs(updated);
      toast.success('Organization deleted successfully!');
    }
  };

  const handleToggleStatus = (id: string, currentStatus: string) => {
    const nextStatus = currentStatus === 'ACTIVE' ? 'INACTIVE' : 'ACTIVE';
    const updated = orgs.map(o => {
      if (o.id === id) {
        return { ...o, status: nextStatus };
      }
      return o;
    });
    saveOrgs(updated);
    toast.success(`Organization status updated to ${nextStatus}`);
  };

  const openEditModal = (org: Organization) => {
    setCurrentOrg(org);
    setFormName(org.name);
    setFormTenantId(org.tenantId);
    setFormPlan(org.plan);
    setFormUsers(org.users);
    setIsEditOpen(true);
  };

  const clearForm = () => {
    setFormName('');
    setFormTenantId('');
    setFormPlan('Enterprise');
    setFormUsers(1);
  };

  // Filter computation
  const filteredOrgs = orgs.filter(org => {
    // Multi-tenant check: Tenant Admins only see their own organization
    if (!isSuperAdmin && currentTenant && org.name !== (currentTenant.company_name || currentTenant.tenant_name)) {
      return false;
    }

    const matchesSearch = 
      org.name.toLowerCase().includes(search.toLowerCase()) ||
      org.tenantId.toLowerCase().includes(search.toLowerCase()) ||
      org.plan.toLowerCase().includes(search.toLowerCase());
    
    const matchesStatus = statusFilter === 'ALL' || org.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Organization Management</h1>
          <p className="text-muted-foreground mt-1">
            {isSuperAdmin 
              ? 'Manage tenants, subscriptions, plans and overall structure globally.'
              : `Configure departments and view metrics for ${currentTenant?.company_name || currentTenant?.tenant_name || 'your organization'}.`
            }
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => setIsHierarchyOpen(true)} variant="outline" size="sm">
            <FolderTree className="w-4 h-4 mr-2" />
            Visual Hierarchy
          </Button>
          {isSuperAdmin && (
            <Button onClick={() => setIsAddOpen(true)} size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Add Organization
            </Button>
          )}
        </div>
      </div>

      {/* Control bar */}
      <Card className="glass-card">
        <CardContent className="p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Search by name, plan, tenant ID..." 
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="flex w-full md:w-auto gap-3 items-center justify-end">
            <div className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm font-medium text-muted-foreground">Filters:</span>
            </div>
            
            <select 
              value={statusFilter} 
              onChange={e => setStatusFilter(e.target.value)}
              className="bg-background border rounded-md px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="ALL">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Organizations Table */}
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Organization</TableHead>
                <TableHead>Tenant ID</TableHead>
                <TableHead>Plan</TableHead>
                <TableHead>Users Count</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredOrgs.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="h-64 text-center text-muted-foreground">
                    No organizations found.
                  </TableCell>
                </TableRow>
              ) : (
                filteredOrgs.map((org) => (
                  <TableRow key={org.id}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center text-primary">
                          <Building2 className="w-5 h-5" />
                        </div>
                        <span className="font-semibold text-foreground">{org.name}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <code className="text-xs bg-muted px-2 py-1 rounded font-mono">{org.tenantId}</code>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20">
                        {org.plan}
                      </Badge>
                    </TableCell>
                    <TableCell>{org.users}</TableCell>
                    <TableCell>
                      <Badge 
                        variant={org.status === 'ACTIVE' ? 'default' : 'secondary'} 
                        className={org.status === 'ACTIVE' ? 'bg-green-500 hover:bg-green-600 text-white' : ''}
                      >
                        {org.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-1">
                        {isSuperAdmin ? (
                          <>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              onClick={() => handleToggleStatus(org.id, org.status)}
                              title={org.status === 'ACTIVE' ? 'Deactivate Tenant' : 'Activate Tenant'}
                            >
                              <Network className={`w-4 h-4 ${org.status === 'ACTIVE' ? 'text-orange-500' : 'text-green-500'}`} />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              onClick={() => openEditModal(org)}
                              title="Edit Organization"
                            >
                              <Edit className="w-4 h-4 text-blue-500" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              onClick={() => handleDeleteOrg(org.id)}
                              title="Delete Organization"
                            >
                              <Trash2 className="w-4 h-4 text-destructive" />
                            </Button>
                          </>
                        ) : (
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => toast.info('Organization settings can be adjusted in general settings.')}
                          >
                            <Settings className="w-4 h-4 mr-2" />
                            Settings
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Visual Hierarchy Modal */}
      <Dialog open={isHierarchyOpen} onOpenChange={setIsHierarchyOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Organization Hierarchy</DialogTitle>
            <DialogDescription>Visual structure of departments, branches, and teams.</DialogDescription>
          </DialogHeader>
          <div className="p-6 border rounded-lg bg-card/50 space-y-4">
            <div className="flex flex-col items-center">
              <div className="px-4 py-2 bg-primary text-primary-foreground font-bold rounded-lg shadow">
                {currentTenant?.company_name || currentTenant?.tenant_name || 'Organization'}
              </div>
              <div className="w-0.5 h-8 bg-border" />
              
              <div className="grid grid-cols-3 gap-6 w-full relative">
                {/* Branches / Depts */}
                <div className="flex flex-col items-center border p-3 rounded-lg bg-background">
                  <span className="font-semibold text-sm">Engineering Dept</span>
                  <div className="w-0.5 h-4 bg-border my-1" />
                  <span className="text-xs text-muted-foreground">Frontend Team</span>
                  <span className="text-xs text-muted-foreground">Platform Team</span>
                </div>
                
                <div className="flex flex-col items-center border p-3 rounded-lg bg-background">
                  <span className="font-semibold text-sm">Sales & Marketing</span>
                  <div className="w-0.5 h-4 bg-border my-1" />
                  <span className="text-xs text-muted-foreground">Enterprise Team</span>
                  <span className="text-xs text-muted-foreground">Design Team</span>
                </div>

                <div className="flex flex-col items-center border p-3 rounded-lg bg-background">
                  <span className="font-semibold text-sm">Operations</span>
                  <div className="w-0.5 h-4 bg-border my-1" />
                  <span className="text-xs text-muted-foreground">HR Team</span>
                  <span className="text-xs text-muted-foreground">IT Support</span>
                </div>
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button onClick={() => setIsHierarchyOpen(false)}>Close</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Add Org Modal */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Tenant / Organization</DialogTitle>
            <DialogDescription>Provision a new enterprise tenant and database space.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleAddOrg} className="space-y-4">
            <div className="space-y-1">
              <Label htmlFor="add-org-name">Organization Name</Label>
              <Input 
                id="add-org-name"
                value={formName} 
                onChange={e => setFormName(e.target.value)} 
                placeholder="E.g., Globex Corporation" 
              />
            </div>
            
            <div className="space-y-1">
              <Label htmlFor="add-org-tenant">Tenant Unique ID</Label>
              <Input 
                id="add-org-tenant"
                value={formTenantId} 
                onChange={e => setFormTenantId(e.target.value)} 
                placeholder="globex-corp" 
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="add-org-plan">Subscription Plan</Label>
                <select 
                  id="add-org-plan"
                  value={formPlan} 
                  onChange={e => setFormPlan(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="Enterprise">Enterprise</option>
                  <option value="Pro">Pro</option>
                  <option value="Starter">Starter</option>
                </select>
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="add-org-users">Initial Users Limit</Label>
                <Input 
                  id="add-org-users"
                  type="number"
                  value={formUsers} 
                  onChange={e => setFormUsers(parseInt(e.target.value) || 0)} 
                />
              </div>
            </div>

            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => { setIsAddOpen(false); clearForm(); }}>
                Cancel
              </Button>
              <Button type="submit">
                Provision Organization
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Edit Org Modal */}
      <Dialog open={isEditOpen} onOpenChange={(open) => { if(!open) { setIsEditOpen(false); setCurrentOrg(null); } }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Organization Profile</DialogTitle>
            <DialogDescription>Modify plan limits and configuration details.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleEditOrg} className="space-y-4">
            <div className="space-y-1">
              <Label htmlFor="edit-org-name">Organization Name</Label>
              <Input 
                id="edit-org-name"
                value={formName} 
                onChange={e => setFormName(e.target.value)} 
              />
            </div>
            
            <div className="space-y-1">
              <Label htmlFor="edit-org-tenant">Tenant Unique ID</Label>
              <Input 
                id="edit-org-tenant"
                value={formTenantId} 
                onChange={e => setFormTenantId(e.target.value)} 
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="edit-org-plan">Subscription Plan</Label>
                <select 
                  id="edit-org-plan"
                  value={formPlan} 
                  onChange={e => setFormPlan(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="Enterprise">Enterprise</option>
                  <option value="Pro">Pro</option>
                  <option value="Starter">Starter</option>
                </select>
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="edit-org-users">Users Limit</Label>
                <Input 
                  id="edit-org-users"
                  type="number"
                  value={formUsers} 
                  onChange={e => setFormUsers(parseInt(e.target.value) || 0)} 
                />
              </div>
            </div>

            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => { setIsEditOpen(false); setCurrentOrg(null); clearForm(); }}>
                Cancel
              </Button>
              <Button type="submit">
                Save Changes
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
};
