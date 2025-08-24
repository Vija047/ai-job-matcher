'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Brain,
    Briefcase,
    TrendingUp,
    Users,
    Clock,
    MapPin,
    Star,
    Download,
    ExternalLink,
    Bot,
    Zap,
    Target,
    BookOpen,
    Award
} from 'lucide-react';
import toast from 'react-hot-toast';
import ResumeScore from './ResumeScore';
import ResumeScoreBoard from './ResumeScoreBoard';
import {
    getEnhancedRecommendations,
    getRealTimeJobs,
    getSkillGapAnalysis,
    getCareerGuidance,
    generateCoverLetter,
    applyToJob,
    getApplicationHistory
} from '../../utils/api';

export default function EnhancedDashboard({ resumeAnalysis, analysisId }) {
    const [activeTab, setActiveTab] = useState('recommendations');
    const [recommendations, setRecommendations] = useState(null);
    const [realTimeJobs, setRealTimeJobs] = useState([]);
    const [skillGaps, setSkillGaps] = useState(null);
    const [careerPaths, setCareerPaths] = useState([]);
    const [applicationHistory, setApplicationHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [preferences, setPreferences] = useState({
        location: '',
        salary_min: '',
        job_type: 'Full Time',
        remote_preference: false
    });

    useEffect(() => {
        if (analysisId) {
            loadDashboardData();
        } else {
            // Create mock recommendations for demo purposes immediately
            setLoading(true);
            setTimeout(() => {
                createMockRecommendations();
                setLoading(false);
            }, 1000); // Small delay to show loading state
        }
    }, [analysisId]); // eslint-disable-line react-hooks/exhaustive-deps

    const createMockRecommendations = () => {
        const mockJobs = [
            {
                id: 'mock-1',
                title: 'Senior Software Engineer',
                company: 'TechCorp Inc.',
                location: 'San Francisco, CA',
                description: 'Join our engineering team to build scalable web applications using React, Node.js, and cloud technologies. We\'re looking for experienced developers who can work in a fast-paced environment.',
                requirements: 'React, Node.js, JavaScript, Python, AWS',
                salary_min: 120000,
                salary_max: 180000,
                salary_currency: '$',
                experience_level: 'Senior',
                employment_type: 'Full Time',
                posted_date: new Date().toISOString(),
                source: 'Demo',
                apply_url: 'https://example.com/apply',
                skills: ['React', 'Node.js', 'JavaScript', 'Python', 'AWS', 'MongoDB'],
                remote_allowed: true,
                compatibility_score: 0.92,
                matched_role: 'Software Engineer',
                match_type: 'primary'
            },
            {
                id: 'mock-2',
                title: 'Full Stack Developer',
                company: 'StartupXYZ',
                location: 'New York, NY',
                description: 'We\'re seeking a versatile full-stack developer to help build our next-generation platform. Experience with modern web technologies is essential.',
                requirements: 'JavaScript, React, Python, PostgreSQL',
                salary_min: 90000,
                salary_max: 130000,
                salary_currency: '$',
                experience_level: 'Mid-Level',
                employment_type: 'Full Time',
                posted_date: new Date().toISOString(),
                source: 'Demo',
                apply_url: 'https://example.com/apply',
                skills: ['JavaScript', 'React', 'Python', 'PostgreSQL', 'Git'],
                remote_allowed: false,
                compatibility_score: 0.85,
                matched_role: 'Full Stack Developer',
                match_type: 'primary'
            },
            {
                id: 'mock-3',
                title: 'Cloud Solutions Architect',
                company: 'CloudTech Solutions',
                location: 'Austin, TX',
                description: 'Design and implement cloud infrastructure solutions for our enterprise clients. AWS and DevOps experience required.',
                requirements: 'AWS, Docker, Kubernetes, Python, Terraform',
                salary_min: 140000,
                salary_max: 200000,
                salary_currency: '$',
                experience_level: 'Senior',
                employment_type: 'Full Time',
                posted_date: new Date().toISOString(),
                source: 'Demo',
                apply_url: 'https://example.com/apply',
                skills: ['AWS', 'Docker', 'Kubernetes', 'Python', 'Terraform', 'CI/CD'],
                remote_allowed: true,
                compatibility_score: 0.78,
                matched_role: 'Cloud Architect',
                match_type: 'alternative'
            }
        ];

        const mockInternships = [
            {
                id: 'intern-1',
                title: 'Software Engineering Intern',
                company: 'Microsoft',
                location: 'Seattle, WA',
                description: 'Join our summer internship program and work on real projects that impact millions of users worldwide. Perfect for computer science students.',
                requirements: 'Python, JavaScript, Java, or C# experience',
                salary_min: 6000,
                salary_max: 8000,
                salary_currency: '$',
                experience_level: 'Entry',
                employment_type: 'Internship',
                posted_date: new Date().toISOString(),
                source: 'Demo',
                apply_url: 'https://example.com/apply/intern1',
                skills: ['Python', 'JavaScript', 'Git', 'Agile'],
                remote_allowed: false,
                compatibility_score: 0.75,
                matched_role: 'Software Engineer',
                match_type: 'internship',
                job_type: 'Internship'
            },
            {
                id: 'intern-2',
                title: 'Frontend Development Intern',
                company: 'Google',
                location: 'Mountain View, CA',
                description: 'Work with our UX team to create beautiful, responsive web applications. Great opportunity for students interested in frontend development.',
                requirements: 'React, JavaScript, HTML, CSS, TypeScript',
                salary_min: 7000,
                salary_max: 9000,
                salary_currency: '$',
                experience_level: 'Entry',
                employment_type: 'Internship',
                posted_date: new Date().toISOString(),
                source: 'Demo',
                apply_url: 'https://example.com/apply/intern2',
                skills: ['React', 'JavaScript', 'HTML', 'CSS', 'TypeScript'],
                remote_allowed: true,
                compatibility_score: 0.68,
                matched_role: 'Frontend Developer',
                match_type: 'internship',
                job_type: 'Internship'
            }
        ];

        // Mock role analysis
        const mockRoleAnalysis = {
            primary_role: 'Full Stack Developer',
            alternative_roles: ['Software Engineer', 'Frontend Developer', 'Backend Developer'],
            career_stage: 'mid_career',
            experience_level: 'mid',
            years_experience: 3,
            suitable_for_internships: false,
            skill_match_strength: 'strong',
            recommended_job_types: ['Full Time', 'Contract', 'Remote'],
            growth_potential: 'high'
        };

        setRecommendations({
            success: true,
            recommendations: mockJobs,
            internships: mockInternships,
            role_analysis: mockRoleAnalysis,
            total_found: mockJobs.length,
            total_internships_found: mockInternships.length,
            categories: {
                primary_role_matches: 2,
                alternative_role_matches: 1,
                skill_based_matches: 0
            },
            metadata: {
                search_timestamp: new Date().toISOString(),
                primary_role: 'Full Stack Developer',
                career_stage: 'mid_career',
                includes_internships: false
            }
        });

        toast.success('Demo recommendations loaded! Shows role-based job and internship matching.');
    };

    const loadDashboardData = async () => {
        setLoading(true);
        try {
            // Load all data in parallel with individual error handling
            const [recsData, skillsData, careerData, historyData] = await Promise.allSettled([
                getEnhancedRecommendations(analysisId, preferences, 20),
                getSkillGapAnalysis(analysisId),
                getCareerGuidance(analysisId),
                getApplicationHistory()
            ]);

            // Handle recommendations data
            if (recsData.status === 'fulfilled') {
                setRecommendations(recsData.value);
            } else {
                console.error('Failed to load recommendations:', recsData.reason);
                setRecommendations(null);
            }

            // Handle skills data
            if (skillsData.status === 'fulfilled') {
                setSkillGaps(skillsData.value);
            } else {
                console.error('Failed to load skill gaps:', skillsData.reason);
                setSkillGaps(null);
            }

            // Handle career data
            if (careerData.status === 'fulfilled') {
                setCareerPaths(careerData.value?.career_paths || []);
            } else {
                console.error('Failed to load career paths:', careerData.reason);
                setCareerPaths([]);
            }

            // Handle application history
            if (historyData.status === 'fulfilled') {
                setApplicationHistory(historyData.value?.application_history || []);
            } else {
                console.error('Failed to load application history:', historyData.reason);
                setApplicationHistory([]);
            }

            // Load real-time jobs based on user skills
            try {
                const userSkills = extractUserSkills(resumeAnalysis);
                if (userSkills.length > 0) {
                    const jobsData = await getRealTimeJobs(userSkills.slice(0, 3));
                    setRealTimeJobs(jobsData?.jobs || []);
                } else {
                    setRealTimeJobs([]);
                }
            } catch (error) {
                console.error('Failed to load real-time jobs:', error);
                setRealTimeJobs([]);
            }

        } catch (error) {
            console.error('Error loading dashboard data:', error);
            toast.error('Failed to load dashboard data. Please try refreshing the page.');
        } finally {
            setLoading(false);
        }
    };

    const extractUserSkills = (analysis) => {
        const skills = [];
        try {
            if (analysis?.skills_analysis?.skills_by_category) {
                Object.values(analysis.skills_analysis.skills_by_category).forEach(categorySkills => {
                    if (Array.isArray(categorySkills)) {
                        skills.push(...categorySkills);
                    }
                });
            }
            // Also try to extract from other possible locations
            if (analysis?.skills && Array.isArray(analysis.skills)) {
                skills.push(...analysis.skills);
            }
        } catch (error) {
            console.error('Error extracting user skills:', error);
        }
        return skills.filter(skill => skill && typeof skill === 'string');
    };

    const handleApplyToJob = async (job, applicationType = 'job') => {
        try {
            if (!job || !job.title || !job.company) {
                toast.error('Job information is incomplete');
                return;
            }

            setLoading(true);

            // Enhanced application data
            const applicationData = {
                analysis_id: analysisId,
                application_type: applicationType,
                job_details: {
                    id: job.id,
                    title: job.title,
                    company: job.company,
                    location: job.location,
                    description: job.description || '',
                    apply_url: job.apply_url || '',
                    skills: job.skills || [],
                    matched_role: job.matched_role || '',
                    compatibility_score: job.compatibility_score || 0,
                    match_type: job.match_type || 'general',
                    salary_min: job.salary_min,
                    salary_max: job.salary_max,
                    employment_type: job.employment_type || applicationType
                }
            };

            const result = await applyToJob(applicationData);

            if (result.success) {
                const jobType = applicationType === 'internship' ? 'internship' : 'job';
                toast.success(
                    `Application processed for ${job.title} at ${job.company}!`,
                    {
                        duration: 5000,
                        style: {
                            background: applicationType === 'internship' ? '#10B981' : '#3B82F6',
                            color: 'white',
                        }
                    }
                );

                // Show application assistance if available
                if (result.assistance && result.assistance.tailored_advice?.length > 0) {
                    setTimeout(() => {
                        toast(
                            <div className="text-sm">
                                <div className="font-semibold mb-2">Application Tips:</div>
                                <ul className="list-disc list-inside space-y-1">
                                    {result.assistance.tailored_advice.slice(0, 2).map((tip, idx) => (
                                        <li key={idx} className="text-xs">{tip}</li>
                                    ))}
                                </ul>
                            </div>,
                            {
                                duration: 8000,
                                style: {
                                    background: '#F3F4F6',
                                    color: '#374151',
                                    maxWidth: '400px'
                                }
                            }
                        );
                    }, 2000);
                }

                // If application URL is available, open it
                if (job.apply_url) {
                    setTimeout(() => {
                        window.open(job.apply_url, '_blank', 'noopener,noreferrer');
                    }, 1000);
                }

            } else {
                toast.error(result.error || 'Application failed');
            }

            // Refresh application history
            try {
                const historyData = await getApplicationHistory();
                setApplicationHistory(historyData.application_history || []);
            } catch (historyError) {
                console.warn('Failed to refresh application history:', historyError);
            }

        } catch (error) {
            console.error('Application error:', error);
            const errorMessage = error.message || 'Failed to process application';
            toast.error(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateCoverLetter = async (job) => {
        try {
            if (!job || !job.title || !job.company) {
                toast.error('Job information is incomplete');
                return;
            }

            setLoading(true);
            const result = await generateCoverLetter(
                analysisId,
                job.title,
                job.company,
                job.description || ''
            );

            // Create a downloadable file
            const blob = new Blob([result.cover_letter], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cover-letter-${job.company}-${job.title}.txt`;
            a.click();
            URL.revokeObjectURL(url);

            toast.success('Cover letter generated and downloaded!');
        } catch (error) {
            console.error('Cover letter generation error:', error);
            toast.error('Failed to generate cover letter');
        } finally {
            setLoading(false);
        }
    };

    const renderRecommendations = () => (
        <div className="space-y-6">
            {/* Role Analysis Section */}
            {recommendations?.role_analysis && (
                <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-200">
                    <h3 className="text-xl font-bold text-purple-900 mb-4 flex items-center">
                        <Target className="mr-2" />
                        Role Analysis
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="text-center">
                            <div className="text-lg font-bold text-purple-600">
                                {recommendations.role_analysis.primary_role || 'Not specified'}
                            </div>
                            <div className="text-sm text-purple-700">Primary Role</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-bold text-blue-600">
                                {recommendations.role_analysis.career_stage || 'Not specified'}
                            </div>
                            <div className="text-sm text-blue-700">Career Stage</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-bold text-green-600">
                                {recommendations.role_analysis.skill_match_strength || 'Unknown'}
                            </div>
                            <div className="text-sm text-green-700">Skill Strength</div>
                        </div>
                        <div className="text-center">
                            <div className="text-lg font-bold text-orange-600">
                                {recommendations.role_analysis.years_experience || 0} years
                            </div>
                            <div className="text-sm text-orange-700">Experience</div>
                        </div>
                    </div>
                    {recommendations.role_analysis.alternative_roles?.length > 0 && (
                        <div className="mt-4">
                            <h4 className="text-sm font-medium text-purple-900 mb-2">Alternative Roles:</h4>
                            <div className="flex flex-wrap gap-2">
                                {recommendations.role_analysis.alternative_roles.slice(0, 3).map((role, idx) => (
                                    <span
                                        key={idx}
                                        className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm"
                                    >
                                        {role}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Job Statistics */}
            {recommendations && (recommendations.recommendations?.length > 0 || recommendations.internships?.length > 0) && (
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                    <h3 className="text-xl font-bold text-blue-900 mb-4 flex items-center">
                        <Brain className="mr-2" />
                        AI Insights
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div className="text-center">
                            <div className="text-2xl font-bold text-blue-600">
                                {recommendations.total_found || 0}
                            </div>
                            <div className="text-sm text-blue-700">Job Matches</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-green-600">
                                {recommendations.total_internships_found || 0}
                            </div>
                            <div className="text-sm text-green-700">Internships</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-purple-600">
                                {recommendations.recommendations?.length > 0
                                    ? (recommendations.recommendations.reduce((acc, job) => acc + (job.compatibility_score || 0), 0) / recommendations.recommendations.length * 100).toFixed(1)
                                    : 0}%
                            </div>
                            <div className="text-sm text-purple-700">Average Match</div>
                        </div>
                        <div className="text-center">
                            <div className="text-2xl font-bold text-orange-600">
                                {recommendations.categories?.primary_role_matches || 0}
                            </div>
                            <div className="text-sm text-orange-700">Primary Role Matches</div>
                        </div>
                    </div>
                </div>
            )}

            {/* Internships Section */}
            {recommendations?.internships?.length > 0 && (
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-xl font-bold text-gray-900 flex items-center">
                            <BookOpen className="mr-2" />
                            Internship Opportunities
                        </h3>
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                            {recommendations.internships.length} found
                        </span>
                    </div>
                    <div className="grid gap-4">
                        {recommendations.internships.map((internship, index) => (
                            <motion.div
                                key={`internship-${index}`}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="bg-green-50 border border-green-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300"
                            >
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-2">
                                            <h3 className="text-lg font-bold text-gray-900">
                                                {internship?.title || 'Internship Title Not Available'}
                                            </h3>
                                            <span className="ml-2 bg-green-200 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                                                INTERNSHIP
                                            </span>
                                        </div>
                                        <div className="flex items-center text-gray-600 mb-2">
                                            <Briefcase className="w-4 h-4 mr-2" />
                                            {internship?.company || 'Company Not Available'}
                                            <MapPin className="w-4 h-4 ml-4 mr-2" />
                                            {internship?.location || 'Location Not Available'}
                                        </div>
                                        <div className="text-sm text-gray-500">
                                            Matched Role: {internship?.matched_role || 'General'}
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="flex items-center mb-2">
                                            <Star className="w-4 h-4 text-yellow-500 mr-1" />
                                            <span className="text-lg font-bold text-gray-900">
                                                {internship?.compatibility_score ? (internship.compatibility_score * 100).toFixed(0) : 0}%
                                            </span>
                                        </div>
                                        <div className="text-sm text-gray-500">Match Score</div>
                                    </div>
                                </div>

                                <p className="text-gray-700 mb-4 line-clamp-2">
                                    {internship?.description || 'No description available'}
                                </p>

                                <div className="flex justify-between items-center">
                                    <div className="flex flex-wrap gap-2">
                                        {internship?.skills?.slice(0, 3).map((skill, idx) => (
                                            <span
                                                key={idx}
                                                className="bg-green-100 text-green-700 px-2 py-1 rounded text-sm"
                                            >
                                                {skill}
                                            </span>
                                        )) || (
                                                <span className="text-gray-500 text-sm">No skills listed</span>
                                            )}
                                    </div>
                                    <div className="flex space-x-2">
                                        <button
                                            onClick={() => handleApplyToJob(internship, 'internship')}
                                            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm flex items-center"
                                            disabled={loading || !internship}
                                        >
                                            <Bot className="w-4 h-4 mr-2" />
                                            Apply
                                        </button>
                                        <a
                                            href={internship?.apply_url || '#'}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className={`${internship?.apply_url ? 'bg-gray-600 hover:bg-gray-700' : 'bg-gray-400 cursor-not-allowed'} text-white px-4 py-2 rounded-lg transition-colors text-sm flex items-center`}
                                            onClick={!internship?.apply_url ? (e) => e.preventDefault() : undefined}
                                        >
                                            <ExternalLink className="w-4 h-4 mr-2" />
                                            View
                                        </a>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            )}

            {/* Jobs Section */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h3 className="text-xl font-bold text-gray-900 flex items-center">
                        <Briefcase className="mr-2" />
                        Job Opportunities
                    </h3>
                    {recommendations?.recommendations?.length > 0 && (
                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                            {recommendations.recommendations.length} found
                        </span>
                    )}
                </div>
                <div className="grid gap-6">
                    {loading ? (
                        <div className="text-center py-12">
                            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
                            <p className="text-gray-600">Loading job recommendations...</p>
                        </div>
                    ) : recommendations?.recommendations?.length > 0 ? (
                        recommendations.recommendations.map((job, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-all duration-300"
                            >
                                <div className="flex justify-between items-start mb-4">
                                    <div className="flex-1">
                                        <div className="flex items-center mb-2">
                                            <h3 className="text-xl font-bold text-gray-900">
                                                {job?.title || 'Job Title Not Available'}
                                            </h3>
                                            <span className={`ml-2 px-2 py-1 rounded-full text-xs font-medium ${job?.match_type === 'primary' ? 'bg-blue-200 text-blue-800' :
                                                    job?.match_type === 'alternative' ? 'bg-purple-200 text-purple-800' :
                                                        'bg-gray-200 text-gray-800'
                                                }`}>
                                                {job?.match_type === 'primary' ? 'PRIMARY MATCH' :
                                                    job?.match_type === 'alternative' ? 'ALT MATCH' : 'SKILL MATCH'}
                                            </span>
                                        </div>
                                        <div className="flex items-center text-gray-600 mb-2">
                                            <Briefcase className="w-4 h-4 mr-2" />
                                            {job?.company || 'Company Not Available'}
                                            <MapPin className="w-4 h-4 ml-4 mr-2" />
                                            {job?.location || 'Location Not Available'}
                                        </div>
                                        <div className="flex items-center text-gray-500 text-sm">
                                            <Clock className="w-4 h-4 mr-2" />
                                            {job?.posted_date ? new Date(job.posted_date).toLocaleDateString() : 'Date Not Available'}
                                            <span className="ml-4 bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                                                {job?.source || 'Unknown'}
                                            </span>
                                            {job?.matched_role && (
                                                <span className="ml-2 text-xs text-gray-600">
                                                    Role: {job.matched_role}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="flex items-center mb-2">
                                            <Star className="w-5 h-5 text-yellow-500 mr-1" />
                                            <span className="text-lg font-bold text-gray-900">
                                                {job?.compatibility_score ? (job.compatibility_score * 100).toFixed(0) : 0}%
                                            </span>
                                        </div>
                                        <div className="text-sm text-gray-500">Match Score</div>
                                    </div>
                                </div>

                                <p className="text-gray-700 mb-4 line-clamp-3">
                                    {job?.description || 'No description available'}
                                </p>

                                <div className="flex flex-wrap gap-2 mb-4">
                                    {job?.skills?.slice(0, 5).map((skill, idx) => (
                                        <span
                                            key={idx}
                                            className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                                        >
                                            {skill}
                                        </span>
                                    )) || (
                                            <span className="text-gray-500 text-sm">No skills listed</span>
                                        )}
                                </div>

                                <div className="flex justify-between items-center">
                                    <div className="text-lg font-semibold text-green-600">
                                        {job?.salary_min && job?.salary_max
                                            ? `${job.salary_currency || '$'}${job.salary_min} - ${job.salary_currency || '$'}${job.salary_max}`
                                            : 'Salary not specified'}
                                    </div>
                                    <div className="flex space-x-2">
                                        <button
                                            onClick={() => handleGenerateCoverLetter(job)}
                                            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center"
                                            disabled={loading || !job}
                                        >
                                            <Download className="w-4 h-4 mr-2" />
                                            Cover Letter
                                        </button>
                                        <button
                                            onClick={() => handleApplyToJob(job, 'job')}
                                            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm flex items-center"
                                            disabled={loading || !job}
                                        >
                                            <Bot className="w-4 h-4 mr-2" />
                                            Auto Apply
                                        </button>
                                        <a
                                            href={job?.apply_url || '#'}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className={`${job?.apply_url ? 'bg-gray-600 hover:bg-gray-700' : 'bg-gray-400 cursor-not-allowed'} text-white px-4 py-2 rounded-lg transition-colors text-sm flex items-center`}
                                            onClick={!job?.apply_url ? (e) => e.preventDefault() : undefined}
                                        >
                                            <ExternalLink className="w-4 h-4 mr-2" />
                                            View Job
                                        </a>
                                    </div>
                                </div>
                            </motion.div>
                        ))
                    ) : (
                        <div className="text-center py-8">
                            <div className="text-gray-500 mb-4">
                                <Brain className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                                <h3 className="text-lg font-medium mb-2">
                                    {analysisId ? 'No job recommendations found' : 'Job Recommendations Demo'}
                                </h3>
                                <p className="text-sm mb-4">
                                    {analysisId
                                        ? 'Try updating your preferences or upload a different resume.'
                                        : 'See how our AI matches your profile with relevant job opportunities.'
                                    }
                                </p>
                                {!analysisId && (
                                    <button
                                        onClick={createMockRecommendations}
                                        className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
                                    >
                                        Show Demo Recommendations
                                    </button>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );

    const renderRealTimeJobs = () => (
        <div className="space-y-6">
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
                <h3 className="text-xl font-bold text-green-900 mb-2 flex items-center">
                    <Zap className="mr-2" />
                    Live Job Market Data
                </h3>
                <p className="text-green-700">
                    Fresh opportunities updated in real-time from multiple job boards
                </p>
            </div>

            <div className="grid gap-4">
                {realTimeJobs?.filter(job => job && job.id)?.length > 0 ? (
                    realTimeJobs.filter(job => job && job.id).map((job, index) => (
                        <motion.div
                            key={job.id}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className="bg-white rounded-lg shadow-md border border-gray-200 p-4 hover:shadow-lg transition-all duration-300"
                        >
                            <div className="flex justify-between items-start">
                                <div className="flex-1">
                                    <h4 className="font-semibold text-gray-900 mb-1">{job.title || 'Job Title Not Available'}</h4>
                                    <div className="flex items-center text-gray-600 text-sm mb-2">
                                        <Briefcase className="w-4 h-4 mr-1" />
                                        {job.company || 'Company Not Available'}
                                        <MapPin className="w-4 h-4 ml-3 mr-1" />
                                        {job.location || 'Location Not Available'}
                                    </div>
                                    <div className="flex flex-wrap gap-2">
                                        {job.skills?.slice(0, 3).map((skill, idx) => (
                                            <span
                                                key={idx}
                                                className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs"
                                            >
                                                {skill}
                                            </span>
                                        )) || (
                                                <span className="text-gray-500 text-xs">No skills listed</span>
                                            )}
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="text-sm font-medium text-green-600 mb-2">
                                        {job.salary_range || 'Salary not specified'}
                                    </div>
                                    <a
                                        href={job.apply_url || '#'}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className={`${job.apply_url ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'} text-white px-3 py-1 rounded text-sm transition-colors inline-flex items-center`}
                                        onClick={!job.apply_url ? (e) => e.preventDefault() : undefined}
                                    >
                                        <ExternalLink className="w-3 h-3 mr-1" />
                                        Apply
                                    </a>
                                </div>
                            </div>
                        </motion.div>
                    ))
                ) : (
                    <div className="text-center py-8">
                        <div className="text-gray-500 mb-4">
                            <Zap className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                            <h3 className="text-lg font-medium mb-2">No real-time jobs available</h3>
                            <p className="text-sm">Check back later for fresh opportunities.</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );

    const renderSkillAnalysis = () => (
        <div className="space-y-6">
            {skillGaps && (
                <>
                    <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-xl p-6 border border-red-200">
                        <h3 className="text-xl font-bold text-red-900 mb-4 flex items-center">
                            <Target className="mr-2" />
                            Skill Gap Analysis
                        </h3>

                        {skillGaps.skill_gaps?.critical_gaps?.length > 0 && (
                            <div className="mb-6">
                                <h4 className="font-semibold text-red-800 mb-3">Critical Skills to Learn</h4>
                                <div className="grid gap-3">
                                    {skillGaps.skill_gaps.critical_gaps.slice(0, 5).map(([skill, demand], index) => (
                                        <div key={skill} className="flex justify-between items-center bg-white rounded-lg p-3 border border-red-100">
                                            <span className="font-medium text-gray-900">{skill}</span>
                                            <div className="flex items-center">
                                                <div className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm mr-2">
                                                    {demand} jobs demand this
                                                </div>
                                                <div className="w-16 h-2 bg-red-200 rounded-full">
                                                    <div
                                                        className="h-full bg-red-500 rounded-full"
                                                        style={{ width: `${Math.min(100, (demand / 10) * 100)}%` }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {skillGaps.skill_gaps?.learning_recommendations?.length > 0 && (
                            <div>
                                <h4 className="font-semibold text-orange-800 mb-3 flex items-center">
                                    <BookOpen className="w-5 h-5 mr-2" />
                                    Learning Recommendations
                                </h4>
                                <div className="grid gap-4">
                                    {skillGaps.skill_gaps.learning_recommendations.map((rec, index) => (
                                        <div key={index} className="bg-white rounded-lg p-4 border border-orange-100">
                                            <div className="flex justify-between items-start mb-2">
                                                <h5 className="font-medium text-gray-900">{rec.skill}</h5>
                                                <span className={`px-2 py-1 rounded text-xs ${rec.priority === 'High' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                    {rec.priority} Priority
                                                </span>
                                            </div>
                                            <p className="text-sm text-gray-600 mb-2">
                                                Time estimate: {rec.learning_resources.time_estimate}
                                            </p>
                                            <div className="text-sm">
                                                <div className="mb-1">
                                                    <strong>Courses:</strong> {rec.learning_resources.courses.join(', ')}
                                                </div>
                                                <div>
                                                    <strong>Practice:</strong> {rec.learning_resources.practice.join(', ')}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );

    const renderCareerPaths = () => (
        <div className="space-y-6">
            <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border border-purple-200">
                <h3 className="text-xl font-bold text-purple-900 mb-2 flex items-center">
                    <TrendingUp className="mr-2" />
                    AI-Powered Career Guidance
                </h3>
                <p className="text-purple-700">
                    Personalized career paths based on your skills and market demand
                </p>
            </div>

            <div className="grid gap-6">
                {careerPaths.map((path, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="bg-white rounded-xl shadow-lg border border-gray-200 p-6"
                    >
                        <div className="flex justify-between items-start mb-4">
                            <div className="flex-1">
                                <h4 className="text-lg font-bold text-gray-900 mb-2">{path.path}</h4>
                                <div className="flex items-center space-x-4 text-sm text-gray-600">
                                    <span className="flex items-center">
                                        <Clock className="w-4 h-4 mr-1" />
                                        {path.timeline}
                                    </span>
                                    <span className="flex items-center">
                                        <TrendingUp className="w-4 h-4 mr-1" />
                                        {path.growth_potential} Growth
                                    </span>
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                                    {path.current_match} Match
                                </div>
                            </div>
                        </div>

                        <div className="mb-4">
                            <h5 className="font-medium text-gray-800 mb-2">Required Skills:</h5>
                            <div className="flex flex-wrap gap-2">
                                {path.required_skills.map((skill, idx) => (
                                    <span
                                        key={idx}
                                        className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
                                    >
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>

                        {path.missing_skills?.length > 0 && (
                            <div>
                                <h5 className="font-medium text-gray-800 mb-2">Skills to Learn:</h5>
                                <div className="flex flex-wrap gap-2">
                                    {path.missing_skills.map((skill, idx) => (
                                        <span
                                            key={idx}
                                            className="bg-red-100 text-red-800 px-2 py-1 rounded text-sm"
                                        >
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                    </motion.div>
                ))}
            </div>
        </div>
    );

    const renderApplications = () => (
        <div className="space-y-6">
            <div className="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-xl p-6 border border-indigo-200">
                <h3 className="text-xl font-bold text-indigo-900 mb-2 flex items-center">
                    <Briefcase className="mr-2" />
                    Application History
                </h3>
                <p className="text-indigo-700">
                    Track your job applications and success rate
                </p>
            </div>

            <div className="grid gap-4">
                {applicationHistory.length > 0 ? (
                    applicationHistory.slice(0, 10).map((app, index) => (
                        <div
                            key={index}
                            className={`bg-white rounded-lg border p-4 ${app.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'
                                }`}
                        >
                            <div className="flex justify-between items-start">
                                <div>
                                    <h4 className="font-medium text-gray-900">{app.job_title}</h4>
                                    <p className="text-gray-600">{app.company}</p>
                                    <p className="text-sm text-gray-500">
                                        {new Date(app.timestamp).toLocaleDateString()}
                                    </p>
                                </div>
                                <div className="text-right">
                                    <span className={`px-2 py-1 rounded text-sm ${app.success
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-red-100 text-red-800'
                                        }`}>
                                        {app.success ? 'Applied' : 'Failed'}
                                    </span>
                                    <p className="text-xs text-gray-500 mt-1">{app.method}</p>
                                </div>
                            </div>
                            {app.error && (
                                <p className="text-sm text-red-600 mt-2">{app.error}</p>
                            )}
                        </div>
                    ))
                ) : (
                    <div className="text-center py-8 text-gray-500">
                        <Briefcase className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                        <p>No applications yet. Start applying to jobs!</p>
                    </div>
                )}
            </div>
        </div>
    );

    if (loading && !recommendations) {
        return (
            <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    // Show message when no analysis data is available
    if (!analysisId && !resumeAnalysis) {
        return (
            <div className="max-w-4xl mx-auto">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="glass-card p-8 text-center"
                >
                    <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
                        <Brain className="w-8 h-8 text-white" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">
                        AI-Powered Career Hub
                    </h2>
                    <p className="text-gray-600 mb-6 max-w-md mx-auto">
                        Upload your resume first to unlock personalized AI job recommendations and career insights.
                    </p>
                    <div className="text-sm text-gray-500">
                        🎯 Upload your resume → 🤖 Get AI analysis → 📊 View dashboard
                    </div>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto relative">
            {/* Loading Overlay */}
            {loading && (
                <div className="fixed inset-0 bg-black bg-opacity-20 backdrop-blur-sm flex items-center justify-center z-50">
                    <div className="glass-card p-8 text-center">
                        <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center animate-pulse">
                            <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        </div>
                        <p className="text-gray-700 font-medium">Loading dashboard data...</p>
                    </div>
                </div>
            )}

            {/* Hero Header */}
            <div className="text-center mb-12">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full mb-6 animate-float">
                    <Brain className="w-10 h-10 text-white" />
                </div>
                <h1 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 bg-clip-text text-transparent mb-4">
                    AI-Powered Career Hub
                </h1>
                <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                    Advanced AI insights, real-time job matching, and personalized career guidance
                </p>
            </div>

            {/* Resume Score Components */}
            {resumeAnalysis && (
                <div className="mb-8 space-y-6">
                    {/* Enhanced Score Dashboard */}
                    <ResumeScoreBoard resumeAnalysis={resumeAnalysis} />

                    {/* Original Score Component for compatibility */}
                    <div className="block lg:hidden">
                        <ResumeScore resumeAnalysis={resumeAnalysis} />
                    </div>
                </div>
            )}

            {/* Modern Tab Navigation */}

            {/* Tab Content */}
            <div className="animate-fade-in">
                {activeTab === 'recommendations' && renderRecommendations()}
                {activeTab === 'realtime' && renderRealTimeJobs()}
                {activeTab === 'skills' && renderSkillAnalysis()}
                {activeTab === 'career' && renderCareerPaths()}
                {activeTab === 'applications' && renderApplications()}
            </div>
        </div>
    );
}
