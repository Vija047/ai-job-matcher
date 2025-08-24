'use client';

import { useState } from 'react';
import { AuthProvider, useAuth } from '../components/auth/AuthContext';
import Header from '../components/layout/Header';
import LandingPage from '../components/landing/LandingPage';
import ResumeUpload from '../components/features/ResumeUpload';
import EnhancedDashboard from '../components/features/Dashboard';
import JobsList from '../components/features/JobsList';
import SettingsPage from '../components/settings/SettingsPage';
import { Toaster } from 'react-hot-toast';
import { useRouter } from 'next/navigation';

function AppContent() {
    const { isAuthenticated } = useAuth();
    const [analysisData, setAnalysisData] = useState(null);
    const [activeTab, setActiveTab] = useState('landing');
    const router = useRouter();

    const handleGetStarted = () => {
        if (isAuthenticated) {
            setActiveTab('upload');
        } else {
            router.push('/auth');
        }
    };

    const handleAuthClick = () => {
        router.push('/auth');
    };

    const handleNavigate = (tab) => {
        setActiveTab(tab);
    };

    if (!isAuthenticated && activeTab === 'landing') {
        return (
            <div className="min-h-screen">
                <Header
                    onAuthClick={handleAuthClick}
                    onNavigate={handleNavigate}
                />
                <LandingPage onGetStarted={handleGetStarted} />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400/10 via-purple-400/5 to-cyan-400/10"></div>
            <div className="absolute top-0 left-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
            <div className="absolute top-0 right-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>

            <Header
                onAuthClick={handleAuthClick}
                onNavigate={handleNavigate}
            />

            {/* Main Content */}
            <div className="container mx-auto px-6 pb-8">
                {/* Navigation Tabs */}
                {isAuthenticated && (
                    <nav className="glass-card p-2 rounded-2xl mb-8 inline-flex gap-2">
                        <button
                            onClick={() => setActiveTab('upload')}
                            className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${activeTab === 'upload'
                                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                    : 'text-gray-600 hover:text-blue-600 hover:bg-white/50'
                                }`}
                        >
                            🎯 Smart Upload
                        </button>
                        <button
                            onClick={() => setActiveTab('dashboard')}
                            className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${activeTab === 'dashboard'
                                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                    : 'text-gray-600 hover:text-blue-600 hover:bg-white/50'
                                }`}
                        >
                            📊 Dashboard
                        </button>
                        <button
                            onClick={() => setActiveTab('jobs')}
                            className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 ${activeTab === 'jobs'
                                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                    : 'text-gray-600 hover:text-blue-600 hover:bg-white/50'
                                }`}
                        >
                            💼 Job Market
                        </button>
                    </nav>
                )}

                {/* Tab Content */}
                {activeTab === 'upload' && (
                    <ResumeUpload onAnalysisComplete={setAnalysisData} />
                )}

                {activeTab === 'dashboard' && (
                    <EnhancedDashboard analysisData={analysisData} />
                )}

                {activeTab === 'jobs' && (
                    <JobsList analysisData={analysisData} />
                )}

                {activeTab === 'settings' && (
                    <SettingsPage onBack={() => setActiveTab('dashboard')} />
                )}
            </div>
        </div>
    );
}

export default function Home() {
    return (
        <>
            <Toaster
                position="top-right"
                toastOptions={{
                    style: {
                        background: 'rgba(255, 255, 255, 0.9)',
                        backdropFilter: 'blur(20px)',
                        border: '1px solid rgba(255, 255, 255, 0.2)',
                        borderRadius: '12px',
                        fontWeight: '500',
                    }
                }}
            />
            <AuthProvider>
                <AppContent />
            </AuthProvider>
        </>
    );
}
