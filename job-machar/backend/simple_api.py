"""
Simple API server for testing frontend functionality
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'], supports_credentials=True)

# Simple in-memory storage
analysis_cache = {}

def generate_mock_jobs():
    """Generate mock job data"""
    return [
        {
            'id': str(uuid.uuid4()),
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc',
            'location': 'Remote',
            'salary': '$90,000 - $120,000',
            'description': 'We are looking for a senior software engineer with Python and React experience.',
            'requirements': ['Python', 'React', 'JavaScript', 'SQL'],
            'posted_date': '2025-08-15',
            'employment_type': 'full-time'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Full Stack Developer',
            'company': 'Innovation Labs',
            'location': 'San Francisco, CA',
            'salary': '$85,000 - $110,000',
            'description': 'Join our team to build cutting-edge web applications.',
            'requirements': ['JavaScript', 'Node.js', 'React', 'MongoDB'],
            'posted_date': '2025-08-16',
            'employment_type': 'full-time'
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Python Developer',
            'company': 'DataFlow Systems',
            'location': 'New York, NY',
            'salary': '$75,000 - $95,000',
            'description': 'Work on data processing and analytics systems.',
            'requirements': ['Python', 'Django', 'PostgreSQL', 'Docker'],
            'posted_date': '2025-08-17',
            'employment_type': 'full-time'
        }
    ]

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and analyze resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Generate mock analysis
        analysis_id = str(uuid.uuid4())
        mock_analysis = {
            'skills': ['Python', 'JavaScript', 'React', 'SQL', 'Git'],
            'experience_analysis': {
                'experience_level': 'mid',
                'job_titles': ['Software Developer', 'Full Stack Developer'],
                'years_of_experience': 3
            },
            'skills_analysis': {
                'all_skills': ['Python', 'JavaScript', 'React', 'SQL', 'Git', 'HTML', 'CSS'],
                'technical_skills': ['Python', 'JavaScript', 'React', 'SQL'],
                'soft_skills': ['Communication', 'Problem Solving', 'Team Work']
            },
            'summary': 'Experienced software developer with strong technical skills'
        }
        
        # Store in cache
        analysis_cache[analysis_id] = mock_analysis
        
        return jsonify({
            'analysis_id': analysis_id,
            'analysis': mock_analysis,
            'message': 'Resume analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs"""
    jobs = generate_mock_jobs()
    return jsonify({'jobs': jobs})

@app.route('/job-match', methods=['POST'])
def job_match():
    """Get job match score"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        analysis_id = data.get('analysis_id')
        
        if not job_id or not analysis_id:
            return jsonify({'error': 'job_id and analysis_id required'}), 400
        
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify({
            'match_score': 0.85,
            'job_id': job_id,
            'analysis_id': analysis_id,
            'compatibility': 'High'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Get job recommendations"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id:
            return jsonify({'error': 'Analysis ID required'}), 400
        
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        jobs = generate_mock_jobs()
        # Add match scores
        for i, job in enumerate(jobs):
            job['match_score'] = 0.9 - (i * 0.1)
        
        return jsonify({
            'recommendations': jobs,
            'total_found': len(jobs),
            'analysis_id': analysis_id,
            'message': f'Found {len(jobs)} matching jobs'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/realtime-jobs', methods=['POST'])
def realtime_jobs():
    """Get realtime jobs"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', '')
        location = data.get('location', '')
        limit = data.get('limit', 50)
        
        jobs = generate_mock_jobs()
        return jsonify({
            'jobs': jobs[:limit],
            'total_found': len(jobs),
            'keywords': keywords,
            'location': location
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/apply-to-job', methods=['POST'])
def apply_to_job():
    """Apply to job"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        analysis_id = data.get('analysis_id')
        
        if not job_id or not analysis_id:
            return jsonify({'error': 'job_id and analysis_id required'}), 400
        
        return jsonify({
            'application_id': str(uuid.uuid4()),
            'status': 'submitted',
            'message': 'Application submitted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate cover letter"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        job_title = data.get('job_title', 'Software Developer')
        company = data.get('company', 'Company')
        
        if not analysis_id:
            return jsonify({'error': 'analysis_id required'}), 400
        
        cover_letter = f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. 
Based on my technical skills and experience, I believe I would be a great fit for this role.

Thank you for your consideration.

Best regards,
[Your Name]"""
        
        return jsonify({
            'cover_letter': cover_letter,
            'analysis_id': analysis_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get analysis by ID"""
    if analysis_id not in analysis_cache:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify({
        'analysis_id': analysis_id,
        'analysis': analysis_cache[analysis_id]
    })

@app.route('/skill-gap-analysis', methods=['POST'])
def skill_gap_analysis():
    """Get skill gap analysis"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id:
            return jsonify({'error': 'analysis_id required'}), 400
        
        if analysis_id not in analysis_cache:
            return jsonify({'error': 'Analysis not found'}), 404
        
        return jsonify({
            'skill_gaps': [
                {'skill': 'Docker', 'proficiency': 'Beginner', 'importance': 'High'},
                {'skill': 'Kubernetes', 'proficiency': 'None', 'importance': 'Medium'},
                {'skill': 'AWS', 'proficiency': 'Basic', 'importance': 'High'}
            ],
            'recommended_learning': [
                {'skill': 'Docker', 'resources': ['Docker Documentation', 'Docker Tutorials']},
                {'skill': 'AWS', 'resources': ['AWS Free Tier', 'AWS Certified Developer']}
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/career-guidance', methods=['POST'])
def career_guidance():
    """Get career guidance"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        
        if not analysis_id:
            return jsonify({'error': 'analysis_id required'}), 400
        
        return jsonify({
            'career_paths': [
                {
                    'title': 'Senior Software Engineer',
                    'growth_potential': 'High',
                    'required_skills': ['Python', 'System Design', 'Leadership'],
                    'estimated_timeline': '2-3 years'
                },
                {
                    'title': 'Technical Lead',
                    'growth_potential': 'High',
                    'required_skills': ['Architecture', 'Team Management', 'Strategic Planning'],
                    'estimated_timeline': '3-5 years'
                }
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/application-history', methods=['GET'])
def application_history():
    """Get application history"""
    try:
        return jsonify({
            'application_history': [
                {
                    'id': str(uuid.uuid4()),
                    'job_title': 'Software Engineer',
                    'company': 'TechCorp',
                    'status': 'Pending',
                    'applied_date': '2025-08-15',
                    'last_updated': '2025-08-16'
                }
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Simple AI Job Matcher API on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
