'use client'

import React, { useState } from 'react'
import axios from 'axios'
import { API_ENDPOINTS } from '@/config/api'
import { useToast } from "@/components/ui/use-toast"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useRouter } from 'next/navigation'

export function CustomerCreationForm() {
  const [cnnid, setCnnid] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await axios.post(API_ENDPOINTS.CUSTOMERS, { cnnid, name })
      toast({
        title: "Success",
        description: "Customer created successfully.",
      })
      router.push('/customers')
    } catch (error) {
      console.error('Error creating customer:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to create customer. Please try again.",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create New Customer</CardTitle>
        <CardDescription>Enter customer details</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label htmlFor="cnnid">CNNID</Label>
            <Input
              id="cnnid"
              value={cnnid}
              onChange={(e) => setCnnid(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <Button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Customer'}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}

