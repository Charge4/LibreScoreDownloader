import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess, os, platform, threading, urllib.request, zipfile, tempfile, shutil, sys

CURRENT_VERSION = "1.0.0"
VERSION_URL = "https://raw.githubusercontent.com/yourusername/LibreScoreDownloader/main/version.txt"
ZIP_URL = "https://github.com/yourusername/LibreScoreDownloader/archive/refs/heads/main.zip"

APP_DIR = os.path.dirname(os.path.abspath(__file__))

class LibreScoreDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("LibreScore Downloader 🎵")
        self.root.geometry("600x400")

        try:
            self.root.iconbitmap(os.path.join(APP_DIR, "icon.ico"))
        except Exception as e:
            print(f"⚠️ Icon load failed: {e}")

        ttk.Style().configure("TButton", font=("Segoe UI", 10), padding=6)

        tk.Label(root, text="🎼 MuseScore URL or .mscz file:", font=("Segoe UI", 11)).pack(pady=8)
        self.url_entry = tk.Entry(root, width=70, font=("Segoe UI", 10))
        self.url_entry.pack(pady=4)

        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Paste", command=self.paste_clipboard)
        self.url_entry.bind("<Button-3>", self.show_context_menu)

        self.var_pdf = tk.BooleanVar()
        self.var_midi = tk.BooleanVar()
        self.var_mp3 = tk.BooleanVar()

        tk.Label(root, text="📁 Select file formats:", font=("Segoe UI", 11)).pack(pady=6)
        checkbox_frame = tk.Frame(root)
        checkbox_frame.pack()
        tk.Checkbutton(checkbox_frame, text="PDF", variable=self.var_pdf, font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Checkbutton(checkbox_frame, text="MIDI", variable=self.var_midi, font=("Segoe UI", 10)).pack(side="left", padx=10)
        tk.Checkbutton(checkbox_frame, text="MP3", variable=self.var_mp3, font=("Segoe UI", 10)).pack(side="left", padx=10)

        self.output_dir = os.path.expanduser("~/Downloads")
        ttk.Button(root, text="📂 Choose save directory", command=self.select_output_dir).pack(pady=10)

        folder_name = os.path.basename(self.output_dir) or self.output_dir
        self.output_dir_label = tk.Label(root, text=f"📁 Save folder: {folder_name}", font=("Segoe UI", 9))
        self.output_dir_label.pack()

        self.download_btn = ttk.Button(root, text="🚀 Start download", command=self.start_download_thread)
        self.download_btn.pack(pady=10)

        self.root.after(1000, self.check_for_update)  # Start update check

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def paste_clipboard(self):
        try:
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, self.root.clipboard_get())
        except tk.TclError:
            messagebox.showerror("Error", "Clipboard is empty")

    def select_output_dir(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.output_dir = selected_dir
            self.output_dir_label.config(text=f"📁 Save folder: {os.path.basename(self.output_dir)}")

    def start_download_thread(self):
        threading.Thread(target=self.start_download, daemon=True).start()

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url or (not url.startswith("http") and not os.path.isfile(url)):
            messagebox.showerror("Error", "❌ Please enter a valid URL or file path.")
            return

        filetypes = []
        if self.var_pdf.get(): filetypes.append("pdf")
        if self.var_midi.get(): filetypes.append("midi")
        if self.var_mp3.get(): filetypes.append("mp3")

        if not filetypes:
            messagebox.showerror("Error", "❌ Please select at least one file type.")
            return

        npx_cmd = "npx.cmd" if platform.system() == "Windows" else "npx"

        if not shutil.which(npx_cmd):
            messagebox.showerror("Error", "❌ Node.js (npx) not found.\nPlease install Node.js → https://nodejs.org/")
            return

        cmd = [npx_cmd, "dl-librescore@latest", url, "--output", self.output_dir]
        cmd += ["--" + ft for ft in filetypes]

        self.download_btn.config(text="⏳ Downloading...", state="disabled")
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Success", "🎉 Download completed!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"⚠️ Error:\n{e}")
        finally:
            self.download_btn.config(text="🚀 Start download", state="normal")

    def check_for_update(self):
        try:
            with urllib.request.urlopen(VERSION_URL) as response:
                latest_version = response.read().decode().strip()

            if latest_version != CURRENT_VERSION:
                if messagebox.askyesno("🔔 Update Available", f"New version {latest_version} is available.\nUpdate now?"):
                    self.download_and_replace()
        except Exception as e:
            print(f"Update check failed: {e}")

    def download_and_replace(self):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_path = os.path.join(tmpdir, "update.zip")
                urllib.request.urlretrieve(ZIP_URL, zip_path)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmpdir)

                extracted_folder = [f for f in os.listdir(tmpdir) if os.path.isdir(os.path.join(tmpdir, f))][0]
                extracted_path = os.path.join(tmpdir, extracted_folder)

                for item in os.listdir(extracted_path):
                    s = os.path.join(extracted_path, item)
                    d = os.path.join(APP_DIR, item)
                    if os.path.isdir(s):
                        shutil.rmtree(d, ignore_errors=True)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)

                messagebox.showinfo("✅ Updated", "App updated. Restarting...")
                self.root.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            messagebox.showerror("Update Error", f"❌ Update failed:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibreScoreDownloader(root)
    root.mainloop()
