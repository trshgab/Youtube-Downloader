from pytube import YouTube
from moviepy.editor import *
import os

def descargar_video(url, path, on_progress):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        return os.path.join(path, stream.default_filename), None
    except Exception as e:
        return None, str(e)

def convertir_a_mp3(ruta_video, ruta_mp3):
    try:
        video = VideoFileClip(ruta_video)
        video.audio.write_audiofile(ruta_mp3)
    except Exception as e:
        raise e
