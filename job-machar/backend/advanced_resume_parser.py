"""
Advanced Resume Parser using Hugging Face Models
Extracts skills, experience, and other relevant information from PDF resumes
"""

import os
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from sentence_transformers import SentenceTransformer
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

class AdvancedResumeParser:
    """
    Advanced resume parser using Hugging Face NLP models
    """
    
    def __init__(self):
        print("🚀 Initializing Advanced Resume Parser...")
        
        # Initialize models
        self._init_models()
        
        # Predefined skill categories and keywords
        self.skill_categories = {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'swift',
                'kotlin', 'typescript', 'php', 'ruby', 'scala', 'r', 'matlab',
                'perl', 'shell', 'bash', 'powershell'
            ],
            'web_technologies': [
                'react', 'angular', 'vue.js', 'node.js', 'express', 'django',
                'flask', 'fastapi', 'spring boot', 'asp.net', 'laravel',
                'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite', 'cassandra', 'dynamodb',
                'firebase', 'neo4j', 'influxdb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'vercel',
                'netlify', 'digital ocean', 'linode', 'vultr'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'terraform', 'ansible', 'chef', 'puppet', 'vagrant',
                'prometheus', 'grafana', 'elk stack'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'jupyter', 'tableau', 'power bi', 'spark', 'hadoop'
            ],
            'mobile_development': [
                'ios', 'android', 'react native', 'flutter', 'xamarin',
                'ionic', 'cordova', 'swift', 'objective-c', 'kotlin'
            ],
            'testing': [
                'unit testing', 'integration testing', 'selenium', 'jest',
                'pytest', 'junit', 'cucumber', 'cypress', 'postman'
            ]
        }
        
        # Experience indicators
        self.experience_indicators = {
            'entry': ['intern', 'junior', 'entry', 'associate', 'trainee', 'graduate'],
            'mid': ['developer', 'engineer', 'analyst', 'specialist', 'consultant'],
            'senior': ['senior', 'lead', 'principal', 'staff', 'architect', 'manager'],
            'executive': ['director', 'vp', 'cto', 'ceo', 'head', 'chief']
        }
        
        print("✅ Advanced Resume Parser initialized successfully!")
    
    def _init_models(self):
        """Initialize Hugging Face models"""
        try:
            # Named Entity Recognition for extracting entities
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple",
                device=-1  # Force CPU usage
            )
            
            # Text classification for skill categorization
            self.text_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1
            )
            
            # Sentence transformer for semantic similarity
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load spaCy model
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy English model not found. Installing...")
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            
            logger.info("✅ NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            # Fallback to basic processing
            self.ner_pipeline = None
            self.text_classifier = None
            self.sentence_model = None
            self.nlp = None
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and extract comprehensive information
        """
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(file_path)
            
            if not text or len(text.strip()) < 100:
                return {'error': 'Could not extract sufficient text from resume'}
            
            # Perform comprehensive analysis
            analysis = {
                'raw_text': text,
                'personal_info': self._extract_personal_info(text),
                'skills_analysis': self._analyze_skills(text),
                'experience_analysis': self._analyze_experience(text),
                'education_analysis': self._analyze_education(text),
                'contact_info': self._extract_contact_info(text),
                'projects': self._extract_projects(text),
                'certifications': self._extract_certifications(text),
                'achievements': self._extract_achievements(text),
                'quality_assessment': self._assess_resume_quality(text),
                'summary': self._generate_summary(text),
                'metadata': {
                    'processed_at': datetime.now().isoformat(),
                    'word_count': len(text.split()),
                    'char_count': len(text),
                    'sections_found': self._count_sections(text)
                }
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Resume parsing error: {e}")
            return {'error': f'Failed to parse resume: {str(e)}'}
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""
        
        # Method 1: pdfplumber (best for text extraction)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"pdfplumber extraction failed: {e}")
        
        # Method 2: PyMuPDF
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
            
            if text.strip():
                return text
        except Exception as e:
            logger.warning(f"PyMuPDF extraction failed: {e}")
        
        # Method 3: PyPDF2 (fallback)
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            logger.warning(f"PyPDF2 extraction failed: {e}")
        
        return text
    
    def _extract_personal_info(self, text: str) -> Dict[str, Any]:
        """Extract personal information using NER"""
        personal_info = {
            'name': None,
            'title': None,
            'summary': None
        }
        
        try:
            if self.ner_pipeline:
                # Use NER to extract person names
                entities = self.ner_pipeline(text[:1000])  # Process first 1000 chars
                
                for entity in entities:
                    if entity['entity_group'] == 'PER' and entity['score'] > 0.8:
                        personal_info['name'] = entity['word']
                        break
            
            # Fallback: extract name from first lines
            if not personal_info['name']:
                lines = text.split('\n')[:5]
                for line in lines:
                    line = line.strip()
                    if len(line) > 5 and len(line) < 50 and not any(char.isdigit() for char in line):
                        # Simple heuristic for name detection
                        words = line.split()
                        if len(words) >= 2 and all(word.istitle() for word in words):
                            personal_info['name'] = line
                            break
            
            # Extract title/headline
            title_patterns = [
                r'(?i)(software engineer|data scientist|product manager|developer|analyst)',
                r'(?i)(senior|junior|lead|principal)\s+\w+',
                r'(?i)\w+\s+(engineer|developer|manager|analyst|consultant)'
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, text[:500])
                if match:
                    personal_info['title'] = match.group().strip()
                    break
            
        except Exception as e:
            logger.error(f"Personal info extraction error: {e}")
        
        return personal_info
    
    def _analyze_skills(self, text: str) -> Dict[str, Any]:
        """Comprehensive skills analysis"""
        skills_analysis = {
            'skills_by_category': {},
            'all_skills': [],
            'skill_proficiency': {},
            'trending_skills': [],
            'skill_density': 0
        }
        
        try:
            text_lower = text.lower()
            
            # Extract skills by category
            for category, skills in self.skill_categories.items():
                found_skills = []
                for skill in skills:
                    if skill.lower() in text_lower:
                        found_skills.append(skill)
                        skills_analysis['all_skills'].append(skill)
                
                if found_skills:
                    skills_analysis['skills_by_category'][category] = found_skills
            
            # Calculate skill proficiency based on context
            for skill in skills_analysis['all_skills']:
                proficiency = self._assess_skill_proficiency(text, skill)
                skills_analysis['skill_proficiency'][skill] = proficiency
            
            # Calculate skill density
            if skills_analysis['all_skills']:
                skills_analysis['skill_density'] = len(skills_analysis['all_skills']) / len(text.split()) * 1000
            
            # Identify trending skills
            trending_tech = ['ai', 'machine learning', 'blockchain', 'cloud', 'kubernetes', 'react', 'tensorflow']
            skills_analysis['trending_skills'] = [skill for skill in trending_tech if skill in text_lower]
            
        except Exception as e:
            logger.error(f"Skills analysis error: {e}")
        
        return skills_analysis
    
    def _assess_skill_proficiency(self, text: str, skill: str) -> str:
        """Assess skill proficiency based on context"""
        skill_contexts = []
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            if skill.lower() in sentence.lower():
                skill_contexts.append(sentence.lower())
        
        if not skill_contexts:
            return 'basic'
        
        # Look for proficiency indicators
        expert_indicators = ['expert', 'advanced', 'lead', 'architect', 'senior', 'proficient', 'extensive']
        intermediate_indicators = ['experience', 'worked with', 'familiar', 'knowledge']
        
        context_text = ' '.join(skill_contexts)
        
        if any(indicator in context_text for indicator in expert_indicators):
            return 'expert'
        elif any(indicator in context_text for indicator in intermediate_indicators):
            return 'intermediate'
        else:
            return 'basic'
    
    def _analyze_experience(self, text: str) -> Dict[str, Any]:
        """Analyze work experience"""
        experience_analysis = {
            'total_years': 0,
            'experience_level': 'entry',
            'job_titles': [],
            'companies': [],
            'key_achievements': [],
            'responsibilities': []
        }
        
        try:
            # Extract years of experience
            year_patterns = [
                r'(\d+)\+?\s*years?\s*(of\s*)?experience',
                r'(\d+)\s*yrs?\s*experience',
                r'experience.*?(\d+)\s*years?'
            ]
            
            for pattern in year_patterns:
                matches = re.findall(pattern, text.lower())
                if matches:
                    years = max([int(match[0] if isinstance(match, tuple) else match) for match in matches])
                    experience_analysis['total_years'] = years
                    break
            
            # Determine experience level
            if experience_analysis['total_years'] >= 8:
                experience_analysis['experience_level'] = 'senior'
            elif experience_analysis['total_years'] >= 3:
                experience_analysis['experience_level'] = 'mid'
            else:
                # Check for experience indicators in text
                text_lower = text.lower()
                for level, indicators in self.experience_indicators.items():
                    if any(indicator in text_lower for indicator in indicators):
                        experience_analysis['experience_level'] = level
                        break
            
            # Extract job titles and companies using NER
            if self.ner_pipeline:
                entities = self.ner_pipeline(text[:2000])
                for entity in entities:
                    if entity['entity_group'] == 'ORG' and entity['score'] > 0.7:
                        company = entity['word']
                        if len(company) > 3 and company not in experience_analysis['companies']:
                            experience_analysis['companies'].append(company)
            
            # Extract job titles using patterns
            title_patterns = [
                r'(?i)(software engineer|data scientist|product manager|developer|analyst|consultant)',
                r'(?i)(senior|junior|lead|principal)\s+\w+\s+(engineer|developer|manager)',
                r'(?i)\w+\s+(engineer|developer|manager|analyst|consultant|specialist)'
            ]
            
            for pattern in title_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    title = match if isinstance(match, str) else ' '.join(match)
                    if title not in experience_analysis['job_titles']:
                        experience_analysis['job_titles'].append(title)
            
            # Extract achievements and responsibilities
            achievement_keywords = ['achieved', 'improved', 'increased', 'reduced', 'led', 'managed', 'created', 'developed']
            sentences = sent_tokenize(text)
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(keyword in sentence_lower for keyword in achievement_keywords):
                    if len(sentence) > 20 and len(sentence) < 200:
                        experience_analysis['key_achievements'].append(sentence.strip())
            
        except Exception as e:
            logger.error(f"Experience analysis error: {e}")
        
        return experience_analysis
    
    def _analyze_education(self, text: str) -> Dict[str, Any]:
        """Analyze educational background"""
        education_analysis = {
            'degrees': [],
            'institutions': [],
            'majors': [],
            'graduation_years': [],
            'certifications': []
        }
        
        try:
            # Degree patterns
            degree_patterns = [
                r'(?i)(bachelor|master|phd|doctorate|mba|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?)',
                r'(?i)(computer science|engineering|mathematics|physics|business|economics)',
                r'(?i)(university|college|institute|school)'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    education_analysis['degrees'].extend([match.strip() for match in matches])
            
            # Extract graduation years
            year_pattern = r'(?:19|20)\d{2}'
            years = re.findall(year_pattern, text)
            education_analysis['graduation_years'] = list(set(years))
            
            # Extract institutions using NER
            if self.ner_pipeline:
                entities = self.ner_pipeline(text)
                for entity in entities:
                    if entity['entity_group'] == 'ORG' and 'university' in entity['word'].lower():
                        education_analysis['institutions'].append(entity['word'])
            
        except Exception as e:
            logger.error(f"Education analysis error: {e}")
        
        return education_analysis
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information"""
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None,
            'location': None
        }
        
        try:
            # Email pattern
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            email_match = re.search(email_pattern, text)
            if email_match:
                contact_info['email'] = email_match.group()
            
            # Phone pattern
            phone_pattern = r'[\+]?[1-9]?[\s\-\.]?[\(]?[0-9]{3}[\)]?[\s\-\.]?[0-9]{3}[\s\-\.]?[0-9]{4}'
            phone_match = re.search(phone_pattern, text)
            if phone_match:
                contact_info['phone'] = phone_match.group()
            
            # LinkedIn profile
            linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
            linkedin_match = re.search(linkedin_pattern, text.lower())
            if linkedin_match:
                contact_info['linkedin'] = linkedin_match.group()
            
            # GitHub profile
            github_pattern = r'github\.com/[\w\-]+'
            github_match = re.search(github_pattern, text.lower())
            if github_match:
                contact_info['github'] = github_match.group()
            
        except Exception as e:
            logger.error(f"Contact info extraction error: {e}")
        
        return contact_info
    
    def _extract_projects(self, text: str) -> List[Dict[str, Any]]:
        """Extract project information"""
        projects = []
        
        try:
            # Look for project sections
            project_keywords = ['project', 'portfolio', 'github', 'built', 'developed', 'created']
            sentences = sent_tokenize(text)
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(keyword in sentence_lower for keyword in project_keywords):
                    if len(sentence) > 30 and len(sentence) < 300:
                        # Extract project details
                        project = {
                            'description': sentence.strip(),
                            'technologies': self._extract_technologies_from_text(sentence)
                        }
                        projects.append(project)
            
        except Exception as e:
            logger.error(f"Project extraction error: {e}")
        
        return projects[:5]  # Limit to 5 projects
    
    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technologies mentioned in text"""
        technologies = []
        text_lower = text.lower()
        
        all_skills = []
        for skills in self.skill_categories.values():
            all_skills.extend(skills)
        
        for skill in all_skills:
            if skill.lower() in text_lower:
                technologies.append(skill)
        
        return technologies
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        
        cert_keywords = [
            'certified', 'certification', 'aws', 'azure', 'google cloud',
            'cisco', 'microsoft', 'oracle', 'pmp', 'scrum master',
            'cissp', 'comptia', 'itil'
        ]
        
        sentences = sent_tokenize(text)
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in cert_keywords):
                if len(sentence) > 10 and len(sentence) < 150:
                    certifications.append(sentence.strip())
        
        return certifications[:3]  # Limit to 3 certifications
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extract key achievements"""
        achievements = []
        
        achievement_patterns = [
            r'achieved \w+',
            r'increased \w+ by \d+%',
            r'reduced \w+ by \d+%',
            r'improved \w+ by \d+%',
            r'led a team of \d+',
            r'managed \$[\d,]+'
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            achievements.extend(matches)
        
        return achievements[:5]  # Limit to 5 achievements
    
    def _assess_resume_quality(self, text: str) -> Dict[str, Any]:
        """Assess overall resume quality"""
        quality_metrics = {
            'length_score': 0,
            'structure_score': 0,
            'keyword_density': 0,
            'contact_completeness': 0,
            'overall_score': 0,
            'quality_grade': 'C',
            'suggestions': []
        }
        
        try:
            word_count = len(text.split())
            
            # Length score (optimal: 400-800 words)
            if 400 <= word_count <= 800:
                quality_metrics['length_score'] = 10
            elif 300 <= word_count < 400 or 800 < word_count <= 1000:
                quality_metrics['length_score'] = 8
            elif 200 <= word_count < 300 or 1000 < word_count <= 1200:
                quality_metrics['length_score'] = 6
            else:
                quality_metrics['length_score'] = 4
            
            # Structure score (check for key sections)
            sections = ['experience', 'education', 'skills', 'contact']
            section_count = sum(1 for section in sections if section in text.lower())
            quality_metrics['structure_score'] = (section_count / len(sections)) * 10
            
            # Keyword density
            tech_keywords = []
            for skills in self.skill_categories.values():
                tech_keywords.extend(skills)
            
            keyword_count = sum(1 for keyword in tech_keywords if keyword.lower() in text.lower())
            quality_metrics['keyword_density'] = min(keyword_count / 10, 1) * 10
            
            # Contact completeness
            contact = self._extract_contact_info(text)
            contact_score = sum(1 for value in contact.values() if value) / len(contact) * 10
            quality_metrics['contact_completeness'] = contact_score
            
            # Overall score
            scores = [
                quality_metrics['length_score'],
                quality_metrics['structure_score'],
                quality_metrics['keyword_density'],
                quality_metrics['contact_completeness']
            ]
            quality_metrics['overall_score'] = sum(scores) / len(scores)
            
            # Grade assignment
            if quality_metrics['overall_score'] >= 9:
                quality_metrics['quality_grade'] = 'A'
            elif quality_metrics['overall_score'] >= 7:
                quality_metrics['quality_grade'] = 'B'
            elif quality_metrics['overall_score'] >= 5:
                quality_metrics['quality_grade'] = 'C'
            else:
                quality_metrics['quality_grade'] = 'D'
            
            # Generate suggestions
            suggestions = []
            if quality_metrics['length_score'] < 8:
                if word_count < 400:
                    suggestions.append("Add more details about your experience and achievements")
                else:
                    suggestions.append("Consider making your resume more concise")
            
            if quality_metrics['structure_score'] < 8:
                suggestions.append("Include clear sections for Experience, Education, and Skills")
            
            if quality_metrics['keyword_density'] < 6:
                suggestions.append("Include more relevant technical keywords and skills")
            
            if quality_metrics['contact_completeness'] < 8:
                suggestions.append("Ensure all contact information is complete")
            
            quality_metrics['suggestions'] = suggestions
            
        except Exception as e:
            logger.error(f"Quality assessment error: {e}")
        
        return quality_metrics
    
    def _generate_summary(self, text: str) -> str:
        """Generate a brief summary of the resume"""
        try:
            # Extract key information
            skills = []
            for category_skills in self.skill_categories.values():
                for skill in category_skills:
                    if skill.lower() in text.lower():
                        skills.append(skill)
            
            experience = self._analyze_experience(text)
            education = self._analyze_education(text)
            
            # Generate summary
            summary_parts = []
            
            if experience['experience_level']:
                summary_parts.append(f"{experience['experience_level'].title()}-level professional")
            
            if skills:
                top_skills = skills[:5]
                summary_parts.append(f"with expertise in {', '.join(top_skills)}")
            
            if experience['total_years'] > 0:
                summary_parts.append(f"with {experience['total_years']} years of experience")
            
            if education['degrees']:
                summary_parts.append(f"holding a {education['degrees'][0]} degree")
            
            summary = ' '.join(summary_parts) + "."
            return summary if len(summary) > 20 else "Professional with diverse technical background."
            
        except Exception as e:
            logger.error(f"Summary generation error: {e}")
            return "Professional with technical background."
    
    def _count_sections(self, text: str) -> int:
        """Count the number of sections in the resume"""
        section_indicators = [
            'experience', 'education', 'skills', 'projects', 'achievements',
            'certifications', 'summary', 'objective', 'contact'
        ]
        
        found_sections = 0
        text_lower = text.lower()
        
        for section in section_indicators:
            if section in text_lower:
                found_sections += 1
        
        return found_sections
