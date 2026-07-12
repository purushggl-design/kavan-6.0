import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { useAppSelector } from '@/hooks/redux';
import { selectCurrentRole } from '@/store/authSlice';
import { cn } from '@/lib/utils';
import { KavanLogo } from '@/components/ui/KavanLogo';
import { 
  superAdminNavigation,
  tenantAdminNavigation,
  managerNavigation,
  employeeNavigation,
  developerNavigation,
  securityAdminNavigation
} from '@/config/navigation';

export function Sidebar() {
  const currentRole = useAppSelector(selectCurrentRole);
  const location = useLocation();

  const getNavigation = () => {
    switch (currentRole) {
      case 'SUPER_ADMIN':
        return superAdminNavigation;
      case 'TENANT_ADMIN':
        return tenantAdminNavigation;
      case 'MANAGER':
        return managerNavigation;
      case 'EMPLOYEE':
        return employeeNavigation;
      case 'DEVELOPER':
        return developerNavigation;
      case 'SECURITY_ANALYST':
        return securityAdminNavigation;
      default:
        return [];
    }
  };

  const navigationConfig = getNavigation();

  // Dynamic accent style per role
  const getRoleStyle = () => {
    switch (currentRole) {
      case 'SUPER_ADMIN':
        return {
          logoBg: 'bg-red-500',
          activeLink: 'bg-red-500/10 text-red-500',
          border: 'border-red-500/20'
        };
      case 'TENANT_ADMIN':
        return {
          logoBg: 'bg-purple-500',
          activeLink: 'bg-purple-500/10 text-purple-500',
          border: 'border-purple-500/20'
        };
      case 'MANAGER':
        return {
          logoBg: 'bg-green-500',
          activeLink: 'bg-green-500/10 text-green-500',
          border: 'border-green-500/20'
        };
      case 'DEVELOPER':
        return {
          logoBg: 'bg-amber-500',
          activeLink: 'bg-amber-500/10 text-amber-500',
          border: 'border-amber-500/20'
        };
      case 'SECURITY_ANALYST':
        return {
          logoBg: 'bg-rose-500',
          activeLink: 'bg-rose-500/10 text-rose-500',
          border: 'border-rose-500/20'
        };
      case 'EMPLOYEE':
      default:
        return {
          logoBg: 'bg-primary',
          activeLink: 'bg-primary/10 text-primary',
          border: 'border-primary/20'
        };
    }
  };

  const roleStyle = getRoleStyle();

  return (
    <div className={cn("w-64 h-screen bg-card border-r flex flex-col sticky top-0 animate-in slide-in-from-left-4 duration-500", roleStyle.border)}>
      <div className="p-6 border-b">
        <KavanLogo size="md" showText={true} textClassName="text-foreground" />
        <span className="text-[10px] text-muted-foreground uppercase font-mono tracking-wider ml-[42px] -mt-1.5 block">
          {currentRole?.replace('_', ' ') || 'Guest'}
        </span>
      </div>

      <div className="flex-1 overflow-y-auto py-6 px-3 space-y-6">
        {navigationConfig.map((group, i) => (
          <div key={i}>
            <h4 className="px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
              {group.group}
            </h4>
            <div className="space-y-1">
              {group.items.map((item, j) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href || location.pathname.startsWith(item.href + '?') || location.pathname.startsWith(item.href + '/');
                return (
                  <NavLink
                    key={j}
                    to={item.href}
                    className={cn(
                      "flex items-center gap-3 px-4 py-2 rounded-md transition-all text-sm font-medium",
                      isActive 
                        ? roleStyle.activeLink
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    {item.title}
                  </NavLink>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default Sidebar;
