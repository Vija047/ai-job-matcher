export async function POST(request) {
  try {
    const formData = await request.formData();
    const file = formData.get('resume');
    
    if (!file) {
      return Response.json({ error: "No resume file provided" }, { status: 400 });
    }

    // Simple file processing for demo
    const analysis_id = `resume_${Date.now()}`;
    
    // Mock analysis results
    const mockSkills = ["JavaScript", "React", "Node.js", "Python", "SQL"];
    const mockExperience = 3;
    
    return Response.json({
      id: analysis_id,
      skills: mockSkills,
      experience: mockExperience,
      filename: file.name,
      message: "Resume uploaded and analyzed successfully"
    });
    
  } catch (error) {
    console.error('Resume upload error:', error);
    return Response.json({ error: "Failed to process resume" }, { status: 500 });
  }
}
