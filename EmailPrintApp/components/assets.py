import tkinter as tk
from tkinter import font
import logging as log
import json
from components.TimerApp import TimerApp
from typing import List, Tuple
from EmailScript.email_script_handler import read_email_script
from Setup.setup_system_handler import credential_obj, save_credentials
import threading
from Setup.SystemicFunctions.setup_printer_system import *

log.basicConfig(level=log.INFO)

#_________________________________________________________________ Globals _________________________________________________________________ #

default_printer = None
excel_set = False # Will be used to store string path. Will evaluate as True

current_email = None
current_password = None

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
FRAME_PRINTER = tk.Frame(container)

frames = [FRAME_MAIN, FRAME_RUN, FRAME_SETUP, FRAME_MAIL, FRAME_PRINTER]

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
    log.info(f'Switched onto {current_frame} frame')
    bind_hover_effects()

    # Make All Existant Widgets Unseeable
    if current_frame != FRAME_SETUP:
        email_editor.text_editor.place_forget()
        pw_editor.text_editor.place_forget()
        instructions_email_setup.place_forget()
    
    if current_frame != FRAME_PRINTER:
        default_printer_editor.text_editor.place_forget()
        


# Button Division Canvas #

MAIN_CANVAS = tk.Canvas(WINDOW, width=800, height=600)
MAIN_CANVAS.pack()

#_________________________________________________________________ Status _________________________________________________________________#

current_frame = FRAME_MAIN

status = 'Not Running'
running = False

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

# _________________________________________________________________ Labels / Widgets _________________________________________________________________ #

# Timer #

timer_label = TimerApp(FRAME_RUN)

# Email Set Up Instructions Label #

password_setup_txt = 'IMPORTANT:\nEMAIL SETUP INSTRUCTIONS.\nPassword IS NOT the same password used for you email.\nProceed with the following link:\nhttps://myaccount.google.com/u/3/apppasswords?\nWithin the text box labeled "App name", please input "Python Automation Script".\nPlease use the given auto-generated code as a password to input onto this program.'
instructions_email_setup = tk.Label(WINDOW, text=password_setup_txt, width=65, height=8)

# Set Email Widgets #

email_editor, pw_editor = credential_obj(WINDOW, ['Email', 'Password'], 33, 1, FONT)

if current_frame != FRAME_SETUP:
    email_editor.text_editor.pack_forget()
    pw_editor.text_editor.pack_forget()

# Set Printer Widgets #

default_printer_editor, none = credential_obj(WINDOW, ['Default Printer', 'none'], 33, 1, FONT)
none.text_editor.destroy()

if current_frame != FRAME_PRINTER:
    default_printer_editor.text_editor.pack_forget()

#_________________________________________________________________ Handlers _________________________________________________________________# 

# Universal Handlers #

def handle_back_to_main():

    log.info('Back Button Clicked! Back to Main')
    switch_frame(FRAME_MAIN)
    show_button_on_canvas(main_frame_btns)

#__________________________ Main Frame Handlers __________________________#

def handle_click_setup():
    log.info('Set Up Button Clicked! Switch')
    switch_frame(FRAME_SETUP)
    show_button_on_canvas(setup_frame_btns)
    hide_button_on_canvas([(confirm_rect, confirm_text)]) # Only for Confirm Button

def handle_click_see_mail():
    log.info('See Mail Button Clicked! Switch')
    switch_frame(FRAME_MAIL)
    show_button_on_canvas(mail_frame_btns)

def handle_click_run():
    log.info('Run Button Clicked! Switch')
    switch_frame(FRAME_RUN)
    show_button_on_canvas(run_frame_btns)

def handle_set_printer_menu():
    log.info('Printer Setup Button Clicked! Switch')
    switch_frame(FRAME_SETUP)
    show_button_on_canvas(printer_frame_btns)

    handle_set_printer()

#__________________________ Set Up Frame Handlers __________________________#

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

    log.info(f'Timer, Status: {status}')

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

    log.info(f'Timer, Status: {status}')
    return

# Set Printer - Handlers #

def on_confirm_printer():
    global default_printer

    log.info('Confirmed!')

    default_printer = default_printer_editor.get_text()
    text = ''

    if setup_printer_system(default_printer):
        text = f"Successfully set '{default_printer}' as the default printer."
    elif not setup_printer_system(default_printer):
        text = f"The printer '{default_printer}' is already set as the default printer."
    elif setup_printer_system(default_printer) is None:
        text = f'Printer name {default_printer} not available in Windows printer devices'

    info_label = tk.Label(WINDOW, text=text, width=50, height=2)
    info_label.place(x=140, y=150)
    WINDOW.after(5000, info_label.destroy)

def handle_set_printer():

    def order_str_list(l):
        result = 'Available Printers:\n\n'
        for element in l:
            result += element + '\n'
        return result
    
    printer_list = tk.Label(WINDOW, text=order_str_list(list_printers()), width=45, height=15)
    
    if current_frame == FRAME_SETUP:
        default_printer_editor.text_editor.place(x=180, y=100)
        printer_list.place(x=280, y=160)

# Set Credentials - Handler #

def handle_set_credentials():

    show_button_on_canvas([(confirm_rect, confirm_text)])
    instructions_email_setup.place(x=205, y=450)
    
    if current_frame == FRAME_SETUP:
        email_editor.text_editor.place(x=180, y=100)
        pw_editor.text_editor.place(x=180, y=150)
        instructions_email_setup.place(x=205, y=450)

def on_confirm_click_setup(credentials_path=os.path.join(__file__,"..",'Setup','credentials.json')):
    global email_editor, pw_editor, current_email, current_password
    
    current_email = email_editor.get_text()
    current_password = pw_editor.get_text()
    
    confirmed_cred = None
    
    if '@gmail.com' not in current_email:
        confirmed_cred = tk.Label(WINDOW, text=f'Invalid Email. Must be Google Email ending in @gmail.com', width=50, height=2)
    else:    
        confirmed_cred = tk.Label(WINDOW, text=f'Credentials Confirmed. Email: {current_email}, Password: {current_password}', width=50, height=2)
        save_credentials(email_editor, pw_editor, credentials_path)
    
    confirmed_cred.place(x=200, y=200)

    WINDOW.after(5000, confirmed_cred.destroy)
        
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

back_to_main_rect, back_to_main_text = create_button(70, 380, 'Back', command=handle_back_to_main)

# Main Frame Buttons #

set_up_rect, set_up_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Up', command=handle_click_setup)
see_mail_rect, see_mail_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'See Mail', command=handle_click_see_mail)
run_rect, run_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Run', command=handle_click_run)

main_frame_btns = [(set_up_rect, set_up_text), (see_mail_rect, see_mail_text), (run_rect, run_text)]

# Mail Frame Buttons #

mail_frame_btns = [(back_to_main_rect, back_to_main_text)]

# SetUp Frame Buttons #

confirm_rect, confirm_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 20, 'Confirm', on_confirm_click_setup)

set_printer_rect, set_printer_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Printer', command=handle_set_printer_menu)
set_credentials_rect, set_credentials_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Set Email', command=handle_set_credentials)
set_excel_rect, set_excel_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Set Excel', command=handle_set_excel_path)

setup_frame_btns = [(back_to_main_rect, back_to_main_text), (set_printer_rect, set_printer_text),(set_credentials_rect, set_credentials_text),(set_excel_rect, set_excel_text), (confirm_rect, confirm_text)]

# Run Frame Buttons #

run_script_rect, run_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Run', command=handle_run_script)
stop_script_rect, stop_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Stop', command=handle_stop_script)

run_frame_btns = [(back_to_main_rect, back_to_main_text), (run_script_rect, run_script_text), (stop_script_rect, stop_script_text)]

# Printer Frame Buttons #

confirm_rect_print, confirm_text_print = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 20, 'Confirm', on_confirm_printer)

printer_frame_btns = [(back_to_main_rect, back_to_main_text), (confirm_rect_print, confirm_text_print)]

# All Frame Buttons #

all_frame_btns = [main_frame_btns, run_frame_btns, mail_frame_btns, setup_frame_btns, printer_frame_btns]

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
    elif current_frame == FRAME_PRINTER:
        frame_buttons = printer_frame_btns

    try:
        for rect, text_id in frame_buttons:
            MAIN_CANVAS.tag_bind(rect, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(rect, '<Leave>', on_leave)
            MAIN_CANVAS.tag_bind(text_id, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(text_id, '<Leave>', on_leave)
    except Exception as e:
        log.warn(f'Error: {e}')

bind_hover_effects()