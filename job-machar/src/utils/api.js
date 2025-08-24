import axios from 'axios';

// Configure axios with base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' ? `${window.location.origin}/api` : 'http://localhost:5000');

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds timeout for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    const message = error.response?.data?.error || error.message || 'An error occurred';
    return Promise.reject(new Error(message));
  }
);

// Enhanced API functions

// Fetch all jobs
export const getJobs = async () => {
  // Assumes backend endpoint returns { jobs: [...] }
  return await api.get('/jobs');
};

// Get job match score/details for a specific job and analysisId
export const getJobMatch = async (jobId, analysisId) => {
  // Assumes backend endpoint expects job_id and analysis_id
  return await api.post('/job-match', {
    job_id: jobId,
    analysis_id: analysisId
  });
};

// Upload and analyze resume with enhanced AI models
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('resume', file);

  return await api.post('/upload-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Get enhanced job recommendations with real-time data
export const getEnhancedRecommendations = async (analysisId, preferences = {}, limit = 20) => {
  return await api.post('/get-recommendations', {
    analysis_id: analysisId,
    preferences,
    limit
  });
};

// Fetch real-time job data
export const getRealTimeJobs = async (keywords, location = '', limit = 50) => {
  return await api.post('/realtime-jobs', {
    keywords,
    location,
    limit
  });
};

// Search jobs using regular API
export const searchJobs = async (keywords, location = '', experienceLevel = '', limit = 20) => {
  return await api.post('/search-jobs', {
    keywords: Array.isArray(keywords) ? keywords : [keywords],
    location,
    experience_level: experienceLevel,
    limit
  });
};

// Search jobs specifically from Wellfound and LinkedIn
export const searchWellfoundLinkedinJobs = async (keywords, location = '', experienceLevel = '', limit = 20) => {
  return await api.post('/search-wellfound-linkedin', {
    keywords: Array.isArray(keywords) ? keywords : [keywords],
    location,
    experience_level: experienceLevel,
    limit
  });
};

// Apply to job with automation assistance
export const applyToJob = async (data) => {
  return await api.post('/apply-to-job', data);
};

// Generate personalized cover letter
export const generateCoverLetter = async (analysisId, jobTitle, company, jobDescription = '') => {
  return await api.post('/generate-cover-letter', {
    analysis_id: analysisId,
    job_title: jobTitle,
    company,
    job_description: jobDescription
  });
};

// Get application history and statistics
export const getApplicationHistory = async () => {
  return await api.get('/application-history');
};

// Perform skill gap analysis
export const getSkillGapAnalysis = async (analysisId, keywords = []) => {
  return await api.post('/skill-gap-analysis', {
    analysis_id: analysisId,
    keywords
  });
};

// Get AI-powered career guidance
export const getCareerGuidance = async (analysisId) => {
  return await api.post('/career-guidance', {
    analysis_id: analysisId
  });
};

// Get detailed analysis results
export const getDetailedAnalysis = async (analysisId) => {
  return await api.get(`/analysis/${analysisId}`);
};

// Export analysis results
export const exportAnalysis = async (analysisId) => {
  return await api.get(`/export-analysis/${analysisId}`);
};

// Health check
export const healthCheck = async () => {
  return await api.get('/health');
};

// Get application statistics and real-time data
export const getStats = async () => {
  return await api.get('/stats');
};

export default api;
