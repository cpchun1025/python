Sub LoadDataAndRefreshPivot()
    Dim wsData As Worksheet
    Dim wsPivot As Worksheet
    Dim pivotTable As PivotTable
    Dim dataWorkbook As Workbook
    Dim filePath As String
    Dim lastRow As Long
    Dim lastCol As Long
    Dim dataRange As Range
    Dim pivotCache As PivotCache
    Dim dynamicPath As String
    Dim fileName As String
    
    ' Define the name of the CSV or Excel file
    fileName = "target.csv" ' Change this to the name of the file you're looking for
    
    ' Dynamically construct the folder path with today's date in yyyyMMdd format
    dynamicPath = "C:\data\" & Format(Date, "yyyyMMdd") & "\"
    
    ' Combine the path and the filename
    filePath = dynamicPath & fileName
    
    ' Check if the file exists
    If Dir(filePath) = "" Then
        MsgBox "The file " & fileName & " does not exist in the folder: " & dynamicPath, vbExclamation
        Exit Sub
    End If
    
    ' Open the selected file
    Set dataWorkbook = Workbooks.Open(filePath)
    
    ' Assuming the data is in the first sheet of the opened workbook
    Set wsData = dataWorkbook.Sheets(1)
    
    ' Find the last row and column with data in the loaded worksheet
    lastRow = wsData.Cells(wsData.Rows.Count, 1).End(xlUp).Row
    lastCol = wsData.Cells(1, wsData.Columns.Count).End(xlToLeft).Column
    
    ' Define the range of data
    Set dataRange = wsData.Range(wsData.Cells(1, 1), wsData.Cells(lastRow, lastCol))
    
    ' Copy the data to the main workbook (where the Pivot Table is)
    ThisWorkbook.Sheets("Data").Cells.Clear
    dataRange.Copy Destination:=ThisWorkbook.Sheets("Data").Range("A1")
    
    ' Close the opened data workbook
    dataWorkbook.Close SaveChanges:=False
    
    ' Set the Pivot Table worksheet and the Pivot Table object (adjust these names as needed)
    Set wsPivot = ThisWorkbook.Sheets("Pivot")
    Set pivotTable = wsPivot.PivotTables("PivotTable1") ' Change "PivotTable1" to the actual name of your Pivot Table
    
    ' Update the Pivot Table data source
    Set pivotCache = ThisWorkbook.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=ThisWorkbook.Sheets("Data").Range("A1").CurrentRegion)
    
    ' Set the new pivot cache to the existing pivot table
    pivotTable.ChangePivotCache pivotCache
    
    ' Refresh the Pivot Table
    pivotTable.RefreshTable
    
    MsgBox "Pivot Table updated successfully!", vbInformation
End Sub