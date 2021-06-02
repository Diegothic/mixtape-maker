from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from constants import *

class SongList(ttk.Treeview):
    def __init__(self, master, mode='extended'):
        super().__init__(master, show='tree', padding=[-22,0,0,0], selectmode=mode)
        self['columns'] = ('Title', 'Duration')
        self.column('#0', anchor='w', width=181, stretch=0)
        self.column('Title', anchor='center', width=120)
        self.column('Duration', anchor='center', width=100, stretch=0)
        self.grid(row=0, column=0, sticky='nsew')

        self.images = []
        self.songs = []

        self.style = ttk.Style()
        self.style.configure('Treeview', rowheight=90)

    def set_contents(self, songs):
        self.images.clear()
        self.songs.clear()
        for item in self.get_children():
            self.delete(item)
        counter = 0
        self.songs = songs
        for song in self.songs:
            th = ImageTk.PhotoImage(song.thumbnail)
            self.images.append(th)
            self.insert(parent='', index='end', iid=counter, text='', 
                            image=self.images[counter],
                            values=(song.title, song.duration))
            counter += 1



class SongListScrollbar(Frame):
    def __init__(self, master):
        super().__init__(master, bg=entry_color)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.tree = SongList(self)
        self.tree.grid(row=0, column=0, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')

        self.tree.configure(yscrollcommand=self.scrollbar.set)

    def set_contents(self, songs):
        self.tree.set_contents(songs)



class SearchResults(Canvas):
    def __init__(self, appdata, parent, master):
        super().__init__(master, bg=entry_color, highlightbackground=dark_color)
        self.list = SongList(self, 'browse')
        self.list.place(anchor='nw', relwidth=1, relheight=1)

        self.appdata = appdata
        self.parent = parent
        
        self.list.bind('<Double-1>', self.get_selected_item)
        self.list.bind('<Return>', self.get_selected_item)
        self.list.bind('<Escape>', self.parent.on_escape)

    def show(self):
        self.place(x=35, y=65, relwidth=0.7, height=275)

    def hide(self):
        self.place_forget()

    def set_contents(self, songs):
        self.list.set_contents(songs)

    def get_selected_item(self, event):
        try:
            item = int(self.list.selection()[0])
            self.appdata.add_song(self.list.songs[item])
            print(self.list.songs[item].id)
            self.parent.hide_results()
            self.parent.escape()
        except:
            print('No item selected')

    def focus_on_list(self):
        try:
            self.list.selection_set(0)
            self.list.focus_set()
            self.list.focus(0)
        except:
            print('No items to focus')

