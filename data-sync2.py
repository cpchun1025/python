using System;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.IO.Compression;
using CsvHelper;
using System.Globalization;
using Dapper;

class Program
{
    static string zipFolder = @"C:\path\to\zip_folder";
    static string extractedFolder = @"C:\path\to\extracted_folder";
    static string connectionString = "your_connection_string_here";

    static void Main(string[] args)
    {
        while (true)
        {
            foreach (var file in Directory.GetFiles(zipFolder, "*.zip"))
            {
                ProcessZipFile(file);
                File.Delete(file); // Remove the zip file after processing
            }
            System.Threading.Thread.Sleep(60000); // Wait for 1 minute before checking again
        }
    }

    static void ProcessZipFile(string zipFilePath)
    {
        ZipFile.ExtractToDirectory(zipFilePath, extractedFolder);

        foreach (var file in Directory.GetFiles(extractedFolder, "*.csv"))
        {
            ProcessCsvFile(file);
            File.Delete(file); // Clean up extracted files
        }
    }

    static void ProcessCsvFile(string csvFilePath)
    {
        using (var reader = new StreamReader(csvFilePath))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            var conn = new SqlConnection(connectionString);
            conn.Open();

            // Process CSV in chunks
            while (csv.Read())
            {
                var record = csv.GetRecord<YourDataModel>();
                UpsertRecord(conn, record);
            }

            conn.Close();
        }
    }

    static void UpsertRecord(SqlConnection conn, YourDataModel record)
    {
        var sql = @"
            MERGE INTO YourTable AS target
            USING (VALUES (@Column1, @Column2, @Column3)) AS source (Column1, Column2, Column3)
            ON target.UniqueKeyColumn = source.Column1
            WHEN MATCHED THEN
                UPDATE SET target.Column2 = source.Column2, target.Column3 = source.Column3
            WHEN NOT MATCHED THEN
                INSERT (Column1, Column2, Column3)
                VALUES (source.Column1, source.Column2, source.Column3);";

        conn.Execute(sql, record);
    }
}

public class YourDataModel
{
    public string Column1 { get; set; }
    public string Column2 { get; set; }
    public string Column3 { get; set; }
}