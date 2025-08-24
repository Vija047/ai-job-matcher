'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Building,
    DollarSign,
    Clock,
    Star,
    TrendingUp,
    CheckCircle,
    AlertCircle,
    Search,
    MapPin,
    Briefcase,
    Rocket,
    Users,
    ExternalLink,
    Filter,
    Globe,
    Heart,
    Bookmark
} from 'lucide-react';
import toast from 'react-hot-toast';
import { searchJobs, searchWellfoundLinkedinJobs, getJobMatch } from '../../utils/api';

export default function EnhancedJobsList({ analysisId }) {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [jobMatch, setJobMatch] = useState(null);
    const [matchLoading, setMatchLoading] = useState(false);

    // Search filters
    const [searchType, setSearchType] = useState('wellfound-linkedin'); // 'all', 'wellfound-linkedin'
    const [keywords, setKeywords] = useState('');
    const [location, setLocation] = useState('');
    const [experienceLevel, setExperienceLevel] = useState('');
    const [showFilters, setShowFilters] = useState(false);

    // Job data
    const [sourceBreakdown, setSourceBreakdown] = useState({});
    const [totalJobs, setTotalJobs] = useState(0);

    const handleSearch = async () => {
        if (!keywords.trim()) {
            toast.error('Please enter keywords to search');
            return;
        }

        try {
            setLoading(true);
            setJobs([]);

            const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k);

            let data;
            if (searchType === 'wellfound-linkedin') {
                data = await searchWellfoundLinkedinJobs(keywordList, location, experienceLevel, 30);
                toast.success(`Found ${data.total_found} jobs from Wellfound & LinkedIn!`);
            } else {
                data = await searchJobs(keywordList, location, experienceLevel, 30);
                toast.success(`Found ${data.total_found} jobs from multiple sources!`);
            }

            setJobs(data.jobs || []);
            setTotalJobs(data.total_found || 0);
            setSourceBreakdown(data.source_breakdown || {});

        } catch (error) {
            console.error('Search error:', error);
            toast.error('Failed to search jobs: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleJobSelect = async (job) => {
        setSelectedJob(job);

        if (analysisId) {
            try {
                setMatchLoading(true);
                const matchData = await getJobMatch(job.id, analysisId);
                setJobMatch(matchData);
            } catch (error) {
                toast.error('Failed to calculate job match');
            } finally {
                setMatchLoading(false);
            }
        }
    };

    const getCompanyTypeIcon = (source, isStartup) => {
        if (source === 'Wellfound' || isStartup) {
            return <Rocket className="w-4 h-4 text-orange-500" />;
        }
        if (source === 'LinkedIn') {
            return <Users className="w-4 h-4 text-blue-500" />;
        }
        return <Building className="w-4 h-4 text-gray-500" />;
    };

    const getCompanyTypeBadge = (source, isStartup, fundingStage) => {
        if (source === 'Wellfound' || isStartup) {
            return (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-orange-100 text-orange-800">
                    <Rocket className="w-3 h-3 mr-1" />
                    Startup {fundingStage && `(${fundingStage})`}
                </span>
            );
        }
        if (source === 'LinkedIn') {
            return (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                    <Users className="w-3 h-3 mr-1" />
                    Professional Network
                </span>
            );
        }
        return (
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-800">
                <Building className="w-3 h-3 mr-1" />
                Traditional
            </span>
        );
    };

    return (
        <div className="max-w-7xl mx-auto p-6">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    Job Search
                </h1>
                <p className="text-gray-600">
                    Discover opportunities from Wellfound startups and LinkedIn professionals
                </p>
            </div>

            {/* Search Section */}
            <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                <div className="flex flex-col space-y-4">
                    {/* Search Type Selector */}
                    <div className="flex flex-wrap gap-2">
                        <button
                            onClick={() => setSearchType('wellfound-linkedin')}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${searchType === 'wellfound-linkedin'
                                    ? 'bg-gradient-to-r from-orange-500 to-blue-500 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            <span className="flex items-center">
                                <Rocket className="w-4 h-4 mr-2" />
                                Wellfound + LinkedIn
                            </span>
                        </button>
                        <button
                            onClick={() => setSearchType('all')}
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${searchType === 'all'
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            <span className="flex items-center">
                                <Globe className="w-4 h-4 mr-2" />
                                All Sources
                            </span>
                        </button>
                    </div>

                    {/* Main Search Row */}
                    <div className="flex flex-col md:flex-row gap-4">
                        <div className="flex-1">
                            <input
                                type="text"
                                placeholder="Enter keywords (e.g., Software Engineer, Data Scientist)"
                                value={keywords}
                                onChange={(e) => setKeywords(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                        </div>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setShowFilters(!showFilters)}
                                className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center"
                            >
                                <Filter className="w-4 h-4 mr-2" />
                                Filters
                            </button>
                            <button
                                onClick={handleSearch}
                                disabled={loading}
                                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                            >
                                {loading ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                                        Searching...
                                    </>
                                ) : (
                                    <>
                                        <Search className="w-4 h-4 mr-2" />
                                        Search Jobs
                                    </>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Filters */}
                    <AnimatePresence>
                        {showFilters && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-gray-200"
                            >
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Location
                                    </label>
                                    <input
                                        type="text"
                                        placeholder="San Francisco, Remote, etc."
                                        value={location}
                                        onChange={(e) => setLocation(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-2">
                                        Experience Level
                                    </label>
                                    <select
                                        value={experienceLevel}
                                        onChange={(e) => setExperienceLevel(e.target.value)}
                                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                                    >
                                        <option value="">All Levels</option>
                                        <option value="entry">Entry Level</option>
                                        <option value="mid">Mid Level</option>
                                        <option value="senior">Senior Level</option>
                                        <option value="executive">Executive</option>
                                    </select>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>

            {/* Results Summary */}
            {(totalJobs > 0 || Object.keys(sourceBreakdown).length > 0) && (
                <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Search Results</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="bg-blue-50 rounded-lg p-4">
                            <div className="text-2xl font-bold text-blue-600">{totalJobs}</div>
                            <div className="text-sm text-blue-800">Total Jobs Found</div>
                        </div>
                        {sourceBreakdown.wellfound_count !== undefined && (
                            <div className="bg-orange-50 rounded-lg p-4">
                                <div className="text-2xl font-bold text-orange-600">{sourceBreakdown.wellfound_count}</div>
                                <div className="text-sm text-orange-800">Startup Opportunities</div>
                            </div>
                        )}
                        {sourceBreakdown.linkedin_count !== undefined && (
                            <div className="bg-blue-50 rounded-lg p-4">
                                <div className="text-2xl font-bold text-blue-600">{sourceBreakdown.linkedin_count}</div>
                                <div className="text-sm text-blue-800">LinkedIn Jobs</div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Jobs List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="space-y-4">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">
                        {jobs.length > 0 ? `${jobs.length} Jobs Found` : 'No Jobs Yet'}
                    </h3>

                    {loading ? (
                        <div className="space-y-4">
                            {[...Array(3)].map((_, i) => (
                                <div key={i} className="bg-white rounded-xl shadow-lg p-6 animate-pulse">
                                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                                    <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
                                    <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
                                    <div className="h-3 bg-gray-200 rounded w-5/6"></div>
                                </div>
                            ))}
                        </div>
                    ) : jobs.length === 0 ? (
                        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
                            <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                No Jobs Found
                            </h3>
                            <p className="text-gray-600 mb-4">
                                Try adjusting your search criteria or keywords
                            </p>
                            <button
                                onClick={() => {
                                    setKeywords('software engineer');
                                    setLocation('');
                                    setExperienceLevel('');
                                }}
                                className="text-blue-600 hover:text-blue-800 font-medium"
                            >
                                Try &quot;software engineer&quot;
                            </button>
                        </div>
                    ) : (
                        <div className="space-y-4">
                            {jobs.map((job, index) => (
                                <motion.div
                                    key={job.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ delay: index * 0.1 }}
                                    onClick={() => handleJobSelect(job)}
                                    className={`bg-white rounded-xl shadow-lg p-6 cursor-pointer transition-all hover:shadow-xl border-2 ${selectedJob?.id === job.id ? 'border-blue-500' : 'border-transparent'
                                        }`}
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="flex-1">
                                            <h4 className="text-lg font-semibold text-gray-900 mb-2">
                                                {job.title}
                                            </h4>
                                            <div className="flex items-center space-x-2 mb-2">
                                                {getCompanyTypeIcon(job.source, job.is_startup)}
                                                <span className="font-medium text-gray-800">{job.company}</span>
                                                {job.company_logo && (
                                                    <div
                                                        className="w-6 h-6 rounded bg-gray-200 flex items-center justify-center text-xs font-medium text-gray-600"
                                                        title={`${job.company} logo`}
                                                    >
                                                        {job.company.charAt(0).toUpperCase()}
                                                    </div>
                                                )}
                                            </div>
                                            <div className="flex flex-wrap items-center gap-2 mb-3">
                                                {getCompanyTypeBadge(job.source, job.is_startup, job.funding_stage)}
                                                {job.remote_allowed && (
                                                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                                                        <Globe className="w-3 h-3 mr-1" />
                                                        Remote
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <div className="flex flex-col items-end space-y-2">
                                            <button className="p-2 hover:bg-gray-100 rounded-full">
                                                <Bookmark className="w-4 h-4 text-gray-400" />
                                            </button>
                                        </div>
                                    </div>

                                    <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                                        {job.location && (
                                            <div className="flex items-center">
                                                <MapPin className="w-4 h-4 mr-1" />
                                                {job.location}
                                            </div>
                                        )}
                                        {job.salary_range && job.salary_range !== "Salary not specified" && (
                                            <div className="flex items-center">
                                                <DollarSign className="w-4 h-4 mr-1" />
                                                {job.salary_range}
                                            </div>
                                        )}
                                        {job.posted_date && (
                                            <div className="flex items-center">
                                                <Clock className="w-4 h-4 mr-1" />
                                                {new Date(job.posted_date).toLocaleDateString()}
                                            </div>
                                        )}
                                    </div>

                                    <p className="text-gray-700 text-sm mb-4 line-clamp-3">
                                        {job.description}
                                    </p>

                                    {job.skills_required && job.skills_required.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mb-4">
                                            {job.skills_required.slice(0, 5).map((skill, i) => (
                                                <span
                                                    key={i}
                                                    className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                                                >
                                                    {skill}
                                                </span>
                                            ))}
                                            {job.skills_required.length > 5 && (
                                                <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                                                    +{job.skills_required.length - 5} more
                                                </span>
                                            )}
                                        </div>
                                    )}

                                    <div className="flex justify-between items-center">
                                        <span className="text-sm font-medium text-blue-600">
                                            via {job.source}
                                        </span>
                                        {job.apply_url && (
                                            <a
                                                href={job.apply_url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                onClick={(e) => e.stopPropagation()}
                                                className="inline-flex items-center px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
                                            >
                                                Apply
                                                <ExternalLink className="w-3 h-3 ml-1" />
                                            </a>
                                        )}
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    )}
                </div>

                {/* Job Details Panel */}
                <div className="lg:sticky lg:top-6">
                    {selectedJob ? (
                        <div className="bg-white rounded-xl shadow-lg p-6">
                            <div className="flex justify-between items-start mb-4">
                                <h3 className="text-xl font-semibold text-gray-900">
                                    Job Details
                                </h3>
                                <button
                                    onClick={() => setSelectedJob(null)}
                                    className="text-gray-400 hover:text-gray-600"
                                >
                                    ✕
                                </button>
                            </div>

                            <div className="space-y-4">
                                <div>
                                    <h4 className="text-lg font-medium text-gray-900 mb-1">
                                        {selectedJob.title}
                                    </h4>
                                    <div className="flex items-center space-x-2 mb-2">
                                        {getCompanyTypeIcon(selectedJob.source, selectedJob.is_startup)}
                                        <span className="font-medium text-gray-800">{selectedJob.company}</span>
                                    </div>
                                    <div className="flex flex-wrap gap-2 mb-4">
                                        {getCompanyTypeBadge(selectedJob.source, selectedJob.is_startup, selectedJob.funding_stage)}
                                        {selectedJob.remote_allowed && (
                                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                                                <Globe className="w-3 h-3 mr-1" />
                                                Remote
                                            </span>
                                        )}
                                    </div>
                                </div>

                                {/* Job Match Score */}
                                {analysisId && (
                                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4">
                                        <h5 className="font-medium text-gray-900 mb-2">
                                            Compatibility Score
                                        </h5>
                                        {matchLoading ? (
                                            <div className="animate-pulse">
                                                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                                            </div>
                                        ) : jobMatch ? (
                                            <div className="space-y-2">
                                                <div className="flex items-center justify-between">
                                                    <span className="text-sm text-gray-600">Overall Match</span>
                                                    <span className="font-semibold text-blue-600">
                                                        {jobMatch.compatibility_score || 75}%
                                                    </span>
                                                </div>
                                                <div className="w-full bg-gray-200 rounded-full h-2">
                                                    <div
                                                        className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                                                        style={{ width: `${jobMatch.compatibility_score || 75}%` }}
                                                    ></div>
                                                </div>
                                            </div>
                                        ) : (
                                            <p className="text-sm text-gray-600">
                                                Upload your resume to see compatibility score
                                            </p>
                                        )}
                                    </div>
                                )}

                                {/* Job Description */}
                                <div>
                                    <h5 className="font-medium text-gray-900 mb-2">Description</h5>
                                    <p className="text-gray-700 text-sm leading-relaxed">
                                        {selectedJob.description}
                                    </p>
                                </div>

                                {/* Requirements */}
                                {selectedJob.requirements && selectedJob.requirements.length > 0 && (
                                    <div>
                                        <h5 className="font-medium text-gray-900 mb-2">Requirements</h5>
                                        <ul className="space-y-1">
                                            {selectedJob.requirements.slice(0, 5).map((req, i) => (
                                                <li key={i} className="flex items-start text-sm text-gray-700">
                                                    <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                                                    {req}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {/* Skills */}
                                {selectedJob.skills_required && selectedJob.skills_required.length > 0 && (
                                    <div>
                                        <h5 className="font-medium text-gray-900 mb-2">Skills Required</h5>
                                        <div className="flex flex-wrap gap-2">
                                            {selectedJob.skills_required.map((skill, i) => (
                                                <span
                                                    key={i}
                                                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                                                >
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Company Info */}
                                <div className="space-y-2">
                                    {selectedJob.company_size && (
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-gray-600">Company Size</span>
                                            <span className="text-gray-900">{selectedJob.company_size}</span>
                                        </div>
                                    )}
                                    {selectedJob.industry && (
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-gray-600">Industry</span>
                                            <span className="text-gray-900">{selectedJob.industry}</span>
                                        </div>
                                    )}
                                    {selectedJob.funding_stage && (
                                        <div className="flex items-center justify-between text-sm">
                                            <span className="text-gray-600">Funding Stage</span>
                                            <span className="text-gray-900">{selectedJob.funding_stage}</span>
                                        </div>
                                    )}
                                </div>

                                {/* Apply Button */}
                                {selectedJob.apply_url && (
                                    <div className="pt-4 border-t border-gray-200">
                                        <a
                                            href={selectedJob.apply_url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="w-full inline-flex items-center justify-center px-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 transition-colors"
                                        >
                                            Apply on {selectedJob.source}
                                            <ExternalLink className="w-4 h-4 ml-2" />
                                        </a>
                                    </div>
                                )}
                            </div>
                        </div>
                    ) : (
                        <div className="bg-white rounded-xl shadow-lg p-8 text-center">
                            <Briefcase className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-gray-900 mb-2">
                                Select a Job
                            </h3>
                            <p className="text-gray-600">
                                Click on any job to view detailed information and requirements
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
