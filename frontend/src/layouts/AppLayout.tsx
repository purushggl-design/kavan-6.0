import React, { useState, useEffect } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Breadcrumbs } from './Breadcrumbs';
import { RoleSwitcher } from './RoleSwitcher';
import { useAppSelector, useAppDispatch } from '@/hooks/redux';
import { selectCurrentUser, logout } from '@/store/authSlice';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  LogOut, 
  Bot, 
  Send, 
  X, 
  Terminal, 
  Search,
  Sparkles,
  Command,
  User as UserIcon
} from 'lucide-react';
import { toast } from 'sonner';

export const AppLayout: React.FC = () => {
  const user = useAppSelector(selectCurrentUser);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleLogout = async () => {
    dispatch(logout());
  };

  // AI Assistant Chat Panel
  const [isAiOpen, setIsAiOpen] = useState(false);
  const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([
    { sender: 'bot', text: 'Hello! I am your KAVAN AI Workspace Assistant. How can I help you manage your teams or reports today?' }
  ]);
  const [inputVal, setInputVal] = useState('');

  // Command Palette
  const [isCmdOpen, setIsCmdOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsCmdOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;

    const userMsg = inputVal;
    setMessages(prev => [...prev, { sender: 'user', text: userMsg }]);
    setInputVal('');

    // Mock response
    setTimeout(() => {
      let reply = "I'm analyzing your request. You can access reports in the Report Generator, or manage workspace items via User Settings.";
      if (userMsg.toLowerCase().includes('report')) {
        reply = "To create a report, click 'Reports Center' on the sidebar. Choose your filters and click 'Generate Visualization' then export as PDF/Excel.";
      } else if (userMsg.toLowerCase().includes('user')) {
        reply = "You can add, edit, or delete members in 'User Management' on the sidebar, where you can also cycle account locking status.";
      }
      setMessages(prev => [...prev, { sender: 'bot', text: reply }]);
    }, 800);
  };

  const handleCommandRun = (route: string) => {
    navigate(route);
    setIsCmdOpen(false);
    toast.success(`Navigated to ${route}`);
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden">
      <Sidebar />
      
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <header className="h-16 border-b bg-card/50 backdrop-blur-md flex items-center justify-between px-6 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <Breadcrumbs />

            <Button 
              variant="outline" 
              size="sm" 
              className="text-xs text-muted-foreground hidden md:flex items-center gap-1.5 px-3 py-1.5"
              onClick={() => setIsCmdOpen(true)}
            >
              <Search className="w-3.5 h-3.5 mr-1" />
              Search workspace...
              <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100 ml-2">
                <span className="text-xs">Ctrl+</span>K
              </kbd>
            </Button>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Dev tool only */}
            {import.meta.env.DEV && <RoleSwitcher />}
            
            <div className="flex items-center gap-3 pl-4 border-l">
              <div className="flex flex-col items-end">
                <span className="text-sm font-medium">{user?.first_name} {user?.last_name}</span>
                <span className="text-xs text-muted-foreground">{user?.platform_role?.replace('_', ' ')}</span>
              </div>
              <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                {user?.first_name?.[0]}{user?.last_name?.[0]}
              </div>
              <Button variant="ghost" size="icon" onClick={handleLogout} title="Logout">
                <LogOut className="w-4 h-4 text-muted-foreground" />
              </Button>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6 relative">
          <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-primary/5 -z-10" />
          <div className="max-w-7xl mx-auto space-y-6">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Floating AI Trigger Button */}
      <div className="fixed bottom-6 right-6 z-40">
        <Button 
          onClick={() => setIsAiOpen(true)} 
          className="rounded-full w-14 h-14 bg-primary text-primary-foreground shadow-2xl flex items-center justify-center hover:scale-105 transition-transform"
        >
          <Bot className="w-6 h-6" />
        </Button>
      </div>

      {/* AI Panel Drawer */}
      {isAiOpen && (
        <div className="fixed inset-y-0 right-0 w-96 bg-card border-l shadow-2xl z-50 flex flex-col animate-in slide-in-from-right duration-300">
          <div className="p-4 border-b flex justify-between items-center bg-muted/40">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              <span className="font-semibold">KAVAN Workspace AI</span>
            </div>
            <Button variant="ghost" size="icon" onClick={() => setIsAiOpen(false)}>
              <X className="w-4 h-4" />
            </Button>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`p-3 rounded-2xl max-w-[80%] text-sm ${
                  m.sender === 'user' 
                    ? 'bg-primary text-primary-foreground rounded-tr-none' 
                    : 'bg-muted text-foreground rounded-tl-none border'
                }`}>
                  {m.text}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSendMessage} className="p-4 border-t flex gap-2">
            <Input 
              value={inputVal}
              onChange={e => setInputVal(e.target.value)}
              placeholder="Ask KAVAN AI..."
              className="flex-1"
            />
            <Button type="submit" size="icon">
              <Send className="w-4 h-4" />
            </Button>
          </form>
        </div>
      )}

      {/* Global Cmd+K Search Palette Modal */}
      {isCmdOpen && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-start justify-center pt-24">
          <div className="bg-card w-full max-w-lg border rounded-xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-4 border-b flex items-center gap-2">
              <Command className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm font-semibold text-muted-foreground">KAVAN Command Search</span>
            </div>
            
            <div className="p-2 space-y-1">
              {[
                { title: 'Go to Dashboard', path: '/dashboard' },
                { title: 'Manage Users', path: '/users' },
                { title: 'Manage Organizations', path: '/organizations' },
                { title: 'Manage Employees', path: '/employees' },
                { title: 'Reports Analytics', path: '/reports' },
                { title: 'Security Audits', path: '/security' },
                { title: 'Integration Status', path: '/integrations' },
                { title: 'Notification Alerts', path: '/notifications' }
              ].map(cmd => (
                <button
                  key={cmd.path}
                  onClick={() => handleCommandRun(cmd.path)}
                  className="w-full text-left px-4 py-3 text-sm rounded-lg hover:bg-muted font-medium transition-colors flex justify-between"
                >
                  <span>{cmd.title}</span>
                  <span className="text-xs text-muted-foreground">{cmd.path}</span>
                </button>
              ))}
            </div>
            
            <div className="p-3 border-t bg-muted/30 text-center">
              <Button size="sm" variant="ghost" onClick={() => setIsCmdOpen(false)}>Close Command Search</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
