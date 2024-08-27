import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine, text

# Database Configuration
db_config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': '5432',
    'database': 'your_database'
}

# Directory Configuration
zip_folder = "/path/to/zip_folder"
extracted_folder = "/path/to/extracted_folder"

# SQLAlchemy Engine
engine = create_engine(f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

def process_zip_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    
    for root, _, files in os.walk(extracted_folder):
        for file in files:
            if file.endswith('.csv'):
                process_csv_file(os.path.join(root, file))

def process_csv_file(csv_file):
    # Read CSV in chunks to manage memory usage
    chunksize = 10000
    for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        # Perform upsert operation for each chunk
        upsert_to_db(chunk)

def upsert_to_db(df_chunk):
    with engine.connect() as conn:
        for index, row in df_chunk.iterrows():
            # Customize SQL as per your table structure
            sql = text("""
                INSERT INTO your_table (column1, column2, column3)
                VALUES (:column1, :column2, :column3)
                ON CONFLICT (unique_key_column)
                DO UPDATE SET
                    column1 = EXCLUDED.column1,
                    column2 = EXCLUDED.column2,
                    column3 = EXCLUDED.column3;
            """)
            conn.execute(sql, **row.to_dict())

def main():
    while True:
        # Monitor the folder for new zip files
        for file in os.listdir(zip_folder):
            if file.endswith('.zip'):
                zip_file_path = os.path.join(zip_folder, file)
                process_zip_file(zip_file_path)
                os.remove(zip_file_path)  # Remove the zip file after processing

if __name__ == "__main__":
    main()