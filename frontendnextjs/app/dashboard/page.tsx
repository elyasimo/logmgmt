'use client'

import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { API_ENDPOINTS } from "@/config/api"
import { Bar, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

interface DashboardData {
  totalLogs: number;
  logsBySeverity: { [key: string]: number };
  logsByVendor: { [key: string]: number };
  recentLogs: any[]; // We'll type this more specifically later
}

export default function DashboardPage() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setIsLoading(true)
        setError(null)

        const [totalLogsResponse, logsBySeverityResponse, logsByVendorResponse, recentLogsResponse] = await Promise.all([
          axios.get(`${API_ENDPOINTS.LOGS}/count`),
          axios.get(`${API_ENDPOINTS.LOGS}/severity-distribution`),
          axios.get(`${API_ENDPOINTS.LOGS}/vendor-counts`),
          axios.get(`${API_ENDPOINTS.LOGS}?page=1&page_size=5`) // Fetch only 5 recent logs
        ])

        setDashboardData({
          totalLogs: totalLogsResponse.data.total_logs,
          logsBySeverity: logsBySeverityResponse.data,
          logsByVendor: logsByVendorResponse.data,
          recentLogs: recentLogsResponse.data.items
        })
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        setError('Failed to fetch dashboard data. Please try again later.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  const renderMetricCard = (title: string, value: number | string) => (
    <Card className="bg-gray-900/50 border-gray-800">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-400">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-cyan-400">{value}</div>
      </CardContent>
    </Card>
  )

  const renderSeverityChart = () => {
    if (!dashboardData) return null

    const data = {
      labels: Object.keys(dashboardData.logsBySeverity),
      datasets: [
        {
          data: Object.values(dashboardData.logsBySeverity),
          backgroundColor: [
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)',
            'rgba(255, 206, 86, 0.8)',
            'rgba(75, 192, 192, 0.8)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
          ],
          borderWidth: 1,
        },
      ],
    }

    return (
      <Card className="bg-gray-900/50 border-gray-800">
        <CardHeader>
          <CardTitle className="text-gray-400">Log Severity Distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <Doughnut 
            data={data} 
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'bottom',
                  labels: {
                    color: 'rgba(255, 255, 255, 0.8)'
                  }
                }
              }
            }} 
          />
        </CardContent>
      </Card>
    )
  }

  const renderVendorChart = () => {
    if (!dashboardData) return null

    const data = {
      labels: Object.keys(dashboardData.logsByVendor),
      datasets: [
        {
          label: 'Logs by Vendor',
          data: Object.values(dashboardData.logsByVendor),
          backgroundColor: 'rgba(0, 243, 255, 0.6)',
          borderColor: 'rgba(0, 243, 255, 1)',
          borderWidth: 1,
        },
      ],
    }

    return (
      <Card className="bg-gray-900/50 border-gray-800">
        <CardHeader>
          <CardTitle className="text-gray-400">Logs by Vendor</CardTitle>
        </CardHeader>
        <CardContent>
          <Bar 
            data={data} 
            options={{
              responsive: true,
              plugins: {
                legend: {
                  display: false
                }
              },
              scales: {
                x: {
                  ticks: {
                    color: 'rgba(255, 255, 255, 0.8)'
                  }
                },
                y: {
                  ticks: {
                    color: 'rgba(255, 255, 255, 0.8)'
                  }
                }
              }
            }} 
          />
        </CardContent>
      </Card>
    )
  }

  const renderRecentLogs = () => {
    if (!dashboardData) return null

    return (
      <Card className="bg-gray-900/50 border-gray-800">
        <CardHeader>
          <CardTitle className="text-gray-400">Recent Logs</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {dashboardData.recentLogs.map((log) => (
              <div key={log.id} className="bg-gray-800 p-4 rounded-md">
                <p className="text-sm text-gray-400">{new Date(log.timestamp).toLocaleString()}</p>
                <p className="text-cyan-400">{log.message}</p>
                <p className="text-xs text-gray-500">Severity: {log.severity} | Vendor: {log.vendor}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-neon-blue">Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="bg-gray-900/50 border-gray-800">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium"><Skeleton className="h-4 w-[150px]" /></CardTitle>
              </CardHeader>
              <CardContent>
                <Skeleton className="h-8 w-[100px]" />
              </CardContent>
            </Card>
          ))}
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <Card className="bg-gray-900/50 border-gray-800">
            <CardHeader>
              <CardTitle><Skeleton className="h-6 w-[200px]" /></CardTitle>
            </CardHeader>
            <CardContent>
              <Skeleton className="h-[300px] w-full" />
            </CardContent>
          </Card>
          <Card className="bg-gray-900/50 border-gray-800">
            <CardHeader>
              <CardTitle><Skeleton className="h-6 w-[200px]" /></CardTitle>
            </CardHeader>
            <CardContent>
              <Skeleton className="h-[300px] w-full" />
            </CardContent>
          </Card>
        </div>
        <Card className="bg-gray-900/50 border-gray-800">
          <CardHeader>
            <CardTitle><Skeleton className="h-6 w-[200px]" /></CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <Skeleton key={i} className="h-20 w-full" />
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-neon-blue">Dashboard</h1>
        <Card className="bg-red-900/50 border-red-800">
          <CardContent className="p-4">
            <p className="text-red-400">{error}</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Dashboard
      </motion.h1>
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        {renderMetricCard("Total Logs", dashboardData?.totalLogs || 0)}
        {renderMetricCard("Critical Logs", dashboardData?.logsBySeverity.critical || 0)}
        {renderMetricCard("High Severity Logs", dashboardData?.logsBySeverity.high || 0)}
        {renderMetricCard("Medium Severity Logs", dashboardData?.logsBySeverity.medium || 0)}
      </motion.div>
      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        {renderSeverityChart()}
        {renderVendorChart()}
      </motion.div>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        {renderRecentLogs()}
      </motion.div>
    </div>
  )
}

