"""
Vercel Serverless API Handler for AI Job Matcher
This file serves as the main API endpoint for Vercel deployment
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the backend directory to the path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the main app from backend
try:
    from app import app as backend_app
    app = backend_app
except ImportError:
    # Fallback: create a minimal app
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy", "message": "AI Job Matcher API is running"})
    
    @app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    def fallback(path):
        return jsonify({"error": "Backend not properly loaded", "path": path}), 500

# Configure CORS for production
CORS(app, origins=['*'], allow_headers=['Content-Type', 'Authorization'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Vercel handler
def handler(request, context):
    """Vercel serverless function handler"""
    return app(request.environ, context)

# For local testing
if __name__ == '__main__':
    app.run(debug=True)
