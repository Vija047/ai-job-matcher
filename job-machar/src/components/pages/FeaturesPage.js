'use client';

import { motion } from 'framer-motion';
import {
    Zap,
    Target,
    Users,
    Shield,
    TrendingUp,
    Clock,
    Award,
    CheckCircle,
    Star,
    ArrowRight
} from 'lucide-react';

const FeaturesPage = () => {
    const features = [
        {
            icon: <Zap className="w-12 h-12" />,
            title: "AI-Powered Matching",
            description: "Our advanced machine learning algorithms analyze your resume, skills, and preferences to match you with the most relevant job opportunities.",
            benefits: [
                "98% accuracy in skill matching",
                "Real-time job market analysis",
                "Personalized recommendations"
            ]
        },
        {
            icon: <Target className="w-12 h-12" />,
            title: "Precision Targeting",
            description: "Get highly targeted job recommendations based on your experience, career goals, and salary expectations.",
            benefits: [
                "Location-based filtering",
                "Salary range matching",
                "Company culture fit analysis"
            ]
        },
        {
            icon: <TrendingUp className="w-12 h-12" />,
            title: "Career Growth Insights",
            description: "Track your career progression and get actionable insights on skills to develop for advancement.",
            benefits: [
                "Skill gap analysis",
                "Career path recommendations",
                "Market trend insights"
            ]
        },
        {
            icon: <Shield className="w-12 h-12" />,
            title: "Privacy & Security",
            description: "Your data is encrypted and secure. We never share your information without explicit consent.",
            benefits: [
                "End-to-end encryption",
                "GDPR compliant",
                "Transparent data usage"
            ]
        },
        {
            icon: <Clock className="w-12 h-12" />,
            title: "Real-time Updates",
            description: "Get instant notifications when new jobs matching your profile become available.",
            benefits: [
                "Push notifications",
                "Email alerts",
                "Weekly digest reports"
            ]
        },
        {
            icon: <Award className="w-12 h-12" />,
            title: "Success Tracking",
            description: "Monitor your application success rate and get tips to improve your job search effectiveness.",
            benefits: [
                "Application analytics",
                "Success rate tracking",
                "Improvement suggestions"
            ]
        }
    ];

    const stats = [
        { number: "500K+", label: "Jobs Matched" },
        { number: "98%", label: "Success Rate" },
        { number: "50K+", label: "Happy Users" },
        { number: "24/7", label: "Support" }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Hero Section */}
            <section className="relative pt-20 pb-16">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        className="text-center max-w-4xl mx-auto"
                    >
                        <h1 className="text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent mb-8">
                            Powerful Features for Your
                            <br />
                            Dream Career
                        </h1>
                        <p className="text-xl text-gray-600 mb-12 leading-relaxed">
                            Discover how our cutting-edge AI technology revolutionizes the way you find and apply for jobs.
                            Every feature is designed to maximize your career success.
                        </p>

                        {/* Stats */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
                            {stats.map((stat, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 + index * 0.1, duration: 0.6 }}
                                    className="text-center"
                                >
                                    <div className="text-3xl lg:text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                                        {stat.number}
                                    </div>
                                    <div className="text-gray-600 font-medium">{stat.label}</div>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Features Grid */}
            <section className="py-20">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl font-bold text-gray-900 mb-6">
                            Everything You Need to Succeed
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Our comprehensive suite of features ensures you never miss an opportunity
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-7xl mx-auto">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.1 * index, duration: 0.6 }}
                                className="glass-card p-8 rounded-2xl hover:shadow-xl transition-all duration-300 group"
                            >
                                <div className="flex items-start gap-6">
                                    <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-4 rounded-xl text-blue-600 group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                                        {feature.icon}
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="text-2xl font-bold text-gray-900 mb-4">
                                            {feature.title}
                                        </h3>
                                        <p className="text-gray-600 leading-relaxed mb-6">
                                            {feature.description}
                                        </p>
                                        <ul className="space-y-3">
                                            {feature.benefits.map((benefit, benefitIndex) => (
                                                <li key={benefitIndex} className="flex items-center gap-3">
                                                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                                    <span className="text-gray-700">{benefit}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Feature Highlight */}
            <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center text-white"
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                            Ready to Experience These Features?
                        </h2>
                        <p className="text-xl text-blue-100 mb-12 max-w-3xl mx-auto">
                            Join thousands of professionals who have already discovered their perfect career match
                        </p>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all duration-200 flex items-center justify-center gap-2 mx-auto shadow-lg hover:shadow-xl"
                        >
                            Start Your Free Trial
                            <ArrowRight className="w-5 h-5" />
                        </motion.button>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default FeaturesPage;
