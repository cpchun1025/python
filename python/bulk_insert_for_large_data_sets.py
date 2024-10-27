import pandas as pd
import pyodbc

def bulk_insert_to_staging(df_chunk, staging_table_name):
    """
    Bulk insert the data frame chunk into a staging table.
    """
    cursor = conn.cursor()

    # Convert the DataFrame to a list of tuples
    data = [tuple(x) for x in df_chunk.to_numpy()]

    # Create a SQL query for bulk insert
    placeholders = ', '.join(['?'] * len(df_chunk.columns))
    query = f"INSERT INTO {staging_table_name} VALUES ({placeholders})"

    # Execute the bulk insert for the entire chunk
    cursor.executemany(query, data)

    conn.commit()

def merge_staging_to_main_table(staging_table_name, main_table_name):
    """
    Merge the staging table data into the main table with an UPSERT operation.
    """
    cursor = conn.cursor()

    # Perform the MERGE operation
    query = f"""
    MERGE INTO {main_table_name} AS target
    USING {staging_table_name} AS source
    ON target.ID = source.ID  -- Assuming 'ID' is a unique key
    WHEN MATCHED THEN 
        UPDATE SET target.Column1 = source.Column1, target.Column2 = source.Column2
    WHEN NOT MATCHED BY TARGET THEN 
        INSERT (ID, Column1, Column2) VALUES (source.ID, source.Column1, source.Column2);
    """

    cursor.execute(query)
    conn.commit()

# Example usage
csv_file_path = 'path_to_large_csv_file.csv'
staging_table_name = 'staging_table'
main_table_name = 'main_table'

# Step 1: Process CSV in chunks and bulk insert into staging table
chunk_iter = pd.read_csv(csv_file_path, chunksize=5000)
for chunk in chunk_iter:
    bulk_insert_to_staging(chunk, staging_table_name)

# Step 2: Merge staging table into main table
merge_staging_to_main_table(staging_table_name, main_table_name)