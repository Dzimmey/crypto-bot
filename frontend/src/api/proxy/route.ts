// frontend/src/app/api/proxy/route.ts
import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'https://crypto-trading-bot-5ecx.onrender.com'

export async function OPTIONS() {
  // Pozwala na preflight z dowolnego miejsca
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    },
  })
}

export async function GET(req: NextRequest) {
  const path = req.nextUrl.searchParams.get('path') || ''
  const url = `${BACKEND_URL}/${path}`

  const apiKey = process.env.NEXT_PUBLIC_API_KEY || ''

  const backendRes = await fetch(url, {
    method: 'GET',
    headers: {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json',
    },
    // credentials: 'include', // jeśli potrzebujesz cookies
  })

  const text = await backendRes.text()
  return new NextResponse(text, {
    status: backendRes.status,
    headers: { 'Content-Type': 'application/json' }
  })
}

export async function POST(req: NextRequest) {
  const path = req.nextUrl.searchParams.get('path') || ''
  const url = `${BACKEND_URL}/${path}`

  const apiKey = process.env.NEXT_PUBLIC_API_KEY || ''
  const body = await req.text()

  const backendRes = await fetch(url, {
    method: 'POST',
    headers: {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json',
    },
    body,
  })

  const text = await backendRes.text()
  return new NextResponse(text, {
    status: backendRes.status,
    headers: { 'Content-Type': 'application/json' }
  })
}
