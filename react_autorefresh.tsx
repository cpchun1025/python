import React, { useEffect, useCallback, useRef } from 'react';

export const ChinaFXList = () => {
  const gridRef = useRef(null); // Assuming you have a ref to the data grid

  // Callback to refresh the grid
  const refresh = useCallback(() => {
    if (gridRef.current) {
      gridRef.current.instance.refresh(); // Assuming 'instance.refresh()' refreshes the data grid
    }
  }, []);

  // Auto-refresh every 30 seconds (or any interval you prefer)
  useEffect(() => {
    const intervalId = setInterval(() => {
      refresh(); // Call the refresh function every 30 seconds
    }, 30000); // 30 seconds interval (30000 milliseconds)

    // Cleanup function to clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, [refresh]);

  return (
    <div className="view china-fx-list">
      <div className="view-wrapper view-wrapper-fx-list list-page">
        <DataGrid
          className="grid theme-dependent"
          noDataText="No data"
          keyExpr="id"
          focusedRowEnabled
          height="auto"
          dataSource={gridDataSource}
          onRowClick={onRowClick}
          onExporting={onExporting}
          allowColumnReordering
          showBorders
          ref={gridRef} // Attach the ref to the DataGrid
        >
          {/* Other components and configurations */}
        </DataGrid>
      </div>
    </div>
  );
};

