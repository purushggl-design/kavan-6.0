import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAppSelector } from '@/hooks/redux';
import { selectCurrentUser } from '@/store/authSlice';
import { 
  User, 
  Lock, 
  Settings, 
  Upload, 
  Check, 
  Languages, 
  SunMoon,
  Save
} from 'lucide-react';
import { toast } from 'sonner';
import { KavanLogo } from '@/components/ui/KavanLogo';

export const ProfileSettings: React.FC = () => {
  const user = useAppSelector(selectCurrentUser);
  const [activeTab, setActiveTab] = useState<'profile' | 'password' | 'preferences'>('profile');

  // Profile Form State
  const [firstName, setFirstName] = useState(user?.first_name || 'John');
  const [lastName, setLastName] = useState(user?.last_name || 'Doe');
  const [email, setEmail] = useState(user?.email || 'employee@kavan.com');

  // Password Form State
  const [currPass, setCurrPass] = useState('');
  const [newPass, setNewPass] = useState('');
  const [confirmPass, setConfirmPass] = useState('');

  // Preference states
  const [theme, setTheme] = useState('dark');
  const [lang, setLang] = useState('English');

  const [isLoading, setIsLoading] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      toast.success('Profile details updated successfully (Demo Mode)!');
      setIsLoading(false);
    }, 500);
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currPass || !newPass || !confirmPass) {
      toast.error('All password fields are required.');
      return;
    }
    if (newPass !== confirmPass) {
      toast.error('Passwords do not match.');
      return;
    }
    
    setIsLoading(true);
    setTimeout(() => {
      toast.success('Your security password has been changed (Demo Mode).');
      setCurrPass('');
      setNewPass('');
      setConfirmPass('');
      setIsLoading(false);
    }, 500);
  };

  const handleToggleMfa = async (enabled: boolean) => {
    setIsLoading(true);
    setTimeout(() => {
      toast.success(`MFA ${enabled ? 'enabled' : 'disabled'} successfully (Demo Mode).`);
      setIsLoading(false);
    }, 500);
  };

  const handleAvatarUpload = () => {
    toast.success('Avatar image uploaded successfully.');
  };

  const handleSavePreferences = () => {
    // Theme switching hook logic
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    toast.success(`Preferences updated. Theme: ${theme}, Language: ${lang}`);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Profile & Preferences</h1>
        <p className="text-muted-foreground mt-1">Configure your personal credentials, password rules, and client display preferences.</p>
      </div>

      <div className="flex border-b">
        {[
          { id: 'profile', label: 'My Profile', icon: User },
          { id: 'password', label: 'Security Password', icon: Lock },
          { id: 'preferences', label: 'Display Preferences', icon: SunMoon },
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

      {activeTab === 'profile' && (
        <div className="grid gap-6 md:grid-cols-3">
          <Card className="glass-card md:col-span-2">
            <CardHeader>
              <CardTitle>Personal Details</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleUpdateProfile} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <Label htmlFor="prof-first">First Name</Label>
                    <Input 
                      id="prof-first"
                      value={firstName} 
                      onChange={e => setFirstName(e.target.value)} 
                    />
                  </div>
                  <div className="space-y-1">
                    <Label htmlFor="prof-last">Last Name</Label>
                    <Input 
                      id="prof-last"
                      value={lastName} 
                      onChange={e => setLastName(e.target.value)} 
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <Label htmlFor="prof-email">Email Address</Label>
                  <Input 
                    id="prof-email"
                    type="email"
                    value={email} 
                    onChange={e => setEmail(e.target.value)} 
                  />
                </div>

                <Button type="submit">
                  <Save className="w-4 h-4 mr-2" />
                  Save Profile Details
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card className="glass-card md:col-span-1 overflow-hidden relative border-primary/20">
            {/* Ambient background glow */}
            <div className="absolute -right-16 -top-16 w-32 h-32 bg-primary/10 rounded-full blur-2xl" />
            <div className="absolute -left-16 -bottom-16 w-32 h-32 bg-[#ef4444]/10 rounded-full blur-2xl" />
            
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">KAVAN Enterprise Profile Card</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col items-center relative z-10 pt-4">
              {/* Branded Avatar container with red gradient border */}
              <div className="relative mb-4 group cursor-pointer" onClick={handleAvatarUpload}>
                <div className="absolute inset-0 bg-gradient-to-tr from-[#ef4444] to-[#b91c1c] rounded-full animate-pulse opacity-50 blur-sm group-hover:opacity-75 transition-opacity" />
                <div className="w-24 h-24 rounded-full p-1 bg-gradient-to-tr from-[#ef4444] to-[#b91c1c] relative z-10">
                  <div className="w-full h-full rounded-full bg-card flex items-center justify-center text-foreground font-bold text-3xl border border-background shadow-inner">
                    {firstName?.[0]}{lastName?.[0]}
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-1.5 mb-1 mt-2">
                <KavanLogo size={16} />
                <span className="font-extrabold text-lg tracking-tight">{firstName} {lastName}</span>
              </div>
              
              <p className="text-xs font-mono bg-primary/10 text-primary border border-primary/20 px-2 py-0.5 rounded-full uppercase tracking-wider mb-4">
                {user?.platform_role?.replace('_', ' ') || 'EMPLOYEE'}
              </p>
              
              <p className="text-[10px] text-muted-foreground text-center mb-6 max-w-[180px]">
                Authorized user on the KAVAN Enterprise Ecosystem.
              </p>

              <Button variant="outline" size="sm" onClick={handleAvatarUpload} className="w-full">
                <Upload className="w-4 h-4 mr-2" />
                Upload New Photo
              </Button>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'password' && (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Change Password</CardTitle>
            <CardDescription>Keep your account secure by cycling passwords regularly.</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleChangePassword} className="space-y-4 max-w-md">
              <div className="space-y-1">
                <Label htmlFor="curr-pass">Current Password</Label>
                <Input 
                  id="curr-pass"
                  type="password"
                  value={currPass} 
                  onChange={e => setCurrPass(e.target.value)} 
                />
              </div>

              <div className="space-y-1">
                <Label htmlFor="new-pass">New Password</Label>
                <Input 
                  id="new-pass"
                  type="password"
                  value={newPass} 
                  onChange={e => setNewPass(e.target.value)} 
                />
              </div>

              <div className="space-y-1">
                <Label htmlFor="confirm-pass">Confirm New Password</Label>
                <Input 
                  id="confirm-pass"
                  type="password"
                  value={confirmPass} 
                  onChange={e => setConfirmPass(e.target.value)} 
                />
              </div>

              <Button type="submit">
                <Check className="w-4 h-4 mr-2" />
                Change Password
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {activeTab === 'preferences' && (
        <Card className="glass-card">
          <CardHeader>
            <CardTitle>Workspace Themes & Languages</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 max-w-md">
            <div className="space-y-1">
              <Label>Theme Setting</Label>
              <select 
                value={theme}
                onChange={e => setTheme(e.target.value)}
                className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none"
              >
                <option value="light">Light Theme Mode</option>
                <option value="dark">Dark Theme Mode</option>
              </select>
            </div>

            <div className="space-y-1">
              <Label>Language Selection</Label>
              <select 
                value={lang}
                onChange={e => setLang(e.target.value)}
                className="w-full bg-background border rounded-md px-3 py-2 text-sm outline-none"
              >
                <option value="English">English (US)</option>
                <option value="Spanish">Spanish (ES)</option>
                <option value="French">French (FR)</option>
              </select>
            </div>

            <Button onClick={handleSavePreferences}>
              <Save className="w-4 h-4 mr-2" />
              Save Preferences
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
