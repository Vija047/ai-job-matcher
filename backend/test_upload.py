#!/usr/bin/env python3
"""
Test script to check what the upload endpoint is returning
"""

import requests
import json
from io import BytesIO

def test_upload():
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
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("\nResponse Data:")
            print(json.dumps(data, indent=2))
            
            # Check specifically for technical skills
            if 'skills_by_category' in data:
                print(f"\nSkills by category found: {data['skills_by_category']}")
            if 'technical_skills' in data:
                print(f"\nTechnical skills found: {data['technical_skills']}")
            if 'skills_extracted' in data:
                print(f"\nExtracted skills found: {data['skills_extracted']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_upload()
