'use client'
import React from 'react'
import TradeForm from '../components/TradeForm'
import OpenPositionsTable from '../components/OpenPositionsTable'

export default function Dashboard() {
  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Crypto Trading Dashboard</h1>
      <TradeForm />
      <OpenPositionsTable />
    </div>
  )
}
