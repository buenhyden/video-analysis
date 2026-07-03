import React from 'react';
import { Play, Lock, LogOut, Plus } from 'lucide-react';
import { useStore } from '../../store/useStore';
import Button from '../ui/Button';

const Navbar = ({ onOpenLogin, onOpenUpload }) =>
{
    const { isAuthenticated, user, logout } = useStore();

    return (
        <nav className="sticky top-0 z-40 w-full backdrop-blur-xl border-b border-slate-800/60 bg-slate-950/80">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <Play fill="white" size={14} className="ml-0.5 text-white" />
                        </div>
                        <span className="font-bold text-xl tracking-tight text-white">Portfolio.io</span>
                    </div>

                    <div className="flex items-center gap-4">
                        {isAuthenticated ? (
                            <div className="flex items-center gap-4">
                                <span className="hidden sm:block text-sm text-slate-400">
                                    Welcome, <span className="text-indigo-400 font-semibold">{user?.username}</span>
                                </span>
                                <Button variant="primary" onClick={onOpenUpload} className="text-sm py-1.5 px-3">
                                    <Plus size={16} /> <span className="hidden sm:inline">New Project</span>
                                </Button>
                                <Button variant="secondary" onClick={logout} className="text-sm py-1.5 px-3">
                                    <LogOut size={16} />
                                </Button>
                            </div>
                        ) : (
                            <button
                                onClick={onOpenLogin}
                                className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors"
                            >
                                <Lock size={14} /> Admin
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;