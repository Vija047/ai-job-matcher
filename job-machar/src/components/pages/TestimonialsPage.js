'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Star, Quote, ArrowRight, TrendingUp, Award, Users } from 'lucide-react';
import Image from 'next/image';

const TestimonialsPage = () => {
    const testimonials = [
        {
            id: 1,
            name: "Sarah Johnson",
            role: "Software Engineer",
            company: "TechCorp",
            content: "This platform completely transformed my job search. The AI recommendations were spot-on, and I landed my dream job within 3 weeks!",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "Software Development",
            timeToJob: "3 weeks",
            salaryIncrease: "40%"
        },
        {
            id: 2,
            name: "Michael Chen",
            role: "Data Scientist",
            company: "DataFlow Inc",
            content: "The skill analysis was incredibly accurate. It helped me identify gaps in my knowledge and provided targeted job suggestions that matched my career goals perfectly.",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "Data Science",
            timeToJob: "2 weeks",
            salaryIncrease: "55%"
        },
        {
            id: 3,
            name: "Emily Rodriguez",
            role: "Product Manager",
            company: "InnovateLab",
            content: "I was amazed by how well the platform understood my career aspirations. The personalized recommendations saved me countless hours of searching.",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "Product Management",
            timeToJob: "1 month",
            salaryIncrease: "30%"
        },
        {
            id: 4,
            name: "David Thompson",
            role: "UX Designer",
            company: "DesignStudio",
            content: "The quality of job matches was exceptional. Every recommendation felt hand-picked for my specific skills and experience level.",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "Design",
            timeToJob: "3 weeks",
            salaryIncrease: "35%"
        },
        {
            id: 5,
            name: "Lisa Wang",
            role: "Marketing Director",
            company: "GrowthTech",
            content: "The platform's insights into market trends and salary expectations helped me negotiate a much better offer than I initially thought possible.",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "Marketing",
            timeToJob: "2 weeks",
            salaryIncrease: "45%"
        },
        {
            id: 6,
            name: "James Wilson",
            role: "DevOps Engineer",
            company: "CloudSystems",
            content: "Outstanding experience! The AI understood my technical background perfectly and connected me with companies that valued my specific skill set.",
            rating: 5,
            image: "/api/placeholder/64/64",
            category: "DevOps",
            timeToJob: "1 week",
            salaryIncrease: "50%"
        }
    ];

    const stats = [
        { number: "50K+", label: "Success Stories", icon: <Users className="w-6 h-6" /> },
        { number: "94%", label: "User Satisfaction", icon: <Star className="w-6 h-6" /> },
        { number: "3.2x", label: "Faster Job Search", icon: <TrendingUp className="w-6 h-6" /> },
        { number: "98%", label: "Would Recommend", icon: <Award className="w-6 h-6" /> }
    ];

    const categories = [
        "All",
        "Software Development",
        "Data Science",
        "Product Management",
        "Design",
        "Marketing",
        "DevOps"
    ];

    const [selectedCategory, setSelectedCategory] = useState("All");

    const filteredTestimonials = selectedCategory === "All"
        ? testimonials
        : testimonials.filter(t => t.category === selectedCategory);

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
                            Success Stories
                        </h1>
                        <p className="text-xl text-gray-600 mb-12 leading-relaxed">
                            Join thousands of professionals who have transformed their careers with our AI-powered job matching platform.
                            Read their inspiring success stories and see how we can help you too.
                        </p>

                        {/* Stats */}
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
                            {stats.map((stat, index) => (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.2 + index * 0.1, duration: 0.6 }}
                                    className="text-center glass-card p-6 rounded-xl"
                                >
                                    <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600 inline-block mb-3">
                                        {stat.icon}
                                    </div>
                                    <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                                        {stat.number}
                                    </div>
                                    <div className="text-gray-600 font-medium text-sm">{stat.label}</div>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Category Filter */}
            <section className="py-8 bg-white">
                <div className="container mx-auto px-6">
                    <div className="flex flex-wrap justify-center gap-4">
                        {categories.map((category, index) => (
                            <motion.button
                                key={category}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                onClick={() => setSelectedCategory(category)}
                                className={`px-6 py-3 rounded-full font-medium transition-all duration-200 ${selectedCategory === category
                                        ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                    }`}
                            >
                                {category}
                            </motion.button>
                        ))}
                    </div>
                </div>
            </section>

            {/* Testimonials Grid */}
            <section className="py-20">
                <div className="container mx-auto px-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                        {filteredTestimonials.map((testimonial, index) => (
                            <motion.div
                                key={testimonial.id}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                className="glass-card p-8 rounded-2xl hover:shadow-xl transition-all duration-300 relative"
                            >
                                {/* Quote Icon */}
                                <div className="absolute top-6 right-6 text-blue-200">
                                    <Quote className="w-8 h-8" />
                                </div>

                                {/* Rating */}
                                <div className="flex items-center gap-1 mb-4">
                                    {[...Array(testimonial.rating)].map((_, i) => (
                                        <Star key={i} className="w-5 h-5 fill-yellow-400 text-yellow-400" />
                                    ))}
                                </div>

                                {/* Content */}
                                <p className="text-gray-600 mb-6 leading-relaxed italic">
                                    &quot;{testimonial.content}&quot;
                                </p>

                                {/* Success Metrics */}
                                <div className="grid grid-cols-2 gap-4 mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
                                    <div className="text-center">
                                        <div className="text-lg font-bold text-blue-600">{testimonial.timeToJob}</div>
                                        <div className="text-xs text-gray-600">Time to Job</div>
                                    </div>
                                    <div className="text-center">
                                        <div className="text-lg font-bold text-green-600">+{testimonial.salaryIncrease}</div>
                                        <div className="text-xs text-gray-600">Salary Increase</div>
                                    </div>
                                </div>

                                {/* User Info */}
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 bg-gradient-to-r from-blue-200 to-purple-200 rounded-full flex items-center justify-center">
                                        <span className="text-blue-600 font-bold text-lg">
                                            {testimonial.name.charAt(0)}
                                        </span>
                                    </div>
                                    <div>
                                        <div className="font-semibold text-gray-900">
                                            {testimonial.name}
                                        </div>
                                        <div className="text-sm text-gray-600">
                                            {testimonial.role} at {testimonial.company}
                                        </div>
                                        <div className="text-xs text-blue-600 font-medium">
                                            {testimonial.category}
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Featured Testimonial */}
            <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="max-w-4xl mx-auto text-center text-white"
                    >
                        <Quote className="w-16 h-16 mx-auto mb-8 text-blue-200" />
                        <p className="text-2xl lg:text-3xl font-light mb-8 leading-relaxed italic">
                            &quot;The AI job matching was so accurate, it felt like having a personal career advisor who knew exactly what I was looking for. I got multiple offers within two weeks!&quot;
                        </p>
                        <div className="flex items-center justify-center gap-4">
                            <div className="w-16 h-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                                <span className="text-white font-bold text-xl">A</span>
                            </div>
                            <div className="text-left">
                                <div className="text-xl font-bold">Alex Martinez</div>
                                <div className="text-blue-200">Senior Full Stack Developer at TechGiant</div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20">
                <div className="container mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                    >
                        <h2 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6">
                            Ready to Write Your Success Story?
                        </h2>
                        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
                            Join the thousands of professionals who have already transformed their careers with our platform
                        </p>
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2 mx-auto"
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

export default TestimonialsPage;
