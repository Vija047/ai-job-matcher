"""
Role-Based Job Recommender
Enhanced job matching based on role analysis with internship support
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import numpy as np
from collections import defaultdict
from urllib.parse import quote

logger = logging.getLogger(__name__)

class RoleBasedRecommender:
    """
    Advanced role-based job recommendation system
    Analyzes user's role fit and recommends both jobs and internships
    """
    
    def __init__(self):
        self.role_patterns = {
            # Software Engineering Roles
            'Software Engineer': ['python', 'javascript', 'java', 'react', 'node.js', 'git', 'sql'],
            'Frontend Developer': ['react', 'vue', 'angular', 'javascript', 'html', 'css', 'typescript'],
            'Backend Developer': ['python', 'java', 'node.js', 'sql', 'api', 'microservices', 'database'],
            'Full Stack Developer': ['react', 'node.js', 'python', 'javascript', 'sql', 'mongodb', 'api'],
            'DevOps Engineer': ['docker', 'kubernetes', 'aws', 'jenkins', 'terraform', 'ci/cd', 'linux'],
            'Mobile Developer': ['react native', 'flutter', 'swift', 'kotlin', 'android', 'ios'],
            
            # Data & AI Roles
            'Data Scientist': ['python', 'machine learning', 'pandas', 'numpy', 'tensorflow', 'sql', 'statistics'],
            'Data Analyst': ['sql', 'python', 'excel', 'tableau', 'power bi', 'statistics', 'data visualization'],
            'Machine Learning Engineer': ['python', 'tensorflow', 'pytorch', 'machine learning', 'aws', 'docker'],
            'AI Engineer': ['python', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow'],
            
            # Cloud & Infrastructure
            'Cloud Architect': ['aws', 'azure', 'gcp', 'terraform', 'kubernetes', 'microservices', 'devops'],
            'System Administrator': ['linux', 'windows', 'networking', 'security', 'monitoring', 'scripting'],
            'Security Engineer': ['cybersecurity', 'penetration testing', 'security', 'compliance', 'firewall'],
            
            # Management & Leadership
            'Technical Lead': ['leadership', 'architecture', 'mentoring', 'project management', 'agile', 'scrum'],
            'Engineering Manager': ['management', 'leadership', 'team lead', 'project management', 'strategy'],
            'Product Manager': ['product management', 'agile', 'scrum', 'roadmap', 'stakeholder', 'analytics'],
            
            # Quality & Testing
            'QA Engineer': ['testing', 'automation', 'selenium', 'cypress', 'quality assurance', 'bug tracking'],
            'Test Automation Engineer': ['selenium', 'cypress', 'automation', 'testing', 'ci/cd', 'python'],
            
            # Specialized Roles
            'Business Analyst': ['business analysis', 'requirements', 'documentation', 'stakeholder', 'process'],
            'UI/UX Designer': ['ui design', 'ux design', 'figma', 'sketch', 'prototyping', 'user research'],
            'Database Administrator': ['sql', 'database', 'mysql', 'postgresql', 'oracle', 'performance tuning'],
        }
        
        # Experience level mapping for different role types
        self.experience_levels = {
            'entry': ['junior', 'entry', 'graduate', 'trainee', 'intern'],
            'mid': ['mid', 'intermediate', 'associate', 'regular'],
            'senior': ['senior', 'lead', 'principal', 'expert'],
            'executive': ['manager', 'director', 'head', 'vp', 'chief']
        }
        
        # Internship keywords
        self.internship_keywords = [
            'intern', 'internship', 'trainee', 'graduate program', 
            'entry level', 'junior', 'apprentice', 'co-op', 'coop'
        ]
        
    def analyze_role_compatibility(self, resume_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze role compatibility based on resume analysis
        Returns detailed role analysis with primary and alternative roles
        """
        try:
            # Extract relevant data from resume analysis
            skills_analysis = resume_analysis.get('skills_analysis', {})
            experience_analysis = resume_analysis.get('experience_analysis', {})
            role_suggestion = resume_analysis.get('role_suggestion', {})
            
            all_skills = skills_analysis.get('all_skills', [])
            experience_level = experience_analysis.get('experience_level', 'mid')
            years_experience = experience_analysis.get('total_years', 0)
            
            # Calculate role compatibility scores
            role_scores = self._calculate_role_scores(all_skills, experience_level)
            
            # Determine career stage
            career_stage = self._determine_career_stage(years_experience, experience_level)
            
            # Get role recommendations
            primary_role = role_suggestion.get('primary_role', 'Software Engineer')
            alternative_roles = role_suggestion.get('alternative_roles', [])
            
            # Enhanced role analysis
            role_analysis = {
                'primary_role': primary_role,
                'alternative_roles': alternative_roles[:5],  # Top 5 alternatives
                'role_scores': role_scores,
                'career_stage': career_stage,
                'experience_level': experience_level,
                'years_experience': years_experience,
                'suitable_for_internships': career_stage in ['entry', 'student'] or years_experience < 2,
                'skill_match_strength': self._calculate_skill_strength(all_skills),
                'recommended_job_types': self._get_recommended_job_types(career_stage, experience_level),
                'growth_potential': self._assess_growth_potential(role_scores, career_stage)
            }
            
            return role_analysis
            
        except Exception as e:
            logger.error(f"Role compatibility analysis error: {e}")
            return {
                'primary_role': 'Software Engineer',
                'alternative_roles': [],
                'role_scores': {},
                'career_stage': 'mid',
                'experience_level': 'mid',
                'years_experience': 0,
                'suitable_for_internships': False,
                'skill_match_strength': 'moderate',
                'recommended_job_types': ['Full Time'],
                'growth_potential': 'moderate'
            }
    
    def get_role_based_recommendations(self, role_analysis: Dict[str, Any], 
                                     available_jobs: List[Dict], 
                                     preferences: Dict = None) -> Dict[str, Any]:
        """
        Get job recommendations based on role analysis
        Includes both jobs and internships based on career stage with apply options
        """
        try:
            preferences = preferences or {}
            primary_role = role_analysis.get('primary_role', '')
            alternative_roles = role_analysis.get('alternative_roles', [])
            career_stage = role_analysis.get('career_stage', 'mid')
            suitable_for_internships = role_analysis.get('suitable_for_internships', False)
            
            # Categorize jobs
            categorized_jobs = self._categorize_jobs(available_jobs)
            
            # Get role-matched jobs
            matched_jobs = []
            internships = []
            
            # Match primary role
            primary_matches = self._match_jobs_to_role(
                primary_role, categorized_jobs['jobs'], role_analysis
            )
            matched_jobs.extend(primary_matches)
            
            # Match alternative roles
            for alt_role in alternative_roles[:3]:  # Top 3 alternatives
                alt_matches = self._match_jobs_to_role(
                    alt_role, categorized_jobs['jobs'], role_analysis, is_alternative=True
                )
                matched_jobs.extend(alt_matches)
            
            # Get internships if suitable
            if suitable_for_internships:
                internship_matches = self._match_internships(
                    primary_role, alternative_roles, categorized_jobs['internships'], role_analysis
                )
                internships.extend(internship_matches)
            
            # Remove duplicates and sort by compatibility
            unique_jobs = self._remove_duplicates_and_sort(matched_jobs)
            unique_internships = self._remove_duplicates_and_sort(internships)
            
            # Apply preferences filter
            filtered_jobs = self._apply_preferences_filter(unique_jobs, preferences)
            filtered_internships = self._apply_preferences_filter(unique_internships, preferences)
            
            # Add apply options to jobs
            filtered_jobs = self._add_apply_options(filtered_jobs)
            filtered_internships = self._add_apply_options(filtered_internships)
            
            # Limit results
            max_jobs = preferences.get('limit', 20)
            final_jobs = filtered_jobs[:max_jobs]
            final_internships = filtered_internships[:10]  # Max 10 internships
            
            return {
                'success': True,
                'role_analysis': role_analysis,
                'jobs': final_jobs,
                'internships': final_internships,
                'total_jobs_found': len(final_jobs),
                'total_internships_found': len(final_internships),
                'categories': {
                    'primary_role_matches': len([j for j in final_jobs if j.get('match_type') == 'primary']),
                    'alternative_role_matches': len([j for j in final_jobs if j.get('match_type') == 'alternative']),
                    'skill_based_matches': len([j for j in final_jobs if j.get('match_type') == 'skill'])
                },
                'recommendations_metadata': {
                    'search_timestamp': datetime.now().isoformat(),
                    'primary_role': primary_role,
                    'career_stage': career_stage,
                    'includes_internships': suitable_for_internships
                },
                'quick_apply_available': True,
                'apply_options': {
                    'bulk_apply': {
                        'available': True,
                        'max_applications': 5,
                        'description': 'Apply to multiple positions at once'
                    },
                    'saved_applications': {
                        'available': True,
                        'description': 'Save applications as drafts for later'
                    },
                    'application_tracking': {
                        'available': True,
                        'description': 'Track your application status'
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Role-based recommendation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'jobs': [],
                'internships': [],
                'total_jobs_found': 0,
                'total_internships_found': 0
            }
    
    def _calculate_role_scores(self, user_skills: List[str], experience_level: str) -> Dict[str, float]:
        """Calculate compatibility scores for different roles"""
        role_scores = {}
        user_skills_lower = [skill.lower() for skill in user_skills]
        
        for role, required_skills in self.role_patterns.items():
            score = 0
            matched_skills = 0
            
            for req_skill in required_skills:
                for user_skill in user_skills_lower:
                    if req_skill in user_skill or user_skill in req_skill:
                        score += 1
                        matched_skills += 1
                        break
            
            # Normalize score (0-1)
            normalized_score = score / len(required_skills) if required_skills else 0
            
            # Adjust based on experience level
            if experience_level == 'entry' and 'junior' not in role.lower():
                normalized_score *= 0.8
            elif experience_level == 'senior' and 'senior' not in role.lower():
                normalized_score *= 1.2
            
            role_scores[role] = round(normalized_score, 3)
        
        return role_scores
    
    def _determine_career_stage(self, years_experience: int, experience_level: str) -> str:
        """Determine career stage based on experience"""
        if years_experience == 0 or experience_level == 'entry':
            return 'entry'
        elif years_experience <= 2:
            return 'early_career'
        elif years_experience <= 5:
            return 'mid_career'
        elif years_experience <= 10:
            return 'senior'
        else:
            return 'executive'
    
    def _calculate_skill_strength(self, skills: List[str]) -> str:
        """Assess overall skill strength"""
        skill_count = len(skills)
        if skill_count >= 15:
            return 'strong'
        elif skill_count >= 8:
            return 'moderate'
        else:
            return 'developing'
    
    def _get_recommended_job_types(self, career_stage: str, experience_level: str) -> List[str]:
        """Get recommended job types based on career stage"""
        if career_stage in ['entry', 'early_career']:
            return ['Full Time', 'Internship', 'Contract', 'Part Time']
        elif career_stage == 'mid_career':
            return ['Full Time', 'Contract', 'Remote']
        else:
            return ['Full Time', 'Contract', 'Remote', 'Consulting']
    
    def _assess_growth_potential(self, role_scores: Dict[str, float], career_stage: str) -> str:
        """Assess growth potential based on role scores and career stage"""
        max_score = max(role_scores.values()) if role_scores else 0
        
        if max_score >= 0.8 and career_stage in ['entry', 'early_career']:
            return 'high'
        elif max_score >= 0.6:
            return 'moderate'
        else:
            return 'developing'
    
    def _categorize_jobs(self, jobs: List[Dict]) -> Dict[str, List]:
        """Categorize jobs into regular jobs and internships"""
        regular_jobs = []
        internships = []
        
        for job in jobs:
            job_title = job.get('title', '').lower()
            job_description = job.get('description', '').lower()
            job_type = job.get('employment_type', '').lower()
            
            # Check if it's an internship
            is_internship = any(keyword in job_title or keyword in job_description 
                              for keyword in self.internship_keywords)
            
            if is_internship or job_type == 'internship':
                internships.append(job)
            else:
                regular_jobs.append(job)
        
        return {'jobs': regular_jobs, 'internships': internships}
    
    def _match_jobs_to_role(self, role: str, jobs: List[Dict], 
                           role_analysis: Dict, is_alternative: bool = False) -> List[Dict]:
        """Match jobs to a specific role"""
        matched_jobs = []
        role_keywords = self.role_patterns.get(role, [])
        
        for job in jobs:
            compatibility_score = self._calculate_job_compatibility(job, role_keywords, role_analysis)
            
            if compatibility_score > 0.3:  # Minimum threshold
                job_copy = job.copy()
                job_copy['compatibility_score'] = compatibility_score
                job_copy['matched_role'] = role
                job_copy['match_type'] = 'alternative' if is_alternative else 'primary'
                matched_jobs.append(job_copy)
        
        return matched_jobs
    
    def _match_internships(self, primary_role: str, alternative_roles: List[str], 
                          internships: List[Dict], role_analysis: Dict) -> List[Dict]:
        """Match internships based on roles"""
        matched_internships = []
        all_roles = [primary_role] + alternative_roles[:3]
        
        for internship in internships:
            best_score = 0
            best_role = primary_role
            
            for role in all_roles:
                role_keywords = self.role_patterns.get(role, [])
                score = self._calculate_job_compatibility(internship, role_keywords, role_analysis)
                
                if score > best_score:
                    best_score = score
                    best_role = role
            
            if best_score > 0.2:  # Lower threshold for internships
                internship_copy = internship.copy()
                internship_copy['compatibility_score'] = best_score
                internship_copy['matched_role'] = best_role
                internship_copy['match_type'] = 'internship'
                internship_copy['job_type'] = 'Internship'
                matched_internships.append(internship_copy)
        
        return matched_internships
    
    def _calculate_job_compatibility(self, job: Dict, role_keywords: List[str], 
                                   role_analysis: Dict) -> float:
        """Calculate compatibility score between job and role"""
        job_text = f"{job.get('title', '')} {job.get('description', '')} {job.get('requirements', '')}"
        job_text_lower = job_text.lower()
        
        # Keyword matching score
        keyword_matches = sum(1 for keyword in role_keywords if keyword in job_text_lower)
        keyword_score = keyword_matches / len(role_keywords) if role_keywords else 0
        
        # Skills matching score
        job_skills = job.get('skills', [])
        if job_skills:
            skill_matches = 0
            for skill in job_skills:
                if any(keyword in skill.lower() for keyword in role_keywords):
                    skill_matches += 1
            skill_score = skill_matches / len(job_skills)
        else:
            skill_score = 0
        
        # Experience level matching
        experience_level = role_analysis.get('experience_level', 'mid')
        job_experience = job.get('experience_level', '').lower()
        
        experience_score = 1.0  # Default
        if experience_level == 'entry' and 'senior' in job_experience:
            experience_score = 0.5
        elif experience_level == 'senior' and 'junior' in job_experience:
            experience_score = 0.7
        
        # Combined score
        final_score = (keyword_score * 0.4 + skill_score * 0.4 + experience_score * 0.2)
        return round(min(final_score, 1.0), 3)
    
    def _remove_duplicates_and_sort(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs and sort by compatibility score"""
        seen_jobs = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a unique identifier for the job
            job_id = f"{job.get('title', '')}-{job.get('company', '')}-{job.get('location', '')}"
            
            if job_id not in seen_jobs:
                seen_jobs.add(job_id)
                unique_jobs.append(job)
        
        # Sort by compatibility score (descending)
        return sorted(unique_jobs, key=lambda x: x.get('compatibility_score', 0), reverse=True)
    
    def _apply_preferences_filter(self, jobs: List[Dict], preferences: Dict) -> List[Dict]:
        """Apply user preferences to filter jobs"""
        if not preferences:
            return jobs
        
        filtered_jobs = []
        
        for job in jobs:
            # Location filter
            location_pref = preferences.get('location', '').lower()
            if location_pref:
                job_location = job.get('location', '').lower()
                if location_pref not in job_location and job_location not in location_pref:
                    continue
            
            # Salary filter
            min_salary = preferences.get('salary_min')
            if min_salary:
                job_salary_min = job.get('salary_min', 0)
                if job_salary_min and job_salary_min < min_salary:
                    continue
            
            # Job type filter
            job_type_pref = preferences.get('job_type', '').lower()
            if job_type_pref and job_type_pref != 'any':
                job_type = job.get('employment_type', '').lower()
                if job_type_pref not in job_type:
                    continue
            
            # Remote preference
            if preferences.get('remote_preference', False):
                if not job.get('remote_allowed', False):
                    continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _add_apply_options(self, jobs: List[Dict]) -> List[Dict]:
        """Add application options and metadata to jobs"""
        enhanced_jobs = []
        
        for job in jobs:
            enhanced_job = job.copy()
            
            # Add apply options
            enhanced_job['apply_options'] = {
                'quick_apply': {
                    'available': True,
                    'one_click': job.get('source', '') in ['linkedin', 'indeed', 'glassdoor'],
                    'requires_cover_letter': job.get('match_type') in ['primary', 'alternative'],
                    'estimated_time': '2-5 minutes'
                },
                'direct_apply': {
                    'available': True,
                    'url': job.get('apply_url', ''),
                    'external_site': job.get('source', 'company website'),
                    'estimated_time': '10-15 minutes'
                },
                'save_for_later': {
                    'available': True,
                    'folder_suggestions': self._get_folder_suggestions(job)
                },
                'company_research': {
                    'available': True,
                    'company_profile_url': self._get_company_profile_url(job.get('company', '')),
                    'glassdoor_url': self._get_glassdoor_url(job.get('company', '')),
                    'linkedin_url': self._get_linkedin_company_url(job.get('company', ''))
                }
            }
            
            # Add application tracking info
            enhanced_job['application_info'] = {
                'difficulty_level': self._assess_application_difficulty(job),
                'competition_level': self._assess_competition_level(job),
                'success_probability': self._calculate_success_probability(job),
                'recommended_preparation': self._get_preparation_tips(job),
                'application_deadline': job.get('expires_date'),
                'response_time_estimate': self._estimate_response_time(job)
            }
            
            # Add personalized recommendations
            enhanced_job['personalized_tips'] = self._get_personalized_tips(job)
            
            enhanced_jobs.append(enhanced_job)
        
        return enhanced_jobs
    
    def _get_folder_suggestions(self, job: Dict) -> List[str]:
        """Suggest folders for saving jobs"""
        folders = ['Favorites']
        
        if job.get('match_type') == 'primary':
            folders.append('High Priority')
        if job.get('remote_allowed', False):
            folders.append('Remote Jobs')
        if job.get('employment_type', '').lower() == 'internship':
            folders.append('Internships')
        
        industry = job.get('industry', '')
        if industry:
            folders.append(f"{industry} Jobs")
            
        return folders
    
    def _get_company_profile_url(self, company_name: str) -> str:
        """Generate company profile URL"""
        if not company_name:
            return ""
        return f"https://www.google.com/search?q={quote(company_name)}+company+profile"
    
    def _get_glassdoor_url(self, company_name: str) -> str:
        """Generate Glassdoor company URL"""
        if not company_name:
            return ""
        return f"https://www.glassdoor.com/Search/results.htm?keyword={quote(company_name)}"
    
    def _get_linkedin_company_url(self, company_name: str) -> str:
        """Generate LinkedIn company URL"""
        if not company_name:
            return ""
        return f"https://www.linkedin.com/search/results/companies/?keywords={quote(company_name)}"
    
    def _assess_application_difficulty(self, job: Dict) -> str:
        """Assess how difficult the application process might be"""
        score = 0
        
        # Check requirements complexity
        requirements = job.get('requirements', [])
        if len(requirements) > 10:
            score += 2
        elif len(requirements) > 5:
            score += 1
        
        # Check experience level
        experience_level = job.get('experience_level', '').lower()
        if 'senior' in experience_level or 'lead' in experience_level:
            score += 2
        elif 'mid' in experience_level:
            score += 1
        
        # Check company size (larger companies often have more complex processes)
        company_size = job.get('company_size', '').lower()
        if 'large' in company_size or '1000+' in company_size:
            score += 1
        
        if score >= 4:
            return 'High'
        elif score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _assess_competition_level(self, job: Dict) -> str:
        """Assess competition level for the job"""
        score = 0
        
        # Popular companies have more competition
        popular_companies = ['google', 'microsoft', 'amazon', 'apple', 'meta', 'netflix']
        company = job.get('company', '').lower()
        if any(pop_company in company for pop_company in popular_companies):
            score += 3
        
        # Remote jobs typically have more competition
        if job.get('remote_allowed', False):
            score += 1
        
        # High salary jobs have more competition
        salary_max = job.get('salary_max', 0)
        if salary_max > 150000:
            score += 2
        elif salary_max > 100000:
            score += 1
        
        if score >= 4:
            return 'High'
        elif score >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_success_probability(self, job: Dict) -> str:
        """Calculate probability of application success"""
        compatibility_score = job.get('compatibility_score', 0)
        
        if compatibility_score >= 0.8:
            return 'High (80%+)'
        elif compatibility_score >= 0.6:
            return 'Medium (60-80%)'
        elif compatibility_score >= 0.4:
            return 'Moderate (40-60%)'
        else:
            return 'Low (<40%)'
    
    def _get_preparation_tips(self, job: Dict) -> List[str]:
        """Get personalized preparation tips"""
        tips = []
        
        match_type = job.get('match_type', '')
        if match_type == 'primary':
            tips.append("Perfect match! Review your relevant projects and achievements")
        elif match_type == 'alternative':
            tips.append("Good fit! Highlight transferable skills from your experience")
        
        # Skill-specific tips
        skills = job.get('skills', [])
        if skills:
            tips.append(f"Focus on highlighting these key skills: {', '.join(skills[:3])}")
        
        # Experience level tips
        experience_level = job.get('experience_level', '').lower()
        if 'senior' in experience_level:
            tips.append("Emphasize leadership experience and complex project management")
        elif 'junior' in experience_level or 'entry' in experience_level:
            tips.append("Highlight your learning ability and relevant coursework/projects")
        
        # Company-specific tips
        company_size = job.get('company_size', '').lower()
        if 'startup' in company_size:
            tips.append("Emphasize adaptability and willingness to wear multiple hats")
        elif 'large' in company_size:
            tips.append("Highlight experience with structured processes and team collaboration")
        
        return tips[:4]  # Limit to 4 tips
    
    def _estimate_response_time(self, job: Dict) -> str:
        """Estimate response time based on company and job characteristics"""
        company_size = job.get('company_size', '').lower()
        
        if 'startup' in company_size or 'small' in company_size:
            return '1-2 weeks'
        elif 'large' in company_size:
            return '2-4 weeks'
        else:
            return '1-3 weeks'
    
    def _get_personalized_tips(self, job: Dict) -> Dict[str, Any]:
        """Get personalized tips for the specific job"""
        return {
            'cover_letter_tips': [
                f"Mention specific interest in {job.get('company', 'the company')}",
                f"Highlight relevant experience for {job.get('title', 'this role')}",
                "Keep it concise and focused on value you can bring"
            ],
            'interview_prep': [
                "Research the company's recent news and developments",
                f"Prepare examples demonstrating skills: {', '.join(job.get('skills', [])[:3])}",
                "Practice explaining your career progression and goals"
            ],
            'application_timing': {
                'best_time_to_apply': 'Tuesday-Thursday, 10 AM - 2 PM',
                'urgency_level': 'Medium' if job.get('posted_date') else 'Unknown',
                'follow_up_timing': '1 week after application'
            }
        }
    
    def get_application_assistance(self, job_id: str, user_profile: Dict) -> Dict[str, Any]:
        """Get detailed application assistance for a specific job"""
        return {
            'cover_letter_template': self._generate_cover_letter_template(job_id, user_profile),
            'resume_optimization': self._get_resume_optimization_tips(job_id, user_profile),
            'interview_questions': self._get_likely_interview_questions(job_id),
            'application_checklist': self._get_application_checklist(job_id),
            'networking_suggestions': self._get_networking_suggestions(job_id)
        }
    
    def _generate_cover_letter_template(self, job_id: str, user_profile: Dict) -> str:
        """Generate a personalized cover letter template"""
        return f"""
Dear Hiring Manager,

I am writing to express my strong interest in the [JOB_TITLE] position at [COMPANY_NAME]. 
With my background in {user_profile.get('primary_skills', 'relevant technologies')} and 
{user_profile.get('years_experience', 'X')} years of experience, I am excited about the 
opportunity to contribute to your team.

[CUSTOMIZE: Mention specific company research and why you're interested]

In my previous role, I [CUSTOMIZE: Add relevant achievement]. This experience has prepared 
me well for the challenges of this position, particularly [CUSTOMIZE: Mention specific 
job requirements you can address].

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute 
to [COMPANY_NAME]'s continued success.

Best regards,
[YOUR_NAME]
        """.strip()
    
    def _get_resume_optimization_tips(self, job_id: str, user_profile: Dict) -> List[str]:
        """Get resume optimization tips for specific job"""
        return [
            "Add relevant keywords from the job description",
            "Quantify achievements with specific numbers and metrics",
            "Reorder experience to highlight most relevant roles first",
            "Include any relevant certifications or training",
            "Customize your professional summary for this role"
        ]
    
    def _get_likely_interview_questions(self, job_id: str) -> List[str]:
        """Get likely interview questions for the job"""
        return [
            "Tell me about yourself and your relevant experience",
            "Why are you interested in this position and our company?",
            "Describe a challenging project you worked on and how you handled it",
            "How do you stay updated with industry trends and technologies?",
            "What are your salary expectations for this role?"
        ]
    
    def _get_application_checklist(self, job_id: str) -> List[Dict[str, Any]]:
        """Get application checklist"""
        return [
            {"task": "Update resume with relevant keywords", "completed": False, "priority": "High"},
            {"task": "Write customized cover letter", "completed": False, "priority": "High"},
            {"task": "Research company background", "completed": False, "priority": "Medium"},
            {"task": "Prepare portfolio/work samples", "completed": False, "priority": "Medium"},
            {"task": "Set up job alert for similar positions", "completed": False, "priority": "Low"}
        ]
    
    def _get_networking_suggestions(self, job_id: str) -> List[str]:
        """Get networking suggestions for the job"""
        return [
            "Connect with current employees on LinkedIn",
            "Follow the company on social media platforms",
            "Attend industry events where company representatives might be present",
            "Look for mutual connections who can provide referrals",
            "Engage with company content on LinkedIn to increase visibility"
        ]


# Example usage and testing
if __name__ == "__main__":
    print("Testing Role-Based Recommender...")
    recommender = RoleBasedRecommender()
    
    # Mock resume analysis
    mock_analysis = {
        'skills_analysis': {
            'all_skills': ['Python', 'React', 'JavaScript', 'SQL', 'Git']
        },
        'experience_analysis': {
            'experience_level': 'mid',
            'total_years': 3
        },
        'role_suggestion': {
            'primary_role': 'Full Stack Developer',
            'alternative_roles': ['Software Engineer', 'Frontend Developer']
        }
    }
    
    role_analysis = recommender.analyze_role_compatibility(mock_analysis)
    print("Role Analysis:", role_analysis)
