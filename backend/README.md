# 🔧 AI Job Matcher Backend

## 🚀 Overview

A production-ready Flask backend that powers the AI Job Matcher platform. This backend uses advanced AI models for resume parsing, real-time job data from multiple APIs, and intelligent matching algorithms to provide personalized job recommendations.

🌐 **Live API**: [Backend Documentation](https://ai-job-matcher-backend.vercel.app/docs)  
📊 **Health Check**: [API Status](https://ai-job-matcher-backend.vercel.app/health)

The system accepts PDF resumes, analyzes them using advanced AI models (BERT, BART, spaCy), fetches real-time job listings from LinkedIn, Adzuna, and other platforms, and returns ranked recommendations with detailed explanations.

## ✨ Features

### Core Functionality
- **Advanced Resume Parsing**: AI-powered PDF analysis using Hugging Face models
- **Real-time Job Data**: Integration with multiple job platforms via official APIs
- **AI-Powered Matching**: Semantic similarity and multi-factor scoring
- **User Authentication**: JWT-based secure authentication system
- **Rate Limiting**: API rate limiting to prevent abuse
- **Comprehensive Error Handling**: Robust error handling and logging

### AI Models & Technologies
- **Resume Analysis**: BERT NER, BART Classification, spaCy NLP
- **Job Matching**: Sentence Transformers, Cosine Similarity
- **Skill Extraction**: Multi-category skill analysis with proficiency assessment
- **Career Insights**: AI-powered career recommendations and gap analysis

## 🧠 How the Backend Works

### 1. Resume Processing Pipeline
```
PDF Upload → Text Extraction → AI Analysis → Skill Categorization → Storage
```

**Step 1: PDF Text Extraction**
- Uses PyPDF2 and pdfplumber for robust PDF parsing
- Handles various PDF formats and encodings
- Extracts text while preserving structure

**Step 2: AI-Powered Analysis**
- **BERT NER**: Extracts personal information (name, email, phone)
- **spaCy NLP**: Processes natural language and identifies entities
- **BART Classification**: Zero-shot classification for experience levels
- **Custom Patterns**: Regex patterns for structured data extraction

**Step 3: Skill Extraction & Categorization**
```python
# Example skill categorization
skills_categories = {
    'programming': ['Python', 'JavaScript', 'Java', 'C++'],
    'frameworks': ['React', 'Django', 'Express', 'Spring'],
    'databases': ['MySQL', 'PostgreSQL', 'MongoDB'],
    'cloud': ['AWS', 'Azure', 'GCP', 'Docker'],
    'soft_skills': ['Leadership', 'Communication', 'Problem Solving']
}
```

### 2. Job Data Integration
```
API Calls → Data Normalization → Caching → Real-time Access
```

**Supported Job APIs:**
- **Adzuna API**: Global job search with salary data (300 req/hour)
- **JSearch (RapidAPI)**: Comprehensive listings (100 req/hour)
- **Remotive**: Remote job positions (unlimited)
- **FindWork**: Tech-focused opportunities (unlimited)

**Data Normalization Process:**
1. Fetch jobs from multiple APIs concurrently
2. Standardize job schema across different sources
3. Enhance with additional metadata
4. Cache for performance optimization

### 3. AI Matching Algorithm
```
Resume Analysis + Job Requirements → Multi-Factor Scoring → Ranked Results
```

**Scoring Components:**
```python
def calculate_job_match(resume_data, job_data):
    skills_score = calculate_skills_match(resume_data.skills, job_data.requirements)
    experience_score = calculate_experience_match(resume_data.experience, job_data.experience_level)
    semantic_score = calculate_semantic_similarity(resume_data.summary, job_data.description)
    
    # Weighted scoring
    final_score = (skills_score * 0.4) + (experience_score * 0.3) + (semantic_score * 0.3)
    return final_score
```

**Semantic Similarity Engine:**
- Uses Sentence Transformers (all-MiniLM-L6-v2)
- Generates embeddings for resume content and job descriptions
- Calculates cosine similarity for semantic matching

### 4. Authentication & Security
```
JWT Token Generation → Request Validation → Rate Limiting → Response
```

**Security Features:**
- **JWT Authentication**: Stateless token-based auth
- **Rate Limiting**: Prevents API abuse
- **CORS Protection**: Secure cross-origin requests
- **Input Validation**: Sanitizes all user inputs
- **Error Handling**: Secure error responses without data leakage

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Setup

#### Windows
```bash
# Clone and navigate to backend directory
cd backend

# Run setup script
setup.bat
```

#### Linux/macOS
```bash
# Clone and navigate to backend directory
cd backend

# Make setup script executable and run
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Create Virtual Environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Download AI Models**
```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

4. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys (see API Keys section)
```

## 🔑 API Keys Configuration

Create a `.env` file with the following configuration:

```env
# Server Configuration
PORT=5000
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production

# Authentication
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# Job API Keys (Required for full functionality)
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
RAPIDAPI_KEY=your_rapidapi_key

# Optional: Redis for caching and rate limiting
REDIS_URL=redis://localhost:6379/0

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Getting API Keys

#### Adzuna API (Free Tier Available)
1. Visit [Adzuna Developer](https://developer.adzuna.com/)
2. Sign up for a free account
3. Create an application to get App ID and App Key
4. Free tier: 300 requests/hour

#### RapidAPI (JSearch)
1. Visit [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/)
2. Sign up for RapidAPI account
3. Subscribe to JSearch API (free tier available)
4. Get your RapidAPI key from the dashboard
5. Free tier: 100 requests/hour

## 🚀 Running the Application

### Development Mode
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Start development server
python app.py
```

### Production Mode
```bash
# Install gunicorn (if not already installed)
pip install gunicorn

# Start production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```bash
# Build Docker image
docker build -t ai-job-matcher-backend .

# Run container
docker run -p 5000:5000 --env-file .env ai-job-matcher-backend
```

## 📖 API Documentation

### Quick Start
1. **Register**: `POST /auth/register`
2. **Login**: `POST /auth/login` (get JWT token)
3. **Upload Resume**: `POST /upload-resume` (with auth)
4. **Get Job Matches**: `POST /match-jobs` (with auth)

### Interactive Documentation
Start the documentation server:
```bash
python api_docs.py
```
Visit: http://localhost:8080/docs/html

### Core Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout and invalidate token
- `GET /auth/profile` - Get user profile

#### Resume Analysis
- `POST /upload-resume` - Upload and analyze PDF resume
- `GET /analysis/{id}` - Get analysis results

#### Job Operations
- `POST /search-jobs` - Search jobs from real APIs
- `POST /match-jobs` - Get AI-powered job matches

#### Advanced Features
- `POST /skill-gap-analysis` - Analyze skill gaps
- `POST /career-insights` - Get career recommendations
- `GET /user/history` - Get user's analysis history

#### System
- `GET /health` - Health check and API status

### Authentication
All protected endpoints require JWT token in header:
```
Authorization: Bearer <your-jwt-token>
```

### Rate Limits
- Registration: 5 requests per 5 minutes
- Login: 10 requests per 5 minutes
- Resume Upload: 5 uploads per 5 minutes
- Job Search: 20 searches per hour
- Job Matching: 10 matches per hour

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Register User
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secure123", "name": "Test User"}'
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secure123"}'
```

### Upload Resume
```bash
curl -X POST http://localhost:5000/upload-resume \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "resume=@path/to/resume.pdf"
```

## 🏗️ Architecture

### Components
- **app.py**: Main Flask application with all endpoints
- **advanced_resume_parser.py**: AI-powered PDF resume parsing
- **job_api_client.py**: Real job API integrations
- **ai_job_matcher.py**: AI matching engine
- **auth.py**: Authentication and security
- **api_docs.py**: Interactive API documentation

### Data Flow
1. User uploads PDF resume
2. Advanced parser extracts skills, experience, education
3. AI models analyze and categorize information
4. Job APIs fetch real-time job listings
5. Matching engine scores jobs using multiple factors
6. Ranked recommendations returned with explanations

### AI Models Used
- **BERT NER**: Named entity recognition for personal info
- **BART Classification**: Zero-shot text classification
- **Sentence Transformers**: Semantic similarity matching
- **spaCy NLP**: Natural language processing
- **TF-IDF**: Keyword matching and analysis

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 5000)
- `DEBUG`: Debug mode (default: False)
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `REDIS_URL`: Redis connection URL
- `CORS_ORIGINS`: Allowed CORS origins

### Rate Limiting
Configurable rate limits per endpoint to prevent abuse while allowing legitimate usage.

### Error Handling
Comprehensive error handling with detailed logging and user-friendly error messages.

## 📊 Performance

### Optimizations
- **Memory Management**: Optimized model loading and memory usage
- **Caching**: Redis-based caching for improved performance
- **Async Operations**: Concurrent API calls for faster job fetching
- **Rate Limiting**: Prevents API overuse and ensures stability

### Scaling
- **Horizontal Scaling**: Stateless design allows multiple instances
- **Database**: PostgreSQL support for production data storage
- **Load Balancing**: Compatible with load balancers
- **Monitoring**: Comprehensive logging for monitoring and debugging

## 🚀 Production Deployment

### Requirements
- Python 3.8+
- Redis (for caching and rate limiting)
- PostgreSQL (optional, for user data persistence)
- NGINX (for reverse proxy)

### Environment Setup
1. Set production environment variables
2. Configure Redis for session management
3. Set up database for user persistence
4. Configure NGINX for SSL and load balancing

### Monitoring
- Application logs in `app.log`
- Health check endpoint for monitoring
- Rate limit headers for API usage tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the API documentation: http://localhost:8080/docs/html
2. Review the logs in `app.log`
3. Ensure all API keys are configured correctly
4. Verify all dependencies are installed

## 🔄 Version History

### v3.0.0 (Current)
- Production-ready backend with real job APIs
- Advanced AI-powered resume parsing
- JWT authentication and rate limiting
- Comprehensive error handling
- Interactive API documentation

---

**Ready to match talent with opportunity using AI! 🚀**
