import yt_dlp
from app.config.ydl_config import YDL_OPTS, PATH
from app.service.search_download_directory import search_directory


class Downloader:
    def __init__(self, url):
        self.url = url
        self.output_path = PATH
        self.ydl_opts = YDL_OPTS.copy()
        self.ydl_opts["outtmpl"] = f"{self.output_path}/%(title)s.%(ext)s"

    def download(self):
        search_directory()
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(self.url)
