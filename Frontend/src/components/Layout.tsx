import React from 'react'
import { BarChart3, Users, Shield, Settings, LogOut } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from "@/components/ui/button"

interface LayoutProps {
  children: React.ReactNode
  onLogout: () => void
  isLoggedIn: boolean
}

interface SidebarItem {
  icon: React.ElementType
  label: string
  href: string
  isActive?: boolean
  subItems?: { label: string; href: string }[]
}

export function Layout({ children, onLogout, isLoggedIn }: LayoutProps) {
  const sidebarItems: SidebarItem[] = [
    { icon: BarChart3, label: 'Analytics', href: '/analytics' },
    { icon: Users, label: 'Customers', href: '/customers' },
    { icon: Shield, label: 'Security', href: '/security' },
    { icon: Settings, label: 'Logsettings', href: '/logsettings' },
    {
      icon: Settings,
      label: 'Administration',
      href: '/admin',
      isActive: true,
      subItems: [
        { label: 'User Management', href: '/admin/users' },
        { label: 'Group Management', href: '/admin/groups' },
        { label: 'System Settings', href: '/admin/settings' },
      ],
    },
  ]

  return (
    <div className="min-h-screen bg-background">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center px-4">
          <span className="text-sm">localhost:3000</span>
          <div className="ml-auto flex items-center space-x-4">
            {isLoggedIn && (
              <Button onClick={onLogout} variant="ghost" size="sm">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            )}
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-3.5rem)]">
        {/* Sidebar */}
        {isLoggedIn && (
          <aside className="w-64 bg-indigo-700 text-white">
            <nav className="flex flex-col h-full">
              <div className="flex-1 py-4">
                {sidebarItems.map((item) => (
                  <div key={item.label}>
                    <a
                      href={item.href}
                      className={cn(
                        "flex items-center gap-3 px-4 py-2 text-sm font-medium transition-colors hover:bg-indigo-600",
                        item.isActive && "bg-indigo-800"
                      )}
                    >
                      <item.icon className="h-4 w-4" />
                      {item.label}
                    </a>
                    {item.isActive && item.subItems && (
                      <div className="ml-4 border-l-2 border-indigo-500 pl-4 mt-1">
                        {item.subItems.map((subItem) => (
                          <a
                            key={subItem.label}
                            href={subItem.href}
                            className="block py-2 text-sm text-indigo-100 hover:text-white transition-colors"
                          >
                            {subItem.label}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </nav>
          </aside>
        )}

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}

