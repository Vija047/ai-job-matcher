export async function GET() {
  return Response.json({
    status: "healthy",
    message: "AI Job Matcher API is running",
    timestamp: new Date().toISOString()
  });
}
