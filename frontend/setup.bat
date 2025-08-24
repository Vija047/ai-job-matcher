@echo off
echo 🚀 Setting up AI Job Matcher Application...

REM Backend Setup
echo 📦 Setting up backend...
cd backend

REM Create virtual environment
echo 🔧 Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install -r requirements.txt

REM Download spaCy model
echo 🤖 Downloading spaCy English model...
python -m spacy download en_core_web_sm

REM Download NLTK data
echo 📚 Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); print('✅ NLTK data downloaded successfully!')"

echo ✅ Backend setup complete!

REM Return to main directory
cd ..

REM Frontend Setup
echo 📦 Setting up frontend...

REM Install Node.js dependencies
echo 📥 Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Start the backend: cd backend ^&^& python app.py
echo 2. Start the frontend: npm run dev
echo 3. Open http://localhost:3000 in your browser
echo.
echo 💡 Tips:
echo - Place your PDF resume in the data/ folder
echo - Backend runs on http://localhost:5000
echo - Frontend runs on http://localhost:3000
echo.
echo 🎯 Happy job matching!

pause
