import os
from googleapiclient.discovery import build

class Video:
    def __init__(self, video_id: str, title=None, url=None, view_count=None, view_like=None) -> None:
        youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        request = youtube.videos().list(part='snippet, statistics', id=video_id)
        response = request.execute()
        item = response['items'][0]
        self.video_id = video_id
        self.title = item['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.view_count = item['statistics'].get('viewCount', 0)
        self.view_like = item['statistics'].get('likeCount', 0)


    def __str__(self):
        return self.title

class PLVideo(Video):
    def __init__(self, video_id, playlist_id, title=None, url=None, view_count=None, view_like=None):
        super().__init__(video_id, title, url, view_count, view_like)
        self.playlist_id = playlist_id


