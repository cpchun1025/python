using System;
using System.Collections.Generic;
using System.Dynamic;
using System.IO;
using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;

public class Program
{
    public static void Main()
    {
        using (var reader = new StreamReader("path/to/your/file.csv"))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            var records = new List<dynamic>();
            csv.Read();
            csv.ReadHeader();
            
            while (csv.Read())
            {
                var expandoObject = new ExpandoObject() as IDictionary<string, object>;

                foreach (var header in csv.HeaderRecord)
                {
                    expandoObject[header] = csv.GetField(header);
                }

                records.Add(expandoObject);
            }

            // Now you have records in a dynamic form, you can bulk insert into the database
            BulkInsertIntoDatabase(records);
        }
    }

    public static void BulkInsertIntoDatabase(List<dynamic> records)
    {
        // Implement your bulk insert logic here.
        // You could use Dapper or Entity Framework to map the dynamic objects to the table.
    }
}

using System;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using CsvHelper;
using System.Globalization;

public class Program
{
    public static void Main()
    {
        using (var reader = new StreamReader("path/to/your/file.csv"))
        using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
        {
            using (DataTable dt = new DataTable())
            {
                // Read the CSV header
                csv.Read();
                csv.ReadHeader();
                
                foreach (var header in csv.HeaderRecord)
                {
                    dt.Columns.Add(header);
                }

                // Read the CSV rows
                while (csv.Read())
                {
                    var row = dt.NewRow();
                    foreach (var header in csv.HeaderRecord)
                    {
                        row[header] = csv.GetField(header);
                    }
                    dt.Rows.Add(row);
                }

                // Bulk insert into the database
                BulkInsert(dt);
            }
        }
    }

    public static void BulkInsert(DataTable dataTable)
    {
        string connectionString = "your-database-connection-string";

        using (SqlConnection connection = new SqlConnection(connectionString))
        {
            connection.Open();
            using (SqlBulkCopy bulkCopy = new SqlBulkCopy(connection))
            {
                bulkCopy.DestinationTableName = "YourDestinationTable";
                try
                {
                    // Map the CSV columns with the database columns as needed
                    // bulkCopy.ColumnMappings.Add("CSVColumn", "DatabaseColumn");

                    bulkCopy.WriteToServer(dataTable);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}

using System;
using System.IO;

public class Program
{
    public static void Main()
    {
        using (var reader = new StreamReader("path/to/your/file.csv"))
        {
            string headerLine = reader.ReadLine();
            string[] headers = headerLine.Split(',');

            Console.WriteLine("public class CsvRecord {");

            foreach (var header in headers)
            {
                Console.WriteLine($"    public string {header} {{ get; set; }}");
            }

            Console.WriteLine("}");
        }
    }
}