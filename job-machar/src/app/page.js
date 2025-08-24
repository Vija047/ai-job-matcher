'use client';

import { useState } from 'react';
import { useAuth } from '../components/auth/AuthContext';
import { useNavigation } from '../components/navigation/NavigationContext';
import Header from '../components/layout/Header';
import LandingPage from '../components/landing/LandingPage';
import FeaturesPage from '../components/pages/FeaturesPage';
import HowItWorksPage from '../components/pages/HowItWorksPage';
import TestimonialsPage from '../components/pages/TestimonialsPage';
import ContactPage from '../components/pages/ContactPage';
import ResumeUpload from '../components/features/ResumeUpload';
import EnhancedDashboard from '../components/features/Dashboard';
import JobsList from '../components/features/JobsList';
import SettingsPage from '../components/settings/SettingsPage';
import { Toaster } from 'react-hot-toast';
import { useRouter } from 'next/navigation';

function AppContent() {
  const { isAuthenticated } = useAuth();
  const { currentPage } = useNavigation();
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

  const handleAnalysisComplete = (analysisData) => {
    setAnalysisData(analysisData);
    localStorage.setItem('latestResumeAnalysis', JSON.stringify(analysisData));
    setActiveTab('dashboard');
  };

  const renderPage = () => {
    // If authenticated and using app functionality
    if (isAuthenticated && ['upload', 'dashboard', 'jobs', 'settings'].includes(activeTab)) {
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
            <nav className="glass-card p-2 rounded-2xl mb-8 inline-flex gap-2">
              <button
                onClick={() => setActiveTab('upload')}
                className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center space-x-2 ${activeTab === 'upload'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-white/50'
                  }`}
              >
                <span>🎯</span>
                <span>Smart Upload</span>
                {analysisData && (
                  <span className="text-xs bg-green-100 text-green-600 px-2 py-1 rounded-full">✓</span>
                )}
              </button>
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center space-x-2 ${activeTab === 'dashboard'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                  : 'text-gray-600 hover:text-blue-600 hover:bg-white/50'
                  }`}
              >
                <span>📊</span>
                <span>Dashboard</span>
                {analysisData && (
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                )}
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

            {/* Tab Content */}
            {activeTab === 'upload' && (
              <ResumeUpload onAnalysisComplete={handleAnalysisComplete} />
            )}

            {activeTab === 'dashboard' && (
              <EnhancedDashboard
                resumeAnalysis={analysisData}
                analysisId={analysisData?.analysis_id}
              />
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

    // Public pages based on navigation context
    switch (currentPage) {
      case 'features':
        return (
          <div className="min-h-screen">
            <Header onAuthClick={handleAuthClick} onNavigate={handleNavigate} />
            <FeaturesPage />
          </div>
        );
      case 'how-it-works':
        return (
          <div className="min-h-screen">
            <Header onAuthClick={handleAuthClick} onNavigate={handleNavigate} />
            <HowItWorksPage />
          </div>
        );
      case 'testimonials':
        return (
          <div className="min-h-screen">
            <Header onAuthClick={handleAuthClick} onNavigate={handleNavigate} />
            <TestimonialsPage />
          </div>
        );
      case 'contact':
        return (
          <div className="min-h-screen">
            <Header onAuthClick={handleAuthClick} onNavigate={handleNavigate} />
            <ContactPage />
          </div>
        );
      default:
        return (
          <div className="min-h-screen">
            <Header onAuthClick={handleAuthClick} onNavigate={handleNavigate} />
            <LandingPage onGetStarted={handleGetStarted} />
          </div>
        );
    }
  };

  return renderPage();
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
      <AppContent />
    </>
  );
}
