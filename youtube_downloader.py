from pytube import YouTube, Playlist
import os
from converter import convertir_a_mp3

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

def descargar_playlist(url, path, on_progress, format):
    print(f"Iniciando descarga de playlist: {url}")
    try:
        pl = Playlist(url)
        for video in pl.videos:
            if format == "mp4":
                ruta_video, error = descargar_video(video.watch_url, path, on_progress)
                if not ruta_video:
                    print(f"Error al descargar el video: {error}")
            elif format == "mp3":
                ruta_audio, error = descargar_audio(video.watch_url, path, on_progress)
                if not ruta_audio:
                    print(f"Error al descargar el audio: {error}")
                else:
                    nombre_archivo_mp3 = os.path.splitext(os.path.basename(ruta_audio))[0] + '.mp3'
                    ruta_mp3 = os.path.join(path, nombre_archivo_mp3)
                    convertir_a_mp3(ruta_audio, ruta_mp3)
                    os.remove(ruta_audio)  # Eliminar archivo de audio temporal
        return True, None
    except Exception as e:
        print(f"Error al descargar la playlist: {e}")
        return False, str(e)
