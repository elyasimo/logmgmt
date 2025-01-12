'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { API_ENDPOINTS } from '@/config/api'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/components/ui/use-toast"
import { Skeleton } from "@/components/ui/skeleton"
import { AlertTriangle } from 'lucide-react'

interface Customer {
  id: number;
  cnnid: string;
  name: string;
}

interface CustomerDetailsProps {
  cnnid: string;
}

export function CustomerDetails({ cnnid }: CustomerDetailsProps) {
  const [customer, setCustomer] = useState<Customer | null>(null)
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    fetchCustomerDetails()
  }, [cnnid])

  const fetchCustomerDetails = async () => {
    try {
      setLoading(true)
      const response = await axios.get(`${API_ENDPOINTS.CUSTOMERS}/${cnnid}`)
      setCustomer(response.data)
    } catch (error) {
      console.error('Error fetching customer details:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch customer details. Please try again.",
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Customer Details</CardTitle>
          <CardDescription>Loading customer information...</CardDescription>
        </CardHeader>
        <CardContent>
          <Skeleton className="w-full h-[200px]" />
        </CardContent>
      </Card>
    )
  }

  if (!customer) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Customer Details</CardTitle>
          <CardDescription>Customer not found</CardDescription>
        </CardHeader>
        <CardContent>
          <p>The requested customer could not be found.</p>
        </CardContent>
      </Card>
    )
  }

  const isUnknownCustomer = customer.cnnid.startsWith('UNKNOWN_')

  return (
    <Card>
      <CardHeader>
        <CardTitle>Customer Details</CardTitle>
        <CardDescription>Information about {customer.name}</CardDescription>
      </CardHeader>
      <CardContent>
        {isUnknownCustomer && (
          <div className="mb-4 p-4 bg-yellow-100 dark:bg-yellow-900 rounded-md flex items-start">
            <AlertTriangle className="mr-2 mt-1 flex-shrink-0" size={20} />
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              This is an automatically generated customer for logs with unparsed CNNIDs. 
              The system administrator should review and manage these entries to maintain data integrity.
            </p>
          </div>
        )}
        <div className="space-y-2">
          <p><strong>CNNID:</strong> {customer.cnnid}</p>
          <p><strong>Name:</strong> {customer.name}</p>
          {/* Add more customer details here as needed */}
        </div>
      </CardContent>
    </Card>
  )
}

