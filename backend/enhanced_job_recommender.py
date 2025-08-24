"""
Enhanced Job Recommender with Hugging Face Models
Advanced job matching using state-of-the-art NLP models and real-time data
"""

import numpy as np
from typing import List, Dict, Tuple, Any, Optional
import asyncio
from datetime import datetime, timedelta

# Hugging Face transformers
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
    pipeline, BertTokenizer, BertModel
)
import torch
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

# Custom imports
from realtime_job_scraper import RealTimeJobScraper, JobPosting

class EnhancedJobRecommender:
    @staticmethod
    def _make_serializable(obj):
        """Recursively convert numpy types and dataclasses to serializable types."""
        import numpy as np
        from dataclasses import asdict, is_dataclass
        if isinstance(obj, dict):
            return {k: EnhancedJobRecommender._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [EnhancedJobRecommender._make_serializable(i) for i in obj]
        elif is_dataclass(obj):
            return EnhancedJobRecommender._make_serializable(asdict(obj))
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        else:
            return obj
    """
    Enhanced Job Recommender using Hugging Face models and real-time job data
    """
    
    def __init__(self):
        print("🚀 Initializing Enhanced Job Recommender with Hugging Face models...")
        
        # Initialize job scraper
        self.job_scraper = RealTimeJobScraper()
        
        # Initialize Hugging Face models
        self._init_huggingface_models()
        
        # Initialize sentence transformer for semantic analysis
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Job cache for performance
        self.job_cache = {}
        self.cache_timestamp = None
        self.cache_duration = timedelta(hours=2)  # Cache jobs for 2 hours
        
        print("✅ Enhanced Job Recommender initialized successfully!")
    
    def _init_huggingface_models(self):
        """Initialize lightweight Hugging Face models for job recommendation"""
        try:
            print("Loading lightweight models for job recommendation...")
            
            # Job-resume matching model - force CPU usage to save memory
            try:
                self.job_match_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # Force CPU usage
                )
                print("✅ Job match classifier loaded")
            except Exception as e:
                print(f"⚠️  Job match classifier failed: {e}")
                self.job_match_classifier = None
            
            # Skill compatibility assessment - keep this as it's already lightweight
            try:
                self.skill_compatibility = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1
                )
                print("✅ Skill compatibility model loaded")
            except Exception as e:
                print(f"⚠️  Skill compatibility failed: {e}")
                self.skill_compatibility = None
            
            # Skip heavy models to save memory
            self.salary_predictor = None
            self.career_analyzer = None
            
            print("✅ Lightweight job recommendation models initialized!")
            
        except Exception as e:
            print(f"⚠️  Error loading job recommendation models: {e}")
            # Fallback to None
            self.job_match_classifier = None
            self.skill_compatibility = None
            self.salary_predictor = None
            self.career_analyzer = None
    
    async def get_personalized_recommendations(
        self, 
        resume_analysis: Dict[str, Any], 
        preferences: Dict[str, Any] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Get personalized job recommendations based on resume analysis"""
        
        print("🔍 Getting personalized job recommendations...")
        
        # Extract key information from resume
        skills = self._extract_user_skills(resume_analysis)
        experience_level = resume_analysis.get('experience', {}).get('primary_level', 'mid')
        location = preferences.get('location', '') if preferences else ''
        
        # Fetch real-time jobs
        jobs = await self._get_cached_jobs(skills[:5], location, limit * 2)  # Fetch more for better filtering
        
        if not jobs:
            print("⚠️  No jobs found from real-time sources")
            jobs = self._get_fallback_jobs(skills, experience_level)
        
        # Score and rank jobs
        scored_jobs = []
        for job in jobs:
            score_details = await self._calculate_comprehensive_job_score(resume_analysis, job)
            scored_jobs.append({
                'job': job,
                'score': score_details['total_score'],
                'score_details': score_details
            })
        
        # Sort by score and limit results
        scored_jobs.sort(key=lambda x: x['score'], reverse=True)
        top_jobs = scored_jobs[:limit]
        
        # Generate insights and recommendations
        insights = self._generate_insights(resume_analysis, top_jobs)
        
        # Create application assistance
        application_help = self._generate_application_assistance(top_jobs[:5])
        
        result = {
            'recommendations': top_jobs,
            'insights': insights,
            'application_assistance': application_help,
            'market_analysis': self._analyze_job_market(jobs),
            'skill_gaps': self._identify_skill_gaps(resume_analysis, jobs),
            'career_paths': self._suggest_career_paths(resume_analysis, jobs),
            'timestamp': datetime.now().isoformat()
        }
        return EnhancedJobRecommender._make_serializable(result)
    
    def get_recommendations_sync(
        self, 
        resume_analysis: Dict[str, Any], 
        preferences: Dict[str, Any] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Synchronous wrapper for getting recommendations"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.get_personalized_recommendations(resume_analysis, preferences, limit)
            )
        finally:
            loop.close()
    
    async def _get_cached_jobs(self, keywords: List[str], location: str, limit: int) -> List[JobPosting]:
        """Get jobs with caching mechanism"""
        cache_key = f"{'-'.join(keywords)}_{location}_{limit}"
        
        # Check if cache is valid
        if (self.cache_timestamp and 
            datetime.now() - self.cache_timestamp < self.cache_duration and
            cache_key in self.job_cache):
            print("📋 Using cached job data")
            return self.job_cache[cache_key]
        
        # Fetch fresh jobs
        print("🌐 Fetching real-time job data...")
        jobs = await self.job_scraper.fetch_jobs_async(keywords, location, limit)
        
        # Update cache
        self.job_cache[cache_key] = jobs
        self.cache_timestamp = datetime.now()
        
        print(f"✅ Found {len(jobs)} real-time jobs")
        return jobs
    
    async def _calculate_comprehensive_job_score(
        self, 
        resume_analysis: Dict[str, Any], 
        job: JobPosting
    ) -> Dict[str, Any]:
        """Calculate comprehensive job matching score using multiple factors"""
        
        scores = {}
        
        # 1. Skill matching score (40% weight)
        skill_score = self._calculate_skill_match_score(resume_analysis, job)
        scores['skill_match'] = skill_score
        
        # 2. Experience level matching (20% weight)
        experience_score = self._calculate_experience_match_score(resume_analysis, job)
        scores['experience_match'] = experience_score
        
        # 3. Semantic similarity using Hugging Face (25% weight)
        semantic_score = await self._calculate_semantic_similarity_enhanced(resume_analysis, job)
        scores['semantic_similarity'] = semantic_score
        
        # 4. Company and role fit (10% weight)
        role_fit_score = self._calculate_role_fit_score(resume_analysis, job)
        scores['role_fit'] = role_fit_score
        
        # 5. Salary and benefits match (5% weight)
        compensation_score = self._calculate_compensation_score(resume_analysis, job)
        scores['compensation'] = compensation_score
        
        # Calculate weighted total score
        weights = {
            'skill_match': 0.40,
            'experience_match': 0.20,
            'semantic_similarity': 0.25,
            'role_fit': 0.10,
            'compensation': 0.05
        }
        
        total_score = sum(scores[key] * weights[key] for key in scores.keys())
        
        return {
            'total_score': total_score,
            'individual_scores': scores,
            'weights': weights,
            'recommendation_reason': self._generate_recommendation_reason(scores, job)
        }
    
    def _calculate_skill_match_score(self, resume_analysis: Dict[str, Any], job: JobPosting) -> float:
        """Calculate skill matching score"""
        user_skills = self._extract_user_skills(resume_analysis)
        job_skills = job.skills + self._extract_skills_from_text(job.description)
        
        if not user_skills or not job_skills:
            return 0.0
        
        # Convert to lowercase for comparison
        user_skills_lower = [skill.lower() for skill in user_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        # Calculate matches
        matched_skills = set(user_skills_lower) & set(job_skills_lower)
        
        # Base skill match score
        base_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
        
        # Bonus for high-demand skills
        high_demand_skills = ['python', 'react', 'aws', 'machine learning', 'docker', 'kubernetes']
        bonus = sum(1 for skill in matched_skills if skill in high_demand_skills) * 0.1
        
        return min(1.0, base_score + bonus)
    
    def _calculate_experience_match_score(self, resume_analysis: Dict[str, Any], job: JobPosting) -> float:
        """Calculate experience level matching score"""
        experience_hierarchy = {'entry': 1, 'mid': 2, 'senior': 3, 'executive': 4}
        
        user_level = resume_analysis.get('experience', {}).get('primary_level', 'mid')
        job_level = job.experience_level
        
        user_score = experience_hierarchy.get(user_level, 2)
        job_score = experience_hierarchy.get(job_level, 2)
        
        # Perfect match gets 1.0
        if user_score == job_score:
            return 1.0
        # Overqualified gets slight penalty
        elif user_score > job_score:
            return 0.8 - (user_score - job_score) * 0.1
        # Underqualified gets larger penalty
        else:
            return max(0.2, 0.6 - (job_score - user_score) * 0.15)
    
    async def _calculate_semantic_similarity_enhanced(
        self, 
        resume_analysis: Dict[str, Any], 
        job: JobPosting
    ) -> float:
        """Calculate semantic similarity using enhanced methods"""
        
        # Get resume text
        resume_text = resume_analysis.get('raw_text', '')[:1000]  # Limit text
        job_text = f"{job.title} {job.description}"[:1000]
        
        # Basic sentence transformer similarity
        try:
            resume_embedding = self.sentence_model.encode([resume_text])
            job_embedding = self.sentence_model.encode([job_text])
            base_similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        except:
            base_similarity = 0.5
        
        # Enhanced similarity using Hugging Face zero-shot classification
        enhanced_similarity = base_similarity
        
        if self.job_match_classifier:
            try:
                # Classify if resume matches job categories
                job_categories = ['software engineering', 'data science', 'product management', 
                                'design', 'marketing', 'sales', 'operations']
                
                resume_classification = self.job_match_classifier(resume_text, job_categories)
                job_classification = self.job_match_classifier(job_text, job_categories)
                
                # If both classify to same category with high confidence, boost similarity
                if (resume_classification['labels'][0] == job_classification['labels'][0] and
                    resume_classification['scores'][0] > 0.7 and job_classification['scores'][0] > 0.7):
                    enhanced_similarity = min(1.0, enhanced_similarity + 0.2)
                    
            except Exception as e:
                print(f"Enhanced similarity calculation failed: {e}")
        
        return enhanced_similarity
    
    def _calculate_role_fit_score(self, resume_analysis: Dict[str, Any], job: JobPosting) -> float:
        """Calculate how well the role fits the candidate"""
        score = 0.5  # Base score
        
        # Check job title alignment
        resume_text = resume_analysis.get('raw_text', '').lower()
        job_title_lower = job.title.lower()
        
        # Look for role-related keywords in resume
        if any(word in resume_text for word in job_title_lower.split()):
            score += 0.3
        
        # Check company size preference (if available)
        # This would be enhanced with more sophisticated analysis
        
        # Check location preference
        user_location = resume_analysis.get('contact_info', {}).get('location', '')
        if user_location and user_location.lower() in job.location.lower():
            score += 0.2
        
        return min(1.0, score)
    
    def _calculate_compensation_score(self, resume_analysis: Dict[str, Any], job: JobPosting) -> float:
        """Calculate compensation satisfaction score"""
        # This is a simplified version - in reality, you'd have user preferences
        if 'not specified' in job.salary_range.lower():
            return 0.5
        
        # Extract salary range and apply basic logic
        # For demo purposes, assume all salaries are reasonable
        return 0.8
    
    def _extract_user_skills(self, resume_analysis: Dict[str, Any]) -> List[str]:
        """Extract all user skills from resume analysis"""
        skills = []
        
        # From skills analysis
        skills_analysis = resume_analysis.get('skills_analysis', {})
        if 'skills_by_category' in skills_analysis:
            for category_skills in skills_analysis['skills_by_category'].values():
                skills.extend(category_skills)
        elif 'skills' in resume_analysis:  # Fallback to older format
            for category_skills in resume_analysis['skills'].values():
                skills.extend(category_skills)
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from job description text"""
        skills = []
        
        # Common tech skills to look for
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'django', 'flask', 'spring', 'aws', 'azure', 'docker', 'kubernetes',
            'sql', 'postgresql', 'mongodb', 'redis', 'git', 'ci/cd', 'agile',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'data science',
            'html', 'css', 'typescript', 'graphql', 'rest api', 'microservices'
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill in text_lower:
                skills.append(skill)
        
        return skills
    
    def _generate_insights(self, resume_analysis: Dict[str, Any], scored_jobs: List[Dict]) -> Dict[str, Any]:
        """Generate insights about job market and recommendations"""
        
        insights = {
            'total_matches': len(scored_jobs),
            'average_score': np.mean([job['score'] for job in scored_jobs]) if scored_jobs else 0,
            'top_skills_demanded': {},
            'experience_level_distribution': {},
            'salary_insights': {},
            'recommendations': []
        }
        
        if not scored_jobs:
            return insights
        
        # Analyze top skills demanded
        all_job_skills = []
        for job_data in scored_jobs:
            all_job_skills.extend(job_data['job'].skills)
        
        from collections import Counter
        skill_counter = Counter(all_job_skills)
        insights['top_skills_demanded'] = dict(skill_counter.most_common(10))
        
        # Experience level distribution
        exp_levels = [job_data['job'].experience_level for job_data in scored_jobs]
        exp_counter = Counter(exp_levels)
        insights['experience_level_distribution'] = dict(exp_counter)
        
        # Generate recommendations
        user_skills = self._extract_user_skills(resume_analysis)
        missing_skills = set(insights['top_skills_demanded'].keys()) - set([s.lower() for s in user_skills])
        
        if missing_skills:
            insights['recommendations'].append(
                f"Consider learning {', '.join(list(missing_skills)[:3])} to increase your job match rate"
            )
        
        if insights['average_score'] < 0.6:
            insights['recommendations'].append(
                "Your current profile matches {:.1f}% of jobs. Consider updating your resume with more relevant keywords"
                .format(insights['average_score'] * 100)
            )
        
        return insights
    
    def _generate_application_assistance(self, top_jobs: List[Dict]) -> Dict[str, Any]:
        """Generate assistance for job applications"""
        
        assistance = {
            'cover_letter_tips': [],
            'interview_preparation': [],
            'application_checklist': [],
            'custom_applications': []
        }
        
        if not top_jobs:
            return assistance
        
        # General tips
        assistance['cover_letter_tips'] = [
            "Highlight skills that match the job requirements",
            "Mention specific achievements with quantifiable results",
            "Research the company and mention why you want to work there",
            "Keep it concise and professional"
        ]
        
        assistance['interview_preparation'] = [
            "Review the job description and prepare examples for each requirement",
            "Research the company's recent news and developments",
            "Prepare questions about the role and company culture",
            "Practice coding challenges if it's a technical role"
        ]
        
        assistance['application_checklist'] = [
            "✓ Tailor resume to job requirements",
            "✓ Write personalized cover letter",
            "✓ Update LinkedIn profile",
            "✓ Prepare portfolio/work samples",
            "✓ Research company and interviewer"
        ]
        
        # Custom applications for top jobs
        for i, job_data in enumerate(top_jobs[:3]):
            job = job_data['job']
            custom_app = {
                'job_title': job.title,
                'company': job.company,
                'key_points_to_highlight': [],
                'questions_to_ask': [],
                'application_url': job.apply_url
            }
            
            # Generate key points based on job requirements
            if job.skills:
                custom_app['key_points_to_highlight'] = [
                    f"Emphasize your experience with {', '.join(job.skills[:3])}",
                    f"Highlight projects that demonstrate {job.experience_level} level expertise"
                ]
            
            custom_app['questions_to_ask'] = [
                f"What does a typical day look like for this {job.title} role?",
                "What are the biggest challenges the team is currently facing?",
                "What opportunities are there for professional development?"
            ]
            
            assistance['custom_applications'].append(custom_app)
        
        return assistance
    
    def _analyze_job_market(self, jobs: List[JobPosting]) -> Dict[str, Any]:
        """Analyze the job market trends"""
        if not jobs:
            return {}
        
        # Get trending skills
        trending_skills = self.job_scraper.get_trending_skills(jobs)
        
        # Salary insights
        salary_insights = self.job_scraper.get_salary_insights(jobs)
        
        # Location analysis
        locations = [job.location for job in jobs if job.location != 'Not specified']
        from collections import Counter
        location_counter = Counter(locations)
        
        return {
            'trending_skills': trending_skills,
            'salary_insights': salary_insights,
            'top_locations': dict(location_counter.most_common(10)),
            'total_jobs_analyzed': len(jobs),
            'job_sources': list(set([job.source for job in jobs]))
        }
    
    def _identify_skill_gaps(self, resume_analysis: Dict[str, Any], jobs: List[JobPosting]) -> Dict[str, Any]:
        """Identify skill gaps based on job market demand"""
        user_skills = set([s.lower() for s in self._extract_user_skills(resume_analysis)])
        
        # Get all skills from jobs
        market_skills = set()
        for job in jobs:
            market_skills.update([s.lower() for s in job.skills])
            market_skills.update([s.lower() for s in self._extract_skills_from_text(job.description)])
        
        # Calculate gaps
        skill_gaps = market_skills - user_skills
        
        # Prioritize gaps by frequency in job postings
        gap_frequency = {}
        for job in jobs:
            job_skills_lower = [s.lower() for s in job.skills + self._extract_skills_from_text(job.description)]
            for gap_skill in skill_gaps:
                if gap_skill in job_skills_lower:
                    gap_frequency[gap_skill] = gap_frequency.get(gap_skill, 0) + 1
        
        # Sort by frequency
        prioritized_gaps = sorted(gap_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'critical_gaps': prioritized_gaps[:5],
            'nice_to_have': prioritized_gaps[5:10],
            'learning_recommendations': self._generate_learning_recommendations(prioritized_gaps[:5])
        }
    
    def _suggest_career_paths(self, resume_analysis: Dict[str, Any], jobs: List[JobPosting]) -> List[Dict[str, Any]]:
        """Suggest potential career paths based on current skills and market demand"""
        user_skills = self._extract_user_skills(resume_analysis)
        current_level = resume_analysis.get('experience', {}).get('primary_level', 'mid')
        
        # Define career progression paths
        career_paths = [
            {
                'path': 'Full Stack Developer → Senior Developer → Tech Lead',
                'required_skills': ['javascript', 'react', 'node', 'database', 'aws'],
                'timeline': '2-5 years',
                'growth_potential': 'High'
            },
            {
                'path': 'Data Analyst → Data Scientist → Senior Data Scientist',
                'required_skills': ['python', 'sql', 'machine learning', 'statistics', 'visualization'],
                'timeline': '3-6 years',
                'growth_potential': 'Very High'
            },
            {
                'path': 'DevOps Engineer → Senior DevOps → Platform Architect',
                'required_skills': ['docker', 'kubernetes', 'aws', 'terraform', 'monitoring'],
                'timeline': '3-7 years',
                'growth_potential': 'High'
            }
        ]
        
        # Score each path based on user's current skills
        scored_paths = []
        for path in career_paths:
            skill_match = len(set([s.lower() for s in user_skills]) & 
                            set([s.lower() for s in path['required_skills']]))
            match_percentage = skill_match / len(path['required_skills'])
            
            scored_paths.append({
                **path,
                'current_match': f"{match_percentage:.1%}",
                'missing_skills': list(set(path['required_skills']) - 
                                     set([s.lower() for s in user_skills]))
            })
        
        return sorted(scored_paths, key=lambda x: float(x['current_match'].strip('%')), reverse=True)
    
    def _generate_learning_recommendations(self, skill_gaps: List[Tuple[str, int]]) -> List[Dict[str, Any]]:
        """Generate learning recommendations for skill gaps"""
        recommendations = []
        
        learning_resources = {
            'python': {
                'courses': ['Python for Everybody (Coursera)', 'Automate the Boring Stuff'],
                'practice': ['LeetCode', 'HackerRank'],
                'time_estimate': '2-3 months'
            },
            'react': {
                'courses': ['React Documentation', 'The Complete React Course'],
                'practice': ['Build a portfolio project', 'Contribute to open source'],
                'time_estimate': '1-2 months'
            },
            'aws': {
                'courses': ['AWS Cloud Practitioner', 'A Cloud Guru'],
                'practice': ['AWS Free Tier projects', 'Build a serverless app'],
                'time_estimate': '3-4 months'
            },
            'machine learning': {
                'courses': ['Andrew Ng ML Course', 'Fast.ai'],
                'practice': ['Kaggle competitions', 'Personal ML projects'],
                'time_estimate': '4-6 months'
            }
        }
        
        for skill, frequency in skill_gaps[:5]:
            resource = learning_resources.get(skill, {
                'courses': [f'Search for {skill} courses on Coursera/Udemy'],
                'practice': [f'Build projects using {skill}'],
                'time_estimate': '1-3 months'
            })
            
            recommendations.append({
                'skill': skill,
                'demand_frequency': frequency,
                'priority': 'High' if frequency > 5 else 'Medium',
                'learning_resources': resource
            })
        
        return recommendations
    
    def _generate_recommendation_reason(self, scores: Dict[str, float], job: JobPosting) -> str:
        """Generate a human-readable reason for job recommendation"""
        reasons = []
        
        if scores['skill_match'] > 0.7:
            reasons.append("Strong skill match")
        
        if scores['experience_match'] > 0.8:
            reasons.append("Perfect experience level fit")
        
        if scores['semantic_similarity'] > 0.7:
            reasons.append("High content relevance")
        
        if not reasons:
            reasons.append("Good overall compatibility")
        
        return f"Recommended because: {', '.join(reasons)}"
    
    def _get_fallback_jobs(self, skills: List[str], experience_level: str) -> List[JobPosting]:
        """Get fallback jobs when real-time scraping fails"""
        # Return some sample jobs as fallback
        return [
            JobPosting(
                id="fallback_1",
                title=f"Senior {skills[0].title()} Developer" if skills else "Software Developer",
                company="Tech Solutions Inc.",
                location="Remote",
                description=f"We are looking for a skilled developer with experience in {', '.join(skills[:3]) if skills else 'programming'}.",
                requirements=[f"Experience with {skill}" for skill in skills[:3]] if skills else ["Programming experience"],
                salary_range="$80,000 - $120,000",
                experience_level=experience_level,
                job_type="Full Time",
                posted_date=datetime.now().isoformat(),
                source="Fallback",
                apply_url="https://example.com/apply",
                skills=skills[:5] if skills else ["programming"]
            )
        ]
