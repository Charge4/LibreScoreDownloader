import tkinter as tk
from tkinter import messagebox
import urllib.request, subprocess, sys, os, platform

APP_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(APP_DIR, "version.txt")

# 📄 წაიკითხე ლოკალური ვერსია version.txt-დან
def get_local_version():
    try:
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    except:
        return "0.0.0"

LOCAL_VERSION = get_local_version()
GITHUB_RAW = "https://raw.githubusercontent.com/besochargeishvili/LibreScoreDownloader/main"
UPDATE_FILES = ["main.py", "version.txt"]

def check_for_update():
    try:
        version_url = f"{GITHUB_RAW}/version.txt"
        with urllib.request.urlopen(version_url) as res:
            remote_version = res.read().decode().strip()
        if remote_version != LOCAL_VERSION:
            answer = messagebox.askyesno("🔄 Update available", f"New version available:\n{remote_version}\nUpdate now?")
            if answer:
                for filename in UPDATE_FILES:
                    urllib.request.urlretrieve(f"{GITHUB_RAW}/{filename}", os.path.join(APP_DIR, filename))
                messagebox.showinfo("✅ Updated", "Application updated. Restarting...")
                restart_app()
    except Exception as e:
        print(f"Update check failed: {e}")

def restart_app():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# 🪟 მარტივი GUI
class App:
    def __init__(self, root):
        root.title("LibreScore Downloader 🎵")
        tk.Label(root, text=f"📥 Version {LOCAL_VERSION}", font=("Segoe UI", 12)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.after(1000, check_for_update)
    root.mainloop()
