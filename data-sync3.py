CREATE TABLE YourTempTable (
    UniqueKeyColumn NVARCHAR(50),
    Column1 NVARCHAR(MAX),
    Column2 NVARCHAR(MAX),
    Column3 NVARCHAR(MAX),
    -- Add more columns as needed
);

using System;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using CsvHelper;
using System.Globalization;

class Program
{
    static string connectionString = "your_connection_string_here";

    static void Main(string[] args)
    {
        string csvFilePath = @"C:\path\to\your.csv";
        DataTable dataTable = ReadCsvIntoDataTable(csvFilePath);
        
        using (var conn = new SqlConnection(connectionString))
        {
            conn.Open();

            // Bulk insert into the temporary table
            BulkInsert(conn, dataTable);

            // Merge data into the main table
            MergeData(conn);

            conn.Close();
        }
    }

    static DataTable ReadCsvIntoDataTable(string csvFilePath)
    {
        var dataTable = new DataTable();
        using (var reader = new StreamReader(csvFilePath))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            using (var dr = new CsvDataReader(csv))
            {
                dataTable.Load(dr);
            }
        }
        return dataTable;
    }

    static void BulkInsert(SqlConnection conn, DataTable dataTable)
    {
        using (var bulkCopy = new SqlBulkCopy(conn))
        {
            bulkCopy.DestinationTableName = "YourTempTable";
            bulkCopy.WriteToServer(dataTable);
        }
    }

    static void MergeData(SqlConnection conn)
    {
        var sql = @"
            MERGE INTO YourMainTable AS target
            USING YourTempTable AS source
            ON target.UniqueKeyColumn = source.UniqueKeyColumn
            WHEN MATCHED THEN
                UPDATE SET 
                    Column1 = source.Column1,
                    Column2 = source.Column2,
                    Column3 = source.Column3
            WHEN NOT MATCHED THEN
                INSERT (UniqueKeyColumn, Column1, Column2, Column3)
                VALUES (source.UniqueKeyColumn, source.Column1, source.Column2, source.Column3);";

        using (var command = new SqlCommand(sql, conn))
        {
            command.ExecuteNonQuery();
        }

        // Optionally, truncate the temporary table after the merge
        using (var command = new SqlCommand("TRUNCATE TABLE YourTempTable;", conn))
        {
            command.ExecuteNonQuery();
        }
    }
}