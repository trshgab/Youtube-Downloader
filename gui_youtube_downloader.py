import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from youtube_downloader import descargar_video, convertir_a_mp3, descargar_audio
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Settings:
    def __init__(self):
        self.download_folder = None  # Inicialmente no hay carpeta seleccionada

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

        self.download_button = ttk.Button(self.main_frame, text="Descargar", command=self.download_action, bootstyle=SUCCESS)
        self.download_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = ttk.Label(self.main_frame, text="", bootstyle=INFO)
        self.progress_label.pack(pady=5)

        # Área de texto para mostrar mensajes de progreso
        self.info_text = tk.Text(self.main_frame, height=10, width=60, wrap="word")
        self.info_text.pack(pady=10)

        # Botón de modo oscuro
        self.dark_mode_button = ttk.Button(self.main_frame, text="Modo Oscuro", command=self.toggle_dark_mode, bootstyle=INFO)
        self.dark_mode_button.pack(pady=5)

        # Variables para control de visibilidad
        self.downloading = False  # Indica si se está descargando actualmente

    def download_action(self):
        if self.downloading:
            messagebox.showinfo("Información", "Ya se está realizando una descarga.")
            return

        threading.Thread(target=self.download).start()

    def download(self):
        self.downloading = True
        url = self.url_entry.get()
        format = self.format_var.get()

        self.log_message(f"URL ingresada: {url}")
        self.log_message(f"Formato seleccionado: {format}")

        if not url:
            self.show_error("Por favor, ingresa una URL de YouTube.")
            self.downloading = False
            return

        download_path = self.settings.download_folder
        if not download_path:
            download_path = self.select_download_folder()

        self.log_message(f"Carpeta de descarga: {download_path}")

        if not download_path:
            self.show_error("Selecciona una carpeta de descargas.")
            self.downloading = False
            return

        self.progress['value'] = 0
        self.progress_label.config(text="Inicializando descarga...")
        self.root.update_idletasks()

        if format == "mp3":
            ruta_audio, error = descargar_audio(url, download_path, self.on_progress)
            if not ruta_audio:
                self.show_error(f"Error al descargar el audio: {error}")
                self.downloading = False
                return
            nombre_archivo_mp3 = os.path.splitext(os.path.basename(ruta_audio))[0] + '.mp3'
            ruta_mp3 = os.path.join(download_path, nombre_archivo_mp3)
            try:
                convertir_a_mp3(ruta_audio, ruta_mp3)
                self.show_info(f"Descarga completada: {ruta_mp3}")
                self.log_message(f"Archivo MP3 convertido: {ruta_mp3}")
                os.remove(ruta_audio)  # Eliminar archivo de audio temporal
            except Exception as e:
                self.show_error(f"Error al convertir a MP3: {e}")
                self.log_message(f"Error al convertir a MP3: {e}")
        elif format == "mp4":
            ruta_video, error = descargar_video(url, download_path, self.on_progress)
            if not ruta_video:
                self.show_error(f"Error al descargar el video: {error}")
                self.downloading = False
                return

            nombre_archivo_mp4 = os.path.basename(ruta_video)
            ruta_mp4 = os.path.join(download_path, nombre_archivo_mp4)

            try:
                shutil.move(ruta_video, ruta_mp4)
                self.show_info(f"Descarga completada: {ruta_mp4}")
                self.log_message(f"Archivo MP4 movido: {ruta_mp4}")
            except Exception as e:
                self.show_error(f"Error al mover el archivo: {e}")
                self.log_message(f"Error al mover el archivo: {e}")

        self.progress_label.config(text="")
        self.progress['value'] = 0
        self.root.update_idletasks()
        self.downloading = False

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress['value'] = percentage
        self.progress_label.config(text=f"Descargando: {bytes_downloaded // 1024} KB de {total_size // 1024} KB ({percentage:.1f}%)")
        self.log_message(f"Progreso: {percentage:.1f}% - {bytes_downloaded // 1024} KB de {total_size // 1024} KB")

        # Mostrar mensajes en el área de texto
        message = f"Progreso: {percentage:.1f}% - {bytes_downloaded // 1024} KB de {total_size // 1024} KB\n"
        self.info_text.insert(tk.END, message)
        self.info_text.see(tk.END)  # Hacer scroll hacia abajo automáticamente

        self.root.update_idletasks()

    def toggle_dark_mode(self):
        current_theme = self.style.theme_use()
        self.log_message(f"Tema actual: {current_theme}")
        if current_theme == 'cosmo':
            self.style.theme_use('darkly')
            self.log_message("Modo oscuro activado")
        else:
            self.style.theme_use('cosmo')
            self.log_message("Modo claro activado")

    def select_download_folder(self):
        folder = filedialog.askdirectory()
        self.log_message(f"Carpeta seleccionada: {folder}")
        if folder:
            self.settings.download_folder = folder
        return folder

    def log_message(self, message):
        print(message)
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)  # Hacer scroll hacia abajo automáticamente

    def show_info(self, message):
        messagebox.showinfo("Información", message)
        self.log_message(message)

    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.log_message(f"Error: {message}")

if __name__ == "__main__":
    root = ttk.Window(themename='cosmo')
    app = YouTubeDownloaderApp(root)
    root.mainloop()
