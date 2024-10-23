import yt_dlp
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.ydl_opts = {}
        self.title = "Video sin título"

    def show_streams(self, audio_only=False):
        try:
            # Configurar las opciones para mostrar streams
            self.ydl_opts = {
                'format': 'bestaudio' if audio_only else 'best',
                'noplaylist': True,
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.title = info.get('title', 'Video sin título')
                st.write(f"**Título:** {self.title}")
                
                # Recopilar opciones de formato
                formats = info['formats']
                stream_options = []
                for f in formats:
                    format_id = f.get('format_id', 'Desconocido')
                    ext = f.get('ext', 'N/A')
                    resolution = f.get('resolution', 'N/A')
                    vbr = f.get('vbr', 'N/A')
                    format_note = f.get('format_note', 'N/A')
                    stream_options.append(f"{format_id} - {ext} - {resolution} - {format_note} - {vbr}kbps")
                
                choice = st.selectbox(f"Elija una opción para {self.url}:", stream_options)
                
                # Seleccionar el formato elegido
                self.ydl_opts['format'] = formats[stream_options.index(choice)]['format_id']
        
        except Exception as e:
            st.error("Error al obtener los streams del video.")
            st.write(f"Detalles del error: {str(e)}")

    def download(self):
        try:
            # Configurar la descarga usando `yt-dlp`
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url])
                st.success(f"¡Descarga completada para {self.title}!")
        except Exception as e:
            st.error(f"Error durante la descarga de {self.title}: {str(e)}")

def download_videos(urls, audio_only):
    with ThreadPoolExecutor(max_workers=3) as executor:
        for url in urls:
            downloader = YouTubeDownloader(url)
            downloader.show_streams(audio_only=audio_only)
            executor.submit(downloader.download)

if __name__ == "__main__":
    st.title("Descargador de Videos de YouTube Simultáneo")

    # Ingresar hasta 3 URLs
    urls = st.text_area("Ingrese hasta 3 URLs de videos de YouTube, separadas por una nueva línea:").splitlines()
    audio_only = st.checkbox("Descargar solo el audio")

    if st.button("Descargar"):
        valid_urls = [url.strip() for url in urls if url.strip()]
        if len(valid_urls) > 0 and len(valid_urls) <= 3:
            st.info("Iniciando la descarga de los videos...")
            download_videos(valid_urls, audio_only=audio_only)
        else:
            st.warning("Por favor, ingrese entre 1 y 3 URLs.")

