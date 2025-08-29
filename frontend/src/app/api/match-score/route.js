import { NextResponse } from 'next/server'

export async function POST(request) {
  try {
    const { skills = [], job } = await request.json()
    const text = `${job?.title || ''} ${job?.description || ''} ${job?.requirements || ''}`.toLowerCase()
    let matches = 0
    for (const s of skills) if (text.includes(s.toLowerCase())) matches++
    const score = skills.length ? Math.round((matches / skills.length) * 100) : 50

    return NextResponse.json({ success: true, match_score: score })
  } catch (err) {
    console.error('match-score error', err)
    return NextResponse.json({ error: String(err) }, { status: 500 })
  }
}
