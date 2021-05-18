from __future__ import unicode_literals
import youtube_dl
import os

class Logger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting...')

download_path = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [hook],
    'outtmpl': '{}/%(title)s.%(ext)s'.format(download_path),
}

def try_downloading(URL):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([URL])
        except Exception as e:
            print(type(e).__name__)
            return False
        return True