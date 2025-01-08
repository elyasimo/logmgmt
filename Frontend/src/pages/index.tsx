import React, { useState } from 'react';
import { LogSearch } from '../components/LogSearch';

const Home: React.FC = () => {
  const [error, setError] = useState<string | null>(null);

  const handleApiError = (message: string) => {
    setError(message);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto py-8">
        {error && (
          <div className="error-message bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <strong className="font-bold">Error:</strong>
            <span className="block sm:inline"> {error}</span>
          </div>
        )}
        <LogSearch onError={handleApiError} />
      </main>
    </div>
  );
};

export default Home;

