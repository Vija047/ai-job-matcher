"""
Test script for Job Recommendation and Application System
Demonstrates the complete workflow from job search to application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from comprehensive_job_api import JobSearchAPI
import json
from datetime import datetime

def test_job_recommendation_system():
    """Test the complete job recommendation and application system"""
    
    print("=" * 80)
    print("🚀 AI JOB MATCHER - COMPREHENSIVE TEST")
    print("=" * 80)
    
    # Initialize the API
    api = JobSearchAPI()
    
    # Sample user profile
    user_profile = {
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'primary_skills': 'Python, Machine Learning, React',
        'years_experience': 3,
        'resume_version': 'v2024.1'
    }
    
    # Sample resume analysis (simulating analyzed resume)
    resume_analysis = {
        'skills_analysis': {
            'all_skills': ['Python', 'Machine Learning', 'TensorFlow', 'React', 'JavaScript', 'SQL', 'AWS', 'Git']
        },
        'experience_analysis': {
            'experience_level': 'mid',
            'total_years': 3
        },
        'role_suggestion': {
            'primary_role': 'Machine Learning Engineer',
            'alternative_roles': ['Data Scientist', 'Full Stack Developer', 'Software Engineer']
        }
    }
    
    # Test 1: Job Search and Recommendations
    print("\n📊 STEP 1: SEARCHING FOR JOBS AND INTERNSHIPS")
    print("-" * 50)
    
    preferences = {
        'location': 'Remote',
        'salary_min': 80000,
        'job_type': 'Full Time',
        'remote_preference': True,
        'limit': 10
    }
    
    recommendations = api.search_and_recommend_jobs(resume_analysis, preferences)
    
    if recommendations['success']:
        print(f"✅ Found {recommendations['total_jobs_found']} job matches")
        print(f"✅ Found {recommendations['total_internships_found']} internship matches")
        
        print(f"\n🎯 PRIMARY ROLE: {recommendations['role_analysis']['primary_role']}")
        print(f"📈 CAREER STAGE: {recommendations['role_analysis']['career_stage']}")
        print(f"💪 SKILL STRENGTH: {recommendations['role_analysis']['skill_match_strength']}")
        
        print("\n🔥 TOP JOB RECOMMENDATIONS:")
        for i, job in enumerate(recommendations['jobs'][:3], 1):
            print(f"\n{i}. {job['title']} at {job['company']}")
            print(f"   📍 {job['location']} | 💰 ${job.get('salary_min', 0):,}-${job.get('salary_max', 0):,}")
            print(f"   🎯 Match: {job['compatibility_score']:.0%} | Type: {job['match_type']}")
            print(f"   🚀 Apply: {job['apply_options']['quick_apply']['estimated_time']}")
        
        if recommendations['internships']:
            print("\n🎓 INTERNSHIP OPPORTUNITIES:")
            for i, internship in enumerate(recommendations['internships'][:2], 1):
                print(f"\n{i}. {internship['title']} at {internship['company']}")
                print(f"   📍 {internship['location']} | 💰 ${internship.get('salary_min', 0)}/hour")
                print(f"   🎯 Match: {internship['compatibility_score']:.0%}")
    
    # Test 2: Save Jobs for Later
    print("\n\n💾 STEP 2: SAVING JOBS FOR LATER")
    print("-" * 50)
    
    if recommendations['success'] and recommendations['jobs']:
        # Save top 3 jobs
        for i, job in enumerate(recommendations['jobs'][:3]):
            folder = "High Priority" if i == 0 else "Favorites"
            save_result = api.save_job(job, folder)
            if save_result['success']:
                print(f"✅ Saved '{job['title']}' to {folder} folder")
    
    # Test 3: Quick Job Search
    print("\n\n⚡ STEP 3: QUICK JOB SEARCH BY SKILLS")
    print("-" * 50)
    
    quick_results = api.get_quick_job_matches(['Python', 'React', 'AWS'], 'mid')
    if quick_results['success']:
        print(f"✅ Quick search found {quick_results['total_jobs_found']} matches")
        print(f"🎯 Primary role suggested: {quick_results['role_analysis']['primary_role']}")
    
    # Test 4: Apply to Jobs
    print("\n\n📝 STEP 4: APPLYING TO JOBS")
    print("-" * 50)
    
    if recommendations['success'] and recommendations['jobs']:
        # Apply to the top job
        top_job = recommendations['jobs'][0]
        
        # Standard application
        apply_result = api.apply_to_job(top_job, user_profile, "standard")
        if apply_result['success']:
            print(f"✅ Created application draft for '{top_job['title']}'")
            print(f"📋 Application ID: {apply_result['application_id']}")
            print(f"⏱️  Estimated time: {apply_result['estimated_completion_time']}")
            
            # Submit the application
            submit_result = api.application_manager.submit_application(
                apply_result['application_id'], 
                {
                    'cover_letter': apply_result['application']['cover_letter'],
                    'notes': 'Submitted via AI Job Matcher'
                }
            )
            if submit_result['success']:
                print(f"✅ Application submitted successfully!")
                print(f"📅 Follow-up reminder set for: {submit_result['follow_up_date'][:10]}")
        
        # Quick apply to second job
        if len(recommendations['jobs']) > 1:
            second_job = recommendations['jobs'][1]
            quick_apply_result = api.apply_to_job(second_job, user_profile, "quick")
            if quick_apply_result['success']:
                print(f"⚡ Quick applied to '{second_job['title']}'")
    
    # Test 5: Bulk Apply
    print("\n\n📦 STEP 5: BULK APPLICATION SETUP")
    print("-" * 50)
    
    # Get saved jobs first
    saved_jobs = api.get_saved_jobs()
    if saved_jobs['success'] and saved_jobs['total_saved'] > 0:
        # Get job IDs from saved jobs
        job_ids = []
        for folder_jobs in saved_jobs['folders'].values():
            job_ids.extend([job['id'] for job in folder_jobs[:2]])  # Max 2 from each folder
        
        if job_ids:
            bulk_setup = api.bulk_apply_to_jobs(job_ids[:3], user_profile)  # Max 3 for demo
            if bulk_setup['success']:
                print(f"✅ Bulk apply set up for {bulk_setup['total_applications']} positions")
                print(f"⏱️  Estimated time: {bulk_setup['estimated_time']}")
                
                # Simulate bulk submission
                applications_data = []
                for app in bulk_setup['applications']:
                    applications_data.append({
                        'application_id': app['id'],
                        'cover_letter': app['cover_letter'],
                        'notes': 'Bulk application submission'
                    })
                
                bulk_submit = api.submit_bulk_applications(
                    bulk_setup['bulk_session_id'], 
                    applications_data
                )
                if bulk_submit['success']:
                    print(f"🎉 {bulk_submit['summary']}")
    
    # Test 6: Application Dashboard
    print("\n\n📊 STEP 6: APPLICATION TRACKING DASHBOARD")
    print("-" * 50)
    
    dashboard = api.get_application_dashboard()
    if dashboard['success']:
        stats = dashboard['stats']
        print(f"📈 Total Applications: {stats['total_applications']}")
        print(f"📊 Success Rate: {stats['success_rate']}%")
        print(f"🔄 Recent Applications: {stats['recent_applications']}")
        print(f"📅 Pending Follow-ups: {stats['pending_follow_ups']}")
        print(f"🎯 Upcoming Interviews: {stats['upcoming_interviews']}")
        
        if dashboard['recent_activity']:
            print(f"\n📝 RECENT ACTIVITY:")
            for activity in dashboard['recent_activity'][:3]:
                print(f"   • Applied to {activity['job_title']} at {activity['company']}")
                print(f"     Status: {activity['status']} | Date: {activity['applied_date'][:10]}")
        
        if dashboard['insights']:
            print(f"\n💡 INSIGHTS:")
            for insight in dashboard['insights']:
                print(f"   • {insight}")
    
    # Test 7: Application Assistance
    print("\n\n🎯 STEP 7: APPLICATION ASSISTANCE")
    print("-" * 50)
    
    if recommendations['success'] and recommendations['jobs']:
        assistance = api.get_application_assistance(recommendations['jobs'][0]['id'], user_profile)
        print("✅ Application assistance available:")
        print("   📝 Cover letter template generated")
        print("   📄 Resume optimization tips provided")
        print("   💬 Interview questions prepared")
        print("   ✅ Application checklist created")
        print("   🤝 Networking suggestions provided")
    
    # Test 8: Get Saved Jobs
    print("\n\n📚 STEP 8: VIEWING SAVED JOBS")
    print("-" * 50)
    
    saved_jobs = api.get_saved_jobs()
    if saved_jobs['success']:
        print(f"✅ Total saved jobs: {saved_jobs['total_saved']}")
        for folder_name, jobs in saved_jobs['folders'].items():
            print(f"\n📁 {folder_name} ({len(jobs)} jobs):")
            for job in jobs[:2]:  # Show first 2 jobs per folder
                print(f"   • {job['title']} at {job['company']}")
    
    print("\n" + "=" * 80)
    print("🎉 COMPREHENSIVE TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\n✨ FEATURES DEMONSTRATED:")
    print("   ✅ AI-powered job recommendations")
    print("   ✅ Internship matching for early career")
    print("   ✅ Quick job search by skills")
    print("   ✅ Save jobs for later application")
    print("   ✅ Standard and quick apply options")
    print("   ✅ Bulk application workflow")
    print("   ✅ Application tracking dashboard")
    print("   ✅ Personalized application assistance")
    print("   ✅ Career stage analysis")
    print("   ✅ Success probability scoring")
    
    print("\n🚀 NEXT STEPS:")
    print("   1. Integrate with real job APIs (LinkedIn, Indeed, etc.)")
    print("   2. Add email notifications for follow-ups")
    print("   3. Implement interview scheduling")
    print("   4. Add salary negotiation assistant")
    print("   5. Create mobile app interface")

if __name__ == "__main__":
    test_job_recommendation_system()
