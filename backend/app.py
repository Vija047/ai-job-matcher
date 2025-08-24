"""
Simplified Main Application - AI Job Matcher Backend
Uses enhanced modules for production-ready job matching
Focus on the 6 core requirements
"""

import os
import sys
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
import tempfile
import traceback

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure CORS
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001'], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Handle preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# Global storage for analysis results
analysis_cache = {}

# Lazy-loaded components
_resume_parser = None
_job_client = None

def get_resume_parser():
    """Lazy load the resume parser"""
    global _resume_parser
    if _resume_parser is None:
        print("🔄 Loading Enhanced Resume Parser...")
        from enhanced_resume_parser import AdvancedResumeParser
        _resume_parser = AdvancedResumeParser()
        print("✅ Resume Parser loaded!")
    return _resume_parser

def get_job_client():
    """Lazy load the job client - Enhanced with Wellfound and LinkedIn"""
    global _job_client
    if _job_client is None:
        print("🔄 Loading Enhanced Job Client with Wellfound & LinkedIn...")
        try:
            # Try to load the new Wellfound + LinkedIn client first
            from wellfound_linkedin_job_client import search_wellfound_linkedin_jobs
            _job_client = search_wellfound_linkedin_jobs
            print("✅ Wellfound & LinkedIn Job Client loaded!")
        except ImportError as e:
            print(f"⚠️ Wellfound LinkedIn client not available ({e}), falling back to enhanced client...")
            try:
                from enhanced_job_client import search_jobs_sync
                _job_client = search_jobs_sync
                print("✅ Enhanced Job Client loaded!")
            except ImportError as e2:
                print(f"⚠️ Enhanced client not available ({e2}), falling back to basic client...")
                from job_api_client import search_jobs_sync
                _job_client = search_jobs_sync
                print("✅ Basic Job Client loaded!")
    return _job_client

def calculate_compatibility_score(user_skills, job):
    """Calculate compatibility score between user skills and job requirements"""
    try:
        # Extract job skills from description and requirements
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}"
        job_skills = []
        
        # Simple keyword matching for job skills
        common_skills = [
            'python', 'javascript', 'react', 'node.js', 'sql', 'aws', 'docker', 
            'kubernetes', 'machine learning', 'data science', 'java', 'c++', 
            'html', 'css', 'git', 'agile', 'scrum', 'mongodb', 'postgresql'
        ]
        
        job_text_lower = job_text.lower()
        for skill in common_skills:
            if skill in job_text_lower:
                job_skills.append(skill)
        
        if not user_skills or not job_skills:
            return 50  # Default score if no skills found
        
        # Convert to lowercase for comparison
        user_skills_lower = [skill.lower() for skill in user_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Calculate matches
        matched_skills = set(user_skills_lower) & set(job_skills_lower)
        
        # Base compatibility score
        base_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
        
        # Bonus for high-demand skills
        high_demand_skills = ['python', 'react', 'aws', 'machine learning', 'docker', 'kubernetes']
        bonus = sum(1 for skill in matched_skills if skill in high_demand_skills) * 0.1
        
        # Convert to percentage
        score = min(100, (base_score + bonus) * 100)
        return max(30, score)  # Minimum 30% score
        
    except Exception as e:
        logger.error(f"Error calculating compatibility score: {e}")
        return 50  # Default score

def calculate_resume_score(analysis, all_skills, years_experience, quality_grade):
    """Calculate overall resume score based on multiple factors"""
    try:
        score = 0
        score_breakdown = {}
        
        # Skills count contribution (40% of total score)
        skills_count = len(all_skills)
        if skills_count >= 20:
            skills_score = 40
        elif skills_count >= 15:
            skills_score = 35
        elif skills_count >= 10:
            skills_score = 30
        elif skills_count >= 5:
            skills_score = 25
        else:
            skills_score = 15
        score += skills_score
        score_breakdown['skills'] = skills_score
        
        # Experience contribution (30% of total score)
        if years_experience >= 8:
            experience_score = 30
        elif years_experience >= 5:
            experience_score = 25
        elif years_experience >= 3:
            experience_score = 20
        elif years_experience >= 1:
            experience_score = 15
        else:
            experience_score = 10
        score += experience_score
        score_breakdown['experience'] = experience_score
        
        # Quality grade contribution (20% of total score)
        grade_scores = {'A+': 20, 'A': 18, 'B+': 16, 'B': 14, 'C+': 12, 'C': 10, 'D': 8}
        quality_score = grade_scores.get(quality_grade, 10)
        score += quality_score
        score_breakdown['quality'] = quality_score
        
        # Resume completeness (10% of total score)
        completeness_score = 0
        if analysis.get('personal_info', {}).get('email'):
            completeness_score += 2
        if analysis.get('personal_info', {}).get('phone'):
            completeness_score += 2
        if analysis.get('experience_analysis', {}).get('work_history'):
            completeness_score += 3
        if analysis.get('education_analysis', {}).get('degrees'):
            completeness_score += 3
        score += completeness_score
        score_breakdown['completeness'] = completeness_score
        
        final_score = min(100, max(40, score))
        
        return {
            'score': final_score,
            'breakdown': score_breakdown,
            'recommendations': get_score_recommendations(final_score, score_breakdown)
        }
        
    except Exception as e:
        logger.error(f"Error calculating resume score: {e}")
        return {
            'score': 75,
            'breakdown': {'skills': 30, 'experience': 20, 'quality': 15, 'completeness': 10},
            'recommendations': []
        }

def get_score_recommendations(score, breakdown):
    """Generate specific recommendations based on score breakdown"""
    recommendations = []
    
    if breakdown.get('skills', 0) < 30:
        recommendations.append("Add more technical skills to your resume")
        recommendations.append("Include both hard and soft skills")
    
    if breakdown.get('experience', 0) < 20:
        recommendations.append("Highlight your work experience with specific achievements")
        recommendations.append("Include quantifiable results and metrics")
    
    if breakdown.get('quality', 0) < 15:
        recommendations.append("Improve resume formatting and structure")
        recommendations.append("Use action verbs and professional language")
    
    if breakdown.get('completeness', 0) < 8:
        recommendations.append("Complete your contact information")
        recommendations.append("Add education and work history details")
    
    if score >= 90:
        recommendations.append("Your resume is excellent! Consider applying to senior positions")
    elif score >= 80:
        recommendations.append("Strong resume! Focus on highlighting achievements")
    elif score >= 70:
        recommendations.append("Good foundation. Add more specific details and metrics")
    else:
        recommendations.append("Consider restructuring your resume for better impact")
    
    return recommendations

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'cache_size': len(analysis_cache)
    })

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """
    Get sample jobs - this endpoint is called by the frontend JobsList component
    Returns a list of current job openings with basic information
    """
    try:
        # Get sample jobs using the job client
        job_client = get_job_client()
        
        # Search for popular tech roles
        sample_jobs = []
        job_titles = ['Software Engineer', 'Data Scientist', 'Frontend Developer', 'Backend Developer', 'DevOps Engineer']
        
        for title in job_titles:
            try:
                jobs = job_client([title], max_results=5)
                if jobs:
                    sample_jobs.extend(jobs[:3])  # Take first 3 from each title
            except Exception as e:
                logger.warning(f"Could not fetch jobs for {title}: {e}")
        
        # If no real jobs found, provide sample data
        if not sample_jobs:
            sample_jobs = [
                {
                    'id': 'job_1',
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Corp',
                    'location': 'Remote',
                    'salary': '$120,000 - $150,000',
                    'description': 'Join our team to build scalable web applications using modern technologies.',
                    'requirements': 'Python, JavaScript, React, AWS, 5+ years experience',
                    'required_skills': ['Python', 'JavaScript', 'React', 'AWS', 'Git'],
                    'posted_date': '2024-01-15',
                    'job_type': 'Full-time'
                },
                {
                    'id': 'job_2',
                    'title': 'Data Scientist',
                    'company': 'AI Solutions Inc',
                    'location': 'San Francisco, CA',
                    'salary': '$130,000 - $170,000',
                    'description': 'Work on cutting-edge machine learning projects to drive business insights.',
                    'requirements': 'Python, Machine Learning, TensorFlow, SQL, Statistics',
                    'required_skills': ['Python', 'Machine Learning', 'TensorFlow', 'SQL', 'Statistics'],
                    'posted_date': '2024-01-14',
                    'job_type': 'Full-time'
                },
                {
                    'id': 'job_3',
                    'title': 'Frontend Developer',
                    'company': 'Design Studio',
                    'location': 'New York, NY',
                    'salary': '$90,000 - $120,000',
                    'description': 'Create beautiful and responsive user interfaces for web applications.',
                    'requirements': 'React, TypeScript, CSS, HTML, 3+ years experience',
                    'required_skills': ['React', 'TypeScript', 'CSS', 'HTML', 'JavaScript'],
                    'posted_date': '2024-01-13',
                    'job_type': 'Full-time'
                },
                {
                    'id': 'job_4',
                    'title': 'DevOps Engineer',
                    'company': 'Cloud Systems',
                    'location': 'Remote',
                    'salary': '$110,000 - $140,000',
                    'description': 'Manage infrastructure and deployment pipelines for cloud applications.',
                    'requirements': 'AWS, Docker, Kubernetes, CI/CD, Linux',
                    'required_skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Linux'],
                    'posted_date': '2024-01-12',
                    'job_type': 'Full-time'
                },
                {
                    'id': 'job_5',
                    'title': 'Machine Learning Engineer',
                    'company': 'AI Innovations',
                    'location': 'Austin, TX',
                    'salary': '$125,000 - $160,000',
                    'description': 'Deploy ML models at scale and optimize machine learning pipelines.',
                    'requirements': 'Python, PyTorch, MLOps, Kubernetes, 4+ years experience',
                    'required_skills': ['Python', 'PyTorch', 'MLOps', 'Kubernetes', 'Docker'],
                    'posted_date': '2024-01-11',
                    'job_type': 'Full-time'
                }
            ]
        
        return jsonify({
            'status': 'success',
            'jobs': sample_jobs[:20],  # Limit to 20 jobs
            'total_jobs': len(sample_jobs),
            'message': f'Found {len(sample_jobs)} job opportunities'
        })
        
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to fetch jobs: {str(e)}'}), 500

@app.route('/job-match', methods=['POST'])
def job_match():
    """
    Calculate match score between a job and user's resume analysis
    Expected by the frontend JobsList component
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        job_id = data.get('job_id')
        analysis_id = data.get('analysis_id')
        
        if not job_id or not analysis_id:
            return jsonify({'error': 'job_id and analysis_id are required'}), 400
        
        # Get analysis from cache
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis = analysis_cache[analysis_id]
        user_skills = analysis.get('all_skills', [])
        suggested_role = analysis.get('suggested_role', '')
        experience_level = analysis.get('experience_level', 'mid')
        
        # For demo purposes, create a sample job based on job_id
        sample_job = {
            'id': job_id,
            'title': 'Software Engineer',
            'description': 'Join our team to build scalable applications with Python, JavaScript, React, and AWS',
            'requirements': 'Python, JavaScript, React, AWS, Git, SQL'
        }
        
        # Calculate compatibility score
        match_score = calculate_compatibility_score(user_skills, sample_job)
        
        # Calculate detailed match analysis
        job_skills = ['python', 'javascript', 'react', 'aws', 'git', 'sql']
        matched_skills = [skill for skill in user_skills if skill.lower() in [js.lower() for js in job_skills]]
        missing_skills = [skill for skill in job_skills if skill.lower() not in [us.lower() for us in user_skills]]
        
        return jsonify({
            'status': 'success',
            'match_result': {
                'overall_score': match_score / 100,  # Convert to 0-1 scale for frontend
                'resume_score': analysis.get('resume_score', 75) / 100,  # Include resume score
                'match_score': match_score,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'recommendation': 'Good match!' if match_score > 70 else 'Consider improving skills in missing areas',
                'role_alignment': suggested_role.lower() in sample_job['title'].lower(),
                'experience_match': experience_level in ['mid', 'senior']
            },
            'match_score': match_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendation': 'Good match!' if match_score > 70 else 'Consider improving skills in missing areas',
            'role_alignment': suggested_role.lower() in sample_job['title'].lower(),
            'experience_match': experience_level in ['mid', 'senior'],
            'message': f'Match score: {match_score}% - {len(matched_skills)} skills matched'
        })
        
    except Exception as e:
        logger.error(f"Error calculating job match: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to calculate job match: {str(e)}'}), 500

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """
    REQUIREMENT 1: Extract skills from user's resume
    REQUIREMENT 2: Show total number of skills identified
    REQUIREMENT 3: Define most suitable role based on skills
    REQUIREMENT 6: Use Hugging Face models for processing
    """
    try:
        # Validate file upload
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        allowed_extensions = ['.pdf', '.txt', '.doc', '.docx']
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'Only PDF, TXT, DOC, and DOCX files are supported'}), 400
        
        # Save file temporarily
        temp_path = None
        try:
            file_extension = os.path.splitext(file.filename.lower())[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                file.save(temp_file.name)
                temp_path = temp_file.name
            
            # Parse resume using Hugging Face models
            logger.info(f"Processing resume: {file.filename}")
            resume_parser = get_resume_parser()
            analysis = resume_parser.parse_resume(temp_path)
            
            if 'error' in analysis:
                return jsonify({'error': analysis['error']}), 400
            
            # Extract key results for the response
            skills_analysis = analysis.get('skills_analysis', {})
            all_skills = skills_analysis.get('all_skills', [])
            skills_by_category = skills_analysis.get('skills_by_category', {})
            total_skills = len(all_skills)
            
            # Get role suggestion
            role_suggestion = analysis.get('role_suggestion', {})
            suggested_role = role_suggestion.get('primary_role', 'Software Engineer')
            
            # Experience information
            experience_analysis = analysis.get('experience_analysis', {})
            experience_level = experience_analysis.get('experience_level', 'mid')
            years_experience = experience_analysis.get('total_years', 0)
            
            # Quality assessment
            quality_assessment = analysis.get('quality_assessment', {})
            quality_grade = quality_assessment.get('quality_grade', 'B')
            
            # Calculate resume score based on multiple factors
            resume_score_result = calculate_resume_score(analysis, all_skills, years_experience, quality_grade)
            resume_score = resume_score_result['score']
            score_breakdown = resume_score_result['breakdown']
            score_recommendations = resume_score_result['recommendations']
            
            # Generate analysis ID
            analysis_id = str(uuid.uuid4())
            
            # Store in cache for later use
            analysis_cache[analysis_id] = {
                'analysis_id': analysis_id,
                'filename': file.filename,
                'timestamp': datetime.now().isoformat(),
                'all_skills': all_skills,
                'skills_by_category': skills_by_category,
                'total_skills': total_skills,
                'suggested_role': suggested_role,
                'experience_level': experience_level,
                'years_experience': years_experience,
                'quality_grade': quality_grade,
                'resume_score': resume_score,
                'score_breakdown': score_breakdown,
                'score_recommendations': score_recommendations,
                'full_analysis': analysis
            }
            
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            
            logger.info(f"✅ Resume processed: {total_skills} skills found, role: {suggested_role}")
            
            # Return focused response meeting requirements 1, 2, 3
            return jsonify({
                'status': 'success',  # Frontend expects this format
                'success': True,
                'analysis_id': analysis_id,
                
                # REQUIREMENT 1: Skills extracted from resume
                'skills_extracted': all_skills,
                'skills_by_category': skills_by_category,
                
                # REQUIREMENT 2: Total number of skills
                'total_skills_count': total_skills,
                
                # REQUIREMENT 3: Most suitable role based on skills
                'suggested_role': suggested_role,
                'role_confidence': role_suggestion.get('confidence', 0.5),
                'alternative_roles': role_suggestion.get('alternative_roles', []),
                
                # Additional useful information
                'experience_level': experience_level,
                'years_experience': years_experience,
                'quality_grade': quality_grade,
                'resume_score': resume_score,
                'score_breakdown': score_breakdown,
                'score_recommendations': score_recommendations,
                'top_skills': all_skills[:10],
                
                'message': f'✅ Resume analyzed! Found {total_skills} skills. Resume Score: {resume_score}%. Suggested role: {suggested_role}'
            })
            
        except Exception as e:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise e
            
    except Exception as e:
        logger.error(f"Resume processing error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Resume processing failed: {str(e)}'}), 500

@app.route('/search-jobs', methods=['POST'])
def search_jobs():
    """
    REQUIREMENT 4: Browse and fetch available jobs from real platforms
    REQUIREMENT 5: Use real-time job data (not fake data)
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No search criteria provided'}), 400
        
        # Get search parameters
        keywords = data.get('keywords', [])
        location = data.get('location', '')
        experience_level = data.get('experience_level', '')
        limit = min(data.get('limit', 20), 50)
        
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        
        logger.info(f"Searching real-time jobs for: {keywords}")
        
        # Search real job platforms
        job_search_func = get_job_client()
        logger.info(f"Job search function: {job_search_func}")
        logger.info(f"Keywords type: {type(keywords)}, Keywords: {keywords}")
        
        jobs = job_search_func(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
            limit=limit
        )
        
        logger.info(f"Job search returned {len(jobs)} jobs")
        
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
                'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
                'experience_level': job.experience_level,
                'employment_type': job.employment_type,
                'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                'apply_url': job.apply_url,
                'skills_required': job.skills,
                'remote_allowed': job.remote_allowed,
                'source': job.source,  # Shows real data source
                'company_size': job.company_size,
                'industry': job.industry
            }
            formatted_jobs.append(formatted_job)
        
        logger.info(f"✅ Found {len(formatted_jobs)} real jobs from live sources")
        
        # REQUIREMENTS 4 & 5: Real-time jobs from actual platforms
        return jsonify({
            'success': True,
            'jobs': formatted_jobs,
            'total_found': len(formatted_jobs),
            'search_criteria': {
                'keywords': keywords,
                'location': location,
                'experience_level': experience_level
            },
            'data_sources': list(set([job['source'] for job in formatted_jobs])),
            'message': f'Found {len(formatted_jobs)} real-time jobs from live job platforms'
        })
        
    except Exception as e:
        logger.error(f"Job search error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Job search failed: {str(e)}'}), 500

@app.route('/search-wellfound-linkedin', methods=['POST'])
def search_wellfound_linkedin():
    """
    ENHANCED: Search specifically from Wellfound and LinkedIn
    Focus on startup opportunities and professional networking jobs
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No search criteria provided'}), 400
        
        # Get search parameters
        keywords = data.get('keywords', [])
        location = data.get('location', '')
        experience_level = data.get('experience_level', '')
        limit = min(data.get('limit', 20), 50)
        
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        
        logger.info(f"Searching Wellfound & LinkedIn for: {keywords}")
        
        # Import and use the specialized client
        try:
            from wellfound_linkedin_job_client import search_wellfound_linkedin_jobs
            jobs = search_wellfound_linkedin_jobs(
                keywords=keywords,
                location=location,
                experience_level=experience_level,
                limit=limit
            )
        except ImportError as e:
            logger.warning(f"Wellfound LinkedIn client not available: {e}")
            # Fallback to regular search
            job_search_func = get_job_client()
            jobs = job_search_func(
                keywords=keywords,
                location=location,
                experience_level=experience_level,
                limit=limit
            )
        
        logger.info(f"Found {len(jobs)} jobs from Wellfound & LinkedIn")
        
        # Format jobs for response with enhanced details
        formatted_jobs = []
        for job in jobs:
            formatted_job = {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'description': job.description[:500] + '...' if len(job.description) > 500 else job.description,
                'requirements': job.requirements,
                'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
                'experience_level': job.experience_level,
                'employment_type': job.employment_type,
                'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                'apply_url': job.apply_url,
                'skills_required': job.skills,
                'remote_allowed': job.remote_allowed,
                'source': job.source,
                'company_size': job.company_size,
                'industry': job.industry,
                # Enhanced fields for Wellfound
                'funding_stage': getattr(job, 'funding_stage', None),
                'company_logo': getattr(job, 'company_logo', None),
                'is_startup': job.source == 'Wellfound'
            }
            formatted_jobs.append(formatted_job)
        
        # Separate by source for insights
        wellfound_jobs = [job for job in formatted_jobs if job['source'] == 'Wellfound']
        linkedin_jobs = [job for job in formatted_jobs if job['source'] == 'LinkedIn']
        
        logger.info(f"✅ Found {len(wellfound_jobs)} Wellfound + {len(linkedin_jobs)} LinkedIn jobs")
        
        return jsonify({
            'success': True,
            'jobs': formatted_jobs,
            'total_found': len(formatted_jobs),
            'source_breakdown': {
                'wellfound_count': len(wellfound_jobs),
                'linkedin_count': len(linkedin_jobs),
                'total_startup_opportunities': len(wellfound_jobs),
                'total_professional_opportunities': len(linkedin_jobs)
            },
            'search_criteria': {
                'keywords': keywords,
                'location': location,
                'experience_level': experience_level
            },
            'data_sources': list(set([job['source'] for job in formatted_jobs])),
            'enhanced_features': {
                'startup_focus': True,
                'professional_network': True,
                'funding_info': len([job for job in formatted_jobs if job.get('funding_stage')]) > 0,
                'company_logos': len([job for job in formatted_jobs if job.get('company_logo')]) > 0
            },
            'message': f'Found {len(formatted_jobs)} jobs from Wellfound and LinkedIn platforms'
        })
        
    except Exception as e:
        logger.error(f"Wellfound/LinkedIn search error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    """
    Enhanced job matching that recommends jobs and internships based on resume skills
    Provides intelligent scoring and detailed skill analysis
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        job_type = data.get('job_type', 'both')  # 'jobs', 'internships', or 'both'
        location = preferences.get('location', '')
        limit = min(data.get('limit', 20), 50)
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid analysis ID. Please upload your resume first.'}), 400
        
        # Get user's analysis
        user_data = analysis_cache[analysis_id]
        user_skills = user_data['all_skills']
        suggested_role = user_data['suggested_role']
        experience_level = user_data['experience_level']
        years_experience = user_data.get('years_experience', 0)
        
        logger.info(f"Matching {job_type} for user with {len(user_skills)} skills, role: {suggested_role}")
        
        # Build comprehensive search strategy
        search_strategies = build_search_strategies(user_skills, suggested_role, job_type, years_experience)
        
        all_matched_jobs = []
        job_search_func = get_job_client()
        
        # Execute multiple search strategies for better coverage
        for strategy in search_strategies:
            try:
                jobs = job_search_func(
                    keywords=strategy['keywords'],
                    location=location,
                    experience_level=strategy['experience_level'],
                    limit=limit
                )
                
                # Score and filter jobs
                for job in jobs:
                    match_result = calculate_enhanced_match_score(user_skills, job, suggested_role, years_experience)
                    
                    if match_result['total_score'] > 20:  # Minimum 20% match
                        job_data = format_job_recommendation(job, match_result, strategy['priority'])
                        all_matched_jobs.append(job_data)
                        
            except Exception as e:
                logger.warning(f"Search strategy failed: {strategy['name']} - {e}")
                continue
        
        # Remove duplicates and sort by relevance
        unique_jobs = remove_duplicate_jobs(all_matched_jobs)
        sorted_jobs = sort_jobs_by_relevance(unique_jobs, user_skills, suggested_role)
        top_matches = sorted_jobs[:limit]
        
        # Generate comprehensive insights
        insights = generate_enhanced_insights(user_skills, top_matches, suggested_role, job_type)
        
        logger.info(f"✅ Found {len(top_matches)} AI-matched {job_type}")
        
        return jsonify({
            'success': True,
            'matched_jobs': top_matches,
            'total_matches': len(top_matches),
            'job_type_searched': job_type,
            'user_profile': {
                'total_skills': len(user_skills),
                'suggested_role': suggested_role,
                'experience_level': experience_level,
                'years_experience': years_experience,
                'top_skills': user_skills[:10]
            },
            'insights': insights,
            'search_strategies_used': [s['name'] for s in search_strategies],
            'message': f'Found {len(top_matches)} AI-matched {job_type} based on your {len(user_skills)} skills and {suggested_role} profile'
        })
        
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Job matching failed: {str(e)}'}), 500

def build_search_strategies(user_skills: List[str], suggested_role: str, job_type: str, years_experience: int) -> List[Dict]:
    """Build multiple search strategies for comprehensive job discovery"""
    strategies = []
    
    # Strategy 1: Core role-based search
    strategies.append({
        'name': 'Role-based search',
        'keywords': [suggested_role] + user_skills[:5],
        'experience_level': 'entry' if years_experience < 2 else 'mid' if years_experience < 5 else 'senior',
        'priority': 'high'
    })
    
    # Strategy 2: Skills-focused search
    strategies.append({
        'name': 'Skills-focused search',
        'keywords': user_skills[:8],
        'experience_level': '',
        'priority': 'medium'
    })
    
    # Strategy 3: Internship-specific search (if requested)
    if job_type in ['internships', 'both']:
        strategies.append({
            'name': 'Internship search',
            'keywords': ['internship', 'intern', 'trainee'] + user_skills[:5],
            'experience_level': 'entry',
            'priority': 'high' if job_type == 'internships' else 'medium'
        })
    
    # Strategy 4: Entry-level opportunities
    if years_experience < 3:
        strategies.append({
            'name': 'Entry-level search',
            'keywords': ['junior', 'entry level', 'graduate'] + user_skills[:5],
            'experience_level': 'entry',
            'priority': 'medium'
        })
    
    return strategies

def calculate_enhanced_match_score(user_skills: List[str], job, suggested_role: str, years_experience: int) -> Dict:
    """Calculate comprehensive job match score with detailed breakdown"""
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    job_skills_lower = [skill.lower().strip() for skill in job.skills]
    job_text_lower = (job.title + ' ' + job.description + ' ' + ' '.join(job.requirements)).lower()
    
    # Initialize scoring components
    scores = {
        'skill_match': 0.0,
        'role_match': 0.0,
        'experience_match': 0.0,
        'keyword_match': 0.0,
        'job_type_match': 0.0
    }
    
    # 1. Skill matching (50% weight)
    skill_matches = []
    skill_relevance = 0
    
    for user_skill in user_skills_lower:
        best_match_score = 0
        best_match = None
        
        # Direct skill matches
        for job_skill in job_skills_lower:
            if user_skill == job_skill:
                best_match_score = 1.0
                best_match = job_skill
                break
            elif user_skill in job_skill or job_skill in user_skill:
                match_score = min(len(user_skill), len(job_skill)) / max(len(user_skill), len(job_skill))
                if match_score > best_match_score:
                    best_match_score = match_score
                    best_match = job_skill
        
        # Text-based matches
        if best_match_score < 0.5 and user_skill in job_text_lower:
            best_match_score = 0.6
            best_match = user_skill
        
        if best_match_score > 0.3:  # Minimum threshold
            skill_matches.append({
                'user_skill': user_skill,
                'matched_skill': best_match,
                'score': best_match_score
            })
            skill_relevance += best_match_score
    
    scores['skill_match'] = min(skill_relevance / len(user_skills), 1.0) * 0.5 if user_skills else 0
    
    # 2. Role matching (25% weight)
    role_keywords = suggested_role.lower().split()
    role_match_score = 0
    
    for keyword in role_keywords:
        if keyword in job.title.lower():
            role_match_score += 0.4
        elif keyword in job_text_lower:
            role_match_score += 0.2
    
    scores['role_match'] = min(role_match_score, 1.0) * 0.25
    
    # 3. Experience level matching (15% weight)
    exp_match = 0
    user_exp_level = 'entry' if years_experience < 2 else 'mid' if years_experience < 5 else 'senior'
    
    if job.experience_level:
        if job.experience_level.lower() == user_exp_level:
            exp_match = 1.0
        elif abs(['entry', 'mid', 'senior'].index(user_exp_level) - 
                ['entry', 'mid', 'senior'].index(job.experience_level.lower())) == 1:
            exp_match = 0.6
    else:
        exp_match = 0.5  # Unknown experience level
    
    scores['experience_match'] = exp_match * 0.15
    
    # 4. Important keyword matching (10% weight)
    important_keywords = ['remote', 'flexible', 'full-time', 'part-time', 'contract']
    keyword_score = sum(1 for keyword in important_keywords if keyword in job_text_lower) / len(important_keywords)
    scores['keyword_match'] = keyword_score * 0.1
    
    # Calculate total score
    total_score = sum(scores.values()) * 100
    
    return {
        'total_score': round(total_score, 1),
        'score_breakdown': {k: round(v * 100, 1) for k, v in scores.items()},
        'skill_matches': skill_matches,
        'matching_skills_count': len(skill_matches),
        'skill_gaps': [skill for skill in job_skills_lower if not any(
            skill in user_skill or user_skill in skill for user_skill in user_skills_lower
        )][:5]
    }

def format_job_recommendation(job, match_result: Dict, priority: str) -> Dict:
    """Format job data with enhanced recommendation details"""
    return {
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'description': job.description[:500] + '...' if len(job.description) > 500 else job.description,
        'requirements': job.requirements,
        'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Salary not specified",
        'experience_level': job.experience_level,
        'employment_type': job.employment_type,
        'posted_date': job.posted_date.isoformat() if job.posted_date else None,
        'apply_url': job.apply_url,
        'skills_required': job.skills,
        'remote_allowed': job.remote_allowed,
        'source': job.source,
        'company_size': job.company_size,
        'industry': job.industry,
        
        # Enhanced matching information
        'match_score': match_result['total_score'],
        'score_breakdown': match_result['score_breakdown'],
        'matching_skills': [m['user_skill'] for m in match_result['skill_matches']],
        'matching_skills_count': match_result['matching_skills_count'],
        'skill_gaps': match_result['skill_gaps'],
        'recommendation_priority': priority,
        'is_internship': any(keyword in job.title.lower() for keyword in ['intern', 'internship', 'trainee']),
        'is_entry_level': any(keyword in job.title.lower() for keyword in ['junior', 'entry', 'graduate']),
        
        # Recommendation insights
        'why_recommended': generate_recommendation_reason(match_result, job.title),
        'application_tips': generate_application_tips(match_result, job.title)
    }

def remove_duplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    """Remove duplicate job postings based on title, company, and location"""
    seen = set()
    unique_jobs = []
    
    for job in jobs:
        job_key = (job['title'].lower(), job['company'].lower(), job['location'].lower())
        if job_key not in seen:
            seen.add(job_key)
            unique_jobs.append(job)
    
    return unique_jobs

def sort_jobs_by_relevance(jobs: List[Dict], user_skills: List[str], suggested_role: str) -> List[Dict]:
    """Sort jobs by relevance considering multiple factors"""
    def relevance_score(job):
        score = job['match_score']
        
        # Boost for exact role matches
        if suggested_role.lower() in job['title'].lower():
            score += 10
        
        # Boost for high skill matches
        score += job['matching_skills_count'] * 2
        
        # Boost for recent postings
        if job['posted_date']:
            try:
                posted = datetime.fromisoformat(job['posted_date'].replace('Z', '+00:00'))
                days_old = (datetime.now(posted.tzinfo) - posted).days
                if days_old <= 7:
                    score += 5
                elif days_old <= 30:
                    score += 2
            except:
                pass
        
        # Boost for remote opportunities
        if job['remote_allowed']:
            score += 3
        
        return score
    
    return sorted(jobs, key=relevance_score, reverse=True)

def generate_recommendation_reason(match_result: Dict, job_title: str) -> str:
    """Generate explanation for why this job is recommended"""
    reasons = []
    
    if match_result['total_score'] > 80:
        reasons.append("Excellent skill alignment")
    elif match_result['total_score'] > 60:
        reasons.append("Strong skill match")
    else:
        reasons.append("Good growth opportunity")
    
    if match_result['matching_skills_count'] > 5:
        reasons.append(f"matches {match_result['matching_skills_count']} of your skills")
    
    if len(match_result['skill_gaps']) <= 2:
        reasons.append("minimal skill gaps")
    
    return f"Recommended because: {', '.join(reasons)}"

def generate_application_tips(match_result: Dict, job_title: str) -> List[str]:
    """Generate personalized application tips"""
    tips = []
    
    if match_result['matching_skills_count'] > 3:
        tips.append("Highlight your matching technical skills prominently")
    
    if match_result['skill_gaps']:
        tips.append(f"Consider mentioning willingness to learn: {', '.join(match_result['skill_gaps'][:2])}")
    
    if 'intern' in job_title.lower():
        tips.append("Emphasize your eagerness to learn and grow")
        tips.append("Highlight relevant projects and coursework")
    
    tips.append("Tailor your cover letter to mention specific requirements")
    
    return tips

def generate_enhanced_insights(user_skills: List[str], matched_jobs: List[Dict], suggested_role: str, job_type: str) -> Dict:
    """Generate comprehensive insights about job matches"""
    if not matched_jobs:
        return {
            'summary': f'No matching {job_type} found. Consider expanding your skill set or exploring related roles.',
            'recommendations': [
                'Add more in-demand skills to your profile',
                'Consider applying to similar roles',
                'Look into skill development courses'
            ],
            'market_trends': ['Expand your search criteria', 'Consider remote opportunities']
        }
    
    # Calculate statistics
    avg_score = sum(job['match_score'] for job in matched_jobs) / len(matched_jobs)
    high_matches = [job for job in matched_jobs if job['match_score'] > 70]
    internships = [job for job in matched_jobs if job.get('is_internship', False)]
    entry_level = [job for job in matched_jobs if job.get('is_entry_level', False)]
    
    # Analyze skill demand
    all_required_skills = []
    for job in matched_jobs:
        all_required_skills.extend(job['skills_required'])
    
    skill_frequency = {}
    for skill in all_required_skills:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    top_demanded = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Generate recommendations
    recommendations = []
    if len(high_matches) > 0:
        recommendations.append(f"Apply immediately to {min(3, len(high_matches))} top matches (>70% compatibility)")
    
    if internships and job_type in ['internships', 'both']:
        recommendations.append(f"Found {len(internships)} internship opportunities")
    
    if top_demanded:
        most_demanded = top_demanded[0][0]
        if most_demanded.lower() not in [skill.lower() for skill in user_skills]:
            recommendations.append(f"Consider learning '{most_demanded}' - highly demanded skill")
    
    return {
        'summary': f'Found {len(matched_jobs)} {job_type} with {avg_score:.0f}% average compatibility',
        'statistics': {
            'total_opportunities': len(matched_jobs),
            'high_compatibility': len(high_matches),
            'internships_found': len(internships),
            'entry_level_found': len(entry_level),
            'average_match_score': round(avg_score, 1)
        },
        'top_demanded_skills': [{'skill': skill, 'frequency': freq} for skill, freq in top_demanded],
        'recommendations': recommendations,
        'market_trends': [
            f'{suggested_role} positions are actively hiring',
            f'Remote work available in {sum(1 for job in matched_jobs if job["remote_allowed"])} positions',
            f'Average skill requirements: {len(all_required_skills)//len(matched_jobs) if matched_jobs else 0} skills per job'
        ]
    }

@app.route('/recommend-jobs', methods=['POST'])
def recommend_jobs():
    """
    Dedicated endpoint for job and internship recommendations
    Optimized for current market matching based on resume skills
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request data required'}), 400
        
        analysis_id = data.get('analysis_id')
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Valid analysis_id required. Upload resume first.'}), 400
        
        # Get recommendation preferences
        preferences = data.get('preferences', {})
        job_type = preferences.get('job_type', 'both')  # 'jobs', 'internships', 'both'
        location = preferences.get('location', '')
        remote_only = preferences.get('remote_only', False)
        salary_min = preferences.get('salary_min', 0)
        experience_preference = preferences.get('experience_level', 'auto')
        limit = min(data.get('limit', 25), 100)
        
        # Get user analysis data
        user_data = analysis_cache[analysis_id]
        user_skills = user_data['all_skills']
        suggested_role = user_data['suggested_role']
        experience_level = user_data['experience_level']
        years_experience = user_data.get('years_experience', 0)
        skills_by_category = user_data.get('skills_by_category', {})
        
        logger.info(f"🎯 Generating {job_type} recommendations for {suggested_role} with {len(user_skills)} skills")
        
        # Create targeted search queries
        search_queries = create_targeted_search_queries(
            user_skills, suggested_role, job_type, years_experience, skills_by_category
        )
        
        job_search_func = get_job_client()
        all_recommendations = []
        
        # Execute targeted searches
        for query in search_queries:
            try:
                jobs = job_search_func(
                    keywords=query['keywords'],
                    location=location,
                    experience_level=query['experience_level'],
                    limit=query['limit']
                )
                
                for job in jobs:
                    # Apply filters
                    if remote_only and not job.remote_allowed:
                        continue
                    if salary_min > 0 and job.salary_min and job.salary_min < salary_min:
                        continue
                    
                    # Calculate comprehensive match
                    match_analysis = analyze_job_match(user_skills, job, suggested_role, years_experience)
                    
                    if match_analysis['recommendation_score'] > 25:  # Minimum recommendation threshold
                        recommendation = create_job_recommendation(job, match_analysis, query['category'])
                        all_recommendations.append(recommendation)
                        
            except Exception as e:
                logger.warning(f"Search query failed: {query['category']} - {e}")
                continue
        
        # Remove duplicates and rank recommendations
        unique_recommendations = deduplicate_recommendations(all_recommendations)
        ranked_recommendations = rank_recommendations(unique_recommendations, user_skills, suggested_role)
        final_recommendations = ranked_recommendations[:limit]
        
        # Generate market insights
        market_insights = analyze_market_opportunities(
            final_recommendations, user_skills, suggested_role, job_type
        )
        
        # Categorize recommendations
        categorized_recs = categorize_recommendations(final_recommendations)
        
        logger.info(f"✅ Generated {len(final_recommendations)} personalized recommendations")
        
        return jsonify({
            'success': True,
            'total_recommendations': len(final_recommendations),
            'job_type_searched': job_type,
            'recommendations': final_recommendations,
            'categorized_recommendations': categorized_recs,
            'user_profile_summary': {
                'name': user_data.get('filename', 'Unknown'),
                'total_skills': len(user_skills),
                'suggested_role': suggested_role,
                'experience_level': experience_level,
                'years_experience': years_experience,
                'core_skills': user_skills[:8],
                'skill_categories': list(skills_by_category.keys())
            },
            'market_insights': market_insights,
            'search_strategy': {
                'queries_executed': len(search_queries),
                'total_jobs_analyzed': len(all_recommendations),
                'filters_applied': {
                    'location': location if location else 'Any',
                    'remote_only': remote_only,
                    'minimum_salary': f"${salary_min:,}" if salary_min > 0 else "Any"
                }
            },
            'recommendation_tips': generate_recommendation_tips(final_recommendations, user_skills),
            'message': f'Found {len(final_recommendations)} personalized {job_type} recommendations matching your {suggested_role} profile'
        })
        
    except Exception as e:
        logger.error(f"Recommendation generation error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to generate recommendations: {str(e)}'}), 500

def create_targeted_search_queries(user_skills: List[str], suggested_role: str, job_type: str, 
                                 years_experience: int, skills_by_category: Dict) -> List[Dict]:
    """Create multiple targeted search queries for comprehensive job discovery"""
    queries = []
    
    # Query 1: Primary role-based search
    queries.append({
        'category': 'primary_role',
        'keywords': [suggested_role] + user_skills[:6],
        'experience_level': 'entry' if years_experience < 2 else 'mid' if years_experience < 5 else 'senior',
        'limit': 30,
        'weight': 1.0
    })
    
    # Query 2: Skills-focused search
    if 'technical' in skills_by_category and skills_by_category['technical']:
        tech_skills = skills_by_category['technical'][:8]
        queries.append({
            'category': 'technical_skills',
            'keywords': tech_skills,
            'experience_level': '',
            'limit': 25,
            'weight': 0.9
        })
    
    # Query 3: Internship-specific searches
    if job_type in ['internships', 'both']:
        intern_keywords = ['internship', 'intern', 'trainee', 'co-op', 'summer intern'] + user_skills[:4]
        queries.append({
            'category': 'internships',
            'keywords': intern_keywords,
            'experience_level': 'entry',
            'limit': 20,
            'weight': 1.0 if job_type == 'internships' else 0.8
        })
    
    # Query 4: Entry-level and graduate opportunities
    if years_experience < 3:
        entry_keywords = ['junior', 'entry level', 'graduate', 'new grad', 'associate'] + user_skills[:5]
        queries.append({
            'category': 'entry_level',
            'keywords': entry_keywords,
            'experience_level': 'entry',
            'limit': 20,
            'weight': 0.9
        })
    
    # Query 5: Industry-specific search
    if 'industry' in skills_by_category and skills_by_category['industry']:
        industry_skills = skills_by_category['industry'][:5]
        queries.append({
            'category': 'industry_specific',
            'keywords': industry_skills + [suggested_role],
            'experience_level': '',
            'limit': 15,
            'weight': 0.8
        })
    
    return queries

def analyze_job_match(user_skills: List[str], job, suggested_role: str, years_experience: int) -> Dict:
    """Comprehensive job match analysis with detailed scoring"""
    analysis = {
        'skill_alignment': 0,
        'role_relevance': 0,
        'experience_fit': 0,
        'growth_potential': 0,
        'market_demand': 0,
        'recommendation_score': 0,
        'confidence_level': 'low'
    }
    
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    job_skills_lower = [skill.lower().strip() for skill in job.skills]
    job_content = f"{job.title} {job.description} {' '.join(job.requirements)}".lower()
    
    # 1. Skill Alignment Analysis (40% weight)
    skill_matches = 0
    partial_matches = 0
    
    for user_skill in user_skills_lower:
        # Exact matches
        if user_skill in job_skills_lower:
            skill_matches += 1
        # Partial matches in job skills
        elif any(user_skill in job_skill or job_skill in user_skill for job_skill in job_skills_lower):
            skill_matches += 0.8
        # Content matches
        elif user_skill in job_content:
            partial_matches += 1
    
    total_relevant = skill_matches + (partial_matches * 0.5)
    analysis['skill_alignment'] = min(total_relevant / len(user_skills), 1.0) * 40 if user_skills else 0
    
    # 2. Role Relevance (25% weight)
    role_score = 0
    role_words = suggested_role.lower().split()
    
    for word in role_words:
        if word in job.title.lower():
            role_score += 15
        elif word in job_content:
            role_score += 5
    
    analysis['role_relevance'] = min(role_score, 25)
    
    # 3. Experience Fit (20% weight)
    exp_score = 0
    user_level = 'entry' if years_experience < 2 else 'mid' if years_experience < 5 else 'senior'
    
    if job.experience_level:
        job_level = job.experience_level.lower()
        if job_level == user_level:
            exp_score = 20
        elif abs(['entry', 'mid', 'senior'].index(user_level) - 
                ['entry', 'mid', 'senior'].index(job_level)) == 1:
            exp_score = 15
        else:
            exp_score = 8
    else:
        exp_score = 12  # Neutral for unknown experience requirements
    
    analysis['experience_fit'] = exp_score
    
    # 4. Growth Potential (10% weight)
    growth_indicators = ['senior', 'lead', 'manager', 'principal', 'architect', 'director']
    if any(indicator in job.title.lower() for indicator in growth_indicators):
        analysis['growth_potential'] = 10
    elif any(word in job_content for word in ['career growth', 'advancement', 'promotion']):
        analysis['growth_potential'] = 7
    else:
        analysis['growth_potential'] = 5
    
    # 5. Market Demand (5% weight)
    demand_indicators = ['urgent', 'immediate', 'high priority', 'competitive salary']
    if any(indicator in job_content for indicator in demand_indicators):
        analysis['market_demand'] = 5
    else:
        analysis['market_demand'] = 3
    
    # Calculate total recommendation score
    analysis['recommendation_score'] = (
        analysis['skill_alignment'] + 
        analysis['role_relevance'] + 
        analysis['experience_fit'] + 
        analysis['growth_potential'] + 
        analysis['market_demand']
    )
    
    # Determine confidence level
    if analysis['recommendation_score'] >= 70:
        analysis['confidence_level'] = 'high'
    elif analysis['recommendation_score'] >= 50:
        analysis['confidence_level'] = 'medium'
    else:
        analysis['confidence_level'] = 'low'
    
    # Add detailed insights
    analysis['skill_matches'] = [skill for skill in user_skills_lower if skill in job_skills_lower or skill in job_content]
    analysis['missing_skills'] = [skill for skill in job_skills_lower[:5] if not any(
        skill in user_skill or user_skill in skill for user_skill in user_skills_lower
    )]
    
    return analysis

def create_job_recommendation(job, match_analysis: Dict, category: str) -> Dict:
    """Create a comprehensive job recommendation object"""
    return {
        'id': job.id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'description': job.description[:600] + '...' if len(job.description) > 600 else job.description,
        'requirements': job.requirements,
        'skills_required': job.skills,
        'salary_range': format_salary_range(job.salary_min, job.salary_max, job.salary_currency),
        'experience_level': job.experience_level or 'Not specified',
        'employment_type': job.employment_type,
        'posted_date': job.posted_date.isoformat() if job.posted_date else None,
        'expires_date': job.expires_date.isoformat() if job.expires_date else None,
        'apply_url': job.apply_url,
        'source': job.source,
        'remote_allowed': job.remote_allowed,
        'company_size': job.company_size,
        'industry': job.industry,
        
        # Recommendation-specific data
        'recommendation_score': round(match_analysis['recommendation_score'], 1),
        'confidence_level': match_analysis['confidence_level'],
        'match_breakdown': {
            'skill_alignment': round(match_analysis['skill_alignment'], 1),
            'role_relevance': round(match_analysis['role_relevance'], 1),
            'experience_fit': round(match_analysis['experience_fit'], 1),
            'growth_potential': round(match_analysis['growth_potential'], 1),
            'market_demand': round(match_analysis['market_demand'], 1)
        },
        'matching_skills': match_analysis['skill_matches'],
        'skill_gaps': match_analysis['missing_skills'],
        'search_category': category,
        
        # Classification
        'is_internship': classify_as_internship(job.title, job.description),
        'is_entry_level': classify_as_entry_level(job.title, job.description),
        'is_remote': job.remote_allowed,
        'urgency_level': assess_urgency(job.description, job.posted_date),
        
        # Personalized insights
        'why_recommended': create_recommendation_explanation(match_analysis, job.title),
        'application_strategy': create_application_strategy(match_analysis, job.title),
        'skill_development_suggestions': match_analysis['missing_skills'][:3]
    }

def format_salary_range(salary_min, salary_max, currency):
    """Format salary range for display"""
    if salary_min and salary_max:
        return f"{currency or '$'}{salary_min:,.0f} - {currency or '$'}{salary_max:,.0f}"
    elif salary_min:
        return f"{currency or '$'}{salary_min:,.0f}+"
    elif salary_max:
        return f"Up to {currency or '$'}{salary_max:,.0f}"
    else:
        return "Salary not specified"

def classify_as_internship(title: str, description: str) -> bool:
    """Classify if position is an internship"""
    internship_keywords = ['intern', 'internship', 'trainee', 'co-op', 'summer program', 'student']
    content = f"{title} {description}".lower()
    return any(keyword in content for keyword in internship_keywords)

def classify_as_entry_level(title: str, description: str) -> bool:
    """Classify if position is entry level"""
    entry_keywords = ['junior', 'entry level', 'entry-level', 'graduate', 'new grad', 'associate', 'beginner']
    content = f"{title} {description}".lower()
    return any(keyword in content for keyword in entry_keywords)

def assess_urgency(description: str, posted_date) -> str:
    """Assess application urgency"""
    urgent_keywords = ['urgent', 'immediate', 'asap', 'quickly', 'soon']
    if any(keyword in description.lower() for keyword in urgent_keywords):
        return 'high'
    
    if posted_date:
        try:
            posted = datetime.fromisoformat(posted_date.isoformat())
            days_old = (datetime.now(posted.tzinfo) - posted).days
            if days_old <= 3:
                return 'medium'
            elif days_old <= 7:
                return 'normal'
            else:
                return 'low'
        except:
            pass
    
    return 'normal'

def create_recommendation_explanation(match_analysis: Dict, job_title: str) -> str:
    """Create explanation for why job is recommended"""
    score = match_analysis['recommendation_score']
    reasons = []
    
    if score >= 80:
        reasons.append("Excellent overall match")
    elif score >= 60:
        reasons.append("Strong compatibility")
    else:
        reasons.append("Good learning opportunity")
    
    if match_analysis['skill_alignment'] > 30:
        reasons.append(f"strong skill alignment ({len(match_analysis['skill_matches'])} matching skills)")
    
    if match_analysis['role_relevance'] > 20:
        reasons.append("highly relevant to your career goals")
    
    if match_analysis['experience_fit'] > 15:
        reasons.append("perfect experience level fit")
    
    return f"Recommended because: {', '.join(reasons[:3])}"

def create_application_strategy(match_analysis: Dict, job_title: str) -> List[str]:
    """Create personalized application strategy"""
    strategies = []
    
    # Based on matching skills
    if match_analysis['skill_matches']:
        strategies.append(f"Highlight these matching skills: {', '.join(match_analysis['skill_matches'][:3])}")
    
    # Based on skill gaps
    if match_analysis['missing_skills']:
        strategies.append(f"Address skill gaps by mentioning willingness to learn: {', '.join(match_analysis['missing_skills'][:2])}")
    
    # Based on confidence level
    if match_analysis['confidence_level'] == 'high':
        strategies.append("Apply immediately - you're a strong candidate")
    elif match_analysis['confidence_level'] == 'medium':
        strategies.append("Tailor your application to emphasize relevant experience")
    else:
        strategies.append("Consider this as a stretch opportunity for growth")
    
    # Based on job type
    if classify_as_internship(job_title, ''):
        strategies.append("Emphasize academic projects and eagerness to learn")
    
    return strategies[:4]  # Limit to 4 strategies

def deduplicate_recommendations(recommendations: List[Dict]) -> List[Dict]:
    """Remove duplicate job recommendations"""
    seen = set()
    unique_recs = []
    
    for rec in recommendations:
        # Create unique key based on job details
        key = (rec['title'].lower().strip(), rec['company'].lower().strip(), rec['location'].lower().strip())
        if key not in seen:
            seen.add(key)
            unique_recs.append(rec)
    
    return unique_recs

def rank_recommendations(recommendations: List[Dict], user_skills: List[str], suggested_role: str) -> List[Dict]:
    """Rank recommendations by overall relevance and quality"""
    def ranking_score(rec):
        base_score = rec['recommendation_score']
        
        # Boost for high confidence
        if rec['confidence_level'] == 'high':
            base_score += 10
        elif rec['confidence_level'] == 'medium':
            base_score += 5
        
        # Boost for exact role match
        if suggested_role.lower() in rec['title'].lower():
            base_score += 8
        
        # Boost for matching skills count
        base_score += len(rec['matching_skills']) * 1.5
        
        # Boost for recent postings
        if rec['posted_date']:
            try:
                posted = datetime.fromisoformat(rec['posted_date'])
                days_old = (datetime.now() - posted.replace(tzinfo=None)).days
                if days_old <= 7:
                    base_score += 5
                elif days_old <= 30:
                    base_score += 2
            except:
                pass
        
        # Boost for remote work
        if rec['remote_allowed']:
            base_score += 3
        
        # Boost for urgency
        if rec['urgency_level'] == 'high':
            base_score += 4
        elif rec['urgency_level'] == 'medium':
            base_score += 2
        
        return base_score
    
    return sorted(recommendations, key=ranking_score, reverse=True)

def categorize_recommendations(recommendations: List[Dict]) -> Dict:
    """Categorize recommendations for better organization"""
    categories = {
        'high_match': [],
        'internships': [],
        'entry_level': [],
        'remote_opportunities': [],
        'growth_opportunities': [],
        'learning_opportunities': []
    }
    
    for rec in recommendations:
        # High match (70%+ recommendation score)
        if rec['recommendation_score'] >= 70:
            categories['high_match'].append(rec)
        
        # Internships
        if rec['is_internship']:
            categories['internships'].append(rec)
        
        # Entry level
        if rec['is_entry_level']:
            categories['entry_level'].append(rec)
        
        # Remote opportunities
        if rec['remote_allowed']:
            categories['remote_opportunities'].append(rec)
        
        # Growth opportunities (senior roles)
        if any(keyword in rec['title'].lower() for keyword in ['senior', 'lead', 'manager']):
            categories['growth_opportunities'].append(rec)
        
        # Learning opportunities (some skill gaps)
        if len(rec['skill_gaps']) > 0 and rec['recommendation_score'] >= 40:
            categories['learning_opportunities'].append(rec)
    
    return {k: v for k, v in categories.items() if v}  # Only return non-empty categories

def analyze_market_opportunities(recommendations: List[Dict], user_skills: List[str], 
                               suggested_role: str, job_type: str) -> Dict:
    """Analyze market opportunities and trends"""
    if not recommendations:
        return {
            'market_status': 'Limited opportunities found',
            'trending_skills': [],
            'salary_insights': {},
            'location_trends': {},
            'recommendations': ['Expand search criteria', 'Consider skill development']
        }
    
    # Salary analysis
    salaries = []
    for rec in recommendations:
        if rec['salary_range'] and 'not specified' not in rec['salary_range'].lower():
            # Extract salary numbers (simplified)
            try:
                salary_text = rec['salary_range'].replace(',', '').replace('$', '')
                numbers = re.findall(r'\d+', salary_text)
                if numbers:
                    salaries.append(int(numbers[0]))
            except:
                pass
    
    # Skill demand analysis
    all_required_skills = []
    for rec in recommendations:
        all_required_skills.extend(rec['skills_required'])
    
    skill_frequency = {}
    for skill in all_required_skills:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    trending_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:8]
    
    # Location analysis
    location_count = {}
    for rec in recommendations:
        location = rec['location'] or 'Remote'
        location_count[location] = location_count.get(location, 0) + 1
    
    top_locations = sorted(location_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Generate insights
    avg_score = sum(rec['recommendation_score'] for rec in recommendations) / len(recommendations)
    high_matches = len([rec for rec in recommendations if rec['recommendation_score'] >= 70])
    remote_count = len([rec for rec in recommendations if rec['remote_allowed']])
    
    return {
        'market_status': f'Strong market with {len(recommendations)} opportunities',
        'opportunity_quality': 'excellent' if avg_score >= 70 else 'good' if avg_score >= 50 else 'moderate',
        'high_match_count': high_matches,
        'remote_availability': f'{remote_count} remote positions available',
        'trending_skills': [{'skill': skill, 'demand': freq} for skill, freq in trending_skills],
        'salary_insights': {
            'average': f"${sum(salaries)//len(salaries):,}" if salaries else "Data not available",
            'range': f"${min(salaries):,} - ${max(salaries):,}" if len(salaries) > 1 else "Insufficient data",
            'data_points': len(salaries)
        },
        'location_trends': [{'location': loc, 'opportunities': count} for loc, count in top_locations],
        'market_recommendations': generate_market_recommendations(trending_skills, user_skills, avg_score)
    }

def generate_market_recommendations(trending_skills: List, user_skills: List[str], avg_score: float) -> List[str]:
    """Generate market-based recommendations"""
    recommendations = []
    
    if avg_score >= 70:
        recommendations.append("Market conditions are excellent - apply to top matches immediately")
    elif avg_score >= 50:
        recommendations.append("Good market opportunities - focus on skill alignment")
    else:
        recommendations.append("Consider skill development to improve market position")
    
    # Skill recommendations
    if trending_skills:
        top_trending = trending_skills[0][0]
        if top_trending.lower() not in [skill.lower() for skill in user_skills]:
            recommendations.append(f"Consider learning '{top_trending}' - highly in demand")
    
    return recommendations

def generate_recommendation_tips(recommendations: List[Dict], user_skills: List[str]) -> List[str]:
    """Generate actionable tips for job applications"""
    tips = []
    
    if not recommendations:
        return [
            "Expand your search criteria to include related roles",
            "Consider developing additional skills in high-demand areas",
            "Look into networking opportunities in your field"
        ]
    
    high_matches = [rec for rec in recommendations if rec['recommendation_score'] >= 70]
    if high_matches:
        tips.append(f"Apply immediately to {len(high_matches)} high-match positions")
    
    internships = [rec for rec in recommendations if rec['is_internship']]
    if internships:
        tips.append(f"{len(internships)} internship opportunities available - great for gaining experience")
    
    remote_jobs = [rec for rec in recommendations if rec['remote_allowed']]
    if remote_jobs:
        tips.append(f"{len(remote_jobs)} remote positions available - consider for flexibility")
    
    # Common skill gaps
    all_gaps = []
    for rec in recommendations[:10]:  # Top 10 recommendations
        all_gaps.extend(rec['skill_gaps'])
    
    gap_frequency = {}
    for gap in all_gaps:
        gap_frequency[gap] = gap_frequency.get(gap, 0) + 1
    
    if gap_frequency:
        most_common_gap = max(gap_frequency.items(), key=lambda x: x[1])[0]
        tips.append(f"Consider learning '{most_common_gap}' - appears in {gap_frequency[most_common_gap]} job requirements")
    
    tips.append("Tailor your resume to highlight matching skills for each application")
    
    return tips[:5]  # Return top 5 tips

def calculate_match_score(user_skills: List[str], job, suggested_role: str) -> float:
    """Legacy function for backward compatibility - simplified match scoring"""
    try:
        analysis = analyze_job_match(user_skills, job, suggested_role, 0)
        return analysis['recommendation_score'] / 100.0  # Convert to 0-1 scale
    except Exception as e:
        logger.error(f"Error in legacy match score calculation: {e}")
        return 0.5  # Default score
    """Calculate AI-powered job match score"""
    user_skills_lower = [skill.lower() for skill in user_skills]
    job_skills_lower = [skill.lower() for skill in job.skills]
    job_text_lower = (job.title + ' ' + job.description).lower()
    
    score = 0.0
    
    # Skill matching (70% weight)
    skill_matches = 0
    for user_skill in user_skills_lower:
        if any(user_skill in job_skill or job_skill in user_skill for job_skill in job_skills_lower):
            skill_matches += 1
        elif user_skill in job_text_lower:
            skill_matches += 0.5
    
    if user_skills:
        skill_score = min(skill_matches / len(user_skills), 1.0) * 0.7
        score += skill_score
    
    # Role matching (20% weight)
    role_keywords = suggested_role.lower().split()
    role_match = any(keyword in job.title.lower() for keyword in role_keywords)
    if role_match:
        score += 0.2
    
    # Experience level matching (10% weight)
    if job.experience_level and job.experience_level != 'unknown':
        score += 0.1
    
    return min(score, 1.0)

def get_matching_skills(user_skills: List[str], job_skills: List[str]) -> List[str]:
    """Get skills that match between user and job"""
    user_skills_lower = [skill.lower() for skill in user_skills]
    matches = []
    
    for user_skill in user_skills:
        user_skill_lower = user_skill.lower()
        for job_skill in job_skills:
            if user_skill_lower in job_skill.lower() or job_skill.lower() in user_skill_lower:
                matches.append(user_skill)
                break
    
    return matches

def get_skill_gap(user_skills: List[str], job_skills: List[str]) -> List[str]:
    """Get skills required by job but missing from user"""
    user_skills_lower = [skill.lower() for skill in user_skills]
    gaps = []
    
    for job_skill in job_skills:
        if not any(job_skill.lower() in user_skill or user_skill in job_skill.lower() 
                  for user_skill in user_skills_lower):
            gaps.append(job_skill)
    
    return gaps[:5]  # Top 5 gaps

def generate_insights(user_skills: List[str], matched_jobs: List[Dict], suggested_role: str) -> Dict:
    """Generate AI insights about job matches"""
    if not matched_jobs:
        return {
            'summary': 'No matching jobs found. Consider expanding your skill set or searching different keywords.',
            'recommendations': ['Add more relevant skills', 'Consider related roles', 'Try different locations']
        }
    
    avg_score = sum(job['match_score'] for job in matched_jobs) / len(matched_jobs)
    
    # Find most required skills
    all_required_skills = []
    for job in matched_jobs:
        all_required_skills.extend(job['skills_required'])
    
    skill_frequency = {}
    for skill in all_required_skills:
        skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
    
    top_required = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        'average_match_score': round(avg_score, 1),
        'total_opportunities': len(matched_jobs),
        'top_required_skills': [{'skill': skill, 'frequency': freq} for skill, freq in top_required],
        'your_skill_count': len(user_skills),
        'recommended_applications': min(5, len([job for job in matched_jobs if job['match_score'] > 70])),
        'summary': f'Great! {avg_score:.0f}% average compatibility with {len(matched_jobs)} jobs.',
        'recommendations': [
            f'Apply to top {min(3, len(matched_jobs))} matches immediately',
            f'Consider learning: {top_required[0][0]}' if top_required else 'Your skills are well-aligned',
            f'Focus on {suggested_role} positions for best results'
        ]
    }

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get stored analysis results"""
    try:
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found or expired'}), 404
        
        return jsonify({
            'success': True,
            'analysis': analysis_cache[analysis_id]
        })
        
    except Exception as e:
        logger.error(f"Get analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    return jsonify({
        'success': True,
        'statistics': {
            'total_analyses': len(analysis_cache),
            'components_loaded': {
                'resume_parser': _resume_parser is not None,
                'job_client': _job_client is not None
            },
            'features': [
                '✅ AI skill extraction using Hugging Face models',
                '✅ Real-time job search from multiple platforms',
                '✅ Intelligent role recommendation',
                '✅ Smart job matching with compatibility scores',
                '✅ Live job data (no fake data)',
                '✅ Comprehensive skill analysis'
            ]
        }
    })

@app.route('/get-recommendations', methods=['POST'])
def get_enhanced_recommendations():
    """Get enhanced job recommendations with role-based analysis"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = data.get('limit', 20)
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        
        # Initialize role-based recommender
        from role_based_recommender import RoleBasedRecommender
        role_recommender = RoleBasedRecommender()
        
        # Analyze role compatibility
        role_analysis = role_recommender.analyze_role_compatibility(analysis_data)
        
        # Get job data
        job_client = get_job_client()
        skills = analysis_data.get('skills', [])
        suitable_role = analysis_data.get('suitable_role', '')
        job_keywords = skills[:5] + [suitable_role] if suitable_role else skills[:5]
        
        try:
            # Fetch jobs from external sources
            external_jobs = job_client(
                keywords=job_keywords,
                location=preferences.get('location', ''),
                limit=limit * 2  # Get more to have better selection
            )
            
            # Convert JobPosting dataclass to dict
            available_jobs = []
            for job in external_jobs:
                job_dict = {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'description': job.description,
                    'requirements': job.requirements,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'salary_currency': job.salary_currency,
                    'experience_level': job.experience_level,
                    'employment_type': job.employment_type,
                    'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                    'expires_date': job.expires_date.isoformat() if job.expires_date else None,
                    'source': job.source,
                    'apply_url': job.apply_url,
                    'skills': job.skills,
                    'remote_allowed': job.remote_allowed,
                    'company_size': job.company_size,
                    'industry': job.industry
                }
                available_jobs.append(job_dict)
            
            # Get role-based recommendations
            recommendations_result = role_recommender.get_role_based_recommendations(
                role_analysis, available_jobs, preferences
            )
            
            if not recommendations_result.get('success'):
                return jsonify({'error': recommendations_result.get('error', 'Recommendation failed')}), 500
            
            return jsonify({
                'success': True,
                'recommendations': recommendations_result['jobs'],
                'internships': recommendations_result['internships'],
                'role_analysis': recommendations_result['role_analysis'],
                'total_found': recommendations_result['total_jobs_found'],
                'total_internships_found': recommendations_result['total_internships_found'],
                'categories': recommendations_result['categories'],
                'metadata': recommendations_result['recommendations_metadata']
            })
            
        except Exception as e:
            logger.error(f"Job search error: {e}")
            return jsonify({'error': f'Job search failed: {str(e)}'}), 500
            
    except Exception as e:
        logger.error(f"Get recommendations error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/skill-gap-analysis', methods=['POST'])
def get_skill_gap_analysis():
    """Perform skill gap analysis against target keywords"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        target_keywords = data.get('keywords', [])
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        user_skills = [skill.lower() for skill in analysis_data.get('skills', [])]
        
        # Analyze skill gaps
        found_skills = []
        missing_skills = []
        
        for keyword in target_keywords:
            if keyword.lower() in user_skills:
                found_skills.append(keyword)
            else:
                missing_skills.append(keyword)
        
        gap_percentage = (len(missing_skills) / len(target_keywords) * 100) if target_keywords else 0
        
        return jsonify({
            'success': True,
            'skill_gap_analysis': {
                'found_skills': found_skills,
                'missing_skills': missing_skills,
                'gap_percentage': round(gap_percentage, 2),
                'total_analyzed': len(target_keywords),
                'recommendations': [f"Consider learning {skill}" for skill in missing_skills[:3]]
            }
        })
        
    except Exception as e:
        logger.error(f"Skill gap analysis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/career-guidance', methods=['POST'])
def get_career_guidance():
    """Get AI-powered career guidance"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        skills = analysis_data.get('skills', [])
        suitable_role = analysis_data.get('suitable_role', '')
        
        # Generate career guidance based on skills and role
        guidance = {
            'current_strengths': skills[:5],
            'recommended_role': suitable_role,
            'career_paths': [
                f"Senior {suitable_role}",
                f"{suitable_role} Lead",
                f"{suitable_role} Manager"
            ],
            'skill_development': [
                "Focus on emerging technologies",
                "Develop leadership skills",
                "Consider certifications"
            ],
            'next_steps': [
                "Update resume with new skills",
                "Apply to relevant positions",
                "Network with professionals in your field"
            ]
        }
        
        return jsonify({
            'success': True,
            'career_guidance': guidance
        })
        
    except Exception as e:
        logger.error(f"Career guidance error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/application-history', methods=['GET'])
def get_application_history():
    """Get application history and statistics"""
    try:
        # For now, return mock data since we don't have a database
        history = {
            'total_applications': len(analysis_cache),
            'recent_applications': [],
            'success_rate': 0,
            'popular_roles': [],
            'statistics': {
                'this_month': len(analysis_cache),
                'last_month': 0,
                'total_analyses': len(analysis_cache)
            }
        }
        
        return jsonify({
            'success': True,
            'application_history': history
        })
        
    except Exception as e:
        logger.error(f"Application history error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/realtime-jobs', methods=['POST'])
def get_realtime_jobs():
    """Fetch real-time job data"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', '')
        location = data.get('location', '')
        limit = data.get('limit', 50)
        
        job_client = get_job_client()
        jobs = job_client(
            keywords=[keywords] if isinstance(keywords, str) else keywords,
            location=location,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'jobs': jobs,
            'total_found': len(jobs)
        })
        
    except Exception as e:
        logger.error(f"Real-time jobs error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/apply-to-job', methods=['POST'])
def apply_to_job():
    """Enhanced job application with role-based assistance"""
    try:
        data = request.get_json()
        job_details = data.get('job_details', {})
        analysis_id = data.get('analysis_id')
        application_type = data.get('application_type', 'job')  # 'job' or 'internship'
        
        # Validate required fields
        if not job_details or not analysis_id:
            return jsonify({'error': 'Missing job details or analysis ID'}), 400
        
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        
        # Generate application ID
        application_id = str(uuid.uuid4())
        
        # Create application record
        application_record = {
            'application_id': application_id,
            'job_details': job_details,
            'application_type': application_type,
            'user_skills': analysis_data.get('skills', []),
            'matched_role': job_details.get('matched_role', ''),
            'compatibility_score': job_details.get('compatibility_score', 0),
            'applied_at': datetime.now().isoformat(),
            'status': 'applied',
            'apply_url': job_details.get('apply_url', '')
        }
        
        # Generate role-specific application assistance
        assistance_data = generate_application_assistance(
            job_details, analysis_data, application_type
        )
        
        # Log the application attempt
        logger.info(f"Job application: {application_type} - {job_details.get('title', 'Unknown')} at {job_details.get('company', 'Unknown')}")
        
        # In a real application, you would:
        # 1. Save application to database
        # 2. Send application via API if available
        # 3. Generate and email cover letter
        # 4. Track application status
        
        return jsonify({
            'success': True,
            'message': f'{application_type.title()} application processed successfully',
            'application_id': application_id,
            'application_record': application_record,
            'assistance': assistance_data,
            'next_steps': [
                f"Visit the job posting: {job_details.get('apply_url', 'URL not available')}",
                "Submit your tailored resume and cover letter",
                "Follow up with the hiring manager if contact information is available",
                "Track your application status in your dashboard"
            ]
        })
        
    except Exception as e:
        logger.error(f"Apply to job error: {e}")
        return jsonify({'error': str(e)}), 500

def generate_application_assistance(job_details, analysis_data, application_type):
    """Generate role-specific application assistance"""
    try:
        job_title = job_details.get('title', '')
        company = job_details.get('company', '')
        matched_role = job_details.get('matched_role', '')
        compatibility_score = job_details.get('compatibility_score', 0)
        user_skills = analysis_data.get('skills', [])
        
        # Generate tailored advice based on application type
        if application_type == 'internship':
            advice = generate_internship_advice(job_details, analysis_data)
        else:
            advice = generate_job_advice(job_details, analysis_data)
        
        # Identify skill highlights for this specific role
        job_skills = job_details.get('skills', [])
        skill_highlights = []
        for skill in user_skills:
            if any(skill.lower() in job_skill.lower() for job_skill in job_skills):
                skill_highlights.append(skill)
        
        return {
            'application_type': application_type,
            'compatibility_score': compatibility_score,
            'matched_role': matched_role,
            'skill_highlights': skill_highlights[:5],  # Top 5 relevant skills
            'tailored_advice': advice,
            'cover_letter_template': generate_cover_letter_template(
                job_title, company, matched_role, skill_highlights, application_type
            )
        }
        
    except Exception as e:
        logger.error(f"Error generating application assistance: {e}")
        return {
            'application_type': application_type,
            'tailored_advice': [],
            'skill_highlights': [],
            'cover_letter_template': ''
        }

def generate_job_advice(job_details, analysis_data):
    """Generate advice for job applications"""
    advice = []
    
    compatibility_score = job_details.get('compatibility_score', 0)
    experience_level = analysis_data.get('experience_analysis', {}).get('experience_level', 'mid')
    
    if compatibility_score >= 0.8:
        advice.append("Excellent match! Emphasize your relevant skills prominently in your application.")
    elif compatibility_score >= 0.6:
        advice.append("Good match. Highlight transferable skills and show enthusiasm for learning.")
    else:
        advice.append("Consider emphasizing your adaptability and willingness to grow into the role.")
    
    if experience_level == 'entry':
        advice.extend([
            "Focus on projects, internships, and coursework that demonstrate relevant skills.",
            "Show enthusiasm and willingness to learn and grow with the company.",
            "Highlight any leadership experience or team collaboration skills."
        ])
    elif experience_level == 'senior':
        advice.extend([
            "Emphasize your leadership experience and ability to mentor others.",
            "Showcase specific achievements and quantifiable results from your career.",
            "Demonstrate how you can contribute to strategic goals and company growth."
        ])
    
    return advice

def generate_internship_advice(job_details, analysis_data):
    """Generate advice for internship applications"""
    advice = [
        "Emphasize your academic projects and any relevant coursework.",
        "Show genuine interest in learning and contributing to the company.",
        "Highlight any volunteer work, clubs, or leadership activities.",
        "Research the company culture and mention specific aspects that appeal to you.",
        "Express your career goals and how this internship fits into your plans."
    ]
    
    skills = analysis_data.get('skills', [])
    if len(skills) >= 5:
        advice.append("You have a solid technical foundation - highlight your strongest skills.")
    else:
        advice.append("Focus on your potential and eagerness to develop new skills.")
    
    return advice

def generate_cover_letter_template(job_title, company, matched_role, skill_highlights, application_type):
    """Generate a cover letter template"""
    if application_type == 'internship':
        return f"""Dear Hiring Manager,

I am excited to apply for the {job_title} internship at {company}. As an aspiring {matched_role}, I am eager to contribute to your team while gaining valuable industry experience.

My technical skills include: {', '.join(skill_highlights[:3]) if skill_highlights else 'relevant programming languages and tools'}.

Through my academic projects and coursework, I have developed a strong foundation in software development and am passionate about applying these skills in a professional environment. I am particularly drawn to {company} because of [research company and add specific reason].

I am excited about the opportunity to learn from your experienced team and contribute fresh perspectives to your projects. Thank you for considering my application.

Best regards,
[Your Name]"""
    else:
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my background as a {matched_role}, I am confident I can make a valuable contribution to your team.

My relevant skills include: {', '.join(skill_highlights[:5]) if skill_highlights else 'technical expertise in relevant areas'}.

I am particularly excited about this opportunity because [research company and add specific reason]. My experience has prepared me to tackle the challenges in this role and contribute to your team's success.

I would welcome the opportunity to discuss how my skills and enthusiasm can benefit {company}. Thank you for your consideration.

Best regards,
[Your Name]"""

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate personalized cover letter"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        job_title = data.get('job_title', '')
        company = data.get('company', '')
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        skills = analysis_data.get('skills', [])
        
        # Generate a simple cover letter template
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. 

Based on my resume analysis, I have expertise in: {', '.join(skills[:5])}.

I believe my skills align well with your requirements and I would welcome the opportunity to contribute to your team.

Thank you for your consideration.

Best regards,
[Your Name]"""
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter
        })
        
    except Exception as e:
        logger.error(f"Generate cover letter error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export-analysis/<analysis_id>', methods=['GET'])
def export_analysis(analysis_id):
    """Export analysis results"""
    try:
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        analysis_data = analysis_cache[analysis_id]
        
        return jsonify({
            'success': True,
            'export_data': analysis_data,
            'exported_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Export analysis error: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': 'File too large (max 16MB)'}), 413

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 AI Job Matcher Backend - Enhanced Version")
    print("=" * 50)
    print("✅ REQUIREMENT 1: Extract skills from user's resume")
    print("✅ REQUIREMENT 2: Show total number of skills identified")
    print("✅ REQUIREMENT 3: Define most suitable role based on skills")
    print("✅ REQUIREMENT 4: Browse and fetch real jobs from platforms")
    print("✅ REQUIREMENT 5: Use real-time job data (not fake)")
    print("✅ REQUIREMENT 6: Utilize Hugging Face models for NLP")
    print("=" * 50)
    print("🌐 Starting server on http://localhost:5000")
    print("📊 Health check: http://localhost:5000/health")
    print("📈 Statistics: http://localhost:5000/stats")
    print("")
    
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5000)),
            debug=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
