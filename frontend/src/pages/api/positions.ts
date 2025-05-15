// /frontend/src/pages/api/positions.ts

import type { NextApiRequest, NextApiResponse } from 'next'

const API_URL = process.env.BACKEND_API_URL || 'https://crypto-trading-bot-5ecx.onrender.com'
const API_KEY = process.env.BACKEND_API_KEY

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Proxy tylko GET!
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET'])
    return res.status(405).end(`Method ${req.method} Not Allowed`)
  }

  const apiRes = await fetch(`${API_URL}/positions`, {
    headers: {
      'X-API-Key': API_KEY || ''
    }
  })

  const data = await apiRes.json()
  res.status(apiRes.status).json(data)
}
