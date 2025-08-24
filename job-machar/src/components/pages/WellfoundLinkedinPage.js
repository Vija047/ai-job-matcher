'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Rocket,
    Users,
    TrendingUp,
    Star,
    ArrowRight,
    Building,
    MapPin
} from 'lucide-react';
import EnhancedJobsList from '../features/EnhancedJobsList';
import { searchWellfoundLinkedinJobs } from '../../utils/api';

export default function WellfoundLinkedinPage({ analysisId }) {
    const [stats, setStats] = useState({
        totalJobs: 0,
        startupJobs: 0,
        linkedinJobs: 0,
        remoteJobs: 0
    });

    const [popularRoles, setPopularRoles] = useState([
        'Software Engineer',
        'Product Manager',
        'Data Scientist',
        'Frontend Developer',
        'Backend Engineer',
        'DevOps Engineer'
    ]);

    const [featuredCompanies, setFeaturedCompanies] = useState([
        { name: 'OpenAI', stage: 'Series C', employees: '200-500', logo: '🤖' },
        { name: 'Stripe', stage: 'Public', employees: '5000+', logo: '💳' },
        { name: 'Figma', stage: 'Series E', employees: '1000-5000', logo: '🎨' },
        { name: 'Notion', stage: 'Series C', employees: '500-1000', logo: '📝' },
        { name: 'Airbnb', stage: 'Public', employees: '5000+', logo: '🏠' },
        { name: 'Uber', stage: 'Public', employees: '10000+', logo: '🚗' }
    ]);

    const handleQuickSearch = async (role) => {
        // This would trigger a search in the EnhancedJobsList component
        // For now, we'll just show some demo stats
        try {
            const data = await searchWellfoundLinkedinJobs([role], '', '', 30);
            setStats({
                totalJobs: data.total_found || 0,
                startupJobs: data.source_breakdown?.wellfound_count || 0,
                linkedinJobs: data.source_breakdown?.linkedin_count || 0,
                remoteJobs: data.jobs?.filter(job => job.remote_allowed).length || 0
            });
        } catch (error) {
            console.error('Quick search error:', error);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50">
            {/* Hero Section */}
            <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-orange-500 text-white py-16">
                <div className="max-w-7xl mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-8"
                    >
                        <div className="flex items-center justify-center space-x-4 mb-6">
                            <div className="bg-white bg-opacity-20 rounded-full p-3">
                                <Rocket className="w-8 h-8" />
                            </div>
                            <div className="text-2xl font-bold">×</div>
                            <div className="bg-white bg-opacity-20 rounded-full p-3">
                                <Users className="w-8 h-8" />
                            </div>
                        </div>
                        <h1 className="text-4xl lg:text-6xl font-bold mb-4">
                            Startup Jobs + Professional Network
                        </h1>
                        <p className="text-xl lg:text-2xl text-blue-100 max-w-3xl mx-auto">
                            Discover opportunities from innovative startups on Wellfound and professional connections on LinkedIn
                        </p>
                    </motion.div>

                    {/* Quick Stats */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto"
                    >
                        <div className="bg-white bg-opacity-20 rounded-lg p-4">
                            <div className="text-2xl font-bold">{stats.totalJobs.toLocaleString()}</div>
                            <div className="text-sm text-blue-100">Total Jobs</div>
                        </div>
                        <div className="bg-white bg-opacity-20 rounded-lg p-4">
                            <div className="text-2xl font-bold">{stats.startupJobs.toLocaleString()}</div>
                            <div className="text-sm text-blue-100">Startup Roles</div>
                        </div>
                        <div className="bg-white bg-opacity-20 rounded-lg p-4">
                            <div className="text-2xl font-bold">{stats.linkedinJobs.toLocaleString()}</div>
                            <div className="text-sm text-blue-100">LinkedIn Jobs</div>
                        </div>
                        <div className="bg-white bg-opacity-20 rounded-lg p-4">
                            <div className="text-2xl font-bold">{stats.remoteJobs.toLocaleString()}</div>
                            <div className="text-sm text-blue-100">Remote Options</div>
                        </div>
                    </motion.div>
                </div>
            </div>

            {/* Quick Role Search */}
            <div className="max-w-7xl mx-auto px-6 py-12">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="text-center mb-12"
                >
                    <h2 className="text-3xl font-bold text-gray-900 mb-4">
                        Popular Roles
                    </h2>
                    <p className="text-gray-600 mb-8">
                        Quick search for trending positions across startups and established companies
                    </p>

                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        {popularRoles.map((role, index) => (
                            <motion.button
                                key={role}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: 0.1 * index }}
                                onClick={() => handleQuickSearch(role)}
                                className="bg-white rounded-xl shadow-lg p-4 hover:shadow-xl transition-all duration-300 border-2 border-transparent hover:border-blue-500 group"
                            >
                                <div className="text-sm font-semibold text-gray-900 group-hover:text-blue-600">
                                    {role}
                                </div>
                                <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-blue-500 mx-auto mt-2 transform group-hover:translate-x-1 transition-transform" />
                            </motion.button>
                        ))}
                    </div>
                </motion.div>

                {/* Featured Companies */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="mb-12"
                >
                    <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                        Featured Companies
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        {featuredCompanies.map((company, index) => (
                            <motion.div
                                key={company.name}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index }}
                                className="bg-white rounded-xl shadow-lg p-4 text-center hover:shadow-xl transition-all duration-300"
                            >
                                <div className="text-2xl mb-2">{company.logo}</div>
                                <div className="font-semibold text-gray-900 text-sm mb-1">
                                    {company.name}
                                </div>
                                <div className="text-xs text-gray-600 mb-1">
                                    {company.stage}
                                </div>
                                <div className="text-xs text-gray-500">
                                    {company.employees}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Features Highlight */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="grid md:grid-cols-2 gap-8 mb-12"
                >
                    <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6">
                        <div className="flex items-center mb-4">
                            <div className="bg-orange-500 rounded-lg p-2 mr-3">
                                <Rocket className="w-6 h-6 text-white" />
                            </div>
                            <h4 className="text-xl font-bold text-gray-900">Wellfound Startups</h4>
                        </div>
                        <ul className="space-y-2 text-gray-700">
                            <li className="flex items-center">
                                <TrendingUp className="w-4 h-4 text-orange-500 mr-2" />
                                Early-stage to unicorn companies
                            </li>
                            <li className="flex items-center">
                                <Star className="w-4 h-4 text-orange-500 mr-2" />
                                Equity opportunities
                            </li>
                            <li className="flex items-center">
                                <Building className="w-4 h-4 text-orange-500 mr-2" />
                                Direct founder connections
                            </li>
                            <li className="flex items-center">
                                <MapPin className="w-4 h-4 text-orange-500 mr-2" />
                                Global remote-first culture
                            </li>
                        </ul>
                    </div>

                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
                        <div className="flex items-center mb-4">
                            <div className="bg-blue-500 rounded-lg p-2 mr-3">
                                <Users className="w-6 h-6 text-white" />
                            </div>
                            <h4 className="text-xl font-bold text-gray-900">LinkedIn Professional</h4>
                        </div>
                        <ul className="space-y-2 text-gray-700">
                            <li className="flex items-center">
                                <TrendingUp className="w-4 h-4 text-blue-500 mr-2" />
                                Established companies
                            </li>
                            <li className="flex items-center">
                                <Star className="w-4 h-4 text-blue-500 mr-2" />
                                Professional networking
                            </li>
                            <li className="flex items-center">
                                <Building className="w-4 h-4 text-blue-500 mr-2" />
                                Enterprise opportunities
                            </li>
                            <li className="flex items-center">
                                <MapPin className="w-4 h-4 text-blue-500 mr-2" />
                                Traditional + remote hybrid
                            </li>
                        </ul>
                    </div>
                </motion.div>
            </div>

            {/* Enhanced Jobs List */}
            <div className="bg-white">
                <EnhancedJobsList analysisId={analysisId} />
            </div>
        </div>
    );
}
