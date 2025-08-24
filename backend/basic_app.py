"""
Basic AI-Powered Resume Analyzer and Job Recommender Backend API
Lightweight version without large transformer models
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import logging
from datetime import datetime
import uuid
import json
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Basic imports without heavy models
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("⚠️  PDF libraries not available")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError:
    print("⚠️  Scikit-learn not available")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

class BasicResumeAnalyzer:
    """Basic resume analyzer using only lightweight libraries"""
    
    def __init__(self):
        self.skills_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask'],
            'data': ['sql', 'mysql', 'postgresql', 'mongodb', 'pandas', 'numpy', 'scipy', 'matplotlib'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform'],
            'ai_ml': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp']
        }
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF using basic methods"""
        text = ""
        try:
            # Try pdfplumber first
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            try:
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                print(f"Error extracting PDF text: {e2}")
                
        return text
    
    def extract_basic_info(self, text):
        """Extract basic information using regex patterns"""
        info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        info['email'] = emails[0] if emails else None
        
        # Extract phone
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        phones = re.findall(phone_pattern, text)
        info['phone'] = ''.join(phones[0]) if phones else None
        
        # Extract name (first two capitalized words)
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        names = re.findall(name_pattern, text)
        info['name'] = names[0] if names else "Not found"
        
        return info
    
    def extract_skills(self, text):
        """Extract skills using keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'skill': skill,
                        'category': category,
                        'confidence': 0.8  # Basic confidence score
                    })
        
        return found_skills
    
    def analyze_experience(self, text):
        """Basic experience analysis"""
        text_lower = text.lower()
        
        # Count years mentioned
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        
        # Experience keywords
        exp_keywords = ['experience', 'worked', 'developed', 'managed', 'led', 'created']
        exp_count = sum(1 for keyword in exp_keywords if keyword in text_lower)
        
        # Rough experience estimation
        if len(years) >= 4 or exp_count >= 5:
            level = "Senior"
        elif len(years) >= 2 or exp_count >= 3:
            level = "Mid-level"
        else:
            level = "Entry-level"
            
        return {
            'level': level,
            'years_mentioned': len(years),
            'experience_indicators': exp_count
        }
    
    def analyze_resume(self, file_path):
        """Main resume analysis function"""
        try:
            # Extract text
            text = self.extract_text_from_pdf(file_path)
            
            if not text.strip():
                return {'error': 'Could not extract text from PDF'}
            
            # Extract information
            basic_info = self.extract_basic_info(text)
            skills = self.extract_skills(text)
            experience = self.analyze_experience(text)
            
            # Calculate quality score
            quality_score = min(100, 
                30 + 
                (10 if basic_info['email'] else 0) +
                (10 if basic_info['phone'] else 0) +
                (len(skills) * 2) +
                (experience['experience_indicators'] * 5)
            )
            
            return {
                'success': True,
                'basic_info': basic_info,
                'skills': skills,
                'experience': experience,
                'quality_score': quality_score,
                'text_length': len(text),
                'total_skills': len(skills)
            }
            
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}

class BasicJobRecommender:
    """Basic job recommender using simple matching"""
    
    def __init__(self):
        self.sample_jobs = [
            {
                'id': '1',
                'title': 'Python Developer',
                'company': 'Tech Corp',
                'location': 'Remote',
                'required_skills': ['python', 'django', 'flask', 'sql'],
                'description': 'Looking for a Python developer with web framework experience',
                'salary': '$70,000 - $90,000'
            },
            {
                'id': '2',
                'title': 'Data Scientist',
                'company': 'Data Solutions',
                'location': 'New York',
                'required_skills': ['python', 'machine learning', 'pandas', 'sql'],
                'description': 'Data scientist role requiring ML and Python skills',
                'salary': '$80,000 - $120,000'
            },
            {
                'id': '3',
                'title': 'Frontend Developer',
                'company': 'Web Studio',
                'location': 'San Francisco',
                'required_skills': ['javascript', 'react', 'html', 'css'],
                'description': 'Frontend developer for modern web applications',
                'salary': '$65,000 - $85,000'
            },
            {
                'id': '4',
                'title': 'DevOps Engineer',
                'company': 'Cloud Systems',
                'location': 'Seattle',
                'required_skills': ['aws', 'docker', 'kubernetes', 'jenkins'],
                'description': 'DevOps engineer for cloud infrastructure',
                'salary': '$90,000 - $130,000'
            }
        ]
    
    def calculate_job_match(self, user_skills, job_skills):
        """Calculate match score between user skills and job requirements"""
        user_skill_names = [skill['skill'].lower() for skill in user_skills]
        job_skill_names = [skill.lower() for skill in job_skills]
        
        matches = sum(1 for skill in job_skill_names if skill in user_skill_names)
        total_required = len(job_skill_names)
        
        if total_required == 0:
            return 0
        
        return (matches / total_required) * 100
    
    def recommend_jobs(self, resume_analysis):
        """Recommend jobs based on resume analysis"""
        try:
            user_skills = resume_analysis.get('skills', [])
            recommendations = []
            
            for job in self.sample_jobs:
                match_score = self.calculate_job_match(user_skills, job['required_skills'])
                
                if match_score > 0:  # Only include jobs with some match
                    recommendations.append({
                        **job,
                        'match_score': round(match_score, 1),
                        'matched_skills': [
                            skill for skill in job['required_skills'] 
                            if skill.lower() in [s['skill'].lower() for s in user_skills]
                        ]
                    })
            
            # Sort by match score
            recommendations.sort(key=lambda x: x['match_score'], reverse=True)
            
            return {
                'success': True,
                'recommendations': recommendations[:10],  # Top 10
                'total_jobs_analyzed': len(self.sample_jobs)
            }
            
        except Exception as e:
            return {'error': f'Job recommendation failed: {str(e)}'}

# Initialize analyzers
print("🚀 Initializing Basic AI Job Matcher...")
resume_analyzer = BasicResumeAnalyzer()
job_recommender = BasicJobRecommender()
print("✅ Basic AI Job Matcher initialized successfully!")

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'Basic AI Job Matcher API',
        'version': '1.0.0',
        'status': 'running',
        'features': ['Basic Resume Analysis', 'Simple Job Recommendations'],
        'endpoints': ['/analyze', '/recommend', '/health']
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'memory_usage': 'low',
        'ai_models': 'basic'
    })

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze uploaded resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            file.save(temp_file.name)
            
            # Analyze resume
            analysis = resume_analyzer.analyze_resume(temp_file.name)
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            if 'error' in analysis:
                return jsonify(analysis), 400
            
            return jsonify(analysis)
            
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    """Get job recommendations based on resume analysis"""
    try:
        data = request.get_json()
        
        if not data or 'resume_analysis' not in data:
            return jsonify({'error': 'Resume analysis data required'}), 400
        
        recommendations = job_recommender.recommend_jobs(data['resume_analysis'])
        
        if 'error' in recommendations:
            return jsonify(recommendations), 400
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({'error': f'Recommendation failed: {str(e)}'}), 500

@app.route('/jobs', methods=['GET'])
def get_sample_jobs():
    """Get sample job listings"""
    return jsonify({
        'success': True,
        'jobs': job_recommender.sample_jobs,
        'total': len(job_recommender.sample_jobs)
    })

if __name__ == '__main__':
    print("🚀 Starting Basic AI Job Matcher API on port 5001")
    print("🔧 Debug mode: False")
    print("📊 Features: Basic Resume Analysis, Simple Job Recommendations")
    app.run(host='0.0.0.0', port=5001, debug=False)
