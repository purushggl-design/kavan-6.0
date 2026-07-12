import React from 'react';
import { useAppDispatch, useAppSelector } from '@/hooks/redux';
import { selectCurrentRole } from '@/store/authSlice';
import type { PlatformRole } from '@/types/auth';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useNavigate } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';

const rolePermissions: Record<string, string[]> = {
  SUPER_ADMIN: ['*'],
  TENANT_ADMIN: ['users.read', 'users.write', 'billing.manage', 'tenant.settings'],
  SECURITY_ANALYST: ['security.read', 'security.write', 'audit.logs'],
  DEVELOPER: ['api.read', 'deployments.manage', 'logs.read'],
  EMPLOYEE: ['dashboard.view', 'profile.edit'],
  MANAGER: ['dashboard.view', 'profile.edit', 'team.manage', 'approvals.write'],
};

export function RoleSwitcher() {
  const dispatch = useAppDispatch();
  const currentRole = useAppSelector(selectCurrentRole);
  const navigate = useNavigate();

  const handleRoleChange = (role: PlatformRole) => {
    toast.error('Role switching is disabled in the real backend environment.');
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" className="border-dashed border-primary/50 hover:border-primary bg-primary/5">
          <span className="mr-2 text-xs">DEV:</span>
          <Badge variant="secondary" className="bg-primary/20 hover:bg-primary/30">
            {currentRole?.replace('_', ' ')}
          </Badge>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel>Switch Role (Dev Only)</DropdownMenuLabel>
        <DropdownMenuSeparator />
        {(Object.keys(rolePermissions) as PlatformRole[]).map((role) => (
          <DropdownMenuItem 
            key={role} 
            onClick={() => handleRoleChange(role)}
            className="cursor-pointer"
          >
            <span className={currentRole === role ? 'font-bold text-primary' : ''}>
              {role.replace('_', ' ')}
            </span>
            {currentRole === role && <Badge className="ml-auto w-2 h-2 p-0 rounded-full bg-primary" />}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
