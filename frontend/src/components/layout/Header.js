'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../auth/AuthContext';
import { useNavigation } from '../navigation/NavigationContext';
import { Menu, X, User, LogOut, Settings, ChevronDown, Rocket } from 'lucide-react';
import Link from 'next/link';

const Header = ({ onAuthClick, onNavigate }) => {
    const { user, isAuthenticated, logout } = useAuth();
    const { navigateTo } = useNavigation();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

    const navItems = [
        { label: 'Home', action: () => navigateTo('home') },
        { label: 'Features', action: () => navigateTo('features') },
        { label: 'How It Works', action: () => navigateTo('how-it-works') },
        { label: 'Testimonials', action: () => navigateTo('testimonials') },
        { label: 'Contact', action: () => navigateTo('contact') }
    ];

    const handleLogout = () => {
        logout();
        setIsUserMenuOpen(false);
        navigateTo('home');
    };

    const handleNavClick = (action) => {
        action();
        setIsMenuOpen(false);
    };

    return (
        <header className="relative z-50 glass-card mx-4 mt-4 mb-8">
            <div className="container mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <button
                        onClick={() => navigateTo('home')}
                        className="flex items-center gap-3"
                    >
                        <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                            <span className="text-white font-bold text-lg">🚀</span>
                        </div>
                        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                            AI Job Matcher
                        </span>
                    </button>

                    {/* Desktop Navigation */}
                    <nav className="hidden lg:flex items-center gap-8">
                        {navItems.map((item) => (
                            <button
                                key={item.label}
                                onClick={item.action}
                                className="text-gray-600 hover:text-blue-600 font-medium transition-colors duration-200"
                            >
                                {item.label}
                            </button>
                        ))}
                    </nav>

                    {/* Desktop Auth/User Menu */}
                    <div className="hidden lg:flex items-center gap-4">
                        {isAuthenticated ? (
                            <div className="relative">
                                <button
                                    onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                                    className="flex items-center gap-2 bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-xl text-blue-700 hover:from-blue-200 hover:to-purple-200 transition-all duration-200"
                                >
                                    <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                                        <User className="w-4 h-4 text-white" />
                                    </div>
                                    <span className="font-medium">
                                        {user?.firstName || 'User'}
                                    </span>
                                    <ChevronDown className="w-4 h-4" />
                                </button>

                                {/* User Dropdown */}
                                <AnimatePresence>
                                    {isUserMenuOpen && (
                                        <motion.div
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            exit={{ opacity: 0, y: 10 }}
                                            className="absolute right-0 top-full mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-200 py-2"
                                        >
                                            <div className="px-4 py-2 border-b border-gray-100">
                                                <p className="font-medium text-gray-900">
                                                    {user?.firstName} {user?.lastName}
                                                </p>
                                                <p className="text-sm text-gray-500">{user?.email}</p>
                                            </div>
                                            <button
                                                onClick={() => onNavigate('dashboard')}
                                                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                                            >
                                                <User className="w-4 h-4" />
                                                Dashboard
                                            </button>
                                            <button
                                                onClick={() => onNavigate('wellfound-linkedin')}
                                                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                                            >
                                                <Rocket className="w-4 h-4" />
                                                Wellfound + LinkedIn
                                            </button>
                                            <button
                                                onClick={() => onNavigate('settings')}
                                                className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center gap-2"
                                            >
                                                <Settings className="w-4 h-4" />
                                                Settings
                                            </button>
                                            <button
                                                onClick={handleLogout}
                                                className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center gap-2"
                                            >
                                                <LogOut className="w-4 h-4" />
                                                Logout
                                            </button>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        ) : (
                            <div className="flex items-center gap-3">
                                <button
                                    onClick={onAuthClick}
                                    className="text-gray-600 hover:text-blue-600 font-medium transition-colors duration-200"
                                >
                                    Sign In
                                </button>
                                <button
                                    onClick={onAuthClick}
                                    className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium"
                                >
                                    Get Started
                                </button>
                            </div>
                        )}
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="lg:hidden p-2 text-gray-600 hover:text-blue-600 transition-colors"
                    >
                        {isMenuOpen ? (
                            <X className="w-6 h-6" />
                        ) : (
                            <Menu className="w-6 h-6" />
                        )}
                    </button>
                </div>

                {/* Mobile Menu */}
                <AnimatePresence>
                    {isMenuOpen && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="lg:hidden overflow-hidden border-t border-gray-200 mt-4 pt-4"
                        >
                            <nav className="flex flex-col gap-4">
                                {navItems.map((item) => (
                                    <button
                                        key={item.label}
                                        onClick={() => handleNavClick(item.action)}
                                        className="text-gray-600 hover:text-blue-600 font-medium transition-colors duration-200 py-2 text-left"
                                    >
                                        {item.label}
                                    </button>
                                ))}

                                {isAuthenticated ? (
                                    <div className="flex flex-col gap-3 pt-4 border-t border-gray-200">
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center">
                                                <User className="w-4 h-4 text-white" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">
                                                    {user?.firstName} {user?.lastName}
                                                </p>
                                                <p className="text-sm text-gray-500">{user?.email}</p>
                                            </div>
                                        </div>
                                        <button
                                            onClick={() => {
                                                onNavigate('dashboard');
                                                setIsMenuOpen(false);
                                            }}
                                            className="text-left text-gray-700 hover:text-blue-600 font-medium transition-colors py-2"
                                        >
                                            Dashboard
                                        </button>
                                        <button
                                            onClick={() => {
                                                onNavigate('settings');
                                                setIsMenuOpen(false);
                                            }}
                                            className="text-left text-gray-700 hover:text-blue-600 font-medium transition-colors py-2"
                                        >
                                            Settings
                                        </button>
                                        <button
                                            onClick={() => {
                                                handleLogout();
                                                setIsMenuOpen(false);
                                            }}
                                            className="text-left text-red-600 hover:text-red-700 font-medium transition-colors py-2"
                                        >
                                            Logout
                                        </button>
                                    </div>
                                ) : (
                                    <div className="flex flex-col gap-3 pt-4 border-t border-gray-200">
                                        <button
                                            onClick={() => {
                                                onAuthClick();
                                                setIsMenuOpen(false);
                                            }}
                                            className="text-gray-600 hover:text-blue-600 font-medium transition-colors text-left py-2"
                                        >
                                            Sign In
                                        </button>
                                        <button
                                            onClick={() => {
                                                onAuthClick();
                                                setIsMenuOpen(false);
                                            }}
                                            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-200 font-medium text-center"
                                        >
                                            Get Started
                                        </button>
                                    </div>
                                )}
                            </nav>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </header>
    );
};

export default Header;
