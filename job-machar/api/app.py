"""
Vercel-optimized Flask API for AI Job Matcher
Simplified for serverless deployment
"""

import os
import sys
import json
import tempfile
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure CORS for production
CORS(app, origins=['*'], allow_headers=['Content-Type', 'Authorization'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Global storage for analysis results (in-memory for serverless)
analysis_cache = {}

# Lazy-loaded components
_resume_parser = None
_job_client = None

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

def get_simple_resume_parser():
    """Simple resume parser for Vercel deployment"""
    global _resume_parser
    if _resume_parser is None:
        try:
            import PyPDF2
            import re
            
            class SimpleResumeParser:
                def parse_resume(self, file_content, filename):
                    """Simple resume parsing"""
                    try:
                        if filename.endswith('.pdf'):
                            # Handle PDF
                            import io
                            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                            text = ""
                            for page in pdf_reader.pages:
                                text += page.extract_text()
                        else:
                            # Handle text file
                            text = file_content.decode('utf-8')
                        
                        # Simple extraction
                        skills = self.extract_skills(text)
                        experience = self.extract_experience(text)
                        education = self.extract_education(text)
                        
                        return {
                            'text': text,
                            'skills': skills,
                            'experience': experience,
                            'education': education,
                            'summary': f"Resume parsed with {len(skills)} skills identified"
                        }
                    except Exception as e:
                        logger.error(f"Resume parsing error: {e}")
                        return {'error': str(e)}
                
                def extract_skills(self, text):
                    """Extract skills from text"""
                    common_skills = [
                        'Python', 'JavaScript', 'React', 'Node.js', 'Flask', 'Django',
                        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Docker', 'AWS',
                        'Azure', 'GCP', 'Kubernetes', 'Git', 'CI/CD', 'API',
                        'Machine Learning', 'AI', 'Data Science', 'Analytics'
                    ]
                    
                    found_skills = []
                    text_upper = text.upper()
                    for skill in common_skills:
                        if skill.upper() in text_upper:
                            found_skills.append(skill)
                    
                    return found_skills
                
                def extract_experience(self, text):
                    """Extract experience from text"""
                    exp_patterns = [
                        r'(\d+)\s*years?\s*of\s*experience',
                        r'(\d+)\s*years?\s*experience',
                        r'(\d+)\+\s*years?'
                    ]
                    
                    for pattern in exp_patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            return f"{match.group(1)} years"
                    
                    return "Experience level not specified"
                
                def extract_education(self, text):
                    """Extract education from text"""
                    edu_keywords = ['Bachelor', 'Master', 'PhD', 'Degree', 'University', 'College']
                    
                    for keyword in edu_keywords:
                        if keyword.lower() in text.lower():
                            return f"Education includes {keyword}"
                    
                    return "Education not specified"
            
            _resume_parser = SimpleResumeParser()
            logger.info("Simple Resume Parser loaded")
        except Exception as e:
            logger.error(f"Failed to load resume parser: {e}")
            _resume_parser = None
    
    return _resume_parser

def get_simple_job_client():
    """Simple job search client"""
    global _job_client
    if _job_client is None:
        try:
            import requests
            
            def search_jobs_simple(query, location="Remote", limit=10):
                """Simple job search using free APIs"""
                try:
                    # Mock job data for demo (replace with actual API calls)
                    mock_jobs = [
                        {
                            "id": f"job_{i}",
                            "title": f"{query} Developer",
                            "company": f"Tech Company {i}",
                            "location": location,
                            "description": f"We are looking for a skilled {query} developer to join our team...",
                            "requirements": f"Strong skills in {query}, teamwork, and problem-solving.",
                            "salary": f"${50000 + i * 10000} - ${70000 + i * 10000}",
                            "remote": True,
                            "url": f"https://example.com/job/{i}"
                        }
                        for i in range(1, min(limit + 1, 6))
                    ]
                    
                    return {
                        "success": True,
                        "jobs": mock_jobs,
                        "total": len(mock_jobs)
                    }
                except Exception as e:
                    logger.error(f"Job search error: {e}")
                    return {"success": False, "error": str(e), "jobs": []}
            
            _job_client = search_jobs_simple
            logger.info("Simple Job Client loaded")
        except Exception as e:
            logger.error(f"Failed to load job client: {e}")
            _job_client = None
    
    return _job_client

def calculate_simple_compatibility(skills, job):
    """Simple compatibility calculation"""
    try:
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}".lower()
        matches = 0
        total_skills = len(skills)
        
        if total_skills == 0:
            return 50  # Default score if no skills
        
        for skill in skills:
            if skill.lower() in job_text:
                matches += 1
        
        score = (matches / total_skills) * 100
        return min(max(score, 10), 95)  # Keep between 10-95%
    except:
        return 50

# API Routes
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Job Matcher API is running on Vercel",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Parse resume
        parser = get_simple_resume_parser()
        if not parser:
            return jsonify({"error": "Resume parser not available"}), 500
        
        file_content = file.read()
        result = parser.parse_resume(file_content, file.filename)
        
        if 'error' in result:
            return jsonify({"error": result['error']}), 400
        
        # Store in cache (session-based for serverless)
        user_id = request.form.get('user_id', 'anonymous')
        analysis_cache[user_id] = result
        
        return jsonify({
            "success": True,
            "message": "Resume uploaded and parsed successfully",
            "data": result
        })
    
    except Exception as e:
        logger.error(f"Upload resume error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/search-jobs', methods=['POST'])
def search_jobs():
    """Search for jobs"""
    try:
        data = request.get_json()
        query = data.get('query', 'Software Developer')
        location = data.get('location', 'Remote')
        limit = data.get('limit', 10)
        
        job_client = get_simple_job_client()
        if not job_client:
            return jsonify({"error": "Job search not available"}), 500
        
        results = job_client(query, location, limit)
        
        return jsonify({
            "success": True,
            "jobs": results.get('jobs', []),
            "total": results.get('total', 0)
        })
    
    except Exception as e:
        logger.error(f"Search jobs error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-recommendations', methods=['POST'])
def get_recommendations():
    """Get job recommendations based on resume"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        preferences = data.get('preferences', {})
        
        # Get user resume data
        user_data = analysis_cache.get(user_id)
        if not user_data:
            return jsonify({"error": "No resume data found. Please upload a resume first."}), 400
        
        # Search for jobs
        job_client = get_simple_job_client()
        if not job_client:
            return jsonify({"error": "Job search not available"}), 500
        
        # Use skills for job search
        skills = user_data.get('skills', [])
        query = preferences.get('role', skills[0] if skills else 'Developer')
        location = preferences.get('location', 'Remote')
        
        job_results = job_client(query, location, 20)
        jobs = job_results.get('jobs', [])
        
        # Calculate compatibility scores
        recommendations = []
        for job in jobs:
            score = calculate_simple_compatibility(skills, job)
            recommendations.append({
                **job,
                'compatibility_score': score,
                'matched_skills': [skill for skill in skills if skill.lower() in job.get('description', '').lower()]
            })
        
        # Sort by compatibility score
        recommendations.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return jsonify({
            "success": True,
            "recommendations": recommendations[:10],
            "total": len(recommendations),
            "user_skills": skills
        })
    
    except Exception as e:
        logger.error(f"Get recommendations error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/job-match', methods=['POST'])
def job_match():
    """Match jobs with user profile"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        job_id = data.get('job_id')
        
        user_data = analysis_cache.get(user_id)
        if not user_data:
            return jsonify({"error": "No user profile found"}), 400
        
        # For demo, return a sample match analysis
        return jsonify({
            "success": True,
            "match_score": 85,
            "matched_skills": user_data.get('skills', [])[:3],
            "missing_skills": ["Advanced Python", "Cloud Architecture"],
            "recommendation": "Strong match! Consider highlighting your experience with the matched skills."
        })
    
    except Exception as e:
        logger.error(f"Job match error: {e}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# For Vercel
def handler(event, context):
    """Vercel serverless function handler"""
    return app(event, context)

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=5000)
