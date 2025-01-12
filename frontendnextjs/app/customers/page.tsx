'use client'

import React from 'react'
import { CustomerList } from '@/components/customer-list'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function CustomersPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Customers</h1>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Automatic Customer Creation</CardTitle>
          <CardDescription>How customers are added to the system</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="mb-4">
            Customers are automatically created in the system when new CNNIDs are encountered in log entries. 
            This process ensures that all customers sending logs are properly registered without manual intervention.
          </p>
          <p className="mb-4">
            In cases where a log entry is received without a parsed CNNID, a default "UNKNOWN" customer is created
            with a unique identifier. This ensures that no log data is lost, even if the source cannot be immediately identified.
          </p>
          <p>
            The system administrator should regularly review and manage these "UNKNOWN" customers to maintain data integrity
            and ensure proper attribution of log entries.
          </p>
        </CardContent>
      </Card>
      <CustomerList />
    </div>
  )
}

