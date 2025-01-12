'use client'

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function AuditLog() {
  return (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader>
        <CardTitle className="text-gray-100">Audit Log</CardTitle>
        <CardDescription className="text-gray-400">
          Track and review user activities.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-gray-400">Audit log features coming soon...</p>
      </CardContent>
    </Card>
  )
}

