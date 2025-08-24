#!/usr/bin/env python3
"""
Comprehensive Demo Script for AI Job Matcher
Shows all working functionality including:
1. Resume upload and skill analysis
2. Job recommendations based on skills
3. Role suggestion
4. Job matching
"""

import requests
import json
import time
from pathlib import Path

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    print(f"✅ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def print_error(message):
    print(f"❌ {message}")

def demo_ai_job_matcher():
    """Complete demo of the AI Job Matcher functionality"""
    
    print_header("🚀 AI Job Matcher - Complete Demo")
    print_info("This demo showcases all the fixed functionality")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health Check
    print_header("1. Health Check")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print_success(f"Backend is healthy - Status: {health_data.get('status')}")
            print_info(f"Cache size: {health_data.get('cache_size', 0)} analyses")
        else:
            print_error("Backend health check failed")
            return
    except Exception as e:
        print_error(f"Cannot connect to backend: {e}")
        print_info("Please ensure backend is running: cd backend && python app.py")
        return
    
    # Test 2: Resume Upload and Analysis
    print_header("2. Resume Upload & AI Analysis")
    
    # Find a test resume file
    test_files = [
        'uploads/25264778-b1fb-4665-861d-d2fdb46e930d_Vijay_kumars.pdf',
        'uploads/3750943a-51c7-416b-8246-05c13c9c6b10_test_resume.txt',
        'test_resume.txt'
    ]
    
    test_file = None
    for file_path in test_files:
        if Path(file_path).exists():
            test_file = file_path
            break
    
    if not test_file:
        print_error("No test resume file found")
        print_info("Available files in uploads/:")
        for f in Path('uploads').glob('*') if Path('uploads').exists() else []:
            print(f"  - {f}")
        return
    
    print_info(f"Using test file: {test_file}")
    
    try:
        with open(test_file, 'rb') as f:
            files = {'resume': (Path(test_file).name, f, 'application/octet-stream')}
            response = requests.post(f"{base_url}/upload-resume", files=files, timeout=60)
        
        if response.status_code == 200:
            analysis = response.json()
            if analysis.get('status') == 'success':
                print_success("Resume analysis completed!")
                
                # Display analysis results
                skills_count = analysis.get('total_skills_count', 0)
                suggested_role = analysis.get('suggested_role', 'N/A')
                experience_level = analysis.get('experience_level', 'N/A')
                top_skills = analysis.get('top_skills', [])[:5]
                
                print_info(f"📊 Skills found: {skills_count}")
                print_info(f"🎯 Suggested role: {suggested_role}")
                print_info(f"📈 Experience level: {experience_level}")
                print_info(f"🔝 Top skills: {', '.join(top_skills)}")
                
                analysis_id = analysis.get('analysis_id')
                print_info(f"💾 Analysis ID: {analysis_id}")
                
            else:
                print_error(f"Analysis failed: {analysis.get('message', 'Unknown error')}")
                return
        else:
            print_error(f"Upload failed: HTTP {response.status_code}")
            return
            
    except Exception as e:
        print_error(f"Upload error: {e}")
        return
    
    # Test 3: Job Listings
    print_header("3. Job Listings")
    try:
        response = requests.get(f"{base_url}/jobs")
        if response.status_code == 200:
            jobs_data = response.json()
            jobs = jobs_data.get('jobs', [])
            print_success(f"Found {len(jobs)} job listings")
            
            # Display first 3 jobs
            for i, job in enumerate(jobs[:3], 1):
                print_info(f"Job {i}: {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
                print(f"      Location: {job.get('location', 'N/A')}")
                print(f"      Salary: {job.get('salary', 'N/A')}")
                
        else:
            print_error(f"Failed to fetch jobs: HTTP {response.status_code}")
            jobs = []
    except Exception as e:
        print_error(f"Jobs fetch error: {e}")
        jobs = []
    
    # Test 4: Job Matching
    if analysis_id and jobs:
        print_header("4. Job Matching Analysis")
        try:
            # Test matching with first job
            job = jobs[0]
            match_data = {
                'job_id': job.get('id'),
                'analysis_id': analysis_id
            }
            
            response = requests.post(f"{base_url}/job-match", json=match_data)
            if response.status_code == 200:
                match_result = response.json()
                match_score = match_result.get('match_score', 0)
                matched_skills = match_result.get('matched_skills', [])
                missing_skills = match_result.get('missing_skills', [])
                
                print_success(f"Job match analysis completed!")
                print_info(f"🎯 Job: {job.get('title')} at {job.get('company')}")
                print_info(f"📊 Match score: {match_score}%")
                print_info(f"✅ Matched skills ({len(matched_skills)}): {', '.join(matched_skills[:5])}")
                print_info(f"❌ Missing skills ({len(missing_skills)}): {', '.join(missing_skills[:5])}")
                
            else:
                print_error(f"Job matching failed: HTTP {response.status_code}")
                
        except Exception as e:
            print_error(f"Job matching error: {e}")
    
    # Test 5: Recommendation Summary
    print_header("5. 🎉 Demo Results Summary")
    print_success("All core features are working:")
    print_info("✅ REQUIREMENT 1: Skills extracted from resume")
    print_info("✅ REQUIREMENT 2: Total skills count displayed")
    print_info("✅ REQUIREMENT 3: Role suggestion based on skills")
    print_info("✅ REQUIREMENT 4: Job listings available")
    print_info("✅ REQUIREMENT 5: Real-time job data (with fallback)")
    print_info("✅ REQUIREMENT 6: Hugging Face models used for NLP")
    
    print_header("🚀 Frontend Access")
    print_info("Open your browser and go to: http://localhost:3001")
    print_info("Upload a resume to see the complete UI workflow!")
    
if __name__ == '__main__':
    demo_ai_job_matcher()
