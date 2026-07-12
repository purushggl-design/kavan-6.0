import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Check, X } from 'lucide-react';

type Role = 'SUPER_ADMIN' | 'TENANT_ADMIN' | 'SECURITY_ANALYST' | 'DEVELOPER' | 'EMPLOYEE' | 'MANAGER';

const allPermissions = [
  'users.read', 'users.write', 'users.delete',
  'billing.manage', 'billing.read',
  'tenant.settings', 'tenant.create',
  'security.read', 'security.write',
  'audit.logs', 'api.read', 'deployments.manage',
  'dashboard.view', 'profile.edit'
];

const roleMatrix: Record<Role, string[]> = {
  SUPER_ADMIN: ['*'], // Has all effectively
  TENANT_ADMIN: ['users.read', 'users.write', 'billing.manage', 'billing.read', 'tenant.settings', 'dashboard.view', 'profile.edit'],
  SECURITY_ANALYST: ['security.read', 'security.write', 'audit.logs', 'users.read', 'dashboard.view', 'profile.edit'],
  DEVELOPER: ['api.read', 'deployments.manage', 'audit.logs', 'dashboard.view', 'profile.edit'],
  EMPLOYEE: ['dashboard.view', 'profile.edit'],
  MANAGER: ['users.read', 'dashboard.view', 'profile.edit'],
};

export const PermissionMatrix: React.FC = () => {
  const roles: Role[] = ['SUPER_ADMIN', 'TENANT_ADMIN', 'SECURITY_ANALYST', 'DEVELOPER', 'EMPLOYEE', 'MANAGER'];

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Permission Matrix</h2>
        <p className="text-muted-foreground mt-1">Global view of access control capabilities per role.</p>
      </div>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle>Role Capabilities</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border/50 bg-background/50 backdrop-blur-sm overflow-hidden">
            <Table>
              <TableHeader className="bg-muted/50">
                <TableRow>
                  <TableHead className="w-[200px] font-bold">Permission</TableHead>
                  {roles.map(role => (
                    <TableHead key={role} className="text-center font-bold">
                      <Badge variant="outline" className="bg-background">
                        {role.replace('_', ' ')}
                      </Badge>
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {allPermissions.map((permission) => (
                  <TableRow key={permission}>
                    <TableCell className="font-medium text-muted-foreground">
                      {permission}
                    </TableCell>
                    {roles.map(role => {
                      const hasPerm = role === 'SUPER_ADMIN' || roleMatrix[role].includes(permission);
                      return (
                        <TableCell key={`${permission}-${role}`} className="text-center">
                          {hasPerm ? (
                            <Check className="w-4 h-4 text-green-500 mx-auto" />
                          ) : (
                            <X className="w-4 h-4 text-muted-foreground/30 mx-auto" />
                          )}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
