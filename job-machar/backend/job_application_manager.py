"""
Job Application Manager
Handles job applications, tracking, and bulk application features
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class ApplicationStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"

@dataclass
class JobApplication:
    """Job application data structure"""
    id: str
    job_id: str
    job_title: str
    company: str
    applied_date: datetime
    status: ApplicationStatus
    cover_letter: Optional[str] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    salary_negotiation: Optional[Dict] = None
    documents: List[str] = None
    
    def __post_init__(self):
        if self.documents is None:
            self.documents = []

class JobApplicationManager:
    """
    Manages job applications, tracking, and bulk application features
    """
    
    def __init__(self):
        self.applications: Dict[str, JobApplication] = {}
        self.saved_jobs: Dict[str, Dict] = {}
        self.application_templates = {}
        self.bulk_apply_queue: List[str] = []
        
    def save_job_for_later(self, job: Dict, folder: str = "default") -> Dict[str, Any]:
        """Save a job for later application"""
        try:
            job_id = job.get('id', str(uuid.uuid4()))
            
            saved_job = {
                **job,
                'saved_date': datetime.now(),
                'folder': folder,
                'notes': '',
                'priority': 'medium',
                'reminder_date': None
            }
            
            self.saved_jobs[job_id] = saved_job
            
            return {
                'success': True,
                'message': f"Job saved to {folder} folder",
                'job_id': job_id,
                'saved_count': len(self.saved_jobs)
            }
            
        except Exception as e:
            logger.error(f"Error saving job: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_saved_jobs(self, folder: str = None) -> Dict[str, Any]:
        """Get saved jobs, optionally filtered by folder"""
        try:
            if folder:
                filtered_jobs = {
                    job_id: job for job_id, job in self.saved_jobs.items()
                    if job.get('folder') == folder
                }
            else:
                filtered_jobs = self.saved_jobs
            
            # Group by folder
            folders = {}
            for job_id, job in filtered_jobs.items():
                folder_name = job.get('folder', 'default')
                if folder_name not in folders:
                    folders[folder_name] = []
                folders[folder_name].append({**job, 'id': job_id})
            
            return {
                'success': True,
                'folders': folders,
                'total_saved': len(filtered_jobs)
            }
            
        except Exception as e:
            logger.error(f"Error getting saved jobs: {e}")
            return {
                'success': False,
                'error': str(e),
                'folders': {},
                'total_saved': 0
            }
    
    def create_application_draft(self, job: Dict, user_profile: Dict) -> Dict[str, Any]:
        """Create a draft application for a job"""
        try:
            application_id = str(uuid.uuid4())
            job_id = job.get('id', str(uuid.uuid4()))
            
            # Generate cover letter template
            cover_letter = self._generate_cover_letter(job, user_profile)
            
            application = JobApplication(
                id=application_id,
                job_id=job_id,
                job_title=job.get('title', ''),
                company=job.get('company', ''),
                applied_date=datetime.now(),
                status=ApplicationStatus.DRAFT,
                cover_letter=cover_letter,
                resume_version=user_profile.get('resume_version', 'default'),
                notes=f"Application draft created for {job.get('title', 'position')}"
            )
            
            self.applications[application_id] = application
            
            return {
                'success': True,
                'application_id': application_id,
                'application': asdict(application),
                'estimated_completion_time': '5-10 minutes',
                'checklist': self._get_application_checklist(job),
                'tips': self._get_application_tips(job, user_profile)
            }
            
        except Exception as e:
            logger.error(f"Error creating application draft: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def submit_application(self, application_id: str, final_data: Dict) -> Dict[str, Any]:
        """Submit a job application"""
        try:
            if application_id not in self.applications:
                return {
                    'success': False,
                    'error': 'Application not found'
                }
            
            application = self.applications[application_id]
            
            # Update application with final data
            application.cover_letter = final_data.get('cover_letter', application.cover_letter)
            application.resume_version = final_data.get('resume_version', application.resume_version)
            application.notes = final_data.get('notes', application.notes)
            application.status = ApplicationStatus.SUBMITTED
            application.applied_date = datetime.now()
            
            # Set follow-up reminder (1 week from now)
            application.follow_up_date = datetime.now() + timedelta(days=7)
            
            return {
                'success': True,
                'message': f"Application submitted for {application.job_title} at {application.company}",
                'application_id': application_id,
                'follow_up_date': application.follow_up_date.isoformat(),
                'next_steps': [
                    'Application submitted successfully',
                    'Follow-up reminder set for next week',
                    'Continue applying to similar positions',
                    'Prepare for potential interviews'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def setup_bulk_apply(self, job_ids: List[str], user_profile: Dict) -> Dict[str, Any]:
        """Setup bulk application for multiple jobs"""
        try:
            if len(job_ids) > 5:
                return {
                    'success': False,
                    'error': 'Maximum 5 applications allowed in bulk apply'
                }
            
            bulk_session_id = str(uuid.uuid4())
            applications = []
            
            for job_id in job_ids:
                # Create draft applications
                if job_id in self.saved_jobs:
                    job = self.saved_jobs[job_id]
                    draft_result = self.create_application_draft(job, user_profile)
                    if draft_result['success']:
                        applications.append(draft_result['application'])
            
            self.bulk_apply_queue = [app['id'] for app in applications]
            
            return {
                'success': True,
                'bulk_session_id': bulk_session_id,
                'applications': applications,
                'total_applications': len(applications),
                'estimated_time': f"{len(applications) * 3}-{len(applications) * 5} minutes",
                'bulk_apply_tips': [
                    'Review each cover letter for company-specific details',
                    'Ensure your resume highlights relevant skills for each role',
                    'Apply to most preferred positions first',
                    'Keep track of application deadlines'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error setting up bulk apply: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_bulk_apply(self, bulk_session_id: str, applications_data: List[Dict]) -> Dict[str, Any]:
        """Execute bulk application submission"""
        try:
            successful_applications = []
            failed_applications = []
            
            for app_data in applications_data:
                app_id = app_data.get('application_id')
                if app_id in self.bulk_apply_queue:
                    result = self.submit_application(app_id, app_data)
                    if result['success']:
                        successful_applications.append(app_id)
                    else:
                        failed_applications.append({'id': app_id, 'error': result['error']})
            
            # Clear bulk apply queue
            self.bulk_apply_queue = []
            
            return {
                'success': True,
                'successful_applications': len(successful_applications),
                'failed_applications': len(failed_applications),
                'failures': failed_applications,
                'total_submitted': len(successful_applications),
                'summary': f"Successfully submitted {len(successful_applications)} applications"
            }
            
        except Exception as e:
            logger.error(f"Error executing bulk apply: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def track_application_status(self, application_id: str, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Update application status"""
        try:
            if application_id not in self.applications:
                return {
                    'success': False,
                    'error': 'Application not found'
                }
            
            application = self.applications[application_id]
            old_status = application.status
            
            # Update status
            try:
                application.status = ApplicationStatus(new_status)
            except ValueError:
                return {
                    'success': False,
                    'error': f'Invalid status: {new_status}'
                }
            
            # Add notes
            if notes:
                current_notes = application.notes or ""
                application.notes = f"{current_notes}\n[{datetime.now().strftime('%Y-%m-%d')}] {notes}"
            
            # Set interview reminder if interview scheduled
            if application.status == ApplicationStatus.INTERVIEW_SCHEDULED:
                application.interview_date = datetime.now() + timedelta(days=3)  # Default to 3 days
            
            return {
                'success': True,
                'message': f"Status updated from {old_status.value} to {new_status}",
                'application': asdict(application),
                'next_actions': self._get_next_actions(application.status)
            }
            
        except Exception as e:
            logger.error(f"Error tracking application status: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_application_dashboard(self) -> Dict[str, Any]:
        """Get application dashboard with statistics and insights"""
        try:
            total_applications = len(self.applications)
            if total_applications == 0:
                return {
                    'success': True,
                    'message': 'No applications found',
                    'stats': {},
                    'recent_activity': [],
                    'upcoming_actions': []
                }
            
            # Calculate statistics
            status_counts = {}
            for app in self.applications.values():
                status = app.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Recent activity (last 30 days)
            recent_apps = [
                app for app in self.applications.values()
                if app.applied_date > (datetime.now() - timedelta(days=30))
            ]
            
            # Upcoming actions
            upcoming_actions = []
            for app in self.applications.values():
                if app.follow_up_date and app.follow_up_date > datetime.now():
                    upcoming_actions.append({
                        'action': 'Follow up',
                        'job_title': app.job_title,
                        'company': app.company,
                        'date': app.follow_up_date.isoformat()
                    })
                if app.interview_date and app.interview_date > datetime.now():
                    upcoming_actions.append({
                        'action': 'Interview',
                        'job_title': app.job_title,
                        'company': app.company,
                        'date': app.interview_date.isoformat()
                    })
            
            # Success rate
            submitted_count = status_counts.get('submitted', 0) + status_counts.get('under_review', 0)
            interview_count = status_counts.get('interview_scheduled', 0)
            success_rate = (interview_count / submitted_count * 100) if submitted_count > 0 else 0
            
            return {
                'success': True,
                'stats': {
                    'total_applications': total_applications,
                    'status_breakdown': status_counts,
                    'recent_applications': len(recent_apps),
                    'success_rate': round(success_rate, 1),
                    'pending_follow_ups': len([a for a in upcoming_actions if a['action'] == 'Follow up']),
                    'upcoming_interviews': len([a for a in upcoming_actions if a['action'] == 'Interview'])
                },
                'recent_activity': [
                    {
                        'job_title': app.job_title,
                        'company': app.company,
                        'status': app.status.value,
                        'applied_date': app.applied_date.isoformat()
                    }
                    for app in sorted(recent_apps, key=lambda x: x.applied_date, reverse=True)[:5]
                ],
                'upcoming_actions': sorted(upcoming_actions, key=lambda x: x['date'])[:10],
                'insights': self._generate_application_insights(status_counts, success_rate)
            }
            
        except Exception as e:
            logger.error(f"Error getting application dashboard: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_cover_letter(self, job: Dict, user_profile: Dict) -> str:
        """Generate a personalized cover letter"""
        template = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.get('title', '[JOB_TITLE]')} position at {job.get('company', '[COMPANY_NAME]')}. With my background in {user_profile.get('primary_skills', '[YOUR_SKILLS]')} and {user_profile.get('years_experience', 'X')} years of experience, I am excited about the opportunity to contribute to your team.

{job.get('company', '[COMPANY_NAME]')} has always impressed me with [RESEARCH COMPANY - add specific details about the company]. I am particularly drawn to this role because [CUSTOMIZE - explain why this specific position interests you].

In my previous experience, I have [ADD RELEVANT ACHIEVEMENT]. This background has prepared me well for the challenges of this position, particularly [MENTION SPECIFIC JOB REQUIREMENTS YOU CAN ADDRESS].

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to {job.get('company', '[COMPANY_NAME]')}'s continued success. Thank you for considering my application.

Best regards,
{user_profile.get('name', '[YOUR_NAME]')}"""
        
        return template
    
    def _get_application_checklist(self, job: Dict) -> List[Dict[str, Any]]:
        """Get application checklist for a specific job"""
        return [
            {"item": "Review job description thoroughly", "completed": False, "priority": "High"},
            {"item": "Customize resume for this position", "completed": False, "priority": "High"},
            {"item": "Write personalized cover letter", "completed": False, "priority": "High"},
            {"item": "Research company background", "completed": False, "priority": "Medium"},
            {"item": "Prepare work portfolio/samples", "completed": False, "priority": "Medium"},
            {"item": "Practice common interview questions", "completed": False, "priority": "Low"},
            {"item": "Prepare questions to ask interviewer", "completed": False, "priority": "Low"}
        ]
    
    def _get_application_tips(self, job: Dict, user_profile: Dict) -> List[str]:
        """Get personalized application tips"""
        tips = [
            f"Highlight your {user_profile.get('primary_skills', 'relevant skills')} in your application",
            f"Research {job.get('company', 'the company')} recent news and achievements",
            "Quantify your achievements with specific numbers and results"
        ]
        
        if job.get('remote_allowed'):
            tips.append("Mention your experience with remote work tools and self-management")
        
        if job.get('match_type') == 'alternative':
            tips.append("Emphasize transferable skills that apply to this role")
        
        return tips
    
    def _get_next_actions(self, status: ApplicationStatus) -> List[str]:
        """Get next recommended actions based on application status"""
        actions_map = {
            ApplicationStatus.DRAFT: [
                "Complete and submit your application",
                "Review cover letter and resume one more time",
                "Research the company thoroughly"
            ],
            ApplicationStatus.SUBMITTED: [
                "Set a follow-up reminder for one week",
                "Continue applying to similar positions",
                "Prepare for potential interviews"
            ],
            ApplicationStatus.UNDER_REVIEW: [
                "Be patient and wait for response",
                "Prepare for potential interview",
                "Continue job search activities"
            ],
            ApplicationStatus.INTERVIEW_SCHEDULED: [
                "Research common interview questions",
                "Prepare specific examples from your experience",
                "Research the company and interviewers",
                "Prepare questions to ask them"
            ],
            ApplicationStatus.REJECTED: [
                "Request feedback if possible",
                "Review and improve your application materials",
                "Continue applying to similar positions",
                "Learn from this experience"
            ],
            ApplicationStatus.ACCEPTED: [
                "Negotiate salary if appropriate",
                "Review the job offer carefully",
                "Notify other applications of your decision",
                "Prepare for onboarding"
            ]
        }
        
        return actions_map.get(status, ["Continue with your job search"])
    
    def _generate_application_insights(self, status_counts: Dict, success_rate: float) -> List[str]:
        """Generate insights based on application data"""
        insights = []
        
        total_apps = sum(status_counts.values())
        
        if total_apps < 5:
            insights.append("Consider applying to more positions to increase your chances")
        
        if success_rate < 10:
            insights.append("Consider improving your resume and cover letter to increase interview rates")
        elif success_rate > 30:
            insights.append("Great interview rate! Your application materials are working well")
        
        submitted_count = status_counts.get('submitted', 0)
        if submitted_count > 10:
            insights.append("You're being very active! Make sure to track all your applications")
        
        rejected_count = status_counts.get('rejected', 0)
        if rejected_count > 5:
            insights.append("Consider targeting positions that better match your experience level")
        
        return insights
