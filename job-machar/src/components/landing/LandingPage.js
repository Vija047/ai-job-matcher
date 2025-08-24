'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../auth/AuthContext';
import Image from 'next/image';
import {
    ArrowRight,
    Zap,
    Target,
    Users,
    CheckCircle,
    Star,
    Sparkles,
    TrendingUp,
    Shield,
    Clock,
    Award,
    ChevronRight
} from 'lucide-react';

const LandingPage = ({ onGetStarted }) => {
    const { isAuthenticated } = useAuth();

    const features = [
        {
            icon: <Zap className="w-8 h-8" />,
            title: "AI-Powered Matching",
            description: "Advanced algorithms analyze your skills and match you with perfect job opportunities."
        },
        {
            icon: <Target className="w-8 h-8" />,
            title: "Precision Targeting",
            description: "Get highly targeted job recommendations based on your experience and career goals."
        },
        {
            icon: <TrendingUp className="w-8 h-8" />,
            title: "Career Growth",
            description: "Track your progress and get insights on skills to develop for career advancement."
        },
        {
            icon: <Shield className="w-8 h-8" />,
            title: "Privacy First",
            description: "Your data is secure and private. We never share your information without consent."
        }
    ];

    const testimonials = [
        {
            name: "Sarah Johnson",
            role: "Software Engineer",
            company: "TechCorp",
            image: "https://images.unsplash.com/photo-1494790108755-2616b612b5b0?w=150&h=150&fit=crop&crop=face",
            content: "Found my dream job in just 2 weeks! The AI matching is incredibly accurate."
        },
        {
            name: "Michael Chen",
            role: "Product Manager",
            company: "InnovateLab",
            image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            content: "The platform helped me transition to a new industry seamlessly. Highly recommend!"
        },
        {
            name: "Emily Rodriguez",
            role: "Data Scientist",
            company: "DataFlow",
            image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
            content: "Best job search platform I've used. The recommendations were spot-on!"
        }
    ];

    const stats = [
        { number: "50K+", label: "Jobs Matched" },
        { number: "10K+", label: "Happy Users" },
        { number: "95%", label: "Success Rate" },
        { number: "24/7", label: "Support" }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400/10 via-purple-400/5 to-cyan-400/10"></div>
            <div className="absolute top-0 left-0 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float"></div>
            <div className="absolute top-0 right-0 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>

            {/* Hero Section */}
            <section className="relative z-10 pt-20 pb-32">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        className="text-center max-w-5xl mx-auto"
                    >
                        <div className="flex justify-center mb-6">
                            <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-full text-sm font-medium text-blue-700 border border-blue-200">
                                <Sparkles className="w-4 h-4" />
                                AI-Powered Job Matching Platform
                            </div>
                        </div>

                        <h1 className="text-5xl lg:text-7xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-600 bg-clip-text text-transparent mb-8 leading-tight">
                            Find Your Perfect
                            <br />
                            <span className="relative">
                                Dream Job
                                <motion.div
                                    className="absolute -bottom-2 left-0 right-0 h-3 bg-gradient-to-r from-yellow-200 to-orange-200 rounded-full opacity-60"
                                    initial={{ scaleX: 0 }}
                                    animate={{ scaleX: 1 }}
                                    transition={{ delay: 1, duration: 0.8 }}
                                />
                            </span>
                        </h1>

                        <p className="text-xl lg:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
                            Leverage the power of AI to match your skills with the perfect job opportunities.
                            Upload your resume and let our intelligent system do the rest.
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
                            <motion.button
                                onClick={onGetStarted}
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
                            >
                                Get Started Free
                                <ArrowRight className="w-5 h-5" />
                            </motion.button>

                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-gray-400 hover:bg-gray-50 transition-all duration-200 flex items-center justify-center gap-2"
                            >
                                Watch Demo
                                <Sparkles className="w-5 h-5" />
                            </motion.button>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
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

            {/* Features Section */}
            <section className="relative z-10 py-20">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
                            Why Choose Our Platform?
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Experience the future of job searching with our cutting-edge AI technology
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
                        {features.map((feature, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                viewport={{ once: true }}
                                className="glass-card p-8 rounded-2xl hover:shadow-xl transition-all duration-300 group"
                            >
                                <div className="flex items-start gap-4">
                                    <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600 group-hover:scale-110 transition-transform duration-300">
                                        {feature.icon}
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-gray-900 mb-3">
                                            {feature.title}
                                        </h3>
                                        <p className="text-gray-600 leading-relaxed">
                                            {feature.description}
                                        </p>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="relative z-10 py-20 bg-gradient-to-r from-blue-50 to-purple-50">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
                            How It Works
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Get matched with your dream job in just three simple steps
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
                        {[
                            {
                                step: "01",
                                title: "Upload Resume",
                                description: "Simply upload your resume and let our AI analyze your skills, experience, and career preferences."
                            },
                            {
                                step: "02",
                                title: "AI Analysis",
                                description: "Our advanced algorithms process your information and match you with relevant job opportunities."
                            },
                            {
                                step: "03",
                                title: "Get Matched",
                                description: "Receive personalized job recommendations and apply to positions that truly fit your profile."
                            }
                        ].map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.2, duration: 0.6 }}
                                viewport={{ once: true }}
                                className="text-center relative"
                            >
                                {index < 2 && (
                                    <div className="hidden lg:block absolute top-16 -right-4 text-gray-300">
                                        <ChevronRight className="w-8 h-8" />
                                    </div>
                                )}
                                <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-6">
                                    {step.step}
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-4">
                                    {step.title}
                                </h3>
                                <p className="text-gray-600 leading-relaxed">
                                    {step.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials Section */}
            <section className="relative z-10 py-20">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
                            Success Stories
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Join thousands of professionals who found their dream jobs through our platform
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
                        {testimonials.map((testimonial, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                viewport={{ once: true }}
                                className="glass-card p-8 rounded-2xl"
                            >
                                <div className="flex items-center gap-1 mb-4">
                                    {[...Array(5)].map((_, i) => (
                                        <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                                    ))}
                                </div>
                                <p className="text-gray-600 mb-6 leading-relaxed">
                                    &quot;{testimonial.content}&quot;
                                </p>
                                <div className="flex items-center gap-4">
                                    <Image
                                        src={testimonial.image}
                                        alt={testimonial.name}
                                        width={48}
                                        height={48}
                                        className="w-12 h-12 rounded-full object-cover"
                                    />
                                    <div>
                                        <div className="font-semibold text-gray-900">
                                            {testimonial.name}
                                        </div>
                                        <div className="text-sm text-gray-600">
                                            {testimonial.role} at {testimonial.company}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="relative z-10 py-20 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="container mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
                            Ready to Find Your Dream Job?
                        </h2>
                        <p className="text-xl text-blue-100 mb-12 max-w-3xl mx-auto">
                            Join thousands of professionals who have already found their perfect career match
                        </p>
                        <motion.button
                            onClick={onGetStarted}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-white text-blue-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all duration-200 flex items-center justify-center gap-2 mx-auto shadow-lg hover:shadow-xl"
                        >
                            Start Your Journey Today
                            <ArrowRight className="w-5 h-5" />
                        </motion.button>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;
