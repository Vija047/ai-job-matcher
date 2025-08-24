'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Award,
    TrendingUp,
    User,
    Star,
    CheckCircle,
    AlertCircle,
    Target,
    Brain,
    Briefcase,
    BarChart3,
    Gauge,
    Trophy,
    MapPin,
    Calendar,
    Zap,
    Code,
    Shield,
    Rocket,
    Users
} from 'lucide-react';
import IndustryComparison from './IndustryComparison';

export default function ResumeScoreBoard({ resumeAnalysis }) {
    const [activeTab, setActiveTab] = useState('overview');

    if (!resumeAnalysis) return null;

    const {
        resume_score = 75,
        quality_grade = 'B',
        total_skills_count = 0,
        experience_level = 'mid',
        years_experience = 0,
        suggested_role = 'Software Engineer',
        all_skills = [],
        skills_by_category = {},
        skills_extracted = [],
        contact_info = {},
        education = []
    } = resumeAnalysis;

    // Extract technical skills from skills_by_category
    const extractTechnicalSkills = () => {
        const technicalCategories = [
            'programming_languages',
            'web_technologies',
            'frameworks_libraries',
            'databases',
            'cloud_platforms',
            'devops_tools',
            'tools_technologies'
        ];

        let technicalSkills = [];

        if (skills_by_category && typeof skills_by_category === 'object') {
            technicalCategories.forEach(category => {
                if (skills_by_category[category] && Array.isArray(skills_by_category[category])) {
                    technicalSkills.push(...skills_by_category[category]);
                }
            });
        }

        // Remove duplicates and filter out invalid entries
        return [...new Set(technicalSkills)].filter(skill =>
            skill &&
            typeof skill === 'string' &&
            skill.trim().length > 0 &&
            !skill.includes('\n') && // Filter out malformed entries
            skill.length < 50 // Reasonable skill name length
        );
    };

    // Extract soft skills from skills_by_category  
    const extractSoftSkills = () => {
        const softCategories = ['soft_skills'];
        let softSkills = [];

        if (skills_by_category && typeof skills_by_category === 'object') {
            softCategories.forEach(category => {
                if (skills_by_category[category] && Array.isArray(skills_by_category[category])) {
                    softSkills.push(...skills_by_category[category]);
                }
            });
        }

        // If no soft skills found in categories, use some common defaults based on role
        if (softSkills.length === 0) {
            softSkills = ['Communication', 'Problem Solving', 'Teamwork', 'Leadership'];
        }

        return [...new Set(softSkills)].filter(skill =>
            skill && typeof skill === 'string' && skill.trim().length > 0
        );
    };

    const technical_skills = extractTechnicalSkills();
    const soft_skills = extractSoftSkills();

    // Enhanced scoring breakdown
    const scoreBreakdown = {
        technical_skills: Math.min(100, (technical_skills?.length || 0) * 8),
        experience: Math.min(100, years_experience * 15),
        education: education?.length > 0 ? 85 : 60,
        contact_completeness: Object.keys(contact_info || {}).length * 20,
        role_alignment: calculateRoleAlignment(),
        soft_skills: Math.min(100, (soft_skills?.length || 0) * 12)
    };

    function calculateRoleAlignment() {
        const roleKeywords = suggested_role.toLowerCase().split(' ');
        // Use both technical skills and extracted skills for better alignment calculation
        const allUserSkills = [...technical_skills, ...soft_skills, ...(skills_extracted || [])];
        const skillsText = allUserSkills.join(' ').toLowerCase();
        const matches = roleKeywords.filter(keyword => skillsText.includes(keyword));
        return Math.min(100, (matches.length / roleKeywords.length) * 100);
    }

    // Market demand simulation
    const marketDemand = {
        suggested_role,
        demand_score: Math.floor(Math.random() * 30) + 70, // 70-100
        avg_salary: getSalaryRange(suggested_role),
        job_openings: Math.floor(Math.random() * 500) + 100,
        growth_rate: Math.floor(Math.random() * 15) + 5
    };

    function getSalaryRange(role) {
        const salaryRanges = {
            'software engineer': '$80K - $150K',
            'data scientist': '$90K - $160K',
            'product manager': '$100K - $180K',
            'ui/ux designer': '$70K - $130K',
            'devops engineer': '$85K - $155K',
            'full stack developer': '$75K - $140K',
            'machine learning engineer': '$100K - $170K'
        };
        return salaryRanges[role.toLowerCase()] || '$70K - $140K';
    }

    // Color scheme based on score
    const getScoreColor = (score) => {
        if (score >= 90) return 'from-green-500 to-emerald-600';
        if (score >= 80) return 'from-blue-500 to-cyan-600';
        if (score >= 70) return 'from-yellow-500 to-orange-600';
        if (score >= 60) return 'from-orange-500 to-red-500';
        return 'from-red-500 to-red-600';
    };

    const getScoreLabel = (score) => {
        if (score >= 90) return 'Excellent';
        if (score >= 80) return 'Good';
        if (score >= 70) return 'Average';
        if (score >= 60) return 'Below Average';
        return 'Needs Improvement';
    };

    const tabs = [
        { id: 'overview', label: 'Overview', icon: Gauge },
        { id: 'breakdown', label: 'Score Breakdown', icon: BarChart3 },
        { id: 'roles', label: 'Role Analysis', icon: Briefcase },
        { id: 'market', label: 'Market Insights', icon: TrendingUp },
        { id: 'comparison', label: 'Industry Comparison', icon: Users }
    ];

    const renderOverview = () => (
        <div className="space-y-6">
            {/* Main Score Display */}
            <div className="flex items-center justify-center mb-8">
                <div className="relative">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                        className={`w-40 h-40 rounded-full bg-gradient-to-r ${getScoreColor(resume_score)} flex items-center justify-center shadow-xl`}
                    >
                        <div className="text-center text-white">
                            <div className="text-4xl font-bold">{resume_score}</div>
                            <div className="text-sm opacity-90">/ 100</div>
                        </div>
                    </motion.div>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.5 }}
                        className="absolute -bottom-3 left-1/2 transform -translate-x-1/2 bg-white px-4 py-2 rounded-full shadow-lg"
                    >
                        <span className={`text-sm font-semibold ${resume_score >= 80 ? 'text-green-600' :
                            resume_score >= 70 ? 'text-yellow-600' : 'text-red-600'
                            }`}>
                            {getScoreLabel(resume_score)}
                        </span>
                    </motion.div>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="bg-blue-50 p-4 rounded-xl text-center border border-blue-200"
                >
                    <User className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-blue-900">{total_skills_count}</div>
                    <div className="text-sm text-blue-600">Skills Identified</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="bg-green-50 p-4 rounded-xl text-center border border-green-200"
                >
                    <TrendingUp className="h-6 w-6 text-green-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-green-900">{years_experience}</div>
                    <div className="text-sm text-green-600">Years Experience</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="bg-purple-50 p-4 rounded-xl text-center border border-purple-200"
                >
                    <Star className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                    <div className="text-lg font-bold text-purple-900 capitalize">{experience_level}</div>
                    <div className="text-sm text-purple-600">Level</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="bg-orange-50 p-4 rounded-xl text-center border border-orange-200"
                >
                    <Trophy className="h-6 w-6 text-orange-600 mx-auto mb-2" />
                    <div className="text-sm font-bold text-orange-900">{quality_grade}</div>
                    <div className="text-sm text-orange-600">Grade</div>
                </motion.div>
            </div>

            {/* Progress Bars */}
            <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-gray-50 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Skills Progress</h3>
                    <div className="space-y-3">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span>Technical Skills</span>
                                <span>{technical_skills?.length || 0}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="h-2 rounded-full bg-blue-500 transition-all duration-700"
                                    style={{ width: `${Math.min(100, (technical_skills?.length || 0) * 10)}%` }}
                                />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span>Soft Skills</span>
                                <span>{soft_skills?.length || 0}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="h-2 rounded-full bg-green-500 transition-all duration-700"
                                    style={{ width: `${Math.min(100, (soft_skills?.length || 0) * 15)}%` }}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                <div className="bg-gray-50 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Profile Completeness</h3>
                    <div className="space-y-3">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span>Contact Information</span>
                                <span>{Object.keys(contact_info || {}).length}/5</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="h-2 rounded-full bg-purple-500 transition-all duration-700"
                                    style={{ width: `${Object.keys(contact_info || {}).length * 20}%` }}
                                />
                            </div>
                        </div>
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span>Education</span>
                                <span>{education?.length > 0 ? 'Complete' : 'Incomplete'}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="h-2 rounded-full bg-orange-500 transition-all duration-700"
                                    style={{ width: `${education?.length > 0 ? 100 : 20}%` }}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );

    const renderScoreBreakdown = () => (
        <div className="space-y-6">
            <div className="grid gap-4">
                {Object.entries(scoreBreakdown).map(([category, score], index) => (
                    <motion.div
                        key={category}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm"
                    >
                        <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center">
                                {category === 'technical_skills' && <Code className="h-5 w-5 text-blue-600 mr-2" />}
                                {category === 'experience' && <Briefcase className="h-5 w-5 text-green-600 mr-2" />}
                                {category === 'education' && <Award className="h-5 w-5 text-purple-600 mr-2" />}
                                {category === 'contact_completeness' && <User className="h-5 w-5 text-orange-600 mr-2" />}
                                {category === 'role_alignment' && <Target className="h-5 w-5 text-red-600 mr-2" />}
                                {category === 'soft_skills' && <Star className="h-5 w-5 text-yellow-600 mr-2" />}
                                <span className="font-medium text-gray-900 capitalize">
                                    {category.replace('_', ' ')}
                                </span>
                            </div>
                            <span className="text-lg font-bold text-gray-900">{Math.round(score)}/100</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${score}%` }}
                                transition={{ delay: 0.5 + index * 0.1, duration: 0.8 }}
                                className={`h-3 rounded-full ${getScoreColor(score).replace('to-', 'to-')}`}
                                style={{
                                    background: `linear-gradient(90deg, ${score >= 80 ? '#10b981, #059669' :
                                        score >= 60 ? '#f59e0b, #d97706' :
                                            '#ef4444, #dc2626'
                                        })`
                                }}
                            />
                        </div>
                        <div className="mt-2 text-sm text-gray-600">
                            {category === 'technical_skills' && (
                                <div>
                                    <div>{technical_skills?.length || 0} technical skills identified</div>
                                    {technical_skills?.length > 0 && (
                                        <div className="text-xs text-blue-600 mt-1">
                                            Top skills: {technical_skills.slice(0, 3).join(', ')}
                                            {technical_skills.length > 3 && ` +${technical_skills.length - 3} more`}
                                        </div>
                                    )}
                                </div>
                            )}
                            {category === 'experience' && `${years_experience} years of professional experience`}
                            {category === 'education' && (education?.length > 0 ? 'Education information provided' : 'Add education details')}
                            {category === 'contact_completeness' && `${Object.keys(contact_info || {}).length}/5 contact fields complete`}
                            {category === 'role_alignment' && `Skills align with ${suggested_role} role`}
                            {category === 'soft_skills' && `${soft_skills?.length || 0} soft skills identified`}
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );

    const renderRoleAnalysis = () => (
        <div className="space-y-6">
            {/* Suggested Role Card */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-6 border border-blue-200"
            >
                <div className="flex items-center mb-4">
                    <Rocket className="h-6 w-6 text-blue-600 mr-2" />
                    <h3 className="text-xl font-bold text-blue-900">Recommended Role</h3>
                </div>
                <div className="text-center">
                    <div className="text-3xl font-bold text-blue-900 mb-2">{suggested_role}</div>
                    <div className="text-blue-700 mb-4">Based on your skills and experience</div>
                    <div className="inline-flex items-center bg-blue-200 text-blue-800 px-4 py-2 rounded-full">
                        <CheckCircle className="h-4 w-4 mr-1" />
                        {Math.round(scoreBreakdown.role_alignment)}% Match
                    </div>
                </div>
            </motion.div>

            {/* Alternative Roles */}
            <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Target className="h-5 w-5 mr-2 text-purple-600" />
                    Alternative Career Paths
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                    {getAlternativeRoles().map((role, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.1 }}
                            className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
                        >
                            <div className="flex justify-between items-start mb-2">
                                <div className="font-medium text-gray-900">{role.title}</div>
                                <span className="text-sm bg-gray-100 text-gray-600 px-2 py-1 rounded">
                                    {role.match}% match
                                </span>
                            </div>
                            <div className="text-sm text-gray-600 mb-2">{role.description}</div>
                            <div className="flex flex-wrap gap-1">
                                {role.requiredSkills.map((skill, idx) => (
                                    <span
                                        key={idx}
                                        className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </div>
    );

    const renderMarketInsights = () => (
        <div className="space-y-6">
            {/* Market Demand */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-6 border border-green-200"
            >
                <div className="flex items-center mb-4">
                    <TrendingUp className="h-6 w-6 text-green-600 mr-2" />
                    <h3 className="text-xl font-bold text-green-900">Market Demand for {suggested_role}</h3>
                </div>
                <div className="grid md:grid-cols-4 gap-4">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-900">{marketDemand.demand_score}%</div>
                        <div className="text-sm text-green-700">Demand Score</div>
                    </div>
                    <div className="text-center">
                        <div className="text-lg font-bold text-green-900">{marketDemand.avg_salary}</div>
                        <div className="text-sm text-green-700">Salary Range</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-900">{marketDemand.job_openings}+</div>
                        <div className="text-sm text-green-700">Open Positions</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-900">+{marketDemand.growth_rate}%</div>
                        <div className="text-sm text-green-700">Growth Rate</div>
                    </div>
                </div>
            </motion.div>

            {/* Skills in Demand */}
            <div className="bg-white rounded-xl p-6 border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <Zap className="h-5 w-5 mr-2 text-yellow-600" />
                    Top Skills in Demand
                </h3>
                <div className="grid md:grid-cols-2 gap-6">
                    <div>
                        <h4 className="font-medium text-gray-900 mb-3">Technical Skills</h4>
                        <div className="space-y-2">
                            {getTopDemandSkills('technical').map((skill, index) => (
                                <div key={index} className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        <span className={`text-sm ${skill.userHas ? 'text-green-700 font-medium' : 'text-gray-700'}`}>
                                            {skill.name}
                                        </span>
                                        {skill.userHas && (
                                            <CheckCircle className="h-4 w-4 text-green-600 ml-2" />
                                        )}
                                    </div>
                                    <div className="flex items-center">
                                        <div className="w-16 h-2 bg-gray-200 rounded-full mr-2">
                                            <div
                                                className={`h-2 rounded-full ${skill.userHas ? 'bg-green-500' : 'bg-blue-500'}`}
                                                style={{ width: `${skill.demand}%` }}
                                            />
                                        </div>
                                        <span className="text-xs text-gray-500">{skill.demand}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div>
                        <h4 className="font-medium text-gray-900 mb-3">Soft Skills</h4>
                        <div className="space-y-2">
                            {getTopDemandSkills('soft').map((skill, index) => (
                                <div key={index} className="flex items-center justify-between">
                                    <span className="text-sm text-gray-700">{skill.name}</span>
                                    <div className="flex items-center">
                                        <div className="w-16 h-2 bg-gray-200 rounded-full mr-2">
                                            <div
                                                className="h-2 bg-green-500 rounded-full"
                                                style={{ width: `${skill.demand}%` }}
                                            />
                                        </div>
                                        <span className="text-xs text-gray-500">{skill.demand}%</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Recommendations */}
            <div className="bg-yellow-50 rounded-xl p-6 border border-yellow-200">
                <h3 className="text-lg font-semibold text-yellow-900 mb-4 flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2" />
                    Career Recommendations
                </h3>
                <ul className="space-y-2">
                    {getCareerRecommendations().map((recommendation, index) => (
                        <motion.li
                            key={index}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="flex items-start"
                        >
                            <CheckCircle className="h-4 w-4 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
                            <span className="text-yellow-800 text-sm">{recommendation}</span>
                        </motion.li>
                    ))}
                </ul>
            </div>
        </div>
    );

    function getAlternativeRoles() {
        const baseRoles = [
            {
                title: 'Senior Software Engineer',
                match: 85,
                description: 'Lead technical projects and mentor junior developers',
                requiredSkills: ['React', 'Node.js', 'Leadership', 'Architecture']
            },
            {
                title: 'Full Stack Developer',
                match: 80,
                description: 'Work on both frontend and backend development',
                requiredSkills: ['JavaScript', 'Python', 'Database', 'API Design']
            },
            {
                title: 'Technical Lead',
                match: 75,
                description: 'Combine technical expertise with team leadership',
                requiredSkills: ['Technical Skills', 'Leadership', 'Project Management', 'Mentoring']
            },
            {
                title: 'Product Engineer',
                match: 70,
                description: 'Bridge the gap between product and engineering',
                requiredSkills: ['Product Thinking', 'Engineering', 'User Focus', 'Analytics']
            }
        ];
        return baseRoles;
    }

    function getTopDemandSkills(type) {
        const technicalSkills = [
            { name: 'React/Next.js', demand: 95 },
            { name: 'Python', demand: 90 },
            { name: 'Cloud (AWS/Azure)', demand: 88 },
            { name: 'JavaScript/TypeScript', demand: 85 },
            { name: 'Docker/Kubernetes', demand: 82 }
        ];

        const softSkills = [
            { name: 'Communication', demand: 98 },
            { name: 'Problem Solving', demand: 95 },
            { name: 'Teamwork', demand: 90 },
            { name: 'Adaptability', demand: 88 },
            { name: 'Leadership', demand: 85 }
        ];

        let skillsToShow = type === 'technical' ? technicalSkills : softSkills;

        // If we have user's technical skills, highlight which ones they have
        if (type === 'technical' && technical_skills.length > 0) {
            skillsToShow = skillsToShow.map(skill => {
                const userHasSkill = technical_skills.some(userSkill =>
                    userSkill.toLowerCase().includes(skill.name.toLowerCase().split('/')[0].toLowerCase()) ||
                    skill.name.toLowerCase().includes(userSkill.toLowerCase())
                );
                return {
                    ...skill,
                    userHas: userHasSkill
                };
            });
        }

        return skillsToShow;
    }

    function getCareerRecommendations() {
        return [
            'Focus on developing cloud computing skills (AWS, Azure) - high market demand',
            'Consider obtaining relevant certifications to strengthen your profile',
            'Build a portfolio showcasing your projects and technical achievements',
            'Develop leadership and mentoring skills for senior role preparation',
            'Stay updated with the latest trends in your field through continuous learning'
        ];
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-lg border border-gray-100"
        >
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                        <Brain className="h-6 w-6 mr-2 text-blue-600" />
                        Resume Score Dashboard
                    </h2>
                    <div className="text-sm text-gray-500">
                        Quality Grade: <span className="font-semibold text-blue-600">{quality_grade}</span>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-200">
                <nav className="flex space-x-8 px-6">
                    {tabs.map((tab) => {
                        const Icon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${activeTab === tab.id
                                    ? 'border-blue-500 text-blue-600'
                                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                <Icon className="h-4 w-4 mr-2" />
                                {tab.label}
                            </button>
                        );
                    })}
                </nav>
            </div>

            {/* Tab Content */}
            <div className="p-6">
                {activeTab === 'overview' && renderOverview()}
                {activeTab === 'breakdown' && renderScoreBreakdown()}
                {activeTab === 'roles' && renderRoleAnalysis()}
                {activeTab === 'market' && renderMarketInsights()}
                {activeTab === 'comparison' && <IndustryComparison resumeAnalysis={resumeAnalysis} />}
            </div>
        </motion.div>
    );
}
