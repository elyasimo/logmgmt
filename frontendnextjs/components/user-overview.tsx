'use client'

import { UserPlus, GroupIcon as Groups, Key, History, ShieldIcon as Shield2, KeyRound } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

const features = [
  {
    title: "Users",
    icon: UserPlus,
    description: "Manage user accounts, profiles, and authentication settings.",
    actions: ["Add User", "Import Users", "Export Users"]
  },
  {
    title: "Groups",
    icon: Groups,
    description: "Organize users into teams and manage group permissions.",
    actions: ["Create Group", "Manage Members", "Group Settings"]
  },
  {
    title: "Roles",
    icon: Shield2,
    description: "Define roles and their associated permissions.",
    actions: ["Create Role", "Edit Permissions", "View Role Assignments"]
  },
  {
    title: "Permissions",
    icon: Key,
    description: "Configure granular access controls and permission sets.",
    actions: ["Set Permissions", "Permission Templates", "Access Review"]
  },
  {
    title: "API Keys",
    icon: KeyRound,
    description: "Manage API keys for programmatic access.",
    actions: ["Generate Key", "Revoke Keys", "View Usage"]
  },
  {
    title: "Audit Log",
    icon: History,
    description: "Track user activities and system changes.",
    actions: ["View Logs", "Export Report", "Configure Alerts"]
  }
]

export function UserOverview() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {features.map((feature) => {
        const Icon = feature.icon
        return (
          <Card key={feature.title} className="bg-gray-900/50 border-gray-800">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Icon className="w-5 h-5 text-cyan-400" />
                <CardTitle className="text-gray-100">{feature.title}</CardTitle>
              </div>
              <CardDescription className="text-gray-400">
                {feature.description}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {feature.actions.map((action) => (
                  <Button
                    key={action}
                    variant="secondary"
                    className="bg-gray-800 hover:bg-gray-700 text-gray-200"
                  >
                    {action}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}

