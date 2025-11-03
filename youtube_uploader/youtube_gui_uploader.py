import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys

# ensure emoji printing works on Windows
sys.stdout.reconfigure(encoding='utf-8')


# 🌸 Upload video function
def upload_video():
    file_path = entry_file.get()
    title = entry_title.get()
    description = entry_description.get("1.0", tk.END).strip()
    category = entry_category.get()
    privacy = privacy_var.get()
    thumbnail_path = entry_thumbnail.get()

    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Error", "Please select a valid video file.")
        return
    if not title:
        messagebox.showerror("Error", "Please enter a video title.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))

    cmd = [
        sys.executable, "-m", "youtube_uploader.youtube_uploader",
        "--file", file_path,
        "--title", title,
        "--description", description,
        "--category", category,
        "--privacy", privacy
    ]

    if thumbnail_path:
        cmd.extend(["--thumbnail", thumbnail_path])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=script_dir
        )

        print("\n🪶 DEBUG OUTPUT:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("RETURN CODE:", result.returncode)

        if result.returncode == 0:
            messagebox.showinfo("Success", "✅ Video uploaded successfully!")
        else:
            messagebox.showerror(
                "Failed",
                f"❌ Upload failed.\n\nError details:\n{result.stderr or result.stdout}"
            )

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")


def browse_video():
    path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.webm")]
    )
    if path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, path)


def browse_thumbnail():
    path = filedialog.askopenfilename(
        title="Select Thumbnail Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if path:
        entry_thumbnail.delete(0, tk.END)
        entry_thumbnail.insert(0, path)


# 🌿 Main window setup
def main():
    global entry_file, entry_title, entry_description, entry_category, privacy_var, entry_thumbnail

    root = tk.Tk()
    root.title("YouTube Video Uploader 🌸")
    root.geometry("550x550")
    root.resizable(False, False)
    root.configure(bg="#faf4ff")

    # 🌸 Title Label
    tk.Label(root, text="✨ YouTube Uploader", font=("Segoe UI", 18, "bold"), bg="#faf4ff", fg="#5b3e96").pack(pady=15)

    # Video File
    tk.Label(root, text="🎬 Video File:", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30)
    frame_file = tk.Frame(root, bg="#faf4ff")
    frame_file.pack(pady=5)
    entry_file = tk.Entry(frame_file, width=45)
    entry_file.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_file, text="Browse", command=browse_video, bg="#d8c6ff").pack(side=tk.LEFT)

    # Title
    tk.Label(root, text="📝 Title:", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30, pady=(10, 0))
    entry_title = tk.Entry(root, width=50)
    entry_title.pack(pady=5)

    # Description
    tk.Label(root, text="💬 Description:", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30, pady=(10, 0))
    entry_description = tk.Text(root, width=50, height=4)
    entry_description.pack(pady=5)

    # Category
    tk.Label(root, text="📂 Category ID (e.g., 22):", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30, pady=(10, 0))
    entry_category = tk.Entry(root, width=10)
    entry_category.insert(0, "22")
    entry_category.pack(pady=5)

    # Privacy
    tk.Label(root, text="🔒 Privacy:", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30, pady=(10, 0))
    privacy_var = tk.StringVar(value="private")
    tk.OptionMenu(root, privacy_var, "private", "unlisted", "public").pack(pady=5)

    # Thumbnail
    tk.Label(root, text="🖼 Thumbnail (optional):", bg="#faf4ff", fg="#3c2a68").pack(anchor="w", padx=30, pady=(10, 0))
    frame_thumb = tk.Frame(root, bg="#faf4ff")
    frame_thumb.pack(pady=5)
    entry_thumbnail = tk.Entry(frame_thumb, width=45)
    entry_thumbnail.pack(side=tk.LEFT, padx=5)
    tk.Button(frame_thumb, text="Browse", command=browse_thumbnail, bg="#d8c6ff").pack(side=tk.LEFT)

    # Upload button
    tk.Button(root, text="🚀 Upload Video", command=upload_video, bg="#cbb2ff", fg="#2c184a",
              font=("Segoe UI", 11, "bold")).pack(pady=20)

    # Footer
    tk.Label(root, text="Made with 💜 by Noor", bg="#faf4ff", fg="#7a5dc7", font=("Segoe UI", 9)).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
