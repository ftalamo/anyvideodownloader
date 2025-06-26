YDL_OPTS = {
    "format": "best[ext=mp4]",
    "outtmpl": "%(title)s.%(ext)s",  # ruta relativa o la que prefieras
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    },
    "nocheckcertificate": False,
}

YDL_OPTS_TIKTOK= {
    "format": "best[ext=mp4]",
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "nocheckcertificate": False,
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.tiktok.com/",
        "Origin": "https://www.tiktok.com"
    }
}

PATH = "./Content_download"