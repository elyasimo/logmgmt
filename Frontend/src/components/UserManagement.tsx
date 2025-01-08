import React from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface User {
  username: string
  email: string
  role: string
}

export function UserManagement() {
  const [users] = React.useState<User[]>([
    { username: 'admin', email: 'admin@example.com', role: 'admin' },
    { username: 'user', email: 'user@example.com', role: 'user' },
  ])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold tracking-tight">User Management</h1>
      
      <div className="space-y-4">
        <div className="grid gap-4 max-w-xl">
          <div className="space-y-2">
            <Input
              id="username"
              placeholder="Username"
              className="w-full"
            />
          </div>
          <div className="space-y-2">
            <Input
              id="email"
              type="email"
              placeholder="Email"
              className="w-full"
            />
          </div>
          <div className="space-y-2">
            <Select>
              <SelectTrigger>
                <SelectValue placeholder="User" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="user">User</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button className="w-fit">Add User</Button>
        </div>

        <div className="space-y-4 mt-8">
          {users.map((user) => (
            <div
              key={user.username}
              className="p-4 rounded-lg border bg-card text-card-foreground shadow-sm"
            >
              <div className="space-y-2">
                <div className="space-y-1">
                  <span className="font-medium">Username:</span> {user.username}
                </div>
                <div className="space-y-1">
                  <span className="font-medium">Email:</span> {user.email}
                </div>
                <div className="space-y-1">
                  <span className="font-medium">Role:</span> {user.role}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

