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
            import io
            import re
            
            class SimpleResumeParser:
                def __init__(self):
                    self.skills_keywords = [
                        'python', 'javascript', 'java', 'react', 'node.js', 'sql', 'aws', 
                        'docker', 'kubernetes', 'git', 'html', 'css', 'mongodb', 'postgresql',
                        'machine learning', 'data science', 'artificial intelligence', 'flask',
                        'django', 'fastapi', 'express', 'angular', 'vue.js', 'typescript',
                        'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'
                    ]
                
                def extract_text_from_pdf(self, pdf_file):
                    try:
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                        return text
                    except Exception as e:
                        logger.error(f"PDF extraction error: {e}")
                        return ""
                
                def extract_skills(self, text):
                    text_lower = text.lower()
                    found_skills = []
                    for skill in self.skills_keywords:
                        if skill in text_lower:
                            found_skills.append(skill.title())
                    return list(set(found_skills))
                
                def extract_experience(self, text):
                    # Simple regex patterns for experience
                    exp_patterns = [
                        r'(\d+)[\+\s]*years?\s*(?:of\s*)?experience',
                        r'experience[:\s]*(\d+)[\+\s]*years?',
                        r'(\d+)[\+\s]*yrs?\s*(?:of\s*)?(?:exp|experience)'
                    ]
                    
                    years = []
                    for pattern in exp_patterns:
                        matches = re.findall(pattern, text.lower())
                        years.extend([int(match) for match in matches])
                    
                    return max(years) if years else 0
                
                def parse_resume(self, file_content, filename=""):
                    if filename.endswith('.pdf'):
                        text = self.extract_text_from_pdf(file_content)
                    else:
                        text = file_content.read().decode('utf-8', errors='ignore')
                    
                    return {
                        'text': text,
                        'skills': self.extract_skills(text),
                        'experience': self.extract_experience(text),
                        'filename': filename
                    }
            
            _resume_parser = SimpleResumeParser()
        except ImportError as e:
            logger.error(f"Failed to import dependencies: {e}")
            _resume_parser = None
    
    return _resume_parser

# API Routes
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Job Matcher API is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/upload-resume', methods=['POST', 'OPTIONS'])
def upload_resume():
    """Upload and analyze resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        parser = get_simple_resume_parser()
        if not parser:
            return jsonify({"error": "Resume parser not available"}), 500
        
        # Parse resume
        analysis = parser.parse_resume(file, file.filename)
        
        # Generate a simple ID for caching
        analysis_id = f"resume_{datetime.now().timestamp()}"
        analysis_cache[analysis_id] = analysis
        
        return jsonify({
            "id": analysis_id,
            "skills": analysis['skills'],
            "experience": analysis['experience'],
            "filename": analysis['filename'],
            "message": "Resume uploaded and analyzed successfully"
        })
    
    except Exception as e:
        logger.error(f"Resume upload error: {e}")
        return jsonify({"error": "Failed to process resume"}), 500

@app.route('/api/job-recommendations', methods=['POST', 'OPTIONS'])
def get_job_recommendations():
    """Get job recommendations based on resume analysis"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        
        if not resume_id or resume_id not in analysis_cache:
            return jsonify({"error": "Invalid resume ID"}), 400
        
        resume_data = analysis_cache[resume_id]
        
        # Simple mock job recommendations
        mock_jobs = [
            {
                "id": "job_1",
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "San Francisco, CA",
                "salary": "$120,000 - $150,000",
                "match_score": 85,
                "skills_match": resume_data['skills'][:3],
                "description": "We are looking for a skilled software engineer...",
                "requirements": ["Bachelor's degree", "3+ years experience", "Python", "JavaScript"]
            },
            {
                "id": "job_2",
                "title": "Full Stack Developer",
                "company": "StartupXYZ",
                "location": "Remote",
                "salary": "$100,000 - $130,000",
                "match_score": 78,
                "skills_match": resume_data['skills'][:2],
                "description": "Join our dynamic team as a full stack developer...",
                "requirements": ["React", "Node.js", "Database experience", "Git"]
            },
            {
                "id": "job_3",
                "title": "Data Scientist",
                "company": "DataCorp",
                "location": "New York, NY",
                "salary": "$130,000 - $160,000",
                "match_score": 72,
                "skills_match": ["Python", "Machine Learning"],
                "description": "Seeking a data scientist to analyze complex datasets...",
                "requirements": ["Machine Learning", "Python", "Statistics", "SQL"]
            }
        ]
        
        return jsonify({
            "recommendations": mock_jobs,
            "total": len(mock_jobs),
            "resume_skills": resume_data['skills']
        })
    
    except Exception as e:
        logger.error(f"Job recommendations error: {e}")
        return jsonify({"error": "Failed to get job recommendations"}), 500

@app.route('/api/match-score', methods=['POST', 'OPTIONS'])
def calculate_match_score():
    """Calculate job match score"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_description = data.get('job_description', '')
        
        if not resume_id or resume_id not in analysis_cache:
            return jsonify({"error": "Invalid resume ID"}), 400
        
        resume_data = analysis_cache[resume_id]
        
        # Simple match scoring based on skills overlap
        job_text = job_description.lower()
        resume_skills = [skill.lower() for skill in resume_data['skills']]
        
        matches = sum(1 for skill in resume_skills if skill in job_text)
        total_skills = len(resume_skills)
        
        match_score = (matches / max(total_skills, 1)) * 100
        
        return jsonify({
            "match_score": round(match_score, 1),
            "matched_skills": [skill for skill in resume_data['skills'] if skill.lower() in job_text],
            "total_skills": total_skills
        })
    
    except Exception as e:
        logger.error(f"Match score error: {e}")
        return jsonify({"error": "Failed to calculate match score"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# For local testing
if __name__ == '__main__':
    app.run(debug=True)
