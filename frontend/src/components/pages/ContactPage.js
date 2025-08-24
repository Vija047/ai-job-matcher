'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Mail,
    Phone,
    MapPin,
    Send,
    MessageCircle,
    Clock,
    CheckCircle,
    ArrowRight,
    Linkedin,
    Twitter,
    Github
} from 'lucide-react';

const ContactPage = () => {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        subject: '',
        message: '',
        inquiryType: 'general'
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isSubmitted, setIsSubmitted] = useState(false);

    const contactInfo = [
        {
            icon: <Mail className="w-6 h-6" />,
            title: "Email Us",
            content: "support@aijobmatcher.com",
            description: "Get a response within 24 hours"
        },
        {
            icon: <Phone className="w-6 h-6" />,
            title: "Call Us",
            content: "+1 (555) 123-4567",
            description: "Mon-Fri, 9AM-6PM EST"
        },
        {
            icon: <MapPin className="w-6 h-6" />,
            title: "Visit Us",
            content: "123 Innovation Drive, Tech City, TC 12345",
            description: "Our headquarters"
        },
        {
            icon: <MessageCircle className="w-6 h-6" />,
            title: "Live Chat",
            content: "Available on our platform",
            description: "Instant support during business hours"
        }
    ];

    const inquiryTypes = [
        { value: 'general', label: 'General Inquiry' },
        { value: 'support', label: 'Technical Support' },
        { value: 'partnership', label: 'Partnership Opportunities' },
        { value: 'feedback', label: 'Feedback & Suggestions' },
        { value: 'media', label: 'Media & Press' }
    ];

    const faqs = [
        {
            question: "How does the AI job matching work?",
            answer: "Our AI analyzes your resume, skills, and preferences to match you with relevant job opportunities using advanced machine learning algorithms."
        },
        {
            question: "Is the service free to use?",
            answer: "Yes! Our basic job matching service is completely free. We also offer premium features for enhanced functionality."
        },
        {
            question: "How long does it take to get job matches?",
            answer: "You'll receive your first job matches within minutes of uploading your resume. Our system works in real-time."
        },
        {
            question: "Can I apply to jobs directly through the platform?",
            answer: "Absolutely! You can apply to jobs with one click directly through our platform, and we'll track your application status."
        }
    ];

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Simulate form submission
        setTimeout(() => {
            setIsSubmitting(false);
            setIsSubmitted(true);
        }, 2000);
    };

    if (isSubmitted) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
                <motion.div
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8 }}
                    className="text-center max-w-2xl mx-auto px-6"
                >
                    <div className="bg-green-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-8">
                        <CheckCircle className="w-12 h-12 text-green-500" />
                    </div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-6">
                        Message Sent Successfully!
                    </h1>
                    <p className="text-xl text-gray-600 mb-8">
                        Thank you for reaching out. We&apos;ve received your message and will get back to you within 24 hours.
                    </p>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setIsSubmitted(false)}
                        className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2 mx-auto"
                    >
                        Send Another Message
                        <ArrowRight className="w-5 h-5" />
                    </motion.button>
                </motion.div>
            </div>
        );
    }

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
                            Get in Touch
                        </h1>
                        <p className="text-xl text-gray-600 mb-12 leading-relaxed">
                            Have questions about our AI job matching platform? We&apos;re here to help!
                            Reach out to us and we&apos;ll get back to you as soon as possible.
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Contact Info Cards */}
            <section className="py-12">
                <div className="container mx-auto px-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
                        {contactInfo.map((info, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1, duration: 0.6 }}
                                className="glass-card p-6 rounded-xl text-center hover:shadow-lg transition-all duration-300"
                            >
                                <div className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600 inline-block mb-4">
                                    {info.icon}
                                </div>
                                <h3 className="text-lg font-bold text-gray-900 mb-2">
                                    {info.title}
                                </h3>
                                <p className="text-blue-600 font-medium mb-2">
                                    {info.content}
                                </p>
                                <p className="text-sm text-gray-600">
                                    {info.description}
                                </p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Contact Form & FAQ */}
            <section className="py-20">
                <div className="container mx-auto px-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 max-w-7xl mx-auto">
                        {/* Contact Form */}
                        <motion.div
                            initial={{ opacity: 0, x: -30 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8, delay: 0.2 }}
                        >
                            <div className="glass-card p-8 rounded-2xl">
                                <h2 className="text-3xl font-bold text-gray-900 mb-6">
                                    Send us a Message
                                </h2>
                                <form onSubmit={handleSubmit} className="space-y-6">
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                Your Name
                                            </label>
                                            <input
                                                type="text"
                                                name="name"
                                                value={formData.name}
                                                onChange={handleInputChange}
                                                required
                                                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                                                placeholder="John Doe"
                                            />
                                        </div>
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                                Email Address
                                            </label>
                                            <input
                                                type="email"
                                                name="email"
                                                value={formData.email}
                                                onChange={handleInputChange}
                                                required
                                                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                                                placeholder="john@example.com"
                                            />
                                        </div>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Inquiry Type
                                        </label>
                                        <select
                                            name="inquiryType"
                                            value={formData.inquiryType}
                                            onChange={handleInputChange}
                                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                                        >
                                            {inquiryTypes.map((type) => (
                                                <option key={type.value} value={type.value}>
                                                    {type.label}
                                                </option>
                                            ))}
                                        </select>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Subject
                                        </label>
                                        <input
                                            type="text"
                                            name="subject"
                                            value={formData.subject}
                                            onChange={handleInputChange}
                                            required
                                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                                            placeholder="How can we help you?"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-2">
                                            Message
                                        </label>
                                        <textarea
                                            name="message"
                                            value={formData.message}
                                            onChange={handleInputChange}
                                            required
                                            rows={6}
                                            className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none"
                                            placeholder="Tell us more about your inquiry..."
                                        ></textarea>
                                    </div>

                                    <motion.button
                                        type="submit"
                                        disabled={isSubmitting}
                                        whileHover={{ scale: 1.02 }}
                                        whileTap={{ scale: 0.98 }}
                                        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        {isSubmitting ? (
                                            <div className="flex items-center gap-2">
                                                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                                Sending...
                                            </div>
                                        ) : (
                                            <>
                                                Send Message
                                                <Send className="w-5 h-5" />
                                            </>
                                        )}
                                    </motion.button>
                                </form>
                            </div>
                        </motion.div>

                        {/* FAQ Section */}
                        <motion.div
                            initial={{ opacity: 0, x: 30 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8, delay: 0.4 }}
                        >
                            <h2 className="text-3xl font-bold text-gray-900 mb-8">
                                Frequently Asked Questions
                            </h2>
                            <div className="space-y-6">
                                {faqs.map((faq, index) => (
                                    <motion.div
                                        key={index}
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: 0.1 * index, duration: 0.6 }}
                                        className="glass-card p-6 rounded-xl"
                                    >
                                        <h3 className="text-lg font-bold text-gray-900 mb-3">
                                            {faq.question}
                                        </h3>
                                        <p className="text-gray-600 leading-relaxed">
                                            {faq.answer}
                                        </p>
                                    </motion.div>
                                ))}
                            </div>

                            {/* Social Links */}
                            <div className="mt-12">
                                <h3 className="text-xl font-bold text-gray-900 mb-6">
                                    Follow Us
                                </h3>
                                <div className="flex gap-4">
                                    {[
                                        { icon: <Linkedin className="w-6 h-6" />, name: "LinkedIn" },
                                        { icon: <Twitter className="w-6 h-6" />, name: "Twitter" },
                                        { icon: <Github className="w-6 h-6" />, name: "GitHub" }
                                    ].map((social, index) => (
                                        <motion.a
                                            key={index}
                                            href="#"
                                            whileHover={{ scale: 1.1 }}
                                            whileTap={{ scale: 0.9 }}
                                            className="bg-gradient-to-r from-blue-100 to-purple-100 p-3 rounded-xl text-blue-600 hover:from-blue-200 hover:to-purple-200 transition-all duration-200"
                                        >
                                            {social.icon}
                                        </motion.a>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            {/* Response Time Section */}
            <section className="py-16 bg-gradient-to-r from-blue-600 to-purple-600">
                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center text-white max-w-4xl mx-auto"
                    >
                        <Clock className="w-16 h-16 mx-auto mb-6 text-blue-200" />
                        <h2 className="text-3xl lg:text-4xl font-bold mb-6">
                            Quick Response Guaranteed
                        </h2>
                        <p className="text-xl text-blue-100 mb-8">
                            We typically respond to all inquiries within 24 hours. For urgent matters,
                            please use our live chat feature for immediate assistance.
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
                            <div className="text-center">
                                <div className="text-2xl font-bold text-blue-200 mb-2">&lt; 1 hour</div>
                                <div className="text-blue-100">Live Chat Response</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-blue-200 mb-2">&lt; 24 hours</div>
                                <div className="text-blue-100">Email Response</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-blue-200 mb-2">Same Day</div>
                                <div className="text-blue-100">Phone Call Back</div>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </section>
        </div>
    );
};

export default ContactPage;
