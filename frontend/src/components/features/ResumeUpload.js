'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, FileText, X, Check, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export default function ResumeUpload({ onAnalysisComplete }) {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [analysisComplete, setAnalysisComplete] = useState(false);

    const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
        if (rejectedFiles.length > 0) {
            toast.error('Please upload a valid PDF or text file');
            return;
        }

        const uploadedFile = acceptedFiles[0];
        if (uploadedFile) {
            setFile(uploadedFile);
            toast.success('File selected successfully!');
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf'],
            'text/plain': ['.txt'],
            'application/msword': ['.doc'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        },
        maxFiles: 1,
        onDragEnter: () => setDragActive(true),
        onDragLeave: () => setDragActive(false)
    });

    const uploadResume = async () => {
        if (!file) {
            toast.error('Please select a file first');
            return;
        }

        setUploading(true);
        const formData = new FormData();
        formData.append('resume', file);

        try {
            console.log('Attempting to upload resume to backend...');
            const response = await fetch('http://localhost:5000/upload-resume', {
                method: 'POST',
                body: formData,
                headers: {
                    // Don't set Content-Type for FormData, let browser set it with boundary
                },
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const result = await response.json();
            console.log('Upload result:', result);

            if (result.status === 'success') {
                const skillsCount = result.total_skills_count || 0;
                const suggestedRole = result.suggested_role || 'Software Engineer';

                toast.success(
                    `✅ Resume analyzed! Found ${skillsCount} skills. Redirecting to dashboard...`,
                    { duration: 3000 }
                );

                // Small delay for user to see the success message before navigating
                setTimeout(() => {
                    setAnalysisComplete(true);
                    onAnalysisComplete(result);
                }, 1500);
            } else {
                throw new Error(result.message || 'Analysis failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            toast.error(`Upload failed: ${error.message}`);
        } finally {
            setUploading(false);
        }
    };

    const uploadDemoResume = async () => {
        setUploading(true);

        try {
            // Create a demo resume text content
            const demoResumeContent = `John Doe
Software Engineer

Contact Information:
- Email: john.doe@email.com
- Phone: (555) 123-4567
- Location: San Francisco, CA

SUMMARY
Experienced software engineer with 5+ years of experience in full-stack development, specializing in React, Node.js, Python, and cloud technologies. Passionate about building scalable applications and working with modern technologies.

TECHNICAL SKILLS
- Programming Languages: JavaScript, Python, TypeScript, Java, C++
- Frontend Technologies: React, Vue.js, HTML5, CSS3, Tailwind CSS
- Backend Technologies: Node.js, Express.js, Django, Flask
- Databases: MongoDB, PostgreSQL, MySQL, Redis
- Cloud Platforms: AWS, Google Cloud Platform, Azure
- DevOps Tools: Docker, Kubernetes, Jenkins, Git, GitHub Actions
- Other: REST APIs, GraphQL, Microservices, Agile, Scrum

WORK EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Led development of microservices architecture serving 1M+ users
- Implemented CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews
- Built scalable REST APIs using Node.js and PostgreSQL

Software Engineer | StartupXYZ | 2019 - 2021  
- Developed responsive web applications using React and TypeScript
- Integrated third-party APIs and payment systems
- Optimized application performance improving load times by 40%
- Collaborated with cross-functional teams using Agile methodologies

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2014 - 2018

CERTIFICATIONS
- AWS Certified Solutions Architect`;

            // Create a blob from the demo content
            const blob = new Blob([demoResumeContent], { type: 'text/plain' });
            const formData = new FormData();
            formData.append('resume', blob, 'demo_resume.txt');

            console.log('Attempting to upload demo resume to backend...');
            const response = await fetch('http://localhost:5000/upload-resume', {
                method: 'POST',
                body: formData,
            });

            console.log('Demo upload response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Demo upload error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
            }

            const result = await response.json();
            console.log('Demo upload result:', result);

            if (result.status === 'success') {
                const skillsCount = result.total_skills_count || 0;
                const suggestedRole = result.suggested_role || 'Software Engineer';

                toast.success(
                    `✅ Demo resume analyzed! Found ${skillsCount} skills. Showing job recommendations...`,
                    { duration: 3000 }
                );

                // Small delay for user to see the success message before navigating
                setTimeout(() => {
                    setAnalysisComplete(true);
                    onAnalysisComplete(result);
                }, 1500);
            } else {
                throw new Error(result.message || 'Analysis failed');
            }
        } catch (error) {
            console.error('Demo upload error:', error);
            toast.error(`Demo upload failed: ${error.message}`);
        } finally {
            setUploading(false);
        }
    };

    const removeFile = () => {
        setFile(null);
        setDragActive(false);
        setAnalysisComplete(false);
    };

    return (
        <div className="max-w-4xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass-card p-8"
            >
                <div className="text-center mb-8">
                    <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
                        Upload Your Resume
                    </h2>
                    <p className="text-gray-600 max-w-2xl mx-auto">
                        Upload your resume and let our AI analyze your skills, experience, and match you with perfect job opportunities
                    </p>
                </div>

                <div className="space-y-6">
                    {/* File Upload Area */}
                    <div
                        {...getRootProps()}
                        className={`
                            relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer
                            transition-all duration-300 ease-in-out
                            ${isDragActive || dragActive
                                ? 'border-blue-500 bg-blue-50 scale-105'
                                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                            }
                            ${file ? 'border-green-400 bg-green-50' : ''}
                        `}
                    >
                        <input {...getInputProps()} />

                        <div className="space-y-4">
                            {!file ? (
                                <>
                                    <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                                        <Upload className="w-8 h-8 text-white" />
                                    </div>
                                    <div>
                                        <p className="text-xl font-semibold text-gray-700 mb-2">
                                            {isDragActive ? 'Drop your resume here!' : 'Drag & drop your resume'}
                                        </p>
                                        <p className="text-gray-500 mb-4">or click to browse files</p>
                                        <p className="text-sm text-gray-400">
                                            Supports PDF, DOC, DOCX, TXT files (max 10MB)
                                        </p>
                                    </div>
                                </>
                            ) : (
                                <div className="flex items-center justify-center space-x-4">
                                    <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
                                        <FileText className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="text-left">
                                        <p className="font-semibold text-gray-700">{file.name}</p>
                                        <p className="text-sm text-gray-500">
                                            {(file.size / (1024 * 1024)).toFixed(2)} MB
                                        </p>
                                    </div>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            removeFile();
                                        }}
                                        className="p-1 hover:bg-red-100 rounded-full transition-colors"
                                    >
                                        <X className="w-5 h-5 text-red-500" />
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Upload Button or Success Message */}
                    {file && !analysisComplete && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center"
                        >
                            <button
                                onClick={uploadResume}
                                disabled={uploading}
                                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold rounded-2xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                            >
                                {uploading ? (
                                    <span className="flex items-center space-x-2">
                                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                        <span>Analyzing Resume...</span>
                                    </span>
                                ) : (
                                    <span className="flex items-center space-x-2">
                                        <Check className="w-5 h-5" />
                                        <span>Analyze Resume</span>
                                    </span>
                                )}
                            </button>
                        </motion.div>
                    )}

                    {/* Demo Button */}
                    {!file && !analysisComplete && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center"
                        >
                            <div className="space-y-4">
                                <div className="text-gray-500 text-sm">
                                    Want to see how it works? Try our demo!
                                </div>
                                <button
                                    onClick={uploadDemoResume}
                                    disabled={uploading}
                                    className="px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-2xl hover:from-green-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                                >
                                    {uploading ? (
                                        <span className="flex items-center space-x-2">
                                            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                                            <span>Processing Demo...</span>
                                        </span>
                                    ) : (
                                        <span className="flex items-center space-x-2">
                                            <span>🚀</span>
                                            <span>Try Demo Resume</span>
                                        </span>
                                    )}
                                </button>
                            </div>
                        </motion.div>
                    )}

                    {/* Success Message */}
                    {analysisComplete && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center p-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl border border-green-200"
                        >
                            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Check className="w-8 h-8 text-white" />
                            </div>
                            <h3 className="text-xl font-bold text-green-800 mb-2">
                                ✅ Resume Analysis Complete!
                            </h3>
                            <p className="text-green-700 mb-4">
                                Your resume has been successfully analyzed. Check out your personalized dashboard for AI recommendations!
                            </p>
                            <button
                                onClick={() => {
                                    setFile(null);
                                    setAnalysisComplete(false);
                                }}
                                className="px-6 py-2 bg-green-600 text-white rounded-xl hover:bg-green-700 transition-colors"
                            >
                                Upload Another Resume
                            </button>
                        </motion.div>
                    )}

                    {/* Features Grid */}
                    <div className="grid md:grid-cols-3 gap-6 mt-12">
                        <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-100">
                            <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <FileText className="w-6 h-6 text-white" />
                            </div>
                            <h3 className="font-semibold text-gray-800 mb-2">Smart Parsing</h3>
                            <p className="text-sm text-gray-600">AI extracts skills, experience, and achievements</p>
                        </div>

                        <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-purple-50 to-pink-100">
                            <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <AlertCircle className="w-6 h-6 text-white" />
                            </div>
                            <h3 className="font-semibold text-gray-800 mb-2">Skill Analysis</h3>
                            <p className="text-sm text-gray-600">Identifies strengths and improvement areas</p>
                        </div>

                        <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-green-50 to-emerald-100">
                            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                                <Check className="w-6 h-6 text-white" />
                            </div>
                            <h3 className="font-semibold text-gray-800 mb-2">Job Matching</h3>
                            <p className="text-sm text-gray-600">Finds perfect opportunities based on your profile</p>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
}
