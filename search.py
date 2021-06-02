from youtubesearchpython import VideosSearch
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
from youtubesearchpython import VideosSearch

class Song():
    def __init__(self, id, title, thumbnail, duration):
        self.id=id
        self.title=title
        self.thumbnail=thumbnail
        self.duration=duration

class Search():
    def __init__(self):
        pass

    def search(self, phrase, amount):
        videosSearch = VideosSearch(phrase, limit = amount)
        songs = []
        for result in videosSearch.result()['result']:
            id = result['id']
            title = result['title']
            thumbnail = self.url_to_img(result['thumbnails'][0]['url'])
            duration = result['duration']
            song = Song(id, title, thumbnail, duration)
            songs.append(song)
        return songs

    def url_to_img(self, url):
        raw_data = urlopen(url).read()
        im = Image.open(BytesIO(raw_data))
        size = 160, 90
        im.thumbnail(size, Image.ANTIALIAS)
        return im