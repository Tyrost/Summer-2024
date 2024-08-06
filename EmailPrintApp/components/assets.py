import tkinter as tk
from tkinter import font
import logging as log
from components.TimerApp import TimerApp
from typing import List, Tuple
from EmailScript.email_script_handler import read_email_script
import threading

log.basicConfig(level=log.INFO)

#_________________________________________________________________ Globals _________________________________________________________________ #

printer_set = False
excel_set = False # Will be used to store string path. Will evaluate as True
credentials_set = False # Will be used to store string path. Will evaluate as True

#_________________________________________________________________ Window _________________________________________________________________#

WINDOW = tk.Tk()

WHEIGHT = 600
WWIDTH = 800

FONT = font.Font(family='Summer-2024/EmailPrintApp/components/Font/Lexend-VariableFont_wght.ttf', size=18)

container = tk.Frame(WINDOW)
container.pack(fill='both', expand=True)

FRAME_MAIN = tk.Frame(container)
FRAME_RUN = tk.Frame(container)
FRAME_SETUP = tk.Frame(container)
FRAME_MAIL = tk.Frame(container)

frames = [FRAME_MAIN, FRAME_RUN, FRAME_SETUP, FRAME_MAIL]

for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')

try:
    custom_font = font.Font(family='Lexend', size=12)
    WINDOW.option_add('*Font', custom_font)
except Exception as e:
    log.error(f'Error loading font: {e}')

def set_window(window=WINDOW):
    window.title('Email Printer - Wet Designs')
    window.geometry(f'{str(WWIDTH)}x{str(WHEIGHT)}')
    window.configure(bg='lightblue')

def switch_frame(frame:tk.Frame):
    global current_frame

    current_frame = frame
    hide_all(all_frame_btns)
    frame.tkraise()

    bind_hover_effects()

# Button Division Canvas #

MAIN_CANVAS = tk.Canvas(WINDOW, width=800, height=600)
MAIN_CANVAS.pack()

# Timer #

timer_label = TimerApp(FRAME_RUN)

#_________________________________________________________________ Status _________________________________________________________________#

status = 'Not Running'
running = False
current_frame = FRAME_MAIN

def create_status_icon(window):
    icon_canvas = tk.Canvas(window, width=50, height=50, highlightthickness=0)
    icon_canvas.place(relx=1.0, rely=0.0, anchor='ne')
    circle = icon_canvas.create_oval(15, 15, 35, 35, outline='black', fill='red')
    return icon_canvas, circle

def update_icon_color(icon_canvas, circle, color):
    '''Update the color of the status icon.'''
    icon_canvas.itemconfig(circle, fill=color)

def create_status_label(window):
    '''Create a status label and position it in the top-right corner of the window.'''
    status_label = tk.Label(window, text=f'Status: {status}', width=20, height=2)
    status_label.place(relx=0.95, rely=0.01, anchor='ne')  # Position in the top-right corner
    return status_label

status_icon, circle = create_status_icon(WINDOW)
status_label = create_status_label(WINDOW)

def update_status(new_status):
    global status
    status = new_status
    status_label.config(text=f'Status: {status}')
    if status == 'Running':
        update_icon_color(status_icon, circle, 'green')
    else:
        update_icon_color(status_icon, circle, 'red')

#_________________________________________________________________ Handlers _________________________________________________________________# 

# Universal Handlers #

def handle_back_to_main():
    print('Back Button Clicked! Back to Main')
    switch_frame(FRAME_MAIN)
    show_button_on_canvas(main_frame_btns)

# Main Frame Handlers #

def handle_click_setup():
    print('Set Up Button Clicked! Switch')
    switch_frame(FRAME_SETUP)
    show_button_on_canvas(setup_frame_btns)

def handle_click_see_mail():
    print('See Mail Button Clicked! Switch')
    switch_frame(FRAME_MAIL)
    show_button_on_canvas(mail_frame_btns)

def handle_click_run():
    print('Run Button Clicked! Switch')
    switch_frame(FRAME_RUN)
    show_button_on_canvas(run_frame_btns)

# Run Frame - Handlers #

stop_event = threading.Event()

def start_email_thread():
    global email_thread
    email_thread = threading.Thread(target=read_email_script, args=(running, stop_event))
    email_thread.start()

def stop_email_thread():
    global stop_event
    if email_thread.is_alive():
        stop_event.set()
        email_thread.join()

def handle_run_script():
    global running
    global status

    if running:
        print('Script is already running.')
        return

    timer_label.reset_timer()

    running = True
    status = 'Running'

    timer_label.start_timer()
    timer_label.timer_label.pack()
    update_status(status)

    start_email_thread()

    log.info(f'Timer, Status: {status}: {running}')

def handle_stop_script():
    global running
    global status

    if not running:
        print(f'Status {status}, please run the script first')
        return
    
    running = False
    status = 'Not Running'

    timer_label.stop_timer()
    timer_label.timer_label.pack_forget()
    update_status(status)

    stop_email_thread()

    log.info(f'Timer, Status: {status}: {running}')

# Set Up Frame Handlers #

def handle_set_printer():
    pass

def handle_set_credentials():
    pass

def handle_set_excel_path():
    pass
  
# See Mail Handlers #
pass

#_________________________________________________________________ Buttons _________________________________________________________________#

# Dimensions and Colors #

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
SEPARATION = 10

DEFAULT_COLOR = 'lightgray'
HOVER_COLOR = 'gray'

def create_button(x, y, text, command):
    rect = MAIN_CANVAS.create_rectangle(x, y, x + BUTTON_WIDTH, y + BUTTON_HEIGHT, outline='black', fill='lightgray')
    text_id = MAIN_CANVAS.create_text(x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2, text=text, fill='black', font=(FONT, 14, 'bold'))
    
    MAIN_CANVAS.tag_bind(rect, '<Button-1>', lambda event: command())
    MAIN_CANVAS.tag_bind(text_id, '<Button-1>', lambda event: command())
    return rect, text_id

# Universal Button #

back_to_main_rect, back_to_main_text = create_button(70, 400, 'Back', command=handle_back_to_main)

# Main Frame Buttons #

set_up_rect, set_up_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Up', command=handle_click_setup)
see_mail_rect, see_mail_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'See Mail', command=handle_click_see_mail)
run_rect, run_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Run', command=handle_click_run)

main_frame_btns = [(set_up_rect, set_up_text), (see_mail_rect, see_mail_text), (run_rect, run_text)]

# Mail Frame Buttons #

mail_frame_btns = [(back_to_main_rect, back_to_main_text)]

# SetUp Frame Buttons #

set_printer_rect, set_printer_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Printer', command=handle_set_printer)
set_credentials_rect, set_credentials_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Set Email', command=handle_set_credentials)
set_excel_rect, set_excel_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Set Excel', command=handle_set_excel_path)

setup_frame_btns = [(back_to_main_rect, back_to_main_text), (set_printer_rect, set_printer_text),(set_credentials_rect, set_credentials_text),(set_excel_rect, set_excel_text)]

# Run Frame Buttons #

run_script_rect, run_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Run', command=handle_run_script)
stop_script_rect, stop_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Stop', command=handle_stop_script)

run_frame_btns = [(back_to_main_rect, back_to_main_text), (run_script_rect, run_script_text), (stop_script_rect, stop_script_text)]

# All Frame Buttons #

all_frame_btns = [main_frame_btns, run_frame_btns, mail_frame_btns, setup_frame_btns]

# Hide / Show Buttons #

def hide_button_on_canvas(btns: List[Tuple[int, int]]):
    for rect, text_id in btns:
        MAIN_CANVAS.itemconfig(rect, state=tk.HIDDEN)
        MAIN_CANVAS.itemconfig(text_id, state=tk.HIDDEN)

def show_button_on_canvas(btns: List[Tuple[int, int]]):
    for rect, text_id in btns:
        MAIN_CANVAS.itemconfig(rect, state=tk.NORMAL)
        MAIN_CANVAS.itemconfig(text_id, state=tk.NORMAL)

def hide_all(frame_btns: List[List[Tuple[int, int]]]):
    for btns in frame_btns:
        hide_button_on_canvas(btns)

# Function Hndle Hovering #

def on_enter(event):
    try:
        item_id = MAIN_CANVAS.find_closest(event.x, event.y)[0]
        if MAIN_CANVAS.type(item_id) == 'rectangle':
            MAIN_CANVAS.itemconfig(item_id, fill=HOVER_COLOR)
    except Exception as e:
        log.warning(f'Error Occured: {e}')

def on_leave(event):
    try:
        item_id = MAIN_CANVAS.find_closest(event.x, event.y)[0]
        if MAIN_CANVAS.type(item_id) == 'rectangle':
            MAIN_CANVAS.itemconfig(item_id, fill=DEFAULT_COLOR)
    except Exception as e:
        log.warning(f'Error Occured: {e}')

def bind_hover_effects():
    global current_frame

    if current_frame == FRAME_MAIN:
        frame_buttons = main_frame_btns
    elif current_frame == FRAME_SETUP:
        frame_buttons = setup_frame_btns
    elif current_frame == FRAME_MAIL:
        frame_buttons = mail_frame_btns
    elif current_frame == FRAME_RUN:
        frame_buttons = run_frame_btns

    try:
        for rect, text_id in frame_buttons:
            MAIN_CANVAS.tag_bind(rect, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(rect, '<Leave>', on_leave)
            MAIN_CANVAS.tag_bind(text_id, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(text_id, '<Leave>', on_leave)
    except Exception as e:
        log.warn(f'Error: {e}')

bind_hover_effects()