const [childData, setChildData] = useState({}); // Store child data for each parent row
const [expandedRowId, setExpandedRowId] = useState(null); // Track the expanded row

// Handle row click
const onRowClick = async (e) => {
  const parentId = e.data.id; // Get the parent row's ID

  // If the row is already expanded, collapse it
  if (expandedRowId === parentId) {
    setExpandedRowId(null);
    return;
  }

  // Fetch child data from the backend
  try {
    const response = await fetch(`/api/child-data/${parentId}`); // Assuming your API endpoint
    const data = await response.json();
    
    // Store the child data for this specific parent row
    setChildData((prev) => ({ ...prev, [parentId]: data }));
    setExpandedRowId(parentId); // Set the expanded row ID
  } catch (error) {
    console.error('Error fetching child data:', error);
  }
};

<DataGrid
  className='grid theme-dependent'
  noDataText=''
  focusedRowEnabled
  height='100%'
  dataSource={gridDataSource}
  onRowClick={onRowClick}
  onExporting={onExporting}
  allowColumnReordering
  showBorders
  ref={gridRef}
>
  {/* Other columns and features */}

  {/* MasterDetail for Child Grid */}
  <MasterDetail
    enabled={true}
    render={(detailData) => {
      const parentId = detailData.data.id; // Parent row ID
      const childRows = childData[parentId]; // Get child data for this parent

      if (!childRows) {
        return <div>Loading child data...</div>; // Loading state while the child data is being fetched
      }

      return (
        <DataGrid
          dataSource={childRows} // Populate child grid with fetched child data
          showBorders
          height="100%"
        >
          <Column dataField="childField1" caption="Child Field 1" />
          <Column dataField="childField2" caption="Child Field 2" />
          <Column dataField="childField3" caption="Child Field 3" />
        </DataGrid>
      );
    }}
  />
</DataGrid>

[HttpGet("child-data/{parentId}")]
public IActionResult GetChildData(int parentId)
{
    // Fetch child data from the database based on the parentId
    var childData = _dbContext.ChildEntities
                    .Where(c => c.ParentId == parentId)
                    .ToList();

    return Ok(childData);
}

import React, { useState, useCallback, useEffect, useRef } from 'react';
import DataGrid, { Column, MasterDetail, LoadPanel, SearchPanel, Toolbar, Item, Export, Selection, HeaderFilter, Sorting, Scrolling } from 'devextreme-react/data-grid';
import { Button } from 'devextreme-react/button';
import ContactPanel from './ContactPanel';
import FormPopup from './FormPopup';
import ContactNewForm from './ContactNewForm';

const ChinaFXList = () => {
  const gridRef = useRef(null);
  const [gridDataSource, setGridDataSource] = useState([]);
  const [childData, setChildData] = useState({});
  const [expandedRowId, setExpandedRowId] = useState(null); // Track the expanded row
  const [popupVisible, setPopupVisible] = useState(false);
  const [formDataDefaults, setFormDataDefaults] = useState({});
  const [contactId, setContactId] = useState(null);
  const [isPanelOpened, setIsPanelOpened] = useState(false);

  // Handle row click
  const onRowClick = async (e) => {
    const parentId = e.data.id; // Get the parent row's ID

    // If the row is already expanded, collapse it
    if (expandedRowId === parentId) {
      setExpandedRowId(null);
      return;
    }

    // Fetch child data from the backend
    try {
      const response = await fetch(`/api/child-data/${parentId}`); // Assuming your API endpoint
      const data = await response.json();
      
      // Store the child data for this specific parent row
      setChildData((prev) => ({ ...prev, [parentId]: data }));
      setExpandedRowId(parentId); // Set the expanded row ID
    } catch (error) {
      console.error('Error fetching child data:', error);
    }
  };

  // Refresh method
  const refresh = useCallback(() => {
    gridRef.current?.instance.refresh();
  }, []);

  return (
    <div className='view crm-contact-list'>
      <div className='view-wrapper view-wrapper-contact-list list-page'>
        <DataGrid
          className='grid theme-dependent'
          noDataText=''
          focusedRowEnabled
          height='100%'
          dataSource={gridDataSource}
          onRowClick={onRowClick}
          allowColumnReordering
          showBorders
          ref={gridRef}
        >
          <LoadPanel showPane={false} />
          <SearchPanel visible placeholder='Contact Search' />
          <ColumnChooser enabled />
          <Export enabled allowExportSelectedData formats={['xlsx', 'pdf']} />
          <Selection
            selectAllMode='allPages'
            showCheckBoxesMode='always'
            mode='multiple'
          />
          <HeaderFilter visible />
          <Sorting mode='multiple' />
          <Scrolling mode='virtual' />
          <Toolbar>
            <Item location='before'>
              <div className='grid-header'>Contacts</div>
            </Item>
            <Item location='after'>
              <Button icon='plus' text='Add Contact' onClick={() => setPopupVisible(true)} />
            </Item>
            <Item location='after'>
              <Button icon='refresh' text='Refresh' onClick={refresh} />
            </Item>
            <Item name='exportButton' />
          </Toolbar>

          {/* Define your columns */}
          <Column dataField='name' caption='Name' />
          <Column dataField='company' caption='Company' />
          <Column dataField='status' caption='Status' />
          <Column dataField='phone' caption='Phone' />
          <Column dataField='email' caption='Email' />

          {/* MasterDetail for Child Grid */}
          <MasterDetail
            enabled={true}
            render={(detailData) => {
              const parentId = detailData.data.id; // Parent row ID
              const childRows = childData[parentId]; // Get child data for this parent

              if (!childRows) {
                return <div>Loading child data...</div>; // Loading state while the child data is being fetched
              }

              return (
                <DataGrid
                  dataSource={childRows} // Populate child grid with fetched child data
                  showBorders
                  height="100%"
                >
                  <Column dataField="childField1" caption="Child Field 1" />
                  <Column dataField="childField2" caption="Child Field 2" />
                  <Column dataField="childField3" caption="Child Field 3" />
                </DataGrid>
              );
            }}
          />
        </DataGrid>

        {/* Additional components */}
        <ContactPanel contactId={contactId} isOpened={isPanelOpened} />
        <FormPopup title='New Contact' visible={popupVisible} setVisible={setPopupVisible}>
          <ContactNewForm initData={formDataDefaults} />
        </FormPopup>
      </div>
    </div>
  );
};

export default ChinaFXList;