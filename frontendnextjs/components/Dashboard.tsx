'use client'

import React, { useEffect, useState } from 'react'
import axios from 'axios'
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
import { API_ENDPOINTS } from '@/config/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const Dashboard = () => {
  const [vendorCounts, setVendorCounts] = useState<Record<string, number>>({})
  const [severityDistribution, setSeverityDistribution] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        
        const [vendorResponse, severityResponse] = await Promise.all([
          axios.get(API_ENDPOINTS.VENDOR_COUNTS),
          axios.get(API_ENDPOINTS.SEVERITY_DISTRIBUTION)
        ])

        setVendorCounts(vendorResponse.data)
        setSeverityDistribution(severityResponse.data)
      } catch (error) {
        console.error('Dashboard data fetch error:', error)
        if (axios.isAxiosError(error)) {
          if (error.code === 'ERR_NETWORK') {
            setError('Unable to connect to the server. Please check your connection.')
          } else if (error.response?.status === 404) {
            setError('The requested data is not available.')
          } else {
            setError(`Error: ${error.message}`)
          }
        } else {
          setError('An unexpected error occurred')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: 'rgba(255, 255, 255, 0.8)',
          font: {
            size: 12
          }
        }
      },
      title: {
        display: false
      }
    },
    scales: {
      x: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.8)'
        }
      },
      y: {
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.8)'
        }
      }
    }
  }

  const doughnutOptions = {
    ...chartOptions,
    scales: undefined,
    plugins: {
      ...chartOptions.plugins,
      legend: {
        ...chartOptions.plugins.legend,
        position: 'bottom' as const
      }
    }
  }

  const vendorChartData = {
    labels: Object.keys(vendorCounts),
    datasets: [
      {
        label: 'Log Count by Vendor',
        data: Object.values(vendorCounts),
        backgroundColor: 'rgba(0, 243, 255, 0.6)', // neon blue
        borderColor: 'rgba(0, 243, 255, 1)',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  }

  const severityChartData = {
    labels: Object.keys(severityDistribution),
    datasets: [
      {
        data: Object.values(severityDistribution),
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',  // low - pink
          'rgba(0, 243, 255, 0.8)',   // high - neon blue
          'rgba(255, 206, 86, 0.8)',  // critical - yellow
          'rgba(75, 192, 192, 0.8)',  // medium - turquoise
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(0, 243, 255, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-pulse text-neon-blue">Loading dashboard data...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] p-4">
        <div className="text-red-500 mb-4">{error}</div>
        <button 
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-neon-blue text-white rounded hover:bg-blue-600 transition-colors"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div className="glassmorphism p-6">
        <h3 className="text-xl font-bold mb-6 text-neon-blue">Log Count by Vendor</h3>
        <div className="h-[250px]">
          <Bar data={vendorChartData} options={chartOptions} />
        </div>
      </div>
      <div className="glassmorphism p-6">
        <h3 className="text-xl font-bold mb-6 text-neon-pink">Severity Distribution</h3>
        <div className="h-[250px]">
          <Doughnut data={severityChartData} options={doughnutOptions} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard

