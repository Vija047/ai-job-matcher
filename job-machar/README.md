# 🎯 AI Job Matcher

An intelligent resume analysis and job matching platform powered by AI that helps candidates find the perfect job opportunities based on their skills, experience, and qualifications.

## ✨ Features

### 🤖 AI-Powered Resume Analysis
- **PDF Text Extraction**: Automatically extracts and processes text from PDF resumes
- **Skills Recognition**: Identifies and categorizes technical and soft skills
- **Experience Assessment**: Determines experience level and years of experience
- **Contact Information Extraction**: Finds email, phone, LinkedIn, and GitHub profiles

### 🎯 Smart Job Matching
- **Compatibility Scoring**: Calculates match scores based on skills, experience, and semantic similarity
- **Multi-Factor Analysis**: Uses 40% skills matching, 30% experience matching, and 30% semantic similarity
- **Recommendation Engine**: Provides Excellent, Good, Fair, or Poor match ratings

### 📊 Comprehensive Analytics
- **Interactive Dashboard**: Beautiful visualizations of skills distribution and job matches
- **Skills Gap Analysis**: Identifies missing skills needed for target positions
- **Improvement Recommendations**: Personalized suggestions to enhance your resume
- **Detailed Reports**: Export analysis results to CSV format

### 💼 Job Database
- **Browse Opportunities**: Explore available job positions with detailed descriptions
- **Real-time Matching**: See compatibility scores for each job position
- **Salary Information**: View salary ranges and experience requirements

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### 🔧 Installation

#### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
./setup.bat
```

**For macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/ai-job-matcher.git
cd ai-job-matcher/job-machar
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Frontend Setup**
```bash
cd ..
npm install
```

### 🏃‍♂️ Running the Application

1. **Start the Backend** (Terminal 1)
```bash
cd backend
python app.py
```
Backend will run on `http://localhost:5000`

2. **Start the Frontend** (Terminal 2)
```bash
npm run dev
```
Frontend will run on `http://localhost:3000`

3. **Access the Application**
Open your browser and navigate to `http://localhost:3000`

## 📖 Usage Guide

### 1. Upload Your Resume
- Click on the upload area or drag & drop your PDF resume
- The AI will automatically analyze your document
- Wait for the analysis to complete (usually 10-30 seconds)

### 2. View Dashboard
- **Overview Tab**: See your contact info, experience profile, and top job match
- **Skills Analysis**: Detailed breakdown of your skills by category
- **Job Matches**: View all job recommendations with compatibility scores
- **Improvements**: Get personalized suggestions to enhance your resume

### 3. Browse Jobs
- Explore available job opportunities
- Click on any job to see detailed information
- View real-time compatibility analysis for each position

### 4. Export Results
- Download skills gap analysis as CSV
- Save analysis summary for future reference

## 🏗️ Architecture

### Backend (Flask + AI/ML)
```
backend/
├── app.py                 # Main Flask application
├── resume_analyzer.py     # Resume analysis logic
├── job_recommender.py     # Job matching algorithms
├── utils.py              # Utility functions
└── requirements.txt      # Python dependencies
```

### Frontend (Next.js + React)
```
src/
├── app/
│   ├── components/       # React components
│   │   ├── Dashboard.js     # Main dashboard
│   │   ├── ResumeUpload.js  # File upload component
│   │   └── JobsList.js      # Jobs browser
│   ├── utils/
│   │   └── api.js           # API client
│   ├── globals.css          # Global styles
│   ├── layout.js           # Root layout
│   └── page.js             # Main page
```

## 🤖 AI Technology Stack

- **NLP Processing**: spaCy for natural language processing
- **Semantic Analysis**: Sentence Transformers for text similarity
- **Skill Extraction**: Custom categorized keyword matching
- **Experience Assessment**: Pattern recognition algorithms
- **Machine Learning**: scikit-learn for feature extraction

## 📊 Scoring Algorithm

The AI uses a weighted scoring system:

```
Overall Score = (Skills Match × 40%) + (Experience Match × 30%) + (Semantic Similarity × 30%)
```

**Rating Scale:**
- 🟢 **80%+**: Excellent Match
- 🟡 **60-79%**: Good Match
- 🟠 **40-59%**: Fair Match
- 🔴 **<40%**: Poor Match

## 🛠️ API Endpoints

### Resume Analysis
- `POST /upload-resume` - Upload and analyze resume
- `GET /analysis/{id}` - Get detailed analysis results
- `GET /skills-gap/{id}` - Get skills gap analysis
- `GET /improvement-plan/{id}` - Get improvement recommendations

### Job Matching
- `GET /jobs` - List all available jobs
- `GET /jobs/{job_id}/match/{analysis_id}` - Get job match analysis

### Health Check
- `GET /health` - API health status

## 📞 Support

For questions or issues, please check the documentation or create an issue in the repository.

---

**Made with ❤️ for job seekers everywhere**
