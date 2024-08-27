import os
import time
import shutil
from datetime import datetime, timedelta

# Configuration
source_folder = "/path/to/source_folder"
dest_folder = "/path/to/dest_folder"
filename = "your_file_name"  # e.g., "data.csv"
check_interval = 10  # seconds to wait between file size checks
timeout = 3600  # max seconds to wait for the file (1 hour)

def is_file_fully_written(filepath, check_interval):
    """
    Check if the file is fully written by monitoring its size.
    """
    initial_size = os.path.getsize(filepath)
    time.sleep(check_interval)
    new_size = os.path.getsize(filepath)
    return initial_size == new_size

def copy_file_if_ready(source_path, dest_path, check_interval, timeout):
    """
    Copy file from source to destination if it's fully written.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if os.path.exists(source_path):
            if is_file_fully_written(source_path, check_interval):
                shutil.copy2(source_path, dest_path)
                print(f"File copied successfully to {dest_path}")
                return True
            else:
                print("File not fully written yet, waiting...")
        else:
            print("File not found, waiting...")
        
        time.sleep(check_interval)
    
    print("File not available or not fully written within the timeout period.")
    return False

def main():
    current_time = datetime.now()
    
    # Adjust for files arriving late or on the next day
    check_date = current_time.strftime("%Y%m%d")
    source_file = os.path.join(source_folder, f"{check_date}_{filename}")
    dest_file = os.path.join(dest_folder, f"{check_date}_{filename}")
    
    if not copy_file_if_ready(source_file, dest_file, check_interval, timeout):
        # If the file didn't arrive in time, you might want to log it or retry later
        print(f"File {filename} was not ready to be copied.")

if __name__ == "__main__":
    main()