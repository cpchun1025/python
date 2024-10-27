from sqlalchemy import create_engine
import pandas as pd

# Create SQLAlchemy engine
engine = create_engine('mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server')

def bulk_insert_sqlalchemy(df_chunk, table_name):
    """
    Bulk insert the DataFrame chunk using SQLAlchemy's `to_sql` method.
    """
    df_chunk.to_sql(table_name, engine, if_exists='append', index=False, chunksize=5000)

# Example usage
csv_file_path = 'path_to_large_csv_file.csv'
chunk_iter = pd.read_csv(csv_file_path, chunksize=5000)

for chunk in chunk_iter:
    bulk_insert_sqlalchemy(chunk, 'staging_table')

# CREATE INDEX idx_main_table_id ON main_table (ID);