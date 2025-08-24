export async function POST(request) {
  try {
    const data = await request.json();
    const { resume_id, job_description = '' } = data;
    
    if (!resume_id) {
      return Response.json({ error: "Invalid resume ID" }, { status: 400 });
    }
    
    // Simple match scoring based on keywords
    const resumeSkills = ["javascript", "react", "node.js", "python", "sql"];
    const jobText = job_description.toLowerCase();
    
    const matches = resumeSkills.filter(skill => jobText.includes(skill)).length;
    const matchScore = (matches / resumeSkills.length) * 100;
    
    return Response.json({
      match_score: Math.round(matchScore * 10) / 10,
      matched_skills: resumeSkills.filter(skill => jobText.includes(skill)),
      total_skills: resumeSkills.length
    });
    
  } catch (error) {
    console.error('Match score error:', error);
    return Response.json({ error: "Failed to calculate match score" }, { status: 500 });
  }
}
