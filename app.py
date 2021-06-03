import downloader as dl

class Application():
    def __init__(self):
        self.songs = {}
        self.download_queue = []
        self.dir = ''

    def set_song_list(self, song_list):
        self.song_list = song_list

    def add_song(self, song):
        self.songs[song.id] = song
        values_list = list(self.songs.values())
        self.song_list.set_contents(values_list)

    def download_songs(self, dir):
        print(dir)
        self.dir = dir
        songIDs = self.songs.keys()
        self.download_queue = list(songIDs)

    def download_next_in_queue(self):
        song = self.download_queue.pop()
        self.download(song)

    def download(self, url):
        dl.try_downloading(self.dir, url)