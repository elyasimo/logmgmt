import './globals.css'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@/components/theme-provider'
import { CubeNavigation } from '@/components/cube-navigation'

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
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
          <div className="flex bg-gradient-to-br from-gray-900 to-black text-white min-h-screen">
            <CubeNavigation />
            <main className="flex-1 p-8 ml-64">
              {children}
            </main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  )
}

