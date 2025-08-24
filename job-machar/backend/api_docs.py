"""
API Documentation for Production AI Job Matcher
Comprehensive REST API for resume analysis and job matching
"""

from flask import Flask, jsonify
from datetime import datetime

def create_api_docs():
    """Create comprehensive API documentation"""
    
    docs = {
        "api": {
            "name": "AI Job Matcher API",
            "version": "3.0.0",
            "description": "Production-ready API for AI-powered resume analysis and job matching",
            "base_url": "http://localhost:5000",
            "authentication": "JWT Bearer Token"
        },
        "endpoints": {
            "authentication": {
                "POST /auth/register": {
                    "description": "Register a new user account",
                    "rate_limit": "5 requests per 5 minutes",
                    "body": {
                        "email": "string (required)",
                        "password": "string (required, min 6 chars)",
                        "name": "string (required)"
                    },
                    "response": {
                        "success": "boolean",
                        "message": "string"
                    },
                    "example": {
                        "request": {
                            "email": "user@example.com",
                            "password": "securepassword123",
                            "name": "John Doe"
                        },
                        "response": {
                            "success": True,
                            "message": "User created successfully"
                        }
                    }
                },
                "POST /auth/login": {
                    "description": "Login and receive JWT token",
                    "rate_limit": "10 requests per 5 minutes",
                    "body": {
                        "email": "string (required)",
                        "password": "string (required)"
                    },
                    "response": {
                        "success": "boolean",
                        "token": "string (JWT)",
                        "user": "object",
                        "message": "string"
                    },
                    "example": {
                        "request": {
                            "email": "user@example.com",
                            "password": "securepassword123"
                        },
                        "response": {
                            "success": True,
                            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "user": {
                                "id": "uuid",
                                "email": "user@example.com",
                                "name": "John Doe",
                                "session_id": "session-uuid"
                            },
                            "message": "Login successful"
                        }
                    }
                },
                "POST /auth/logout": {
                    "description": "Logout and invalidate token",
                    "auth_required": True,
                    "response": {
                        "success": "boolean",
                        "message": "string"
                    }
                },
                "GET /auth/profile": {
                    "description": "Get user profile information",
                    "auth_required": True,
                    "response": {
                        "success": "boolean",
                        "user": "object"
                    }
                }
            },
            "resume_analysis": {
                "POST /upload-resume": {
                    "description": "Upload and analyze resume with advanced AI",
                    "auth_required": True,
                    "rate_limit": "5 uploads per 5 minutes",
                    "content_type": "multipart/form-data",
                    "body": {
                        "resume": "file (PDF only, max 16MB)"
                    },
                    "response": {
                        "success": "boolean",
                        "analysis_id": "string (UUID)",
                        "resume_analysis": "object",
                        "message": "string"
                    },
                    "resume_analysis_structure": {
                        "personal_info": {
                            "name": "string",
                            "title": "string",
                            "summary": "string"
                        },
                        "skills_analysis": {
                            "skills_by_category": "object",
                            "all_skills": "array",
                            "skill_proficiency": "object",
                            "trending_skills": "array",
                            "skill_density": "number"
                        },
                        "experience_analysis": {
                            "total_years": "number",
                            "experience_level": "string",
                            "job_titles": "array",
                            "companies": "array",
                            "key_achievements": "array"
                        },
                        "education_analysis": {
                            "degrees": "array",
                            "institutions": "array",
                            "majors": "array",
                            "graduation_years": "array"
                        },
                        "quality_assessment": {
                            "overall_score": "number",
                            "quality_grade": "string (A-D)",
                            "suggestions": "array"
                        }
                    }
                },
                "GET /analysis/{analysis_id}": {
                    "description": "Get detailed analysis results",
                    "auth_required": True,
                    "path_params": {
                        "analysis_id": "string (UUID)"
                    },
                    "response": {
                        "success": "boolean",
                        "analysis_id": "string",
                        "filename": "string",
                        "timestamp": "string (ISO)",
                        "resume_analysis": "object"
                    }
                }
            },
            "job_search": {
                "POST /search-jobs": {
                    "description": "Search for jobs using real APIs from multiple platforms",
                    "auth_required": True,
                    "rate_limit": "20 searches per hour",
                    "body": {
                        "keywords": "array (required)",
                        "location": "string (optional)",
                        "experience_level": "string (optional: entry|mid|senior|executive)",
                        "employment_type": "string (optional)",
                        "salary_min": "number (optional)",
                        "limit": "number (max 50, default 20)"
                    },
                    "response": {
                        "success": "boolean",
                        "jobs": "array",
                        "statistics": "object",
                        "total_found": "number",
                        "message": "string"
                    },
                    "job_structure": {
                        "id": "string",
                        "title": "string",
                        "company": "string",
                        "location": "string",
                        "description": "string",
                        "requirements": "array",
                        "salary_min": "number",
                        "salary_max": "number",
                        "salary_currency": "string",
                        "experience_level": "string",
                        "employment_type": "string",
                        "posted_date": "string (ISO)",
                        "source": "string",
                        "apply_url": "string",
                        "skills": "array",
                        "remote_allowed": "boolean"
                    },
                    "example": {
                        "request": {
                            "keywords": ["python", "machine learning"],
                            "location": "San Francisco",
                            "experience_level": "mid",
                            "limit": 10
                        }
                    }
                }
            },
            "ai_matching": {
                "POST /match-jobs": {
                    "description": "Get AI-powered job matches for uploaded resume",
                    "auth_required": True,
                    "rate_limit": "10 matches per hour",
                    "body": {
                        "analysis_id": "string (required, UUID)",
                        "preferences": "object (optional)",
                        "limit": "number (max 50, default 20)"
                    },
                    "preferences_structure": {
                        "location": "string",
                        "preferred_location": "string",
                        "employment_type": "string",
                        "salary_min": "number",
                        "preferred_companies": "array"
                    },
                    "response": {
                        "success": "boolean",
                        "analysis_id": "string",
                        "matches": "object",
                        "message": "string"
                    },
                    "matches_structure": {
                        "matches": "array",
                        "total_found": "number",
                        "search_keywords": "array",
                        "insights": "object",
                        "statistics": "object"
                    },
                    "match_object": {
                        "job": "object (job details)",
                        "match_score": "number (0-1)",
                        "score_breakdown": "object",
                        "match_reasons": "array",
                        "skill_overlap": "array",
                        "missing_skills": "array",
                        "recommendation": "string"
                    }
                }
            },
            "advanced_features": {
                "POST /skill-gap-analysis": {
                    "description": "Analyze skill gaps based on job market demand",
                    "auth_required": True,
                    "rate_limit": "5 analyses per hour",
                    "body": {
                        "analysis_id": "string (required, UUID)",
                        "target_roles": "array (optional)"
                    },
                    "response": {
                        "success": "boolean",
                        "skill_gaps": "array",
                        "user_skills_count": "number",
                        "market_jobs_analyzed": "number",
                        "recommendations": "array",
                        "message": "string"
                    },
                    "skill_gap_object": {
                        "skill": "string",
                        "importance": "number (0-1)",
                        "frequency": "number",
                        "gap_severity": "string (low|medium|high)"
                    }
                },
                "POST /career-insights": {
                    "description": "Get AI-powered career insights and recommendations",
                    "auth_required": True,
                    "rate_limit": "5 insights per hour",
                    "body": {
                        "analysis_id": "string (required, UUID)"
                    },
                    "response": {
                        "success": "boolean",
                        "insights": "object",
                        "message": "string"
                    },
                    "insights_structure": {
                        "profile_summary": "object",
                        "market_positioning": "object",
                        "growth_opportunities": "array",
                        "salary_insights": "object",
                        "recommendations": "array"
                    }
                }
            },
            "user_management": {
                "GET /user/history": {
                    "description": "Get user's analysis history",
                    "auth_required": True,
                    "response": {
                        "success": "boolean",
                        "history": "array",
                        "total_analyses": "number"
                    }
                }
            },
            "system": {
                "GET /health": {
                    "description": "Health check and system status",
                    "response": {
                        "status": "string",
                        "timestamp": "string (ISO)",
                        "version": "string",
                        "features": "object",
                        "api_status": "object"
                    },
                    "example": {
                        "response": {
                            "status": "healthy",
                            "timestamp": "2025-01-01T12:00:00Z",
                            "version": "3.0.0",
                            "features": {
                                "authentication": True,
                                "advanced_resume_parsing": True,
                                "real_job_apis": True,
                                "ai_job_matching": True,
                                "rate_limiting": True
                            },
                            "api_status": {
                                "adzuna": True,
                                "jsearch": True,
                                "remotive": True,
                                "findwork": True
                            }
                        }
                    }
                }
            }
        },
        "authentication": {
            "type": "JWT Bearer Token",
            "header": "Authorization: Bearer <token>",
            "token_expiry": "1 hour",
            "note": "Include the token in the Authorization header for protected endpoints"
        },
        "rate_limiting": {
            "headers": {
                "X-RateLimit-Limit": "Maximum requests allowed",
                "X-RateLimit-Remaining": "Remaining requests",
                "X-RateLimit-Reset": "Reset time (Unix timestamp)"
            },
            "limits": {
                "registration": "5 requests per 5 minutes",
                "login": "10 requests per 5 minutes",
                "resume_upload": "5 uploads per 5 minutes",
                "job_search": "20 searches per hour",
                "job_matching": "10 matches per hour",
                "skill_analysis": "5 analyses per hour",
                "career_insights": "5 insights per hour"
            }
        },
        "error_codes": {
            "400": "Bad Request - Invalid request data",
            "401": "Unauthorized - Authentication required or token invalid",
            "403": "Forbidden - Access denied",
            "404": "Not Found - Resource not found",
            "429": "Rate Limit Exceeded - Too many requests",
            "500": "Internal Server Error - Server error"
        },
        "data_sources": {
            "job_apis": {
                "adzuna": {
                    "description": "Global job search API",
                    "coverage": "Worldwide",
                    "rate_limit": "300 requests/hour",
                    "requires_key": True
                },
                "jsearch": {
                    "description": "Comprehensive job search via RapidAPI",
                    "coverage": "Worldwide",
                    "rate_limit": "100 requests/hour",
                    "requires_key": True
                },
                "remotive": {
                    "description": "Remote job listings",
                    "coverage": "Remote positions worldwide",
                    "rate_limit": "60 requests/hour",
                    "requires_key": False
                },
                "findwork": {
                    "description": "Tech job listings",
                    "coverage": "Primarily tech positions",
                    "rate_limit": "100 requests/hour",
                    "requires_key": False
                }
            }
        },
        "ai_models": {
            "resume_parsing": {
                "ner_model": "dbmdz/bert-large-cased-finetuned-conll03-english",
                "classification": "facebook/bart-large-mnli",
                "sentence_transformer": "all-MiniLM-L6-v2",
                "spacy_model": "en_core_web_sm"
            },
            "job_matching": {
                "semantic_similarity": "all-MiniLM-L6-v2",
                "text_classification": "facebook/bart-large-mnli",
                "matching_algorithm": "Weighted cosine similarity with multiple factors"
            }
        },
        "setup_requirements": {
            "api_keys": {
                "required": [
                    "ADZUNA_APP_ID",
                    "ADZUNA_APP_KEY",
                    "RAPIDAPI_KEY"
                ],
                "optional": [
                    "HUGGINGFACE_API_KEY"
                ]
            },
            "environment_variables": [
                "JWT_SECRET_KEY",
                "REDIS_URL (for production)",
                "DATABASE_URL (for production)",
                "CORS_ORIGINS"
            ],
            "system_dependencies": [
                "Python 3.8+",
                "Redis (optional, for caching)",
                "PostgreSQL (optional, for production database)"
            ]
        }
    }
    
    return docs

# Create endpoint to serve documentation
def create_docs_app():
    """Create Flask app for serving documentation"""
    app = Flask(__name__)
    
    @app.route('/docs', methods=['GET'])
    def get_docs():
        """Serve API documentation"""
        return jsonify(create_api_docs())
    
    @app.route('/docs/html', methods=['GET'])
    def get_docs_html():
        """Serve HTML documentation"""
        docs = create_api_docs()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Job Matcher API Documentation</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { background: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; }
                .auth-required { background: #ff9800; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }
                pre { background: #f0f0f0; padding: 10px; border-radius: 3px; overflow-x: auto; }
                h1 { color: #333; }
                h2 { color: #666; border-bottom: 2px solid #eee; }
                h3 { color: #888; }
            </style>
        </head>
        <body>
            <h1>🚀 AI Job Matcher API Documentation</h1>
            <p><strong>Version:</strong> 3.0.0</p>
            <p><strong>Base URL:</strong> http://localhost:5000</p>
            <p><strong>Authentication:</strong> JWT Bearer Token</p>
            
            <h2>🔐 Authentication</h2>
            <p>Include JWT token in Authorization header: <code>Authorization: Bearer &lt;token&gt;</code></p>
            
            <h2>📝 Quick Start</h2>
            <ol>
                <li>Register: POST /auth/register</li>
                <li>Login: POST /auth/login (get JWT token)</li>
                <li>Upload Resume: POST /upload-resume (with auth)</li>
                <li>Get Job Matches: POST /match-jobs (with auth)</li>
            </ol>
            
            <h2>📊 Rate Limits</h2>
            <ul>
                <li>Registration: 5 requests per 5 minutes</li>
                <li>Login: 10 requests per 5 minutes</li>
                <li>Resume Upload: 5 uploads per 5 minutes</li>
                <li>Job Search: 20 searches per hour</li>
                <li>Job Matching: 10 matches per hour</li>
            </ul>
            
            <h2>🌐 Data Sources</h2>
            <ul>
                <li><strong>Adzuna:</strong> Global job search API</li>
                <li><strong>JSearch (RapidAPI):</strong> Comprehensive job listings</li>
                <li><strong>Remotive:</strong> Remote job positions</li>
                <li><strong>FindWork:</strong> Tech job listings</li>
            </ul>
            
            <h2>🤖 AI Models</h2>
            <ul>
                <li><strong>Resume Parsing:</strong> BERT NER + BART Classification</li>
                <li><strong>Job Matching:</strong> Sentence Transformers + Cosine Similarity</li>
                <li><strong>Skill Analysis:</strong> Multi-factor semantic analysis</li>
            </ul>
            
            <h2>📞 Support</h2>
            <p>For API keys and setup instructions, see the README.md file.</p>
            
            <h2>⚡ Example Usage</h2>
            <pre>
# 1. Register
curl -X POST http://localhost:5000/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "password": "secure123", "name": "John Doe"}'

# 2. Login
curl -X POST http://localhost:5000/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email": "user@example.com", "password": "secure123"}'

# 3. Upload Resume
curl -X POST http://localhost:5000/upload-resume \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -F "resume=@path/to/resume.pdf"

# 4. Search Jobs
curl -X POST http://localhost:5000/search-jobs \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"keywords": ["python", "machine learning"], "location": "San Francisco"}'

# 5. Get Job Matches
curl -X POST http://localhost:5000/match-jobs \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"analysis_id": "your-analysis-uuid", "limit": 10}'
            </pre>
        </body>
        </html>
        """
        
        return html

if __name__ == '__main__':
    app = create_docs_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
