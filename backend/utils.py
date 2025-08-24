"""
Utility functions for visualization and data processing
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Any

def create_skills_gap_analysis(recommendations: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a skills gap analysis DataFrame"""
    gap_data = []
    
    for rec in recommendations:
        gap_data.append({
            'Job Title': rec['job_title'],
            'Company': rec['company'],
            'Overall Score': f"{rec['overall_score']['overall_score']:.1%}",
            'Skills Match': f"{rec['skill_match']['skill_match_score']:.1%}",
            'Missing Skills': ', '.join(rec['skill_match']['missing_skills']) if rec['skill_match']['missing_skills'] else 'None',
            'Matched Skills': ', '.join(rec['skill_match']['matched_skills']) if rec['skill_match']['matched_skills'] else 'None',
            'Experience Match': f"{rec['experience_match']['experience_match_score']:.1%}",
            'Recommendation': rec['overall_score']['recommendation']
        })
    
    return pd.DataFrame(gap_data)

def create_visualization(resume_analysis: Dict[str, Any], recommendations: List[Dict[str, Any]]):
    """Create comprehensive visualizations for the analysis results"""
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(20, 15))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Skills Distribution (Pie Chart)
    ax1 = fig.add_subplot(gs[0, 0])
    skills_data = {cat.replace('_', ' ').title(): len(skills) 
                  for cat, skills in resume_analysis['skills'].items() if skills}
    
    if skills_data:
        colors = plt.cm.Set3(np.linspace(0, 1, len(skills_data)))
        wedges, texts, autotexts = ax1.pie(skills_data.values(), labels=skills_data.keys(), 
                                          autopct='%1.1f%%', colors=colors)
        ax1.set_title('Skills Distribution by Category', fontsize=12, fontweight='bold')
    else:
        ax1.text(0.5, 0.5, 'No skills found', ha='center', va='center', transform=ax1.transAxes)
        ax1.set_title('Skills Distribution by Category', fontsize=12, fontweight='bold')
    
    # 2. Job Match Scores (Horizontal Bar Chart)
    ax2 = fig.add_subplot(gs[0, 1:])
    job_titles = [rec['job_title'] for rec in recommendations]
    overall_scores = [rec['overall_score']['overall_score'] for rec in recommendations]
    
    colors_map = {'Excellent Match': 'green', 'Good Match': 'gold', 'Fair Match': 'orange', 'Poor Match': 'red'}
    bar_colors = [colors_map.get(rec['overall_score']['recommendation'], 'gray') for rec in recommendations]
    
    bars = ax2.barh(job_titles, overall_scores, color=bar_colors, alpha=0.7)
    ax2.set_xlabel('Match Score', fontweight='bold')
    ax2.set_title('Job Compatibility Scores', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 1)
    
    # Add score labels on bars
    for i, (bar, score) in enumerate(zip(bars, overall_scores)):
        ax2.text(score + 0.01, bar.get_y() + bar.get_height()/2, f'{score:.1%}', 
                va='center', fontweight='bold')
    
    # 3. Score Breakdown for Top Job (Stacked Bar)
    ax3 = fig.add_subplot(gs[1, 0])
    if recommendations:
        top_job = recommendations[0]
        breakdown = top_job['overall_score']['score_breakdown']
        categories = ['Skills', 'Experience', 'Semantic']
        values = [breakdown['skills_score'], breakdown['experience_score'], breakdown['semantic_score']]
        
        bars = ax3.bar(categories, values, color=['skyblue', 'lightcoral', 'lightgreen'])
        ax3.set_ylabel('Score Contribution', fontweight='bold')
        ax3.set_title(f'Score Breakdown: {top_job["job_title"]}', fontsize=12, fontweight='bold')
        ax3.set_ylim(0, max(values) * 1.2)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f'{value:.2f}', 
                    ha='center', va='bottom', fontweight='bold')
    
    # 4. Skills Match Comparison (Bar chart)
    ax4 = fig.add_subplot(gs[1, 1])
    if recommendations:
        skill_scores = [rec['skill_match']['skill_match_score'] for rec in recommendations[:5]]
        job_names = [rec['job_title'][:15] + '...' if len(rec['job_title']) > 15 
                    else rec['job_title'] for rec in recommendations[:5]]
        
        bars = ax4.bar(range(len(skill_scores)), skill_scores, color='steelblue', alpha=0.7)
        ax4.set_xlabel('Jobs', fontweight='bold')
        ax4.set_ylabel('Skills Match Score', fontweight='bold')
        ax4.set_title('Skills Match Across Top Jobs', fontsize=12, fontweight='bold')
        ax4.set_xticks(range(len(job_names)))
        ax4.set_xticklabels(job_names, rotation=45, ha='right')
        ax4.set_ylim(0, 1)
        
        # Add score labels
        for i, (bar, score) in enumerate(zip(bars, skill_scores)):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{score:.1%}', 
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # 5. Experience Level Comparison
    ax5 = fig.add_subplot(gs[1, 2])
    experience_levels = ['Entry', 'Mid', 'Senior', 'Executive']
    resume_level = resume_analysis['experience']['primary_level']
    job_levels = [rec['experience_match']['job_level'] for rec in recommendations]
    
    level_counts = {level: 0 for level in experience_levels}
    for level in job_levels:
        if level in level_counts:
            level_counts[level] += 1
    
    bars = ax5.bar(experience_levels, level_counts.values(), color='mediumpurple', alpha=0.7)
    ax5.set_ylabel('Number of Jobs', fontweight='bold')
    ax5.set_title('Job Experience Level Distribution', fontsize=12, fontweight='bold')
    
    # Highlight candidate's level
    for i, level in enumerate(experience_levels):
        if level.lower() == resume_level:
            bars[i].set_color('red')
            bars[i].set_alpha(0.9)
    
    # 6. Salary Range Visualization
    ax6 = fig.add_subplot(gs[2, :2])
    if recommendations:
        job_titles_short = [rec['job_title'][:20] + '...' if len(rec['job_title']) > 20 
                           else rec['job_title'] for rec in recommendations]
        
        # Extract salary ranges (simplified parsing)
        salary_data = []
        for rec in recommendations:
            salary_str = rec['salary_range']
            # Extract numbers from salary string (e.g., "$70,000 - $95,000")
            import re
            numbers = re.findall(r'\$?([\d,]+)', salary_str)
            if len(numbers) >= 2:
                min_sal = int(numbers[0].replace(',', ''))
                max_sal = int(numbers[1].replace(',', ''))
                salary_data.append((min_sal, max_sal))
            else:
                salary_data.append((0, 0))
        
        if salary_data:
            min_salaries = [sal[0] for sal in salary_data]
            max_salaries = [sal[1] for sal in salary_data]
            
            x_pos = np.arange(len(job_titles_short))
            ax6.barh(x_pos, max_salaries, color='lightblue', alpha=0.7, label='Max Salary')
            ax6.barh(x_pos, min_salaries, color='darkblue', alpha=0.7, label='Min Salary')
            
            ax6.set_yticks(x_pos)
            ax6.set_yticklabels(job_titles_short)
            ax6.set_xlabel('Salary ($)', fontweight='bold')
            ax6.set_title('Salary Ranges for Recommended Jobs', fontsize=12, fontweight='bold')
            ax6.legend()
            
            # Format x-axis labels
            ax6.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
    
    # 7. Overall Summary Stats
    ax7 = fig.add_subplot(gs[2, 2])
    ax7.axis('off')
    
    # Create summary text
    top_job_title = recommendations[0]['job_title'] if recommendations else 'N/A'
    top_job_score = recommendations[0]['overall_score']['overall_score'] if recommendations else 0
    top_job_rec = recommendations[0]['overall_score']['recommendation'] if recommendations else 'N/A'
    
    excellent_count = sum(1 for r in recommendations if r['overall_score']['recommendation'] == 'Excellent Match')
    good_count = sum(1 for r in recommendations if r['overall_score']['recommendation'] == 'Good Match')
    fair_count = sum(1 for r in recommendations if r['overall_score']['recommendation'] == 'Fair Match')
    poor_count = sum(1 for r in recommendations if r['overall_score']['recommendation'] == 'Poor Match')
    
    summary_text = f"""📊 ANALYSIS SUMMARY
    
👤 Candidate Profile:
• Experience: {resume_analysis['experience']['primary_level'].title()}
• Years: {resume_analysis['experience']['years_of_experience']}
• Skills Found: {resume_analysis['total_skills_found']}

🎯 Top Match:
• Job: {top_job_title}
• Score: {top_job_score:.1%}
• Rating: {top_job_rec}

📈 Recommendations:
• Excellent: {excellent_count}
• Good: {good_count}
• Fair: {fair_count}
• Poor: {poor_count}"""
    
    ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))
    
    plt.suptitle('🎯 AI Resume Analysis & Job Matching Dashboard', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    return fig
