import tkinter as tk
import downloader as dl

bg_color = '#FFFFFF'
entry_color = '#d6d6d6'

success_color = '#00ff77'
failure_color = '#ff0040'

def download():
    status_text.delete('1.0', tk.END)
    status_text.config(state='normal')
    url = dir_entry.get()
    if dl.try_downloading(url):
        status_text.insert('end', 'SUCCESS', ('success'))
    else:
        status_text.fg = failure_color
        status_text.insert('end', 'FAILURE', ('failure'))
    dir_entry.delete(0, tk.END)
    status_text.config(state='disabled')

root = tk.Tk()
root.geometry('800x800')
root.title('Mixtape-Maker')

canvas = tk.Canvas(root, height=800, width=800, bg=bg_color, bd=0, highlightthickness=0)
canvas.pack(fill = 'both', expand = True)
canvas.bind('<1>', lambda event: canvas.focus_set())

dir_entry = tk.Entry(root, font=('Helvetica', 16), width=50, bg = entry_color, bd=0)
dir_window = canvas.create_window(35, 50, anchor='nw', window=dir_entry)

download_button = tk.Button(root, font=('Helvetica', 12), text='Download', command=download)
download_window = canvas.create_window(600, 48, anchor='nw', window=download_button)

status_text = tk.Text(root, font=('Helvetica', 16), width=8, height=1, bd=0, state='disabled')
status_window = canvas.create_window(350, 10, anchor='nw', window=status_text)
status_text.tag_add('failure', '1.0', 'end')
status_text.tag_configure('failure', foreground=failure_color)
status_text.tag_add('success', '1.0', 'end')
status_text.tag_configure('success', foreground=success_color)

def start_window():
    root.mainloop()
