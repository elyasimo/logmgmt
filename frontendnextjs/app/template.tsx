'use client'

import { ThemeProvider } from '@/components/theme-provider'
import { CubeNavigation } from '@/components/cube-navigation'
import { LayoutDashboard, ScrollText, BarChart3, Bell, Server, Settings, Users, User, Shield, Key, Cog, Briefcase } from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Logs', href: '/logs', icon: ScrollText },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Alerts', href: '/alerts', icon: Bell },
  { name: 'Infrastructure', href: '/infrastructure', icon: Server },
  { name: 'Customers', href: '/customers', icon: Briefcase },
  { 
    name: 'Settings', 
    href: '/settings', 
    icon: Settings,
    submenu: [
      { 
        name: 'User Management', 
        href: '/settings/user-management', 
        icon: Users,
        submenu: [
          { name: 'Users', href: '/settings/user-management/users', icon: User },
          { name: 'Groups', href: '/settings/user-management/groups', icon: Users },
          { name: 'Roles', href: '/settings/user-management/roles', icon: Shield },
          { name: 'Authentication', href: '/settings/user-management/authentication', icon: Key },
        ]
      },
      { name: 'System Settings', href: '/settings/system', icon: Cog },
    ]
  },
]

export default function Template({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
      <div className="flex bg-gradient-to-br from-gray-900 to-black text-white min-h-screen">
        <CubeNavigation navigation={navigation} />
        <main className="flex-1 p-8 ml-64">
          {children}
        </main>
      </div>
    </ThemeProvider>
  )
}

