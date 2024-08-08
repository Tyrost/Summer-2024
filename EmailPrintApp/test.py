import tkinter as tk
from tkinter import font

WINDOW = tk.Tk()

FONT = 'Helvetica 12'

container = tk.Frame(WINDOW)
container.pack(fill='both', expand=True)

FRAME_MAIN = tk.Frame(container)
FRAME_RUN = tk.Frame(container)
FRAME_SETUP = tk.Frame(container)
FRAME_MAIL = tk.Frame(container)

def set_credentials(window, font):
    text_edit = tk.Text(window, font=font)
    text_edit.grid(row=0, column=1)

set_credentials(WINDOW, FONT)

WINDOW.mainloop()