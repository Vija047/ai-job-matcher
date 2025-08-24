"""
Production AI-Powered Job Matcher Backend API (Lightweight Version)
Flask application with basic functionality, fallback for heavy AI models
"""

import os
import warnings
import logging
from datetime import datetime
import uuid
import json

warnings.filterwarnings("ignore")

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file = os.getenv('LOG_FILE', 'app.log')

logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-in-production')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))  # 16MB
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure CORS
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# Try to initialize AI components with fallbacks
print("Initializing AI Job Matcher...")
try:
    from advanced_resume_parser import AdvancedResumeParser
    resume_parser = AdvancedResumeParser()
    AI_FEATURES_AVAILABLE = True
    logger.info("Advanced Resume Parser initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize Advanced Resume Parser: {str(e)}")
    resume_parser = None
    AI_FEATURES_AVAILABLE = False

try:
    from job_api_client import JobAPIClient
    job_client = JobAPIClient()
    logger.info("Job API Client initialized successfully")
except Exception as e:
    logger.warning(f"⚠️ Could not initialize Job API Client: {str(e)}")
    job_client = None

# Session storage (use Redis/Database in production)
user_sessions = {}
analysis_cache = {}

# ================================
# Utility Functions
# ================================

def generate_mock_analysis():
    """Generate mock analysis when AI features are not available"""
    return {
        'contact_info': {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-234-567-8900',
            'linkedin': 'linkedin.com/in/johndoe',
            'github': 'github.com/johndoe'
        },
        'skills': {
            'technical_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'AWS', 'Docker'],
            'soft_skills': ['Communication', 'Problem Solving', 'Team Leadership', 'Project Management'],
            'programming_languages': ['Python', 'JavaScript', 'Java', 'C++'],
            'frameworks': ['React', 'Django', 'Express.js', 'Flask'],
            'databases': ['MySQL', 'PostgreSQL', 'MongoDB'],
            'tools': ['Git', 'Docker', 'Jenkins', 'VS Code']
        },
        'education': [
            {
                'degree': 'Bachelor of Computer Science',
                'institution': 'University of Technology',
                'year': 2021,
                'gpa': '3.8/4.0'
            }
        ],
        'experience': [
            {
                'title': 'Software Developer',
                'company': 'Tech Solutions Inc.',
                'duration': '2021-2023',
                'responsibilities': [
                    'Developed web applications using React and Node.js',
                    'Collaborated with cross-functional teams',
                    'Maintained and optimized database systems'
                ]
            }
        ],
        'certifications': [
            'AWS Certified Developer Associate',
            'Google Cloud Professional Developer'
        ]
    }

def generate_mock_job_matches():
    """Generate mock job matches"""
    return [
        {
            'job_title': 'Senior Python Developer',
            'company': 'TechCorp Inc.',
            'location': 'San Francisco, CA',
            'salary_range': '$80,000 - $120,000',
            'overall_score': 85,
            'skill_match_score': 88,
            'experience_match_score': 82,
            'recommendation': 'Excellent Match',
            'match_reasons': [
                'Strong Python experience',
                'Relevant framework knowledge',
                'Good cultural fit'
            ],
            'job_description': 'We are looking for a Senior Python Developer with 3+ years experience...',
            'requirements': ['Python', 'Django', 'PostgreSQL', 'AWS'],
            'posted_date': '2024-08-10',
            'application_deadline': '2024-09-10'
        },
        {
            'job_title': 'Full Stack Developer',
            'company': 'StartupXYZ',
            'location': 'Remote',
            'salary_range': '$70,000 - $100,000',
            'overall_score': 78,
            'skill_match_score': 80,
            'experience_match_score': 75,
            'recommendation': 'Good Match',
            'match_reasons': [
                'Full stack skills match',
                'Remote work experience',
                'Startup environment fit'
            ],
            'job_description': 'Join our dynamic startup as a Full Stack Developer...',
            'requirements': ['JavaScript', 'React', 'Node.js', 'MongoDB'],
            'posted_date': '2024-08-12',
            'application_deadline': '2024-09-15'
        },
        {
            'job_title': 'Frontend Developer',
            'company': 'DesignCo',
            'location': 'New York, NY',
            'salary_range': '$65,000 - $90,000',
            'overall_score': 72,
            'skill_match_score': 85,
            'experience_match_score': 65,
            'recommendation': 'Moderate Match',
            'match_reasons': [
                'Strong frontend skills',
                'React expertise',
                'Design collaboration experience'
            ],
            'job_description': 'We need a Frontend Developer to join our design team...',
            'requirements': ['React', 'CSS', 'JavaScript', 'Figma'],
            'posted_date': '2024-08-08',
            'application_deadline': '2024-09-08'
        }
    ]

# ================================
# API Endpoints
# ================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'ai_features_available': AI_FEATURES_AVAILABLE,
        'mode': 'lightweight' if not AI_FEATURES_AVAILABLE else 'full'
    })

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload and analysis"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Save file
        filename = f"{analysis_id}_{file.filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Try AI analysis first, fallback to mock data
        if AI_FEATURES_AVAILABLE and resume_parser:
            try:
                analysis_result = resume_parser.parse_resume(filepath)
                logger.info("AI resume analysis completed")
            except Exception as e:
                logger.warning(f"⚠️ AI analysis failed, using mock data: {str(e)}")
                analysis_result = generate_mock_analysis()
        else:
            logger.info("ℹ️ Using mock analysis data")
            analysis_result = generate_mock_analysis()
        
        # Generate job matches
        job_matches = generate_mock_job_matches()
        
        # Store in cache
        analysis_cache[analysis_id] = {
            'filename': file.filename,
            'filepath': filepath,
            'timestamp': datetime.now().isoformat(),
            'resume_analysis': analysis_result,
            'job_matches': job_matches
        }
        
        # Return response matching frontend expectations
        return jsonify({
            'analysis_id': analysis_id,
            'filename': file.filename,
            'resume_summary': {
                'total_skills': len(analysis_result.get('skills', {}).get('technical_skills', [])),
                'experience_level': 'mid-level',
                'years_experience': 3,
                'contact_info': analysis_result.get('contact_info', {})
            },
            'top_matches': [
                {
                    'job_title': match['job_title'],
                    'company': match['company'],
                    'overall_score': match['overall_score'],
                    'recommendation': match['recommendation'],
                    'salary_range': match['salary_range']
                }
                for match in job_matches[:3]
            ]
        })
        
    except Exception as e:
        logger.error(f"Resume upload error: {str(e)}")
        return jsonify({'error': 'Failed to process resume'}), 500

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get detailed analysis results"""
    try:
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        data = analysis_cache[analysis_id]
        
        return jsonify({
            'analysis_id': analysis_id,
            'filename': data['filename'],
            'timestamp': data['timestamp'],
            'resume_analysis': data['resume_analysis'],
            'job_matches': data['job_matches'],
            'ai_powered': AI_FEATURES_AVAILABLE
        })
        
    except Exception as e:
        logger.error(f"Analysis retrieval error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve analysis'}), 500

@app.route('/jobs/search', methods=['GET'])
def search_jobs():
    """Search for jobs"""
    try:
        query = request.args.get('query', 'software developer')
        location = request.args.get('location', 'remote')
        
        # Try real job search first, fallback to mock data
        if job_client:
            try:
                jobs = job_client.search_jobs(query, location)
                logger.info("Real job search completed")
            except Exception as e:
                logger.warning(f"⚠️ Real job search failed, using mock data: {str(e)}")
                jobs = generate_mock_job_matches()
        else:
            logger.info("ℹ️ Using mock job data")
            jobs = generate_mock_job_matches()
        
        return jsonify({
            'jobs': jobs,
            'total_results': len(jobs),
            'query': query,
            'location': location,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Job search error: {str(e)}")
        return jsonify({'error': 'Failed to search jobs'}), 500

@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    """Get all available jobs"""
    try:
        # Return mock jobs for compatibility
        jobs = generate_mock_job_matches()
        return jsonify({
            'jobs': jobs,
            'total_results': len(jobs),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Get jobs error: {str(e)}")
        return jsonify({'error': 'Failed to get jobs'}), 500

@app.route('/job-match', methods=['POST'])
def get_job_match():
    """Get job match details"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        analysis_id = data.get('analysis_id')
        
        if not job_id or not analysis_id:
            return jsonify({'error': 'job_id and analysis_id required'}), 400
        
        # Get analysis from cache
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Return mock match score for now
        match_score = 0.85  # Mock score
        return jsonify({
            'match_score': match_score,
            'job_id': job_id,
            'analysis_id': analysis_id,
            'compatibility': 'High',
            'reasons': ['Skills match', 'Experience level appropriate', 'Location compatible']
        })
        
    except Exception as e:
        logger.error(f"Job match error: {str(e)}")
        return jsonify({'error': 'Failed to get job match'}), 500

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Get job recommendations based on analysis"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        preferences = data.get('preferences', {})
        limit = data.get('limit', 20)
        
        if not analysis_id:
            return jsonify({'error': 'Analysis ID required'}), 400
        
        # Get analysis from cache
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Generate mock recommendations
        recommendations = generate_mock_job_matches()[:limit]
        
        # Add match scores to each recommendation
        for i, job in enumerate(recommendations):
            job['match_score'] = 0.9 - (i * 0.05)  # Decreasing scores
            job['match_reasons'] = ['Skills alignment', 'Experience match', 'Location preference']
        
        return jsonify({
            'recommendations': recommendations,
            'total_found': len(recommendations),
            'insights': {
                'top_skills_matched': ['Python', 'JavaScript', 'React'],
                'experience_level': 'Mid-level',
                'location_match': 'Good'
            },
            'statistics': {
                'avg_salary': 75000,
                'total_positions': len(recommendations)
            },
            'search_keywords': ['software developer', 'full stack', 'python'],
            'message': f'Found {len(recommendations)} matching jobs',
            'analysis_id': analysis_id
        })
        
    except Exception as e:
        logger.error(f"Recommendations error: {str(e)}")
        return jsonify({'error': f'Recommendations failed: {str(e)}'}), 500

@app.route('/realtime-jobs', methods=['POST'])
def get_realtime_jobs():
    """Get real-time job data"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', 'software developer')
        location = data.get('location', '')
        limit = data.get('limit', 50)
        
        # Return mock realtime jobs
        jobs = generate_mock_job_matches()[:limit]
        
        return jsonify({
            'jobs': jobs,
            'total_found': len(jobs),
            'keywords': keywords,
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'source': 'mock_api'
        })
        
    except Exception as e:
        logger.error(f"Realtime jobs error: {str(e)}")
        return jsonify({'error': 'Failed to get realtime jobs'}), 500

@app.route('/apply-to-job', methods=['POST'])
def apply_to_job():
    """Apply to a job"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        analysis_id = data.get('analysis_id')
        
        if not job_id or not analysis_id:
            return jsonify({'error': 'job_id and analysis_id required'}), 400
        
        # Mock application submission
        application_id = str(uuid.uuid4())
        
        return jsonify({
            'application_id': application_id,
            'status': 'submitted',
            'job_id': job_id,
            'message': 'Application submitted successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Apply to job error: {str(e)}")
        return jsonify({'error': 'Failed to apply to job'}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate a cover letter"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        job_title = data.get('job_title')
        company = data.get('company')
        job_description = data.get('job_description', '')
        
        if not analysis_id or not job_title or not company:
            return jsonify({'error': 'analysis_id, job_title, and company required'}), 400
        
        # Get analysis from cache
        analysis = analysis_cache.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Generate mock cover letter
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With my background in software development and the skills identified in my resume analysis, I believe I would be a valuable addition to your team.

Based on my experience with Python, JavaScript, and other technologies, I am confident I can contribute effectively to your projects. My passion for technology and continuous learning aligns well with {company}'s innovative approach.

Thank you for considering my application. I look forward to the opportunity to discuss how my skills and enthusiasm can benefit {company}.

Best regards,
[Your Name]"""
        
        return jsonify({
            'cover_letter': cover_letter,
            'job_title': job_title,
            'company': company,
            'analysis_id': analysis_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Cover letter generation error: {str(e)}")
        return jsonify({'error': 'Failed to generate cover letter'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ================================
# Application Startup
# ================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Lightweight AI Job Matcher API on port {port}")
    print(f"Debug mode: {debug}")
    print(f"AI Features Available: {AI_FEATURES_AVAILABLE}")
    print(f"Mode: {'Full AI' if AI_FEATURES_AVAILABLE else 'Lightweight/Mock'}")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Application error: {e}")
