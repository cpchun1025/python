Sub LoadDataAndPerformVLookup()
    ' Declare variables
    Dim masterWorkbook As Workbook
    Dim referenceWorkbook As Workbook
    Dim wsMaster As Worksheet
    Dim wsReference As Worksheet
    Dim wsPivotData As Worksheet
    Dim pivotTable As PivotTable
    Dim lastRowMaster As Long
    Dim lastRowReference As Long
    Dim lookupRange As Range
    Dim cell As Range
    Dim lookupCol As Long
    Dim resultCol As Long
    Dim filePathMaster As String
    Dim filePathReference As String
    Dim vlookupValue As Variant
    
    ' Prompt the user to select the master data file
    filePathMaster = Application.GetOpenFilename(FileFilter:="Excel Files (*.xls; *.xlsx; *.xlsm), *.xls; *.xlsx; *.xlsm", Title:="Select Master Data File")
    
    ' Exit if no file is selected
    If filePathMaster = "False" Then
        MsgBox "No file selected.", vbExclamation
        Exit Sub
    End If
    
    ' Open the selected master data file
    Set masterWorkbook = Workbooks.Open(filePathMaster)
    Set wsMaster = masterWorkbook.Sheets(1) ' Assuming data is in the first sheet
    
    ' Find the last row in the master data sheet
    lastRowMaster = wsMaster.Cells(wsMaster.Rows.Count, 1).End(xlUp).Row
    
    ' Prompt the user to select the reference data file (for VLOOKUP)
    filePathReference = Application.GetOpenFilename(FileFilter:="Excel Files (*.xls; *.xlsx; *.xlsm), *.xls; *.xlsx; *.xlsm", Title:="Select Reference Data File")
    
    ' Exit if no file is selected
    If filePathReference = "False" Then
        MsgBox "No file selected.", vbExclamation
        Exit Sub
    End If
    
    ' Open the selected reference data file
    Set referenceWorkbook = Workbooks.Open(filePathReference)
    Set wsReference = referenceWorkbook.Sheets(1) ' Assuming data is in the first sheet
    
    ' Find the last row in the reference data sheet
    lastRowReference = wsReference.Cells(wsReference.Rows.Count, 1).End(xlUp).Row
    
    ' Define the lookup range (adjust columns as needed)
    Set lookupRange = wsReference.Range("A2:B" & lastRowReference) ' Assuming lookup in column A, result in column B
    
    ' Column in the Master Data to apply VLOOKUP (Adjust as needed)
    lookupCol = 1 ' Assuming we're looking up values from column A in the master data
    
    ' Column where the VLOOKUP result will be placed (Adjust as needed)
    resultCol = 3 ' Assuming we put the result in column C of the master data
    
    ' Loop through the master data and perform VLOOKUP
    For Each cell In wsMaster.Range(wsMaster.Cells(2, lookupCol), wsMaster.Cells(lastRowMaster, lookupCol))
        ' Perform VLOOKUP
        On Error Resume Next
        vlookupValue = Application.WorksheetFunction.VLookup(cell.Value, lookupRange, 2, False)
        On Error GoTo 0
        
        ' If VLOOKUP returns an error, return "Not Found", else return the result
        If IsError(vlookupValue) Then
            wsMaster.Cells(cell.Row, resultCol).Value = "Not Found"
        Else
            wsMaster.Cells(cell.Row, resultCol).Value = vlookupValue
        End If
    Next cell
    
    ' Close the reference workbook (no need to save)
    referenceWorkbook.Close SaveChanges:=False
    
    ' Copy the enriched data to the pivot data sheet in this workbook
    Set wsPivotData = ThisWorkbook.Sheets("PivotData") ' Change to the actual name of the sheet where you'd like the data
    
    ' Clear the existing data in the pivot data sheet
    wsPivotData.Cells.Clear
    
    ' Copy the master data (with VLOOKUP results) to the pivot data sheet
    wsMaster.Range("A1:C" & lastRowMaster).Copy Destination:=wsPivotData.Range("A1")
    
    ' Close the master data workbook (no need to save)
    masterWorkbook.Close SaveChanges:=False
    
    ' Refresh the Pivot Table (assuming it is on another sheet)
    Set pivotTable = ThisWorkbook.Sheets("Pivot").PivotTables("PivotTable1") ' Adjust the name of Pivot Table
    
    ' Refresh the Pivot Table
    pivotTable.RefreshTable
    
    MsgBox "Data processing completed and Pivot Table refreshed successfully!", vbInformation
End Sub