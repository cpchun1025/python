using System;
using System.Data.SqlClient;
using System.IO;
using System.Threading.Tasks;

public class CsvLoader
{
    private readonly string connectionString = "YourConnectionStringHere";

    public async Task LoadCsvIfNewAsync(string csvFilePath)
    {
        // Step 1: Get the CSV file's creation date
        DateTime fileCreationDate = File.GetCreationTime(csvFilePath);

        // Step 2: Get the last processed date from the database
        DateTime? dbFileDate = await GetLastProcessedFileDateAsync();

        // Step 3: Compare dates and decide whether to load the file or skip
        if (dbFileDate.HasValue && fileCreationDate <= dbFileDate.Value)
        {
            Console.WriteLine("File is older or same as the last processed file. Skipping.");
            return;  // Skip the loading process since the file is not newer
        }

        // Step 4: Load the file (bulk insert logic goes here)
        Console.WriteLine("Newer file detected. Proceeding with bulk insert...");
        await BulkInsertCsvAsync(csvFilePath);

        // Step 5: Optionally, update the last processed file date in the database
        await UpdateLastProcessedFileDateAsync(fileCreationDate);
    }

    private async Task<DateTime?> GetLastProcessedFileDateAsync()
    {
        // Step 2a: Retrieve the last processed file date from the database
        string query = "SELECT MAX(LastProcessedFileDate) FROM FileProcessingLog";  // Change table/column as per your schema

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            await connection.OpenAsync();
            using (SqlCommand command = new SqlCommand(query, connection))
            {
                object result = await command.ExecuteScalarAsync();
                if (result != DBNull.Value && result != null)
                {
                    return (DateTime)result;
                }
                else
                {
                    return null;  // No previous file date found
                }
            }
        }
    }

    private async Task UpdateLastProcessedFileDateAsync(DateTime fileDate)
    {
        // Step 5: Update the last processed file date in the database
        string query = "UPDATE FileProcessingLog SET LastProcessedFileDate = @FileDate";  // Change table/column as per your schema

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            await connection.OpenAsync();
            using (SqlCommand command = new SqlCommand(query, connection))
            {
                command.Parameters.AddWithValue("@FileDate", fileDate);

                await command.ExecuteNonQueryAsync();
            }
        }
    }

    private async Task BulkInsertCsvAsync(string csvFilePath)
    {
        // Your bulk insert logic (using SqlBulkCopy or other method) goes here
        Console.WriteLine($"Bulk inserting data from {csvFilePath}...");
        
        // Example: Call your bulk insert method here from earlier
        // await YourBulkInsertMethod(csvFilePath);
    }
}