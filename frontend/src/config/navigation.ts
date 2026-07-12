import { 
  LayoutDashboard, 
  Building2, 
  Users, 
  Shield, 
  FileText, 
  BarChart3, 
  Activity, 
  CreditCard, 
  Link, 
  Bell, 
  Settings, 
  Database, 
  Bot, 
  User, 
  CheckSquare, 
  Calendar,
  Lock,
  GitBranch,
  FolderKanban,
  Tv,
  ListTodo,
  Terminal,
  Server,
  Globe,
  Cpu
} from 'lucide-react';

export interface NavItem {
  title: string;
  href: string;
  icon: React.ElementType;
}

export interface NavGroup {
  group: string;
  items: NavItem[];
}

export const superAdminNavigation: NavGroup[] = [
  {
    group: 'Main Control',
    items: [
      { title: 'Dashboard', href: '/platform/dashboard', icon: LayoutDashboard },
      { title: 'Tenants', href: '/super-admin/tenants', icon: Building2 },
      { title: 'Users', href: '/users', icon: Users },
      { title: 'Roles & Permissions', href: '/super-admin/roles', icon: Shield },
      { title: 'Employees', href: '/employees', icon: Users },
    ]
  },
  {
    group: 'Analytics & Security',
    items: [
      { title: 'Analytics', href: '/super-admin/analytics', icon: BarChart3 },
      { title: 'System Monitoring', href: '/super-admin/system-monitoring', icon: Cpu },
      { title: 'Audit Logs', href: '/super-admin/audit-logs', icon: Activity },
      { title: 'Security Center', href: '/security', icon: Shield },
    ]
  },
  {
    group: 'Billing & Provisioning',
    items: [
      { title: 'Subscriptions', href: '/super-admin/subscriptions', icon: CreditCard },
      { title: 'Licenses', href: '/super-admin/licenses', icon: Lock },
      { title: 'Integrations', href: '/integrations', icon: Link },
      { title: 'Notifications', href: '/notifications', icon: Bell },
    ]
  },
  {
    group: 'Global Settings',
    items: [
      { title: 'Global Settings', href: '/super-admin/settings', icon: Settings },
      { title: 'Feature Toggles', href: '/super-admin/feature-toggles', icon: Tv },
      { title: 'Maintenance Mode', href: '/super-admin/maintenance', icon: Lock },
      { title: 'Database Monitor', href: '/super-admin/database-monitor', icon: Database },
      { title: 'AI Assistant', href: '/super-admin/ai-assistant', icon: Bot },
      { title: 'Profile', href: '/profile', icon: User },
    ]
  }
];

export const tenantAdminNavigation: NavGroup[] = [
  {
    group: 'Organization Management',
    items: [
      { title: 'Dashboard', href: '/dashboard/tenant-admin', icon: LayoutDashboard },
      { title: 'Organization', href: '/organizations', icon: Building2 },
      { title: 'Employees', href: '/employees', icon: Users },
    ]
  },
  {
    group: 'Workflows',
    items: [
      { title: 'My Apps', href: '/my-apps', icon: Server },
      { title: 'Reports', href: '/reports', icon: FileText },
    ]
  },
  {
    group: 'Settings & Identity',
    items: [
      { title: 'Notifications', href: '/notifications', icon: Bell },
      { title: 'Integrations', href: '/integrations', icon: Link },
      { title: 'Security', href: '/security', icon: Shield },
      { title: 'Settings', href: '/settings', icon: Settings },
      { title: 'Profile', href: '/profile', icon: User },
    ]
  }
];

export const managerNavigation: NavGroup[] = [
  {
    group: 'Manager Console',
    items: [
      { title: 'Dashboard', href: '/manager/dashboard', icon: LayoutDashboard },
      { title: 'My Team', href: '/manager/team', icon: Users },
      { title: 'Reports', href: '/manager/reports', icon: FileText },
      { title: 'Notifications', href: '/manager/notifications', icon: Bell },
      { title: 'Profile', href: '/manager/profile', icon: User },
      { title: 'Settings', href: '/manager/settings', icon: Settings },
    ]
  }
];

export const employeeNavigation: NavGroup[] = [
  {
    group: 'Self Service',
    items: [
      { title: 'Dashboard', href: '/dashboard/employee', icon: LayoutDashboard },
      { title: 'My Profile', href: '/profile', icon: User },
      { title: 'Notifications', href: '/notifications', icon: Bell },
      { title: 'Settings', href: '/profile?tab=preferences', icon: Settings },
    ]
  }
];

export const developerNavigation: NavGroup[] = [
  {
    group: 'Developer Console',
    items: [
      { title: 'Developer Dashboard', href: '/developer/dashboard', icon: LayoutDashboard },
      { title: 'API Keys', href: '/developer/api-keys', icon: Lock },
      { title: 'Integrations', href: '/integrations', icon: Link },
      { title: 'Webhooks', href: '/developer/webhooks', icon: Link },
      { title: 'Logs', href: '/super-admin/audit-logs', icon: Terminal },
      { title: 'Deployments', href: '/developer/deployments', icon: Server },
      { title: 'Monitoring', href: '/developer/monitoring', icon: BarChart3 },
      { title: 'Developer Settings', href: '/settings', icon: Settings },
    ]
  }
];

export const securityAdminNavigation: NavGroup[] = [
  {
    group: 'SOC Control',
    items: [
      { title: 'Security Dashboard', href: '/security/dashboard', icon: LayoutDashboard },
      { title: 'Audit Logs', href: '/security/audit-logs', icon: Activity },
      { title: 'Threat Monitoring', href: '/security/threats', icon: Shield },
      { title: 'MFA Policies', href: '/security/mfa', icon: Lock },
      { title: 'Sessions', href: '/security/sessions', icon: Calendar },
      { title: 'IP Management', href: '/security/ip-management', icon: Database },
      { title: 'Permissions', href: '/security/permissions', icon: Shield },
      { title: 'Compliance Reports', href: '/security/compliance', icon: FileText },
    ]
  }
];

// Helper placeholders
const ClockIconPlaceholder = Calendar;
const DollarIconPlaceholder = CreditCard;
const KeyIconPlaceholder = Lock;
const ShieldAlertPlaceholder = Shield;
