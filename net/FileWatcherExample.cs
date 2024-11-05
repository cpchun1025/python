using System;
using System.IO;

public class FileWatcherExample
{
    private static FileSystemWatcher _watcher;

    public static void Main()
    {
        // Step 1: Set up the FileSystemWatcher
        _watcher = new FileSystemWatcher
        {
            Path = @"C:\path\to\watch\",  // Directory to monitor
            Filter = "*.csv",             // Only watch CSV files
            NotifyFilter = NotifyFilters.FileName | NotifyFilters.LastWrite  // Watch file name changes and modifications
        };

        // Step 2: Subscribe to the events you want to monitor
        _watcher.Created += OnFileCreated;    // File created event
        _watcher.Changed += OnFileChanged;    // File modified event
        _watcher.Deleted += OnFileDeleted;    // File deleted event
        _watcher.Renamed += OnFileRenamed;    // File renamed event

        // Step 3: Start watching
        _watcher.EnableRaisingEvents = true;

        Console.WriteLine("Watching directory for changes. Press 'Enter' to exit.");
        Console.ReadLine();  // Keep the program running until user presses Enter
    }

    // Event handler for file creation
    private static void OnFileCreated(object sender, FileSystemEventArgs e)
    {
        Console.WriteLine($"File created: {e.FullPath} at {DateTime.Now}");
        // Insert logic here to check file creation date and load if necessary
    }

    // Event handler for file modification
    private static void OnFileChanged(object sender, FileSystemEventArgs e)
    {
        Console.WriteLine($"File modified: {e.FullPath} at {DateTime.Now}");
        // Insert logic here to handle file modification (e.g., reload file if needed)
    }

    // Event handler for file deletion
    private static void OnFileDeleted(object sender, FileSystemEventArgs e)
    {
        Console.WriteLine($"File deleted: {e.FullPath} at {DateTime.Now}");
    }

    // Event handler for file renaming
    private static void OnFileRenamed(object sender, RenamedEventArgs e)
    {
        Console.WriteLine($"File renamed from {e.OldFullPath} to {e.FullPath} at {DateTime.Now}");
    }
}