'use client'

import OpenPositionsTable from '../components/OpenPositionsTable'

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-gray-100 text-gray-900 p-6">
      <h1 className="text-3xl font-bold mb-6">Crypto Trading Dashboard</h1>
      <OpenPositionsTable />
    </main>
  )
}
