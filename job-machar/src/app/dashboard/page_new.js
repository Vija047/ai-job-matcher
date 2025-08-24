'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '../../components/auth/AuthContext';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { LogOut, User, Briefcase, FileText, Settings, TrendingUp, Database, Clock, CheckCircle } from 'lucide-react';
import { getStats, getJobs, getApplicationHistory } from '../../utils/api';

export default function Dashboard() {
    const { user, isAuthenticated, loading, logout } = useAuth();
    const router = useRouter();
    const [stats, setStats] = useState(null);
    const [recentJobs, setRecentJobs] = useState([]);
    const [applicationHistory, setApplicationHistory] = useState(null);
    const [dataLoading, setDataLoading] = useState(true);

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            router.push('/auth');
        }
    }, [loading, isAuthenticated, router]);

    useEffect(() => {
        // Fetch real-time data when component mounts
        const fetchDashboardData = async () => {
            if (isAuthenticated) {
                try {
                    setDataLoading(true);

                    // Fetch real-time statistics
                    const statsResponse = await getStats();
                    setStats(statsResponse.statistics);

                    // Fetch recent jobs
                    const jobsResponse = await getJobs();
                    setRecentJobs(jobsResponse.jobs?.slice(0, 5) || []);

                    // Fetch application history
                    try {
                        const historyResponse = await getApplicationHistory();
                        setApplicationHistory(historyResponse);
                    } catch (error) {
                        console.log('Application history not available:', error.message);
                    }

                } catch (error) {
                    console.error('Error fetching dashboard data:', error);
                } finally {
                    setDataLoading(false);
                }
            }
        };

        fetchDashboardData();
    }, [isAuthenticated]);

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return null; // Will redirect to auth
    }

    const handleLogout = () => {
        logout();
        router.push('/');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center">
                            <Link href="/" className="text-xl font-bold text-blue-600">
                                AI Job Matcher
                            </Link>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="text-gray-700">
                                Welcome, {user?.firstName} {user?.lastName}
                            </span>
                            <button
                                onClick={handleLogout}
                                className="flex items-center gap-2 px-4 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                            >
                                <LogOut className="w-4 h-4" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-600 mt-2">Real-time data and insights from your AI Job Matcher</p>
                </div>

                {/* Real-time Statistics */}
                {dataLoading ? (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                        <div className="animate-pulse">
                            <div className="h-4 bg-gray-300 rounded w-1/4 mb-4"></div>
                            <div className="space-y-2">
                                <div className="h-3 bg-gray-300 rounded w-full"></div>
                                <div className="h-3 bg-gray-300 rounded w-3/4"></div>
                            </div>
                        </div>
                    </div>
                ) : stats && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                            <TrendingUp className="w-5 h-5" />
                            Real-time System Statistics
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                            <div className="bg-blue-50 rounded-lg p-4">
                                <div className="flex items-center gap-2 mb-2">
                                    <Database className="w-5 h-5 text-blue-600" />
                                    <span className="font-medium text-blue-900">Total Analyses</span>
                                </div>
                                <p className="text-2xl font-bold text-blue-600">{stats.total_analyses}</p>
                            </div>
                            <div className="bg-green-50 rounded-lg p-4">
                                <div className="flex items-center gap-2 mb-2">
                                    <CheckCircle className="w-5 h-5 text-green-600" />
                                    <span className="font-medium text-green-900">Resume Parser</span>
                                </div>
                                <p className="text-lg font-semibold text-green-600">
                                    {stats.components_loaded?.resume_parser ? 'Active' : 'Inactive'}
                                </p>
                            </div>
                            <div className="bg-purple-50 rounded-lg p-4">
                                <div className="flex items-center gap-2 mb-2">
                                    <Briefcase className="w-5 h-5 text-purple-600" />
                                    <span className="font-medium text-purple-900">Job Client</span>
                                </div>
                                <p className="text-lg font-semibold text-purple-600">
                                    {stats.components_loaded?.job_client ? 'Connected' : 'Disconnected'}
                                </p>
                            </div>
                        </div>
                        {stats.features && (
                            <div>
                                <h3 className="font-medium text-gray-900 mb-2">Active Features:</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                    {stats.features.map((feature, index) => (
                                        <div key={index} className="text-sm text-gray-700">
                                            {feature}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* Recent Jobs */}
                {recentJobs.length > 0 && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                            <Clock className="w-5 h-5" />
                            Recent Job Opportunities (Live Data)
                        </h2>
                        <div className="space-y-3">
                            {recentJobs.map((job, index) => (
                                <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                                    <h3 className="font-medium text-gray-900">{job.title}</h3>
                                    <p className="text-gray-600">{job.company}</p>
                                    {job.location && <p className="text-sm text-gray-500">{job.location}</p>}
                                    {job.salary && <p className="text-sm text-green-600 font-medium">{job.salary}</p>}
                                    {job.description && (
                                        <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                                            {job.description.substring(0, 100)}...
                                        </p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Application History */}
                {applicationHistory && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                        <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                            <FileText className="w-5 h-5" />
                            Application History
                        </h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-blue-600">{applicationHistory.total_applications || 0}</p>
                                <p className="text-sm text-gray-600">Total Applications</p>
                            </div>
                            <div className="text-center">
                                <p className="text-2xl font-bold text-green-600">{applicationHistory.successful_applications || 0}</p>
                                <p className="text-sm text-gray-600">Successful</p>
                            </div>
                            <div className="text-center">
                                <p className="text-2xl font-bold text-yellow-600">{applicationHistory.pending_applications || 0}</p>
                                <p className="text-sm text-gray-600">Pending</p>
                            </div>
                        </div>
                    </div>
                )}

                {/* User Info Card */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
                        <User className="w-5 h-5" />
                        Profile Information
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Name</label>
                            <p className="text-gray-900">{user?.firstName} {user?.lastName}</p>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email</label>
                            <p className="text-gray-900">{user?.email}</p>
                        </div>
                        {user?.phone && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Phone</label>
                                <p className="text-gray-900">{user.phone}</p>
                            </div>
                        )}
                        {user?.company && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Company</label>
                                <p className="text-gray-900">{user.company}</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Link
                        href="/"
                        className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                    >
                        <div className="flex items-center gap-3 mb-3">
                            <FileText className="w-8 h-8 text-blue-600" />
                            <h3 className="text-lg font-semibold text-gray-900">Upload Resume</h3>
                        </div>
                        <p className="text-gray-600">Upload your resume to get real-time job recommendations</p>
                    </Link>

                    <Link
                        href="/score-dashboard"
                        className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                    >
                        <div className="flex items-center gap-3 mb-3">
                            <Briefcase className="w-8 h-8 text-green-600" />
                            <h3 className="text-lg font-semibold text-gray-900">Job Matches</h3>
                        </div>
                        <p className="text-gray-600">View your personalized job recommendations with live data</p>
                    </Link>

                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center gap-3 mb-3">
                            <Settings className="w-8 h-8 text-purple-600" />
                            <h3 className="text-lg font-semibold text-gray-900">Settings</h3>
                        </div>
                        <p className="text-gray-600">Manage your account settings and job preferences</p>
                    </div>
                </div>

                {/* Real-time Status Footer */}
                <div className="mt-8 text-center">
                    <p className="text-sm text-gray-500">
                        Dashboard data refreshed • {new Date().toLocaleTimeString()}
                        <span className="inline-block w-2 h-2 bg-green-500 rounded-full ml-2 animate-pulse"></span>
                    </p>
                </div>
            </main>
        </div>
    );
}
