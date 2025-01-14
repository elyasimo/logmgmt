'use client'

import React from 'react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Users, Cog } from 'lucide-react'

const settingsMenu = [
  { name: 'User Management', href: '/settings/user-management', icon: Users },
  { name: 'System Settings', href: '/settings/system', icon: Cog },
]

export default function SettingsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Settings
      </motion.h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {settingsMenu.map((item, index) => (
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
                    Manage {item.name.toLowerCase()} settings
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

