'use client'
import React from 'react'
import OpenPositionsTable from '../components/OpenPositionsTable'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Crypto Trading Dashboard</h1>
        <OpenPositionsTable />
        {/* Możesz dodać kolejne komponenty tutaj */}
      </div>
    </div>
  )
}
