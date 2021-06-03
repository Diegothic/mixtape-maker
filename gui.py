from tkinter import *
from constants import *
from custom_widgets import DirectoryEntry, EntryLabel
from custom_widgets import NameEntry
from custom_widgets import SearchEntry
from custom_widgets import DownloadButton
from custom_widgets import Logos
from song_list import SongListScrollbar

class GUI(Tk):
    def __init__(self, app):
        super().__init__()
        self.isFrozen = False

        self.geometry('800x640')
        self.title('Mixtape-Maker')
        self.minsize(600, 480)

        self.app = app

        self.generate_main_frame()
        self.generate_song_list()
        self.generate_entries()
        self.generate_right_panel()

        self.bind_focus(self.frame)
        self.bind_focus(self.right_panel)
        self.bind_focus(self.logos)
        self.bind_focus(self.logos.canvas)
        self.bind_focus(self.logos.credits_frame)

        app.set_song_list(self.song_list)

    def start_window(self):
        self.search_entry.entry.focus()
        self.after(50, self.try_downloading)
        self.mainloop()

    def try_downloading(self):
        if len(self.app.download_queue) > 0:
            if not self.isFrozen:
                self.freeze()
            else:
                app.download_next_in_queue()
        elif self.isFrozen:
            self.unfreeze()
            self.clear_after_downloading()
        self.after(50, self.try_downloading)

    def clear_after_downloading(self):
        self.dir_entry.entry.set_default()
        self.name_entry.entry.set_default()
        self.song_list.set_contents([])
        self.app.songs.clear()
        self.app.dir=''
        self.frame.focus()

    def freeze(self):
        self.isFrozen = True
        self.change_state('disable')

    def unfreeze(self):
        self.isFrozen = False
        self.change_state('normal')

    def change_state(self, new_state):
        children = self.winfo_children()
        for item in children :
            if item.winfo_children() :
                children.extend(item.winfo_children())
        for child in children:
            try:
                child.configure(state=new_state)
            except:
                continue

    def get_directory(self):
        try:
            dir = self.dir_entry.get_dir()
            name = self.name_entry.get_name()
            directory = '{}/{}'.format(dir, name)
        except Exception as e:
            print(e)
            raise RuntimeError('Could not get directory')
        return directory

    def bind_focus(self, widget):
        widget.bind('<1>', lambda event: widget.focus_set())

    def generate_main_frame(self):
        self.frame = Frame(self, height=640, width=480, bg=bg_color)
        self.frame.place(anchor='nw',  relwidth=1, relheight=1)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0, minsize=35)
        self.frame.grid_rowconfigure(0, weight=0, minsize=75)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=0, minsize=150)

    def generate_song_list(self):
        self.list_frame = Frame(self.frame, bg=bg_color)
        self.list_frame.grid(row=1, column=0, sticky='nsew')

        self.song_list = SongListScrollbar(self.list_frame)
        self.song_list.place(anchor='nw', x=35, relwidth=0.7, relheight=1)

    def generate_entries(self):
        self.search_entry = SearchEntry(self.app, self.frame)
        self.search_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, y=35)

        self.search_label = EntryLabel(self.frame, 'Search:')
        self.search_label.place(anchor='sw', x=35, y=35)

        self.dir_entry = DirectoryEntry(self.frame)
        self.dir_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, rely=1, y=-120)

        self.dir_label = EntryLabel(self.frame, 'Directory:')
        self.dir_label.place(anchor='sw', x=35, rely=1, y=-120)

        self.name_entry = NameEntry(self.frame)
        self.name_entry.place(anchor='nw', relwidth=0.7, height=30, x=35, rely=1, y=-60)

        self.name_label = EntryLabel(self.frame, 'Name:')
        self.name_label.place(anchor='sw', x=35, rely=1, y=-60)

    def generate_right_panel(self):
        self.right_panel = Frame(self.frame, bg=bg_color)
        self.right_panel.place(anchor='nw', relwidth=0.24, relx=0.76, relheight=1)

        self.download_button = DownloadButton(self.app, self, self.right_panel)
        self.download_button.place(anchor='nw', rely=1, y=-120, height=90, relwidth=0.9)

        self.logos = Logos(self.right_panel)
        self.logos.place(anchor='nw', y=35, relwidth=0.9, relheight=0.7)