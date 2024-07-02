from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def descargar_video(url, path, on_progress):
    print(f"Iniciando descarga de video: {url}")
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.get_highest_resolution()
        print(f"Stream seleccionado: {stream}")
        stream.download(output_path=path)
        ruta_video = os.path.join(path, stream.default_filename)
        print(f"Video descargado en: {ruta_video}")
        return ruta_video, None
    except Exception as e:
        print(f"Error al descargar el video: {e}")
        return None, str(e)

def descargar_audio(url, path, on_progress):
    print(f"Iniciando descarga de audio: {url}")
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(only_audio=True).first()
        print(f"Stream seleccionado: {stream}")
        stream.download(output_path=path)
        ruta_audio = os.path.join(path, stream.default_filename)
        print(f"Audio descargado en: {ruta_audio}")
        return ruta_audio, None
    except Exception as e:
        print(f"Error al descargar el audio: {e}")
        return None, str(e)

def convertir_a_mp3(ruta_audio, ruta_mp3):
    print(f"Iniciando conversión a MP3: {ruta_audio}")
    try:
        audio = AudioFileClip(ruta_audio)
        audio.write_audiofile(ruta_mp3)
        audio.close()
        print(f"Archivo MP3 guardado en: {ruta_mp3}")
    except Exception as e:
        print(f"Error al convertir a MP3: {e}")
        raise e

