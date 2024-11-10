{
  "timestamp": "2024-11-10T12:30:00.000Z",
  "data": [...]
}

{
  "timestamp": "2024-11-10T12:30:00.000Z"
}

import React, { useState, useEffect, useRef } from 'react';
import { DataGrid } from 'devextreme-react/data-grid'; // Assuming you're using DevExtreme

const AutoRefreshGrid = () => {
  const [data, setData] = useState([]);
  const [lastTimestamp, setLastTimestamp] = useState<string | null>(null); // Tracks last timestamp
  const [isEditing, setIsEditing] = useState(false);
  const autoRefreshInterval = useRef<NodeJS.Timer | null>(null);

  // Fetch full data set and update grid
  const fetchData = async () => {
    const response = await fetch('/api/data');
    const result = await response.json();
    setData(result.data);
    setLastTimestamp(result.timestamp); // Save the latest timestamp
  };

  // Fetch the latest timestamp only
  const fetchLatestTimestamp = async () => {
    const response = await fetch('/api/data-timestamp');
    const result = await response.json();
    return result.timestamp;
  };

  // Function to start auto-refresh
  const startAutoRefresh = () => {
    autoRefreshInterval.current = setInterval(async () => {
      if (!isEditing) {
        const latestTimestamp = await fetchLatestTimestamp();
        if (latestTimestamp !== lastTimestamp) {
          // Only fetch and refresh grid if data has changed
          fetchData();
        }
      }
    }, 30000); // 30 seconds
  };

  // Function to stop auto-refresh
  const stopAutoRefresh = () => {
    if (autoRefreshInterval.current) {
      clearInterval(autoRefreshInterval.current);
    }
  };

  // Effect to start and stop auto-refresh
  useEffect(() => {
    fetchData();
    startAutoRefresh();

    return () => {
      stopAutoRefresh(); // Cleanup on unmount
    };
  }, []);

  // Event handler for starting and stopping edit mode
  const handleEditStart = () => {
    setIsEditing(true);
    stopAutoRefresh(); // Stop auto-refresh when editing starts
  };

  const handleEditEnd = () => {
    setIsEditing(false);
    startAutoRefresh(); // Restart auto-refresh after editing ends
  };

  return (
    <DataGrid
      dataSource={data}
      onEditingStart={handleEditStart}
      onEditingEnd={handleEditEnd}
      // Other grid options...
    />
  );
};

export default AutoRefreshGrid;

<button onClick={fetchData}>Refresh Now</button>

import React, { useState, useEffect, useRef } from 'react';
import { DataGrid } from 'devextreme-react/data-grid'; // Assuming you're using DevExtreme

const AutoRefreshGrid = () => {
  const [data, setData] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [hasNewData, setHasNewData] = useState(false);
  const autoRefreshInterval = useRef<NodeJS.Timer | null>(null);

  // Fetch data from the API
  const fetchData = async () => {
    const response = await fetch('/your-api-endpoint'); // Replace with your API call
    const result = await response.json();
    if (isEditing) {
      setHasNewData(true); // Notify that new data is available
    } else {
      setData(result);
    }
  };

  // Function to start auto-refresh
  const startAutoRefresh = () => {
    autoRefreshInterval.current = setInterval(() => {
      fetchData();
    }, 30000); // 30 seconds
  };

  // Function to stop auto-refresh
  const stopAutoRefresh = () => {
    if (autoRefreshInterval.current) {
      clearInterval(autoRefreshInterval.current);
    }
  };

  // Refresh the data manually on user request
  const refreshDataManually = () => {
    fetchData();
    setHasNewData(false); // Reset the notification
  };

  // Effect to start and stop auto-refresh
  useEffect(() => {
    fetchData();
    startAutoRefresh();

    return () => {
      stopAutoRefresh(); // Cleanup on unmount
    };
  }, []);

  // Event handler for starting and stopping edit mode
  const handleEditStart = () => {
    setIsEditing(true);
    stopAutoRefresh(); // Stop auto-refresh when editing starts
  };

  const handleEditEnd = () => {
    setIsEditing(false);
    startAutoRefresh(); // Restart auto-refresh after editing ends
  };

  return (
    <div>
      {/* Show notification when new data is available */}
      {hasNewData && (
        <div className="new-data-notification">
          New data available. <button onClick={refreshDataManually}>Refresh Now</button>
        </div>
      )}

      <DataGrid
        dataSource={data}
        onEditingStart={handleEditStart}
        onEditingEnd={handleEditEnd}
        // Other grid options...
      />
    </div>
  );
};

export default AutoRefreshGrid;

import React, { useState, useEffect, useRef } from 'react';
import { DataGrid } from 'devextreme-react/data-grid'; // Assuming you're using DevExtreme

const AutoRefreshGrid = () => {
  const [data, setData] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const autoRefreshInterval = useRef<NodeJS.Timer | null>(null);

  // Fetch data from the API
  const fetchData = async () => {
    const response = await fetch('/your-api-endpoint'); // Replace with your API call
    const result = await response.json();
    setData(result);
  };

  // Function to start auto-refresh
  const startAutoRefresh = () => {
    autoRefreshInterval.current = setInterval(() => {
      if (!isEditing) {
        fetchData();
      }
    }, 30000); // 30 seconds
  };

  // Function to stop auto-refresh
  const stopAutoRefresh = () => {
    if (autoRefreshInterval.current) {
      clearInterval(autoRefreshInterval.current);
    }
  };

  // Effect to start and stop auto-refresh
  useEffect(() => {
    fetchData();
    startAutoRefresh();

    return () => {
      stopAutoRefresh(); // Cleanup on unmount
    };
  }, []);

  // Event handler for starting and stopping edit mode
  const handleEditStart = () => {
    setIsEditing(true);
    stopAutoRefresh(); // Stop auto-refresh when editing starts
  };

  const handleEditEnd = () => {
    setIsEditing(false);
    startAutoRefresh(); // Restart auto-refresh after editing ends
  };

  return (
    <DataGrid
      dataSource={data}
      onEditingStart={handleEditStart}
      onEditingEnd={handleEditEnd}
      // Other grid options...
    />
  );
};

export default AutoRefreshGrid;