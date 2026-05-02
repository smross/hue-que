import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Using abspath ensures the script finds the folders regardless of where it's launched
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WATCH_FOLDER = os.path.join(BASE_DIR, "incoming")
DEST_FOLDER = os.path.join(BASE_DIR, "static/photos")

class GuestManager:
    def __init__(self):
        self.current_id = "000"
        self.counter = 1

    def set_guest(self, new_id):
        # Auto-pads (e.g., "5" becomes "005") for better file sorting
        self.current_id = str(new_id).zfill(3)
        self.counter = 1
        print(f"\n[ READY ] Now shooting Guest #{self.current_id}")

manager = GuestManager()

def process_file(file_path):
    """The logic to rename and move the file."""
    if not file_path.lower().endswith(('.jpg', '.jpeg')):
        return

    # Small delay to ensure the file is fully written to disk
    time.sleep(0.7) 
    
    ext = os.path.splitext(file_path)[1]
    new_filename = f"{manager.current_id}_{manager.counter}{ext}"
    dest_path = os.path.join(DEST_FOLDER, new_filename)
    
    try:
        os.rename(file_path, dest_path)
        print(f"  >> Teleported: {new_filename}")
        manager.counter += 1
    except Exception as e:
        print(f"  !! Error moving file: {e}")

def sweep_incoming():
    """Check for files already in 'incoming' on startup."""
    print("[ SWEEPING ] Checking for existing files...")
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)
        
    for filename in os.listdir(WATCH_FOLDER):
        full_path = os.path.join(WATCH_FOLDER, filename)
        if os.path.isfile(full_path):
            process_file(full_path)

class RenameHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

# --- EXECUTION ---
sweep_incoming()
observer = Observer()
observer.schedule(RenameHandler(), WATCH_FOLDER, recursive=False)
observer.start()

try:
    print("="*30)
    print("HUE-QUEUE COMMAND CENTER")
    print("="*30)
    while True:
        val = input("Enter Guest Number (or 'q' to quit): ")
        if val.lower() == 'q': break
        if val: manager.set_guest(val)
except KeyboardInterrupt:
    pass
finally:
    observer.stop()
    observer.join()
