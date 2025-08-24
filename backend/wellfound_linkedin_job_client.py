"""
Enhanced Job API Client with Wellfound and LinkedIn Integration
Integrates with Wellfound (formerly AngelList) and LinkedIn for startup and professional job opportunities
"""

import requests
import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import os
from urllib.parse import urlencode, quote
import feedparser
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

@dataclass
class JobPosting:
    """Standardized job posting data structure"""
    id: str
    title: str
    company: str
    location: str
    description: str
    requirements: List[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    salary_currency: str
    experience_level: str
    employment_type: str
    posted_date: datetime
    expires_date: Optional[datetime]
    source: str
    apply_url: str
    skills: List[str]
    remote_allowed: bool
    company_size: Optional[str]
    industry: Optional[str]
    funding_stage: Optional[str] = None  # For Wellfound startups
    company_logo: Optional[str] = None

class WellfoundLinkedInJobClient:
    """
    Enhanced job client focusing on Wellfound and LinkedIn integration
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # API configurations
        self.apis = {
            'wellfound': {
                'base_url': 'https://wellfound.com',
                'api_url': 'https://wellfound.com/api',
                'search_url': 'https://wellfound.com/jobs',
                'rate_limit': 100,  # requests per hour
                'enabled': True
            },
            'linkedin': {
                'base_url': 'https://www.linkedin.com',
                'jobs_url': 'https://www.linkedin.com/jobs/search',
                'api_url': 'https://api.linkedin.com/rest',
                'api_key': os.getenv('LINKEDIN_API_KEY'),
                'rate_limit': 100,  # requests per hour
                'enabled': True
            },
            'linkedin_jobs_api': {
                'base_url': 'https://linkedin-jobs-search.p.rapidapi.com',
                'api_key': os.getenv('RAPIDAPI_KEY'),
                'rate_limit': 100,
                'enabled': bool(os.getenv('RAPIDAPI_KEY'))
            }
        }
        
        # Rate limiting tracking
        self.rate_limits = {}
        for api in self.apis:
            self.rate_limits[api] = {'count': 0, 'reset_time': datetime.now()}
    
    async def search_jobs(self, 
                         keywords: List[str], 
                         location: str = "", 
                         experience_level: str = "",
                         employment_type: str = "",
                         salary_min: Optional[int] = None,
                         limit: int = 50) -> List[JobPosting]:
        """
        Search for jobs across Wellfound and LinkedIn
        """
        all_jobs = []
        
        async with aiohttp.ClientSession() as session:
            # Search tasks for different platforms
            tasks = []
            
            for keyword in keywords[:3]:  # Limit to 3 keywords to avoid rate limits
                # Wellfound search
                tasks.append(self._search_wellfound(session, keyword, location, experience_level, limit // 2))
                
                # LinkedIn search (multiple methods)
                tasks.append(self._search_linkedin_api(session, keyword, location, experience_level, limit // 2))
                tasks.append(self._search_linkedin_scraper(session, keyword, location, limit // 4))
            
            # Execute all searches concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            for result in results:
                if isinstance(result, list):
                    all_jobs.extend(result)
                elif isinstance(result, Exception):
                    logger.error(f"Search task failed: {result}")
        
        # Remove duplicates and sort by relevance
        unique_jobs = self._remove_duplicates(all_jobs)
        sorted_jobs = self._sort_by_relevance(unique_jobs, keywords)
        
        return sorted_jobs[:limit]
    
    async def _search_wellfound(self, session: aiohttp.ClientSession,
                              keyword: str, location: str, experience_level: str, limit: int) -> List[JobPosting]:
        """Search Wellfound (formerly AngelList) for startup jobs"""
        if not self._check_rate_limit('wellfound'):
            logger.warning("Wellfound rate limit exceeded")
            return []
        
        jobs = []
        try:
            # Method 1: Try API endpoint if available
            await self._search_wellfound_api(session, keyword, location, jobs, limit)
            
            # Method 2: Scrape public job listings
            if len(jobs) < limit // 2:
                await self._search_wellfound_scraper(session, keyword, location, jobs, limit)
            
            self._update_rate_limit('wellfound')
            logger.info(f"Fetched {len(jobs)} jobs from Wellfound for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"Wellfound search error: {e}")
            # Fallback to mock data
            jobs.extend(self._get_wellfound_mock_jobs(keyword, location, limit))
        
        return jobs
    
    async def _search_wellfound_api(self, session: aiohttp.ClientSession, 
                                  keyword: str, location: str, jobs: List[JobPosting], limit: int):
        """Search using Wellfound's API endpoints"""
        try:
            # Wellfound job search endpoint
            search_url = f"{self.apis['wellfound']['api_url']}/startup_jobs"
            params = {
                'query': keyword,
                'location': location,
                'limit': limit,
                'page': 1
            }
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'User-Agent': self.session.headers['User-Agent']
            }
            
            async with session.get(search_url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Parse Wellfound job data
                    for job_data in data.get('startup_jobs', []):
                        job = self._parse_wellfound_job(job_data)
                        if job:
                            jobs.append(job)
                            
        except Exception as e:
            logger.error(f"Wellfound API error: {e}")
    
    async def _search_wellfound_scraper(self, session: aiohttp.ClientSession,
                                      keyword: str, location: str, jobs: List[JobPosting], limit: int):
        """Scrape Wellfound job listings"""
        try:
            search_url = f"{self.apis['wellfound']['search_url']}"
            params = {
                'role': keyword,
                'location': location,
                'remote': 'true'
            }
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Parse job listings from HTML
                    job_elements = soup.find_all('div', class_='job-listing') or soup.find_all('div', {'data-test': 'JobSearchResult'})
                    
                    for job_element in job_elements[:limit]:
                        job = self._parse_wellfound_html(job_element)
                        if job:
                            jobs.append(job)
                            
        except Exception as e:
            logger.error(f"Wellfound scraper error: {e}")
    
    async def _search_linkedin_api(self, session: aiohttp.ClientSession,
                                 keyword: str, location: str, experience_level: str, limit: int) -> List[JobPosting]:
        """Search LinkedIn using RapidAPI LinkedIn Jobs API"""
        if not self._check_rate_limit('linkedin_jobs_api') or not self.apis['linkedin_jobs_api']['enabled']:
            return await self._search_linkedin_official_api(session, keyword, location, experience_level, limit)
        
        jobs = []
        try:
            url = f"{self.apis['linkedin_jobs_api']['base_url']}/search"
            headers = {
                'X-RapidAPI-Key': self.apis['linkedin_jobs_api']['api_key'],
                'X-RapidAPI-Host': 'linkedin-jobs-search.p.rapidapi.com'
            }
            
            params = {
                'keywords': keyword,
                'location': location,
                'dateSincePosted': 'week',
                'sort': 'mostRecent'
            }
            
            if experience_level:
                exp_mapping = {
                    'entry': '1',
                    'associate': '2',
                    'mid': '3',
                    'senior': '4',
                    'director': '5',
                    'executive': '6'
                }
                if experience_level.lower() in exp_mapping:
                    params['experienceLevel'] = exp_mapping[experience_level.lower()]
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for job_data in data.get('data', [])[:limit]:
                        job = self._parse_linkedin_api_job(job_data)
                        if job:
                            jobs.append(job)
                    
                    self._update_rate_limit('linkedin_jobs_api')
                    logger.info(f"Fetched {len(jobs)} jobs from LinkedIn API for keyword: {keyword}")
                
        except Exception as e:
            logger.error(f"LinkedIn API error: {e}")
        
        return jobs
    
    async def _search_linkedin_official_api(self, session: aiohttp.ClientSession,
                                          keyword: str, location: str, experience_level: str, limit: int) -> List[JobPosting]:
        """Search using LinkedIn's official API (if available)"""
        if not self.apis['linkedin']['api_key']:
            return []
        
        jobs = []
        try:
            url = f"{self.apis['linkedin']['api_url']}/jobSearch"
            headers = {
                'Authorization': f"Bearer {self.apis['linkedin']['api_key']}",
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'application/json'
            }
            
            params = {
                'keywords': keyword,
                'location': location,
                'limit': min(limit, 20),
                'sortBy': 'DD'
            }
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    for job_data in data.get('elements', []):
                        job = self._parse_linkedin_official_job(job_data)
                        if job:
                            jobs.append(job)
                            
        except Exception as e:
            logger.error(f"LinkedIn Official API error: {e}")
        
        return jobs
    
    async def _search_linkedin_scraper(self, session: aiohttp.ClientSession,
                                     keyword: str, location: str, limit: int) -> List[JobPosting]:
        """Scrape LinkedIn job listings"""
        jobs = []
        try:
            search_url = f"{self.apis['linkedin']['jobs_url']}"
            params = {
                'keywords': keyword,
                'location': location,
                'f_TPR': 'r86400',  # Last 24 hours
                'f_JT': 'F',  # Full time
                'start': 0
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
            
            async with session.get(search_url, params=params, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Parse job listings
                    job_elements = soup.find_all('div', class_='job-search-card') or soup.find_all('li', class_='jobs-search-results__list-item')
                    
                    for job_element in job_elements[:limit]:
                        job = self._parse_linkedin_html(job_element)
                        if job:
                            jobs.append(job)
                            
            logger.info(f"Scraped {len(jobs)} jobs from LinkedIn for keyword: {keyword}")
            
        except Exception as e:
            logger.error(f"LinkedIn scraper error: {e}")
        
        return jobs
    
    def _parse_wellfound_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse Wellfound API job data"""
        try:
            startup = job_data.get('startup', {})
            
            return JobPosting(
                id=f"wellfound_{job_data.get('id', '')}",
                title=job_data.get('title', ''),
                company=startup.get('name', 'Unknown Startup'),
                location=job_data.get('location_name', '') or startup.get('location', ''),
                description=job_data.get('description', ''),
                requirements=self._extract_requirements(job_data.get('description', '')),
                salary_min=job_data.get('salary_min'),
                salary_max=job_data.get('salary_max'),
                salary_currency=job_data.get('currency', 'USD'),
                experience_level=self._map_experience_level(job_data.get('experience', '')),
                employment_type=self._map_employment_type(job_data.get('job_type', '')),
                posted_date=self._parse_date(job_data.get('created_at')),
                expires_date=None,
                source='Wellfound',
                apply_url=f"https://wellfound.com/company/{startup.get('slug', '')}/jobs/{job_data.get('id', '')}",
                skills=job_data.get('tags', []),
                remote_allowed=job_data.get('remote_ok', False),
                company_size=startup.get('company_size', ''),
                industry=startup.get('markets', [{}])[0].get('name', '') if startup.get('markets') else '',
                funding_stage=startup.get('stage', ''),
                company_logo=startup.get('logo_url', '')
            )
        except Exception as e:
            logger.error(f"Error parsing Wellfound job: {e}")
            return None
    
    def _parse_wellfound_html(self, job_element) -> Optional[JobPosting]:
        """Parse Wellfound HTML job element"""
        try:
            title_elem = job_element.find('h3') or job_element.find('a', class_='job-title')
            company_elem = job_element.find('span', class_='company-name') or job_element.find('h4')
            location_elem = job_element.find('span', class_='location')
            
            title = title_elem.get_text(strip=True) if title_elem else ''
            company = company_elem.get_text(strip=True) if company_elem else ''
            location = location_elem.get_text(strip=True) if location_elem else ''
            
            # Extract job URL
            job_link = job_element.find('a')
            job_url = job_link.get('href', '') if job_link else ''
            if job_url and not job_url.startswith('http'):
                job_url = f"https://wellfound.com{job_url}"
            
            return JobPosting(
                id=f"wellfound_scraped_{hash(title + company)}",
                title=title,
                company=company,
                location=location,
                description=f"Startup opportunity at {company}",
                requirements=[],
                salary_min=None,
                salary_max=None,
                salary_currency='USD',
                experience_level='',
                employment_type='full_time',
                posted_date=datetime.now(),
                expires_date=None,
                source='Wellfound',
                apply_url=job_url,
                skills=[],
                remote_allowed=True,
                company_size='',
                industry='',
                funding_stage='',
                company_logo=''
            )
        except Exception as e:
            logger.error(f"Error parsing Wellfound HTML: {e}")
            return None
    
    def _parse_linkedin_api_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse LinkedIn API job data"""
        try:
            return JobPosting(
                id=f"linkedin_{job_data.get('id', '')}",
                title=job_data.get('title', ''),
                company=job_data.get('company', ''),
                location=job_data.get('location', ''),
                description=job_data.get('description', ''),
                requirements=self._extract_requirements(job_data.get('description', '')),
                salary_min=self._extract_salary_min(job_data.get('salary', '')),
                salary_max=self._extract_salary_max(job_data.get('salary', '')),
                salary_currency='USD',
                experience_level=self._map_experience_level(job_data.get('level', '')),
                employment_type=self._map_employment_type(job_data.get('type', '')),
                posted_date=self._parse_date(job_data.get('date')),
                expires_date=None,
                source='LinkedIn',
                apply_url=job_data.get('link', ''),
                skills=job_data.get('insights', []),
                remote_allowed='remote' in job_data.get('location', '').lower(),
                company_size=job_data.get('company_size', ''),
                industry=job_data.get('industry', ''),
                company_logo=job_data.get('company_logo', '')
            )
        except Exception as e:
            logger.error(f"Error parsing LinkedIn API job: {e}")
            return None
    
    def _parse_linkedin_official_job(self, job_data: Dict) -> Optional[JobPosting]:
        """Parse LinkedIn official API job data"""
        try:
            job_id = str(job_data.get('entityUrn', '').split(':')[-1] if job_data.get('entityUrn') else job_data.get('id', ''))
            
            return JobPosting(
                id=f"linkedin_official_{job_id}",
                title=job_data.get('title', ''),
                company=job_data.get('companyDetails', {}).get('company', {}).get('name', 'Unknown'),
                location=job_data.get('formattedLocation', ''),
                description=job_data.get('description', {}).get('text', ''),
                requirements=self._extract_requirements(job_data.get('description', {}).get('text', '')),
                salary_min=None,
                salary_max=None,
                salary_currency='USD',
                experience_level=self._map_linkedin_experience_level(job_data.get('experienceLevel', '')),
                employment_type=self._map_linkedin_employment_type(job_data.get('employmentType', '')),
                posted_date=datetime.fromtimestamp(job_data.get('listedAt', 0) / 1000) if job_data.get('listedAt') else datetime.now(),
                expires_date=None,
                source='LinkedIn',
                apply_url=f"https://www.linkedin.com/jobs/view/{job_id}",
                skills=job_data.get('skills', []),
                remote_allowed='remote' in job_data.get('workplaceTypes', []) if job_data.get('workplaceTypes') else False,
                company_size=job_data.get('companyDetails', {}).get('company', {}).get('staffCount', None),
                industry=job_data.get('companyDetails', {}).get('company', {}).get('industries', [None])[0]
            )
        except Exception as e:
            logger.error(f"Error parsing LinkedIn official job: {e}")
            return None
    
    def _parse_linkedin_html(self, job_element) -> Optional[JobPosting]:
        """Parse LinkedIn HTML job element"""
        try:
            title_elem = job_element.find('h3') or job_element.find('a', class_='job-title-link')
            company_elem = job_element.find('h4') or job_element.find('a', class_='hidden-nested-link')
            location_elem = job_element.find('span', class_='job-search-card__location')
            
            title = title_elem.get_text(strip=True) if title_elem else ''
            company = company_elem.get_text(strip=True) if company_elem else ''
            location = location_elem.get_text(strip=True) if location_elem else ''
            
            # Extract job URL
            job_link = job_element.find('a', class_='base-card__full-link')
            job_url = job_link.get('href', '') if job_link else ''
            
            return JobPosting(
                id=f"linkedin_scraped_{hash(title + company)}",
                title=title,
                company=company,
                location=location,
                description=f"Professional opportunity at {company}",
                requirements=[],
                salary_min=None,
                salary_max=None,
                salary_currency='USD',
                experience_level='',
                employment_type='full_time',
                posted_date=datetime.now(),
                expires_date=None,
                source='LinkedIn',
                apply_url=job_url,
                skills=[],
                remote_allowed='remote' in location.lower(),
                company_size='',
                industry='',
                company_logo=''
            )
        except Exception as e:
            logger.error(f"Error parsing LinkedIn HTML: {e}")
            return None
    
    def _get_wellfound_mock_jobs(self, keyword: str, location: str, limit: int) -> List[JobPosting]:
        """Generate mock Wellfound jobs for development"""
        jobs = []
        startups = [
            'TechFlow AI', 'DataSync Pro', 'CloudVault Systems', 'AgileDesk', 'FinTech Innovations',
            'HealthTech Solutions', 'EduLearn Platform', 'GreenEnergy Tech', 'CyberShield Security', 'NeuralNet Labs'
        ]
        
        for i in range(min(limit, len(startups))):
            startup = startups[i]
            jobs.append(JobPosting(
                id=f"wellfound_mock_{i}",
                title=f"{keyword} Engineer" if i % 2 == 0 else f"Senior {keyword} Developer",
                company=startup,
                location=location or 'San Francisco, CA',
                description=f"Join {startup}, an innovative startup revolutionizing the {keyword} space. Work with cutting-edge technology and make a real impact.",
                requirements=[f"{keyword} experience", "Startup mindset", "Fast learner", "Team player"],
                salary_min=80000 + (i * 10000),
                salary_max=150000 + (i * 15000),
                salary_currency='USD',
                experience_level='mid' if i % 3 != 0 else 'senior',
                employment_type='full_time',
                posted_date=datetime.now() - timedelta(days=i),
                expires_date=None,
                source='Wellfound',
                apply_url=f"https://wellfound.com/company/{startup.lower().replace(' ', '-')}/jobs/{i}",
                skills=[keyword, 'JavaScript', 'Python', 'React', 'Node.js'][:(i % 4) + 2],
                remote_allowed=i % 2 == 0,
                company_size=f"{10 + i * 5}-{20 + i * 10} employees",
                industry='Technology',
                funding_stage=['Seed', 'Series A', 'Series B', 'Series C'][i % 4],
                company_logo=f"https://logo.clearbit.com/{startup.lower().replace(' ', '')}.com"
            ))
        
        return jobs
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Extract requirements from job description"""
        if not description:
            return []
        
        requirements = []
        
        # Common requirement patterns
        req_patterns = [
            r'(?:requirements?|qualifications?|skills?)[:\s]*([^.]+)',
            r'(?:must have|required)[:\s]*([^.]+)',
            r'(?:experience with|proficient in)[:\s]*([^.]+)'
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            for match in matches:
                # Split by common delimiters
                items = re.split(r'[,;•\n]', match)
                for item in items:
                    cleaned = item.strip()
                    if cleaned and len(cleaned) > 3:
                        requirements.append(cleaned)
        
        return requirements[:10]  # Limit to 10 requirements
    
    def _extract_salary_min(self, salary_text: str) -> Optional[float]:
        """Extract minimum salary from text"""
        if not salary_text:
            return None
        
        # Extract numbers from salary text
        numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', salary_text)
        if len(numbers) >= 1:
            return float(numbers[0].replace(',', ''))
        return None
    
    def _extract_salary_max(self, salary_text: str) -> Optional[float]:
        """Extract maximum salary from text"""
        if not salary_text:
            return None
        
        # Extract numbers from salary text
        numbers = re.findall(r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', salary_text)
        if len(numbers) >= 2:
            return float(numbers[1].replace(',', ''))
        elif len(numbers) == 1:
            # If only one number, assume it's max
            return float(numbers[0].replace(',', ''))
        return None
    
    def _map_experience_level(self, level: str) -> str:
        """Map experience level to standard format"""
        level = level.lower()
        if any(word in level for word in ['entry', 'junior', 'jr', 'new grad', '0-2']):
            return 'entry'
        elif any(word in level for word in ['senior', 'sr', 'lead', '5+']):
            return 'senior'
        elif any(word in level for word in ['mid', 'intermediate', '2-5']):
            return 'mid'
        elif any(word in level for word in ['executive', 'director', 'vp', 'c-level']):
            return 'executive'
        return 'mid'
    
    def _map_employment_type(self, emp_type: str) -> str:
        """Map employment type to standard format"""
        emp_type = emp_type.lower()
        if 'full' in emp_type:
            return 'full_time'
        elif 'part' in emp_type:
            return 'part_time'
        elif 'contract' in emp_type:
            return 'contract'
        elif 'intern' in emp_type:
            return 'internship'
        return 'full_time'
    
    def _map_linkedin_experience_level(self, level: str) -> str:
        """Map LinkedIn experience level to standard format"""
        level_mapping = {
            '1': 'internship',
            '2': 'entry',
            '3': 'associate',
            '4': 'mid',
            '5': 'senior',
            '6': 'director',
            '7': 'vp',
            '8': 'cxo'
        }
        return level_mapping.get(level, 'mid')
    
    def _map_linkedin_employment_type(self, emp_type: str) -> str:
        """Map LinkedIn employment type to standard format"""
        type_mapping = {
            'F': 'full_time',
            'P': 'part_time',
            'C': 'contract',
            'T': 'temporary',
            'I': 'internship',
            'V': 'volunteer',
            'O': 'other'
        }
        return type_mapping.get(emp_type, 'full_time')
    
    def _parse_date(self, date_str) -> datetime:
        """Parse date string to datetime object"""
        if not date_str:
            return datetime.now()
        
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # If all formats fail, return current time
            return datetime.now()
        except:
            return datetime.now()
    
    def _check_rate_limit(self, api_name: str) -> bool:
        """Check if API rate limit allows request"""
        now = datetime.now()
        rate_info = self.rate_limits[api_name]
        
        # Reset counter if an hour has passed
        if now - rate_info['reset_time'] > timedelta(hours=1):
            rate_info['count'] = 0
            rate_info['reset_time'] = now
        
        # Check if under limit
        return rate_info['count'] < self.apis[api_name]['rate_limit']
    
    def _update_rate_limit(self, api_name: str):
        """Update rate limit counter"""
        self.rate_limits[api_name]['count'] += 1
    
    def _remove_duplicates(self, jobs: List[JobPosting]) -> List[JobPosting]:
        """Remove duplicate job postings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create signature based on title, company, and location
            signature = f"{job.title.lower()}_{job.company.lower()}_{job.location.lower()}"
            if signature not in seen:
                seen.add(signature)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def _sort_by_relevance(self, jobs: List[JobPosting], keywords: List[str]) -> List[JobPosting]:
        """Sort jobs by relevance to keywords"""
        def calculate_relevance(job: JobPosting) -> float:
            score = 0
            text = f"{job.title} {job.description} {' '.join(job.skills)}".lower()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                # Title match gets highest score
                if keyword_lower in job.title.lower():
                    score += 10
                # Skills match gets high score
                if any(keyword_lower in skill.lower() for skill in job.skills):
                    score += 5
                # Description match gets moderate score
                if keyword_lower in job.description.lower():
                    score += 2
            
            # Bonus for recent postings
            days_old = (datetime.now() - job.posted_date).days
            if days_old <= 1:
                score += 3
            elif days_old <= 7:
                score += 1
            
            return score
        
        return sorted(jobs, key=calculate_relevance, reverse=True)

# Convenience function for synchronous job search
def search_wellfound_linkedin_jobs(keywords: List[str], 
                                 location: str = "",
                                 experience_level: str = "",
                                 employment_type: str = "",
                                 salary_min: Optional[int] = None,
                                 limit: int = 50) -> List[JobPosting]:
    """
    Synchronous wrapper for job search
    """
    client = WellfoundLinkedInJobClient()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        jobs = loop.run_until_complete(
            client.search_jobs(
                keywords=keywords,
                location=location,
                experience_level=experience_level,
                employment_type=employment_type,
                salary_min=salary_min,
                limit=limit
            )
        )
        return jobs
    finally:
        loop.close()

if __name__ == "__main__":
    # Test the client
    test_keywords = ["software engineer", "python developer"]
    test_location = "San Francisco"
    
    jobs = search_wellfound_linkedin_jobs(
        keywords=test_keywords,
        location=test_location,
        limit=20
    )
    
    print(f"Found {len(jobs)} jobs:")
    for job in jobs[:5]:  # Show first 5 jobs
        print(f"- {job.title} at {job.company} ({job.source})")
        print(f"  Location: {job.location}")
        print(f"  URL: {job.apply_url}")
        print()
