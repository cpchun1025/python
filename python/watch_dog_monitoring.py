import os
import zipfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ZipHandler(FileSystemEventHandler):
    def __init__(self, folder_to_watch):
        self.folder_to_watch = folder_to_watch

    def on_created(self, event):
        # Process only zip files
        if event.src_path.endswith('.zip'):
            self.process_zip(event.src_path)

    def process_zip(self, zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.folder_to_watch)

        # Now proceed to process CSV files
        self.process_csv_files(self.folder_to_watch)

    def process_csv_files(self, folder):
        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        for csv_file in csv_files:
            # Process each CSV file
            self.store_to_database(os.path.join(folder, csv_file))

    def store_to_database(self, csv_file_path):
        # Implement the logic to read the CSV and store in SQL Server
        print(f"Storing {csv_file_path} to database")

# Setup folder observer
folder_to_watch = '/path/to/your/folder'
event_handler = ZipHandler(folder_to_watch)
observer = Observer()
observer.schedule(event_handler, folder_to_watch, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()