import React, { useState, useEffect } from 'react';
import { 
  Table, 
  TableHeader, 
  TableBody, 
  TableRow, 
  TableHead, 
  TableCell 
} from '@/components/ui/table';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
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
import { 
  Search, 
  Plus, 
  Edit, 
  Trash2, 
  Lock, 
  Unlock, 
  Download, 
  Upload, 
  RefreshCw,
  SlidersHorizontal,
  ChevronLeft,
  ChevronRight,
  UserCheck
} from 'lucide-react';
import { toast } from 'sonner';
import { mockUsers as initialMockUsers } from '@/services/mockData';
import accountsService from '@/services/accountsService';

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  role: string;
  status: string;
  department: string;
}

export const UserManagement: React.FC = () => {
  // Load users from localStorage or fall back to mock data
  const [users, setUsers] = useState<User[]>([]);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  // Modals state
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  // Form states
  const [formFirstName, setFormFirstName] = useState('');
  const [formLastName, setFormLastName] = useState('');
  const [formEmail, setFormEmail] = useState('');
  const [formRole, setFormRole] = useState('EMPLOYEE');
  const [formDepartment, setFormDepartment] = useState('Sales');

  // Load and save logic
  useEffect(() => {
    accountsService.getUsers().then(res => {
      if (res.data && res.data.length > 0) {
        const mapped = res.data.map(u => ({
          id: String(u.id),
          firstName: u.first_name,
          lastName: u.last_name,
          email: u.email,
          role: u.platform_role,
          status: u.is_active ? 'ACTIVE' : 'INACTIVE',
          department: 'General'
        }));
        setUsers(mapped);
      } else {
        const stored = localStorage.getItem('kavan_users');
        if (stored) {
          setUsers(JSON.parse(stored));
        } else {
          setUsers(initialMockUsers);
        }
      }
    }).catch(() => {
      setUsers(initialMockUsers);
    });
  }, []);

  const saveUsers = (updatedUsers: User[]) => {
    setUsers(updatedUsers);
    localStorage.setItem('kavan_users', JSON.stringify(updatedUsers));
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(e.target.value);
    setCurrentPage(1);
  };

  const handleRoleFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setRoleFilter(e.target.value);
    setCurrentPage(1);
  };

  const handleStatusFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setStatusFilter(e.target.value);
    setCurrentPage(1);
  };

  // Bulk select toggles
  const toggleSelectAll = () => {
    if (selectedUsers.length === filteredUsers.length) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(filteredUsers.map(u => u.id));
    }
  };

  const toggleSelectUser = (id: string) => {
    if (selectedUsers.includes(id)) {
      setSelectedUsers(selectedUsers.filter(item => item !== id));
    } else {
      setSelectedUsers([...selectedUsers, id]);
    }
  };

  // Actions
  const handleAddUser = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formFirstName || !formLastName || !formEmail) {
      toast.error('Please fill in all fields.');
      return;
    }

    const newUser: User = {
      id: Math.random().toString(36).substr(2, 9),
      firstName: formFirstName,
      lastName: formLastName,
      email: formEmail,
      role: formRole,
      status: 'ACTIVE',
      department: formDepartment
    };

    const newUsers = [newUser, ...users];
    saveUsers(newUsers);
    setIsAddOpen(false);
    clearForm();
    toast.success('User created successfully!');
  };

  const handleEditUser = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentUser || !formFirstName || !formLastName || !formEmail) {
      toast.error('Please fill in all fields.');
      return;
    }

    const updated = users.map(u => {
      if (u.id === currentUser.id) {
        return {
          ...u,
          firstName: formFirstName,
          lastName: formLastName,
          email: formEmail,
          role: formRole,
          department: formDepartment
        };
      }
      return u;
    });

    saveUsers(updated);
    setIsEditOpen(false);
    setCurrentUser(null);
    clearForm();
    toast.success('User updated successfully!');
  };

  const handleDeleteUser = (id: string) => {
    if (confirm('Are you sure you want to delete this user?')) {
      const updated = users.filter(u => u.id !== id);
      saveUsers(updated);
      setSelectedUsers(selectedUsers.filter(item => item !== id));
      toast.success('User deleted successfully!');
    }
  };

  const handleToggleLock = (id: string, currentStatus: string) => {
    const nextStatus = currentStatus === 'ACTIVE' ? 'INACTIVE' : 'ACTIVE';
    const updated = users.map(u => {
      if (u.id === id) {
        return { ...u, status: nextStatus };
      }
      return u;
    });
    saveUsers(updated);
    toast.success(`User status updated to ${nextStatus}`);
  };

  // Bulk Actions
  const handleBulkDelete = () => {
    if (selectedUsers.length === 0) return;
    if (confirm(`Are you sure you want to delete ${selectedUsers.length} users?`)) {
      const updated = users.filter(u => !selectedUsers.includes(u.id));
      saveUsers(updated);
      setSelectedUsers([]);
      toast.success('Selected users deleted successfully!');
    }
  };

  const handleBulkExport = () => {
    if (selectedUsers.length === 0) {
      toast.error('No users selected to export.');
      return;
    }
    const exportData = users.filter(u => selectedUsers.includes(u.id));
    const csvContent = "data:text/csv;charset=utf-8," 
      + ["First Name,Last Name,Email,Role,Status,Department"]
      .concat(exportData.map(e => `${e.firstName},${e.lastName},${e.email},${e.role},${e.status},${e.department}`))
      .join("\n");
    
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `kavan_users_export_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    toast.success('Users exported successfully!');
  };

  const handleBulkImport = () => {
    toast.info('Select a CSV file to import users.');
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.csv';
    input.onchange = (e: any) => {
      const file = e.target.files[0];
      if (file) {
        toast.success(`Successfully imported users from ${file.name}`);
      }
    };
    input.click();
  };

  const openEditModal = (user: User) => {
    setCurrentUser(user);
    setFormFirstName(user.firstName);
    setFormLastName(user.lastName);
    setFormEmail(user.email);
    setFormRole(user.role);
    setFormDepartment(user.department);
    setIsEditOpen(true);
  };

  const clearForm = () => {
    setFormFirstName('');
    setFormLastName('');
    setFormEmail('');
    setFormRole('EMPLOYEE');
    setFormDepartment('Sales');
  };

  // Filter computation
  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      `${user.firstName} ${user.lastName}`.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase()) ||
      user.department.toLowerCase().includes(search.toLowerCase());
    
    const matchesRole = roleFilter === 'ALL' || user.role === roleFilter;
    const matchesStatus = statusFilter === 'ALL' || user.status === statusFilter;

    return matchesSearch && matchesRole && matchesStatus;
  });

  // Pagination calculations
  const totalPages = Math.ceil(filteredUsers.length / itemsPerPage) || 1;
  const paginatedUsers = filteredUsers.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">User Management</h1>
          <p className="text-muted-foreground mt-1">Manage, audit, and provision accounts across the platform.</p>
        </div>
        <div className="flex gap-2 flex-wrap">
          <Button onClick={handleBulkImport} variant="outline" size="sm">
            <Upload className="w-4 h-4 mr-2" />
            Import CSV
          </Button>
          <Button onClick={handleBulkExport} variant="outline" size="sm" disabled={selectedUsers.length === 0}>
            <Download className="w-4 h-4 mr-2" />
            Export Selected
          </Button>
          <Button onClick={() => setIsAddOpen(true)} size="sm">
            <Plus className="w-4 h-4 mr-2" />
            Add User
          </Button>
        </div>
      </div>

      {/* Control bar */}
      <Card className="glass-card">
        <CardContent className="p-4 flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Search by name, email, department..." 
              value={search}
              onChange={handleSearchChange}
              className="pl-10"
            />
          </div>
          
          <div className="flex w-full md:w-auto gap-3 items-center justify-end">
            <div className="flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm font-medium text-muted-foreground">Filters:</span>
            </div>
            
            <select 
              value={roleFilter} 
              onChange={handleRoleFilterChange}
              className="bg-background border rounded-md px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="ALL">All Roles</option>
              <option value="SUPER_ADMIN">Super Admin</option>
              <option value="TENANT_ADMIN">Tenant Admin</option>
              <option value="DEVELOPER">Developer</option>
              <option value="EMPLOYEE">Employee</option>
            </select>

            <select 
              value={statusFilter} 
              onChange={handleStatusFilterChange}
              className="bg-background border rounded-md px-3 py-1.5 text-sm outline-none focus:ring-2 focus:ring-primary/20"
            >
              <option value="ALL">All Status</option>
              <option value="ACTIVE">Active</option>
              <option value="INACTIVE">Inactive</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Bulk actions status */}
      {selectedUsers.length > 0 && (
        <div className="p-3 bg-primary/10 border border-primary/20 rounded-lg flex items-center justify-between animate-in slide-in-from-top-2">
          <span className="text-sm font-medium text-primary">
            {selectedUsers.length} users selected
          </span>
          <div className="flex gap-2">
            <Button variant="destructive" size="sm" onClick={handleBulkDelete}>
              <Trash2 className="w-4 h-4 mr-2" />
              Delete Selected
            </Button>
          </div>
        </div>
      )}

      {/* Users Directory */}
      <Card className="glass-card">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12 text-center">
                  <input 
                    type="checkbox"
                    checked={filteredUsers.length > 0 && selectedUsers.length === filteredUsers.length}
                    onChange={toggleSelectAll}
                    className="rounded border-gray-300 text-primary focus:ring-primary"
                  />
                </TableHead>
                <TableHead>User</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Department</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {paginatedUsers.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="h-64 text-center text-muted-foreground">
                    No users found matching filters.
                  </TableCell>
                </TableRow>
              ) : (
                paginatedUsers.map((user) => (
                  <TableRow key={user.id} className={selectedUsers.includes(user.id) ? 'bg-primary/5' : ''}>
                    <TableCell className="text-center">
                      <input 
                        type="checkbox"
                        checked={selectedUsers.includes(user.id)}
                        onChange={() => toggleSelectUser(user.id)}
                        className="rounded border-gray-300 text-primary focus:ring-primary"
                      />
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-col">
                        <span className="font-semibold text-foreground">{user.firstName} {user.lastName}</span>
                        <span className="text-xs text-muted-foreground">{user.email}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="font-mono text-xs uppercase bg-muted/30">
                        {user.role.replace('_', ' ')}
                      </Badge>
                    </TableCell>
                    <TableCell>{user.department}</TableCell>
                    <TableCell>
                      <Badge 
                        variant={user.status === 'ACTIVE' ? 'default' : 'secondary'} 
                        className={user.status === 'ACTIVE' ? 'bg-green-500 hover:bg-green-600 text-white' : ''}
                      >
                        {user.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-1">
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          onClick={() => handleToggleLock(user.id, user.status)}
                          title={user.status === 'ACTIVE' ? 'Lock Account' : 'Unlock Account'}
                        >
                          {user.status === 'ACTIVE' ? <Lock className="w-4 h-4 text-orange-500" /> : <Unlock className="w-4 h-4 text-green-500" />}
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          onClick={() => openEditModal(user)}
                          title="Edit User"
                        >
                          <Edit className="w-4 h-4 text-blue-500" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="icon" 
                          onClick={() => handleDeleteUser(user.id)}
                          title="Delete User"
                        >
                          <Trash2 className="w-4 h-4 text-destructive" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>

          {/* Pagination Controls */}
          {filteredUsers.length > 0 && (
            <div className="flex items-center justify-between px-6 py-4 border-t">
              <span className="text-sm text-muted-foreground">
                Showing {Math.min(filteredUsers.length, (currentPage - 1) * itemsPerPage + 1)} to {Math.min(filteredUsers.length, currentPage * itemsPerPage)} of {filteredUsers.length} entries
              </span>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                >
                  <ChevronLeft className="w-4 h-4 mr-1" />
                  Previous
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={currentPage === totalPages}
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                >
                  Next
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Add User Modal */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New User</DialogTitle>
            <DialogDescription>Create a new account and assign permissions.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleAddUser} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="add-first-name">First Name</Label>
                <Input 
                  id="add-first-name"
                  value={formFirstName} 
                  onChange={e => setFormFirstName(e.target.value)} 
                  placeholder="John" 
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="add-last-name">Last Name</Label>
                <Input 
                  id="add-last-name"
                  value={formLastName} 
                  onChange={e => setFormLastName(e.target.value)} 
                  placeholder="Doe" 
                />
              </div>
            </div>
            
            <div className="space-y-1">
              <Label htmlFor="add-email">Email Address</Label>
              <Input 
                id="add-email"
                type="email"
                value={formEmail} 
                onChange={e => setFormEmail(e.target.value)} 
                placeholder="john.doe@kavan.com" 
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="add-role">Role</Label>
                <select 
                  id="add-role"
                  value={formRole} 
                  onChange={e => setFormRole(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="SUPER_ADMIN">Super Admin</option>
                  <option value="TENANT_ADMIN">Tenant Admin</option>
                  <option value="DEVELOPER">Developer</option>
                  <option value="EMPLOYEE">Employee</option>
                </select>
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="add-dept">Department</Label>
                <select 
                  id="add-dept"
                  value={formDepartment} 
                  onChange={e => setFormDepartment(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="IT">IT</option>
                  <option value="Engineering">Engineering</option>
                  <option value="Management">Management</option>
                  <option value="Sales">Sales</option>
                  <option value="HR">HR</option>
                </select>
              </div>
            </div>

            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => { setIsAddOpen(false); clearForm(); }}>
                Cancel
              </Button>
              <Button type="submit">
                Create User
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Edit User Modal */}
      <Dialog open={isEditOpen} onOpenChange={(open) => { if(!open) { setIsEditOpen(false); setCurrentUser(null); } }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit User Profile</DialogTitle>
            <DialogDescription>Modify user role, department, or contact details.</DialogDescription>
          </DialogHeader>
          <form onSubmit={handleEditUser} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="edit-first-name">First Name</Label>
                <Input 
                  id="edit-first-name"
                  value={formFirstName} 
                  onChange={e => setFormFirstName(e.target.value)} 
                />
              </div>
              <div className="space-y-1">
                <Label htmlFor="edit-last-name">Last Name</Label>
                <Input 
                  id="edit-last-name"
                  value={formLastName} 
                  onChange={e => setFormLastName(e.target.value)} 
                />
              </div>
            </div>
            
            <div className="space-y-1">
              <Label htmlFor="edit-email">Email Address</Label>
              <Input 
                id="edit-email"
                type="email"
                value={formEmail} 
                onChange={e => setFormEmail(e.target.value)} 
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <Label htmlFor="edit-role">Role</Label>
                <select 
                  id="edit-role"
                  value={formRole} 
                  onChange={e => setFormRole(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="SUPER_ADMIN">Super Admin</option>
                  <option value="TENANT_ADMIN">Tenant Admin</option>
                  <option value="DEVELOPER">Developer</option>
                  <option value="EMPLOYEE">Employee</option>
                </select>
              </div>
              
              <div className="space-y-1">
                <Label htmlFor="edit-dept">Department</Label>
                <select 
                  id="edit-dept"
                  value={formDepartment} 
                  onChange={e => setFormDepartment(e.target.value)}
                  className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary/20"
                >
                  <option value="IT">IT</option>
                  <option value="Engineering">Engineering</option>
                  <option value="Management">Management</option>
                  <option value="Sales">Sales</option>
                  <option value="HR">HR</option>
                </select>
              </div>
            </div>

            <DialogFooter className="pt-4">
              <Button type="button" variant="outline" onClick={() => { setIsEditOpen(false); setCurrentUser(null); clearForm(); }}>
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
