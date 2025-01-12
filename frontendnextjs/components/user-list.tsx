'use client'

import React, { useState, useCallback, useEffect } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import axios from 'axios'
import { useToast } from "@/components/ui/use-toast"
import { API_ENDPOINTS } from "@/config/api"

interface User {
  id: number;
  username: string;
  email: string;
  name: string;
  role: string;
  is_active: boolean;
  password?: string;
}

export function UserList() {
  const { toast } = useToast()
  const [users, setUsers] = useState<User[]>([])
  const [showForm, setShowForm] = useState(false)
  const [newUser, setNewUser] = useState({ username: '', name: '', email: '', role: '', password: '' })
  const [editingUser, setEditingUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const fetchUsers = useCallback(async () => {
    try {
      const response = await axios.get(`${API_ENDPOINTS.USERS}`)
      setUsers(response.data)
    } catch (error) {
      console.error('Error fetching users:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch users. Please try again.",
      })
    }
  }, [toast])

  useEffect(() => {
    fetchUsers()
  }, [fetchUsers])

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    if (editingUser) {
      setEditingUser(prev => prev ? { ...prev, [name]: value } : null)
    } else {
      setNewUser(prev => ({ ...prev, [name]: value }))
    }
  }, [editingUser])

  const handleRoleChange = useCallback((value: string) => {
    if (editingUser) {
      setEditingUser(prev => prev ? { ...prev, role: value } : null)
    } else {
      setNewUser(prev => ({ ...prev, role: value }))
    }
  }, [editingUser])

  const toggleForm = useCallback(() => {
    setShowForm(prev => !prev)
    setEditingUser(null)
    if (showForm) {
      setNewUser({ username: '', name: '', email: '', role: '', password: '' })
    }
  }, [showForm])

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    const userData = editingUser || newUser
    if (!userData.username || !userData.name || !userData.email || !userData.role || (!editingUser && !newUser.password)) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please fill in all fields.",
      })
      return
    }
    setIsLoading(true)
    try {
      let response;
      if (editingUser) {
        const { password, ...userDataWithoutPassword } = userData
        console.log('Updating user with data:', userDataWithoutPassword)
        response = await axios.put(`${API_ENDPOINTS.USERS}/${editingUser.id}`, userDataWithoutPassword)
      } else {
        console.log('Creating user with data:', userData)
        response = await axios.post(`${API_ENDPOINTS.USERS}`, userData)
      }
      const updatedUser = response.data
      setUsers(prev => editingUser 
        ? prev.map(user => user.id === updatedUser.id ? updatedUser : user)
        : [...prev, updatedUser]
      )
      setNewUser({ username: '', name: '', email: '', role: '', password: '' })
      setEditingUser(null)
      setShowForm(false)
      toast({
        title: editingUser ? "User updated" : "User created",
        description: `${updatedUser.name} has been ${editingUser ? 'updated' : 'added'} successfully.`,
      })
    } catch (error) {
      console.error('Error creating/updating user:', error)
      let errorMessage = "An unexpected error occurred. Please try again."
      if (axios.isAxiosError(error)) {
        errorMessage = error.response?.data?.detail || `Failed to ${editingUser ? 'update' : 'create'} user. Please try again.`
        console.error('Detailed error:', error.response?.data)
      }
      toast({
        variant: "destructive",
        title: "Error",
        description: errorMessage,
      })
    } finally {
      setIsLoading(false)
    }
  }, [newUser, editingUser, setUsers, toast])

  const handleEdit = useCallback((user: User) => {
    setEditingUser(user)
    setShowForm(true)
  }, [])

  const handleDelete = useCallback(async (userId: number) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await axios.delete(`${API_ENDPOINTS.USERS}/${userId}`)
        setUsers(prev => prev.filter(user => user.id !== userId))
        toast({
          title: "User deleted",
          description: "The user has been deleted successfully.",
        })
      } catch (error) {
        console.error('Error deleting user:', error)
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to delete user. Please try again.",
        })
      }
    }
  }, [toast])

  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-gray-100">User Management</CardTitle>
        <CardDescription className="text-gray-400">
          Add, edit, and manage user accounts.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex justify-between items-center mb-6">
          <Button 
            type="button"
            onClick={toggleForm}
            className="bg-cyan-600 hover:bg-cyan-700 text-white"
          >
            {showForm ? 'Cancel' : 'Add User'}
          </Button>
        </div>

        {showForm && (
          <form onSubmit={handleSubmit} className="space-y-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input 
                  id="username" 
                  name="username" 
                  value={editingUser?.username || newUser.username} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-gray-800 border-gray-700 text-white w-full"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">Name</Label>
                <Input 
                  id="name" 
                  name="name" 
                  value={editingUser?.name || newUser.name} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-gray-800 border-gray-700 text-white w-full"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input 
                  id="email" 
                  name="email" 
                  type="email" 
                  value={editingUser?.email || newUser.email} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-gray-800 border-gray-700 text-white w-full"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="role">Role</Label>
                <Select onValueChange={handleRoleChange} value={editingUser?.role || newUser.role || undefined}>
                  <SelectTrigger className="bg-gray-800 border-gray-700 text-white w-full">
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Admin">Admin</SelectItem>
                    <SelectItem value="User">User</SelectItem>
                    <SelectItem value="Manager">Manager</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            {!editingUser && (
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input 
                  id="password" 
                  name="password" 
                  type="password" 
                  value={newUser.password} 
                  onChange={handleInputChange} 
                  required 
                  className="bg-gray-800 border-gray-700 text-white w-full"
                />
              </div>
            )}
            <Button 
              type="submit" 
              className="bg-green-600 hover:bg-green-700 text-white w-full md:w-auto"
              disabled={isLoading}
            >
              {isLoading ? 'Processing...' : (editingUser ? 'Update User' : 'Create User')}
            </Button>
          </form>
        )}

        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Username</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="text-gray-300">{user.name}</TableCell>
                  <TableCell className="text-gray-300">{user.username}</TableCell>
                  <TableCell className="text-gray-300">{user.email}</TableCell>
                  <TableCell className="text-gray-300">{user.role}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm" className="mr-2" onClick={() => handleEdit(user)}>Edit</Button>
                    <Button variant="destructive" size="sm" onClick={() => handleDelete(user.id)}>Delete</Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}

