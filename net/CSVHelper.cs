using System;
using System.Data;
using System.Data.SqlClient;
using CsvHelper;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

public class BulkInsertExample
{
    private readonly string connectionString = "YourConnectionStringHere";

    public async Task BulkInsertCsvAsync(string csvFilePath)
    {
        // Step 1: Read the CSV data into a DataTable
        DataTable dataTable = new DataTable();
        dataTable.Columns.Add("Column1", typeof(string));  // Define your columns based on the CSV structure
        dataTable.Columns.Add("Column2", typeof(int));
        // Add more columns as necessary

        using (var reader = new StreamReader(csvFilePath))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            var records = csv.GetRecords<dynamic>();  // or use a strongly-typed class instead of dynamic
            foreach (var record in records)
            {
                var row = dataTable.NewRow();
                row["Column1"] = record.Column1;  // Replace with actual column names from your CSV
                row["Column2"] = record.Column2;
                dataTable.Rows.Add(row);
            }
        }

        // Step 2: Open SQL connection and start a transaction
        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            await connection.OpenAsync();

            using (SqlTransaction transaction = connection.BeginTransaction())
            {
                try
                {
                    // Step 3: Lock the table to prevent partial reads
                    using (SqlCommand lockCommand = new SqlCommand("LOCK TABLE your_table WITH (TABLOCKX)", connection, transaction))
                    {
                        await lockCommand.ExecuteNonQueryAsync();  // Apply an exclusive table lock
                    }

                    // Step 4: Delete existing data
                    using (SqlCommand deleteCommand = new SqlCommand("DELETE FROM your_table", connection, transaction))
                    {
                        await deleteCommand.ExecuteNonQueryAsync();  // Clear the table
                    }

                    // Step 5: Perform bulk insert using SqlBulkCopy
                    using (SqlBulkCopy bulkCopy = new SqlBulkCopy(connection, SqlBulkCopyOptions.Default, transaction))
                    {
                        bulkCopy.DestinationTableName = "your_table";

                        // Optionally map columns if the DataTable column names don't match the database column names
                        bulkCopy.ColumnMappings.Add("Column1", "Column1");
                        bulkCopy.ColumnMappings.Add("Column2", "Column2");
                        // Add more mappings as necessary

                        await bulkCopy.WriteToServerAsync(dataTable);  // Perform the bulk insert
                    }

                    // Step 6: Commit transaction
                    await transaction.CommitAsync();
                }
                catch (Exception ex)
                {
                    // If something goes wrong, rollback the transaction
                    await transaction.RollbackAsync();
                    throw new Exception("Bulk insert failed", ex);
                }
            }
        }
    }
}