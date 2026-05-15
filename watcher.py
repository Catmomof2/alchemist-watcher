
import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def __init__(self, markdown_file, css_file, output_dir):
        self.markdown_file = markdown_file
        self.css_file = css_file
        self.output_dir = output_dir
        self.convert_to_epub()

    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.abspath(event.src_path) == os.path.abspath(self.markdown_file):
            print(f"Markdown file {self.markdown_file} modified. Converting to EPUB...")
            self.convert_to_epub()

    def convert_to_epub(self):
        output_epub = os.path.join(self.output_dir, os.path.splitext(os.path.basename(self.markdown_file))[0] + ".epub")
        command = [
            "pandoc",
            self.markdown_file,
            "-o", output_epub,
            "--css", self.css_file,
            "--standalone",
            "--embed-resources",
            "--metadata", "title=The Alchemist's Watcher",
            "--metadata", "author=Manus AI"
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Successfully converted {self.markdown_file} to {output_epub}")
        except subprocess.CalledProcessError as e:
            print(f"Error during pandoc conversion: {e}")
        except FileNotFoundError:
            print("Error: pandoc not found. Please ensure pandoc is installed and in your PATH.")

if __name__ == "__main__":
    # Ensure pandoc is installed
    try:
        subprocess.run(["pandoc", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("pandoc is not installed or not in PATH. Please install pandoc to use this script.")
        print("On Ubuntu, you can install it with: sudo apt-get update && sudo apt-get install pandoc")
        exit(1)

    markdown_file = "/home/ubuntu/alchemist_watcher/manuscript.md"
    css_file = "/home/ubuntu/alchemist_watcher/gothic.css"
    output_dir = "/home/ubuntu/alchemist_watcher/output"

    os.makedirs(output_dir, exist_ok=True)

    event_handler = MarkdownHandler(markdown_file, css_file, output_dir)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(markdown_file), recursive=False)
    observer.start()

    print(f"Watching for changes in {markdown_file}. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
