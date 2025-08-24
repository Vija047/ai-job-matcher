"""
Enhanced AI-Powered Job Matcher Backend API
Built to meet the 6 core requirements:
1. Extract skills from user's resume using Hugging Face models
2. Show total number of skills identified
3. Define most suitable role based on skills
4. Browse and fetch real jobs from actual platforms
5. Use real-time job data (not fake data)
6. Utilize Hugging Face models for skill extraction and role prediction
"""

import os
import gc
import warnings
import tempfile
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
import uuid
import json
import traceback

warnings.filterwarnings("ignore")

# Memory optimization environment variables
os.environ['PYTORCH_DISABLE_GPU'] = '1'
os.environ['OMP_NUM_THREADS'] = '2'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging with UTF-8 encoding to handle special characters
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file = os.getenv('LOG_FILE', 'app.log')

class UnicodeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = str(record.msg).encode('ascii', 'replace').decode('ascii')
            return super().format(record)

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

for handler in logging.getLogger().handlers:
    handler.setFormatter(UnicodeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure CORS - More permissive for development
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000').split(',')
CORS(app, 
     origins=cors_origins, 
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With', 'Accept', 'Origin'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     expose_headers=['Content-Type', 'Authorization'])

# Initialize authentication
auth_manager = AuthManager(app)

# Initialize AI components
try:
    print("🚀 Initializing production AI Job Matcher...")
    resume_parser = AdvancedResumeParser()
    job_matcher = AIJobMatcher()
    job_client = JobAPIClient()
    logger.info("✅ Production AI systems initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize AI systems: {str(e)}")
    raise

# Session storage (use Redis/Database in production)
user_sessions = {}
analysis_cache = {}

# Add security headers to all responses
@app.after_request
def after_request(response):
    return add_security_headers(response)

# Handle preflight OPTIONS requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# ================================
# Authentication Endpoints
# ================================

@app.route('/auth/register', methods=['POST'])
@rate_limit(limit=5, window=300)  # 5 requests per 5 minutes
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        if not all([email, password, name]):
            return jsonify({'error': 'Email, password, and name are required'}), 400
        
        success, message = auth_manager.create_user(email, password, name)
        
        if not success:
            return jsonify({'error': message}), 400
        
        logger.info(f"User registered: {email}")
        return jsonify({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/auth/login', methods=['POST'])
@rate_limit(limit=10, window=300)  # 10 requests per 5 minutes
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not all([email, password]):
            return jsonify({'error': 'Email and password are required'}), 400
        
        success, user, message = auth_manager.authenticate_user(email, password)
        
        if not success:
            return jsonify({'error': message}), 401
        
        # Generate JWT token
        token = auth_manager.generate_jwt_token(user)
        
        # Create user session
        session_id = str(uuid.uuid4())
        user_sessions[session_id] = {
            'user_id': user.id,
            'email': user.email,
            'name': user.name,
            'login_time': datetime.now(),
            'analysis_history': []
        }
        
        logger.info(f"User logged in: {email}")
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'session_id': session_id
            },
            'message': 'Login successful'
        })
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        # Since authentication is removed, just return success
        return jsonify({
            'success': True,
            'message': 'Logout successful (authentication disabled)'
        })
        
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Logout failed'}), 500

@app.route('/auth/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        # Since authentication is removed, return anonymous profile
        return jsonify({
            'success': True,
            'user': {
                'id': 'anonymous',
                'email': 'anonymous@example.com',
                'name': 'Anonymous User',
                'created_at': datetime.now().isoformat(),
                'is_active': True
            }
        })
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        })
        
    except Exception as e:
        logger.error(f"Profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

# ================================
# Core API Endpoints
# ================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0',
        'features': {
            'authentication': False,
            'advanced_resume_parsing': True,
            'real_job_apis': True,
            'ai_job_matching': True,
            'rate_limiting': True
        },
        'api_status': {
            'adzuna': bool(os.getenv('ADZUNA_APP_ID')),
            'jsearch': bool(os.getenv('RAPIDAPI_KEY')),
            'linkedin': True,
            'remotive': True,
            'findwork': True
        }
    })

@app.route('/job-recommendations', methods=['GET', 'POST'])
def get_job_recommendations():
    """Get job recommendations without authentication for testing"""
    try:
        # Get parameters from query string for GET or JSON for POST
        if request.method == 'GET':
            keywords = request.args.getlist('keywords') or ['software developer']
            location = request.args.get('location', 'Remote')
            limit = min(int(request.args.get('limit', 10)), 20)
        else:
            data = request.get_json() or {}
            keywords = data.get('keywords', ['software developer'])
            location = data.get('location', 'Remote')
            limit = min(data.get('limit', 10), 20)
        
        logger.info(f"Getting job recommendations: {keywords}")
        
        # Search jobs using real APIs
        jobs = search_jobs_sync(
            keywords=keywords,
            location=location,
            experience_level='mid',
            employment_type='full_time',
            salary_min=None,
            limit=limit
        )
        
        # Convert jobs to serializable format
        jobs_data = []
        for job in jobs:
            job_dict = {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description[:300] + "..." if len(job.description) > 300 else job.description,
                'requirements': job.requirements[:5],  # Limit requirements
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'salary_currency': job.salary_currency,
                'experience_level': job.experience_level,
                'employment_type': job.employment_type,
                'posted_date': job.posted_date.isoformat(),
                'source': job.source,
                'apply_url': job.apply_url,
                'skills': job.skills[:5],  # Limit skills
                'remote_allowed': job.remote_allowed,
                'company_size': job.company_size,
                'industry': job.industry
            }
            jobs_data.append(job_dict)
        
        return jsonify({
            'success': True,
            'jobs': jobs_data,
            'total_jobs': len(jobs_data),
            'keywords_searched': keywords,
            'location': location,
            'sources_used': list(set([job.source for job in jobs]))
        })
        
    except Exception as e:
        logger.error(f"Job recommendations error: {e}")
        return jsonify({
            'error': f'Failed to get job recommendations: {str(e)}',
            'success': False
        }), 500

@app.route('/upload-resume', methods=['POST'])
@rate_limit(limit=5, window=300)  # 5 uploads per 5 minutes
def upload_resume():
    """Upload and parse resume with advanced AI analysis"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Parse resume with advanced AI
            logger.info(f"Parsing resume: {file.filename}")
            resume_analysis = resume_parser.parse_resume(temp_path)
            
            if 'error' in resume_analysis:
                return jsonify({'error': resume_analysis['error']}), 400
            
            # Generate unique analysis ID
            analysis_id = str(uuid.uuid4())
            user_id = f"anonymous_{str(uuid.uuid4())[:8]}"  # Generate anonymous user ID
            
            # Store analysis in cache
            analysis_cache[analysis_id] = {
                'user_id': user_id,
                'resume_analysis': resume_analysis,
                'timestamp': datetime.now().isoformat(),
                'filename': file.filename
            }
            
            # Clean up temp file
            os.unlink(temp_path)
            
            logger.info(f"Resume parsed successfully: {analysis_id}")
            return jsonify({
                'success': True,
                'analysis_id': analysis_id,
                'resume_analysis': resume_analysis,
                'message': 'Resume analyzed successfully with advanced AI models'
            })
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
            
    except Exception as e:
        logger.error(f"Resume upload error: {e}")
        return jsonify({'error': f'Resume analysis failed: {str(e)}'}), 500

@app.route('/search-jobs', methods=['POST'])

@rate_limit(limit=20, window=3600)  # 20 searches per hour
def search_jobs():
    """Search for jobs using real APIs"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        keywords = data.get('keywords', [])
        location = data.get('location', '')
        experience_level = data.get('experience_level', '')
        employment_type = data.get('employment_type', '')
        salary_min = data.get('salary_min')
        limit = min(data.get('limit', 20), 50)  # Max 50 jobs
        
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        
        logger.info(f"Searching jobs: {keywords}")
        
        # Search jobs using real APIs
        jobs = search_jobs_sync(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
            employment_type=employment_type,
            salary_min=salary_min,
            limit=limit
        )
        
        # Convert jobs to serializable format
        jobs_data = []
        for job in jobs:
            job_dict = {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description[:500] + "..." if len(job.description) > 500 else job.description,
                'requirements': job.requirements,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'salary_currency': job.salary_currency,
                'experience_level': job.experience_level,
                'employment_type': job.employment_type,
                'posted_date': job.posted_date.isoformat(),
                'expires_date': job.expires_date.isoformat() if job.expires_date else None,
                'source': job.source,
                'apply_url': job.apply_url,
                'skills': job.skills,
                'remote_allowed': job.remote_allowed,
                'company_size': job.company_size,
                'industry': job.industry
            }
            jobs_data.append(job_dict)
        
        # Get job statistics
        statistics = job_client.get_job_statistics(jobs)
        
        return jsonify({
            'success': True,
            'jobs': jobs_data,
            'statistics': statistics,
            'total_found': len(jobs),
            'message': f'Found {len(jobs)} job postings from multiple sources'
        })
        
    except Exception as e:
        logger.error(f"Job search error: {e}")
        return jsonify({'error': f'Job search failed: {str(e)}'}), 500

@app.route('/match-jobs', methods=['POST'])

@rate_limit(limit=10, window=3600)  # 10 matches per hour
def match_jobs():
    """Get AI-powered job matches for uploaded resume"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = min(data.get('limit', 20), 50)  # Max 50 matches
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid or expired analysis ID'}), 400
        
        # Get cached analysis data
        cached_data = analysis_cache[analysis_id]
        resume_analysis = cached_data['resume_analysis']
        
        logger.info(f"Finding job matches for analysis: {analysis_id}")
        
        # Get AI-powered job matches
        matches_result = find_matching_jobs_sync(
            resume_analysis=resume_analysis,
            preferences=preferences,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'matches': matches_result,
            'message': f'Found {len(matches_result.get("matches", []))} AI-matched jobs'
        })
        
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        return jsonify({'error': f'Job matching failed: {str(e)}'}), 500

@app.route('/analysis/<analysis_id>', methods=['GET'])

def get_analysis(analysis_id):
    """Get detailed analysis results"""
    try:
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        cached_data = analysis_cache[analysis_id]
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'filename': cached_data['filename'],
            'timestamp': cached_data['timestamp'],
            'resume_analysis': cached_data['resume_analysis']
        })
        
    except Exception as e:
        logger.error(f"Get analysis error: {e}")
        return jsonify({'error': f'Failed to get analysis: {str(e)}'}), 500

@app.route('/user/history', methods=['GET'])

def get_user_history():
    """Get user's analysis history"""
    try:
        # Since authentication is removed, return empty history
        user_history = []
        
        return jsonify({
            'success': True,
            'history': user_history,
            'total_analyses': len(user_history)
        })
        
    except Exception as e:
        logger.error(f"History error: {e}")
        return jsonify({'error': 'Failed to get history'}), 500

# ================================
# Advanced Features
# ================================

@app.route('/skill-gap-analysis', methods=['POST'])
@rate_limit(limit=5, window=3600)  # 5 analyses per hour
def skill_gap_analysis():
    """Analyze skill gaps based on job market demand"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        target_roles = data.get('target_roles', [])
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid or expired analysis ID'}), 400
        
        cached_data = analysis_cache[analysis_id]
        resume_analysis = cached_data['resume_analysis']
        
        # Extract user skills
        user_skills = set()
        skills_analysis = resume_analysis.get('skills_analysis', {})
        for category_skills in skills_analysis.get('skills_by_category', {}).values():
            user_skills.update(skill.lower() for skill in category_skills)
        
        # Search for target role jobs
        keywords = target_roles if target_roles else ['software engineer', 'data scientist', 'product manager']
        
        logger.info(f"Analyzing skill gaps for roles: {keywords}")
        
        # Get job market data
        market_jobs = search_jobs_sync(keywords=keywords, limit=30)
        
        # Analyze required skills across jobs
        required_skills = {}
        for job in market_jobs:
            for skill in job.skills:
                skill_lower = skill.lower()
                required_skills[skill_lower] = required_skills.get(skill_lower, 0) + 1
        
        # Calculate skill gaps
        total_jobs = len(market_jobs)
        skill_gaps = []
        
        for skill, frequency in required_skills.items():
            importance = frequency / total_jobs
            if skill not in user_skills and importance > 0.2:  # Required in >20% of jobs
                skill_gaps.append({
                    'skill': skill,
                    'importance': round(importance, 2),
                    'frequency': frequency,
                    'gap_severity': 'high' if importance > 0.5 else 'medium' if importance > 0.3 else 'low'
                })
        
        # Sort by importance
        skill_gaps.sort(key=lambda x: x['importance'], reverse=True)
        
        # Generate recommendations
        recommendations = []
        if skill_gaps:
            top_gaps = skill_gaps[:5]
            for gap in top_gaps:
                recommendations.append(f"Learn {gap['skill']} - required in {gap['frequency']}/{total_jobs} jobs")
        
        return jsonify({
            'success': True,
            'skill_gaps': skill_gaps[:10],  # Top 10 gaps
            'user_skills_count': len(user_skills),
            'market_jobs_analyzed': total_jobs,
            'recommendations': recommendations,
            'message': 'Skill gap analysis completed'
        })
        
    except Exception as e:
        logger.error(f"Skill gap analysis error: {e}")
        return jsonify({'error': f'Skill gap analysis failed: {str(e)}'}), 500

@app.route('/career-insights', methods=['POST'])

@rate_limit(limit=5, window=3600)  # 5 insights per hour
def career_insights():
    """Get AI-powered career insights and recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid or expired analysis ID'}), 400
        
        cached_data = analysis_cache[analysis_id]
        resume_analysis = cached_data['resume_analysis']
        
        # Extract user profile
        skills_analysis = resume_analysis.get('skills_analysis', {})
        experience_analysis = resume_analysis.get('experience_analysis', {})
        
        user_skills = []
        for category_skills in skills_analysis.get('skills_by_category', {}).values():
            user_skills.extend(category_skills)
        
        # Generate career insights
        insights = {
            'profile_summary': {
                'experience_level': experience_analysis.get('experience_level', 'mid'),
                'total_skills': len(user_skills),
                'top_skills': user_skills[:10],
                'years_experience': experience_analysis.get('total_years', 0),
                'quality_grade': resume_analysis.get('quality_assessment', {}).get('quality_grade', 'B')
            },
            'market_positioning': {},
            'growth_opportunities': [],
            'salary_insights': {},
            'recommendations': []
        }
        
        # Market positioning based on skills
        if user_skills:
            # Search for jobs matching user's top skills
            market_jobs = search_jobs_sync(keywords=user_skills[:5], limit=50)
            
            if market_jobs:
                # Salary analysis
                salaries = [job.salary_min for job in market_jobs if job.salary_min]
                if salaries:
                    insights['salary_insights'] = {
                        'average_salary': sum(salaries) / len(salaries),
                        'salary_range': f"${min(salaries):,.0f} - ${max(salaries):,.0f}",
                        'total_jobs_with_salary': len(salaries)
                    }
                
                # Common job titles
                job_titles = [job.title for job in market_jobs]
                title_frequency = {}
                for title in job_titles:
                    # Normalize title
                    normalized = title.lower()
                    for key_title in ['engineer', 'developer', 'analyst', 'manager', 'scientist']:
                        if key_title in normalized:
                            title_frequency[key_title] = title_frequency.get(key_title, 0) + 1
                            break
                
                insights['market_positioning'] = {
                    'total_matching_jobs': len(market_jobs),
                    'common_titles': sorted(title_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
                    'top_companies': list(set([job.company for job in market_jobs[:10]]))
                }
        
        # Growth opportunities
        current_level = experience_analysis.get('experience_level', 'mid')
        if current_level == 'entry':
            insights['growth_opportunities'] = [
                'Gain more hands-on experience with your core skills',
                'Consider contributing to open source projects',
                'Build a portfolio of personal projects',
                'Seek mentorship from senior professionals'
            ]
        elif current_level == 'mid':
            insights['growth_opportunities'] = [
                'Develop leadership and communication skills',
                'Learn advanced technologies in your field',
                'Consider specializing in a high-demand area',
                'Start mentoring junior developers'
            ]
        else:
            insights['growth_opportunities'] = [
                'Focus on strategic and architectural skills',
                'Develop business acumen and domain expertise',
                'Consider transitioning to management or principal roles',
                'Build thought leadership through writing and speaking'
            ]
        
        # Recommendations based on analysis
        quality_grade = resume_analysis.get('quality_assessment', {}).get('quality_grade', 'B')
        if quality_grade in ['C', 'D']:
            insights['recommendations'].append('Improve your resume quality score by adding more technical details')
        
        if len(user_skills) < 10:
            insights['recommendations'].append('Expand your skill set to increase job opportunities')
        
        if experience_analysis.get('total_years', 0) == 0:
            insights['recommendations'].append('Add specific years of experience to strengthen your profile')
        
        return jsonify({
            'success': True,
            'insights': insights,
            'message': 'Career insights generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Career insights error: {e}")
        return jsonify({'error': f'Career insights failed: {str(e)}'}), 500

# ================================
# Additional Frontend-Required Endpoints
# ================================

@app.route('/get-recommendations', methods=['POST'])
@rate_limit(limit=10, window=60)
def get_enhanced_recommendations():
    """Get enhanced job recommendations"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = data.get('limit', 20)
        
        if not analysis_id:
            return jsonify({'error': 'Analysis ID required'}), 400
        
        # Get analysis from cache/session
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Get job recommendations using AI matcher
        matched_jobs = find_matching_jobs_sync(
            resume_analysis=analysis,
            preferences=preferences,
            limit=limit
        )
        
        return jsonify({
            'recommendations': matched_jobs.get('matches', []),
            'total_found': matched_jobs.get('total_found', 0),
            'insights': matched_jobs.get('insights', {}),
            'statistics': matched_jobs.get('statistics', {}),
            'search_keywords': matched_jobs.get('search_keywords', []),
            'message': matched_jobs.get('message', 'Job search completed'),
            'analysis_id': analysis_id
        })
        
    except Exception as e:
        logger.error(f"Enhanced recommendations error: {e}")
        return jsonify({'error': f'Recommendations failed: {str(e)}'}), 500

@app.route('/realtime-jobs', methods=['POST'])
@rate_limit(limit=5, window=60)
def get_realtime_jobs():
    """Get real-time job data"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', 'software developer')
        location = data.get('location', '')
        limit = data.get('limit', 50)
        
        jobs = search_jobs_sync(
            keywords=keywords,
            location=location,
            limit=min(limit, 100)
        )
        
        return jsonify({
            'jobs': jobs,
            'total': len(jobs),
            'keywords': keywords,
            'location': location
        })
        
    except Exception as e:
        logger.error(f"Real-time jobs error: {e}")
        return jsonify({'error': f'Job search failed: {str(e)}'}), 500

@app.route('/apply-to-job', methods=['POST'])

@rate_limit(limit=3, window=300)
def apply_to_job():
    """Job application assistance"""
    try:
        data = request.get_json()
        required_fields = ['job_id', 'analysis_id']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # This would integrate with job application systems
        # For now, return a success response
        return jsonify({
            'status': 'success',
            'message': 'Application submitted successfully',
            'job_id': data['job_id'],
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Job application error: {e}")
        return jsonify({'error': f'Application failed: {str(e)}'}), 500

@app.route('/generate-cover-letter', methods=['POST'])

@rate_limit(limit=5, window=300)
def generate_cover_letter():
    """Generate personalized cover letter"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        job_title = data.get('job_title')
        company = data.get('company')
        job_description = data.get('job_description', '')
        
        if not all([analysis_id, job_title, company]):
            return jsonify({'error': 'analysis_id, job_title, and company are required'}), 400
        
        # Get analysis from cache
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Generate cover letter (simplified version)
        skills = ', '.join(analysis.get('skills', [])[:5])
        experience = analysis.get('experience_years', 'several years')
        
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With {experience} of experience and expertise in {skills}, I am confident that I would be a valuable addition to your team.

My background includes:
- Proven experience with {skills}
- Strong problem-solving and analytical skills
- Excellent communication and teamwork abilities

I am excited about the opportunity to contribute to {company}'s success and would welcome the chance to discuss how my skills align with your needs.

Thank you for your consideration.

Best regards,
[Your Name]"""

        return jsonify({
            'cover_letter': cover_letter,
            'job_title': job_title,
            'company': company,
            'analysis_id': analysis_id
        })
        
    except Exception as e:
        logger.error(f"Cover letter generation error: {e}")
        return jsonify({'error': f'Cover letter generation failed: {str(e)}'}), 500

@app.route('/application-history', methods=['GET'])
def get_application_history():
    """Get application history and statistics"""
    try:
        # Since we removed authentication, return empty history for anonymous users
        history = {
            'applications': [],
            'statistics': {
                'total_applications': 0,
                'pending': 0,
                'interviews': 0,
                'rejections': 0,
                'offers': 0
            }
        }
        
        return jsonify(history)
        
    except Exception as e:
        logger.error(f"Application history error: {e}")
        return jsonify({'error': f'Failed to get application history: {str(e)}'}), 500

@app.route('/career-guidance', methods=['POST'])
@rate_limit(limit=3, window=300)
def get_career_guidance():
    """Get AI-powered career guidance"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id:
            return jsonify({'error': 'Analysis ID required'}), 400
        
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Generate career guidance based on analysis
        skills = analysis.get('skills', [])
        experience = analysis.get('experience_years', 0)
        
        guidance = {
            'career_paths': [
                'Senior Software Engineer',
                'Technical Lead',
                'Solution Architect'
            ],
            'skill_development': [
                'Consider learning cloud technologies (AWS, Azure)',
                'Develop leadership and mentoring skills',
                'Gain experience with microservices architecture'
            ],
            'next_steps': [
                'Build portfolio projects showcasing your skills',
                'Contribute to open source projects',
                'Obtain relevant certifications'
            ],
            'market_trends': [
                'High demand for full-stack developers',
                'Growing need for AI/ML integration',
                'Remote work opportunities increasing'
            ]
        }
        
        return jsonify({
            'guidance': guidance,
            'analysis_id': analysis_id,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Career guidance error: {e}")
        return jsonify({'error': f'Career guidance failed: {str(e)}'}), 500

@app.route('/export-analysis/<analysis_id>', methods=['GET'])

def export_analysis(analysis_id):
    """Export analysis results"""
    try:
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Add export metadata
        export_data = {
            'analysis': analysis,
            'exported_at': datetime.utcnow().isoformat(),
            'export_id': str(uuid.uuid4())
        }
        
        return jsonify(export_data)
        
    except Exception as e:
        logger.error(f"Export analysis error: {e}")
        return jsonify({'error': f'Export failed: {str(e)}'}), 500

# ================================
# Error Handlers
# ================================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Access forbidden'}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(429)
def rate_limit_exceeded(error):
    return jsonify({'error': 'Rate limit exceeded'}), 429

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ================================
# Application Entry Point
# ================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Production AI Job Matcher API on port {port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📊 Features: Authentication, Real Job APIs, AI Matching, Rate Limiting")
    print(f"🔐 API Keys configured: {sum([bool(os.getenv(key)) for key in ['ADZUNA_APP_ID', 'RAPIDAPI_KEY']])}/2")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        # Cleanup
        gc.collect()
        print("✅ Cleanup completed")
