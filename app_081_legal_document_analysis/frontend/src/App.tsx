import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:11081';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/metrics`);
      setMetrics(response.data);
    } catch (error) {
      console.error('Failed to load metrics:', error);
    }
  };

  const processData = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/v1/process`, {
        data: [1, 2, 3, 4, 5],
        options: {}
      });
      alert('Processing complete!');
    } catch (error) {
      console.error('Processing failed:', error);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>NLP App Application #81</h1>
      <button onClick={processData} disabled={loading}>
        {loading ? 'Processing...' : 'Process Data'}
      </button>
      {metrics && (
        <div style={{ marginTop: '20px', padding: '10px', background: '#f0f0f0' }}>
          <h3>Metrics</h3>
          <pre>{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
