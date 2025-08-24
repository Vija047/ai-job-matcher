"""
AI-Powered Job Matching Engine
Uses Hugging Face models to match resumes with job postings
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import logging
from dataclasses import asdict
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline
import asyncio

from job_api_client import JobAPIClient, JobPosting
from advanced_resume_parser import AdvancedResumeParser

logger = logging.getLogger(__name__)

class AIJobMatcher:
    """
    Advanced job matching using AI models and semantic analysis
    """
    
    def __init__(self):
        print("🚀 Initializing AI Job Matcher...")
        
        # Initialize components
        self.job_client = JobAPIClient()
        self.resume_parser = AdvancedResumeParser()
        
        # Initialize ML models
        self._init_models()
        
        # Matching weights
        self.matching_weights = {
            'skills_semantic': 0.3,
            'skills_keyword': 0.2,
            'experience_level': 0.2,
            'job_description': 0.15,
            'location': 0.05,
            'salary': 0.05,
            'company_preference': 0.05
        }
        
        print("✅ AI Job Matcher initialized successfully!")
    
    def _init_models(self):
        """Initialize AI models for matching"""
        try:
            # Sentence transformer for semantic similarity
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Text classifier for job categorization
            self.job_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1
            )
            
            # TF-IDF vectorizer for keyword matching
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            logger.info("✅ AI models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading AI models: {e}")
            self.sentence_model = None
            self.job_classifier = None
            self.tfidf_vectorizer = None
    
    async def find_matching_jobs(self, 
                                resume_analysis: Dict[str, Any],
                                preferences: Dict[str, Any] = None,
                                limit: int = 20) -> Dict[str, Any]:
        """
        Find matching jobs for a parsed resume
        """
        try:
            preferences = preferences or {}
            
            # Extract search keywords from resume
            keywords = self._extract_search_keywords(resume_analysis)
            
            # Search for jobs
            logger.info(f"Searching jobs with keywords: {keywords}")
            jobs = await self.job_client.search_jobs(
                keywords=keywords,
                location=preferences.get('location', ''),
                experience_level=resume_analysis.get('experience_analysis', {}).get('experience_level', ''),
                employment_type=preferences.get('employment_type', ''),
                salary_min=preferences.get('salary_min'),
                limit=limit * 2  # Get more jobs for better filtering
            )
            
            if not jobs:
                return {
                    'matches': [],
                    'total_found': 0,
                    'search_keywords': keywords,
                    'message': 'No jobs found matching your criteria'
                }
            
            # Calculate match scores
            scored_jobs = self._calculate_match_scores(resume_analysis, jobs, preferences)
            
            # Sort by score and limit results
            top_matches = sorted(scored_jobs, key=lambda x: x['match_score'], reverse=True)[:limit]
            
            # Generate insights
            insights = self._generate_matching_insights(resume_analysis, top_matches)
            
            return {
                'matches': top_matches,
                'total_found': len(jobs),
                'search_keywords': keywords,
                'insights': insights,
                'statistics': self.job_client.get_job_statistics(jobs),
                'message': f'Found {len(top_matches)} highly matched jobs'
            }
            
        except Exception as e:
            logger.error(f"Job matching error: {e}")
            return {
                'matches': [],
                'total_found': 0,
                'error': f'Job matching failed: {str(e)}'
            }
    
    def _extract_search_keywords(self, resume_analysis: Dict[str, Any]) -> List[str]:
        """Extract relevant keywords for job search"""
        keywords = []
        
        # Add skills
        skills_analysis = resume_analysis.get('skills_analysis', {})
        all_skills = skills_analysis.get('all_skills', [])
        keywords.extend(all_skills[:10])  # Top 10 skills
        
        # Add job titles
        experience = resume_analysis.get('experience_analysis', {})
        job_titles = experience.get('job_titles', [])
        keywords.extend(job_titles[:3])  # Top 3 job titles
        
        # Add trending skills with higher priority
        trending_skills = skills_analysis.get('trending_skills', [])
        keywords.extend(trending_skills)
        
        # Remove duplicates and clean
        keywords = list(set([kw.strip().lower() for kw in keywords if kw and len(kw) > 2]))
        
        # If no keywords found, use defaults
        if not keywords:
            keywords = ['software', 'developer', 'engineer']
        
        return keywords[:15]  # Limit to 15 keywords
    
    def _calculate_match_scores(self, 
                              resume_analysis: Dict[str, Any], 
                              jobs: List[JobPosting],
                              preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate comprehensive match scores for jobs"""
        scored_jobs = []
        
        # Prepare resume data
        resume_skills = set(skill.lower() for skill in resume_analysis.get('skills_analysis', {}).get('all_skills', []))
        resume_experience_level = resume_analysis.get('experience_analysis', {}).get('experience_level', 'mid')
        resume_text = self._create_resume_summary_text(resume_analysis)
        
        for job in jobs:
            try:
                scores = {}
                
                # 1. Skills semantic similarity
                if self.sentence_model:
                    job_text = f"{job.title} {job.description} {' '.join(job.skills)}"
                    scores['skills_semantic'] = self._calculate_semantic_similarity(resume_text, job_text)
                else:
                    scores['skills_semantic'] = 0.5
                
                # 2. Skills keyword matching
                job_skills = set(skill.lower() for skill in job.skills)
                if resume_skills and job_skills:
                    skill_overlap = len(resume_skills.intersection(job_skills))
                    scores['skills_keyword'] = skill_overlap / max(len(resume_skills), len(job_skills))
                else:
                    scores['skills_keyword'] = 0.3
                
                # 3. Experience level matching
                scores['experience_level'] = self._calculate_experience_match(resume_experience_level, job.experience_level)
                
                # 4. Job description relevance
                scores['job_description'] = self._calculate_description_relevance(resume_analysis, job.description)
                
                # 5. Location matching
                scores['location'] = self._calculate_location_match(preferences.get('preferred_location', ''), job.location)
                
                # 6. Salary matching
                scores['salary'] = self._calculate_salary_match(preferences.get('salary_min'), job.salary_min, job.salary_max)
                
                # 7. Company preference (if specified)
                scores['company_preference'] = self._calculate_company_preference(preferences.get('preferred_companies', []), job.company)
                
                # Calculate weighted overall score
                overall_score = sum(
                    scores[factor] * self.matching_weights[factor]
                    for factor in scores
                )
                
                # Create job match result
                job_match = {
                    'job': asdict(job),
                    'match_score': round(overall_score, 3),
                    'score_breakdown': scores,
                    'match_reasons': self._generate_match_reasons(scores, job),
                    'skill_overlap': list(resume_skills.intersection(set(skill.lower() for skill in job.skills))),
                    'missing_skills': list(set(skill.lower() for skill in job.skills) - resume_skills),
                    'recommendation': self._generate_job_recommendation(overall_score, scores)
                }
                
                scored_jobs.append(job_match)
                
            except Exception as e:
                logger.error(f"Error scoring job {job.id}: {e}")
                continue
        
        return scored_jobs
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        try:
            if not self.sentence_model:
                return 0.5
            
            embeddings = self.sentence_model.encode([text1, text2])
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(similarity)
        except:
            return 0.5
    
    def _calculate_experience_match(self, resume_level: str, job_level: str) -> float:
        """Calculate experience level matching score"""
        level_hierarchy = {
            'entry': 1,
            'mid': 2,
            'senior': 3,
            'executive': 4
        }
        
        resume_rank = level_hierarchy.get(resume_level, 2)
        job_rank = level_hierarchy.get(job_level, 2)
        
        # Perfect match
        if resume_rank == job_rank:
            return 1.0
        
        # Adjacent levels
        if abs(resume_rank - job_rank) == 1:
            return 0.7
        
        # Two levels apart
        if abs(resume_rank - job_rank) == 2:
            return 0.4
        
        # Three or more levels apart
        return 0.1
    
    def _calculate_description_relevance(self, resume_analysis: Dict, job_description: str) -> float:
        """Calculate how relevant the job description is to the resume"""
        try:
            # Extract key terms from resume
            resume_terms = []
            
            # Add skills
            skills = resume_analysis.get('skills_analysis', {}).get('all_skills', [])
            resume_terms.extend(skills)
            
            # Add job titles
            job_titles = resume_analysis.get('experience_analysis', {}).get('job_titles', [])
            resume_terms.extend(job_titles)
            
            # Add achievements keywords
            achievements = resume_analysis.get('experience_analysis', {}).get('key_achievements', [])
            for achievement in achievements:
                resume_terms.extend(achievement.split()[:5])  # First 5 words of each achievement
            
            if not resume_terms:
                return 0.5
            
            # Count matches in job description
            job_desc_lower = job_description.lower()
            matches = sum(1 for term in resume_terms if term.lower() in job_desc_lower)
            
            return min(matches / len(resume_terms), 1.0)
            
        except:
            return 0.5
    
    def _calculate_location_match(self, preferred_location: str, job_location: str) -> float:
        """Calculate location matching score"""
        if not preferred_location:
            return 1.0  # No preference specified
        
        if 'remote' in job_location.lower():
            return 1.0  # Remote jobs match any preference
        
        if preferred_location.lower() in job_location.lower():
            return 1.0
        
        # Check for city/state matches
        pref_parts = preferred_location.lower().split(',')
        job_parts = job_location.lower().split(',')
        
        for pref_part in pref_parts:
            for job_part in job_parts:
                if pref_part.strip() in job_part.strip():
                    return 0.8
        
        return 0.3  # Different location
    
    def _calculate_salary_match(self, preferred_min: Optional[int], job_min: Optional[float], job_max: Optional[float]) -> float:
        """Calculate salary matching score"""
        if not preferred_min:
            return 1.0  # No salary preference
        
        if not job_min and not job_max:
            return 0.7  # Salary not specified in job
        
        if job_min and job_min >= preferred_min:
            return 1.0  # Meets minimum requirement
        
        if job_max and job_max >= preferred_min:
            return 0.8  # Max salary meets requirement
        
        if job_min and job_min >= preferred_min * 0.8:
            return 0.6  # Close to requirement
        
        return 0.3  # Below requirement
    
    def _calculate_company_preference(self, preferred_companies: List[str], job_company: str) -> float:
        """Calculate company preference score"""
        if not preferred_companies:
            return 1.0  # No preference specified
        
        for pref_company in preferred_companies:
            if pref_company.lower() in job_company.lower():
                return 1.0
        
        return 0.5  # Not a preferred company
    
    def _create_resume_summary_text(self, resume_analysis: Dict[str, Any]) -> str:
        """Create a summary text representation of the resume"""
        parts = []
        
        # Add summary
        summary = resume_analysis.get('summary', '')
        if summary:
            parts.append(summary)
        
        # Add skills
        skills = resume_analysis.get('skills_analysis', {}).get('all_skills', [])
        if skills:
            parts.append(f"Skills: {', '.join(skills[:15])}")
        
        # Add experience
        experience = resume_analysis.get('experience_analysis', {})
        if experience.get('job_titles'):
            parts.append(f"Experience: {', '.join(experience['job_titles'][:3])}")
        
        return ' '.join(parts)
    
    def _generate_match_reasons(self, scores: Dict[str, float], job: JobPosting) -> List[str]:
        """Generate human-readable reasons for the match"""
        reasons = []
        
        if scores['skills_keyword'] > 0.6:
            reasons.append(f"Strong skill match with {job.title}")
        
        if scores['experience_level'] > 0.8:
            reasons.append(f"Perfect experience level fit for {job.experience_level} role")
        
        if scores['skills_semantic'] > 0.7:
            reasons.append("High semantic similarity with job requirements")
        
        if scores['location'] > 0.9:
            reasons.append("Excellent location match")
        
        if scores['salary'] > 0.8:
            reasons.append("Salary meets your requirements")
        
        if len(reasons) == 0:
            reasons.append("General profile alignment with job requirements")
        
        return reasons
    
    def _generate_job_recommendation(self, overall_score: float, scores: Dict[str, float]) -> str:
        """Generate a recommendation for the job"""
        if overall_score > 0.8:
            return "Highly Recommended - Excellent match for your profile"
        elif overall_score > 0.6:
            return "Recommended - Good fit with some skill development opportunities"
        elif overall_score > 0.4:
            return "Consider - May require additional skill development"
        else:
            return "Low Match - Significant skill gap or requirements mismatch"
    
    def _generate_matching_insights(self, resume_analysis: Dict[str, Any], matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights about the matching results"""
        if not matches:
            return {}
        
        insights = {
            'average_match_score': sum(match['match_score'] for match in matches) / len(matches),
            'top_scoring_companies': [],
            'common_required_skills': [],
            'skill_gaps': [],
            'salary_insights': {},
            'location_insights': {},
            'recommendations': []
        }
        
        # Top scoring companies
        company_scores = {}
        for match in matches:
            company = match['job']['company']
            if company not in company_scores:
                company_scores[company] = []
            company_scores[company].append(match['match_score'])
        
        for company, scores in company_scores.items():
            avg_score = sum(scores) / len(scores)
            company_scores[company] = avg_score
        
        insights['top_scoring_companies'] = sorted(
            company_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Common required skills
        all_job_skills = []
        for match in matches:
            all_job_skills.extend(match['job']['skills'])
        
        skill_frequency = {}
        for skill in all_job_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        insights['common_required_skills'] = sorted(
            skill_frequency.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Skill gaps
        user_skills = set(skill.lower() for skill in resume_analysis.get('skills_analysis', {}).get('all_skills', []))
        missing_skills_freq = {}
        
        for match in matches:
            for missing_skill in match['missing_skills']:
                if missing_skill not in user_skills:
                    missing_skills_freq[missing_skill] = missing_skills_freq.get(missing_skill, 0) + 1
        
        insights['skill_gaps'] = sorted(
            missing_skills_freq.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        # Salary insights
        salaries = [match['job']['salary_min'] for match in matches if match['job']['salary_min']]
        if salaries:
            insights['salary_insights'] = {
                'average': sum(salaries) / len(salaries),
                'min': min(salaries),
                'max': max(salaries)
            }
        
        # Generate recommendations
        recommendations = []
        
        if insights['average_match_score'] < 0.6:
            recommendations.append("Consider developing skills in high-demand areas")
        
        if insights['skill_gaps']:
            top_gap = insights['skill_gaps'][0][0]
            recommendations.append(f"Learning {top_gap} could significantly improve your job matches")
        
        if insights['salary_insights']:
            avg_salary = insights['salary_insights']['average']
            recommendations.append(f"Average salary for matching positions: ${avg_salary:,.0f}")
        
        insights['recommendations'] = recommendations
        
        return insights

# Synchronous wrapper function
def find_matching_jobs_sync(resume_analysis: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """Synchronous wrapper for job matching"""
    matcher = AIJobMatcher()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(matcher.find_matching_jobs(resume_analysis, **kwargs))
    finally:
        loop.close()
