from moviepy.editor import AudioFileClip

def convertir_a_mp3(ruta_audio, ruta_mp3):
    print(f"Iniciando conversión a MP3: {ruta_audio}")
    try:
        audio = AudioFileClip(ruta_audio)
        audio.write_audiofile(ruta_mp3, codec='mp3')
        audio.close()
        print(f"Archivo MP3 guardado en: {ruta_mp3}")
    except Exception as e:
        print(f"Error al convertir a MP3: {e}")
        raise e
