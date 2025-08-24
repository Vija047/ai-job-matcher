'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Users,
    TrendingUp,
    Award,
    Target,
    Star,
    BarChart3,
    AlertCircle,
    CheckCircle,
    ArrowUp,
    ArrowDown,
    Minus
} from 'lucide-react';

export default function IndustryComparison({ resumeAnalysis }) {
    const [selectedIndustry, setSelectedIndustry] = useState('Technology');

    if (!resumeAnalysis) return null;

    const { resume_score = 75, experience_level = 'mid', all_skills = [] } = resumeAnalysis;

    // Industry benchmarks (simulated data)
    const industryBenchmarks = {
        Technology: {
            avgScore: 78,
            topSkills: ['JavaScript', 'Python', 'React', 'AWS', 'Docker'],
            salaryRange: '$80K - $150K',
            demandLevel: 'High',
            growthRate: '+12%',
            competitionLevel: 'High'
        },
        Healthcare: {
            avgScore: 72,
            topSkills: ['Data Analysis', 'SQL', 'Python', 'Statistics', 'Healthcare IT'],
            salaryRange: '$65K - $120K',
            demandLevel: 'Very High',
            growthRate: '+18%',
            competitionLevel: 'Medium'
        },
        Finance: {
            avgScore: 80,
            topSkills: ['Excel', 'Python', 'SQL', 'Financial Modeling', 'Risk Analysis'],
            salaryRange: '$75K - $160K',
            demandLevel: 'High',
            growthRate: '+8%',
            competitionLevel: 'Very High'
        },
        Marketing: {
            avgScore: 69,
            topSkills: ['Digital Marketing', 'Analytics', 'SEO', 'Content Creation', 'Social Media'],
            salaryRange: '$50K - $110K',
            demandLevel: 'Medium',
            growthRate: '+6%',
            competitionLevel: 'High'
        }
    };

    // Experience level benchmarks
    const experienceBenchmarks = {
        entry: { avgScore: 65, range: '0-2 years' },
        mid: { avgScore: 75, range: '3-7 years' },
        senior: { avgScore: 85, range: '8+ years' }
    };

    const currentBenchmark = industryBenchmarks[selectedIndustry];
    const experienceBenchmark = experienceBenchmarks[experience_level];

    const getComparisonIcon = (userScore, benchmarkScore) => {
        if (userScore > benchmarkScore + 5) return <ArrowUp className="h-4 w-4 text-green-500" />;
        if (userScore < benchmarkScore - 5) return <ArrowDown className="h-4 w-4 text-red-500" />;
        return <Minus className="h-4 w-4 text-yellow-500" />;
    };

    const getPerformanceText = (userScore, benchmarkScore) => {
        const diff = userScore - benchmarkScore;
        if (diff > 5) return `${diff} points above average`;
        if (diff < -5) return `${Math.abs(diff)} points below average`;
        return 'Near industry average';
    };

    const skillsOverlap = all_skills.filter(skill =>
        currentBenchmark.topSkills.some(topSkill =>
            topSkill.toLowerCase().includes(skill.toLowerCase()) ||
            skill.toLowerCase().includes(topSkill.toLowerCase())
        )
    );

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100"
        >
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <BarChart3 className="h-6 w-6 mr-2 text-blue-600" />
                    Industry Comparison
                </h2>
                <select
                    value={selectedIndustry}
                    onChange={(e) => setSelectedIndustry(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                    {Object.keys(industryBenchmarks).map(industry => (
                        <option key={industry} value={industry}>{industry}</option>
                    ))}
                </select>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
                {/* Score Comparison */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-blue-900 mb-4 flex items-center">
                        <Target className="h-5 w-5 mr-2" />
                        Score Comparison
                    </h3>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-blue-700">Your Score</span>
                            <div className="flex items-center">
                                <span className="text-2xl font-bold text-blue-900 mr-2">{resume_score}</span>
                                {getComparisonIcon(resume_score, currentBenchmark.avgScore)}
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-blue-700">Industry Average</span>
                            <span className="text-xl font-semibold text-blue-800">{currentBenchmark.avgScore}</span>
                        </div>

                        <div className="bg-white bg-opacity-60 rounded-lg p-3">
                            <div className="text-sm text-blue-800 font-medium">
                                {getPerformanceText(resume_score, currentBenchmark.avgScore)}
                            </div>
                        </div>

                        {/* Visual comparison */}
                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span>Your Score</span>
                                <span>{resume_score}%</span>
                            </div>
                            <div className="w-full bg-blue-200 rounded-full h-3">
                                <div
                                    className="h-3 bg-blue-600 rounded-full transition-all duration-700"
                                    style={{ width: `${resume_score}%` }}
                                />
                            </div>

                            <div className="flex justify-between text-sm">
                                <span>Industry Avg</span>
                                <span>{currentBenchmark.avgScore}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                                <div
                                    className="h-3 bg-gray-500 rounded-full transition-all duration-700"
                                    style={{ width: `${currentBenchmark.avgScore}%` }}
                                />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Experience Level Comparison */}
                <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-green-900 mb-4 flex items-center">
                        <Users className="h-5 w-5 mr-2" />
                        Experience Level
                    </h3>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-green-700">Your Level</span>
                            <span className="text-xl font-bold text-green-900 capitalize">{experience_level}</span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-green-700">Experience Range</span>
                            <span className="text-green-800 font-medium">{experienceBenchmark.range}</span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-green-700">Level Average</span>
                            <div className="flex items-center">
                                <span className="text-xl font-semibold text-green-800 mr-2">{experienceBenchmark.avgScore}</span>
                                {getComparisonIcon(resume_score, experienceBenchmark.avgScore)}
                            </div>
                        </div>

                        <div className="bg-white bg-opacity-60 rounded-lg p-3">
                            <div className="text-sm text-green-800 font-medium">
                                {getPerformanceText(resume_score, experienceBenchmark.avgScore)} for {experience_level} level
                            </div>
                        </div>
                    </div>
                </div>

                {/* Skills Match */}
                <div className="bg-gradient-to-br from-purple-50 to-violet-100 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-purple-900 mb-4 flex items-center">
                        <Star className="h-5 w-5 mr-2" />
                        Skills Alignment
                    </h3>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-purple-700">Matching Skills</span>
                            <span className="text-2xl font-bold text-purple-900">{skillsOverlap.length}</span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-purple-700">Top Industry Skills</span>
                            <span className="text-xl font-semibold text-purple-800">{currentBenchmark.topSkills.length}</span>
                        </div>

                        <div className="w-full bg-purple-200 rounded-full h-3">
                            <div
                                className="h-3 bg-purple-600 rounded-full transition-all duration-700"
                                style={{ width: `${(skillsOverlap.length / currentBenchmark.topSkills.length) * 100}%` }}
                            />
                        </div>

                        <div className="bg-white bg-opacity-60 rounded-lg p-3">
                            <div className="text-xs font-medium text-purple-800 mb-2">Your Matching Skills:</div>
                            <div className="flex flex-wrap gap-1">
                                {skillsOverlap.slice(0, 3).map((skill, index) => (
                                    <span
                                        key={index}
                                        className="text-xs bg-purple-200 text-purple-800 px-2 py-1 rounded"
                                    >
                                        {skill}
                                    </span>
                                ))}
                                {skillsOverlap.length > 3 && (
                                    <span className="text-xs text-purple-600">+{skillsOverlap.length - 3} more</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Market Insights */}
                <div className="bg-gradient-to-br from-orange-50 to-red-100 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-orange-900 mb-4 flex items-center">
                        <TrendingUp className="h-5 w-5 mr-2" />
                        Market Insights
                    </h3>

                    <div className="space-y-3">
                        <div className="flex justify-between items-center">
                            <span className="text-orange-700 text-sm">Salary Range</span>
                            <span className="font-semibold text-orange-900">{currentBenchmark.salaryRange}</span>
                        </div>

                        <div className="flex justify-between items-center">
                            <span className="text-orange-700 text-sm">Demand Level</span>
                            <div className="flex items-center">
                                <span className="font-semibold text-orange-900 mr-1">{currentBenchmark.demandLevel}</span>
                                {currentBenchmark.demandLevel === 'Very High' && <ArrowUp className="h-3 w-3 text-green-500" />}
                                {currentBenchmark.demandLevel === 'High' && <ArrowUp className="h-3 w-3 text-blue-500" />}
                                {currentBenchmark.demandLevel === 'Medium' && <Minus className="h-3 w-3 text-yellow-500" />}
                            </div>
                        </div>

                        <div className="flex justify-between items-center">
                            <span className="text-orange-700 text-sm">Growth Rate</span>
                            <span className="font-semibold text-orange-900">{currentBenchmark.growthRate}</span>
                        </div>

                        <div className="flex justify-between items-center">
                            <span className="text-orange-700 text-sm">Competition</span>
                            <span className="font-semibold text-orange-900">{currentBenchmark.competitionLevel}</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Recommendations */}
            <div className="mt-6 bg-yellow-50 rounded-xl p-6 border border-yellow-200">
                <h3 className="text-lg font-semibold text-yellow-900 mb-4 flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2" />
                    Improvement Recommendations
                </h3>

                <div className="space-y-3">
                    {resume_score < currentBenchmark.avgScore && (
                        <div className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
                            <span className="text-yellow-800 text-sm">
                                Focus on reaching the industry average of {currentBenchmark.avgScore} points
                            </span>
                        </div>
                    )}

                    {skillsOverlap.length < currentBenchmark.topSkills.length * 0.6 && (
                        <div className="flex items-start">
                            <CheckCircle className="h-4 w-4 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
                            <span className="text-yellow-800 text-sm">
                                Consider learning: {currentBenchmark.topSkills.filter(skill =>
                                    !skillsOverlap.some(userSkill =>
                                        userSkill.toLowerCase().includes(skill.toLowerCase())
                                    )
                                ).slice(0, 2).join(', ')}
                            </span>
                        </div>
                    )}

                    <div className="flex items-start">
                        <CheckCircle className="h-4 w-4 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" />
                        <span className="text-yellow-800 text-sm">
                            {selectedIndustry} industry is growing at {currentBenchmark.growthRate} - great career choice!
                        </span>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
