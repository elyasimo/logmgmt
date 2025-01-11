'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Bar, Doughnut, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
)

export default function AnalyticsPage() {
  // Mock data for charts
  const logVolumeData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Log Volume',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: 'rgba(0, 243, 255, 0.6)',
        borderColor: 'rgba(0, 243, 255, 1)',
        borderWidth: 1,
      },
    ],
  }

  const severityDistributionData = {
    labels: ['Critical', 'Error', 'Warning', 'Info'],
    datasets: [
      {
        data: [300, 50, 100, 200],
        backgroundColor: [
          'rgba(255, 99, 132, 0.8)',
          'rgba(255, 206, 86, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(75, 192, 192, 0.8)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  }

  const responseTimeData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Response Time (ms)',
        data: [100, 120, 115, 134, 108, 95],
        fill: false,
        borderColor: 'rgba(255, 0, 255, 1)',
        tension: 0.1,
      },
    ],
  }

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

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-center text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Analytics Dashboard
      </motion.h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <motion.div 
          className="glassmorphism p-6"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">Log Volume Over Time</h2>
          <div className="h-[300px]">
            <Bar data={logVolumeData} options={chartOptions} />
          </div>
        </motion.div>
        <motion.div 
          className="glassmorphism p-6"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">Severity Distribution</h2>
          <div className="h-[300px]">
            <Doughnut data={severityDistributionData} options={{...chartOptions, aspectRatio: 1}} />
          </div>
        </motion.div>
        <motion.div 
          className="glassmorphism p-6 md:col-span-2"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">System Response Time</h2>
          <div className="h-[300px]">
            <Line data={responseTimeData} options={chartOptions} />
          </div>
        </motion.div>
      </div>
    </div>
  )
}

