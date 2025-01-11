"use client"

import React from 'react'
import { motion } from 'framer-motion'
import Dashboard from '@/components/Dashboard'
import VoiceControl from '@/components/VoiceControl'

export default function Home() {
  return (
    <div className="space-y-8">
      <motion.h1 
        className="text-4xl font-bold mb-8 text-center text-neon-blue"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Nexus Log Management System
      </motion.h1>
      <VoiceControl />
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <Dashboard />
      </motion.div>
    </div>
  )
}

