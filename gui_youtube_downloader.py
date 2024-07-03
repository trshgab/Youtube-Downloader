import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from converter import convertir_a_mp3

class Settings:
    def __init__(self):
        self.download_folder = None

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.style = ttk.Style('cosmo')

        self.settings = Settings()

        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill='both', expand=True)

        self.url_label = ttk.Label(self.main_frame, text="URL de YouTube (Video o Playlist):")
        self.url_label.pack(pady=5)

        self.url_entry = ttk.Entry(self.main_frame, width=50)
        self.url_entry.pack(pady=5)

        self.paste_button = ttk.Button(self.main_frame, text="Pegar", command=self.paste_from_clipboard)
        self.paste_button.pack(pady=5)

        self.format_label = ttk.Label(self.main_frame, text="Selecciona el formato:")
        self.format_label.pack(pady=5)

        self.format_var = tk.StringVar(value="mp4")
        self.mp4_radio = ttk.Radiobutton(self.main_frame, text="MP4", variable=self.format_var, value="mp4")
        self.mp4_radio.pack(pady=5)

        self.mp3_radio = ttk.Radiobutton(self.main_frame, text="MP3", variable=self.format_var, value="mp3")
        self.mp3_radio.pack(pady=5)

        self.download_button = ttk.Button(self.main_frame, text="Descargar", command=self.download_action, style="success.TButton")
        self.download_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = ttk.Label(self.main_frame, text="", style="info.TLabel")
        self.progress_label.pack(pady=5)

        self.info_text = tk.Text(self.main_frame, height=10, width=60, wrap="word")
        self.info_text.pack(pady=10)

        self.dark_mode_button = ttk.Button(self.main_frame, text="Modo Oscuro", command=self.toggle_dark_mode, style="info.TButton")
        self.dark_mode_button.pack(pady=5)

        self.downloading = False

    def paste_from_clipboard(self):
        """ Pega el contenido del portapapeles en el campo URL """
        clipboard_content = self.root.clipboard_get()
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, clipboard_content)

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

        try:
            is_playlist = True if Playlist(url) else False
        except:
            is_playlist = False

        if is_playlist:
            success, error = self.descargar_playlist(url, download_path, format)
            if not success:
                self.show_error(f"Error al descargar la playlist: {error}")
                self.downloading = False
                return
            self.show_info("Descarga de playlist completada")
        else:
            if format == "mp3":
                ruta_audio, error = self.descargar_audio(url, download_path)
                if not ruta_audio:
                    self.show_error(f"Error al descargar el audio: {error}")
                    self.downloading = False
                    return
                try:
                    nombre_archivo_mp3 = os.path.splitext(os.path.basename(ruta_audio))[0] + '.mp3'
                    ruta_mp3 = self.avoid_overwrite(download_path, nombre_archivo_mp3)
                    convertir_a_mp3(ruta_audio, ruta_mp3)
                    self.show_info(f"Descarga completada: {ruta_mp3}")
                    self.log_message(f"Archivo MP3 convertido: {ruta_mp3}")
                    os.remove(ruta_audio)  # Eliminar archivo de audio temporal
                except Exception as e:
                    self.show_error(f"Error al convertir a MP3: {e}")
                    self.log_message(f"Error al convertir a MP3: {e}")
            elif format == "mp4":
                ruta_video, error = self.descargar_video(url, download_path)
                if not ruta_video:
                    self.show_error(f"Error al descargar el video: {error}")
                    self.downloading = False
                    return
                try:
                    nombre_archivo_mp4 = os.path.basename(ruta_video)
                    ruta_mp4 = self.avoid_overwrite(download_path, nombre_archivo_mp4)
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

    def avoid_overwrite(self, path, filename):
        """ Evita sobrescribir archivos añadiendo un sufijo numérico si es necesario """
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(path, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        return os.path.join(path, new_filename)

    def descargar_audio(self, url, path):
        """ Descarga el audio de YouTube """
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_path=path)
            ruta_audio = os.path.join(path, stream.default_filename)
            return ruta_audio, None
        except Exception as e:
            return None, str(e)

    def descargar_video(self, url, path):
        """ Descarga el video de YouTube """
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=path)
            ruta_video = os.path.join(path, stream.default_filename)
            return ruta_video, None
        except Exception as e:
            return None, str(e)

    def descargar_playlist(self, url, path, format):
        """ Descarga todos los videos de una playlist de YouTube """
        try:
            pl = Playlist(url)
            total_videos = len(pl.video_urls)
            videos_descargados = 0
            for index, video in enumerate(pl.video_urls, start=1):
                if format == "mp3":
                    ruta_audio, error = self.descargar_audio(video, path)
                    if ruta_audio:
                        nombre_archivo_mp3 = os.path.splitext(os.path.basename(ruta_audio))[0] + '.mp3'
                        ruta_mp3 = self.avoid_overwrite(path, nombre_archivo_mp3)
                        convertir_a_mp3(ruta_audio, ruta_mp3)
                        os.remove(ruta_audio)  # Eliminar archivo de audio temporal
                        videos_descargados += 1
                elif format == "mp4":
                    ruta_video, error = self.descargar_video(video, path)
                    if not ruta_video:
                        return False, error
                    nombre_archivo_mp4 = os.path.basename(ruta_video)
                    ruta_mp4 = self.avoid_overwrite(path, nombre_archivo_mp4)
                    shutil.move(ruta_video, ruta_mp4)
                    videos_descargados += 1
                self.on_progress(videos_descargados, total_videos)
            return True, None
        except Exception as e:
            return False, str(e)

    def on_progress(self, videos_descargados, total_videos):
        """ Actualiza la barra de progreso y muestra el progreso en el log """
        progress_percent = (videos_descargados / total_videos) * 100
        self.progress['value'] = progress_percent
        self.progress_label.config(text=f"{videos_descargados}/{total_videos} videos descargados")
        self.root.update_idletasks()

    def select_download_folder(self):
        """ Abre un diálogo para seleccionar la carpeta de descarga """
        download_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Selecciona una carpeta de descargas")
        if download_path:
            self.settings.download_folder = download_path
            self.log_message(f"Carpeta de descarga seleccionada: {download_path}")
        return download_path

    def show_info(self, message):
        """ Muestra un cuadro de mensaje informativo """
        messagebox.showinfo("Información", message)

    def show_error(self, message):
        """ Muestra un cuadro de mensaje de error """
        messagebox.showerror("Error", message)

    def log_message(self, message):
        """ Muestra un mensaje en el área de texto de información """
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)
        self.root.update_idletasks()

    def toggle_dark_mode(self):
        """ Cambia entre temas claro y oscuro """
        current_theme = self.style.theme_use()
        new_theme = 'superhero' if current_theme != 'superhero' else 'cosmo'
        self.style.theme_use(new_theme)
        self.log_message(f"Tema cambiado a: {new_theme}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
