'use client'

import React, { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import { useDebounce } from 'use-debounce'
import { API_ENDPOINTS } from '@/config/api'
import { Search, SlidersHorizontal, ChevronUp, ChevronDown, Download, Loader2 } from 'lucide-react'

interface Log {
  id: string
  timestamp: string
  message: string
  severity: string
  vendor: string
  cnnid: string
  device_type: string
}

interface FilterState {
  query: string
  vendor: string
  severity: string
  device_type: string
}

interface SortState {
  column: string
  direction: 'asc' | 'desc'
}

const LogViewer: React.FC = () => {
  const [logs, setLogs] = useState<Log[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [logsPerPage] = useState(10)
  const [vendors, setVendors] = useState<string[]>([])
  const [showFilters, setShowFilters] = useState(false)
  const [filters, setFilters] = useState<FilterState>({
    query: '',
    vendor: '',
    severity: '',
    device_type: ''
  })
  const [sort, setSort] = useState<SortState>({
    column: 'timestamp',
    direction: 'desc'
  })

  const [debouncedFilters] = useDebounce(filters, 300)

  const fetchLogs = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${API_ENDPOINTS.LOGS}`, {
        params: {
          page: currentPage,
          page_size: logsPerPage,
          query: debouncedFilters.query,
          vendor: debouncedFilters.vendor,
          severity: debouncedFilters.severity,
          device_type: debouncedFilters.device_type,
          sort_by: sort.column,
          sort_order: sort.direction
        }
      })
      setLogs(response.data.items)
      setTotalPages(response.data.total_pages)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        setError(`Failed to fetch logs: ${err.response.data.detail || 'Unknown error'}`)
      } else {
        setError('Failed to fetch logs. Please try again later.')
      }
      console.error('Error fetching logs:', err)
    } finally {
      setLoading(false)
    }
  }, [currentPage, debouncedFilters, sort, logsPerPage])

  useEffect(() => {
    fetchLogs()
  }, [fetchLogs])

  useEffect(() => {
    fetchVendors()
  }, [])

  const fetchVendors = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINTS.LOGS}/vendors`)
      setVendors(response.data)
    } catch (err) {
      console.error('Error fetching vendors:', err)
      setError('Failed to fetch vendors. Please try again later.')
    }
  }

  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }))
    setCurrentPage(1)
  }

  const handleSort = (column: string) => {
    setSort(prev => ({
      column,
      direction: prev.column === column && prev.direction === 'asc' ? 'desc' : 'asc'
    }))
  }

  const handleExport = async () => {
    try {
      const response = await axios.get(`${API_ENDPOINTS.LOGS}/export`, {
        params: {
          ...filters,
          sort_by: sort.column,
          sort_order: sort.direction
        },
        responseType: 'blob'
      })
      
      const blob = new Blob([response.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `logs-export-${new Date().toISOString()}.csv`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Error exporting logs:', err)
      setError('Failed to export logs. Please try again later.')
    }
  }

  function getSeverityBadge(severity: string): JSX.Element {
    const colors = {
      low: 'bg-blue-500/30 text-blue-300 border-blue-400/30',
      medium: 'bg-yellow-500/30 text-yellow-300 border-yellow-400/30',
      high: 'bg-orange-500/30 text-orange-300 border-orange-400/30',
      critical: 'bg-red-500/30 text-red-300 border-red-400/30'
    }
    return (
      <span className={`px-3 py-1 rounded-full text-xs border ${colors[severity as keyof typeof colors] || colors.low}`}>
        {severity.toLowerCase()}
      </span>
    )
  }

  const renderSortIcon = (column: string) => {
    if (sort.column !== column) {
      return null
    }
    return sort.direction === 'asc' ? <ChevronUp className="inline w-4 h-4" /> : <ChevronDown className="inline w-4 h-4" />
  }

  const columns = [
    { key: 'timestamp', label: 'Timestamp' },
    { key: 'severity', label: 'Severity' },
    { key: 'message', label: 'Message' },
    { key: 'vendor', label: 'Vendor' },
    { key: 'cnnid', label: 'CNNID' },
    { key: 'device_type', label: 'Device Type' }
  ]

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-cyan-200">
          Log Viewer
        </h1>
        <div className="flex gap-4">
          <button
            onClick={handleExport}
            className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 text-white rounded-md flex items-center gap-2 transition-colors"
          >
            <Download className="w-4 h-4" />
            Export Logs
          </button>
          <button
            className="text-gray-400 hover:text-gray-300 flex items-center"
            onClick={() => setShowFilters(!showFilters)}
          >
            <SlidersHorizontal className="h-4 w-4 mr-2" />
            Filters
          </button>
        </div>
      </div>

      {showFilters && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 rounded-lg border border-gray-800 bg-gray-900/50">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search logs..."
              className="w-full pl-8 pr-3 py-2 rounded-md bg-gray-800 border border-gray-700 text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-600"
              value={filters.query}
              onChange={(e) => handleFilterChange('query', e.target.value)}
            />
          </div>
          <select
            className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-600"
            value={filters.vendor}
            onChange={(e) => handleFilterChange('vendor', e.target.value)}
          >
            <option value="">All vendors</option>
            {vendors.map((vendor) => (
              <option key={vendor} value={vendor}>
                {vendor}
              </option>
            ))}
          </select>
          <select
            className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-600"
            value={filters.severity}
            onChange={(e) => handleFilterChange('severity', e.target.value)}
          >
            <option value="">All severities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
          <select
            className="w-full px-3 py-2 rounded-md bg-gray-800 border border-gray-700 text-gray-300 focus:outline-none focus:ring-2 focus:ring-cyan-600"
            value={filters.device_type}
            onChange={(e) => handleFilterChange('device_type', e.target.value)}
          >
            <option value="">All devices</option>
            <option value="firewall">Firewall</option>
            <option value="switch">Switch</option>
            <option value="router">Router</option>
            <option value="endpoint">Endpoint</option>
          </select>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <Loader2 className="w-8 h-8 animate-spin text-cyan-500" />
        </div>
      ) : error ? (
        <div className="text-center text-red-500 bg-red-900/20 border border-red-900 rounded-md p-4">
          {error}
        </div>
      ) : logs.length > 0 ? (
        <div className="overflow-x-auto rounded-lg border border-gray-800">
          <table className="min-w-full divide-y divide-gray-800">
            <thead className="bg-gray-900/50">
              <tr>
                {columns.map((column) => (
                  <th
                    key={column.key}
                    onClick={() => handleSort(column.key)}
                    className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider cursor-pointer hover:bg-gray-800/50 transition-colors"
                  >
                    <div className="flex items-center gap-1">
                      {column.label}
                      {renderSortIcon(column.key)}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800 bg-gray-900/30">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-800/50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    {getSeverityBadge(log.severity)}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-300">
                    {log.message}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {log.vendor}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {log.cnnid}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                    {log.device_type}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center text-gray-400 bg-gray-900/20 border border-gray-800 rounded-md p-4">
          No logs found.
        </div>
      )}
      <div className="flex justify-center gap-2 mt-4">
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
          className="px-4 py-2 text-sm font-medium rounded-md bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <div className="px-4 py-2 text-sm font-medium rounded-md bg-gray-800 text-gray-300">
          Page {currentPage} of {totalPages}
        </div>
        <button
          onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
          disabled={currentPage === totalPages}
          className="px-4 py-2 text-sm font-medium rounded-md bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default LogViewer

