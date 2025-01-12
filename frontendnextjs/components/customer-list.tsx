'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { API_ENDPOINTS } from '@/config/api'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { useToast } from "@/components/ui/use-toast"
import Link from 'next/link'
import { Skeleton } from "@/components/ui/skeleton"
import { AlertCircle } from 'lucide-react'

interface Customer {
  id: number;
  cnnid: string;
  name: string;
}

export function CustomerList() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    fetchCustomers()
  }, [])

  const fetchCustomers = async () => {
    try {
      setLoading(true)
      const response = await axios.get(API_ENDPOINTS.CUSTOMERS)
      setCustomers(response.data)
    } catch (error) {
      console.error('Error fetching customers:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch customers. Please try again.",
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Customer List</CardTitle>
          <CardDescription>Loading customers...</CardDescription>
        </CardHeader>
        <CardContent>
          <Skeleton className="w-full h-[300px]" />
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Customer List</CardTitle>
        <CardDescription>Manage your customers</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-4 p-4 bg-yellow-100 dark:bg-yellow-900 rounded-md">
          <p className="text-sm text-yellow-800 dark:text-yellow-200 flex items-center">
            <AlertCircle className="mr-2" size={16} />
            Customers are automatically created when new CNNIDs are encountered in log entries.
            Logs without a parsed CNNID are assigned to an "UNKNOWN" customer.
          </p>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>CNNID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {customers.map((customer) => (
              <TableRow key={customer.id}>
                <TableCell>{customer.cnnid}</TableCell>
                <TableCell>{customer.name}</TableCell>
                <TableCell>
                  <Link href={`/customers/${customer.cnnid}`} passHref>
                    <Button variant="outline" size="sm">View Details</Button>
                  </Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

