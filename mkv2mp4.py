import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

# ── Core conversion (same logic as the original script) ──────────────────────
def convert_mkv_to_mp4(filename, log):
    output_file = filename.replace('.mkv', '.mp4')
    log(f"Converting {os.path.basename(filename)}...")
    subprocess.run([
        'ffmpeg', '-y', '-i', filename,
        '-c:v', 'copy',    # copy video as-is (HEVC/H.264 both work)
        '-c:a', 'aac',     # re-encode audio to AAC (fixes DTS/Vorbis/TrueHD)
        '-b:a', '192k',    # good audio quality
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log(f"Done → {os.path.basename(output_file)}")

# ── GUI ───────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("MKV → MP4")
root.configure(bg="#1c1c1e")
root.resizable(False, False)

W = 480

# Title
tk.Label(root, text="MKV → MP4 Converter", font=("Segoe UI", 14, "bold"),
         bg="#1c1c1e", fg="#ffffff").pack(pady=(20, 4))
tk.Label(root, text="Video copied · Audio fixed to AAC · Opens everywhere",
         font=("Segoe UI", 9), bg="#1c1c1e", fg="#888888").pack(pady=(0, 16))

# File list box
frame = tk.Frame(root, bg="#1c1c1e")
frame.pack(padx=20, fill="x")

tk.Label(frame, text="Selected files", font=("Segoe UI", 9),
         bg="#1c1c1e", fg="#888888", anchor="w").pack(fill="x")

listbox = tk.Listbox(frame, height=8, width=60,
                     bg="#2c2c2e", fg="#e5e5e7",
                     selectbackground="#0a84ff",
                     font=("Consolas", 9),
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground="#3a3a3c",
                     activestyle="none")
listbox.pack(fill="x", pady=(4, 0))

selected_files = []

def browse():
    files = filedialog.askopenfilenames(
        title="Select MKV files",
        filetypes=[("MKV files", "*.mkv")]
    )
    for f in files:
        if f not in selected_files:
            selected_files.append(f)
            listbox.insert(tk.END, os.path.basename(f))

def clear():
    selected_files.clear()
    listbox.delete(0, tk.END)
    log_box.config(state="normal")
    log_box.delete("1.0", tk.END)
    log_box.config(state="disabled")

# Buttons row
btn_frame = tk.Frame(root, bg="#1c1c1e")
btn_frame.pack(padx=20, pady=10, fill="x")

def make_btn(parent, text, cmd, primary=False):
    return tk.Button(parent, text=text, command=cmd,
                     bg="#0a84ff" if primary else "#3a3a3c",
                     fg="#ffffff",
                     activebackground="#0060df" if primary else "#555558",
                     activeforeground="#ffffff",
                     font=("Segoe UI", 10, "bold") if primary else ("Segoe UI", 10),
                     relief="flat", bd=0, padx=16, pady=7, cursor="hand2")

make_btn(btn_frame, "＋ Add Files", browse).pack(side="left", padx=(0, 8))
make_btn(btn_frame, "✕ Clear", clear).pack(side="left")
btn_convert = make_btn(btn_frame, "▶  Convert", lambda: start(), primary=True)
btn_convert.pack(side="right")

# Log box
tk.Label(root, text="Log", font=("Segoe UI", 9),
         bg="#1c1c1e", fg="#888888", anchor="w").pack(padx=20, fill="x")

log_box = tk.Text(root, height=7, width=60,
                  bg="#2c2c2e", fg="#30d158",
                  font=("Consolas", 9),
                  relief="flat", bd=0,
                  highlightthickness=1,
                  highlightbackground="#3a3a3c",
                  state="disabled", padx=6, pady=6)
log_box.pack(padx=20, pady=(4, 20), fill="x")

def log(msg):
    def _write():
        log_box.config(state="normal")
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)
        log_box.config(state="disabled")
    root.after(0, _write)

# Conversion logic
def start():
    if not selected_files:
        messagebox.showinfo("No files", "Add at least one MKV file first.")
        return

    btn_convert.config(state="disabled", text="Converting…")

    def run():
        for f in selected_files:
            convert_mkv_to_mp4(f, log)
        log("✓ All done!")
        root.after(0, lambda: btn_convert.config(state="normal", text="▶  Convert"))

    threading.Thread(target=run, daemon=True).start()

root.mainloop()
