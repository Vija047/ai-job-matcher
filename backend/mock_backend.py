"""
Mock Backend for AI Job Matcher - Testing Purposes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from datetime import datetime
import random

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'], 
     allow_headers=['Content-Type', 'Authorization'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Mock data storage
mock_analyses = {}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': 'mock-1.0.0',
        'message': 'Mock backend is running'
    })

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Mock resume upload with realistic response"""
    try:
        # Generate mock analysis
        analysis_id = str(uuid.uuid4())
        mock_analysis = {
            'analysis_id': analysis_id,
            'skills': ['Python', 'JavaScript', 'React', 'SQL', 'Machine Learning', 'AWS', 'Git'],
            'total_skills': 7,
            'suitable_role': 'Full Stack Developer',
            'experience_years': 3,
            'confidence_score': 85,
            'timestamp': datetime.now().isoformat()
        }
        
        mock_analyses[analysis_id] = mock_analysis
        
        return jsonify({
            'success': True,
            'analysis_id': analysis_id,
            'data': mock_analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Mock job recommendations"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        limit = data.get('limit', 20)
        
        # Generate mock job recommendations
        mock_jobs = []
        for i in range(min(limit, 10)):
            job = {
                'id': f'job_{i+1}',
                'title': random.choice(['Senior Developer', 'Full Stack Engineer', 'Software Engineer', 'Backend Developer', 'Frontend Developer']),
                'company': random.choice(['TechCorp', 'InnovateLab', 'CodeCraft', 'DataFlow Inc', 'CloudTech']),
                'location': random.choice(['New York, NY', 'San Francisco, CA', 'Austin, TX', 'Seattle, WA', 'Remote']),
                'salary': f'${random.randint(80, 150)}k - ${random.randint(120, 200)}k',
                'description': 'Join our innovative team and work on cutting-edge technologies...',
                'requirements': 'Python, JavaScript, React, SQL, 3+ years experience',
                'compatibility_score': random.randint(70, 95),
                'posted_date': datetime.now().isoformat()
            }
            mock_jobs.append(job)
        
        return jsonify({
            'success': True,
            'recommendations': mock_jobs,
            'total_found': len(mock_jobs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/skill-gap-analysis', methods=['POST'])
def skill_gap_analysis():
    """Mock skill gap analysis"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        target_keywords = data.get('keywords', ['Docker', 'Kubernetes', 'TypeScript', 'GraphQL'])
        
        found_skills = ['Python', 'JavaScript', 'React']
        missing_skills = ['Docker', 'Kubernetes', 'TypeScript']
        gap_percentage = 60
        
        return jsonify({
            'success': True,
            'skill_gap_analysis': {
                'found_skills': found_skills,
                'missing_skills': missing_skills,
                'gap_percentage': gap_percentage,
                'total_analyzed': len(target_keywords),
                'recommendations': [f'Consider learning {skill}' for skill in missing_skills[:3]]
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/career-guidance', methods=['POST'])
def career_guidance():
    """Mock career guidance"""
    try:
        return jsonify({
            'success': True,
            'career_guidance': {
                'current_strengths': ['Python', 'React', 'SQL', 'JavaScript', 'Git'],
                'recommended_role': 'Full Stack Developer',
                'career_paths': ['Senior Full Stack Developer', 'Tech Lead', 'Engineering Manager'],
                'skill_development': ['Master Docker & Kubernetes', 'Learn TypeScript', 'Develop leadership skills'],
                'next_steps': ['Update resume with new skills', 'Apply to relevant positions', 'Network with professionals']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/application-history', methods=['GET'])
def application_history():
    """Mock application history"""
    try:
        return jsonify({
            'success': True,
            'application_history': {
                'total_applications': 5,
                'recent_applications': [
                    {'company': 'TechCorp', 'position': 'Full Stack Developer', 'status': 'Applied', 'date': '2025-08-15'},
                    {'company': 'InnovateLab', 'position': 'Backend Engineer', 'status': 'Interview', 'date': '2025-08-14'}
                ],
                'success_rate': 20,
                'popular_roles': ['Full Stack Developer', 'Software Engineer'],
                'statistics': {
                    'this_month': 3,
                    'last_month': 2,
                    'total_analyses': len(mock_analyses)
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/realtime-jobs', methods=['POST'])
def realtime_jobs():
    """Mock real-time jobs"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', '')
        limit = data.get('limit', 50)
        
        mock_jobs = []
        for i in range(min(limit, 15)):
            job = {
                'id': f'realtime_job_{i+1}',
                'title': f'{keywords} Engineer' if keywords else 'Software Engineer',
                'company': random.choice(['Amazon', 'Google', 'Microsoft', 'Meta', 'Apple']),
                'location': random.choice(['Seattle, WA', 'Mountain View, CA', 'Redmond, WA', 'Menlo Park, CA', 'Cupertino, CA']),
                'salary': f'${random.randint(120, 200)}k',
                'posted_date': datetime.now().isoformat(),
                'source': 'LinkedIn'
            }
            mock_jobs.append(job)
        
        return jsonify({
            'success': True,
            'jobs': mock_jobs,
            'total_found': len(mock_jobs)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/apply-to-job', methods=['POST'])
def apply_to_job():
    """Mock job application"""
    try:
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully',
            'application_id': str(uuid.uuid4())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Mock cover letter generation"""
    try:
        data = request.get_json()
        job_title = data.get('job_title', 'Software Engineer')
        company = data.get('company', 'Tech Company')
        
        cover_letter = f"""Dear Hiring Manager,

I am excited to apply for the {job_title} position at {company}. With my strong background in software development and proven track record of delivering high-quality solutions, I am confident I would be a valuable addition to your team.

My technical skills include Python, JavaScript, React, and SQL, which align well with your requirements. I have 3+ years of experience in full-stack development and am passionate about creating innovative solutions.

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to {company}'s continued success.

Best regards,
[Your Name]"""
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get stored analysis"""
    try:
        if analysis_id in mock_analyses:
            return jsonify({
                'success': True,
                'analysis': mock_analyses[analysis_id]
            })
        else:
            return jsonify({'error': 'Analysis not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export-analysis/<analysis_id>', methods=['GET'])
def export_analysis(analysis_id):
    """Export analysis"""
    try:
        if analysis_id in mock_analyses:
            return jsonify({
                'success': True,
                'export_data': mock_analyses[analysis_id],
                'exported_at': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Analysis not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Mock AI Job Matcher Backend...")
    print("📍 Health check: http://localhost:5555/health")
    print("🔧 Mock data will be generated for all endpoints")
    print("=" * 50)
    
    try:
        app.run(host='127.0.0.1', port=5555, debug=False)
    except Exception as e:
        print(f"Failed to start server: {e}")
