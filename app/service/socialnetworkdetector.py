import re

def detectar_red_social(url: str) -> str:
    url = url.lower()

    if "tiktok.com" in url:
        return "tiktok"

    if "instagram.com" in url:
        if re.search(r"stories?/", url):
            return "instagram_story"
        elif re.search(r"reel/|p/", url):
            return "instagram_post_or_reel"
        else:
            return "instagram"
    if "tiktok.com" in url:
        return "tiktok"
    if "facebook.com" in url:
        return "facebook"

    if "twitter.com" in url or "x.com" in url:
        return "twitter"

    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"

    return "otro"