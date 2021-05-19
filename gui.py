import tkinter as tk
import tkinter.filedialog
import downloader as dl
import os

bg_color = '#FFFFFF'
entry_color = '#d6d6d6'

success_color = '#00ff77'
failure_color = '#ff0040'

def download():
    status_text.config(state='normal')
    status_text.delete('1.0', tk.END)
    url = url_entry.get()
    dir = dir_entry.get()
    if dl.try_downloading(dir, url):
        status_text.insert('end', ' SUCCESS ', ('success'))
    else:
        status_text.fg = failure_color
        status_text.insert('end', ' FAILURE ', ('failure'))
    url_entry.delete(0, tk.END)
    status_text.config(state='disabled')

def choose_dir():
    program_dir = '/'.join(os.getcwd().split('/')[:3])
    directory = tk.filedialog.askdirectory(initialdir=program_dir, title='Select Directory')
    if(len(directory) > 0):
        dir_entry.delete('0', 'end')
        dir_entry.insert('0', directory)

def add_url_to_list():
    pass

root = tk.Tk()
root.geometry('800x800')
root.title('Mixtape-Maker')

canvas = tk.Canvas(root, height=800, width=800, bg=bg_color, bd=0, highlightthickness=0)
canvas.pack(fill = 'both', expand = True)
canvas.bind('<1>', lambda event: canvas.focus_set())

dir_entry = tk.Entry(root, font=('Helvetica', 16), width=57, bg = entry_color, bd=0)
dir_window = canvas.create_window(35, 50, anchor='nw', window=dir_entry)

dir_button = tk.Button(root, font=('Helvetica', 9), text=' ... ', command=choose_dir)
dir_button_window = canvas.create_window(750, 50, anchor='ne', window = dir_button)

url_entry = tk.Entry(root, font=('Helvetica', 16), width=57,bg=entry_color, bd=0)
url_window = canvas.create_window(35, 100, anchor='nw', window=url_entry)

url_add_button = tk.Button(root, font=('Helvetica', 9), text=' + ', command=add_url_to_list)
url_add_window = canvas.create_window(750, 100, anchor='ne', window = url_add_button)

download_button = tk.Button(root, font=('Helvetica', 12), text='Download', command=download)
download_window = canvas.create_window(750, 700, anchor='se', window=download_button)

status_text = tk.Text(root, font=('Helvetica', 16), width=9, height=1, bd=0, state='disabled')
status_window = canvas.create_window(400, 10, anchor='n', window=status_text)
status_text.tag_add('failure', '1.0', 'end')
status_text.tag_configure('failure', foreground=failure_color)
status_text.tag_add('success', '1.0', 'end')
status_text.tag_configure('success', foreground=success_color)

def start_window():
    root.mainloop()
