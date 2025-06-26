import yt_dlp
from app.config.ydl_config import YDL_OPTS, YDL_OPTS_TIKTOK, PATH
from app.service.search_download_directory import search_directory


class Downloader:
    def __init__(self, url, social):
        self.url = url
        self.social = social
        self.output_path = PATH
        self.ydl_opts = YDL_OPTS.copy()
        self.tiktok_opts = YDL_OPTS_TIKTOK.copy()
        self.ydl_opts["outtmpl"] = f"{self.output_path}/%(title)s.%(ext)s"

    def download(self):
        search_directory()
        if self.social =="tiktok.com":
            with yt_dlp.YoutubeDL(self.tiktok_opts) as ydl:
                ydl.download(self.url)
        else:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download(self.url)
