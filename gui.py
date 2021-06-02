import tkinter as tk
import downloader as dl
from constants import *
from custom_widgets import DirectoryEntry, EntryLabel
from custom_widgets import NameEntry
from custom_widgets import SearchEntry
from custom_widgets import DownloadButton
from custom_widgets import Logos
from song_list import SongListScrollbar

class Application():
    def __init__(self):
        self.songs = {}

    def add_song(self, song):
        self.songs[song.id] = song
        values_list = list(self.songs.values())
        self.song_list.set_contents(values_list)

    def set_song_list(self, song_list):
        self.song_list = song_list

    def download_songs(self):
        try:
            directory = '{}/{}'.format(dir_entry.get_dir(), name_entry.get_name())
        except Exception as e:
            print(e)
            return
        print(directory)
        songIDs = self.songs.keys()
        for id in songIDs:
            print(id)
            self.download(directory, id)

    def download(self, dir, url):
        dl.try_downloading(dir, url)

app = Application()

songlist = []

root = tk.Tk()
root.geometry('800x640')
root.title('Mixtape-Maker')
root.minsize(600, 480)

frame = tk.Frame(root, height=640, width=480, bg=bg_color)
frame.place(anchor='nw',  relwidth=1, relheight=1)
frame.bind('<1>', lambda event: frame.focus_set())

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=0, minsize=35)
frame.grid_rowconfigure(0, weight=0, minsize=75)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=0, minsize=150)


list_frame = tk.Frame(frame, bg=bg_color)
list_frame.grid(row=1, column=0, sticky='nsew')

song_list = SongListScrollbar(list_frame)
song_list.place(anchor='nw', x=35, relwidth=0.7, relheight=1)

search_entry = SearchEntry(app, frame)
search_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, y=35)
search_label = EntryLabel(frame, 'Search:')
search_label.place(anchor='sw', x=35, y=35)

app.set_song_list(song_list)

dir_entry = DirectoryEntry(frame)
dir_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, rely=1, y=-120)
dir_label = EntryLabel(frame, 'Directory:')
dir_label.place(anchor='sw', x=35, rely=1, y=-120)

name_entry = NameEntry(frame)
name_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, rely=1, y=-60)
name_label = EntryLabel(frame, 'Name:')
name_label.place(anchor='sw', x=35, rely=1, y=-60)

right_panel = tk.Frame(frame, bg=bg_color)
right_panel.place(anchor='nw', relwidth=0.24, relx=0.76, relheight=1)

download_button = DownloadButton(app, right_panel)
download_button.place(anchor='nw', rely=1, y=-120, height=90, relwidth=0.9)

logos = Logos(right_panel)
logos.place(anchor='nw', y=35, relwidth=0.9, relheight=0.7)


search_entry.entry.focus()

def start_window():
    root.mainloop()

def main():
    start_window()

if __name__ == '__main__':
    main()