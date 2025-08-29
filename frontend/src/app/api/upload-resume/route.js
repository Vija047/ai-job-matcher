import { NextResponse } from 'next/server'

export async function POST(request) {
  try {
    // Accept multipart/form-data or JSON (demo)
    const contentType = request.headers.get('content-type') || ''
    if (contentType.includes('application/json')) {
      const data = await request.json()
      return NextResponse.json({ success: true, message: 'Received JSON resume data', data })
    }

    // For multipart, return a simple acknowledgment (Vercel serverless edge has limitations)
    return NextResponse.json({ success: true, message: 'Resume upload endpoint (use backend for full parsing)' })
  } catch (err) {
    console.error('upload-resume error', err)
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
