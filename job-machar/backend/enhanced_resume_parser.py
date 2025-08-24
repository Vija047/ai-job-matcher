"""
Enhanced Resume Parser using Hugging Face Models
Focuses on skill extraction and role determination for job matching
Optimized for production use with better error handling
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
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import traceback

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
    Enhanced resume parser using Hugging Face NLP models
    Focused on accurate skill extraction and role determination
    """
    
    def __init__(self):
        print("🚀 Initializing Enhanced Resume Parser...")
        
        # Initialize models with error handling
        self._init_models()
        
        # Comprehensive skill categories and keywords
        self.skill_categories = {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'swift',
                'kotlin', 'typescript', 'php', 'ruby', 'scala', 'r', 'matlab',
                'perl', 'shell', 'bash', 'powershell', 'sql', 'dart', 'objective-c'
            ],
            'web_technologies': [
                'react', 'angular', 'vue.js', 'node.js', 'express', 'django',
                'flask', 'fastapi', 'spring boot', 'asp.net', 'laravel',
                'html', 'css', 'sass', 'less', 'bootstrap', 'tailwind',
                'jquery', 'webpack', 'gulp', 'npm', 'yarn'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite', 'cassandra', 'dynamodb',
                'firebase', 'neo4j', 'influxdb', 'mariadb', 'couchdb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'google cloud', 'gcp', 'heroku', 'vercel',
                'netlify', 'digital ocean', 'linode', 'vultr', 'cloudflare',
                'amazon web services', 'microsoft azure'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions',
                'terraform', 'ansible', 'chef', 'puppet', 'vagrant',
                'prometheus', 'grafana', 'elk stack', 'nagios', 'splunk'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'jupyter', 'tableau', 'power bi', 'spark', 'hadoop',
                'keras', 'xgboost', 'opencv', 'nlp', 'computer vision'
            ],
            'mobile_development': [
                'ios', 'android', 'react native', 'flutter', 'xamarin',
                'ionic', 'cordova', 'swift', 'objective-c', 'kotlin',
                'java android', 'xcode', 'android studio'
            ],
            'testing_qa': [
                'unit testing', 'integration testing', 'selenium', 'jest',
                'pytest', 'junit', 'cucumber', 'cypress', 'postman',
                'mocha', 'chai', 'testing', 'quality assurance', 'qa'
            ],
            'project_management': [
                'agile', 'scrum', 'kanban', 'jira', 'confluence', 'trello',
                'asana', 'project management', 'waterfall', 'lean',
                'product management', 'stakeholder management'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical thinking', 'creativity', 'adaptability',
                'time management', 'critical thinking', 'collaboration'
            ]
        }
        
        # Experience indicators for role determination
        self.experience_indicators = {
            'entry': ['intern', 'junior', 'entry', 'associate', 'trainee', 'graduate', 'assistant'],
            'mid': ['developer', 'engineer', 'analyst', 'specialist', 'consultant', 'coordinator'],
            'senior': ['senior', 'lead', 'principal', 'staff', 'architect', 'manager', 'expert'],
            'executive': ['director', 'vp', 'cto', 'ceo', 'head', 'chief', 'executive']
        }
        
        # Role patterns for intelligent role suggestion
        self.role_patterns = {
            'Software Engineer': ['software', 'programming', 'development', 'coding', 'engineer'],
            'Data Scientist': ['data science', 'machine learning', 'analytics', 'statistics', 'modeling'],
            'Frontend Developer': ['frontend', 'ui', 'ux', 'web design', 'user interface'],
            'Backend Developer': ['backend', 'server', 'api', 'database', 'system'],
            'Full Stack Developer': ['full stack', 'fullstack', 'end-to-end', 'complete'],
            'DevOps Engineer': ['devops', 'infrastructure', 'deployment', 'automation', 'operations'],
            'Product Manager': ['product', 'strategy', 'roadmap', 'requirements', 'business'],
            'Mobile Developer': ['mobile', 'ios', 'android', 'app development'],
            'Machine Learning Engineer': ['ml', 'ai', 'artificial intelligence', 'deep learning'],
            'Cloud Engineer': ['cloud', 'aws', 'azure', 'gcp', 'infrastructure']
        }
        
        print("✅ Enhanced Resume Parser initialized successfully!")
    
    def _init_models(self):
        """Initialize Hugging Face models with better error handling"""
        try:
            # Try to load a lightweight NER model
            print("Loading NLP models...")
            
            # Use a more reliable, smaller model
            try:
                self.ner_pipeline = pipeline(
                    "ner", 
                    model="dbmdz/bert-large-cased-finetuned-conll03-english",
                    aggregation_strategy="simple",
                    device=-1  # Use CPU
                )
                print("✅ NER model loaded successfully")
            except Exception as e:
                print(f"⚠️ NER model failed to load: {e}")
                self.ner_pipeline = None
            
            # Initialize spaCy for additional NLP processing
            try:
                self.nlp = spacy.load("en_core_web_sm")
                print("✅ spaCy model loaded successfully")
            except Exception as e:
                print(f"⚠️ spaCy model failed to load: {e}")
                # Download and try again
                try:
                    os.system("python -m spacy download en_core_web_sm")
                    self.nlp = spacy.load("en_core_web_sm")
                    print("✅ spaCy model downloaded and loaded")
                except:
                    self.nlp = None
                    print("⚠️ spaCy model unavailable")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.ner_pipeline = None
            self.nlp = None
            print("⚠️ Running in fallback mode without advanced models")
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and extract comprehensive information
        Focus on skills and role determination
        """
        try:
            # Extract text from PDF
            text = self._extract_text_from_pdf(file_path)
            
            if not text or len(text.strip()) < 50:
                return {'error': 'Could not extract meaningful text from PDF'}
            
            print(f"📄 Extracted {len(text)} characters from resume")
            
            # Perform comprehensive analysis
            skills_analysis = self._analyze_skills(text)
            experience_analysis = self._analyze_experience(text)
            education_analysis = self._analyze_education(text)
            contact_analysis = self._extract_contact_info(text)
            quality_assessment = self._assess_resume_quality(text, skills_analysis)
            role_suggestion = self._suggest_best_role(skills_analysis, experience_analysis, text)
            
            # Compile comprehensive analysis
            analysis_result = {
                'skills_analysis': skills_analysis,
                'experience_analysis': experience_analysis,
                'education_analysis': education_analysis,
                'contact_analysis': contact_analysis,
                'quality_assessment': quality_assessment,
                'role_suggestion': role_suggestion,
                'text_length': len(text),
                'parsing_timestamp': datetime.now().isoformat(),
                'parser_version': '2.0.0'
            }
            
            print(f"✅ Resume analysis complete: {len(skills_analysis['all_skills'])} skills found")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Resume parsing error: {e}")
            logger.error(traceback.format_exc())
            return {'error': f'Resume parsing failed: {str(e)}'}
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods for reliability"""
        text = ""
        
        # Method 1: pdfplumber (most reliable for complex layouts)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\\n"
            
            if text.strip():
                print("✅ Text extracted using pdfplumber")
                return text
        except Exception as e:
            print(f"⚠️ pdfplumber failed: {e}")
        
        # Method 2: PyMuPDF (good for text extraction)
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\\n"
            doc.close()
            
            if text.strip():
                print("✅ Text extracted using PyMuPDF")
                return text
        except Exception as e:
            print(f"⚠️ PyMuPDF failed: {e}")
        
        # Method 3: PyPDF2 (fallback)
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\\n"
            
            if text.strip():
                print("✅ Text extracted using PyPDF2")
                return text
        except Exception as e:
            print(f"⚠️ PyPDF2 failed: {e}")
        
        return text
    
    def _analyze_skills(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive skill analysis using multiple approaches
        """
        try:
            text_lower = text.lower()
            
            # Method 1: Keyword matching with context
            skills_by_category = {}
            all_skills = []
            
            for category, keywords in self.skill_categories.items():
                found_skills = []
                for keyword in keywords:
                    # Look for exact matches and variations
                    escaped_keyword = re.escape(keyword)
                    escaped_keyword_dots = re.escape(keyword.replace('.', '\\.'))
                    escaped_keyword_dashes = re.escape(keyword.replace(' ', '-'))
                    patterns = [
                        f"\\b{escaped_keyword}\\b",
                        f"\\b{escaped_keyword_dots}\\b",
                        f"\\b{escaped_keyword_dashes}\\b"
                    ]
                    
                    for pattern in patterns:
                        if re.search(pattern, text_lower):
                            found_skills.append(keyword.title())
                            break
                
                if found_skills:
                    skills_by_category[category] = list(set(found_skills))
                    all_skills.extend(found_skills)
            
            # Remove duplicates while preserving order
            all_skills = list(dict.fromkeys(all_skills))
            
            # Method 2: NER-based skill extraction (if available)
            ner_skills = []
            if self.ner_pipeline:
                try:
                    entities = self.ner_pipeline(text[:2000])  # Limit text for performance
                    for entity in entities:
                        if entity['entity_group'] in ['ORG', 'MISC'] and len(entity['word']) > 2:
                            # Check if it might be a technology
                            word = entity['word'].lower()
                            if any(tech in word for tech in ['js', 'py', 'sql', 'api', 'framework']):
                                ner_skills.append(entity['word'])
                except Exception as e:
                    logger.warning(f"NER skill extraction failed: {e}")
            
            # Method 3: spaCy-based extraction (if available)
            spacy_skills = []
            if self.nlp:
                try:
                    doc = self.nlp(text[:2000])  # Limit for performance
                    for ent in doc.ents:
                        if ent.label_ in ['ORG', 'PRODUCT'] and len(ent.text) > 2:
                            spacy_skills.append(ent.text)
                except Exception as e:
                    logger.warning(f"spaCy skill extraction failed: {e}")
            
            # Combine all methods and clean results
            combined_skills = all_skills + ner_skills + spacy_skills
            unique_skills = list(dict.fromkeys([skill for skill in combined_skills if len(skill) > 1]))
            
            # Calculate skill confidence scores
            skill_scores = {}
            for skill in unique_skills:
                score = text_lower.count(skill.lower()) * 0.1
                if skill.lower() in skills_by_category:
                    score += 0.5  # Boost for category matches
                skill_scores[skill] = min(score, 1.0)
            
            return {
                'all_skills': unique_skills,
                'skills_by_category': skills_by_category,
                'total_skills_count': len(unique_skills),
                'skill_scores': skill_scores,
                'top_skills': sorted(unique_skills, key=lambda x: skill_scores.get(x, 0), reverse=True)[:10],
                'skill_density': len(unique_skills) / max(len(text.split()), 1) * 1000  # Skills per 1000 words
            }
            
        except Exception as e:
            logger.error(f"Skill analysis error: {e}")
            return {
                'all_skills': [],
                'skills_by_category': {},
                'total_skills_count': 0,
                'skill_scores': {},
                'top_skills': [],
                'skill_density': 0
            }
    
    def _analyze_experience(self, text: str) -> Dict[str, Any]:
        """Analyze work experience and determine level"""
        try:
            text_lower = text.lower()
            
            # Extract years of experience
            year_patterns = [
                r'(\\d+)\\+?\\s*years?\\s*(?:of\\s*)?(?:experience|exp)',
                r'(\\d+)\\+?\\s*yrs?\\s*(?:of\\s*)?(?:experience|exp)',
                r'(?:over|more than)\\s*(\\d+)\\s*years?',
                r'(\\d{4})\\s*[-–]\\s*(\\d{4}|present|current)',
            ]
            
            years_found = []
            for pattern in year_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        if len(match) == 2 and match[1] in ['present', 'current']:
                            # Calculate years from start year to present
                            try:
                                start_year = int(match[0])
                                current_year = datetime.now().year
                                years = current_year - start_year
                                years_found.append(years)
                            except:
                                pass
                        elif len(match) == 2:
                            # Calculate years between two years
                            try:
                                start_year = int(match[0])
                                end_year = int(match[1])
                                years = end_year - start_year
                                years_found.append(years)
                            except:
                                pass
                    else:
                        try:
                            years_found.append(int(match))
                        except:
                            pass
            
            # Determine experience level
            total_years = max(years_found) if years_found else 0
            
            # Also check for experience level keywords
            level_indicators = {
                'entry': ['intern', 'junior', 'entry level', 'graduate', 'trainee', 'assistant'],
                'mid': ['developer', 'engineer', 'analyst', 'specialist', 'consultant'],
                'senior': ['senior', 'lead', 'principal', 'staff', 'architect', 'manager'],
                'executive': ['director', 'vp', 'cto', 'ceo', 'head of', 'chief']
            }
            
            detected_level = 'mid'  # Default
            for level, indicators in level_indicators.items():
                if any(indicator in text_lower for indicator in indicators):
                    detected_level = level
                    break
            
            # Adjust level based on years of experience
            if total_years == 0:
                experience_level = 'entry'
            elif total_years <= 2:
                experience_level = 'entry'
            elif total_years <= 5:
                experience_level = 'mid'
            elif total_years <= 10:
                experience_level = 'senior'
            else:
                experience_level = 'executive'
            
            # Use keyword-detected level if it's higher
            level_hierarchy = {'entry': 0, 'mid': 1, 'senior': 2, 'executive': 3}
            if level_hierarchy.get(detected_level, 1) > level_hierarchy.get(experience_level, 1):
                experience_level = detected_level
            
            return {
                'total_years': total_years,
                'experience_level': experience_level,
                'years_found': years_found,
                'level_confidence': 0.8 if years_found else 0.4
            }
            
        except Exception as e:
            logger.error(f"Experience analysis error: {e}")
            return {
                'total_years': 0,
                'experience_level': 'mid',
                'years_found': [],
                'level_confidence': 0.0
            }
    
    def _analyze_education(self, text: str) -> Dict[str, Any]:
        """Analyze education background"""
        try:
            text_lower = text.lower()
            
            degrees = []
            degree_patterns = [
                r'\\b(bachelor|ba|bs|b\\.?[as])\\.?\\s+(?:of\\s+)?([^\\n,]+)',
                r'\\b(master|ma|ms|m\\.?[as])\\.?\\s+(?:of\\s+)?([^\\n,]+)',
                r'\\b(phd|ph\\.?d|doctorate|doctor)\\s+(?:of\\s+)?([^\\n,]*)',
                r'\\b(associate|diploma|certificate)\\s+(?:in\\s+)?([^\\n,]+)'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    degree_type = match[0]
                    field = match[1].strip()[:50]  # Limit field length
                    degrees.append({
                        'type': degree_type,
                        'field': field
                    })
            
            # Determine education level
            education_level = 'high_school'
            if any('bachelor' in d['type'] for d in degrees):
                education_level = 'bachelor'
            if any('master' in d['type'] for d in degrees):
                education_level = 'master'
            if any('phd' in d['type'] or 'doctorate' in d['type'] for d in degrees):
                education_level = 'doctorate'
            
            return {
                'degrees': degrees,
                'education_level': education_level,
                'degree_count': len(degrees)
            }
            
        except Exception as e:
            logger.error(f"Education analysis error: {e}")
            return {
                'degrees': [],
                'education_level': 'unknown',
                'degree_count': 0
            }
    
    def _extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information"""
        try:
            contact_info = {}
            
            # Email pattern
            email_pattern = r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'
            emails = re.findall(email_pattern, text)
            if emails:
                contact_info['email'] = emails[0]
            
            # Phone pattern
            phone_pattern = r'\\(?\\d{3}\\)?[-.\s]?\\d{3}[-.\s]?\\d{4}'
            phones = re.findall(phone_pattern, text)
            if phones:
                contact_info['phone'] = phones[0]
            
            # LinkedIn profile
            linkedin_pattern = r'linkedin\\.com/in/([^\\s\\n]+)'
            linkedin_matches = re.findall(linkedin_pattern, text.lower())
            if linkedin_matches:
                contact_info['linkedin'] = f"linkedin.com/in/{linkedin_matches[0]}"
            
            return contact_info
            
        except Exception as e:
            logger.error(f"Contact extraction error: {e}")
            return {}
    
    def _assess_resume_quality(self, text: str, skills_analysis: Dict) -> Dict[str, Any]:
        """Assess overall resume quality"""
        try:
            score = 0
            feedback = []
            
            # Length check
            word_count = len(text.split())
            if word_count > 200:
                score += 20
            else:
                feedback.append("Resume is too short. Add more details about your experience.")
            
            # Skills count
            skill_count = skills_analysis['total_skills_count']
            if skill_count >= 10:
                score += 25
            elif skill_count >= 5:
                score += 15
            else:
                feedback.append("Add more technical skills to strengthen your profile.")
            
            # Structure indicators
            structure_keywords = ['experience', 'education', 'skills', 'projects']
            found_sections = sum(1 for keyword in structure_keywords if keyword in text.lower())
            score += found_sections * 10
            
            if found_sections < 3:
                feedback.append("Include clear sections for Experience, Education, and Skills.")
            
            # Contact information
            if re.search(r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b', text):
                score += 10
            else:
                feedback.append("Include contact information (email).")
            
            # Professional keywords
            professional_keywords = ['achieved', 'developed', 'managed', 'led', 'implemented', 'designed']
            found_professional = sum(1 for keyword in professional_keywords if keyword in text.lower())
            score += min(found_professional * 5, 20)
            
            # Determine grade
            if score >= 80:
                grade = 'A'
            elif score >= 60:
                grade = 'B'
            elif score >= 40:
                grade = 'C'
            else:
                grade = 'D'
            
            return {
                'quality_score': score,
                'quality_grade': grade,
                'word_count': word_count,
                'sections_found': found_sections,
                'feedback': feedback[:3],  # Top 3 suggestions
                'strengths': [
                    f"{skill_count} technical skills identified",
                    f"{word_count} words show good detail level" if word_count > 200 else None,
                    "Well-structured resume" if found_sections >= 3 else None
                ]
            }
            
        except Exception as e:
            logger.error(f"Quality assessment error: {e}")
            return {
                'quality_score': 50,
                'quality_grade': 'C',
                'word_count': 0,
                'sections_found': 0,
                'feedback': ['Unable to assess quality'],
                'strengths': []
            }
    
    def _suggest_best_role(self, skills_analysis: Dict, experience_analysis: Dict, text: str) -> Dict[str, Any]:
        """Suggest the best role based on skills and experience"""
        try:
            all_skills = [skill.lower() for skill in skills_analysis.get('all_skills', [])]
            experience_level = experience_analysis.get('experience_level', 'mid')
            text_lower = text.lower()
            
            # Calculate role scores
            role_scores = {}
            for role, keywords in self.role_patterns.items():
                score = 0
                
                # Check skills match
                for keyword in keywords:
                    if any(keyword in skill for skill in all_skills):
                        score += 2
                    if keyword in text_lower:
                        score += 1
                
                # Normalize score
                role_scores[role] = score / len(keywords)
            
            # Get top 3 roles
            sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
            top_roles = sorted_roles[:3]
            
            # Determine primary suggested role
            if top_roles and top_roles[0][1] > 0.3:
                suggested_role = top_roles[0][0]
                confidence = min(top_roles[0][1], 1.0)
            else:
                # Default based on experience level
                role_defaults = {
                    'entry': 'Junior Software Engineer',
                    'mid': 'Software Engineer',
                    'senior': 'Senior Software Engineer',
                    'executive': 'Engineering Manager'
                }
                suggested_role = role_defaults.get(experience_level, 'Software Engineer')
                confidence = 0.5
            
            # Add experience level prefix
            if experience_level == 'entry' and not suggested_role.startswith('Junior'):
                suggested_role = f"Junior {suggested_role}"
            elif experience_level == 'senior' and not suggested_role.startswith('Senior'):
                suggested_role = f"Senior {suggested_role}"
            elif experience_level == 'executive' and 'Manager' not in suggested_role:
                suggested_role = f"Lead {suggested_role}"
            
            return {
                'primary_role': suggested_role,
                'confidence': confidence,
                'alternative_roles': [role for role, score in top_roles[1:] if score > 0.2],
                'role_scores': dict(top_roles),
                'reasoning': f"Based on {len(all_skills)} skills and {experience_level} experience level"
            }
            
        except Exception as e:
            logger.error(f"Role suggestion error: {e}")
            return {
                'primary_role': 'Software Engineer',
                'confidence': 0.5,
                'alternative_roles': [],
                'role_scores': {},
                'reasoning': 'Default suggestion due to analysis error'
            }

# Test function
if __name__ == "__main__":
    print("Testing Enhanced Resume Parser...")
    parser = AdvancedResumeParser()
    print("Parser initialized successfully!")
