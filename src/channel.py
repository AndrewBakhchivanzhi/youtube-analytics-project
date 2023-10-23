import os
import json
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = Channel.get_service().channels().list(
            id=channel_id, part='snippet,contentDetails,statistics').execute()
        self.id = self.channel['items'][0]['id'] # id канала
        self.title = self.channel['items'][0]['snippet']['title'] # название канала
        self.description = self.channel['items'][0]['snippet']['description'] # описание канала
        self.url = f"https://www.youtube.com/channel/{self.channel_id}" # ссылка на канал
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount'] # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount'] # количество видео
        self.view_count = self.channel['items'][0]['statistics']['viewCount'] # общее количество просмотров
        self.attributes = [{'id':self.id, 'titlte':self.title, 'description':self.description,
                            'url':self.url, 'subscriber_count':self.subscriber_count,
                            'video_count':self.video_count, 'view_count':self.view_count}]

    def __str__(self):
        return f"{self.title} {self.url}"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel,indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, moscowpython:dict) -> None:
        with open(moscowpython, "a") as f:
            if os.stat(moscowpython).st_size == 0:
                json.dump([self.attributes], f, indent=2, ensure_ascii=False)
            else:
                with open(moscowpython) as json_file:
                    data_list = json.load(json_file)
                data_list.append(self.attributes)
                with open(moscowpython, "w") as json_file:
                    json.dump(data_list, json_file, indent=2, ensure_ascii=False)
