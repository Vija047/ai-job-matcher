"""
Test Role-Based Job Recommendations
Test the enhanced role analysis and job recommendation system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from role_based_recommender import RoleBasedRecommender
import json

def test_role_based_recommendations():
    """Test the role-based recommendation system"""
    
    print("🧪 Testing Role-Based Job Recommendation System")
    print("=" * 60)
    
    # Initialize recommender
    recommender = RoleBasedRecommender()
    
    # Mock resume analysis data
    mock_resume_analysis = {
        'skills_analysis': {
            'all_skills': ['Python', 'React', 'JavaScript', 'SQL', 'Git', 'Docker', 'AWS', 'Node.js']
        },
        'experience_analysis': {
            'experience_level': 'mid',
            'total_years': 3
        },
        'role_suggestion': {
            'primary_role': 'Full Stack Developer',
            'alternative_roles': ['Software Engineer', 'Frontend Developer', 'Backend Developer']
        }
    }
    
    # Test 1: Role Compatibility Analysis
    print("\n1. 🎯 Testing Role Compatibility Analysis")
    print("-" * 40)
    
    role_analysis = recommender.analyze_role_compatibility(mock_resume_analysis)
    
    print(f"Primary Role: {role_analysis['primary_role']}")
    print(f"Career Stage: {role_analysis['career_stage']}")
    print(f"Experience Level: {role_analysis['experience_level']}")
    print(f"Years Experience: {role_analysis['years_experience']}")
    print(f"Suitable for Internships: {role_analysis['suitable_for_internships']}")
    print(f"Skill Match Strength: {role_analysis['skill_match_strength']}")
    print(f"Alternative Roles: {role_analysis['alternative_roles']}")
    
    # Mock job data
    mock_jobs = [
        {
            'id': 'job-1',
            'title': 'Senior Full Stack Developer',
            'company': 'TechCorp',
            'location': 'San Francisco, CA',
            'description': 'Looking for an experienced full stack developer with React and Node.js experience.',
            'requirements': 'React, Node.js, Python, JavaScript, SQL',
            'skills': ['React', 'Node.js', 'Python', 'JavaScript', 'SQL'],
            'salary_min': 120000,
            'salary_max': 180000,
            'salary_currency': '$',
            'experience_level': 'Senior',
            'employment_type': 'Full Time',
            'apply_url': 'https://example.com/apply/1',
            'remote_allowed': True
        },
        {
            'id': 'job-2',
            'title': 'Frontend Developer Intern',
            'company': 'StartupXYZ',
            'location': 'New York, NY',
            'description': 'Internship opportunity for frontend development with React.',
            'requirements': 'React, JavaScript, HTML, CSS',
            'skills': ['React', 'JavaScript', 'HTML', 'CSS'],
            'salary_min': 25,
            'salary_max': 35,
            'salary_currency': '$',
            'experience_level': 'Entry',
            'employment_type': 'Internship',
            'apply_url': 'https://example.com/apply/2',
            'remote_allowed': False
        },
        {
            'id': 'job-3',
            'title': 'Cloud Solutions Architect',
            'company': 'CloudTech',
            'location': 'Austin, TX',
            'description': 'Design cloud infrastructure with AWS and Docker.',
            'requirements': 'AWS, Docker, Python, Kubernetes',
            'skills': ['AWS', 'Docker', 'Python', 'Kubernetes'],
            'salary_min': 140000,
            'salary_max': 200000,
            'salary_currency': '$',
            'experience_level': 'Senior',
            'employment_type': 'Full Time',
            'apply_url': 'https://example.com/apply/3',
            'remote_allowed': True
        },
        {
            'id': 'intern-1',
            'title': 'Software Engineering Intern',
            'company': 'BigTech Inc',
            'location': 'Seattle, WA',
            'description': 'Summer internship program for computer science students.',
            'requirements': 'Python, Java, or JavaScript experience',
            'skills': ['Python', 'Java', 'JavaScript'],
            'salary_min': 30,
            'salary_max': 40,
            'salary_currency': '$',
            'experience_level': 'Entry',
            'employment_type': 'Internship',
            'apply_url': 'https://example.com/apply/intern1',
            'remote_allowed': False
        }
    ]
    
    # Test 2: Job Recommendations
    print("\n2. 💼 Testing Job Recommendations")
    print("-" * 40)
    
    preferences = {
        'location': '',
        'salary_min': 50000,
        'job_type': 'Full Time',
        'remote_preference': False,
        'limit': 10
    }
    
    recommendations = recommender.get_role_based_recommendations(
        role_analysis, mock_jobs, preferences
    )
    
    if recommendations['success']:
        print(f"✅ Recommendations generated successfully!")
        print(f"📊 Total Jobs Found: {recommendations['total_jobs_found']}")
        print(f"🎓 Total Internships Found: {recommendations['total_internships_found']}")
        
        # Display job recommendations
        if recommendations['jobs']:
            print(f"\n📋 Job Recommendations:")
            for i, job in enumerate(recommendations['jobs'][:3], 1):
                print(f"  {i}. {job['title']} at {job['company']}")
                print(f"     Match Score: {job['compatibility_score']:.2%}")
                print(f"     Match Type: {job['match_type']}")
                print(f"     Matched Role: {job['matched_role']}")
                
        # Display internship recommendations
        if recommendations['internships']:
            print(f"\n🎓 Internship Recommendations:")
            for i, internship in enumerate(recommendations['internships'], 1):
                print(f"  {i}. {internship['title']} at {internship['company']}")
                print(f"     Match Score: {internship['compatibility_score']:.2%}")
                print(f"     Matched Role: {internship['matched_role']}")
        
        # Display categories
        if recommendations['categories']:
            print(f"\n📈 Match Categories:")
            print(f"  Primary Role Matches: {recommendations['categories']['primary_role_matches']}")
            print(f"  Alternative Role Matches: {recommendations['categories']['alternative_role_matches']}")
            print(f"  Skill-based Matches: {recommendations['categories']['skill_based_matches']}")
            
    else:
        print(f"❌ Recommendation failed: {recommendations.get('error', 'Unknown error')}")
    
    # Test 3: Different Career Stages
    print("\n3. 👥 Testing Different Career Stages")
    print("-" * 40)
    
    career_stages = [
        {
            'name': 'Entry Level',
            'analysis': {
                'skills_analysis': {'all_skills': ['Python', 'JavaScript', 'HTML', 'CSS']},
                'experience_analysis': {'experience_level': 'entry', 'total_years': 0},
                'role_suggestion': {'primary_role': 'Junior Developer', 'alternative_roles': ['Frontend Developer']}
            }
        },
        {
            'name': 'Senior Level',
            'analysis': {
                'skills_analysis': {'all_skills': ['Python', 'React', 'AWS', 'Docker', 'Kubernetes', 'Leadership']},
                'experience_analysis': {'experience_level': 'senior', 'total_years': 8},
                'role_suggestion': {'primary_role': 'Senior Software Engineer', 'alternative_roles': ['Technical Lead', 'Cloud Architect']}
            }
        }
    ]
    
    for stage in career_stages:
        print(f"\n{stage['name']}:")
        stage_analysis = recommender.analyze_role_compatibility(stage['analysis'])
        print(f"  Primary Role: {stage_analysis['primary_role']}")
        print(f"  Career Stage: {stage_analysis['career_stage']}")
        print(f"  Suitable for Internships: {stage_analysis['suitable_for_internships']}")
        print(f"  Growth Potential: {stage_analysis['growth_potential']}")
    
    print("\n✅ Role-Based Recommendation System Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_role_based_recommendations()
