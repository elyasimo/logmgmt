'use client'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function RoleManagement() {
  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-gray-100">Role Management</CardTitle>
        <CardDescription className="text-gray-400">
          Define and manage user roles and permissions.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-gray-400">Role management features coming soon...</p>
      </CardContent>
    </Card>
  )
}

