'use client';

import { motion } from 'framer-motion';
import { Award, TrendingUp, User, Star, CheckCircle, AlertCircle } from 'lucide-react';

export default function ResumeScore({ resumeAnalysis }) {
    if (!resumeAnalysis) return null;

    const {
        resume_score = 75,
        quality_grade = 'B',
        total_skills_count = 0,
        experience_level = 'mid',
        years_experience = 0,
        suggested_role = 'Software Engineer'
    } = resumeAnalysis;

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

    const getRecommendations = (score) => {
        if (score >= 90) {
            return [
                "Your resume looks excellent! Consider applying to senior positions.",
                "Add specific achievements with quantifiable results.",
                "Consider adding leadership or mentorship experience."
            ];
        }
        if (score >= 80) {
            return [
                "Strong resume! Add more technical certifications.",
                "Include specific project achievements and metrics.",
                "Consider adding open-source contributions."
            ];
        }
        if (score >= 70) {
            return [
                "Good foundation. Add more relevant skills and projects.",
                "Include quantifiable achievements in your experience.",
                "Consider getting industry certifications."
            ];
        }
        return [
            "Consider adding more relevant technical skills.",
            "Include detailed project descriptions and outcomes.",
            "Add education and certifications to strengthen your profile."
        ];
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100"
        >
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                    <Award className="h-6 w-6 mr-2 text-yellow-500" />
                    Resume Score Analysis
                </h2>
                <div className="text-sm text-gray-500">
                    Quality Grade: <span className="font-semibold text-blue-600">{quality_grade}</span>
                </div>
            </div>

            {/* Main Score Display */}
            <div className="flex items-center justify-center mb-8">
                <div className="relative">
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                        className={`w-32 h-32 rounded-full bg-gradient-to-r ${getScoreColor(resume_score)} flex items-center justify-center shadow-lg`}
                    >
                        <div className="text-center text-white">
                            <div className="text-3xl font-bold">{resume_score}</div>
                            <div className="text-sm opacity-90">/ 100</div>
                        </div>
                    </motion.div>
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.5 }}
                        className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-white px-3 py-1 rounded-full shadow-md"
                    >
                        <span className={`text-sm font-semibold ${resume_score >= 80 ? 'text-green-600' :
                            resume_score >= 70 ? 'text-yellow-600' : 'text-red-600'
                            }`}>
                            {getScoreLabel(resume_score)}
                        </span>
                    </motion.div>
                </div>
            </div>

            {/* Score Breakdown */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.3 }}
                    className="bg-blue-50 p-4 rounded-xl text-center"
                >
                    <User className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-blue-900">{total_skills_count}</div>
                    <div className="text-sm text-blue-600">Skills Identified</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="bg-green-50 p-4 rounded-xl text-center"
                >
                    <TrendingUp className="h-6 w-6 text-green-600 mx-auto mb-2" />
                    <div className="text-2xl font-bold text-green-900">{years_experience}</div>
                    <div className="text-sm text-green-600">Years Experience</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="bg-purple-50 p-4 rounded-xl text-center"
                >
                    <Star className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                    <div className="text-lg font-bold text-purple-900 capitalize">{experience_level}</div>
                    <div className="text-sm text-purple-600">Level</div>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="bg-orange-50 p-4 rounded-xl text-center"
                >
                    <CheckCircle className="h-6 w-6 text-orange-600 mx-auto mb-2" />
                    <div className="text-sm font-bold text-orange-900">{suggested_role}</div>
                    <div className="text-sm text-orange-600">Best Role</div>
                </motion.div>
            </div>

            {/* Recommendations */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
                className="bg-gray-50 rounded-xl p-6"
            >
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                    <AlertCircle className="h-5 w-5 mr-2 text-blue-500" />
                    Recommendations for Improvement
                </h3>
                <ul className="space-y-2">
                    {getRecommendations(resume_score).map((recommendation, index) => (
                        <motion.li
                            key={index}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.8 + index * 0.1 }}
                            className="flex items-start"
                        >
                            <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 mr-2 flex-shrink-0" />
                            <span className="text-gray-700 text-sm">{recommendation}</span>
                        </motion.li>
                    ))}
                </ul>

                {/* Action Button */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.0 }}
                    className="mt-4 pt-4 border-t border-gray-200"
                >
                    <button
                        onClick={() => window.open('/score-dashboard', '_blank')}
                        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white py-3 px-6 rounded-lg font-medium transition-all duration-300 transform hover:scale-105 flex items-center justify-center"
                    >
                        <Award className="h-5 w-5 mr-2" />
                        View Detailed Score Dashboard
                    </button>
                </motion.div>
            </motion.div>

            {/* Score Progress Bar */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.9 }}
                className="mt-6"
            >
                <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Resume Score Progress</span>
                    <span>{resume_score}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${resume_score}%` }}
                        transition={{ delay: 1, duration: 0.8, ease: "easeOut" }}
                        className={`h-2 rounded-full bg-gradient-to-r ${getScoreColor(resume_score)}`}
                    />
                </div>
            </motion.div>
        </motion.div>
    );
}
