const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  VENDOR_COUNTS: `${API_BASE_URL}/api/v1/logs/vendor-counts`,
  SEVERITY_DISTRIBUTION: `${API_BASE_URL}/api/v1/logs/severity-distribution`,
  LOGS: `${API_BASE_URL}/api/v1/logs`,
};

