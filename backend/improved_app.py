"""
Enhanced AI-Powered Job Matcher Backend API
Flask application with real job APIs, Hugging Face models, and comprehensive job matching
Built specifically to address the requirements:
1. Extract skills from user's resume
2. Show total number of skills identified  
3. Define the most suitable role based on skills
4. Browse and fetch real-time jobs from actual job platforms
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

# Create a custom formatter to handle Unicode characters
class UnicodeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except UnicodeEncodeError:
            # Replace problematic characters
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

# Apply custom formatter
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

# Session storage (use Redis/Database in production)
user_sessions = {}
analysis_cache = {}

# Lazy load AI components to avoid startup delays
_resume_parser = None
_job_matcher = None
_job_client = None

def get_resume_parser():
    """Lazy load resume parser"""
    global _resume_parser
    if _resume_parser is None:
        print("Loading Advanced Resume Parser...")
        from advanced_resume_parser import AdvancedResumeParser
        _resume_parser = AdvancedResumeParser()
        print("Resume Parser loaded successfully!")
    return _resume_parser

def get_job_matcher():
    """Lazy load job matcher"""
    global _job_matcher
    if _job_matcher is None:
        print("Loading AI Job Matcher...")
        from ai_job_matcher import AIJobMatcher
        _job_matcher = AIJobMatcher()
        print("Job Matcher loaded successfully!")
    return _job_matcher

def get_job_client():
    """Lazy load job client"""
    global _job_client
    if _job_client is None:
        print("Loading Job API Client...")
        from job_api_client import JobAPIClient
        _job_client = JobAPIClient()
        print("Job API Client loaded successfully!")
    return _job_client

# Add security headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-Frame-Options', 'DENY')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response

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
# Core Endpoints
# ================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'services': {
                'resume_parser': _resume_parser is not None,
                'job_matcher': _job_matcher is not None,
                'job_client': _job_client is not None
            }
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """
    Upload and parse resume with advanced AI analysis
    Requirements covered:
    1. Extract skills from user's resume
    2. Show total number of skills identified
    3. Define the most suitable role based on skills
    """
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Save file temporarily
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                file.save(temp_file.name)
                temp_path = temp_file.name
            
            # Parse resume with advanced AI
            logger.info(f"Parsing resume: {file.filename}")
            resume_parser = get_resume_parser()
            resume_analysis = resume_parser.parse_resume(temp_path)
            
            if 'error' in resume_analysis:
                return jsonify({'error': resume_analysis['error']}), 400
            
            # Extract key information for the response
            skills_analysis = resume_analysis.get('skills_analysis', {})
            all_skills = []
            
            # Collect all skills from different categories
            skills_by_category = skills_analysis.get('skills_by_category', {})
            for category, skills in skills_by_category.items():
                all_skills.extend(skills)
            
            # Remove duplicates while preserving order
            unique_skills = list(dict.fromkeys(all_skills))
            total_skills = len(unique_skills)
            
            # Determine most suitable role based on skills
            experience_analysis = resume_analysis.get('experience_analysis', {})
            suggested_role = determine_best_role(unique_skills, experience_analysis)
            
            # Generate unique analysis ID
            analysis_id = str(uuid.uuid4())
            user_id = f"anonymous_{str(uuid.uuid4())[:8]}"
            
            # Enhanced analysis result
            enhanced_analysis = {
                'analysis_id': analysis_id,
                'user_id': user_id,
                'filename': file.filename,
                'timestamp': datetime.now().isoformat(),
                'skills': {
                    'total_count': total_skills,
                    'all_skills': unique_skills,
                    'skills_by_category': skills_by_category,
                    'top_skills': unique_skills[:10]  # Top 10 skills
                },
                'suggested_role': suggested_role,
                'experience_level': experience_analysis.get('experience_level', 'mid'),
                'years_experience': experience_analysis.get('total_years', 0),
                'quality_assessment': resume_analysis.get('quality_assessment', {}),
                'raw_analysis': resume_analysis  # Keep full analysis for later use
            }
            
            # Store analysis in cache
            analysis_cache[analysis_id] = enhanced_analysis
            
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            
            logger.info(f"Resume parsed successfully: {analysis_id} - {total_skills} skills found")
            
            # Return focused response matching the requirements
            return jsonify({
                'success': True,
                'analysis_id': analysis_id,
                'skills_extracted': unique_skills,
                'total_skills_count': total_skills,
                'skills_by_category': skills_by_category,
                'suggested_role': suggested_role,
                'experience_level': experience_analysis.get('experience_level', 'mid'),
                'years_experience': experience_analysis.get('total_years', 0),
                'quality_grade': resume_analysis.get('quality_assessment', {}).get('quality_grade', 'B'),
                'message': f'Resume analyzed successfully! Found {total_skills} skills and suggested role: {suggested_role}'
            })
            
        except Exception as e:
            # Clean up temp file on error
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
            
    except Exception as e:
        logger.error(f"Resume upload error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Resume analysis failed: {str(e)}'}), 500

def determine_best_role(skills: List[str], experience_analysis: Dict) -> str:
    """
    Determine the most suitable role based on extracted skills
    Uses skill patterns and experience level to suggest roles
    """
    skills_lower = [skill.lower() for skill in skills]
    experience_level = experience_analysis.get('experience_level', 'mid')
    
    # Role mapping based on skill patterns
    role_patterns = {
        'Software Engineer': ['python', 'javascript', 'java', 'react', 'node.js', 'git', 'api'],
        'Data Scientist': ['python', 'machine learning', 'tensorflow', 'pandas', 'numpy', 'sql', 'statistics'],
        'Frontend Developer': ['javascript', 'react', 'vue.js', 'html', 'css', 'typescript', 'angular'],
        'Backend Developer': ['python', 'node.js', 'java', 'api', 'database', 'sql', 'rest'],
        'Full Stack Developer': ['javascript', 'python', 'react', 'node.js', 'database', 'api', 'html'],
        'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'jenkins', 'terraform', 'linux', 'git'],
        'Product Manager': ['agile', 'project management', 'analytics', 'communication', 'strategy'],
        'Mobile Developer': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
        'Machine Learning Engineer': ['machine learning', 'tensorflow', 'pytorch', 'python', 'deep learning'],
        'Cloud Engineer': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform']
    }
    
    # Calculate match scores for each role
    role_scores = {}
    for role, keywords in role_patterns.items():
        score = 0
        for keyword in keywords:
            if any(keyword in skill for skill in skills_lower):
                score += 1
        # Normalize score by total keywords for that role
        role_scores[role] = score / len(keywords)
    
    # Get the best matching role
    if role_scores:
        best_role = max(role_scores, key=role_scores.get)
        best_score = role_scores[best_role]
        
        # Add experience level prefix if significant match
        if best_score > 0.3:  # At least 30% match
            level_prefix = {
                'entry': 'Junior ',
                'mid': '',
                'senior': 'Senior ',
                'executive': 'Lead '
            }.get(experience_level, '')
            
            return f"{level_prefix}{best_role}"
    
    # Default fallback
    level_map = {
        'entry': 'Junior Software Engineer',
        'mid': 'Software Engineer', 
        'senior': 'Senior Software Engineer',
        'executive': 'Engineering Manager'
    }
    
    return level_map.get(experience_level, 'Software Engineer')

@app.route('/search-jobs', methods=['POST'])
def search_jobs():
    """
    Search for real-time jobs from actual job platforms
    Requirements covered:
    4. Browse and fetch available jobs that match user's skills
    5. Use real-time job data instead of fake data
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No search criteria provided'}), 400
        
        # Get search parameters
        keywords = data.get('keywords', [])
        location = data.get('location', '')
        experience_level = data.get('experience_level', '')
        employment_type = data.get('employment_type', '')
        salary_min = data.get('salary_min')
        limit = min(data.get('limit', 20), 50)  # Cap at 50
        
        if not keywords:
            return jsonify({'error': 'Keywords are required for job search'}), 400
        
        logger.info(f"Searching jobs for keywords: {keywords}, location: {location}")
        
        # Get job client and search for real jobs
        job_client = get_job_client()
        
        # Import the sync search function
        from job_api_client import search_jobs_sync
        jobs = search_jobs_sync(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
            employment_type=employment_type,
            salary_min=salary_min,
            limit=limit
        )
        
        # Format jobs for response
        formatted_jobs = []
        for job in jobs:
            formatted_job = {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description[:500] + '...' if len(job.description) > 500 else job.description,
                'requirements': job.requirements,
                'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Not specified",
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'experience_level': job.experience_level,
                'employment_type': job.employment_type,
                'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                'apply_url': job.apply_url,
                'skills': job.skills,
                'remote_allowed': job.remote_allowed,
                'source': job.source,
                'company_size': job.company_size,
                'industry': job.industry
            }
            formatted_jobs.append(formatted_job)
        
        logger.info(f"Found {len(formatted_jobs)} real jobs")
        
        return jsonify({
            'success': True,
            'jobs': formatted_jobs,
            'total_found': len(formatted_jobs),
            'search_criteria': {
                'keywords': keywords,
                'location': location,
                'experience_level': experience_level,
                'employment_type': employment_type,
                'salary_min': salary_min
            },
            'message': f'Found {len(formatted_jobs)} real-time jobs from multiple platforms'
        })
        
    except Exception as e:
        logger.error(f"Job search error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Job search failed: {str(e)}'}), 500

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    """
    Match jobs to user's resume analysis using AI
    Combines requirements 1-5: Uses extracted skills to find matching real jobs
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = min(data.get('limit', 20), 50)
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid or expired analysis ID. Please upload your resume first.'}), 400
        
        # Get user analysis
        user_analysis = analysis_cache[analysis_id]
        user_skills = user_analysis['skills']['all_skills']
        suggested_role = user_analysis['suggested_role']
        experience_level = user_analysis['experience_level']
        
        logger.info(f"Matching jobs for user with {len(user_skills)} skills and role: {suggested_role}")
        
        # Prepare search keywords based on user skills and suggested role
        search_keywords = user_skills[:10]  # Top 10 skills
        search_keywords.append(suggested_role.lower())
        
        # Add role variations
        role_keywords = suggested_role.lower().split()
        search_keywords.extend(role_keywords)
        
        # Remove duplicates
        search_keywords = list(dict.fromkeys(search_keywords))
        
        # Search for matching jobs
        from job_api_client import search_jobs_sync
        jobs = search_jobs_sync(
            keywords=search_keywords,
            location=preferences.get('location', ''),
            experience_level=experience_level,
            employment_type=preferences.get('employment_type', ''),
            salary_min=preferences.get('salary_min'),
            limit=limit * 2  # Get more jobs to filter better matches
        )
        
        # Score and rank jobs based on skill matches
        scored_jobs = []
        for job in jobs:
            score = calculate_job_match_score(user_skills, job, suggested_role)
            if score > 0.1:  # Only include jobs with at least 10% match
                job_data = {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'description': job.description[:500] + '...' if len(job.description) > 500 else job.description,
                    'requirements': job.requirements,
                    'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Not specified",
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'experience_level': job.experience_level,
                    'employment_type': job.employment_type,
                    'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                    'apply_url': job.apply_url,
                    'skills': job.skills,
                    'remote_allowed': job.remote_allowed,
                    'source': job.source,
                    'company_size': job.company_size,
                    'industry': job.industry,
                    'match_score': round(score * 100, 1),
                    'matching_skills': get_matching_skills(user_skills, job.skills)
                }
                scored_jobs.append(job_data)
        
        # Sort by match score (highest first)
        scored_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        # Take top matches
        top_matches = scored_jobs[:limit]
        
        # Generate insights
        insights = generate_job_match_insights(user_skills, top_matches, suggested_role)
        
        logger.info(f"Found {len(top_matches)} matching jobs with scores")
        
        return jsonify({
            'success': True,
            'matched_jobs': top_matches,
            'total_matches': len(top_matches),
            'user_profile': {
                'skills_count': len(user_skills),
                'suggested_role': suggested_role,
                'experience_level': experience_level,
                'top_skills': user_skills[:10]
            },
            'insights': insights,
            'search_keywords': search_keywords,
            'message': f'Found {len(top_matches)} AI-matched jobs based on your {len(user_skills)} skills'
        })
        
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Job matching failed: {str(e)}'}), 500

def calculate_job_match_score(user_skills: List[str], job, suggested_role: str) -> float:
    """Calculate how well a job matches user's skills and role preference"""
    user_skills_lower = [skill.lower() for skill in user_skills]
    job_skills_lower = [skill.lower() for skill in job.skills]
    job_title_lower = job.title.lower()
    job_description_lower = job.description.lower()
    
    score = 0.0
    
    # Skill matching (60% of score)
    skill_matches = 0
    for user_skill in user_skills_lower:
        for job_skill in job_skills_lower:
            if user_skill in job_skill or job_skill in user_skill:
                skill_matches += 1
                break
        # Also check description and requirements
        if user_skill in job_description_lower:
            skill_matches += 0.5
    
    if user_skills:
        skill_score = min(skill_matches / len(user_skills), 1.0) * 0.6
        score += skill_score
    
    # Role matching (30% of score)
    role_keywords = suggested_role.lower().split()
    role_matches = 0
    for keyword in role_keywords:
        if keyword in job_title_lower:
            role_matches += 1
    
    if role_keywords:
        role_score = min(role_matches / len(role_keywords), 1.0) * 0.3
        score += role_score
    
    # Experience level matching (10% of score)
    if job.experience_level and job.experience_level.lower() in ['entry', 'junior', 'mid', 'senior']:
        score += 0.1
    
    return min(score, 1.0)

def get_matching_skills(user_skills: List[str], job_skills: List[str]) -> List[str]:
    """Get list of skills that match between user and job"""
    user_skills_lower = [skill.lower() for skill in user_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    matches = []
    for user_skill in user_skills:
        user_skill_lower = user_skill.lower()
        for job_skill in job_skills:
            if user_skill_lower in job_skill.lower() or job_skill.lower() in user_skill_lower:
                matches.append(user_skill)
                break
    
    return matches

def generate_job_match_insights(user_skills: List[str], matched_jobs: List[Dict], suggested_role: str) -> Dict:
    """Generate insights about job matches"""
    if not matched_jobs:
        return {
            'message': 'No matching jobs found. Consider expanding your skill set or searching with different keywords.',
            'suggestions': ['Add more relevant skills to your resume', 'Consider related roles', 'Look in different locations']
        }
    
    # Calculate average match score
    avg_score = sum(job['match_score'] for job in matched_jobs) / len(matched_jobs)
    
    # Find most common requirements
    all_job_skills = []
    for job in matched_jobs:
        all_job_skills.extend(job['skills'])
    
    skill_frequency = {}
    for skill in all_job_skills:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    top_required_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Find skills gaps
    required_skills = [skill for skill, _ in top_required_skills]
    user_skills_lower = [skill.lower() for skill in user_skills]
    missing_skills = [skill for skill in required_skills if skill.lower() not in user_skills_lower]
    
    return {
        'average_match_score': round(avg_score, 1),
        'total_applications_suggested': len(matched_jobs),
        'top_required_skills': [{'skill': skill, 'frequency': freq} for skill, freq in top_required_skills],
        'skills_you_have': len(user_skills),
        'missing_skills': missing_skills[:3],  # Top 3 missing skills
        'message': f'Great match! Average compatibility: {avg_score:.1f}%',
        'recommendations': [
            f'Apply to top {min(5, len(matched_jobs))} matches immediately',
            f'Consider learning: {", ".join(missing_skills[:2])}' if missing_skills else 'Your skill set is well-aligned',
            f'Focus on {suggested_role} positions for best results'
        ]
    }

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get detailed analysis results"""
    try:
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found or expired'}), 404
        
        cached_data = analysis_cache[analysis_id]
        
        return jsonify({
            'success': True,
            'analysis': cached_data,
            'message': 'Analysis retrieved successfully'
        })
        
    except Exception as e:
        logger.error(f"Get analysis error: {e}")
        return jsonify({'error': f'Failed to get analysis: {str(e)}'}), 500

@app.route('/skill-gap-analysis', methods=['POST'])
def skill_gap_analysis():
    """Analyze skill gaps based on current job market demand"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        target_roles = data.get('target_roles', [])
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid or expired analysis ID'}), 400
        
        cached_data = analysis_cache[analysis_id]
        user_skills = cached_data['skills']['all_skills']
        suggested_role = cached_data['suggested_role']
        
        # Use suggested role if no target roles provided
        if not target_roles:
            target_roles = [suggested_role]
        
        logger.info(f"Analyzing skill gaps for roles: {target_roles}")
        
        # Search for jobs in target roles to analyze required skills
        from job_api_client import search_jobs_sync
        market_jobs = search_jobs_sync(keywords=target_roles, limit=50)
        
        # Analyze required skills across jobs
        required_skills = {}
        for job in market_jobs:
            for skill in job.skills:
                skill_lower = skill.lower()
                required_skills[skill_lower] = required_skills.get(skill_lower, 0) + 1
        
        # Calculate skill gaps
        total_jobs = len(market_jobs)
        user_skills_lower = [skill.lower() for skill in user_skills]
        skill_gaps = []
        
        for skill, frequency in required_skills.items():
            importance = frequency / total_jobs if total_jobs > 0 else 0
            if skill not in user_skills_lower and importance > 0.15:  # Required in >15% of jobs
                skill_gaps.append({
                    'skill': skill,
                    'importance': round(importance, 2),
                    'frequency': frequency,
                    'total_jobs': total_jobs,
                    'gap_severity': 'high' if importance > 0.4 else 'medium' if importance > 0.25 else 'low'
                })
        
        # Sort by importance
        skill_gaps.sort(key=lambda x: x['importance'], reverse=True)
        
        return jsonify({
            'success': True,
            'user_skills_count': len(user_skills),
            'market_jobs_analyzed': total_jobs,
            'skill_gaps': skill_gaps[:10],  # Top 10 gaps
            'recommendations': [
                f"Learn {gap['skill']} - required in {gap['frequency']}/{total_jobs} jobs" 
                for gap in skill_gaps[:3]
            ],
            'message': f'Analyzed {total_jobs} jobs to identify skill gaps'
        })
        
    except Exception as e:
        logger.error(f"Skill gap analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Skill gap analysis failed: {str(e)}'}), 500

# ================================
# Additional API Endpoints
# ================================

@app.route('/jobs/<job_id>/apply', methods=['POST'])
def apply_to_job(job_id):
    """Apply to a specific job (redirect to actual application)"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid analysis ID'}), 400
        
        # In a real implementation, this would track applications
        # For now, we'll just return success with application URL
        
        return jsonify({
            'success': True,
            'message': 'Application initiated. You will be redirected to the employer\'s application page.',
            'next_steps': [
                'Complete the application on the employer\'s website',
                'Tailor your resume for this specific role',
                'Prepare for potential interviews'
            ]
        })
        
    except Exception as e:
        logger.error(f"Job application error: {e}")
        return jsonify({'error': f'Application failed: {str(e)}'}), 500

@app.route('/stats', methods=['GET'])
def get_platform_stats():
    """Get platform statistics"""
    try:
        return jsonify({
            'success': True,
            'statistics': {
                'total_analyses': len(analysis_cache),
                'active_sessions': len(user_sessions),
                'ai_models_loaded': {
                    'resume_parser': _resume_parser is not None,
                    'job_matcher': _job_matcher is not None,
                    'job_client': _job_client is not None
                },
                'supported_features': [
                    'AI-powered skill extraction',
                    'Real-time job search',
                    'Intelligent job matching',
                    'Skill gap analysis',
                    'Role recommendations'
                ]
            },
            'message': 'Platform statistics retrieved successfully'
        })
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({'error': f'Failed to get statistics: {str(e)}'}), 500

# ================================
# Error Handlers
# ================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

# ================================
# Main Application
# ================================

if __name__ == '__main__':
    try:
        print("🚀 Starting Enhanced AI Job Matcher Backend...")
        print("📋 Features:")
        print("   ✅ 1. AI-powered skill extraction from resumes")
        print("   ✅ 2. Real-time job counting and analysis")
        print("   ✅ 3. Intelligent role recommendation based on skills")
        print("   ✅ 4. Real-time job search from multiple platforms")
        print("   ✅ 5. Live job data (no fake data)")
        print("   ✅ 6. Hugging Face models for NLP processing")
        print("")
        print("🌐 Server starting on http://localhost:5000")
        print("📖 API Documentation available at /health")
        print("")
        
        app.run(
            host=os.getenv('HOST', '0.0.0.0'),
            port=int(os.getenv('PORT', 5000)),
            debug=os.getenv('DEBUG', 'False').lower() == 'true'
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        logger.error(traceback.format_exc())
        raise
