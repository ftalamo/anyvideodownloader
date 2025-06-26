from vimeo_downloader import Vimeo
from app.config.ydl_config import PATH


class VimeoD:
    def __init__(self, url):
        self.url = url
        self.path = PATH

    def vmo_download(self):
        try:
            print(f"Descargando desde URL: {self.url}")
            v = Vimeo(self.url)

            if not v.metadata:
                print("No se pudo obtener metadata del video.")
                return

            title = v.metadata.title
            print(f"Título del video: {title}")

            best_stream = v.best_stream
            if not best_stream:
                print("No se encontró un stream descargable.")
                return

            print(f"Iniciando descarga en {self.path}")
            best_stream.download(download_directory=self.path, filename=f"{title}.mp4")
            print("Descarga completada.")

        except Exception as e:
            print(f"❌ Error al descargar el video de Vimeo: {e}")
