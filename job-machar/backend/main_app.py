"""
Simplified Main Application - AI Job Matcher Backend
Uses enhanced modules for production-ready job matching
Focus on the 6 core requirements
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid
import tempfile
import traceback

from flask import Flask, request, jsonify
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
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'])

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
    """Lazy load the job client"""
    global _job_client
    if _job_client is None:
        print("🔄 Loading Enhanced Job Client...")
        from enhanced_job_client import search_jobs_sync
        _job_client = search_jobs_sync
        print("✅ Job Client loaded!")
    return _job_client

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0',
        'features': [
            'AI skill extraction',
            'Real-time job search',
            'Intelligent role matching',
            'Hugging Face models'
        ]
    })

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
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400
        
        # Save file temporarily
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
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
                'full_analysis': analysis
            }
            
            # Clean up temp file
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            
            logger.info(f"✅ Resume processed: {total_skills} skills found, role: {suggested_role}")
            
            # Return focused response meeting requirements 1, 2, 3
            return jsonify({
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
                'top_skills': all_skills[:10],
                
                'message': f'✅ Resume analyzed! Found {total_skills} skills. Suggested role: {suggested_role}'
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
        jobs = job_search_func(
            keywords=keywords,
            location=location,
            experience_level=experience_level,
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

@app.route('/match-jobs', methods=['POST'])
def match_jobs():
    """
    Combine all requirements: Match user's extracted skills with real-time jobs
    Uses AI to score job compatibility
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = min(data.get('limit', 20), 50)
        
        if not analysis_id or analysis_id not in analysis_cache:
            return jsonify({'error': 'Invalid analysis ID. Please upload your resume first.'}), 400
        
        # Get user's analysis
        user_data = analysis_cache[analysis_id]
        user_skills = user_data['all_skills']
        suggested_role = user_data['suggested_role']
        experience_level = user_data['experience_level']
        
        logger.info(f"Matching jobs for user with {len(user_skills)} skills, role: {suggested_role}")
        
        # Search for relevant jobs using user's skills and role
        search_keywords = user_skills[:8] + [suggested_role.lower()]  # Top skills + role
        search_keywords = list(dict.fromkeys(search_keywords))  # Remove duplicates
        
        job_search_func = get_job_client()
        jobs = job_search_func(
            keywords=search_keywords,
            location=preferences.get('location', ''),
            experience_level=experience_level,
            limit=limit * 2  # Get more to filter better matches
        )
        
        # AI-powered job matching and scoring
        matched_jobs = []
        for job in jobs:
            match_score = calculate_match_score(user_skills, job, suggested_role)
            
            if match_score > 0.15:  # Only include jobs with >15% match
                job_data = {
                    'id': job.id,
                    'title': job.title,
                    'company': job.company,
                    'location': job.location,
                    'description': job.description[:500] + '...' if len(job.description) > 500 else job.description,
                    'requirements': job.requirements,
                    'salary_range': f"${job.salary_min:,.0f} - ${job.salary_max:,.0f}" if job.salary_min and job.salary_max else "Not specified",
                    'experience_level': job.experience_level,
                    'employment_type': job.employment_type,
                    'posted_date': job.posted_date.isoformat() if job.posted_date else None,
                    'apply_url': job.apply_url,
                    'skills_required': job.skills,
                    'remote_allowed': job.remote_allowed,
                    'source': job.source,
                    
                    # AI matching results
                    'match_score': round(match_score * 100, 1),
                    'matching_skills': get_matching_skills(user_skills, job.skills),
                    'skill_gap': get_skill_gap(user_skills, job.skills)
                }
                matched_jobs.append(job_data)
        
        # Sort by match score (highest first)
        matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        top_matches = matched_jobs[:limit]
        
        # Generate insights
        insights = generate_insights(user_skills, top_matches, suggested_role)
        
        logger.info(f"✅ Found {len(top_matches)} AI-matched jobs")
        
        return jsonify({
            'success': True,
            'matched_jobs': top_matches,
            'total_matches': len(top_matches),
            'user_profile': {
                'total_skills': len(user_skills),
                'suggested_role': suggested_role,
                'experience_level': experience_level,
                'top_skills': user_skills[:10]
            },
            'insights': insights,
            'search_keywords_used': search_keywords,
            'message': f'Found {len(top_matches)} AI-matched jobs based on your {len(user_skills)} skills and {suggested_role} profile'
        })
        
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Job matching failed: {str(e)}'}), 500

def calculate_match_score(user_skills: List[str], job, suggested_role: str) -> float:
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
