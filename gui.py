import tkinter as tk
import tkinter.filedialog
import downloader as dl
import os

program_dir = '/'.join(os.getcwd().split('/')[:3]).replace('\\','/')

bg_color = '#FFFFFF'
entry_color = '#d6d6d6'

success_color = '#00ff77'
failure_color = '#ff0040'

songlist = []

def download_songs():
    for song in songlist:
        download(song)
    songs_listbox.delete('0','end')
    songlist.clear()
    status_text.config(state='normal')
    status_text.delete('1.0', "end")
    status_text.config(state='disabled')

def download(url):
    dir = dir_entry.get()
    dl.try_downloading(dir, url)

def choose_dir():
    directory = tk.filedialog.askdirectory(initialdir=program_dir, title='Select Directory')
    if(len(directory) > 0):
        dir_entry.delete('0', 'end')
        dir_entry.insert('0', directory)

def add_url_to_list():
    status_text.config(state='normal')
    status_text.delete('1.0', "end")
    url = url_entry.get()
    is_valid = dl.validate_url(url)
    if(is_valid):
        songlist.append(url)
        status_text.insert('end', ' VALID URL ', ('success'))
    else:
        status_text.insert('end', 'INVALID URL', ('failure'))
    status_text.config(state='disabled')
    url_entry.delete('0', 'end')
    update_listbox()

def update_listbox():
    songs_listbox.delete('0', 'end')
    for song in songlist:
        songs_listbox.insert('end', song)

root = tk.Tk()
root.geometry('800x800')
root.title('Mixtape-Maker')

canvas = tk.Canvas(root, height=800, width=800, bg=bg_color, bd=0, highlightthickness=0)
canvas.pack(fill = 'both', expand = True)
canvas.bind('<1>', lambda event: canvas.focus_set())

dir_entry = tk.Entry(root, font=('Helvetica', 16), width=57, bg = entry_color, bd=0)
dir_window = canvas.create_window(35, 50, anchor='nw', window=dir_entry)
dir_entry.insert('0', program_dir)

dir_button = tk.Button(root, font=('Helvetica', 9), text=' ... ', command=choose_dir)
dir_button_window = canvas.create_window(750, 50, anchor='ne', window = dir_button)

url_entry = tk.Entry(root, font=('Helvetica', 16), width=57,bg=entry_color, bd=0)
url_window = canvas.create_window(35, 100, anchor='nw', window=url_entry)

url_add_button = tk.Button(root, font=('Helvetica', 9), text=' + ', command=add_url_to_list)
url_add_window = canvas.create_window(750, 100, anchor='ne', window = url_add_button)

download_button = tk.Button(root, font=('Helvetica', 12), text='Download', command=download_songs)
download_window = canvas.create_window(765, 750, anchor='se', window=download_button)

status_text = tk.Text(root, font=('Helvetica', 16), width=11, height=1, bd=0, state='disabled')
status_window = canvas.create_window(400, 10, anchor='n', window=status_text)
status_text.tag_add('failure', '1.0', 'end')
status_text.tag_configure('failure', foreground=failure_color)
status_text.tag_add('success', '1.0', 'end')
status_text.tag_configure('success', foreground=success_color)

songs_listbox = tk.Listbox(root, font=('Helvetica', 14))
songlist_window = canvas.create_window(35, 200, width=730, height=500, anchor='nw', window=songs_listbox)

def start_window():
    root.mainloop()
