'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  Building,
  DollarSign,
  Clock,
  Star,
  TrendingUp,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import toast from 'react-hot-toast';
import { getJobs, getJobMatch } from '../../utils/api';

export default function JobsList({ analysisId }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);
  const [jobMatch, setJobMatch] = useState(null);
  const [matchLoading, setMatchLoading] = useState(false);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        setLoading(true);
        const data = await getJobs();
        setJobs(data.jobs);
      } catch (error) {
        toast.error('Failed to load jobs');
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []);

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

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto">
        <div className="glass-card p-12">
          <div className="flex flex-col items-center justify-center space-y-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center animate-pulse">
              <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            </div>
            <div className="text-center">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Loading Job Opportunities
              </h3>
              <p className="text-gray-600">
                Fetching the latest job listings for you...
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full mb-6 animate-float">
          <Building className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4">
          💼 Job Opportunities
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover amazing career opportunities tailored to your skills and experience
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Jobs List */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Available Positions ({jobs.length})
            </h2>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              <span>Updated recently</span>
            </div>
          </div>

          {jobs.map((job, index) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`glass-card cursor-pointer transition-all duration-300 hover:scale-[1.02] hover:shadow-xl group ${selectedJob?.id === job.id
                ? 'ring-2 ring-blue-500 shadow-xl scale-[1.02]'
                : 'hover:ring-1 hover:ring-blue-300'
                }`}
              onClick={() => handleJobSelect(job)}
              whileHover={{ y: -2 }}
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {job.title}
                      </h3>
                      {selectedJob?.id === job.id && (
                        <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                      )}
                    </div>

                    <div className="flex items-center space-x-2 text-gray-600 mb-3">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                        <Building className="h-4 w-4 text-white" />
                      </div>
                      <span className="font-medium">{job.company}</span>
                    </div>

                    <div className="flex flex-wrap items-center gap-4 text-sm">
                      <div className="flex items-center space-x-1 text-green-600 bg-green-50 px-2 py-1 rounded-full">
                        <DollarSign className="h-3 w-3" />
                        <span className="font-medium">{job.salary_range}</span>
                      </div>
                      <div className="flex items-center space-x-1 text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                        <Star className="h-3 w-3" />
                        <span className="font-medium capitalize">{job.experience_level}</span>
                      </div>
                      <div className="flex items-center space-x-1 text-purple-600 bg-purple-50 px-2 py-1 rounded-full">
                        <Clock className="h-3 w-3" />
                        <span className="font-medium">{job.employment_type || 'Full-time'}</span>
                      </div>
                    </div>
                  </div>

                  {analysisId && selectedJob?.id === job.id && jobMatch && (
                    <motion.div
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className="text-center"
                    >
                      <div className="w-16 h-16 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center mb-2">
                        <span className="text-white font-bold text-lg">
                          {Math.round(jobMatch.match_result.overall_score * 100)}%
                        </span>
                      </div>
                      <div className="text-xs text-gray-600 font-medium">Match Score</div>
                    </motion.div>
                  )}
                </div>

                <p className="text-gray-600 mb-4 text-clamp-2 leading-relaxed">
                  {job.description}
                </p>

                <div className="flex flex-wrap gap-2">
                  {(job.required_skills || job.requirements?.split(',').map(s => s.trim()) || []).slice(0, 6).map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                    >
                      {skill}
                    </span>
                  ))}
                  {(job.required_skills || job.requirements?.split(',') || []).length > 6 && (
                    <span className="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-full">
                      +{(job.required_skills || job.requirements?.split(',') || []).length - 6} more
                    </span>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Job Details Panel */}
        <div className="lg:col-span-1">
          {selectedJob ? (
            <div className="bg-white rounded-xl shadow-sm border sticky top-6">
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Job Details
                </h3>

                <div className="space-y-4 mb-6">
                  <div>
                    <h4 className="font-medium text-gray-900">{selectedJob.title}</h4>
                    <p className="text-gray-600">{selectedJob.company}</p>
                  </div>

                  <div>
                    <span className="text-sm text-gray-600">Salary Range:</span>
                    <p className="font-medium">{selectedJob.salary_range}</p>
                  </div>

                  <div>
                    <span className="text-sm text-gray-600">Experience Level:</span>
                    <p className="font-medium capitalize">{selectedJob.experience_level}</p>
                  </div>

                  <div>
                    <span className="text-sm text-gray-600">Required Skills:</span>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {(selectedJob.required_skills || selectedJob.requirements?.split(',').map(s => s.trim()) || []).map((skill, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-gray-100 text-gray-800 text-sm rounded"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Match Analysis */}
                {analysisId && (
                  <div className="border-t pt-6">
                    <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                      <Star className="h-5 w-5 mr-2 text-yellow-500" />
                      Match Analysis
                    </h4>

                    {matchLoading ? (
                      <div className="text-center py-4">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                      </div>
                    ) : jobMatch ? (
                      <div className="space-y-4">
                        <div className="text-center">
                          <div className="text-3xl font-bold text-blue-600 mb-1">
                            {Math.round(jobMatch.match_result.overall_score * 100)}%
                          </div>
                          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${jobMatch.match_result.recommendation === 'Excellent Match' ? 'bg-green-100 text-green-800' :
                            jobMatch.match_result.recommendation === 'Good Match' ? 'bg-yellow-100 text-yellow-800' :
                              jobMatch.match_result.recommendation === 'Fair Match' ? 'bg-orange-100 text-orange-800' :
                                'bg-red-100 text-red-800'
                            }`}>
                            {jobMatch.match_result.recommendation}
                          </div>
                        </div>

                        <div className="space-y-3">
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-gray-600">Skills Match:</span>
                            <span className="font-medium">
                              {Math.round(jobMatch.match_result.skill_match_score * 100)}%
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-gray-600">Experience Match:</span>
                            <span className="font-medium">
                              {Math.round(jobMatch.match_result.experience_match_score * 100)}%
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-sm text-gray-600">Semantic Similarity:</span>
                            <span className="font-medium">
                              {Math.round(jobMatch.match_result.semantic_similarity * 100)}%
                            </span>
                          </div>
                        </div>

                        {/* Matched Skills */}
                        {jobMatch.match_result.matched_skills?.length > 0 && (
                          <div>
                            <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                              <CheckCircle className="h-4 w-4 mr-1 text-green-500" />
                              Matched Skills
                            </h5>
                            <div className="flex flex-wrap gap-1">
                              {jobMatch.match_result.matched_skills.map((skill, idx) => (
                                <span
                                  key={idx}
                                  className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Missing Skills */}
                        {jobMatch.match_result.missing_skills?.length > 0 && (
                          <div>
                            <h5 className="font-medium text-gray-900 mb-2 flex items-center">
                              <AlertCircle className="h-4 w-4 mr-1 text-red-500" />
                              Skills to Develop
                            </h5>
                            <div className="flex flex-wrap gap-1">
                              {jobMatch.match_result.missing_skills.map((skill, idx) => (
                                <span
                                  key={idx}
                                  className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Score Breakdown */}
                        {jobMatch.match_result.score_breakdown && (
                          <div>
                            <h5 className="font-medium text-gray-900 mb-2">Score Breakdown</h5>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span>Skills (40%):</span>
                                <span>{(jobMatch.match_result.score_breakdown.skills_score || 0).toFixed(2)}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Experience (30%):</span>
                                <span>{(jobMatch.match_result.score_breakdown.experience_score || 0).toFixed(2)}</span>
                              </div>
                              <div className="flex justify-between">
                                <span>Semantic (30%):</span>
                                <span>{(jobMatch.match_result.score_breakdown.semantic_score || 0).toFixed(2)}</span>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    ) : (
                      <p className="text-gray-600 text-sm">
                        Upload your resume to see match analysis
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border p-6 text-center text-gray-600">
              <Building className="h-12 w-12 mx-auto mb-4 text-gray-400" />
              <p>Select a job to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
