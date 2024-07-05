# YouTube Downloader

**Versión:** 1.1.0-rc

## Descripción

YouTube Downloader es una aplicación sencilla y eficiente para descargar videos y audios de YouTube. Permite seleccionar el formato de descarga (MP4 o MP3) y gestionar las descargas de manera intuitiva, con una interfaz gráfica atractiva y fácil de usar.

## Características

- **Descarga de Videos**: Descarga videos de YouTube en formato MP4 *(solo 360p disponible por ahora)*.
- **Descarga de Audios**: Extrae y descarga solo el audio de los videos de YouTube en formato MP3.
- **Descarga de Playlists**: Descarga playlists enteras de YouTube en formato MP4 o MP3.
- **Modo Oscuro**: Interfaz con modo oscuro para una experiencia de usuario más agradable.
- **Validación de URL**: Verifica que las URLs ingresadas sean válidas.
- **Barra de Progreso**: Muestra el progreso de la descarga con un porcentaje dentro de la barra.
- **Configuración de Carpeta de Descarga**: Permite configurar la carpeta de descarga y la guarda para futuras descargas.
- **Velocidad de Descarga**: Muestra la velocidad de descarga si está habilitada en el menú de configuración.
- **Manejo de Errores Mejorado**: Mejora la gestión de errores para una experiencia más robusta.

## Requisitos

- Python 3.6 o superior
- Librerías: `pytube`, `moviepy`, `tkinter`, `ttkbootstrap`

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/trshgab/Youtube-Downloader.git
    cd youtube-downloader
    ```

2. Instala las dependencias:
    ```bash
    pip install pytube moviepy ttkbootstrap
    ```

## Uso

1. Ejecuta el programa:
    ```bash
    python3 gui_youtube_downloader.py
    ```

2. Ingresa la URL del video de YouTube que deseas descargar.

3. Selecciona el formato de descarga (MP4 o MP3).

4. Haz clic en "Descargar" y selecciona la carpeta donde deseas guardar el archivo si no la has configurado previamente.


## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto
  
Email: gmrgabo@gmail.com

---

¡Gracias por usar YouTube Downloader! Espero que te sea útil.