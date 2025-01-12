'use client'

import React from 'react'
import { CustomerDetails } from '@/components/customer-details'
import { useParams } from 'next/navigation'

export default function CustomerDetailsPage() {
  const params = useParams()
  const cnnid = params?.cnnid as string

  if (!cnnid) {
    return <div>Invalid customer ID</div>
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Customer Details</h1>
      <CustomerDetails cnnid={cnnid} />
    </div>
  )
}

