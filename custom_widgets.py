from tkinter import *
import tkinter.filedialog
from constants import *
from song_list import SearchResults
from search import Search

class PlaceholderEntry(Entry):
    def __init__(self, master, placeholder_text):
        super().__init__(master, fg=text_dark_color, insertbackground=text_color,
                            font=(app_font, 12), bg = entry_color, bd=0)
        self.bind('<FocusIn>', self.on_focus)
        self.bind('<FocusOut>', self.on_unfocus)
        self.placeholder = placeholder_text
        self.insert('0', self.placeholder)

    def on_focus(self, event):
        if self.get() == self.placeholder:
            self.delete('0', 'end')
            self.config(fg=text_color)

    def on_unfocus(self, event):
        if len(self.get()) < 1:
            self.config(fg=text_dark_color)
            self.insert('0', self.placeholder)

    def set_text(self, text):
        self.delete('0', 'end')
        if len(text) > 0:
            self.config(fg=text_color)
            self.insert('0', text)
        else:
            self.config(fg=text_dark_color)
            self.insert('0', self.placeholder)

    def is_empty(self):
        content = self.get()
        return content == self.placeholder or len(content) == 0


class EntryLabel(Label):
    def __init__(self, master, text):
        super().__init__(master, fg=text_color, bg = bg_color, font=(app_font, 8), text=text)


class DirectoryEntry(Frame):
    def __init__(self, master):
        super().__init__(master, bg=entry_color)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.entry = PlaceholderEntry(self, 'Enter a directory, new folder inside will be created...')
        self.entry.grid(row=0, column=0, sticky='nsew', padx=10)

        self.button_frame = Frame(self, width=30)
        self.button_frame.grid(row=0, column=1, sticky='nsew')
        self.button = Button(self.button_frame, font=(app_font, 14), text='...', 
                        bg=dark_color, fg=text_color, bd=0, command=self.choose_dir)
        self.button.place(anchor='nw', relwidth=1, relheight=1)

    def choose_dir(self):
        directory = tkinter.filedialog.askdirectory(initialdir=program_dir, title='Select Directory')
        if(len(directory) > 0):
            self.entry.set_text(directory)

    def is_valid(self):
        dir = self.entry.get()

    def get_dir(self):
        dir = self.entry.get()
        if self.entry.is_empty():
            raise RuntimeError('Directory is empty')
        return self.entry.get()


class NameEntry(Frame):
    def __init__(self, master):
        super().__init__(master, bg=entry_color)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.entry = PlaceholderEntry(self, 'Name your mixtape...')
        self.entry.grid(row=0, column=0, sticky='nsew', padx=10)

    def get_name(self):
        if self.entry.is_empty():
            raise RuntimeError('Name is empty')
        return self.entry.get()

class SearchEntry(Frame):
    def __init__(self, app, master):
        super().__init__(master, bg=entry_color)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.entry = PlaceholderEntry(self, 'Search for songs...')
        self.entry.grid(row=0, column=0, sticky='nsew', padx=10)
        self.entry.bind('<FocusOut>', self.on_unfocus)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Escape>', self.on_escape)

        self.results = SearchResults(app, self, master)
        self.songs_found = []

        self.button_frame = Frame(self, width=30)
        self.button_frame.grid(row=0, column=1, sticky='nsew')
        self.img = PhotoImage(data=mg_imgdata)
        self.img_dark = PhotoImage(data=mg_dark_imgdata)
        self.button = Button(self.button_frame, text='Search', image=self.img,
                        bg=dark_color, fg=text_color, bd=0, command=self.show_results)
        self.button.place(anchor='nw', relwidth=1, relheight=1,)

        self.button.bind('<Button-1>', self.on_click)
        self.button.bind('<ButtonRelease-1>', self.on_unclick)

    def on_unfocus(self, event):
        if self.entry.is_empty():
            self.escape()

    def on_enter(self, event):
        self.show_results()

    def on_escape(self, event):
        self.escape()

    def escape(self):
        self.hide_results()
        self.clear_songs()

    def show_results(self):
        if self.entry.is_empty():
            return
        self.songs_found.clear()
        song_search = Search()
        self.songs_found = song_search.search(self.entry.get(), 3)
        if len(self.songs_found) == 0:
            return
        self.results.set_contents(self.songs_found)
        self.results.show()
        
        self.results.focus_on_list()

    def on_click(self, event):
        self.button.config(image=self.img_dark)

    def on_unclick(self, event):
        self.button.config(image=self.img)

    def hide_results(self):
        self.results.hide()

    def clear_songs(self):
        self.songs_found.clear()
        self.results.set_contents(self.songs_found)
        self.entry.set_text('')

class DownloadButton(Frame):
    def __init__(self, app, master):
        super().__init__(master, bg=entry_color)

        self.download_button = Button(self,font=(app_font, 14), text='Make\nMixtape',
                                bg=dark_color, fg=text_color, bd=0, command=self.download_songs)
        self.download_button.place(anchor='nw', relwidth=1, relheight=1)

        self.app = app

    def download_songs(self):
        self.app.download_songs()

class Logos(Frame):
    def __init__(self, master):
        super().__init__(master, bg=bg_color)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=35)
        self.grid_rowconfigure(1, weight=0, minsize=150)
        self.grid_rowconfigure(2, weight=0, minsize=150)

        self.logo_frame = Frame(self, bg=bg_color)
        self.logo_frame.grid(row=1, column=0, sticky='nsew')

        self.canvas = Canvas(self.logo_frame, width=100, height=100, 
                            background=bg_color, highlightthickness=0)
        self.canvas.place(anchor='nw', relx=0.5, x=-50, y=10)

        self.developed_label = EntryLabel(self,'Developed by:')
        self.developed_label.grid(row=0, column=0)

        self.logo_img = PhotoImage(data=logo_imgdata)
        self.canvas.create_image(50,50,image=self.logo_img, anchor='center')

        self.credits_frame = Frame(self, bg=bg_color)
        self.credits_frame.grid(row=2, column=0, sticky='nsew')

        self.using = EntryLabel(self.credits_frame,'Using:')
        self.using.place(anchor='nw', x=10, y=10)

        self.tech = []
        self.tech.append(EntryLabel(self.credits_frame,'- youtube-dl'))
        self.tech.append(EntryLabel(self.credits_frame,'- youtube-search-python'))
        self.tech.append(EntryLabel(self.credits_frame,'- Pillow'))

        i = 2
        for t in self.tech:
            t.place(anchor='nw', x=15, y=i*15)
            i += 1

    def open_dev_page(self):
        pass
