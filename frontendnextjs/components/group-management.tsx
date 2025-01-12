'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { useToast } from "@/components/ui/use-toast"
import { API_ENDPOINTS } from "@/config/api"

interface Group {
  id: number;
  name: string;
  description: string;
}

export function GroupManagement() {
  const { toast } = useToast()
  const [groups, setGroups] = useState<Group[]>([])
  const [showForm, setShowForm] = useState(false)
  const [newGroup, setNewGroup] = useState({ name: '', description: '' })
  const [editingGroup, setEditingGroup] = useState<Group | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    fetchGroups()
  }, [])

  const fetchGroups = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.GROUPS)
      setGroups(response.data)
    } catch (error) {
      console.error('Error fetching groups:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch groups. Please try again.",
      })
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    if (editingGroup) {
      setEditingGroup({ ...editingGroup, [name]: value })
    } else {
      setNewGroup({ ...newGroup, [name]: value })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      if (editingGroup) {
        await updateGroup(editingGroup)
      } else {
        await createGroup(newGroup)
      }
    } catch (error) {
      handleError(error)
    } finally {
      setIsLoading(false)
    }
  }

  const createGroup = async (group: { name: string; description: string }) => {
    const response = await axios.post(API_ENDPOINTS.GROUPS, group)
    setGroups([...groups, response.data])
    setNewGroup({ name: '', description: '' })
    setShowForm(false)
    toast({
      title: "Group created",
      description: `${response.data.name} has been added successfully.`,
    })
  }

  const updateGroup = async (group: Group) => {
    const response = await axios.put(`${API_ENDPOINTS.GROUPS}/${group.id}`, group)
    setGroups(groups.map(g => g.id === group.id ? response.data : g))
    setEditingGroup(null)
    toast({
      title: "Group updated",
      description: `${response.data.name} has been updated successfully.`,
    })
  }

  const handleEdit = (group: Group) => {
    setEditingGroup(group)
    setShowForm(true)
  }

  const handleCancelEdit = () => {
    setEditingGroup(null)
    setShowForm(false)
  }

  const handleError = (error: unknown) => {
    console.error('Error:', error)
    let errorMessage = "An unexpected error occurred. Please try again."
    if (axios.isAxiosError(error)) {
      errorMessage = error.response?.data?.detail || "Failed to process request. Please try again."
      console.error('Detailed error:', error.response?.data)
    }
    toast({
      variant: "destructive",
      title: "Error",
      description: errorMessage,
    })
  }

  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-gray-100">Group Management</CardTitle>
        <CardDescription className="text-gray-400">
          Create and manage user groups.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <Button 
            className="bg-cyan-600 hover:bg-cyan-700 text-white"
            onClick={() => {
              setShowForm(!showForm)
              setEditingGroup(null)
            }}
          >
            {showForm && !editingGroup ? 'Cancel' : 'Add Group'}
          </Button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} className="space-y-4 mb-6">
            <div className="space-y-2">
              <Label htmlFor="name">Group Name</Label>
              <Input 
                id="name" 
                name="name" 
                value={editingGroup ? editingGroup.name : newGroup.name} 
                onChange={handleInputChange} 
                required 
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Input 
                id="description" 
                name="description" 
                value={editingGroup ? editingGroup.description : newGroup.description} 
                onChange={handleInputChange} 
                required 
              />
            </div>
            <div className="flex space-x-2">
              <Button type="submit" className="bg-green-600 hover:bg-green-700 text-white" disabled={isLoading}>
                {isLoading ? 'Processing...' : (editingGroup ? 'Update Group' : 'Create Group')}
              </Button>
              {editingGroup && (
                <Button type="button" onClick={handleCancelEdit} className="bg-gray-600 hover:bg-gray-700 text-white">
                  Cancel Edit
                </Button>
              )}
            </div>
          </form>
        )}

        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {groups.map((group) => (
              <TableRow key={group.id}>
                <TableCell>{group.name}</TableCell>
                <TableCell>{group.description}</TableCell>
                <TableCell>
                  <Button variant="outline" size="sm" className="mr-2" onClick={() => handleEdit(group)}>Edit</Button>
                  <Button variant="destructive" size="sm">Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

