import { NextResponse } from 'next/server'

export async function POST(request) {
  try {
    const body = await request.json()
    const role = body.role || 'Software'

    // Return a few mock recommendations
    const recommendations = [1, 2, 3].map((i) => ({
      id: `job_${i}`,
      title: `${role} Developer ${i}`,
      company: `Company ${i}`,
      location: 'Remote',
      description: `Sample description for ${role} Developer ${i}`,
      compatibility_score: 70 + i,
    }))

    return NextResponse.json({ success: true, recommendations })
  } catch (err) {
    console.error('job-recommendations error', err)
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
