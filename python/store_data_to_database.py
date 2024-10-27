import pyodbc
import pandas as pd

# Connect to SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=your_server;'
                      'DATABASE=your_db;'
                      'UID=your_username;'
                      'PWD=your_password')

def store_csv_to_db(csv_file, table_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # You can loop through the DataFrame and perform an upsert operation
    cursor = conn.cursor()

    for index, row in df.iterrows():
        # Example using MERGE SQL statement for upsert
        query = f"""
        MERGE INTO {table_name} AS target
        USING (SELECT ? AS col1, ? AS col2, ? AS col3) AS source (col1, col2, col3)
        ON target.col1 = source.col1
        WHEN MATCHED THEN
            UPDATE SET target.col2 = source.col2, target.col3 = source.col3
        WHEN NOT MATCHED THEN
            INSERT (col1, col2, col3) VALUES (source.col1, source.col2, source.col3);
        """
        cursor.execute(query, row['col1'], row['col2'], row['col3'])

    conn.commit()

# Example call
store_csv_to_db('path_to_csv_file.csv', 'your_table_name')