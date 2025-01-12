'use client'

import React from 'react'
import { CustomerCreationForm } from '@/components/customer-creation-form'

export default function CreateCustomerPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Create New Customer</h1>
      <CustomerCreationForm />
    </div>
  )
}

