"""
Automated Job Application System
Helps users apply to jobs with automated form filling and personalized applications
"""

import time
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import requests
from transformers import pipeline

@dataclass
class ApplicationData:
    """Data structure for job application information"""
    name: str
    email: str
    phone: str
    resume_path: str
    cover_letter: str
    linkedin_url: str = ""
    portfolio_url: str = ""
    expected_salary: str = ""
    availability: str = ""

class JobApplicationAssistant:
    """
    Automated job application assistant that helps with form filling and application tracking
    """
    
    def __init__(self):
        self.setup_selenium()
        self.setup_ai_models()
        self.application_history = []
        
    def setup_selenium(self):
        """Setup Selenium WebDriver for browser automation"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Setup Chrome driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            print("✅ Browser automation setup complete")
            
        except Exception as e:
            print(f"⚠️  Browser setup failed: {e}")
            self.driver = None
            self.wait = None
    
    def setup_ai_models(self):
        """Setup AI models for content generation"""
        try:
            # Cover letter generation model
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                max_length=500,
                device=-1  # Use CPU
            )
            
            print("✅ AI models setup complete")
            
        except Exception as e:
            print(f"⚠️  AI models setup failed: {e}")
            self.text_generator = None
    
    def generate_cover_letter(
        self, 
        job_title: str, 
        company: str, 
        job_description: str,
        user_profile: Dict[str, Any]
    ) -> str:
        """Generate a personalized cover letter using AI"""
        
        try:
            # Extract key skills from user profile
            user_skills = []
            if 'skills_analysis' in user_profile:
                for category_skills in user_profile['skills_analysis']['skills_by_category'].values():
                    user_skills.extend(category_skills)
            
            # Create a structured prompt
            prompt = f"""
            Dear Hiring Manager,
            
            I am writing to express my strong interest in the {job_title} position at {company}. 
            
            With my background in {', '.join(user_skills[:3]) if user_skills else 'software development'}, 
            I am confident that I would be a valuable addition to your team.
            
            """
            
            # Use AI to generate additional content if available
            if self.text_generator:
                try:
                    generated = self.text_generator(
                        prompt,
                        max_length=300,
                        num_return_sequences=1,
                        temperature=0.7,
                        pad_token_id=50256
                    )
                    ai_content = generated[0]['generated_text']
                    
                    # Clean up the generated content
                    lines = ai_content.split('\n')
                    clean_lines = [line.strip() for line in lines if line.strip()]
                    cover_letter = '\n\n'.join(clean_lines[:10])  # Limit length
                    
                except Exception as e:
                    print(f"AI generation failed: {e}")
                    cover_letter = self._generate_template_cover_letter(job_title, company, user_skills)
            else:
                cover_letter = self._generate_template_cover_letter(job_title, company, user_skills)
            
            # Add closing
            cover_letter += f"""
            
            I am excited about the opportunity to contribute to {company}'s continued success and would welcome 
            the chance to discuss how my skills and enthusiasm can benefit your team.
            
            Thank you for considering my application. I look forward to hearing from you soon.
            
            Best regards,
            {user_profile.get('contact_info', {}).get('name', 'Your Name')}
            """
            
            return cover_letter.strip()
            
        except Exception as e:
            print(f"Cover letter generation failed: {e}")
            return self._generate_template_cover_letter(job_title, company, user_skills)
    
    def _generate_template_cover_letter(self, job_title: str, company: str, user_skills: List[str]) -> str:
        """Generate a template-based cover letter"""
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. 

With my experience in {', '.join(user_skills[:3]) if user_skills else 'software development'}, 
I am confident that I can contribute effectively to your team's success.

Key qualifications I bring include:
• Strong technical skills in {', '.join(user_skills[:5]) if user_skills else 'relevant technologies'}
• Experience working in collaborative team environments
• Passion for continuous learning and professional growth
• Strong problem-solving and analytical abilities

I am particularly drawn to {company} because of your reputation for innovation and excellence 
in the industry. I am excited about the opportunity to contribute to your team's continued success.

Thank you for considering my application. I look forward to the opportunity to discuss 
how my skills and enthusiasm can benefit your organization.

Best regards,"""
    
    def prepare_application_data(self, user_profile: Dict[str, Any], resume_path: str) -> ApplicationData:
        """Prepare application data from user profile"""
        contact_info = user_profile.get('contact_info', {})
        
        return ApplicationData(
            name=contact_info.get('name', ''),
            email=contact_info.get('email', ''),
            phone=contact_info.get('phone', ''),
            resume_path=resume_path,
            cover_letter="",  # Will be generated per job
            linkedin_url=contact_info.get('linkedin', ''),
            portfolio_url=contact_info.get('website', ''),
            expected_salary="Negotiable",
            availability="Immediate"
        )
    
    def apply_to_job(
        self, 
        job_url: str, 
        application_data: ApplicationData,
        job_title: str,
        company: str,
        job_description: str,
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply to a job automatically"""
        
        if not self.driver:
            return {
                'success': False,
                'error': 'Browser automation not available',
                'manual_application_guide': self._generate_manual_application_guide(
                    job_url, application_data, job_title, company
                )
            }
        
        try:
            print(f"🔄 Applying to {job_title} at {company}...")
            
            # Generate personalized cover letter
            cover_letter = self.generate_cover_letter(job_title, company, job_description, user_profile)
            application_data.cover_letter = cover_letter
            
            # Navigate to job URL
            self.driver.get(job_url)
            time.sleep(3)
            
            # Detect job board type and apply accordingly
            if 'linkedin.com' in job_url:
                result = self._apply_linkedin(application_data, job_title, company)
            elif 'indeed.com' in job_url:
                result = self._apply_indeed(application_data, job_title, company)
            elif 'glassdoor.com' in job_url:
                result = self._apply_glassdoor(application_data, job_title, company)
            else:
                result = self._apply_generic(application_data, job_title, company)
            
            # Record application
            self._record_application(job_url, job_title, company, result)
            
            return result
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'manual_application_guide': self._generate_manual_application_guide(
                    job_url, application_data, job_title, company
                )
            }
            self._record_application(job_url, job_title, company, error_result)
            return error_result
    
    def _apply_linkedin(self, application_data: ApplicationData, job_title: str, company: str) -> Dict[str, Any]:
        """Apply to LinkedIn job posting"""
        try:
            # Look for "Easy Apply" button
            easy_apply_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            easy_apply_btn.click()
            time.sleep(2)
            
            # Fill application form
            self._fill_linkedin_form(application_data)
            
            return {
                'success': True,
                'message': f'Successfully applied to {job_title} at {company} via LinkedIn Easy Apply',
                'application_method': 'LinkedIn Easy Apply'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'LinkedIn application failed: {str(e)}',
                'manual_application_guide': self._generate_manual_application_guide(
                    self.driver.current_url, application_data, job_title, company
                )
            }
    
    def _apply_indeed(self, application_data: ApplicationData, job_title: str, company: str) -> Dict[str, Any]:
        """Apply to Indeed job posting"""
        try:
            # Look for "Apply Now" button
            apply_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply now')]"))
            )
            apply_btn.click()
            time.sleep(2)
            
            # Fill Indeed application form
            self._fill_indeed_form(application_data)
            
            return {
                'success': True,
                'message': f'Successfully applied to {job_title} at {company} via Indeed',
                'application_method': 'Indeed Apply'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Indeed application failed: {str(e)}',
                'manual_application_guide': self._generate_manual_application_guide(
                    self.driver.current_url, application_data, job_title, company
                )
            }
    
    def _apply_glassdoor(self, application_data: ApplicationData, job_title: str, company: str) -> Dict[str, Any]:
        """Apply to Glassdoor job posting"""
        try:
            # Look for apply button
            apply_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'apply')]"))
            )
            apply_btn.click()
            time.sleep(2)
            
            # Fill Glassdoor form
            self._fill_glassdoor_form(application_data)
            
            return {
                'success': True,
                'message': f'Successfully applied to {job_title} at {company} via Glassdoor',
                'application_method': 'Glassdoor Apply'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Glassdoor application failed: {str(e)}',
                'manual_application_guide': self._generate_manual_application_guide(
                    self.driver.current_url, application_data, job_title, company
                )
            }
    
    def _apply_generic(self, application_data: ApplicationData, job_title: str, company: str) -> Dict[str, Any]:
        """Apply to generic job posting"""
        try:
            # Look for common apply button text
            apply_selectors = [
                "//button[contains(text(), 'Apply')]",
                "//a[contains(text(), 'Apply')]",
                "//input[@type='submit' and contains(@value, 'Apply')]",
                "//button[contains(@class, 'apply')]"
            ]
            
            apply_btn = None
            for selector in apply_selectors:
                try:
                    apply_btn = self.driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
            
            if apply_btn:
                apply_btn.click()
                time.sleep(2)
                
                # Try to fill generic form
                self._fill_generic_form(application_data)
                
                return {
                    'success': True,
                    'message': f'Applied to {job_title} at {company}',
                    'application_method': 'Generic Application'
                }
            else:
                raise Exception("Could not find apply button")
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Generic application failed: {str(e)}',
                'manual_application_guide': self._generate_manual_application_guide(
                    self.driver.current_url, application_data, job_title, company
                )
            }
    
    def _fill_linkedin_form(self, application_data: ApplicationData):
        """Fill LinkedIn Easy Apply form"""
        # This is a simplified implementation
        # In reality, LinkedIn forms are complex and dynamic
        
        # Fill phone number if present
        try:
            phone_field = self.driver.find_element(By.XPATH, "//input[contains(@id, 'phone')]")
            phone_field.clear()
            phone_field.send_keys(application_data.phone)
        except:
            pass
        
        # Upload resume if file input is present
        try:
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            if os.path.exists(application_data.resume_path):
                file_input.send_keys(application_data.resume_path)
        except:
            pass
        
        # Submit application
        try:
            submit_btn = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
            submit_btn.click()
        except:
            # Try alternative submit button
            submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
            submit_btn.click()
    
    def _fill_indeed_form(self, application_data: ApplicationData):
        """Fill Indeed application form"""
        # Fill common fields
        self._fill_common_fields(application_data)
        
        # Indeed-specific form handling
        try:
            # Cover letter
            cover_letter_field = self.driver.find_element(By.XPATH, "//textarea[contains(@name, 'cover')]")
            cover_letter_field.clear()
            cover_letter_field.send_keys(application_data.cover_letter)
        except:
            pass
    
    def _fill_glassdoor_form(self, application_data: ApplicationData):
        """Fill Glassdoor application form"""
        self._fill_common_fields(application_data)
    
    def _fill_generic_form(self, application_data: ApplicationData):
        """Fill generic application form"""
        self._fill_common_fields(application_data)
    
    def _fill_common_fields(self, application_data: ApplicationData):
        """Fill common form fields across job boards"""
        field_mappings = [
            ('name', application_data.name),
            ('email', application_data.email),
            ('phone', application_data.phone),
            ('linkedin', application_data.linkedin_url),
            ('portfolio', application_data.portfolio_url),
            ('salary', application_data.expected_salary)
        ]
        
        for field_type, value in field_mappings:
            if not value:
                continue
                
            # Try multiple selector patterns for each field
            selectors = [
                f"//input[contains(@name, '{field_type}')]",
                f"//input[contains(@id, '{field_type}')]",
                f"//input[contains(@placeholder, '{field_type}')]"
            ]
            
            for selector in selectors:
                try:
                    field = self.driver.find_element(By.XPATH, selector)
                    field.clear()
                    field.send_keys(value)
                    break
                except:
                    continue
        
        # Upload resume
        try:
            file_input = self.driver.find_element(By.XPATH, "//input[@type='file']")
            if os.path.exists(application_data.resume_path):
                file_input.send_keys(application_data.resume_path)
        except:
            pass
    
    def _generate_manual_application_guide(
        self, 
        job_url: str, 
        application_data: ApplicationData,
        job_title: str,
        company: str
    ) -> Dict[str, Any]:
        """Generate manual application guide when automation fails"""
        return {
            'job_url': job_url,
            'job_title': job_title,
            'company': company,
            'steps': [
                f"1. Open the job URL: {job_url}",
                "2. Look for the 'Apply' button on the job posting",
                "3. Fill in your personal information:",
                f"   - Name: {application_data.name}",
                f"   - Email: {application_data.email}",
                f"   - Phone: {application_data.phone}",
                "4. Upload your resume",
                "5. Copy and paste the cover letter below",
                "6. Submit the application"
            ],
            'cover_letter': application_data.cover_letter,
            'additional_info': {
                'linkedin': application_data.linkedin_url,
                'portfolio': application_data.portfolio_url,
                'expected_salary': application_data.expected_salary,
                'availability': application_data.availability
            }
        }
    
    def _record_application(self, job_url: str, job_title: str, company: str, result: Dict[str, Any]):
        """Record application attempt for tracking"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'job_url': job_url,
            'job_title': job_title,
            'company': company,
            'success': result.get('success', False),
            'method': result.get('application_method', 'Unknown'),
            'error': result.get('error', None)
        }
        
        self.application_history.append(record)
        
        # Save to file for persistence
        try:
            with open('application_history.json', 'w') as f:
                json.dump(self.application_history, f, indent=2)
        except Exception as e:
            print(f"Failed to save application history: {e}")
    
    def get_application_history(self) -> List[Dict[str, Any]]:
        """Get application history"""
        return self.application_history
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        total_applications = len(self.application_history)
        successful_applications = sum(1 for app in self.application_history if app['success'])
        
        return {
            'total_applications': total_applications,
            'successful_applications': successful_applications,
            'success_rate': successful_applications / total_applications if total_applications > 0 else 0,
            'most_recent': self.application_history[-1] if self.application_history else None
        }
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            self.driver.quit()
    
    def __del__(self):
        """Destructor to cleanup resources"""
        self.cleanup()
