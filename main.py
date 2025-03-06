import os
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, OptionMenu, Checkbutton, BooleanVar, Frame
from tkinter.ttk import Progressbar, Style
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import time
from yt_dlp import YoutubeDL
from tkinter import TclError
from tkinterdnd2 import DND_TEXT, TkinterDnD

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("800x900")
        
        # Variables
        self.url_var = StringVar()
        self.resolution_var = StringVar()
        self.audio_only_var = BooleanVar()  # Audio only toggle
        self.download_path = os.getcwd()
        self.current_theme = StringVar(value="youtube")
        
        # Create styles FIRST
        self.create_styles()
        
        # Configure root background
        self.root.configure(bg=self.get_bg_color())
        
        # Main container with padding
        self.main_frame = Frame(root, bg=self.get_bg_color())
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title Label with YouTube-style red
        Label(self.main_frame,
              text="YouTube Downloader",
              font=('Segoe UI', 32, 'bold'),
              bg=self.get_bg_color(),
              fg=self.get_accent_color()).pack(pady=(0, 40))

        # URL Input section with modern styling
        Label(self.main_frame,
              text="Enter YouTube URL (or drag and drop):",
              font=('Segoe UI', 14),
              bg=self.get_bg_color(),
              fg='#FFFFFF').pack(pady=(0, 10))
        
        # Styled Entry with border
        entry_frame = Frame(self.main_frame, bg='#1A1A1A', padx=3, pady=3)
        entry_frame.pack(fill='x', padx=40)
        
        self.url_entry = Entry(entry_frame,
                              textvariable=self.url_var,
                              font=('Segoe UI', 13),
                              bg='#121212',
                              fg='#FFFFFF',
                              insertbackground='#FFFFFF',
                              relief='flat')
        self.url_entry.pack(fill='x', pady=3, ipady=12)
        
        # Preview Button with sleek modern style
        preview_btn = Button(self.main_frame,
                           text="PREVIEW",
                           command=self.preview_video,
                           font=('Segoe UI', 13),
                           bg='#FF0000',
                           fg='#000000',
                           activebackground='#CC0000',
                           activeforeground='#000000',
                           relief='flat',
                           bd=0,
                           padx=40,
                           pady=15,
                           cursor='hand2')
        preview_btn.pack(pady=25)
        
        # Update hover effect for preview button
        def on_preview_enter(e):
            preview_btn['bg'] = '#CC0000'
            preview_btn['font'] = ('Segoe UI', 13, 'bold')
        def on_preview_leave(e):
            preview_btn['bg'] = '#FF0000'
            preview_btn['font'] = ('Segoe UI', 13)
            
        preview_btn.bind('<Enter>', on_preview_enter)
        preview_btn.bind('<Leave>', on_preview_leave)
        
        # Preview Frame with modern border
        preview_container = Frame(self.main_frame, bg='#1A1A1A', padx=3, pady=3)
        preview_container.pack(fill='x', padx=40)
        
        self.preview_frame = Label(preview_container,
                                 text="",
                                 wraplength=600,
                                 bg='#0A0A0A',
                                 fg='#FFFFFF',
                                 font=('Segoe UI', 13),
                                 pady=20)
        self.preview_frame.pack(fill='x', pady=2)
        
        # Thumbnail Label with dark background
        self.thumbnail_label = Label(self.main_frame, bg='#0F0F0F')
        self.thumbnail_label.pack(pady=15)
        
        # Quality section with darker theme
        Label(self.main_frame,
              text="QUALITY",
              font=('Segoe UI', 14, 'bold'),
              bg='#000000',
              fg='#FFFFFF').pack(pady=(30, 10))
        
        # Quality dropdown with dark theme
        resolution_frame = Frame(self.main_frame, bg='#2F2F2F', padx=2, pady=2)
        resolution_frame.pack(pady=5)
        
        self.resolution_var.set("720p")
        resolution_menu = OptionMenu(resolution_frame,
                                   self.resolution_var,
                                   "360p", "480p", "720p", "1080p")
        resolution_menu.config(bg='#FF0000',
                             fg='#000000',
                             activebackground='#CC0000',
                             activeforeground='#000000',
                             font=('Segoe UI', 10),
                             relief='flat',
                             bd=0,
                             highlightthickness=0,
                             padx=20,
                             pady=8)
        resolution_menu["menu"].config(bg='#FF0000',
                                     fg='#000000',
                                     activebackground='#CC0000',
                                     activeforeground='#000000',
                                     font=('Segoe UI', 10),
                                     relief='flat',
                                     bd=0)
        resolution_menu.pack()

        # Folder Selection Button
        folder_btn = Button(self.main_frame,
                    text="Set Download Folder",
                    command=self.select_folder,
                    font=('Segoe UI', 13),
                    bg='#FF0000',
                    fg='#000000',
                    activebackground='#CC0000',
                    activeforeground='#000000',
                    relief='flat',
                    bd=0,
                    padx=40,
                    pady=15,
                    cursor='hand2')
        folder_btn.pack(pady=10)

        # Audio Only Checkbox
        audio_only_check = Checkbutton(self.main_frame,
                                       text="Audio Only",
                                       variable=self.audio_only_var,
                                       onvalue=True,
                                       offvalue=False,
                                       font=('Segoe UI', 12),
                                       bg=self.get_bg_color(),
                                       fg="#FFFFFF")
        audio_only_check.pack(pady=5)

        # Download Button with modern gradient effect
        download_frame = Frame(self.main_frame, bg='#FF0000', padx=2, pady=2)
        download_frame.pack(pady=25)
        
        download_btn = Button(download_frame,
                            text="DOWNLOAD",
                            command=self.download_video,
                            font=('Segoe UI', 15),
                            bg='#FF0000',
                            fg='#000000',
                            activebackground='#CC0000',
                            activeforeground='#000000',
                            relief='flat',
                            bd=0,
                            padx=45,
                            pady=16,
                            cursor='hand2')
        download_btn.pack()
        
        # Add hover effect for download button
        def on_download_enter(e):
            download_btn['bg'] = '#CC0000'
            download_btn['font'] = ('Segoe UI', 15, 'bold')
        def on_download_leave(e):
            download_btn['bg'] = '#FF0000'
            download_btn['font'] = ('Segoe UI', 15)
            
        download_btn.bind('<Enter>', on_download_enter)
        download_btn.bind('<Leave>', on_download_leave)

        # Progress Bar with darker theme
        style = Style()
        style.configure("YouTube.Horizontal.TProgressbar",
                       troughcolor='#0A0A0A',
                       background='#FF0000',
                       thickness=8,
                       borderwidth=0)
        
        self.progress = Progressbar(self.main_frame,
                                  length=600,
                                  mode='determinate',
                                  style="YouTube.Horizontal.TProgressbar")
        self.progress.pack(pady=20)
        
        # Status Label with dark theme
        self.status_label = Label(self.main_frame,
                                text="",
                                fg='#AAAAAA',
                                bg='#0F0F0F',
                                font=('Segoe UI', 12))
        self.status_label.pack(pady=10)

        # Enable drag and drop
        self.url_entry.drop_target_register(DND_TEXT)
        self.url_entry.dnd_bind('<<Drop>>', self.handle_drop)

    def create_styles(self):
        self.themes = {
            'youtube': {
                'bg': '#000000',          # Pure black background (darker than before)
                'fg': '#FFFFFF',          # White text
                'accent': '#FF0000',      # YouTube red
                'button_bg': '#1A1A1A',   # Darker button background
                'button_fg': '#FFFFFF',   # White button text
                'entry_bg': '#0A0A0A',    # Very dark input background
                'entry_fg': '#FFFFFF',    # White input text
                'hover_bg': '#2D2D2D'     # Slightly lighter hover effect
            }
        }

    def get_bg_color(self): return self.themes[self.current_theme.get()]['bg']
    def get_fg_color(self): return self.themes[self.current_theme.get()]['fg']
    def get_accent_color(self): return self.themes[self.current_theme.get()]['accent']
    def get_button_bg(self): return self.themes[self.current_theme.get()]['button_bg']
    def get_button_fg(self): return self.themes[self.current_theme.get()]['button_fg']
    def get_entry_bg(self): return self.themes[self.current_theme.get()]['entry_bg']
    def get_entry_fg(self): return self.themes[self.current_theme.get()]['entry_fg']

    def preview_video(self):
        """Show video information before downloading"""
        url = self.url_var.get()
        if not url:
            self.status_label.config(text="Please enter a URL first", fg="red")
            return

        try:
            self.status_label.config(text="Fetching video info...", fg="blue")
            self.root.update()

            with YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Display video information
                duration_mins = info['duration'] // 60
                duration_secs = info['duration'] % 60
                
                preview_text = (
                    f"Title: {info['title']}\n"
                    f"Duration: {duration_mins}:{duration_secs:02d}\n"
                    f"Channel: {info['channel']}\n"
                    f"Views: {info.get('view_count', 'N/A')}"
                )
                
                self.preview_frame.config(text=preview_text)
                
                # Load and display thumbnail
                try:
                    response = requests.get(info['thumbnail'])
                    img_data = Image.open(BytesIO(response.content))
                    # Resize thumbnail to fit window
                    img_data.thumbnail((300, 300))
                    img = ImageTk.PhotoImage(img_data)
                    self.thumbnail_label.config(image=img)
                    self.thumbnail_label.image = img  # Keep a reference!
                except Exception as e:
                    print(f"Thumbnail error: {e}")

            self.status_label.config(text="Preview loaded successfully", fg="green")
            
        except Exception as e:
            self.status_label.config(text=f"Preview error: {str(e)}", fg="red")
            self.preview_frame.config(text="")
            self.thumbnail_label.config(image="")

    def handle_drop(self, event):
        """Handle drag and drop events"""
        try:
            url = event.data
            url = url.strip().strip('"\'')
            self.url_var.set(url)
            # Auto-preview when URL is dropped
            self.preview_video()
        except Exception as e:
            self.status_label.config(text=f"Error with dropped URL: {str(e)}", fg="red")

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path = folder_selected
            self.status_label.config(text=f"Download Folder: {self.download_path}")

    def download_video(self):
        url = self.url_var.get()
        resolution = self.resolution_var.get()
        audio_only = self.audio_only_var.get()

        if not url:
            self.status_label.config(text="Please enter a valid URL.", fg="red")
            return

        try:
            # Reset progress bar
            self.progress['value'] = 0
            self.status_label.config(text="Starting download...", fg="blue")
            self.root.update()

            ydl_opts = {
                'format': 'bestaudio/best' if audio_only else f'best[height<={resolution[:-1]}]',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
            }

            if audio_only:
                ydl_opts.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status_label.config(text="Download completed!", fg="green")

        except Exception as e:
            self.progress['value'] = 0
            self.status_label.config(text=f"Error: {str(e)}", fg="red")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Calculate percentage
                total_bytes = d.get('total_bytes', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                if total_bytes > 0:
                    percentage = (downloaded_bytes / total_bytes) * 100
                    self.progress['value'] = percentage
                    
                # Update status with speed and ETA
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / 1024 / 1024  # Convert to MB/s
                    eta = d.get('eta', 0)
                    self.status_label.config(
                        text=f"Downloading... {percentage:.1f}% ({speed_mb:.1f} MB/s, ETA: {eta} seconds)"
                    )
                else:
                    self.status_label.config(text=f"Downloading... {percentage:.1f}%")
                
                self.root.update()
            except:
                pass
        elif d['status'] == 'finished':
            self.progress['value'] = 100
            self.status_label.config(text="Processing...")
            self.root.update()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()