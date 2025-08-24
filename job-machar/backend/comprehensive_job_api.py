"""
Comprehensive Job Search and Application API
Integrates job recommendations, applications, and tracking
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our modules
from role_based_recommender import RoleBasedRecommender
from job_application_manager import JobApplicationManager
from enhanced_job_client import JobAPIClient
from enhanced_resume_analyzer import EnhancedResumeAnalyzer

logger = logging.getLogger(__name__)

class JobSearchAPI:
    """
    Comprehensive job search API with recommendations and application management
    """
    
    def __init__(self):
        self.recommender = RoleBasedRecommender()
        self.application_manager = JobApplicationManager()
        self.job_client = JobAPIClient()
        self.resume_analyzer = EnhancedResumeAnalyzer()
        
        # Sample job data for demonstration
        self.sample_jobs = self._get_sample_jobs()
        
    def search_and_recommend_jobs(self, resume_analysis: Dict, preferences: Dict = None) -> Dict[str, Any]:
        """
        Main function to search and recommend jobs based on resume analysis
        """
        try:
            # Step 1: Analyze role compatibility
            role_analysis = self.recommender.analyze_role_compatibility(resume_analysis)
            
            # Step 2: Get available jobs (using sample data for demo)
            available_jobs = self.sample_jobs
            
            # Step 3: Get role-based recommendations
            recommendations = self.recommender.get_role_based_recommendations(
                role_analysis, available_jobs, preferences
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in job search and recommendation: {e}")
            return {
                'success': False,
                'error': str(e),
                'jobs': [],
                'internships': []
            }
    
    def get_quick_job_matches(self, user_skills: List[str], experience_level: str = 'mid') -> Dict[str, Any]:
        """
        Quick job matching based on skills and experience level
        """
        try:
            # Create a minimal resume analysis
            quick_analysis = {
                'skills_analysis': {
                    'all_skills': user_skills
                },
                'experience_analysis': {
                    'experience_level': experience_level,
                    'total_years': 3 if experience_level == 'mid' else 1 if experience_level == 'entry' else 7
                },
                'role_suggestion': {
                    'primary_role': 'Software Engineer',  # Default
                    'alternative_roles': ['Full Stack Developer', 'Frontend Developer']
                }
            }
            
            return self.search_and_recommend_jobs(quick_analysis)
            
        except Exception as e:
            logger.error(f"Error in quick job matching: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_job(self, job_data: Dict, folder: str = "favorites") -> Dict[str, Any]:
        """Save a job for later"""
        return self.application_manager.save_job_for_later(job_data, folder)
    
    def get_saved_jobs(self, folder: str = None) -> Dict[str, Any]:
        """Get saved jobs"""
        return self.application_manager.get_saved_jobs(folder)
    
    def apply_to_job(self, job_data: Dict, user_profile: Dict, application_type: str = "standard") -> Dict[str, Any]:
        """
        Apply to a job (create draft application)
        """
        try:
            if application_type == "quick":
                # Quick apply - minimal setup
                result = self.application_manager.create_application_draft(job_data, user_profile)
                if result['success']:
                    # Auto-submit for quick apply
                    return self.application_manager.submit_application(
                        result['application_id'], 
                        {
                            'cover_letter': result['application']['cover_letter'],
                            'notes': 'Quick apply submission'
                        }
                    )
                return result
            else:
                # Standard apply - create draft for review
                return self.application_manager.create_application_draft(job_data, user_profile)
                
        except Exception as e:
            logger.error(f"Error applying to job: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def bulk_apply_to_jobs(self, job_ids: List[str], user_profile: Dict) -> Dict[str, Any]:
        """
        Set up bulk application for multiple jobs
        """
        return self.application_manager.setup_bulk_apply(job_ids, user_profile)
    
    def submit_bulk_applications(self, bulk_session_id: str, applications_data: List[Dict]) -> Dict[str, Any]:
        """
        Submit bulk applications
        """
        return self.application_manager.execute_bulk_apply(bulk_session_id, applications_data)
    
    def get_application_dashboard(self) -> Dict[str, Any]:
        """
        Get application tracking dashboard
        """
        return self.application_manager.get_application_dashboard()
    
    def update_application_status(self, application_id: str, status: str, notes: str = None) -> Dict[str, Any]:
        """
        Update application status
        """
        return self.application_manager.track_application_status(application_id, status, notes)
    
    def get_application_assistance(self, job_id: str, user_profile: Dict) -> Dict[str, Any]:
        """
        Get detailed application assistance
        """
        return self.recommender.get_application_assistance(job_id, user_profile)
    
    def _get_sample_jobs(self) -> List[Dict]:
        """
        Get sample job data for demonstration
        """
        return [
            {
                'id': 'job_1',
                'title': 'Senior Machine Learning Engineer',
                'company': 'TechCorp AI',
                'location': 'San Francisco, CA',
                'description': 'Join our AI team to build cutting-edge machine learning models. Work with Python, TensorFlow, and AWS.',
                'requirements': ['Python', 'Machine Learning', 'TensorFlow', 'AWS', 'PhD preferred'],
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'AWS', 'Deep Learning'],
                'salary_min': 150000,
                'salary_max': 220000,
                'salary_currency': 'USD',
                'experience_level': 'senior',
                'employment_type': 'Full Time',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'company_website',
                'apply_url': 'https://techcorp.com/careers/ml-engineer',
                'remote_allowed': True,
                'company_size': 'Large (1000+ employees)',
                'industry': 'Technology'
            },
            {
                'id': 'job_2',
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'location': 'Remote',
                'description': 'Build web applications using React and Node.js. Join a fast-growing startup!',
                'requirements': ['React', 'Node.js', 'JavaScript', 'MongoDB', '2+ years experience'],
                'skills': ['React', 'Node.js', 'JavaScript', 'MongoDB', 'HTML', 'CSS'],
                'salary_min': 80000,
                'salary_max': 120000,
                'salary_currency': 'USD',
                'experience_level': 'mid',
                'employment_type': 'Full Time',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'linkedin',
                'apply_url': 'https://linkedin.com/jobs/startupxyz',
                'remote_allowed': True,
                'company_size': 'Small (10-50 employees)',
                'industry': 'Technology'
            },
            {
                'id': 'job_3',
                'title': 'Frontend Developer Intern',
                'company': 'Digital Agency Pro',
                'location': 'New York, NY',
                'description': 'Summer internship program for frontend development. Learn React, TypeScript, and modern web development.',
                'requirements': ['HTML', 'CSS', 'JavaScript', 'React basics', 'Student status'],
                'skills': ['HTML', 'CSS', 'JavaScript', 'React', 'TypeScript'],
                'salary_min': 20,
                'salary_max': 25,
                'salary_currency': 'USD',
                'experience_level': 'entry',
                'employment_type': 'Internship',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'indeed',
                'apply_url': 'https://indeed.com/jobs/digital-agency-intern',
                'remote_allowed': False,
                'company_size': 'Medium (50-200 employees)',
                'industry': 'Marketing & Advertising'
            },
            {
                'id': 'job_4',
                'title': 'Data Scientist',
                'company': 'DataCorp Analytics',
                'location': 'Austin, TX',
                'description': 'Analyze large datasets and build predictive models. Work with Python, SQL, and cloud platforms.',
                'requirements': ['Python', 'SQL', 'Statistics', 'Machine Learning', 'Data Visualization'],
                'skills': ['Python', 'SQL', 'Pandas', 'Scikit-learn', 'Tableau', 'AWS'],
                'salary_min': 95000,
                'salary_max': 140000,
                'salary_currency': 'USD',
                'experience_level': 'mid',
                'employment_type': 'Full Time',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'glassdoor',
                'apply_url': 'https://glassdoor.com/jobs/datacorp',
                'remote_allowed': True,
                'company_size': 'Medium (200-500 employees)',
                'industry': 'Data & Analytics'
            },
            {
                'id': 'job_5',
                'title': 'DevOps Engineer',
                'company': 'CloudFirst Inc',
                'location': 'Seattle, WA',
                'description': 'Manage cloud infrastructure and CI/CD pipelines. Work with AWS, Docker, and Kubernetes.',
                'requirements': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux', '3+ years experience'],
                'skills': ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Linux'],
                'salary_min': 110000,
                'salary_max': 160000,
                'salary_currency': 'USD',
                'experience_level': 'mid',
                'employment_type': 'Full Time',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'company_website',
                'apply_url': 'https://cloudfirst.com/careers/devops',
                'remote_allowed': True,
                'company_size': 'Large (500+ employees)',
                'industry': 'Cloud Services'
            },
            {
                'id': 'intern_1',
                'title': 'Software Engineering Intern',
                'company': 'BigTech Corp',
                'location': 'Mountain View, CA',
                'description': 'Summer internship program for computer science students. Work on real projects with mentorship.',
                'requirements': ['Programming experience', 'CS student', 'Problem solving'],
                'skills': ['Python', 'Java', 'Algorithms', 'Data Structures'],
                'salary_min': 7000,
                'salary_max': 8500,
                'salary_currency': 'USD',
                'experience_level': 'entry',
                'employment_type': 'Internship',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'company_website',
                'apply_url': 'https://bigtech.com/internships',
                'remote_allowed': False,
                'company_size': 'Large (10000+ employees)',
                'industry': 'Technology'
            },
            {
                'id': 'intern_2',
                'title': 'Data Analysis Intern',
                'company': 'Research Institute',
                'location': 'Boston, MA',
                'description': 'Part-time internship analyzing research data. Great for students interested in data science.',
                'requirements': ['Excel', 'Basic statistics', 'Student status'],
                'skills': ['Excel', 'Python', 'Statistics', 'Data Visualization'],
                'salary_min': 15,
                'salary_max': 20,
                'salary_currency': 'USD',
                'experience_level': 'entry',
                'employment_type': 'Internship',
                'posted_date': datetime.now(),
                'expires_date': None,
                'source': 'university_portal',
                'apply_url': 'https://university.edu/jobs/research-intern',
                'remote_allowed': True,
                'company_size': 'Medium (100-300 employees)',
                'industry': 'Research & Education'
            }
        ]

# Flask API endpoints
app = Flask(__name__)
CORS(app)

job_search_api = JobSearchAPI()

@app.route('/api/jobs/search', methods=['POST'])
def search_jobs():
    """Search and recommend jobs based on resume analysis"""
    try:
        data = request.get_json()
        resume_analysis = data.get('resume_analysis', {})
        preferences = data.get('preferences', {})
        
        result = job_search_api.search_and_recommend_jobs(resume_analysis, preferences)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/jobs/quick-search', methods=['POST'])
def quick_job_search():
    """Quick job search based on skills"""
    try:
        data = request.get_json()
        skills = data.get('skills', [])
        experience_level = data.get('experience_level', 'mid')
        
        result = job_search_api.get_quick_job_matches(skills, experience_level)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/jobs/save', methods=['POST'])
def save_job():
    """Save a job for later"""
    try:
        data = request.get_json()
        job_data = data.get('job', {})
        folder = data.get('folder', 'favorites')
        
        result = job_search_api.save_job(job_data, folder)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/jobs/saved', methods=['GET'])
def get_saved_jobs():
    """Get saved jobs"""
    try:
        folder = request.args.get('folder')
        result = job_search_api.get_saved_jobs(folder)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/apply', methods=['POST'])
def apply_to_job():
    """Apply to a job"""
    try:
        data = request.get_json()
        job_data = data.get('job', {})
        user_profile = data.get('user_profile', {})
        application_type = data.get('type', 'standard')
        
        result = job_search_api.apply_to_job(job_data, user_profile, application_type)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/bulk-apply', methods=['POST'])
def bulk_apply():
    """Set up bulk application"""
    try:
        data = request.get_json()
        job_ids = data.get('job_ids', [])
        user_profile = data.get('user_profile', {})
        
        result = job_search_api.bulk_apply_to_jobs(job_ids, user_profile)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/bulk-submit', methods=['POST'])
def submit_bulk_applications():
    """Submit bulk applications"""
    try:
        data = request.get_json()
        bulk_session_id = data.get('bulk_session_id', '')
        applications_data = data.get('applications', [])
        
        result = job_search_api.submit_bulk_applications(bulk_session_id, applications_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/dashboard', methods=['GET'])
def get_dashboard():
    """Get application dashboard"""
    try:
        result = job_search_api.get_application_dashboard()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/<application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    """Update application status"""
    try:
        data = request.get_json()
        status = data.get('status', '')
        notes = data.get('notes', '')
        
        result = job_search_api.update_application_status(application_id, status, notes)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/applications/assistance/<job_id>', methods=['POST'])
def get_application_assistance(job_id):
    """Get application assistance for a job"""
    try:
        data = request.get_json()
        user_profile = data.get('user_profile', {})
        
        result = job_search_api.get_application_assistance(job_id, user_profile)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("Starting Job Search and Application API...")
    print("Available endpoints:")
    print("- POST /api/jobs/search - Search and recommend jobs")
    print("- POST /api/jobs/quick-search - Quick job search by skills")
    print("- POST /api/jobs/save - Save job for later")
    print("- GET /api/jobs/saved - Get saved jobs")
    print("- POST /api/applications/apply - Apply to job")
    print("- POST /api/applications/bulk-apply - Setup bulk apply")
    print("- POST /api/applications/bulk-submit - Submit bulk applications")
    print("- GET /api/applications/dashboard - Get application dashboard")
    print("- PUT /api/applications/<id>/status - Update application status")
    print("- POST /api/applications/assistance/<job_id> - Get application help")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
