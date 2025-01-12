'use client'

import React from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { User, Users, Shield, Key } from 'lucide-react'

const userManagementMenu = [
  { name: 'Users', href: '/settings/user-management/users', icon: User },
  { name: 'Groups', href: '/settings/user-management/groups', icon: Users },
  { name: 'Roles', href: '/settings/user-management/roles', icon: Shield },
  { name: 'Authentication', href: '/settings/user-management/authentication', icon: Key },
]

export default function UserManagementPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        User Management
      </motion.h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {userManagementMenu.map((item, index) => (
          <motion.div
            key={item.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <Link href={item.href}>
              <Card className="hover:bg-gray-800 transition-colors">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <item.icon className="mr-2 h-6 w-6" />
                    {item.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription>
                    Manage {item.name.toLowerCase()}
                  </CardDescription>
                </CardContent>
              </Card>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

