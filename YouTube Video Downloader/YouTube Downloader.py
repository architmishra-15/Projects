import os
import subprocess
from pytube import YouTube
import customtkinter as ctk
from tkinter import messagebox

class YouTubeDownload:
    def __init__(self, url):
        self.yt = YouTube(url)
        self.video_quality = None

    def set_quality(self, quality):
        video_file = self.yt.streams.filter(only_video=True, mime_type="video/mp4").order_by('resolution')
        self.video_quality = {stream.resolution: stream for stream in video_file}.get(quality)
        if not self.video_quality:
            raise ValueError(f"Quality {quality} not available.")

    def download_audio(self):
        audio_file = self.yt.streams.filter(only_audio=True, mime_type="audio/mp4").first()
        audio_file_name = f"{self.yt.title}.wav"  # Use .wav extension for consistency
        audio_file.download(filename=audio_file_name)
        return audio_file_name

    def download_video(self):
        if not self.video_quality:
            raise ValueError("Video quality not set.")
        video_file_name = f"{self.yt.title}.mp4"
        self.video_quality.download(filename=video_file_name)
        return video_file_name

    def download(self, output_filename):
        try:
            # Download audio and video files
            audio_filename = self.download_audio()
            video_filename = self.download_video()

            # Merge files using ffmpeg
            if not (os.path.exists(audio_filename) and os.path.exists(video_filename)):
                raise FileNotFoundError("Audio or video file missing.")

            command = [
                "ffmpeg",
                "-i", video_filename,
                "-i", audio_filename,
                "-c:v", "copy",
                "-c:a", "aac",
                output_filename
            ]

            subprocess.run(command, check=True)

            # Delete original audio and video files
            os.remove(audio_filename)
            os.remove(video_filename)

            return f"File downloaded as {output_filename}"
        except Exception as e:
            return str(e)


class DownloadGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("1080x720")  # Default window size
        self.center_window()

        self.iconbitmap('icon.ico')

        # URL Entry
        self.url_entry = ctk.CTkEntry(self, width=600, placeholder_text="Enter YouTube URL")
        self.url_entry.pack(pady=10)

        # File Name Entry
        self.output_entry = ctk.CTkEntry(self, width=600, placeholder_text="Enter output file name")
        self.output_entry.pack(pady=10)

        # Quality Selection
        self.quality_var = ctk.StringVar(value="1080zp")
        quality_frame = ctk.CTkFrame(self)
        quality_frame.pack(pady=10)
        self.quality_options = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        for quality in self.quality_options:
            ctk.CTkRadioButton(quality_frame, text=quality, variable=self.quality_var, value=quality).pack(side="left", padx=5)

        # Download Button
        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download)
        self.download_button.pack(pady=10)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10, fill="x", padx=20)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def start_download(self):
        url = self.url_entry.get()
        quality = self.quality_var.get()
        output_name = self.output_entry.get()

        try:
            yt_downloader = YouTubeDownload(url)
            yt_downloader.set_quality(quality)
            result = yt_downloader.download(output_name)
            messagebox.showinfo("Download Complete", result)
        except Exception as e:
            messagebox.showerror("Download Error", str(e))


if __name__ == "__main__":
    app = DownloadGUI()
    app.mainloop()
