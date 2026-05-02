import os
import time
from flask import Flask, render_template, send_from_directory
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

app = Flask(__name__)
# Absolute path to the photo directory
PHOTO_DIR = os.path.join(app.root_path, 'static', 'photos')

# --- THE WATCHER (Detects new files) ---
class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg')):
            print(f"--- [NEW PHOTO] {os.path.basename(event.src_path)} arrived! ---")

def start_watcher():
    if not os.path.exists(PHOTO_DIR): os.makedirs(PHOTO_DIR)
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, PHOTO_DIR, recursive=False)
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

# --- THE SERVER (Shows the photos) ---
@app.route('/')
def index():
    if not os.path.exists(PHOTO_DIR): os.makedirs(PHOTO_DIR)
    # Get files sorted by creation time (newest first)
    files = [f for f in os.listdir(PHOTO_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
    photos = sorted(files, key=lambda x: os.path.getmtime(os.path.join(PHOTO_DIR, x)), reverse=True)
    return render_template('index.html', photos=photos)

if __name__ == '__main__':
    # Start the watcher in the background
    Thread(target=start_watcher, daemon=True).start()
    # Run the web server
    app.run(host='0.0.0.0', port=5000, debug=False)
