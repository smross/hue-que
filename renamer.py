import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WATCH_FOLDER = os.path.join(BASE_DIR, "incoming")
DEST_FOLDER = os.path.join(BASE_DIR, "static/photos")

# Unambiguous alphabet (Removed: I, L, O, U, V)
CLEAN_ALPHABET = "ABCDEFGHJKMNPQRSTWXYZ"

class GuestManager:
    def __init__(self):
        self.current_id = "000"
        self.counter = 0 # Starts at 0 to index into alphabet

    def set_guest(self, new_id):
        self.current_id = str(new_id).zfill(3)
        self.counter = 0
        print(f"\n[ READY ] Now shooting Guest #{self.current_id}")

manager = GuestManager()

def process_file(file_path):
    """The logic to rename and teleport the file with a letter suffix."""
    if not file_path.lower().endswith(('.jpg', '.jpeg')):
        return

    time.sleep(0.7) 
    
    # Get the letter based on the counter
    # If a guest has more than 21 photos, it will start over at A
    letter_index = manager.counter % len(CLEAN_ALPHABET)
    suffix = CLEAN_ALPHABET[letter_index]
    
    ext = os.path.splitext(file_path)[1]
    new_filename = f"{manager.current_id}_{suffix}{ext}"
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
