export async function POST(request) {
  try {
    const data = await request.json();
    const { resume_id } = data;
    
    if (!resume_id) {
      return Response.json({ error: "Invalid resume ID" }, { status: 400 });
    }
    
    // Mock job recommendations
    const mockJobs = [
      {
        id: "job_1",
        title: "Software Engineer",
        company: "Tech Corp",
        location: "San Francisco, CA",
        salary: "$120,000 - $150,000",
        match_score: 85,
        skills_match: ["JavaScript", "React", "Node.js"],
        description: "We are looking for a skilled software engineer...",
        requirements: ["Bachelor's degree", "3+ years experience", "Python", "JavaScript"]
      },
      {
        id: "job_2",
        title: "Full Stack Developer",
        company: "StartupXYZ",
        location: "Remote",
        salary: "$100,000 - $130,000",
        match_score: 78,
        skills_match: ["React", "Node.js"],
        description: "Join our dynamic team as a full stack developer...",
        requirements: ["React", "Node.js", "Database experience", "Git"]
      },
      {
        id: "job_3",
        title: "Data Scientist",
        company: "DataCorp",
        location: "New York, NY",
        salary: "$130,000 - $160,000",
        match_score: 72,
        skills_match: ["Python", "SQL"],
        description: "Seeking a data scientist to analyze complex datasets...",
        requirements: ["Machine Learning", "Python", "Statistics", "SQL"]
      }
    ];
    
    return Response.json({
      recommendations: mockJobs,
      total: mockJobs.length,
      resume_skills: ["JavaScript", "React", "Node.js", "Python", "SQL"]
    });
    
  } catch (error) {
    console.error('Job recommendations error:', error);
    return Response.json({ error: "Failed to get job recommendations" }, { status: 500 });
  }
}
