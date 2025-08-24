'use client';

import { useState } from 'react';
import { useAuth } from '../components/auth/AuthContext';
import { NavigationProvider, useNavigation } from '../components/navigation/NavigationContext';
import Header from '../components/layout/Header';
import LandingPage from '../components/landing/LandingPage';
import FeaturesPage from '../components/pages/FeaturesPage';
import HowItWorksPage from '../components/pages/HowItWorksPage';
import TestimonialsPage from '../components/pages/TestimonialsPage';
import ContactPage from '../components/pages/ContactPage';
import WellfoundLinkedinPage from '../components/pages/WellfoundLinkedinPage';
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
        // If authenticated and on app functionality
        if (isAuthenticated && ['upload', 'dashboard', 'jobs', 'wellfound-linkedin', 'settings'].includes(activeTab)) {
            switch (activeTab) {
                case 'upload':
                    return (
                        <ResumeUpload
                            onAnalysisComplete={handleAnalysisComplete}
                            onNavigate={handleNavigate}
                        />
                    );
                case 'dashboard':
                    return (
                        <EnhancedDashboard
                            analysisData={analysisData}
                            onNavigate={handleNavigate}
                        />
                    );
                case 'jobs':
                    return (
                        <JobsList
                            analysisData={analysisData}
                            onNavigate={handleNavigate}
                        />
                    );
                case 'wellfound-linkedin':
                    return (
                        <WellfoundLinkedinPage
                            analysisId={analysisData?.analysis_id}
                        />
                    );
                case 'settings':
                    return (
                        <SettingsPage
                            onNavigate={handleNavigate}
                        />
                    );
                default:
                    return <LandingPage onGetStarted={handleGetStarted} />;
            }
        }

        // Public pages based on navigation context
        switch (currentPage) {
            case 'features':
                return <FeaturesPage />;
            case 'how-it-works':
                return <HowItWorksPage />;
            case 'testimonials':
                return <TestimonialsPage />;
            case 'contact':
                return <ContactPage />;
            default:
                return <LandingPage onGetStarted={handleGetStarted} />;
        }
    };

    return (
        <div className="min-h-screen">
            <Header
                onAuthClick={handleAuthClick}
                onNavigate={handleNavigate}
            />
            {renderPage()}
            <Toaster position="top-right" />
        </div>
    );
}

export default function MainApp() {
    return (
        <NavigationProvider>
            <AppContent />
        </NavigationProvider>
    );
}
