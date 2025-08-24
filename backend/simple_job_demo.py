"""
Simple Job Recommendation and Application Demo
Demonstrates core functionality without external dependencies
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from urllib.parse import quote

class SimpleJobRecommender:
    """Simple job recommender for demonstration"""
    
    def __init__(self):
        self.role_patterns = {
            'Machine Learning Engineer': ['python', 'machine learning', 'tensorflow', 'aws', 'deep learning'],
            'Data Scientist': ['python', 'sql', 'pandas', 'statistics', 'machine learning'],
            'Full Stack Developer': ['react', 'node.js', 'python', 'javascript', 'sql'],
            'Software Engineer': ['python', 'javascript', 'java', 'react', 'git'],
            'Frontend Developer': ['react', 'javascript', 'html', 'css', 'typescript'],
            'Backend Developer': ['python', 'java', 'node.js', 'sql', 'api'],
            'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'jenkins', 'terraform']
        }
        
        self.sample_jobs = [
            {
                'id': 'job_1',
                'title': 'Senior Machine Learning Engineer',
                'company': 'TechCorp AI',
                'location': 'San Francisco, CA (Remote)',
                'description': 'Join our AI team to build cutting-edge ML models. Work with Python, TensorFlow, and AWS.',
                'skills': ['Python', 'Machine Learning', 'TensorFlow', 'AWS', 'Deep Learning'],
                'salary_min': 150000,
                'salary_max': 220000,
                'experience_level': 'senior',
                'employment_type': 'Full Time',
                'remote_allowed': True,
                'apply_url': 'https://techcorp.com/careers/ml-engineer'
            },
            {
                'id': 'job_2',
                'title': 'Full Stack Developer',
                'company': 'StartupXYZ',
                'location': 'Remote',
                'description': 'Build web applications using React and Node.js. Join a fast-growing startup!',
                'skills': ['React', 'Node.js', 'JavaScript', 'MongoDB', 'HTML', 'CSS'],
                'salary_min': 80000,
                'salary_max': 120000,
                'experience_level': 'mid',
                'employment_type': 'Full Time',
                'remote_allowed': True,
                'apply_url': 'https://startupxyz.com/careers'
            },
            {
                'id': 'job_3',
                'title': 'Data Scientist',
                'company': 'DataCorp Analytics',
                'location': 'Austin, TX',
                'description': 'Analyze large datasets and build predictive models.',
                'skills': ['Python', 'SQL', 'Pandas', 'Scikit-learn', 'Tableau'],
                'salary_min': 95000,
                'salary_max': 140000,
                'experience_level': 'mid',
                'employment_type': 'Full Time',
                'remote_allowed': True,
                'apply_url': 'https://datacorp.com/jobs'
            },
            {
                'id': 'intern_1',
                'title': 'Software Engineering Intern',
                'company': 'BigTech Corp',
                'location': 'Mountain View, CA',
                'description': 'Summer internship program for CS students.',
                'skills': ['Python', 'Java', 'Algorithms', 'Data Structures'],
                'salary_min': 7000,
                'salary_max': 8500,
                'experience_level': 'entry',
                'employment_type': 'Internship',
                'remote_allowed': False,
                'apply_url': 'https://bigtech.com/internships'
            },
            {
                'id': 'intern_2',
                'title': 'Data Analysis Intern',
                'company': 'Research Institute',
                'location': 'Boston, MA (Remote)',
                'description': 'Part-time internship analyzing research data.',
                'skills': ['Excel', 'Python', 'Statistics', 'Data Visualization'],
                'salary_min': 15,
                'salary_max': 20,
                'experience_level': 'entry',
                'employment_type': 'Internship',
                'remote_allowed': True,
                'apply_url': 'https://research-institute.edu/jobs'
            }
        ]
        
        self.saved_jobs = {}
        self.applications = {}
    
    def analyze_user_profile(self, user_skills: List[str], experience_level: str = 'mid') -> Dict:
        """Analyze user profile and determine best role matches"""
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        role_scores = {}
        for role, keywords in self.role_patterns.items():
            score = 0
            for keyword in keywords:
                if any(keyword in skill for skill in user_skills_lower):
                    score += 1
            role_scores[role] = score / len(keywords)
        
        # Sort roles by score
        sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
        
        primary_role = sorted_roles[0][0] if sorted_roles else 'Software Engineer'
        alternative_roles = [role for role, score in sorted_roles[1:4]]
        
        # Determine if suitable for internships
        suitable_for_internships = experience_level in ['entry', 'student'] or any('intern' in skill.lower() for skill in user_skills)
        
        return {
            'primary_role': primary_role,
            'alternative_roles': alternative_roles,
            'experience_level': experience_level,
            'suitable_for_internships': suitable_for_internships,
            'role_scores': dict(sorted_roles),
            'skill_count': len(user_skills)
        }
    
    def get_job_recommendations(self, user_profile: Dict, preferences: Dict = None) -> Dict:
        """Get personalized job recommendations"""
        preferences = preferences or {}
        
        jobs = []
        internships = []
        
        for job in self.sample_jobs:
            # Calculate compatibility score
            score = self._calculate_compatibility(job, user_profile)
            
            if score > 0.2:  # Minimum threshold
                enhanced_job = job.copy()
                enhanced_job['compatibility_score'] = score
                enhanced_job['match_reason'] = self._get_match_reason(job, user_profile, score)
                enhanced_job['apply_options'] = self._get_apply_options(job)
                enhanced_job['application_tips'] = self._get_application_tips(job, user_profile)
                
                if job['employment_type'] == 'Internship':
                    if user_profile['suitable_for_internships']:
                        internships.append(enhanced_job)
                else:
                    jobs.append(enhanced_job)
        
        # Sort by compatibility score
        jobs.sort(key=lambda x: x['compatibility_score'], reverse=True)
        internships.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return {
            'success': True,
            'user_profile': user_profile,
            'jobs': jobs,
            'internships': internships,
            'total_jobs': len(jobs),
            'total_internships': len(internships),
            'search_metadata': {
                'timestamp': datetime.now().isoformat(),
                'primary_role': user_profile['primary_role'],
                'search_quality': 'High' if jobs else 'Low'
            }
        }
    
    def save_job(self, job_id: str, folder: str = 'favorites') -> Dict:
        """Save a job for later application"""
        job = next((j for j in self.sample_jobs if j['id'] == job_id), None)
        if not job:
            return {'success': False, 'error': 'Job not found'}
        
        if folder not in self.saved_jobs:
            self.saved_jobs[folder] = []
        
        self.saved_jobs[folder].append({
            **job,
            'saved_date': datetime.now().isoformat(),
            'folder': folder
        })
        
        return {
            'success': True,
            'message': f"Job saved to {folder}",
            'total_saved': sum(len(jobs) for jobs in self.saved_jobs.values())
        }
    
    def apply_to_job(self, job_id: str, user_profile: Dict, application_type: str = 'standard') -> Dict:
        """Apply to a job"""
        job = next((j for j in self.sample_jobs if j['id'] == job_id), None)
        if not job:
            return {'success': False, 'error': 'Job not found'}
        
        app_id = f"app_{len(self.applications) + 1}"
        
        application = {
            'id': app_id,
            'job_id': job_id,
            'job_title': job['title'],
            'company': job['company'],
            'user_name': user_profile.get('name', 'User'),
            'application_type': application_type,
            'status': 'submitted',
            'applied_date': datetime.now().isoformat(),
            'cover_letter': self._generate_cover_letter(job, user_profile),
            'estimated_response_time': '1-2 weeks'
        }
        
        self.applications[app_id] = application
        
        return {
            'success': True,
            'application_id': app_id,
            'message': f"Successfully applied to {job['title']} at {job['company']}",
            'application_type': application_type,
            'next_steps': [
                'Application submitted successfully',
                'You will receive a confirmation email',
                'Follow up in 1 week if no response',
                'Continue applying to similar positions'
            ]
        }
    
    def get_application_dashboard(self) -> Dict:
        """Get application tracking dashboard"""
        if not self.applications:
            return {
                'success': True,
                'stats': {
                    'total_applications': 0,
                    'message': 'No applications yet. Start applying to jobs!'
                },
                'applications': []
            }
        
        return {
            'success': True,
            'stats': {
                'total_applications': len(self.applications),
                'this_week': len([app for app in self.applications.values() 
                                if datetime.fromisoformat(app['applied_date']) > datetime.now() - timedelta(days=7)]),
                'pending_responses': len(self.applications)
            },
            'applications': list(self.applications.values()),
            'insights': [
                f"You've applied to {len(self.applications)} positions",
                "Keep applying to increase your chances",
                "Follow up on applications after 1 week"
            ]
        }
    
    def _calculate_compatibility(self, job: Dict, user_profile: Dict) -> float:
        """Calculate job compatibility score"""
        job_skills = [skill.lower() for skill in job['skills']]
        
        # Check if job title matches user's primary role
        title_match = 0
        if user_profile['primary_role'].lower() in job['title'].lower():
            title_match = 0.4
        elif any(role.lower() in job['title'].lower() for role in user_profile['alternative_roles']):
            title_match = 0.2
        
        # Check skill overlap
        user_skills_in_job = [skill for skill in job_skills 
                             if any(skill in user_skill.lower() for user_skill in user_profile.get('user_skills', []))]
        skill_match = len(user_skills_in_job) / len(job_skills) if job_skills else 0
        
        # Experience level match
        exp_match = 0.3
        if user_profile['experience_level'] == job['experience_level']:
            exp_match = 0.5
        elif (user_profile['experience_level'] == 'entry' and job['experience_level'] == 'mid') or \
             (user_profile['experience_level'] == 'mid' and job['experience_level'] == 'senior'):
            exp_match = 0.3
        
        return min(title_match + skill_match * 0.4 + exp_match * 0.2, 1.0)
    
    def _get_match_reason(self, job: Dict, user_profile: Dict, score: float) -> str:
        """Get explanation for why this job matches"""
        if score >= 0.8:
            return f"Excellent match! Your {user_profile['primary_role']} background aligns perfectly."
        elif score >= 0.6:
            return f"Strong match based on your skills and experience level."
        elif score >= 0.4:
            return f"Good opportunity to apply your transferable skills."
        else:
            return f"Consider this role to expand your experience."
    
    def _get_apply_options(self, job: Dict) -> Dict:
        """Get application options for a job"""
        return {
            'quick_apply': {
                'available': True,
                'time_estimate': '2-3 minutes',
                'description': 'Apply with pre-filled information'
            },
            'detailed_apply': {
                'available': True,
                'time_estimate': '10-15 minutes',
                'description': 'Customize application with cover letter'
            },
            'company_website': {
                'url': job['apply_url'],
                'description': 'Apply directly on company website'
            },
            'save_for_later': {
                'available': True,
                'suggested_folders': ['High Priority', 'Research Later', 'Backup Options']
            }
        }
    
    def _get_application_tips(self, job: Dict, user_profile: Dict) -> List[str]:
        """Get personalized application tips"""
        tips = [
            f"Highlight your experience with {', '.join(job['skills'][:3])}",
            f"Research {job['company']} recent news and achievements",
            "Customize your cover letter for this specific role"
        ]
        
        if job['remote_allowed']:
            tips.append("Mention your remote work experience and self-management skills")
        
        if job['employment_type'] == 'Internship':
            tips.append("Emphasize your learning goals and enthusiasm")
        
        return tips
    
    def _generate_cover_letter(self, job: Dict, user_profile: Dict) -> str:
        """Generate a basic cover letter template"""
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job['title']} position at {job['company']}. With my background in {user_profile.get('primary_role', 'technology')} and relevant experience, I am excited about the opportunity to contribute to your team.

Your company's work in {job.get('industry', 'technology')} aligns perfectly with my career goals. I am particularly drawn to this role because of the opportunity to work with {', '.join(job['skills'][:3])}.

I believe my skills and enthusiasm make me a strong candidate for this position. I would welcome the opportunity to discuss how I can contribute to {job['company']}'s continued success.

Thank you for considering my application.

Best regards,
{user_profile.get('name', 'Your Name')}"""

def run_demo():
    """Run the job recommendation and application demo"""
    
    print("=" * 80)
    print("🚀 AI JOB MATCHER - COMPREHENSIVE DEMO")
    print("=" * 80)
    
    # Initialize recommender
    recommender = SimpleJobRecommender()
    
    # Sample user profile
    user_data = {
        'name': 'Alex Smith',
        'email': 'alex.smith@email.com',
        'skills': ['Python', 'Machine Learning', 'React', 'JavaScript', 'SQL', 'AWS'],
        'experience_level': 'mid'
    }
    
    print(f"\n👤 USER PROFILE:")
    print(f"   Name: {user_data['name']}")
    print(f"   Skills: {', '.join(user_data['skills'])}")
    print(f"   Experience: {user_data['experience_level']}")
    
    # Step 1: Analyze user profile
    print(f"\n🔍 STEP 1: ANALYZING YOUR PROFILE")
    print("-" * 50)
    
    user_profile = recommender.analyze_user_profile(user_data['skills'], user_data['experience_level'])
    user_profile['user_skills'] = user_data['skills']
    user_profile['name'] = user_data['name']
    
    print(f"✅ Primary Role Match: {user_profile['primary_role']}")
    print(f"📊 Alternative Roles: {', '.join(user_profile['alternative_roles'][:3])}")
    print(f"🎓 Suitable for Internships: {'Yes' if user_profile['suitable_for_internships'] else 'No'}")
    
    # Step 2: Get job recommendations
    print(f"\n📋 STEP 2: FINDING JOB MATCHES")
    print("-" * 50)
    
    recommendations = recommender.get_job_recommendations(user_profile)
    
    if recommendations['success']:
        print(f"✅ Found {recommendations['total_jobs']} job matches")
        print(f"✅ Found {recommendations['total_internships']} internship opportunities")
        
        print(f"\n🔥 TOP JOB RECOMMENDATIONS:")
        for i, job in enumerate(recommendations['jobs'][:3], 1):
            print(f"\n{i}. {job['title']} at {job['company']}")
            print(f"   📍 {job['location']}")
            print(f"   💰 ${job['salary_min']:,} - ${job['salary_max']:,}")
            print(f"   🎯 Match Score: {job['compatibility_score']:.0%}")
            print(f"   💡 Why it matches: {job['match_reason']}")
            print(f"   ⚡ Quick Apply: {job['apply_options']['quick_apply']['time_estimate']}")
        
        if recommendations['internships']:
            print(f"\n🎓 INTERNSHIP OPPORTUNITIES:")
            for i, internship in enumerate(recommendations['internships'], 1):
                print(f"\n{i}. {internship['title']} at {internship['company']}")
                print(f"   📍 {internship['location']}")
                print(f"   💰 ${internship['salary_min']}-${internship['salary_max']}/hour")
                print(f"   🎯 Match Score: {internship['compatibility_score']:.0%}")
    
    # Step 3: Save jobs
    print(f"\n💾 STEP 3: SAVING JOBS FOR LATER")
    print("-" * 50)
    
    if recommendations['jobs']:
        for i, job in enumerate(recommendations['jobs'][:2]):
            folder = 'High Priority' if i == 0 else 'Research Later'
            save_result = recommender.save_job(job['id'], folder)
            if save_result['success']:
                print(f"✅ Saved '{job['title']}' to {folder}")
    
    # Step 4: Apply to jobs
    print(f"\n📝 STEP 4: APPLYING TO JOBS")
    print("-" * 50)
    
    if recommendations['jobs']:
        # Apply to top job with detailed application
        top_job = recommendations['jobs'][0]
        apply_result = recommender.apply_to_job(top_job['id'], user_profile, 'detailed')
        if apply_result['success']:
            print(f"✅ {apply_result['message']}")
            print(f"📋 Application ID: {apply_result['application_id']}")
            print(f"📅 Expected response: {apply_result.get('estimated_response_time', 'Soon')}")
        
        # Quick apply to second job if available
        if len(recommendations['jobs']) > 1:
            second_job = recommendations['jobs'][1]
            quick_apply = recommender.apply_to_job(second_job['id'], user_profile, 'quick')
            if quick_apply['success']:
                print(f"⚡ Quick applied to '{second_job['title']}'")
    
    # Step 5: Application Dashboard
    print(f"\n📊 STEP 5: APPLICATION TRACKING")
    print("-" * 50)
    
    dashboard = recommender.get_application_dashboard()
    if dashboard['success']:
        stats = dashboard['stats']
        print(f"📈 Total Applications: {stats['total_applications']}")
        
        if stats['total_applications'] > 0:
            print(f"📅 Applied This Week: {stats.get('this_week', 0)}")
            print(f"⏳ Pending Responses: {stats.get('pending_responses', 0)}")
            
            print(f"\n📝 YOUR APPLICATIONS:")
            for app in dashboard['applications']:
                print(f"   • {app['job_title']} at {app['company']}")
                print(f"     Status: {app['status']} | Applied: {app['applied_date'][:10]}")
            
            if dashboard.get('insights'):
                print(f"\n💡 INSIGHTS:")
                for insight in dashboard['insights']:
                    print(f"   • {insight}")
    
    # Step 6: Application Tips
    print(f"\n🎯 STEP 6: APPLICATION SUCCESS TIPS")
    print("-" * 50)
    
    if recommendations['jobs']:
        top_job = recommendations['jobs'][0]
        tips = top_job['application_tips']
        print(f"For '{top_job['title']}' application:")
        for tip in tips:
            print(f"   💡 {tip}")
    
    print(f"\n" + "=" * 80)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    print(f"\n✨ FEATURES DEMONSTRATED:")
    print("   ✅ AI-powered job matching based on skills")
    print("   ✅ Personalized role recommendations")
    print("   ✅ Internship opportunities for career growth")
    print("   ✅ Save jobs for later application")
    print("   ✅ Quick and detailed apply options")
    print("   ✅ Application tracking dashboard")
    print("   ✅ Personalized application tips")
    print("   ✅ Compatibility scoring system")
    
    print(f"\n🚀 READY TO START YOUR JOB SEARCH!")
    print("   • Upload your resume to get personalized matches")
    print("   • Apply to jobs with one click")
    print("   • Track all your applications in one place")
    print("   • Get tips to improve your success rate")

if __name__ == "__main__":
    run_demo()
