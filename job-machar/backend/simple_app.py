"""
Simplified AI Job Matcher Backend for testing
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - allow all origins for development
CORS(app, origins=['http://localhost:3000', 'http://localhost:3001'])

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume upload and return mock analysis"""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Generate mock analysis ID
    analysis_id = str(uuid.uuid4())
    
    # Return mock analysis data matching frontend expectations
    return jsonify({
        'analysis_id': analysis_id,
        'filename': file.filename,
        'resume_summary': {
            'total_skills': 8,
            'experience_level': 'mid-level',
            'years_experience': 3,
            'contact_info': {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1-234-567-8900',
                'linkedin': 'linkedin.com/in/johndoe'
            }
        },
        'top_matches': [
            {
                'job_title': 'Senior Python Developer',
                'company': 'TechCorp Inc.',
                'overall_score': 85,
                'recommendation': 'Excellent Match',
                'salary_range': '$80,000 - $120,000'
            },
            {
                'job_title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'overall_score': 78,
                'recommendation': 'Good Match',
                'salary_range': '$70,000 - $100,000'
            }
        ]
    })

@app.route('/analysis/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get analysis results for a given analysis ID"""
    return jsonify({
        'analysis_id': analysis_id,
        'filename': 'resume.pdf',
        'timestamp': datetime.now().isoformat(),
        'resume_analysis': {
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
            'experience': {
                'years_of_experience': 3,
                'primary_level': 'mid-level',
                'positions': [
                    {
                        'title': 'Software Developer',
                        'company': 'Tech Solutions Inc.',
                        'duration': '2022 - Present',
                        'description': 'Developed web applications using React and Node.js'
                    },
                    {
                        'title': 'Junior Developer',
                        'company': 'StartupXYZ',
                        'duration': '2021 - 2022',
                        'description': 'Built REST APIs and database schemas'
                    }
                ]
            },
            'total_skills': 12
        },
        'recommendations': [
            {
                'job_id': '1',
                'job_title': 'Senior Python Developer',
                'company': 'TechCorp Inc.',
                'salary_range': '$80,000 - $120,000',
                'overall_score': 85,
                'recommendation': 'Excellent Match',
                'skill_match_score': 88,
                'experience_match_score': 82,
                'semantic_similarity': 0.89,
                'matched_skills': ['Python', 'JavaScript', 'SQL', 'Git'],
                'missing_skills': ['Django', 'Microservices'],
                'score_breakdown': {
                    'skills': 88,
                    'experience': 82,
                    'education': 90
                }
            },
            {
                'job_id': '2',
                'job_title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'salary_range': '$70,000 - $100,000',
                'overall_score': 78,
                'recommendation': 'Good Match',
                'skill_match_score': 80,
                'experience_match_score': 76,
                'semantic_similarity': 0.82,
                'matched_skills': ['JavaScript', 'React', 'Node.js', 'SQL'],
                'missing_skills': ['Redux', 'TypeScript'],
                'score_breakdown': {
                    'skills': 80,
                    'experience': 76,
                    'education': 85
                }
            }
        ]
    })

@app.route('/skills-gap/<analysis_id>', methods=['GET'])
def get_skills_gap(analysis_id):
    """Get skills gap analysis"""
    return jsonify({
        'analysis_id': analysis_id,
        'top_missing_skills': [
            {
                'skill': 'AWS',
                'frequency': 8,
                'percentage': 80.0
            },
            {
                'skill': 'Docker',
                'frequency': 7,
                'percentage': 70.0
            },
            {
                'skill': 'Kubernetes',
                'frequency': 6,
                'percentage': 60.0
            },
            {
                'skill': 'CI/CD',
                'frequency': 5,
                'percentage': 50.0
            },
            {
                'skill': 'Microservices',
                'frequency': 4,
                'percentage': 40.0
            }
        ],
        'match_distribution': {
            'excellent': 2,
            'good': 3,
            'fair': 3,
            'poor': 2
        },
        'total_jobs_analyzed': 10
    })

@app.route('/improvement-plan/<analysis_id>', methods=['GET'])
def get_improvement_plan(analysis_id):
    """Get personalized improvement plan"""
    return jsonify({
        'analysis_id': analysis_id,
        'contact_suggestions': [
            'Add GitHub profile URL (recommended for tech roles)',
            'Consider adding a portfolio website'
        ],
        'skill_suggestions': [
            'Consider adding more skills (currently 12, recommended: 15+)',
            'Focus on cloud technologies and DevOps skills'
        ],
        'experience_suggestions': [
            'Highlight quantifiable achievements in current role',
            'Consider contributing to open source projects'
        ],
        'top_skills_to_learn': [
            {
                'skill': 'AWS',
                'demand_frequency': 8,
                'percentage': 80.0
            },
            {
                'skill': 'Docker',
                'demand_frequency': 7,
                'percentage': 70.0
            },
            {
                'skill': 'Kubernetes',
                'demand_frequency': 6,
                'percentage': 60.0
            },
            {
                'skill': 'CI/CD',
                'demand_frequency': 5,
                'percentage': 50.0
            },
            {
                'skill': 'Microservices',
                'demand_frequency': 4,
                'percentage': 40.0
            }
        ],
        'general_tips': [
            'Use action verbs to describe achievements',
            'Quantify accomplishments with numbers',
            'Tailor resume for each job application',
            'Keep it concise (1-2 pages)',
            'Use a professional format and font'
        ]
    })

@app.route('/jobs', methods=['GET'])
def get_jobs():
    """Get available jobs"""
    return jsonify({
        'jobs': [
            {
                'id': '1',
                'title': 'Senior Python Developer',
                'company': 'TechCorp Inc.',
                'experience_level': 'Senior',
                'salary_range': '$80,000 - $120,000',
                'required_skills': ['Python', 'Django', 'AWS', 'Docker', 'PostgreSQL'],
                'description': 'We are looking for an experienced Python developer to join our team. You will be responsible for developing scalable web applications and working with cloud technologies...'
            },
            {
                'id': '2',
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'experience_level': 'Mid-level',
                'salary_range': '$70,000 - $100,000',
                'required_skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Redux'],
                'description': 'Join our dynamic startup as a Full Stack Developer. You will work on exciting projects using modern web technologies and contribute to product development...'
            },
            {
                'id': '3',
                'title': 'DevOps Engineer',
                'company': 'CloudTech Solutions',
                'experience_level': 'Senior',
                'salary_range': '$90,000 - $130,000',
                'required_skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform'],
                'description': 'We need a skilled DevOps Engineer to manage our cloud infrastructure and implement automated deployment pipelines. Experience with AWS and container orchestration is required...'
            },
            {
                'id': '4',
                'title': 'Frontend Developer',
                'company': 'Design Studio Inc.',
                'experience_level': 'Mid-level',
                'salary_range': '$65,000 - $90,000',
                'required_skills': ['JavaScript', 'React', 'CSS', 'HTML', 'TypeScript'],
                'description': 'Create beautiful and responsive user interfaces for our web applications. You will collaborate with designers and backend developers to deliver exceptional user experiences...'
            },
            {
                'id': '5',
                'title': 'Backend Developer',
                'company': 'Data Corp',
                'experience_level': 'Mid-level',
                'salary_range': '$75,000 - $105,000',
                'required_skills': ['Java', 'Spring Boot', 'MySQL', 'REST APIs', 'Microservices'],
                'description': 'Develop robust backend services and APIs for our data processing platform. You will work with large datasets and implement scalable solutions...'
            }
        ]
    })

@app.route('/jobs/<job_id>/match/<analysis_id>', methods=['GET'])
def get_job_match(job_id, analysis_id):
    """Get job match details"""
    
    # Mock job data based on job_id
    jobs_data = {
        '1': {
            'title': 'Senior Python Developer',
            'company': 'TechCorp Inc.',
            'description': 'We are looking for an experienced Python developer to join our team. You will be responsible for developing scalable web applications and working with cloud technologies.',
            'required_skills': ['Python', 'Django', 'AWS', 'Docker', 'PostgreSQL'],
            'experience_level': 'Senior',
            'salary_range': '$80,000 - $120,000'
        },
        '2': {
            'title': 'Full Stack Developer',
            'company': 'StartupXYZ',
            'description': 'Join our dynamic startup as a Full Stack Developer. You will work on exciting projects using modern web technologies.',
            'required_skills': ['JavaScript', 'React', 'Node.js', 'MongoDB', 'Redux'],
            'experience_level': 'Mid-level',
            'salary_range': '$70,000 - $100,000'
        }
    }
    
    job_data = jobs_data.get(job_id, jobs_data['1'])  # Default to first job if not found
    
    return jsonify({
        'job': {
            'id': job_id,
            'title': job_data['title'],
            'company': job_data['company'],
            'description': job_data['description'],
            'required_skills': job_data['required_skills'],
            'experience_level': job_data['experience_level'],
            'salary_range': job_data['salary_range']
        },
        'match_result': {
            'overall_score': 85,
            'recommendation': 'Excellent Match',
            'skill_match_score': 88,
            'experience_match_score': 82,
            'semantic_similarity': 0.89,
            'matched_skills': ['Python', 'JavaScript', 'SQL', 'Git'],
            'missing_skills': ['Django', 'AWS'],
            'score_breakdown': {
                'skills': 88,
                'experience': 82,
                'education': 90
            }
        }
    })

@app.route('/get-recommendations', methods=['POST'])
def get_enhanced_recommendations():
    """Get enhanced job recommendations"""
    data = request.get_json()
    analysis_id = data.get('analysis_id', 'default')
    
    return jsonify({
        'recommendations': [
            {
                'id': '1',
                'title': 'Senior Python Developer',
                'company': 'TechCorp Inc.',
                'match_score': 85,
                'salary_range': '$80,000 - $120,000',
                'required_skills': ['Python', 'Django', 'AWS'],
                'location': 'Remote'
            },
            {
                'id': '2', 
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'match_score': 78,
                'salary_range': '$70,000 - $100,000',
                'required_skills': ['JavaScript', 'React', 'Node.js'],
                'location': 'New York'
            }
        ],
        'total_found': 25,
        'analysis_id': analysis_id
    })

@app.route('/realtime-jobs', methods=['POST'])
def get_realtime_jobs():
    """Get real-time job data"""
    data = request.get_json()
    keywords = data.get('keywords', 'developer')
    
    return jsonify({
        'jobs': [
            {
                'id': '1',
                'title': f'{keywords} Position',
                'company': 'TechCorp',
                'salary_range': '$70,000 - $100,000',
                'location': 'Remote',
                'posted_date': '2025-08-15'
            }
        ],
        'total': 1,
        'keywords': keywords
    })

@app.route('/apply-to-job', methods=['POST'])
def apply_to_job():
    """Job application assistance"""
    data = request.get_json()
    
    return jsonify({
        'status': 'success',
        'message': 'Application submitted successfully',
        'job_id': data.get('job_id'),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate personalized cover letter"""
    data = request.get_json()
    job_title = data.get('job_title', 'Developer')
    company = data.get('company', 'Company')
    
    cover_letter = f"""Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. 
With my background in software development and proven track record of delivering 
high-quality solutions, I am confident I would be a valuable addition to your team.

Thank you for your consideration.

Best regards,
[Your Name]"""

    return jsonify({
        'cover_letter': cover_letter,
        'job_title': job_title,
        'company': company
    })

@app.route('/application-history', methods=['GET'])
def get_application_history():
    """Get application history and statistics"""
    return jsonify({
        'applications': [
            {
                'id': str(uuid.uuid4()),
                'job_title': 'Software Engineer',
                'company': 'Tech Corp',
                'status': 'pending',
                'applied_date': '2025-08-10',
                'match_score': 85
            }
        ],
        'statistics': {
            'total_applications': 1,
            'pending': 1,
            'interviews': 0,
            'average_match_score': 85
        }
    })

@app.route('/skill-gap-analysis', methods=['POST'])
def get_skill_gap_analysis():
    """Perform skill gap analysis"""
    data = request.get_json()
    analysis_id = data.get('analysis_id', 'default')
    
    return jsonify({
        'skill_gaps': [
            {
                'skill': 'AWS',
                'importance': 'high',
                'market_demand': 85,
                'learning_resources': ['AWS Documentation', 'Cloud Guru']
            },
            {
                'skill': 'Docker',
                'importance': 'medium',
                'market_demand': 70,
                'learning_resources': ['Docker Documentation', 'Udemy']
            }
        ],
        'analysis_id': analysis_id
    })

@app.route('/career-guidance', methods=['POST'])
def get_career_guidance():
    """Get AI-powered career guidance"""
    data = request.get_json()
    analysis_id = data.get('analysis_id', 'default')
    
    return jsonify({
        'guidance': {
            'career_paths': ['Senior Developer', 'Tech Lead', 'Architect'],
            'skill_development': ['Learn cloud technologies', 'Develop leadership skills'],
            'next_steps': ['Build portfolio', 'Get certifications'],
            'market_trends': ['High demand for full-stack', 'Remote work increasing']
        },
        'analysis_id': analysis_id
    })

@app.route('/export-analysis/<analysis_id>', methods=['GET'])
def export_analysis(analysis_id):
    """Export analysis results"""
    return jsonify({
        'analysis': {
            'id': analysis_id,
            'skills': ['Python', 'JavaScript', 'SQL'],
            'experience_years': 5,
            'education': 'Bachelor\'s in Computer Science'
        },
        'exported_at': datetime.now().isoformat(),
        'export_id': str(uuid.uuid4())
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
