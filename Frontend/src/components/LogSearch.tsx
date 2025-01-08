import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { DateRangeFilter } from './DateRangeFilter';
import { Login } from './Login';
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { HighlightedText } from './HighlightedText';

interface Log {
  id: number;
  timestamp: string;
  message: string;
  device_name: string;
  device_type: string;
  vendor_name: string;
  customer_cnnid: string;
}

interface LogSearchProps {
  onError: (message: string) => void;
}

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const LogSearch: React.FC<LogSearchProps> = ({ onError }) => {
  const [logs, setLogs] = useState<Log[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [startDate, setStartDate] = useState<Date | undefined>(undefined);
  const [endDate, setEndDate] = useState<Date | undefined>(undefined);
  const [sortBy, setSortBy] = useState('timestamp');
  const [sortOrder, setSortOrder] = useState('desc');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
      fetchLogs();
    }
  }, []);

  const fetchLogs = async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('token');
      if (!token) {
        setIsLoggedIn(false);
        onError('No authentication token found. Please log in.');
        return;
      }

      const params = new URLSearchParams({
        query: searchQuery,
        page: currentPage.toString(),
        page_size: '10',
        sort_by: sortBy,
        sort_order: sortOrder,
      });

      if (startDate) {
        params.append('start_time', startDate.toISOString());
      }
      if (endDate) {
        params.append('end_time', endDate.toISOString());
      }

      const response = await axios.get(`${API_URL}/api/v1/search?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setLogs(response.data.items);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error('Error fetching logs:', error);
      if (axios.isAxiosError(error) && error.response) {
        if (error.response.status === 401) {
          setIsLoggedIn(false);
          localStorage.removeItem('token');
          onError('Authentication failed. Please log in again.');
        } else {
          onError(`Failed to fetch logs: ${error.response.data.detail || 'Unknown error'}`);
        }
      } else {
        onError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      fetchLogs();
    }
  }, [currentPage, sortBy, sortOrder, isLoggedIn]);

  const handleSearch = () => {
    setCurrentPage(1);
    fetchLogs();
  };

  const handleDateFilter = () => {
    setCurrentPage(1);
    fetchLogs();
  };

  const handleSortChange = (value: string) => {
    setSortBy(value);
    setCurrentPage(1);
  };

  const handleSortOrderChange = () => {
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    setCurrentPage(1);
  };

  const handleLoginSuccess = (token: string) => {
    localStorage.setItem('token', token);
    setIsLoggedIn(true);
    fetchLogs();
  };

  if (!isLoggedIn) {
    return <Login onLoginSuccess={handleLoginSuccess} onError={onError} />;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold tracking-tight">Log Search</h2>
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <Input
            type="text"
            placeholder="Search logs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-grow"
          />
          <Button onClick={handleSearch} disabled={isLoading}>
            {isLoading ? 'Searching...' : 'Search'}
          </Button>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={sortBy} onValueChange={handleSortChange}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="timestamp">Timestamp</SelectItem>
              <SelectItem value="device_name">Device Name</SelectItem>
              <SelectItem value="vendor_name">Vendor Name</SelectItem>
              <SelectItem value="customer_cnnid">Customer CNNID</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={handleSortOrderChange} variant="outline">
            {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
          </Button>
        </div>
        <DateRangeFilter
          startDate={startDate}
          endDate={endDate}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
          onApplyFilter={handleDateFilter}
        />
      </div>
      <div className="mt-6 overflow-x-auto rounded-md border bg-card">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-muted/50">
              <th className="p-3 text-left text-sm font-medium">Timestamp</th>
              <th className="p-3 text-left text-sm font-medium">Message</th>
              <th className="p-3 text-left text-sm font-medium">Device</th>
              <th className="p-3 text-left text-sm font-medium">Vendor</th>
              <th className="p-3 text-left text-sm font-medium">Customer</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className="border-b">
                <td className="p-3 text-sm">{new Date(log.timestamp).toLocaleString()}</td>
                <td className="p-3 text-sm">
                  <HighlightedText text={log.message} highlight={searchQuery} />
                </td>
                <td className="p-3 text-sm">{`${log.device_name} (${log.device_type})`}</td>
                <td className="p-3 text-sm">{log.vendor_name}</td>
                <td className="p-3 text-sm">{log.customer_cnnid}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex items-center justify-between">
        <Button
          onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
          disabled={currentPage === 1 || isLoading}
          variant="outline"
        >
          Previous
        </Button>
        <span className="text-sm text-muted-foreground">
          Page {currentPage} of {totalPages}
        </span>
        <Button
          onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
          disabled={currentPage === totalPages || isLoading}
          variant="outline"
        >
          Next
        </Button>
      </div>
    </div>
  );
};

