'use client'

import React from 'react'
import { motion } from 'framer-motion'
import LogViewer from '@/components/LogViewer'

export default function LogsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-center text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Log Viewer
      </motion.h1>
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <LogViewer />
      </motion.div>
    </div>
  )
}

