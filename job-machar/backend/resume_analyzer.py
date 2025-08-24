"""
Resume Analyzer Module
Comprehensive Resume Analyzer that extracts and analyzes key information from resumes
"""

import os
import re
import numpy as np
from typing import List, Dict, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# PDF processing
import PyPDF2
import pdfplumber

# NLP libraries
import spacy
import nltk
from textblob import TextBlob
from sentence_transformers import SentenceTransformer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

class ResumeAnalyzer:
    """
    Comprehensive Resume Analyzer that extracts and analyzes key information from resumes
    """
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  spaCy English model not found. Installing...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize sentence transformer for semantic analysis
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define skill categories and keywords
        self.skill_categories = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go',
                'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html',
                'css', 'typescript', 'dart', 'perl', 'bash', 'powershell'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
                'nodejs', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
                'numpy', 'opencv', 'jquery', 'bootstrap', 'laravel', 'rails',
                'dotnet', '.net', 'hibernate', 'struts'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle',
                'sqlite', 'cassandra', 'dynamodb', 'firebase', 'neo4j', 'influxdb'
            ],
            'cloud_technologies': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
                'jenkins', 'terraform', 'ansible', 'vagrant', 'heroku', 'netlify'
            ],
            'tools_technologies': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
                'slack', 'trello', 'jenkins', 'travis', 'circleci', 'webpack',
                'babel', 'eslint', 'prettier', 'jest', 'mocha', 'junit'
            ],
            'soft_skills': [
                'leadership', 'teamwork', 'communication', 'problem-solving',
                'analytical', 'creative', 'adaptable', 'detail-oriented',
                'time management', 'project management', 'collaboration'
            ]
        }
        
        # Education keywords
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'diploma', 'certificate',
            'degree', 'university', 'college', 'institute', 'school'
        ]
        
        # Experience level indicators
        self.experience_indicators = {
            'entry': ['intern', 'trainee', 'junior', 'entry', 'associate', 'assistant'],
            'mid': ['developer', 'engineer', 'analyst', 'specialist', 'coordinator'],
            'senior': ['senior', 'lead', 'principal', 'architect', 'manager', 'director'],
            'executive': ['cto', 'ceo', 'cfo', 'vp', 'vice president', 'head of', 'chief']
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            # If PyPDF2 fails, try pdfplumber
            if not text.strip():
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {e}")
            return ""
    
    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Phone number extraction
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info['phone'] = phones[0] if phones else None
        
        # LinkedIn profile extraction
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = linkedin[0] if linkedin else None
        
        # GitHub profile extraction
        github_pattern = r'github\.com/[\w-]+'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        contact_info['github'] = github[0] if github else None
        
        return contact_info
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills categorized by type"""
        text_lower = text.lower()
        extracted_skills = {}
        
        for category, skills in self.skill_categories.items():
            found_skills = []
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            extracted_skills[category] = found_skills
        
        return extracted_skills
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        doc = self.nlp(text)
        
        # Look for education section
        education_section = ""
        lines = text.split('\n')
        capture = False
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['education', 'academic', 'qualification']):
                capture = True
            elif capture and any(keyword in line.lower() for keyword in ['experience', 'work', 'employment', 'project']):
                break
            elif capture:
                education_section += line + "\n"
        
        # Extract degrees and institutions
        degree_pattern = r'(bachelor|master|phd|doctorate|diploma|certificate|degree|b\.?[aestcm]\.?|m\.?[aestcm]\.?|ph\.?d\.?)'
        degrees = re.findall(degree_pattern, education_section, re.IGNORECASE)
        
        # Extract years
        year_pattern = r'(19|20)\d{2}'
        years = re.findall(year_pattern, education_section)
        
        if degrees:
            education.append({
                'degree': degrees[0] if degrees else 'Not specified',
                'year': years[-1] if years else 'Not specified',
                'details': education_section.strip()
            })
        
        return education
    
    def assess_experience_level(self, text: str) -> Dict[str, Any]:
        """Assess experience level based on keywords and context"""
        text_lower = text.lower()
        experience_scores = {level: 0 for level in self.experience_indicators.keys()}
        
        # Count experience indicators
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                experience_scores[level] += text_lower.count(indicator.lower())
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?\s*of?\s*experience',
            r'(\d+)\+?\s*years?\s*in',
            r'experience.*?(\d+)\+?\s*years?'
        ]
        
        years_found = []
        for pattern in year_patterns:
            matches = re.findall(pattern, text_lower)
            years_found.extend([int(year) for year in matches])
        
        max_years = max(years_found) if years_found else 0
        
        # Determine primary experience level
        primary_level = max(experience_scores.keys(), key=lambda k: experience_scores[k])
        
        return {
            'primary_level': primary_level,
            'years_of_experience': max_years,
            'level_scores': experience_scores,
            'confidence': max(experience_scores.values()) / (sum(experience_scores.values()) + 1)
        }
    
    def analyze_resume(self, pdf_path: str) -> Dict[str, Any]:
        """Complete resume analysis"""
        print(f"🔍 Analyzing resume: {os.path.basename(pdf_path)}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {"error": "Could not extract text from PDF"}
        
        # Perform all analyses
        analysis = {
            'file_path': pdf_path,
            'text_length': len(text),
            'contact_info': self.extract_contact_info(text),
            'skills': self.extract_skills(text),
            'education': self.extract_education(text),
            'experience': self.assess_experience_level(text),
            'raw_text': text[:1000] + "..." if len(text) > 1000 else text  # Truncate for display
        }
        
        # Calculate overall skill count
        total_skills = sum(len(skills) for skills in analysis['skills'].values())
        analysis['total_skills_found'] = total_skills
        
        print(f"✅ Analysis complete! Found {total_skills} skills")
        return analysis
