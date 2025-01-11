'use client'

import React from 'react'
import { motion } from 'framer-motion'

export default function SettingsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1 
        className="text-3xl font-bold mb-6 text-neon-blue"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Settings
      </motion.h1>
      <div className="grid gap-6">
        <motion.div 
          className="glassmorphism p-6"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">System Preferences</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">Dark Mode</label>
              <button className="px-4 py-2 bg-gray-800 rounded-md hover:bg-gray-700 transition-colors">
                Enabled
              </button>
            </div>
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">Notifications</label>
              <button className="px-4 py-2 bg-gray-800 rounded-md hover:bg-gray-700 transition-colors">
                Enabled
              </button>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="glassmorphism p-6"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">Log Settings</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">Auto Refresh</label>
              <select className="px-4 py-2 bg-gray-800 rounded-md hover:bg-gray-700 transition-colors">
                <option value="0">Disabled</option>
                <option value="30">Every 30 seconds</option>
                <option value="60">Every minute</option>
                <option value="300">Every 5 minutes</option>
              </select>
            </div>
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">Default Log View</label>
              <select className="px-4 py-2 bg-gray-800 rounded-md hover:bg-gray-700 transition-colors">
                <option value="compact">Compact</option>
                <option value="detailed">Detailed</option>
                <option value="raw">Raw</option>
              </select>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="glassmorphism p-6"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <h2 className="text-xl font-semibold mb-4 text-neon-pink">API Configuration</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">API Endpoint</label>
              <input 
                type="text" 
                value={process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} 
                readOnly
                className="px-4 py-2 bg-gray-800 rounded-md text-gray-400"
              />
            </div>
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium">API Version</label>
              <span className="px-4 py-2 bg-gray-800 rounded-md">v1</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

