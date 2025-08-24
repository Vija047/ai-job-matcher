'use client';

import { useState } from 'react';
import ResumeUpload from './components/ResumeUpload';
import EnhancedDashboard from './components/EnhancedDashboard';
import JobsList from './components/JobsList';
import { Toaster } from 'react-hot-toast';

export default function Home() {
    const [analysisData, setAnalysisData] = useState(null);
    const [activeTab, setActiveTab] = useState('upload');

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400/10 via-purple-400/5 to-cyan-400/10"></div>
            <div className="absolute top-0 left-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
            <div className="absolute top-0 right-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>

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

            {/* Header */}
            <header className="relative z-10 glass-card mx-4 mt-4 mb-8">
                <div className="container mx-auto px-6 py-8">
                    <div className="flex flex-col lg:flex-row items-center justify-between gap-6">
                        <div className="text-center lg:text-left">
                            <h1 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent mb-2">
                                🚀 AI Job Matcher
                            </h1>
                            <p className="text-lg text-gray-600 max-w-2xl">
                                Next-generation AI-powered career matching with real-time insights and personalized recommendations
                            </p>
                        </div>

                        {/* Navigation */}
                        <nav className="flex flex-wrap gap-3">
                            <button
                                onClick={() => setActiveTab('upload')}
                                className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 ${activeTab === 'upload'
                                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                        : 'glass text-gray-700 hover:text-blue-600'
                                    }`}
                            >
                                📄 Upload Resume
                            </button>

                            {analysisData && (
                                <button
                                    onClick={() => setActiveTab('dashboard')}
                                    className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 ${activeTab === 'dashboard'
                                            ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                            : 'glass text-gray-700 hover:text-blue-600'
                                        }`}
                                >
                                    🎯 AI Dashboard
                                </button>
                            )}

                            <button
                                onClick={() => setActiveTab('jobs')}
                                className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 ${activeTab === 'jobs'
                                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                        : 'glass text-gray-700 hover:text-blue-600'
                                    }`}
                            >
                                💼 Browse Jobs
                            </button>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="relative z-10 container mx-auto px-4 pb-12">
                {activeTab === 'upload' && (
                    <div className="animate-fade-in">
                        <ResumeUpload onAnalysisComplete={(result) => {
                            setAnalysisData(result);
                            setActiveTab('dashboard');
                        }} />
                    </div>
                )}

                {activeTab === 'dashboard' && analysisData && (
                    <div className="animate-fade-in">
                        <EnhancedDashboard
                            resumeAnalysis={analysisData.analysis}
                            analysisId={analysisData.analysis_id}
                        />
                    </div>
                )}

                {activeTab === 'jobs' && (
                    <div className="animate-fade-in">
                        <JobsList analysisId={analysisData?.analysis_id} />
                    </div>
                )}
            </main>
        </div>
    );
}
