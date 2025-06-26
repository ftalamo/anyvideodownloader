import requests
import re
import os

class InstagramStoryDownloader:
    def __init__(self, sessionid, ds_user_id, csrftoken):
        self.cookies = {
            'sessionid': sessionid,
            'ds_user_id': ds_user_id,
            'csrftoken': csrftoken
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.instagram.com/",
            "X-IG-App-ID": "936619743392459"
        }

    def extract_user_from_url(self, url):
        match = re.search(r"instagram\.com/([^/?#]+)", url)
        return match.group(1) if match else None

    def extract_id_from_story_url(self, url):
        match = re.search(r"stories/([^/]+)/(\d+)", url)
        return match.groups() if match else (None, None)

    def get_user_id(self, username):
        url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        r.raise_for_status()
        data = r.json()
        return data['graphql']['user']['id']

    def get_stories(self, user_id):
        url = f"https://i.instagram.com/api/v1/feed/user/{user_id}/story/"
        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        r.raise_for_status()
        return r.json()

    def download_stories(self, media_json, output_folder="stories_downloaded"):
        os.makedirs(output_folder, exist_ok=True)
        items = media_json.get("reel", {}).get("items", [])
        for item in items:
            media_type = item["media_type"]
            if media_type == 1:
                url = item["image_versions2"]["candidates"][0]["url"]
                ext = ".jpg"
            elif media_type == 2:
                url = item["video_versions"][0]["url"]
                ext = ".mp4"
            else:
                continue
            filename = f"{item['id']}{ext}"
            path = os.path.join(output_folder, filename)
            with open(path, "wb") as f:
                f.write(requests.get(url).content)
            print(f"✅ Descargado: {filename}")
