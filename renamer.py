import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# SET THESE PATHS
WATCH_FOLDER = "./incoming_from_canon" # Point Canon EOS Utility here
DEST_FOLDER = "./static/photos"        # Your Flask app's folder

class GuestManager:
    def __init__(self):
        self.current_id = "000"
        self.counter = 1

    def set_guest(self, new_id):
        self.current_id = new_id
        self.counter = 1
        print(f"--- NOW SHOOTING GUEST: #{self.current_id} ---")

manager = GuestManager()

class RenameHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg')):
            time.sleep(0.5) # Wait for file to finish writing
            ext = os.path.splitext(event.src_path)[1]
            new_name = f"{manager.current_id}_{manager.counter}{ext}"
            dest_path = os.path.join(DEST_FOLDER, new_name)
            
            os.rename(event.src_path, dest_path)
            print(f"Saved: {new_name}")
            manager.counter += 1

# Start the Watcher
observer = Observer()
observer.schedule(RenameHandler(), WATCH_FOLDER, recursive=False)
observer.start()

try:
    print("HUE-QUEUE COMMAND CENTER")
    print("-----------------------")
    while True:
        new_id = input("Enter Next Guest ID: ")
        manager.set_guest(new_id)
except KeyboardInterrupt:
    observer.stop()
observer.join()
