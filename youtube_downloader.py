import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar, BooleanVar
import yt_dlp
import threading
import os

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # URL Section
        self.url_label = ttk.Label(self.main_frame, text="YouTube URL/Playlist:")
        self.url_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.url_entry = ttk.Entry(self.main_frame, width=60)
        self.url_entry.grid(row=1, column=0, columnspan=3, pady=5, sticky=tk.EW)
        
        # Playlist Controls
        self.playlist_var = BooleanVar(value=False)
        self.playlist_check = ttk.Checkbutton(self.main_frame, 
                                            text="Download Playlist",
                                            variable=self.playlist_var,
                                            command=self.toggle_playlist_options)
        self.playlist_check.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Playlist Options Frame
        self.playlist_frame = ttk.Frame(self.main_frame)
        self.playlist_start_label = ttk.Label(self.playlist_frame, text="Start Video:")
        self.playlist_start = ttk.Spinbox(self.playlist_frame, from_=1, to=1000, width=5)
        self.playlist_end_label = ttk.Label(self.playlist_frame, text="End Video:")
        self.playlist_end = ttk.Spinbox(self.playlist_frame, from_=1, to=1000, width=5)
        
        self.playlist_start_label.pack(side=tk.LEFT, padx=5)
        self.playlist_start.pack(side=tk.LEFT)
        self.playlist_end_label.pack(side=tk.LEFT, padx=5)
        self.playlist_end.pack(side=tk.LEFT)
        
        # Format Selection
        self.format_label = ttk.Label(self.main_frame, text="Download Format:")
        self.format_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.format_var = StringVar(value='video')
        self.format_combobox = ttk.Combobox(self.main_frame, 
                                          textvariable=self.format_var,
                                          values=('video', 'audio'),
                                          state='readonly',
                                          width=10)
        self.format_combobox.grid(row=3, column=1, sticky=tk.W, pady=5)
        self.format_combobox.bind('<<ComboboxSelected>>', self.update_quality_options)
        
        # Quality Selection
        self.quality_frame = ttk.Frame(self.main_frame)
        self.quality_frame.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Video Quality
        self.video_quality_label = ttk.Label(self.quality_frame, text="Video Quality:")
        self.video_quality_var = StringVar(value='1080p')
        self.video_quality = ttk.Combobox(self.quality_frame, 
                                        textvariable=self.video_quality_var,
                                        values=('2160p', '1440p', '1080p', '720p', '480p', '360p'),
                                        state='readonly',
                                        width=8)
        # Audio Quality
        self.audio_quality_label = ttk.Label(self.quality_frame, text="Audio Quality:")
        self.audio_quality_var = StringVar(value='192k')
        self.audio_quality = ttk.Combobox(self.quality_frame, 
                                       textvariable=self.audio_quality_var,
                                       values=('320k', '256k', '192k', '160k', '128k'),
                                       state='readonly',
                                       width=6)
        
        self.video_quality_label.pack(side=tk.LEFT, padx=5)
        self.video_quality.pack(side=tk.LEFT)
        self.audio_quality_label.pack(side=tk.LEFT, padx=5)
        self.audio_quality.pack(side=tk.LEFT)
        
        # Output Directory
        self.dir_label = ttk.Label(self.main_frame, text="Output Directory:")
        self.dir_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.dir_var = StringVar(value=os.path.expanduser('~/Downloads'))
        self.dir_entry = ttk.Entry(self.main_frame, textvariable=self.dir_var, width=50)
        self.dir_entry.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self.choose_directory)
        self.browse_button.grid(row=6, column=2, sticky=tk.E, padx=5)
        
        # Progress Section
        self.progress_bar = ttk.Progressbar(self.main_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=tk.EW, pady=20)
        
        self.status_label = ttk.Label(self.main_frame, text="Ready", foreground="gray")
        self.status_label.grid(row=8, column=0, columnspan=3, sticky=tk.W)
        
        # Download Button
        self.download_button = ttk.Button(self.main_frame, 
                                        text="Start Download", 
                                        command=self.start_download_thread)
        self.download_button.grid(row=9, column=0, columnspan=3, pady=10)
        
        # Initialize UI
        self.update_quality_options()
        self.toggle_playlist_options()
        
        # Configure grid weights
        self.main_frame.columnconfigure(0, weight=1)

    def toggle_playlist_options(self):
        if self.playlist_var.get():
            self.playlist_frame.grid(row=2, column=1, sticky=tk.W, pady=5)
        else:
            self.playlist_frame.grid_remove()
            
    def update_quality_options(self, event=None):
        if self.format_var.get() == 'video':
            self.video_quality.config(state='readonly')
            self.audio_quality.config(state='disabled')
        else:
            self.video_quality.config(state='disabled')
            self.audio_quality.config(state='readonly')
            
    def choose_directory(self):
        directory = filedialog.askdirectory(initialdir=self.dir_var.get())
        if directory:
            self.dir_var.set(directory)
            
    def start_download_thread(self):
        if not self.validate_inputs():
            return
        
        self.download_button.config(state=tk.DISABLED)
        threading.Thread(target=self.download_content, daemon=True).start()
        
    def validate_inputs(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return False
        if self.playlist_var.get():
            try:
                start = int(self.playlist_start.get())
                end = int(self.playlist_end.get())
                if start > end:
                    messagebox.showerror("Error", "Start index cannot be greater than end index")
                    return False
            except ValueError:
                messagebox.showerror("Error", "Please enter valid playlist indices")
                return False
        return True
    
    def download_content(self):
        url = self.url_entry.get().strip()
        download_format = self.format_var.get()
        output_dir = self.dir_var.get()
        
        ydl_opts = {
            'outtmpl': f"{output_dir}/%(playlist_title)s/%(title)s.%(ext)s",
            'progress_hooks': [self.update_progress],
            'restrictfilenames': True,
            'quiet': True,
            'noplaylist': not self.playlist_var.get(),
        }
        
        # Playlist options
        if self.playlist_var.get():
            ydl_opts.update({
                'playliststart': int(self.playlist_start.get()),
                'playlistend': int(self.playlist_end.get()),
                'ignoreerrors': True
            })
        
        # Format and quality options
        if download_format == 'video':
            quality_map = {'2160p': 2160, '1440p': 1440, '1080p': 1080, 
                          '720p': 720, '480p': 480, '360p': 360}
            selected_quality = quality_map[self.video_quality_var.get()]
            ydl_opts['format'] = f'bestvideo[height<={selected_quality}]+bestaudio/best[height<={selected_quality}]'
            ydl_opts['merge_output_format'] = 'mp4'
        else:
            quality_map = {'320k': 0, '256k': 2, '192k': 5, '160k': 6, '128k': 8}
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': str(quality_map[self.audio_quality_var.get()]),
            }]
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if self.playlist_var.get():
                    success_count = sum(1 for e in info['entries'] if e is not None)
                    self.root.after(0, self.show_success_message, 
                                  f"Downloaded {success_count}/{len(info['entries'])} videos from playlist")
                else:
                    self.root.after(0, self.show_success_message, 
                                  f"Download completed: {info['title']}")
            
        except Exception as e:
            self.root.after(0, self.show_error_message, str(e))
            
        finally:
            self.root.after(0, self.reset_ui)
            
    def update_progress(self, d):
        self.root.after(0, self._handle_progress_update, d)
            
    def _handle_progress_update(self, d):
        if d['status'] == 'downloading':
            title = d.get('info_dict', {}).get('title', 'Unknown Title')
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            
            try:
                progress = float(percent.strip('%'))
                self.progress_bar['value'] = progress
            except:
                pass
            
            self.status_label.config(text=f"Downloading: {title} | {percent} | {speed} | ETA: {eta}")
            
        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.status_label.config(text="Finalizing download...", foreground="green")

    def show_success_message(self, message):
        messagebox.showinfo("Success", message)
        
    def show_error_message(self, error):
        messagebox.showerror("Error", f"Download failed:\n{error}")
        
    def reset_ui(self):
        self.progress_bar['value'] = 0
        self.download_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", foreground="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
