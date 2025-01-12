import './globals.css'
import { Inter } from 'next/font/google'
import { Toaster } from "@/components/ui/toaster"

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Nexus Log - Advanced Log Management',
  description: 'Next-generation log management system with futuristic interface',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <div className="flex bg-gradient-to-br from-gray-900 to-black text-white min-h-screen">
          {children}
        </div>
        <Toaster />
      </body>
    </html>
  )
}

