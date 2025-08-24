'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../auth/AuthContext';
import { User, Mail, Phone, Building, Lock, Save, ArrowLeft } from 'lucide-react';

const SettingsPage = ({ onBack }) => {
    const { user } = useAuth();
    const [formData, setFormData] = useState({
        firstName: user?.firstName || '',
        lastName: user?.lastName || '',
        email: user?.email || '',
        phone: user?.phone || '',
        company: user?.company || ''
    });
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSave = async () => {
        setLoading(true);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        setLoading(false);
        setIsEditing(false);
        // In production, update user data via API
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-2xl mx-auto"
        >
            <div className="glass-card p-8 rounded-2xl">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <button
                        onClick={onBack}
                        className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        Account Settings
                    </h1>
                </div>

                {/* Profile Section */}
                <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* First Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                First Name
                            </label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                                <input
                                    type="text"
                                    name="firstName"
                                    value={formData.firstName}
                                    onChange={handleChange}
                                    disabled={!isEditing}
                                    className={`w-full pl-12 pr-4 py-3 border rounded-lg transition-all ${isEditing
                                            ? 'border-blue-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                                            : 'border-gray-200 bg-gray-50'
                                        }`}
                                />
                            </div>
                        </div>

                        {/* Last Name */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Last Name
                            </label>
                            <div className="relative">
                                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                                <input
                                    type="text"
                                    name="lastName"
                                    value={formData.lastName}
                                    onChange={handleChange}
                                    disabled={!isEditing}
                                    className={`w-full pl-12 pr-4 py-3 border rounded-lg transition-all ${isEditing
                                            ? 'border-blue-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                                            : 'border-gray-200 bg-gray-50'
                                        }`}
                                />
                            </div>
                        </div>
                    </div>

                    {/* Email */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email Address
                        </label>
                        <div className="relative">
                            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                disabled={true} // Email should not be editable
                                className="w-full pl-12 pr-4 py-3 border border-gray-200 bg-gray-50 rounded-lg"
                            />
                        </div>
                        <p className="text-sm text-gray-500 mt-1">
                            Email cannot be changed for security reasons
                        </p>
                    </div>

                    {/* Phone */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Phone Number
                        </label>
                        <div className="relative">
                            <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                            <input
                                type="tel"
                                name="phone"
                                value={formData.phone}
                                onChange={handleChange}
                                disabled={!isEditing}
                                className={`w-full pl-12 pr-4 py-3 border rounded-lg transition-all ${isEditing
                                        ? 'border-blue-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                                        : 'border-gray-200 bg-gray-50'
                                    }`}
                                placeholder="Enter your phone number"
                            />
                        </div>
                    </div>

                    {/* Company */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Company
                        </label>
                        <div className="relative">
                            <Building className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                            <input
                                type="text"
                                name="company"
                                value={formData.company}
                                onChange={handleChange}
                                disabled={!isEditing}
                                className={`w-full pl-12 pr-4 py-3 border rounded-lg transition-all ${isEditing
                                        ? 'border-blue-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent'
                                        : 'border-gray-200 bg-gray-50'
                                    }`}
                                placeholder="Enter your company"
                            />
                        </div>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
                    <button className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium transition-colors">
                        <Lock className="w-4 h-4" />
                        Change Password
                    </button>

                    <div className="flex gap-3">
                        {isEditing ? (
                            <>
                                <button
                                    onClick={() => setIsEditing(false)}
                                    className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={handleSave}
                                    disabled={loading}
                                    className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center gap-2 disabled:opacity-50"
                                >
                                    <Save className="w-4 h-4" />
                                    {loading ? 'Saving...' : 'Save Changes'}
                                </button>
                            </>
                        ) : (
                            <button
                                onClick={() => setIsEditing(true)}
                                className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200"
                            >
                                Edit Profile
                            </button>
                        )}
                    </div>
                </div>
            </div>

            {/* Account Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
                <div className="glass-card p-6 rounded-xl text-center">
                    <div className="text-2xl font-bold text-blue-600 mb-2">12</div>
                    <div className="text-gray-600">Applications Sent</div>
                </div>
                <div className="glass-card p-6 rounded-xl text-center">
                    <div className="text-2xl font-bold text-green-600 mb-2">3</div>
                    <div className="text-gray-600">Interviews Scheduled</div>
                </div>
                <div className="glass-card p-6 rounded-xl text-center">
                    <div className="text-2xl font-bold text-purple-600 mb-2">85%</div>
                    <div className="text-gray-600">Profile Match Score</div>
                </div>
            </div>
        </motion.div>
    );
};

export default SettingsPage;
