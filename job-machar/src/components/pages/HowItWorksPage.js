'use client';

import { motion } from 'framer-motion';
import {
    Upload,
    Brain,
    Target,
    CheckCircle,
    ArrowRight,
    Clock,
    Users,
    TrendingUp
} from 'lucide-react';

const HowItWorksPage = () => {
    const steps = [
        {
            step: "01",
            title: "Upload Your Resume",
            description: "Simply drag and drop your resume or upload it from your device. Our system supports PDF, DOC, and DOCX formats.",
            icon: <Upload className="w-8 h-8" />,
            details: [
                "Secure file processing",
                "Multiple format support",
                "Instant analysis start"
            ]
        },
        {
            step: "02",
            title: "AI Analysis & Processing",
            description: "Our advanced AI algorithms analyze your skills, experience, education, and career preferences to create your unique professional profile.",
            icon: <Brain className="w-8 h-8" />,
            details: [
                "Skills extraction",
                "Experience mapping",
                "Career goal identification"
            ]
        },
        {
            step: "03",
            title: "Smart Job Matching",
            description: "Get personalized job recommendations that match your profile, preferences, and career aspirations from our extensive job database.",
            icon: <Target className="w-8 h-8" />,
            details: [
                "Real-time matching",
                "Compatibility scoring",
                "Filtered recommendations"
            ]
        },
        {
            step: "04",
            title: "Apply & Track Progress",
            description: "Apply to jobs directly through our platform and track your application status with detailed analytics and insights.",
            icon: <TrendingUp className="w-8 h-8" />,
            details: [
                "One-click applications",
                "Status tracking",
                "Success analytics"
            ]
        }
    ];

    const benefits = [
        {
            title: "Save Time",
            description: "Reduce job search time by 70% with AI-powered matching",
            icon: <Clock className="w-6 h-6" />
        },
        {
            title: "Better Matches",
            description: "98% of users find more relevant job opportunities",
            icon: <Target className="w-6 h-6" />
        },
        {
            title: "Higher Success Rate",
            description: "3x higher interview callback rate compared to traditional methods",
            icon: <TrendingUp className="w-6 h-6" />
        },
        {
            title: "Trusted Platform",
            description: "Join 50,000+ professionals who found their dream jobs",
            icon: <Users className="w-6 h-6" />
        }
    ];

    const timeline = [
        { time: "0-2 minutes", action: "Upload and analysis" },
        { time: "2-5 minutes", action: "Review AI insights" },
        { time: "5-10 minutes", action: "Browse job matches" },
        { time: "10+ minutes", action: "Apply to positions" }
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
                            How It Works
                        </h1>
                        <p className="text-xl text-gray-600 mb-12 leading-relaxed">
                            Get matched with your dream job in just four simple steps.
                            Our AI-powered platform makes job searching effortless and effective.
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Timeline Overview */}
            <section className="py-12 bg-white">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="text-center mb-12"
                    >
                        <h2 className="text-3xl font-bold text-gray-900 mb-6">
                            From Upload to Application in Minutes
                        </h2>
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto">
                            {timeline.map((item, index) => (
                                <div key={index} className="text-center">
                                    <div className="bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-full text-blue-600 font-bold mb-2">
                                        {item.time}
                                    </div>
                                    <p className="text-gray-600 text-sm">{item.action}</p>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Steps Section */}
            <section className="py-20">
                <div className="container mx-auto px-6">
                    <div className="max-w-6xl mx-auto">
                        {steps.map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                transition={{ delay: index * 0.2, duration: 0.8 }}
                                viewport={{ once: true }}
                                className={`flex flex-col lg:flex-row items-center gap-12 mb-20 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''
                                    }`}
                            >
                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex items-center gap-4 mb-6">
                                        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold">
                                            {step.step}
                                        </div>
                                        <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600">
                                            {step.icon}
                                        </div>
                                    </div>
                                    <h3 className="text-3xl font-bold text-gray-900 mb-4">
                                        {step.title}
                                    </h3>
                                    <p className="text-xl text-gray-600 mb-6 leading-relaxed">
                                        {step.description}
                                    </p>
                                    <ul className="space-y-3">
                                        {step.details.map((detail, detailIndex) => (
                                            <li key={detailIndex} className="flex items-center gap-3">
                                                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                                                <span className="text-gray-700">{detail}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>

                                {/* Visual */}
                                <div className="flex-1">
                                    <div className="glass-card p-8 rounded-2xl bg-gradient-to-br from-blue-50 to-purple-50">
                                        <div className="aspect-video bg-gradient-to-br from-blue-200 to-purple-200 rounded-xl flex items-center justify-center">
                                            <div className="text-center">
                                                <div className="bg-white p-4 rounded-full mb-4 inline-block">
                                                    {step.icon}
                                                </div>
                                                <p className="text-gray-600 font-medium">Step {step.step} Visual</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Benefits Section */}
            <section className="py-20 bg-gradient-to-r from-blue-50 to-purple-50">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl font-bold text-gray-900 mb-6">
                            Why Our Process Works
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Our streamlined approach delivers measurable results for job seekers
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-6xl mx-auto">
                        {benefits.map((benefit, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                viewport={{ once: true }}
                                className="glass-card p-6 rounded-xl text-center"
                            >
                                <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600 inline-block mb-4">
                                    {benefit.icon}
                                </div>
                                <h3 className="text-lg font-bold text-gray-900 mb-3">
                                    {benefit.title}
                                </h3>
                                <p className="text-gray-600 text-sm leading-relaxed">
                                    {benefit.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="container mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
                            Ready to Get Started?
                        </h2>
                        <p className="text-xl text-blue-100 mb-12 max-w-3xl mx-auto">
                            Join thousands of professionals who have streamlined their job search with our AI-powered platform
                        </p>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all duration-200 flex items-center justify-center gap-2 mx-auto shadow-lg hover:shadow-xl"
                        >
                            Start Your Journey Now
                            <ArrowRight className="w-5 h-5" />
                        </motion.button>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default HowItWorksPage;
