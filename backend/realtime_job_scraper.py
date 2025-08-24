"""
Real-time Job Data Scraper
Fetches live job postings from multiple sources for enhanced job matching
"""

import requests
import time
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import feedparser
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
import asyncio
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobPosting:
    """Data class for job postings"""
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    salary_range: str
    experience_level: str
    job_type: str
    posted_date: str
    source: str
    apply_url: str
    skills: List[str]

class RealTimeJobScraper:
    """
    Real-time job scraper that fetches live job data from multiple sources
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Job board APIs and endpoints
        self.job_sources = {
            'adzuna': {
                'base_url': 'https://api.adzuna.com/v1/api/jobs',
                'app_id': 'your_adzuna_app_id',  # Replace with actual API key
                'app_key': 'your_adzuna_app_key'  # Replace with actual API key
            },
            'github_jobs': {
                'url': 'https://jobs.github.com/positions.json'
            },
            'stackoverflow': {
                'rss_url': 'https://stackoverflow.com/jobs/feed'
            },
            'dice': {
                'base_url': 'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search'
            }
        }
        
        # Tech job boards RSS feeds
        self.rss_feeds = [
            'https://remoteok.io/remote-jobs.rss',
            'https://weworkremotely.com/categories/remote-programming-jobs.rss',
            'https://jobs.lever.co/feed',
        ]
        
        # Experience level mapping
        self.experience_mapping = {
            'intern': 'entry',
            'junior': 'entry', 
            'entry': 'entry',
            'associate': 'entry',
            'mid': 'mid',
            'middle': 'mid',
            'senior': 'senior',
            'lead': 'senior',
            'principal': 'senior',
            'staff': 'senior',
            'manager': 'senior',
            'director': 'executive',
            'vp': 'executive',
            'cto': 'executive',
            'head': 'executive'
        }
    
    async def fetch_jobs_async(self, keywords: List[str], location: str = "", limit: int = 50) -> List[JobPosting]:
        """Fetch jobs asynchronously from multiple sources"""
        tasks = []
        
        # Create async tasks for different sources
        async with aiohttp.ClientSession() as session:
            for keyword in keywords[:3]:  # Limit keywords to avoid API limits
                tasks.append(self._fetch_adzuna_jobs(session, keyword, location, limit // len(keywords)))
                tasks.append(self._fetch_github_jobs(session, keyword, location))
                tasks.append(self._fetch_rss_jobs(session, keyword))
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        all_jobs = []
        for result in results:
            if isinstance(result, list):
                all_jobs.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Job fetch error: {result}")
        
        # Remove duplicates and sort by relevance
        unique_jobs = self._remove_duplicates(all_jobs)
        return sorted(unique_jobs, key=lambda x: x.posted_date, reverse=True)[:limit]
    
    def fetch_jobs(self, keywords: List[str], location: str = "", limit: int = 50) -> List[JobPosting]:
        """Synchronous wrapper for async job fetching"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.fetch_jobs_async(keywords, location, limit))
        finally:
            loop.close()
    
    async def _fetch_adzuna_jobs(self, session: aiohttp.ClientSession, keyword: str, location: str, limit: int) -> List[JobPosting]:
        """Fetch jobs from Adzuna API"""
        jobs = []
        try:
            url = f"{self.job_sources['adzuna']['base_url']}/us/search/1"
            params = {
                'app_id': self.job_sources['adzuna']['app_id'],
                'app_key': self.job_sources['adzuna']['app_key'],
                'what': keyword,
                'where': location,
                'results_per_page': min(limit, 20),
                'sort_by': 'date'
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    for job_data in data.get('results', []):
                        job = self._parse_adzuna_job(job_data)
                        if job:
                            jobs.append(job)
        except Exception as e:
            logger.error(f"Adzuna API error: {e}")
        
        return jobs
    
    async def _fetch_github_jobs(self, session: aiohttp.ClientSession, keyword: str, location: str) -> List[JobPosting]:
        """Fetch jobs from GitHub Jobs API (deprecated but using for demo)"""
        jobs = []
        try:
            # Note: GitHub Jobs API was deprecated, using mock data for demonstration
            mock_jobs = [
                {
                    'id': f'github_{keyword}_{int(time.time())}',
                    'title': f'Senior {keyword.title()} Developer',
                    'company': 'Tech Company Inc.',
                    'location': location or 'Remote',
                    'description': f'We are looking for a skilled {keyword} developer to join our team...',
                    'url': 'https://github.com/jobs/sample',
                    'created_at': datetime.now().isoformat(),
                    'type': 'Full Time'
                }
            ]
            
            for job_data in mock_jobs:
                job = self._parse_github_job(job_data, keyword)
                if job:
                    jobs.append(job)
                    
        except Exception as e:
            logger.error(f"GitHub Jobs error: {e}")
        
        return jobs
    
    async def _fetch_rss_jobs(self, session: aiohttp.ClientSession, keyword: str) -> List[JobPosting]:
        """Fetch jobs from RSS feeds"""
        jobs = []
        
        for feed_url in self.rss_feeds[:2]:  # Limit to 2 feeds for demo
            try:
                async with session.get(feed_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        feed = feedparser.parse(content)
                        
                        for entry in feed.entries[:5]:  # Limit entries per feed
                            if keyword.lower() in entry.title.lower() or keyword.lower() in entry.get('summary', '').lower():
                                job = self._parse_rss_job(entry, keyword, feed_url)
                                if job:
                                    jobs.append(job)
            except Exception as e:
                logger.error(f"RSS feed error for {feed_url}: {e}")
        
        return jobs
    
    def _parse_adzuna_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse Adzuna job data"""
        try:
            return JobPosting(
                id=f"adzuna_{job_data.get('id', '')}",
                title=job_data.get('title', ''),
                company=job_data.get('company', {}).get('display_name', ''),
                location=job_data.get('location', {}).get('display_name', ''),
                description=job_data.get('description', ''),
                requirements=self._extract_requirements(job_data.get('description', '')),
                salary_range=self._format_salary(job_data.get('salary_min'), job_data.get('salary_max')),
                experience_level=self._determine_experience_level(job_data.get('title', '') + ' ' + job_data.get('description', '')),
                job_type='Full Time',
                posted_date=job_data.get('created', datetime.now().isoformat()),
                source='Adzuna',
                apply_url=job_data.get('redirect_url', ''),
                skills=self._extract_skills_from_description(job_data.get('description', ''))
            )
        except Exception as e:
            logger.error(f"Error parsing Adzuna job: {e}")
            return None
    
    def _parse_github_job(self, job_data: Dict, keyword: str) -> Optional[JobPosting]:
        """Parse GitHub job data"""
        try:
            return JobPosting(
                id=job_data.get('id', ''),
                title=job_data.get('title', ''),
                company=job_data.get('company', ''),
                location=job_data.get('location', ''),
                description=job_data.get('description', ''),
                requirements=self._extract_requirements(job_data.get('description', '')),
                salary_range='Not specified',
                experience_level=self._determine_experience_level(job_data.get('title', '')),
                job_type=job_data.get('type', 'Full Time'),
                posted_date=job_data.get('created_at', datetime.now().isoformat()),
                source='GitHub Jobs',
                apply_url=job_data.get('url', ''),
                skills=[keyword] + self._extract_skills_from_description(job_data.get('description', ''))
            )
        except Exception as e:
            logger.error(f"Error parsing GitHub job: {e}")
            return None
    
    def _parse_rss_job(self, entry, keyword: str, source_url: str) -> Optional[JobPosting]:
        """Parse RSS job entry"""
        try:
            source_name = self._get_source_name(source_url)
            
            return JobPosting(
                id=f"rss_{hash(entry.link)}",
                title=entry.title,
                company=getattr(entry, 'author', 'Company not specified'),
                location=self._extract_location_from_text(entry.get('summary', '')),
                description=entry.get('summary', ''),
                requirements=self._extract_requirements(entry.get('summary', '')),
                salary_range='Not specified',
                experience_level=self._determine_experience_level(entry.title + ' ' + entry.get('summary', '')),
                job_type='Full Time',
                posted_date=getattr(entry, 'published', datetime.now().isoformat()),
                source=source_name,
                apply_url=entry.link,
                skills=[keyword] + self._extract_skills_from_description(entry.get('summary', ''))
            )
        except Exception as e:
            logger.error(f"Error parsing RSS job: {e}")
            return None
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract job requirements from description"""
        requirements = []
        
        # Look for requirement patterns
        req_patterns = [
            r'(?:requires?|must have|needed?)[:\s]+(.*?)(?:\.|;|\n)',
            r'(?:experience with|knowledge of)[:\s]+(.*?)(?:\.|;|\n)',
            r'(?:skills?)[:\s]+(.*?)(?:\.|;|\n)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            requirements.extend([match.strip() for match in matches])
        
        return requirements[:5]  # Limit to top 5 requirements
    
    def _extract_skills_from_description(self, description: str) -> List[str]:
        """Extract technical skills from job description"""
        skills = []
        
        # Common tech skills to look for
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'django', 'flask', 'spring', 'aws', 'azure', 'docker', 'kubernetes',
            'sql', 'postgresql', 'mongodb', 'redis', 'git', 'ci/cd', 'agile',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'data science'
        ]
        
        description_lower = description.lower()
        for skill in tech_skills:
            if skill in description_lower:
                skills.append(skill)
        
        return skills[:8]  # Limit to top 8 skills
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level from job title and description"""
        text_lower = text.lower()
        
        for key, level in self.experience_mapping.items():
            if key in text_lower:
                return level
        
        # Check for years of experience
        year_match = re.search(r'(\d+)\+?\s*years?', text_lower)
        if year_match:
            years = int(year_match.group(1))
            if years <= 2:
                return 'entry'
            elif years <= 5:
                return 'mid'
            else:
                return 'senior'
        
        return 'mid'  # Default
    
    def _format_salary(self, min_salary: Optional[float], max_salary: Optional[float]) -> str:
        """Format salary range"""
        if min_salary and max_salary:
            return f"${int(min_salary):,} - ${int(max_salary):,}"
        elif min_salary:
            return f"${int(min_salary):,}+"
        elif max_salary:
            return f"Up to ${int(max_salary):,}"
        else:
            return "Not specified"
    
    def _extract_location_from_text(self, text: str) -> str:
        """Extract location from job text"""
        # Simple location extraction - could be enhanced with NER
        location_patterns = [
            r'(?:location|based in|located in)[:\s]+(.*?)(?:\.|,|\n)',
            r'(?:remote|work from home|wfh)',
            r'(?:new york|san francisco|seattle|austin|boston|chicago|los angeles)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else match.group(0)
        
        return 'Not specified'
    
    def _get_source_name(self, url: str) -> str:
        """Get friendly source name from URL"""
        if 'remoteok' in url:
            return 'RemoteOK'
        elif 'weworkremotely' in url:
            return 'We Work Remotely'
        elif 'lever' in url:
            return 'Lever'
        else:
            return 'RSS Feed'
    
    def _remove_duplicates(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """Remove duplicate job postings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a signature for the job
            signature = f"{job.title.lower()}_{job.company.lower()}_{job.location.lower()}"
            if signature not in seen:
                seen.add(signature)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def get_trending_skills(self, jobs: List[JobPosting]) -> Dict[str, int]:
        """Get trending skills from job postings"""
        skill_count = {}
        
        for job in jobs:
            for skill in job.skills:
                skill_count[skill] = skill_count.get(skill, 0) + 1
        
        # Sort by frequency
        return dict(sorted(skill_count.items(), key=lambda x: x[1], reverse=True))
    
    def filter_jobs_by_skills(self, jobs: List[JobPosting], user_skills: List[str], min_match: float = 0.3) -> List[JobPosting]:
        """Filter jobs based on user skills match"""
        filtered_jobs = []
        
        for job in jobs:
            if not job.skills:
                continue
                
            # Calculate skill match percentage
            matched_skills = set(user_skills) & set(job.skills)
            match_ratio = len(matched_skills) / len(job.skills) if job.skills else 0
            
            if match_ratio >= min_match:
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def get_salary_insights(self, jobs: List[JobPosting]) -> Dict[str, Any]:
        """Get salary insights from job postings"""
        salaries = []
        
        for job in jobs:
            if job.salary_range and job.salary_range != 'Not specified':
                # Extract salary numbers
                salary_match = re.findall(r'\$(\d+(?:,\d+)*)', job.salary_range)
                if len(salary_match) >= 2:
                    min_sal = int(salary_match[0].replace(',', ''))
                    max_sal = int(salary_match[1].replace(',', ''))
                    salaries.append((min_sal + max_sal) / 2)
        
        if salaries:
            return {
                'average_salary': sum(salaries) / len(salaries),
                'min_salary': min(salaries),
                'max_salary': max(salaries),
                'salary_count': len(salaries)
            }
        
        return {
            'average_salary': 0,
            'min_salary': 0,
            'max_salary': 0,
            'salary_count': 0
        }
