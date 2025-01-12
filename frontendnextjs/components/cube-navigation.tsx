'use client'

import React, { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import { TypeIcon as type, type LucideIcon, ChevronDown, ChevronRight } from 'lucide-react'

interface NavigationItem {
  name: string;
  href: string;
  icon: LucideIcon;
  submenu?: NavigationItem[];
}

interface CubeNavigationProps {
  navigation: NavigationItem[];
}

const MenuItem: React.FC<{ item: NavigationItem; isActive: boolean; level: number }> = ({ item, isActive, level }) => {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  const hasSubmenu = item.submenu && item.submenu.length > 0
  const isActiveSubmenu = hasSubmenu && item.submenu && pathname ? item.submenu.some(subItem => pathname.startsWith(subItem.href)) : false

  return (
    <li>
      <Link href={hasSubmenu ? '#' : item.href} passHref>
        <motion.div
          className={`flex items-center p-2 rounded-lg cursor-pointer ${
            (isActive || isActiveSubmenu) ? 'bg-cyan-500/10 text-cyan-400' : 'text-gray-300 hover:bg-gray-800'
          }`}
          style={{ paddingLeft: `${level * 1}rem` }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => hasSubmenu && setIsOpen(!isOpen)}
        >
          <item.icon className="w-6 h-6 mr-3" />
          <span>{item.name}</span>
          {hasSubmenu && (
            <motion.div
              className="ml-auto"
              initial={false}
              animate={{ rotate: isOpen ? 180 : 0 }}
            >
              {isOpen ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </motion.div>
          )}
          {(isActive || isActiveSubmenu) && (
            <motion.div
              className="absolute left-0 w-1 h-8 bg-cyan-400 rounded-r-full"
              layoutId="activeIndicator"
            />
          )}
        </motion.div>
      </Link>
      {hasSubmenu && isOpen && item.submenu && (
        <ul className="mt-2 space-y-2">
          {item.submenu.map((subItem) => (
            <MenuItem key={subItem.name} item={subItem} isActive={pathname === subItem.href} level={level + 1} />
          ))}
        </ul>
      )}
    </li>
  )
}

export function CubeNavigation({ navigation }: CubeNavigationProps) {
  return (
    <nav className="fixed left-0 top-0 bottom-0 w-64 bg-gray-900 p-4 overflow-y-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-cyan-400">Nexus Log</h1>
        <p className="text-sm text-gray-400">Advanced Log Management</p>
      </div>
      <ul className="space-y-2">
        {navigation.map((item) => (
          <MenuItem key={item.name} item={item} isActive={usePathname() === item.href} level={0} />
        ))}
      </ul>
    </nav>
  )
}

