"use client"

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LayoutDashboard, ListFilter, BarChart, Settings, AlertTriangle, Server, Users, Shield } from 'lucide-react'

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Logs', path: '/logs', icon: ListFilter },
  { name: 'Analytics', path: '/analytics', icon: BarChart },
  { name: 'Alerts', path: '/alerts', icon: AlertTriangle },
  { name: 'Infrastructure', path: '/infrastructure', icon: Server },
  { name: 'Users', path: '/users', icon: Users },
  { name: 'Security', path: '/security', icon: Shield },
  { name: 'Settings', path: '/settings', icon: Settings },
]

export const CubeNavigation = () => {
  const pathname = usePathname()

  return (
    <nav className="fixed left-0 top-0 bottom-0 w-64 bg-gray-900 text-white p-4 overflow-y-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-neon-blue">Nexus Log</h1>
        <p className="text-sm text-gray-400">Advanced Log Management</p>
      </div>
      <ul className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.path
          return (
            <li key={item.name}>
              <Link 
                href={item.path}
                className={`flex items-center p-3 rounded-lg transition-colors ${
                  isActive 
                    ? 'bg-neon-blue text-black' 
                    : 'hover:bg-gray-800'
                }`}
              >
                <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-black' : 'text-neon-pink'}`} />
                <span className="font-medium">{item.name}</span>
              </Link>
            </li>
          )
        })}
      </ul>
    </nav>
  )
}

