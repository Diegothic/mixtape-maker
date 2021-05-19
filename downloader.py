from __future__ import unicode_literals
import youtube_dl
import os

from youtube_dl.extractor.youtube import YoutubeBaseInfoExtractor

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

def gen_opts(dir):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [hook],
    'outtmpl': '{}/%(title)s.%(ext)s'.format(dir),
    }
    return ydl_opts

def try_downloading(dir, URL):
    opts = gen_opts(dir)
    with youtube_dl.YoutubeDL(opts) as ydl:
        try:
            ydl.download([URL])
        except Exception as e:
            print(type(e).__name__)
            return False
        return True

def validate_url(url):
    if len(url) < 1:
        return False
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if 'Youtube' in str(type(e)):
            if e.suitable(url) and e.IE_NAME != 'generic':
                return True
    return False