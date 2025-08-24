"""
Enhanced Resume Analyzer with Hugging Face Models
Advanced Resume Analysis using state-of-the-art NLP models from Hugging Face
"""

import os
import re
import numpy as np
from typing import List, Dict, Tuple, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# PDF processing
import PyPDF2
import pdfplumber
import fitz  # PyMuPDF for better text extraction
from PIL import Image
import pytesseract

# NLP libraries
import spacy
import nltk
from textblob import TextBlob

# Hugging Face transformers
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
    pipeline, BertTokenizer, BertModel
)
import torch
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

class EnhancedResumeAnalyzer:
    """
    Enhanced Resume Analyzer using Hugging Face models for advanced NLP tasks
    """
    
    def __init__(self):
        print("🚀 Initializing Enhanced Resume Analyzer with Hugging Face models...")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  spaCy English model not found. Installing...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize Hugging Face models
        self._init_huggingface_models()
        
        # Initialize sentence transformer for semantic analysis
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define enhanced skill categories
        self.skill_categories = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go',
                'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html',
                'css', 'typescript', 'dart', 'perl', 'bash', 'powershell', 'lua',
                'erlang', 'haskell', 'clojure', 'f#', 'assembly', 'cobol', 'fortran'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
                'nodejs', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
                'numpy', 'opencv', 'jquery', 'bootstrap', 'laravel', 'rails',
                'dotnet', '.net', 'hibernate', 'struts', 'fastapi', 'streamlit',
                'gradio', 'huggingface', 'transformers', 'langchain', 'llamaindex'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle',
                'sqlite', 'cassandra', 'dynamodb', 'firebase', 'neo4j', 'influxdb',
                'snowflake', 'bigquery', 'redshift', 'clickhouse', 'couchdb'
            ],
            'cloud_technologies': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
                'jenkins', 'terraform', 'ansible', 'vagrant', 'heroku', 'netlify',
                'cloudflare', 'digitalocean', 'linode', 'vercel', 'serverless'
            ],
            'ai_ml_technologies': [
                'machine learning', 'deep learning', 'neural networks', 'nlp',
                'computer vision', 'generative ai', 'llm', 'gpt', 'bert', 'transformers',
                'hugging face', 'openai', 'anthropic', 'langchain', 'vector databases',
                'embeddings', 'fine-tuning', 'prompt engineering', 'rag', 'mlops'
            ],
            'tools_technologies': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
                'slack', 'trello', 'jenkins', 'travis', 'circleci', 'webpack',
                'babel', 'eslint', 'prettier', 'jest', 'mocha', 'junit', 'postman',
                'swagger', 'figma', 'sketch', 'adobe', 'photoshop', 'illustrator'
            ],
            'soft_skills': [
                'leadership', 'teamwork', 'communication', 'problem-solving',
                'analytical', 'creative', 'adaptable', 'detail-oriented',
                'time management', 'project management', 'collaboration',
                'critical thinking', 'innovation', 'mentoring', 'presentation'
            ],
            'certifications': [
                'aws certified', 'azure certified', 'google cloud certified',
                'certified kubernetes', 'pmp', 'scrum master', 'agile',
                'cissp', 'comptia', 'cisco', 'microsoft certified', 'oracle certified'
            ]
        }
        
        print("✅ Enhanced Resume Analyzer initialized successfully!")
    
    def _init_huggingface_models(self):
        """Initialize Hugging Face models for various NLP tasks"""
        try:
            print("Loading lightweight Hugging Face models...")
            
            # Use smaller, more efficient models
            # Skills extraction model - using smaller model
            try:
                self.skills_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1  # Force CPU usage
                )
                print("✅ Skills classifier loaded")
            except Exception as e:
                print(f"⚠️  Skills classifier failed, using fallback: {e}")
                self.skills_classifier = None
            
            # Use DistilBERT instead of BERT for efficiency
            try:
                self.ner_pipeline = pipeline(
                    "ner",
                    model="distilbert-base-cased",
                    aggregation_strategy="simple",
                    device=-1
                )
                print("✅ NER pipeline loaded")
            except Exception as e:
                print(f"⚠️  NER pipeline failed, using fallback: {e}")
                self.ner_pipeline = None
            
            # Simplified sentiment analysis
            try:
                self.quality_classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1
                )
                print("✅ Quality classifier loaded")
            except Exception as e:
                print(f"⚠️  Quality classifier failed, using fallback: {e}")
                self.quality_classifier = None
            
            # Set other models to None to avoid memory issues
            self.section_classifier = None
            self.experience_classifier = None
            
            print("✅ Lightweight Hugging Face models initialized!")
            
        except Exception as e:
            print(f"⚠️  Error loading Hugging Face models: {e}")
            # Fallback to None for all models
            self.skills_classifier = None
            self.section_classifier = None
            self.ner_pipeline = None
            self.experience_classifier = None
            self.quality_classifier = None
            print("⚠️  Using basic NLP features without Hugging Face models")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Enhanced text extraction from PDF using multiple methods"""
        try:
            text = ""
            
            # Method 1: Try PyMuPDF (best for most PDFs)
            try:
                doc = fitz.open(pdf_path)
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                if text.strip():
                    return text.strip()
            except Exception as e:
                print(f"PyMuPDF failed: {e}")
            
            # Method 2: Try pdfplumber
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                if text.strip():
                    return text.strip()
            except Exception as e:
                print(f"pdfplumber failed: {e}")
            
            # Method 3: Try PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                if text.strip():
                    return text.strip()
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
            
            # Method 4: OCR as last resort (for scanned PDFs)
            try:
                doc = fitz.open(pdf_path)
                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    pix = page.get_pixmap()
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    text += pytesseract.image_to_string(img) + "\n"
                doc.close()
                return text.strip()
            except Exception as e:
                print(f"OCR failed: {e}")
            
            return ""
            
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {e}")
            return ""
    
    def extract_contact_info_enhanced(self, text: str) -> Dict[str, Any]:
        """Enhanced contact information extraction using NER"""
        contact_info = {}
        
        # Use Hugging Face NER if available
        if self.ner_pipeline:
            try:
                entities = self.ner_pipeline(text[:1000])  # Limit text for efficiency
                
                for entity in entities:
                    if entity['entity_group'] == 'PER' and 'name' not in contact_info:
                        contact_info['name'] = entity['word']
                    elif entity['entity_group'] == 'LOC' and 'location' not in contact_info:
                        contact_info['location'] = entity['word']
            except Exception as e:
                print(f"NER extraction failed: {e}")
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Enhanced phone number extraction
        phone_patterns = [
            r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'(\+\d{1,3}[-.\s]?)?\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                contact_info['phone'] = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
                break
        
        # Social media profiles
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = f"https://{linkedin[0]}" if linkedin else None
        
        github_pattern = r'github\.com/[\w-]+'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        contact_info['github'] = f"https://{github[0]}" if github else None
        
        # Portfolio/website
        website_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        websites = re.findall(website_pattern, text)
        contact_info['website'] = websites[0] if websites else None
        
        return contact_info
    
    def extract_skills_enhanced(self, text: str) -> Dict[str, Any]:
        """Enhanced skill extraction using Hugging Face models"""
        extracted_skills = {}
        confidence_scores = {}
        
        # Traditional keyword-based extraction
        text_lower = text.lower()
        for category, skills in self.skill_categories.items():
            found_skills = []
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            extracted_skills[category] = found_skills
        
        # Enhanced extraction using zero-shot classification
        if self.skills_classifier:
            try:
                # Define skill categories for classification
                skill_labels = list(self.skill_categories.keys())
                
                # Split text into chunks for classification
                sentences = [sent.strip() for sent in text.split('.') if len(sent.strip()) > 20]
                
                for sentence in sentences[:10]:  # Limit for efficiency
                    try:
                        result = self.skills_classifier(sentence, skill_labels)
                        if result['scores'][0] > 0.7:  # High confidence threshold
                            category = result['labels'][0]
                            confidence_scores[category] = confidence_scores.get(category, 0) + result['scores'][0]
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"Skills classification failed: {e}")
        
        # Calculate total skills and confidence
        total_skills = sum(len(skills) for skills in extracted_skills.values())
        
        return {
            'skills_by_category': extracted_skills,
            'confidence_scores': confidence_scores,
            'total_skills_found': total_skills,
            'skill_density': total_skills / len(text.split()) if text else 0
        }
    
    def assess_resume_quality(self, text: str) -> Dict[str, Any]:
        """Assess overall resume quality using multiple metrics"""
        quality_metrics = {}
        
        # Basic metrics
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        
        quality_metrics.update({
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': word_count / sentence_count if sentence_count > 0 else 0,
            'readability_score': self._calculate_readability(text)
        })
        
        # Structure assessment
        sections = self._identify_resume_sections(text)
        quality_metrics['sections_found'] = sections
        quality_metrics['section_count'] = len(sections)
        
        # Content quality using Hugging Face model
        if self.quality_classifier:
            try:
                # Analyze sentiment/quality of resume content
                chunks = [text[i:i+500] for i in range(0, len(text), 500)][:5]  # Analyze first 5 chunks
                quality_scores = []
                
                for chunk in chunks:
                    if len(chunk.strip()) > 50:
                        result = self.quality_classifier(chunk)
                        if result[0]['label'] == 'POSITIVE':
                            quality_scores.append(result[0]['score'])
                        else:
                            quality_scores.append(1 - result[0]['score'])
                
                quality_metrics['content_quality_score'] = np.mean(quality_scores) if quality_scores else 0.5
                
            except Exception as e:
                print(f"Quality assessment failed: {e}")
                quality_metrics['content_quality_score'] = 0.5
        
        # Overall quality score
        quality_factors = [
            min(word_count / 300, 1.0),  # Ideal length factor
            min(quality_metrics['section_count'] / 5, 1.0),  # Section completeness
            quality_metrics.get('content_quality_score', 0.5),  # Content quality
            min(quality_metrics['readability_score'] / 50, 1.0)  # Readability factor
        ]
        
        quality_metrics['overall_quality_score'] = np.mean(quality_factors)
        quality_metrics['quality_grade'] = self._get_quality_grade(quality_metrics['overall_quality_score'])
        
        return quality_metrics
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        try:
            blob = TextBlob(text)
            sentences = len(blob.sentences)
            words = len(blob.words)
            syllables = sum([self._count_syllables(str(word)) for word in blob.words])
            
            if sentences == 0 or words == 0:
                return 0
            
            # Flesch Reading Ease formula
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            return max(0, min(100, score))
        except:
            return 50  # Default neutral score
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word"""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count
    
    def _identify_resume_sections(self, text: str) -> List[str]:
        """Identify common resume sections"""
        sections = []
        section_keywords = {
            'contact': ['contact', 'personal information', 'details'],
            'summary': ['summary', 'objective', 'profile', 'about'],
            'experience': ['experience', 'work history', 'employment', 'career'],
            'education': ['education', 'academic', 'qualification', 'degree'],
            'skills': ['skills', 'competencies', 'expertise', 'technologies'],
            'projects': ['projects', 'portfolio', 'work samples'],
            'certifications': ['certifications', 'certificates', 'licenses'],
            'achievements': ['achievements', 'awards', 'accomplishments'],
            'references': ['references', 'recommendations']
        }
        
        text_lower = text.lower()
        for section, keywords in section_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                sections.append(section)
        
        return sections
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert quality score to letter grade"""
        if score >= 0.9:
            return "A+"
        elif score >= 0.8:
            return "A"
        elif score >= 0.7:
            return "B+"
        elif score >= 0.6:
            return "B"
        elif score >= 0.5:
            return "C+"
        elif score >= 0.4:
            return "C"
        else:
            return "D"
    
    def analyze_resume_enhanced(self, pdf_path: str) -> Dict[str, Any]:
        """Complete enhanced resume analysis"""
        print(f"🔍 Analyzing resume with enhanced models: {os.path.basename(pdf_path)}")
        
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return {"error": "Could not extract text from PDF"}
        
        # Perform enhanced analyses
        analysis = {
            'file_path': pdf_path,
            'file_name': os.path.basename(pdf_path),
            'text_length': len(text),
            'word_count': len(text.split()),
            'contact_info': self.extract_contact_info_enhanced(text),
            'skills_analysis': self.extract_skills_enhanced(text),
            'quality_assessment': self.assess_resume_quality(text),
            'raw_text': text[:2000] + "..." if len(text) > 2000 else text  # More text for context
        }
        
        # Generate semantic embedding for the entire resume
        try:
            analysis['resume_embedding'] = self.sentence_model.encode([text[:1000]])[0].tolist()
        except Exception as e:
            print(f"Embedding generation failed: {e}")
            analysis['resume_embedding'] = None
        
        # Add summary statistics
        analysis['summary'] = {
            'total_skills': analysis['skills_analysis']['total_skills_found'],
            'quality_grade': analysis['quality_assessment']['quality_grade'],
            'sections_found': len(analysis['quality_assessment']['sections_found']),
            'readability_score': analysis['quality_assessment']['readability_score']
        }
        
        print(f"✅ Enhanced analysis complete! Quality: {analysis['summary']['quality_grade']}")
        return analysis
