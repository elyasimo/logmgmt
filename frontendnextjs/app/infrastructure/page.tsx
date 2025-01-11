'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Server } from 'lucide-react'

export default function InfrastructurePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-center text-neon-blue flex items-center justify-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Server className="mr-2" />
        Infrastructure Overview
      </motion.h1>
      <motion.div 
        className="glassmorphism p-6"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <p className="text-center text-lg">
          Infrastructure monitoring and management features are in development. Check back soon for updates!
        </p>
      </motion.div>
    </div>
  )
}

