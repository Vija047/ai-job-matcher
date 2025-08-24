'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowLeft, Download, Share2, AlertCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';
import ResumeScoreBoard from '../../components/features/ResumeScoreBoard';

export default function ScoreBoardPage() {
    const router = useRouter();
    const [resumeAnalysis, setResumeAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Get analysis from localStorage or session storage
        const storedAnalysis = localStorage.getItem('latestResumeAnalysis');
        if (storedAnalysis) {
            try {
                const analysis = JSON.parse(storedAnalysis);
                setResumeAnalysis(analysis);
            } catch (error) {
                console.error('Error parsing stored analysis:', error);
            }
        }
        setLoading(false);
    }, []);

    const handleDownloadReport = () => {
        // Generate and download PDF report
        const reportData = {
            timestamp: new Date().toISOString(),
            ...resumeAnalysis
        };

        const dataStr = JSON.stringify(reportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `resume-score-report-${Date.now()}.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

    const handleShare = async () => {
        if (navigator.share && resumeAnalysis) {
            try {
                await navigator.share({
                    title: 'My Resume Score Report',
                    text: `I scored ${resumeAnalysis.resume_score}/100 on my resume analysis! Check out my detailed breakdown.`,
                    url: window.location.href,
                });
            } catch (error) {
                console.error('Error sharing:', error);
                // Fallback to copying link
                navigator.clipboard.writeText(window.location.href);
                alert('Link copied to clipboard!');
            }
        } else {
            // Fallback for browsers that don't support Web Share API
            navigator.clipboard.writeText(window.location.href);
            alert('Link copied to clipboard!');
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading your score report...</p>
                </div>
            </div>
        );
    }

    if (!resumeAnalysis) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center max-w-md mx-auto p-8"
                >
                    <div className="bg-yellow-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                        <AlertCircle className="h-8 w-8 text-yellow-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">No Resume Analysis Found</h2>
                    <p className="text-gray-600 mb-6">
                        Please upload and analyze your resume first to view the score dashboard.
                    </p>
                    <button
                        onClick={() => router.push('/')}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                    >
                        Go to Upload Page
                    </button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
            {/* Header */}
            <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center">
                            <button
                                onClick={() => router.back()}
                                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
                            >
                                <ArrowLeft className="h-5 w-5 mr-2" />
                                Back
                            </button>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button
                                onClick={handleShare}
                                className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
                            >
                                <Share2 className="h-5 w-5 mr-2" />
                                Share
                            </button>
                            <button
                                onClick={handleDownloadReport}
                                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center"
                            >
                                <Download className="h-4 w-4 mr-2" />
                                Download Report
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8 text-center"
                >
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">
                        Resume Score Dashboard
                    </h1>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        Comprehensive analysis of your resume with detailed scoring, role recommendations,
                        and market insights to help advance your career.
                    </p>
                </motion.div>

                <ResumeScoreBoard resumeAnalysis={resumeAnalysis} />

                {/* Footer */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mt-12 text-center text-gray-500"
                >
                    <p className="text-sm">
                        Report generated on {new Date().toLocaleDateString()} •
                        <span className="ml-1">Powered by AI Job Matcher</span>
                    </p>
                </motion.div>
            </div>
        </div>
    );
}
