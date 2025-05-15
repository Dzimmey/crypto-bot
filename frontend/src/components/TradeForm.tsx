'use client'
import React, { useState } from 'react'

const TradeForm: React.FC = () => {
  const [symbol, setSymbol] = useState('')
  const [action, setAction] = useState<'BUY' | 'SELL'>('BUY')
  const [quantity, setQuantity] = useState('0.01')
  const [result, setResult] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setResult(null)
    setError(null)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/trade`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': process.env.NEXT_PUBLIC_API_KEY || '',
        },
        body: JSON.stringify({ symbol, action, quantity }),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`)
      const data = await res.json()
      setResult(`✅ Trade sent: ${data.symbol} ${data.action} (${data.quantity})`)
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || 'Failed to send trade')
      } else {
        setError('Failed to send trade')
      }
    }
  }

  return (
    <form className="p-4 bg-gray-50 rounded shadow mb-4" onSubmit={handleSubmit}>
      <div className="mb-2 flex flex-col gap-2 md:flex-row">
        <input
          className="border p-2 rounded flex-1"
          placeholder="Symbol, np. BTCUSDT"
          value={symbol}
          onChange={e => setSymbol(e.target.value.toUpperCase())}
          required
        />
        <select
          className="border p-2 rounded"
          value={action}
          onChange={e => setAction(e.target.value as 'BUY' | 'SELL')}
        >
          <option value="BUY">BUY</option>
          <option value="SELL">SELL</option>
        </select>
        <input
          className="border p-2 rounded flex-1"
          placeholder="Ilość"
          value={quantity}
          type="number"
          min="0"
          step="any"
          onChange={e => setQuantity(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Wyślij zlecenie
        </button>
      </div>
      {result && <div className="text-green-600">{result}</div>}
      {error && <div className="text-red-600">{error}</div>}
    </form>
  )
}

export default TradeForm
