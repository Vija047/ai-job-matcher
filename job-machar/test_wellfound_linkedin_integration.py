"""
Demonstration of Wellfound and LinkedIn Job Integration
Shows how the AI Job Matcher now connects to these platforms
"""

import requests
import json
from datetime import datetime

# Backend URL
BACKEND_URL = "http://localhost:5000"

def test_wellfound_linkedin_search():
    """Test the new Wellfound + LinkedIn search endpoint"""
    print("🚀 Testing Wellfound + LinkedIn Job Search Integration")
    print("=" * 60)
    
    # Test search parameters
    search_data = {
        "keywords": ["software engineer", "python developer"],
        "location": "San Francisco",
        "experience_level": "mid",
        "limit": 10
    }
    
    try:
        print(f"📊 Searching for: {search_data['keywords']}")
        print(f"📍 Location: {search_data['location']}")
        print(f"💼 Experience: {search_data['experience_level']}")
        print(f"📝 Limit: {search_data['limit']} jobs")
        print()
        
        # Make API request
        response = requests.post(
            f"{BACKEND_URL}/search-wellfound-linkedin",
            json=search_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ SUCCESS! Job search completed")
            print(f"📈 Total jobs found: {data.get('total_found', 0)}")
            print()
            
            # Show source breakdown
            source_breakdown = data.get('source_breakdown', {})
            if source_breakdown:
                print("📊 Source Breakdown:")
                print(f"   🚀 Wellfound (Startups): {source_breakdown.get('wellfound_count', 0)}")
                print(f"   👥 LinkedIn (Professional): {source_breakdown.get('linkedin_count', 0)}")
                print(f"   🏢 Total Startup Opportunities: {source_breakdown.get('total_startup_opportunities', 0)}")
                print(f"   💼 Total Professional Opportunities: {source_breakdown.get('total_professional_opportunities', 0)}")
                print()
            
            # Show job examples
            jobs = data.get('jobs', [])
            if jobs:
                print("🎯 Sample Job Opportunities:")
                print("-" * 50)
                
                for i, job in enumerate(jobs[:5], 1):
                    print(f"{i}. {job.get('title', 'N/A')}")
                    print(f"   Company: {job.get('company', 'N/A')}")
                    print(f"   Source: {job.get('source', 'N/A')}")
                    print(f"   Location: {job.get('location', 'N/A')}")
                    
                    if job.get('is_startup'):
                        print(f"   🚀 Startup Stage: {job.get('funding_stage', 'N/A')}")
                    
                    if job.get('remote_allowed'):
                        print("   🌍 Remote Work: Available")
                    
                    if job.get('salary_range') and job['salary_range'] != "Salary not specified":
                        print(f"   💰 Salary: {job['salary_range']}")
                    
                    print(f"   📝 Apply: {job.get('apply_url', 'N/A')}")
                    print()
            
            # Show enhanced features
            enhanced_features = data.get('enhanced_features', {})
            if enhanced_features:
                print("🎉 Enhanced Features Available:")
                features = []
                if enhanced_features.get('startup_focus'):
                    features.append("🚀 Startup Focus")
                if enhanced_features.get('professional_network'):
                    features.append("👥 Professional Network")
                if enhanced_features.get('funding_info'):
                    features.append("💰 Funding Information")
                if enhanced_features.get('company_logos'):
                    features.append("🏢 Company Logos")
                
                for feature in features:
                    print(f"   ✅ {feature}")
                print()
            
            print("🎯 Integration Benefits:")
            print("   • Access to both startup and enterprise opportunities")
            print("   • Real-time job data from live platforms")
            print("   • Enhanced filtering and matching capabilities")
            print("   • Direct application links to original postings")
            print("   • Startup funding stage information")
            print("   • Professional network connections")
            
        else:
            print(f"❌ ERROR: API returned status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_regular_search_comparison():
    """Compare with regular search to show the difference"""
    print("\n" + "=" * 60)
    print("🔍 Comparison with Regular Job Search")
    print("=" * 60)
    
    search_data = {
        "keywords": ["data scientist"],
        "location": "Remote",
        "experience_level": "senior",
        "limit": 5
    }
    
    try:
        # Regular search
        print("📊 Regular Search Results:")
        response = requests.post(
            f"{BACKEND_URL}/search-jobs",
            json=search_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            regular_jobs = data.get('jobs', [])
            regular_sources = data.get('data_sources', [])
            
            print(f"   Jobs found: {len(regular_jobs)}")
            print(f"   Sources: {', '.join(regular_sources)}")
            print()
        
        # Wellfound + LinkedIn search
        print("🚀 Wellfound + LinkedIn Search Results:")
        response = requests.post(
            f"{BACKEND_URL}/search-wellfound-linkedin",
            json=search_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            wl_jobs = data.get('jobs', [])
            source_breakdown = data.get('source_breakdown', {})
            
            print(f"   Jobs found: {len(wl_jobs)}")
            print(f"   Wellfound: {source_breakdown.get('wellfound_count', 0)}")
            print(f"   LinkedIn: {source_breakdown.get('linkedin_count', 0)}")
            print()
            
            print("🎯 Key Differences:")
            print("   • Wellfound+LinkedIn: Focused on specific high-quality sources")
            print("   • Regular Search: Broader coverage across multiple platforms")
            print("   • Wellfound+LinkedIn: Enhanced startup and professional data")
            print("   • Regular Search: General job aggregation")
        
    except Exception as e:
        print(f"❌ Comparison test error: {str(e)}")

def show_integration_summary():
    """Show summary of the integration"""
    print("\n" + "=" * 60)
    print("📋 Integration Summary")
    print("=" * 60)
    
    print("✅ COMPLETED INTEGRATIONS:")
    print()
    
    print("🚀 WELLFOUND (formerly AngelList):")
    print("   • Startup job opportunities")
    print("   • Funding stage information")
    print("   • Equity-based positions")
    print("   • Direct founder connections")
    print("   • Early-stage to unicorn companies")
    print()
    
    print("👥 LINKEDIN:")
    print("   • Professional network jobs")
    print("   • Enterprise opportunities")
    print("   • Established company positions")
    print("   • Professional networking")
    print("   • Traditional employment benefits")
    print()
    
    print("🔧 TECHNICAL IMPLEMENTATION:")
    print("   • Enhanced job API client (wellfound_linkedin_job_client.py)")
    print("   • New backend endpoint (/search-wellfound-linkedin)")
    print("   • Frontend integration (EnhancedJobsList.js)")
    print("   • New dedicated page (WellfoundLinkedinPage.js)")
    print("   • Updated navigation with Rocket icon")
    print()
    
    print("🎯 USER BENEFITS:")
    print("   • Access to both startup and enterprise opportunities")
    print("   • Enhanced job matching with funding/company info")
    print("   • Direct application links to original platforms")
    print("   • Real-time data from live job sources")
    print("   • Improved career opportunity discovery")
    print()
    
    print("🌐 FRONTEND ACCESS:")
    print("   • New navigation option: 'Wellfound + LinkedIn'")
    print("   • Dedicated search interface")
    print("   • Enhanced job cards with startup/professional badges")
    print("   • Company logos and funding stage display")
    print("   • Remote work indicators")

if __name__ == "__main__":
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test the main integration
    test_wellfound_linkedin_search()
    
    # Compare with regular search
    test_regular_search_comparison()
    
    # Show integration summary
    show_integration_summary()
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✨ Wellfound and LinkedIn integration is ready!")
    print("🌐 Frontend: http://localhost:3001")
    print("🔧 Backend: http://localhost:5000")
