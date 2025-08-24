"""
Job Recommender Module
Job Recommender system that matches resumes with job descriptions and provides scoring
"""

import numpy as np
from typing import List, Dict, Tuple, Any
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobRecommender:
    """
    Job Recommender system that matches resumes with job descriptions and provides scoring
    """
    
    def __init__(self):
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Sample job descriptions (in real implementation, this would come from a job database)
        self.sample_jobs = [
            {
                'id': 'job_001',
                'title': 'Senior Python Developer',
                'company': 'TechCorp Inc.',
                'description': """
                We are seeking a Senior Python Developer to join our dynamic team. The ideal candidate will have 5+ years of experience in Python development, strong knowledge of Django/Flask frameworks, experience with databases like PostgreSQL and MongoDB, and familiarity with cloud platforms like AWS. Experience with machine learning libraries like TensorFlow or PyTorch is a plus. Strong problem-solving skills and ability to work in an agile environment are essential.
                """,
                'required_skills': ['python', 'django', 'flask', 'postgresql', 'mongodb', 'aws'],
                'experience_level': 'senior',
                'salary_range': '$90,000 - $130,000'
            },
            {
                'id': 'job_002',
                'title': 'Frontend React Developer',
                'company': 'WebSolutions Ltd.',
                'description': """
                Looking for a talented Frontend Developer with expertise in React.js. The candidate should have 3+ years of experience in modern JavaScript, React, Redux, HTML5, CSS3, and responsive design. Experience with TypeScript, Node.js, and testing frameworks like Jest is preferred. Must have strong attention to detail and excellent communication skills.
                """,
                'required_skills': ['javascript', 'react', 'redux', 'html', 'css', 'typescript'],
                'experience_level': 'mid',
                'salary_range': '$70,000 - $95,000'
            },
            {
                'id': 'job_003',
                'title': 'Data Scientist',
                'company': 'DataInsights AI',
                'description': """
                We are hiring a Data Scientist to analyze complex datasets and build predictive models. Requirements include advanced Python skills, experience with pandas, numpy, scikit-learn, TensorFlow/PyTorch, statistical analysis, and machine learning algorithms. PhD in Statistics, Mathematics, or Computer Science preferred. Experience with big data tools like Spark and cloud platforms is a plus.
                """,
                'required_skills': ['python', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
                'experience_level': 'senior',
                'salary_range': '$100,000 - $150,000'
            },
            {
                'id': 'job_004',
                'title': 'Junior Full Stack Developer',
                'company': 'StartupHub',
                'description': """
                Entry-level position for a Full Stack Developer. We're looking for someone with basic knowledge of JavaScript, HTML, CSS, and either React or Vue.js for frontend, plus Node.js or Python for backend. Fresh graduates welcome. We provide mentorship and growth opportunities. Interest in learning new technologies is more important than years of experience.
                """,
                'required_skills': ['javascript', 'html', 'css', 'react', 'nodejs', 'python'],
                'experience_level': 'entry',
                'salary_range': '$50,000 - $70,000'
            },
            {
                'id': 'job_005',
                'title': 'DevOps Engineer',
                'company': 'CloudFirst Systems',
                'description': """
                Seeking a DevOps Engineer with expertise in containerization and cloud infrastructure. Requirements include experience with Docker, Kubernetes, AWS/Azure, CI/CD pipelines, Infrastructure as Code (Terraform), monitoring tools, and scripting languages. Experience with microservices architecture and security best practices is essential.
                """,
                'required_skills': ['docker', 'kubernetes', 'aws', 'terraform', 'jenkins', 'python'],
                'experience_level': 'mid',
                'salary_range': '$85,000 - $120,000'
            },
            {
                'id': 'job_006',
                'title': 'AI/ML Engineer',
                'company': 'FutureAI Corp',
                'description': """
                We are seeking an AI/ML Engineer to develop and deploy machine learning models. 
                Requirements include Python, TensorFlow/PyTorch, AWS/GCP, Docker, and experience 
                with MLOps. Knowledge of computer vision and NLP is a plus.
                """,
                'required_skills': ['python', 'tensorflow', 'pytorch', 'aws', 'docker'],
                'experience_level': 'mid',
                'salary_range': '$95,000 - $140,000'
            },
            {
                'id': 'job_007',
                'title': 'Full Stack JavaScript Developer',
                'company': 'Modern Web Co.',
                'description': """
                Looking for a Full Stack JavaScript Developer with expertise in Node.js and React. 
                The ideal candidate should have experience with MongoDB, Express.js, modern JavaScript (ES6+), 
                RESTful APIs, and responsive web design. Knowledge of TypeScript and cloud platforms is preferred.
                """,
                'required_skills': ['javascript', 'nodejs', 'react', 'mongodb', 'express', 'typescript'],
                'experience_level': 'mid',
                'salary_range': '$75,000 - $110,000'
            },
            {
                'id': 'job_008',
                'title': 'Mobile App Developer (React Native)',
                'company': 'AppTech Solutions',
                'description': """
                Seeking a Mobile App Developer with expertise in React Native. Requirements include 
                JavaScript/TypeScript, React Native, iOS/Android development, Redux, and mobile UI/UX best practices. 
                Experience with native iOS (Swift) or Android (Kotlin) development is a plus.
                """,
                'required_skills': ['javascript', 'react', 'typescript', 'redux', 'swift', 'kotlin'],
                'experience_level': 'mid',
                'salary_range': '$80,000 - $115,000'
            },
            {
                'id': 'job_009',
                'title': 'Backend Java Developer',
                'company': 'Enterprise Systems Inc.',
                'description': """
                We are hiring a Backend Java Developer to work on enterprise-grade applications. 
                Requirements include Java 8+, Spring Framework, Hibernate, PostgreSQL/Oracle, 
                microservices architecture, and REST API development. Experience with cloud platforms 
                (AWS/Azure) and containerization (Docker) is preferred.
                """,
                'required_skills': ['java', 'spring', 'hibernate', 'postgresql', 'docker', 'aws'],
                'experience_level': 'mid',
                'salary_range': '$85,000 - $125,000'
            },
            {
                'id': 'job_010',
                'title': 'Cloud Solutions Architect',
                'company': 'CloudNative Corp',
                'description': """
                Seeking a Cloud Solutions Architect to design and implement scalable cloud infrastructure. 
                Requirements include AWS/Azure/GCP expertise, Terraform, Kubernetes, Docker, 
                microservices architecture, and security best practices. Strong communication and 
                leadership skills are essential for client interactions.
                """,
                'required_skills': ['aws', 'azure', 'terraform', 'kubernetes', 'docker', 'python'],
                'experience_level': 'senior',
                'salary_range': '$120,000 - $180,000'
            }
        ]
    
    def calculate_skill_match_score(self, resume_skills: Dict[str, List[str]], job_skills: List[str]) -> Dict[str, Any]:
        """Calculate skill matching score between resume and job"""
        # Flatten resume skills
        all_resume_skills = []
        for category_skills in resume_skills.values():
            all_resume_skills.extend([skill.lower() for skill in category_skills])
        
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Calculate matches
        matched_skills = list(set(all_resume_skills) & set(job_skills_lower))
        missing_skills = list(set(job_skills_lower) - set(all_resume_skills))
        
        # Calculate score
        skill_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
        
        return {
            'skill_match_score': skill_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'total_required_skills': len(job_skills_lower),
            'total_matched_skills': len(matched_skills)
        }
    
    def calculate_experience_match_score(self, resume_experience: Dict[str, Any], job_experience_level: str) -> Dict[str, Any]:
        """Calculate experience level matching score"""
        experience_hierarchy = {'entry': 1, 'mid': 2, 'senior': 3, 'executive': 4}
        
        resume_level_score = experience_hierarchy.get(resume_experience['primary_level'], 1)
        job_level_score = experience_hierarchy.get(job_experience_level, 1)
        
        # Calculate experience match score
        if resume_level_score >= job_level_score:
            experience_score = 1.0  # Perfect match or overqualified
        else:
            # Penalize underqualification
            experience_score = resume_level_score / job_level_score
        
        return {
            'experience_match_score': experience_score,
            'resume_level': resume_experience['primary_level'],
            'job_level': job_experience_level,
            'level_difference': resume_level_score - job_level_score,
            'years_of_experience': resume_experience['years_of_experience']
        }
    
    def calculate_semantic_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        # Generate embeddings
        resume_embedding = self.sentence_model.encode([resume_text])
        job_embedding = self.sentence_model.encode([job_description])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return float(similarity)
    
    def calculate_overall_score(self, skill_match: Dict[str, Any], experience_match: Dict[str, Any], 
                               semantic_similarity: float, weights: Dict[str, float] = None) -> Dict[str, Any]:
        """Calculate overall compatibility score"""
        if weights is None:
            weights = {
                'skills': 0.4,
                'experience': 0.3,
                'semantic': 0.3
            }
        
        # Calculate weighted score
        overall_score = (
            skill_match['skill_match_score'] * weights['skills'] +
            experience_match['experience_match_score'] * weights['experience'] +
            semantic_similarity * weights['semantic']
        )
        
        # Determine recommendation level
        if overall_score >= 0.8:
            recommendation = "Excellent Match"
            color = "🟢"
        elif overall_score >= 0.6:
            recommendation = "Good Match"
            color = "🟡"
        elif overall_score >= 0.4:
            recommendation = "Fair Match"
            color = "🟠"
        else:
            recommendation = "Poor Match"
            color = "🔴"
        
        return {
            'overall_score': overall_score,
            'recommendation': recommendation,
            'color': color,
            'score_breakdown': {
                'skills_score': skill_match['skill_match_score'] * weights['skills'],
                'experience_score': experience_match['experience_match_score'] * weights['experience'],
                'semantic_score': semantic_similarity * weights['semantic']
            },
            'weights_used': weights
        }
    
    def match_resume_with_job(self, resume_analysis: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
        """Match a single resume with a single job"""
        # Calculate individual scores
        skill_match = self.calculate_skill_match_score(resume_analysis['skills'], job['required_skills'])
        experience_match = self.calculate_experience_match_score(resume_analysis['experience'], job['experience_level'])
        semantic_similarity = self.calculate_semantic_similarity(resume_analysis['raw_text'], job['description'])
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(skill_match, experience_match, semantic_similarity)
        
        return {
            'job_id': job['id'],
            'job_title': job['title'],
            'company': job['company'],
            'salary_range': job['salary_range'],
            'skill_match': skill_match,
            'experience_match': experience_match,
            'semantic_similarity': semantic_similarity,
            'overall_score': overall_score
        }
    
    def get_job_recommendations(self, resume_analysis: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """Get top job recommendations for a resume"""
        recommendations = []
        
        for job in self.sample_jobs:
            match_result = self.match_resume_with_job(resume_analysis, job)
            recommendations.append(match_result)
        
        # Sort by overall score
        recommendations.sort(key=lambda x: x['overall_score']['overall_score'], reverse=True)
        
        return recommendations[:top_n]
    
    def generate_detailed_report(self, resume_analysis: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> str:
        """Generate a detailed report of the analysis"""
        report = []
        report.append("=" * 80)
        report.append("📊 RESUME ANALYSIS & JOB RECOMMENDATION REPORT")
        report.append("=" * 80)
        
        # Resume Summary
        report.append("\n📋 RESUME SUMMARY:")
        report.append(f"📧 Email: {resume_analysis['contact_info'].get('email', 'Not found')}")
        report.append(f"📞 Phone: {resume_analysis['contact_info'].get('phone', 'Not found')}")
        report.append(f"💼 Experience Level: {resume_analysis['experience']['primary_level'].title()}")
        report.append(f"📈 Years of Experience: {resume_analysis['experience']['years_of_experience']}")
        report.append(f"🎯 Total Skills Found: {resume_analysis['total_skills_found']}")
        
        # Skills Breakdown
        report.append("\n🛠️  SKILLS BREAKDOWN:")
        for category, skills in resume_analysis['skills'].items():
            if skills:
                report.append(f"  {category.replace('_', ' ').title()}: {', '.join(skills)}")
        
        # Top Recommendations
        report.append("\n🎯 TOP JOB RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            overall = rec['overall_score']
            report.append(f"\n{i}. {overall['color']} {rec['job_title']} at {rec['company']}")
            report.append(f"   💯 Overall Score: {overall['overall_score']:.1%} ({overall['recommendation']})")
            report.append(f"   💰 Salary: {rec['salary_range']}")
            report.append(f"   🎯 Skills Match: {rec['skill_match']['skill_match_score']:.1%} ({rec['skill_match']['total_matched_skills']}/{rec['skill_match']['total_required_skills']} skills)")
            report.append(f"   📈 Experience Match: {rec['experience_match']['experience_match_score']:.1%}")
            report.append(f"   🔍 Semantic Similarity: {rec['semantic_similarity']:.1%}")
            
            if rec['skill_match']['missing_skills']:
                report.append(f"   ⚠️  Missing Skills: {', '.join(rec['skill_match']['missing_skills'])}")
        
        return "\n".join(report)
