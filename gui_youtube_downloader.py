import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from youtube_downloader import descargar_video, convertir_a_mp3
from pytube import request
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Settings:
    def __init__(self):
        self.download_folder = os.path.expanduser("~")
        self.show_speed = False

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.style = ttk.Style('cosmo')  # Tema inicial, cambiará con modo oscuro

        self.settings = Settings()  # Instancia de las configuraciones

        # Configuración de la ventana principal
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill='both', expand=True)

        self.url_label = ttk.Label(self.main_frame, text="URL de YouTube:")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.pack(pady=5)

        self.format_label = ttk.Label(self.main_frame, text="Selecciona el formato:")
        self.format_label.pack(pady=5)

        self.format_var = tk.StringVar(value="mp4")
        self.mp4_radio = ttk.Radiobutton(self.main_frame, text="MP4", variable=self.format_var, value="mp4")
        self.mp4_radio.pack(pady=5)

        self.mp3_radio = ttk.Radiobutton(self.main_frame, text="MP3", variable=self.format_var, value="mp3")
        self.mp3_radio.pack(pady=5)

        self.download_button = ttk.Button(self.main_frame, text="Descargar", command=self.start_download, bootstyle=SUCCESS)
        self.download_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.speed_label = ttk.Label(self.main_frame, text="", bootstyle=INFO)
        self.speed_label.pack(pady=5)

        # Botón de modo oscuro
        self.dark_mode_button = ttk.Button(self.main_frame, text="Modo Oscuro", command=self.toggle_dark_mode, bootstyle=INFO)
        self.dark_mode_button.pack(pady=5)

        # Botón para el menú de opciones
        self.settings_button = ttk.Button(self.main_frame, text="Opciones", command=self.open_settings, bootstyle=PRIMARY)
        self.settings_button.pack(pady=5)

    def start_download(self):
        threading.Thread(target=self.download).start()

    def download(self):
        url = self.url_entry.get()
        format = self.format_var.get()

        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL de YouTube.")
            return

        download_path = self.settings.download_folder
        if not download_path:
            return

        self.progress['value'] = 0
        self.root.update_idletasks()

        ruta_video, error = descargar_video(url, download_path, self.on_progress)
        
        if not ruta_video:
            messagebox.showerror("Error", f"Error al descargar el video: {error}")
            return

        if format == "mp3":
            try:
                nombre_archivo_mp3 = os.path.splitext(os.path.basename(ruta_video))[0] + '.mp3'
                ruta_mp3 = os.path.join(download_path, nombre_archivo_mp3)
                convertir_a_mp3(ruta_video, ruta_mp3)
                messagebox.showinfo("Éxito", f"Descarga completada: {ruta_mp3}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al convertir a MP3: {e}")
        else:
            messagebox.showinfo("Éxito", f"Descarga completada: {ruta_video}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress['value'] = percentage
        self.root.update_idletasks()

        if self.settings.show_speed:
            speed = bytes_downloaded / (request.time.time() - stream._start_time)
            speed_text = f"Velocidad de descarga: {speed / 1024:.2f} KB/s"
            self.speed_label.config(text=speed_text)

    def toggle_dark_mode(self):
        if self.style.theme_use() == 'cosmo':
            self.style.theme_use('darkly')
        else:
            self.style.theme_use('cosmo')

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Opciones")
        settings_window.geometry("400x300")

        ttk.Label(settings_window, text="Carpeta de descargas:").pack(pady=10)
        self.download_folder_var = tk.StringVar(value=self.settings.download_folder)
        download_folder_entry = ttk.Entry(settings_window, textvariable=self.download_folder_var, width=40)
        download_folder_entry.pack(pady=5)

        ttk.Button(settings_window, text="Seleccionar carpeta", command=self.select_download_folder).pack(pady=5)

        self.show_speed_var = tk.BooleanVar(value=self.settings.show_speed)
        show_speed_check = ttk.Checkbutton(settings_window, text="Mostrar velocidad de descarga", variable=self.show_speed_var)
        show_speed_check.pack(pady=10)

        ttk.Button(settings_window, text="Guardar", command=self.save_settings, bootstyle=SUCCESS).pack(pady=20)

    def select_download_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder_var.set(folder)

    def save_settings(self):
        self.settings.download_folder = self.download_folder_var.get()
        self.settings.show_speed = self.show_speed_var.get()
        messagebox.showinfo("Opciones", "Configuraciones guardadas correctamente.")

if __name__ == "__main__":
    root = ttk.Window(themename='cosmo')
    app = YouTubeDownloaderApp(root)
    root.mainloop()
