#!/usr/bin/env python3
"""
Quick test to generate sample localStorage data for testing the technical skills display
"""

import requests
import json
from io import BytesIO

def generate_sample_localStorage_data():
    # Create demo resume content
    demo_content = """John Doe
Software Engineer

Contact Information:
- Email: john.doe@email.com
- Phone: (555) 123-4567
- Location: San Francisco, CA

TECHNICAL SKILLS
- Programming Languages: JavaScript, Python, TypeScript, Java, C++
- Frontend Technologies: React, Vue.js, HTML5, CSS3, Tailwind CSS
- Backend Technologies: Node.js, Express.js, Django, Flask
- Databases: MongoDB, PostgreSQL, MySQL, Redis
- Cloud Platforms: AWS, Google Cloud Platform, Azure
- DevOps Tools: Docker, Kubernetes, Jenkins, Git, GitHub Actions

WORK EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Led development of microservices architecture serving 1M+ users
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews
- Built scalable REST APIs using Node.js and PostgreSQL

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018
"""

    # Create file-like object
    files = {
        'resume': ('test_resume.txt', BytesIO(demo_content.encode('utf-8')), 'text/plain')
    }
    
    try:
        # Send request to backend
        response = requests.post('http://localhost:5000/upload-resume', files=files)
        
        if response.status_code == 200:
            data = response.json()
            
            # Print the localStorage format that should be used
            print("=== SAMPLE localStorage DATA FOR TESTING ===")
            print("To test the technical skills display, paste this into your browser console:")
            print(f"localStorage.setItem('latestResumeAnalysis', '{json.dumps(data)}');")
            print()
            print("=== BREAKDOWN OF EXTRACTED DATA ===")
            print(f"Total Skills Count: {data.get('total_skills_count', 0)}")
            print(f"Skills by Category: {data.get('skills_by_category', {})}")
            print(f"Technical Skills categories found:")
            
            skills_by_category = data.get('skills_by_category', {})
            tech_categories = ['programming_languages', 'web_technologies', 'frameworks_libraries', 'databases', 'cloud_platforms', 'devops_tools']
            
            total_tech_skills = 0
            for category in tech_categories:
                if category in skills_by_category:
                    skills = skills_by_category[category]
                    total_tech_skills += len(skills)
                    print(f"  - {category}: {skills}")
            
            print(f"\nTotal Technical Skills: {total_tech_skills}")
            print(f"Suggested Role: {data.get('suggested_role', 'N/A')}")
            print(f"Resume Score: {data.get('resume_score', 'N/A')}%")
            
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    generate_sample_localStorage_data()
