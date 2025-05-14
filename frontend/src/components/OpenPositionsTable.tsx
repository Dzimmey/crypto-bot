'use client'
import React, { useEffect, useState } from 'react'

type Position = {
  symbol: string
  entryPrice: number
  quantity: number
}

const OpenPositionsTable: React.FC = () => {
  const [positions, setPositions] = useState<Position[]>([])
  const [error, setError] = useState<string | null>(null)
  const [debug, setDebug] = useState({ url: '', apiKey: '' })

  useEffect(() => {
 HEAD
  fetch(`${process.env.NEXT_PUBLIC_API_URL}/positions`, {
    headers: {
      'X-API-Key': process.env.NEXT_PUBLIC_API_KEY || ''
    }
  })
    .then((res) => {
      if (!res.ok) throw new Error('Failed to fetch positions')
      return res.json()
    })
    .then((data) => setPositions(data))
    .catch((err) => {
      console.error('FETCH ERROR', err)
      setError(err.message)
    })
}, [])


    const apiUrl = process.env.NEXT_PUBLIC_API_URL || ''
    const apiKey = process.env.NEXT_PUBLIC_API_KEY || ''
    const fullUrl = `${apiUrl}/positions`

    console.log('🔍 Fetching from:', fullUrl)
    console.log('🔐 Using API Key:', apiKey)

    setDebug({ url: fullUrl, apiKey })

    fetch(fullUrl, {
      headers: {
        'X-API-Key': apiKey
      }
    })
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to fetch positions (${res.status})`)
        return res.json()
      })
      .then((data) => {
        console.log('✅ Data received:', data)
        setPositions(data)
      })
      .catch((err) => {
        console.error('❌ FETCH ERROR:', err)
        setError(err.message)
      })
  }, [])
 d1f9469 (Debug: log URL and API Key usage for positions fetch)

  if (error) {
    return (
      <div className="text-red-500">
        <p><strong>Error:</strong> {error}</p>
        <p><strong>URL:</strong> {debug.url}</p>
        <p><strong>API Key:</strong> {debug.apiKey ? 'Provided' : 'Missing'}</p>
      </div>
    )
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Open Positions</h2>
      <table className="min-w-full bg-white border border-gray-200 rounded shadow">
        <thead>
          <tr>
            <th className="border p-2">Symbol</th>
            <th className="border p-2">Entry Price</th>
            <th className="border p-2">Quantity</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((pos, index) => (
            <tr key={index}>
              <td className="border p-2">{pos.symbol}</td>
              <td className="border p-2">{pos.entryPrice}</td>
              <td className="border p-2">{pos.quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default OpenPositionsTable
