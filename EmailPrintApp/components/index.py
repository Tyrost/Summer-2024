
from EmailScript.email_script_handler import read_email_script # !MAIN Module! Threading Function
from components.Classes.TextEditor import TextEditor # !Class Module! Text editor Widget for User Input
from components.Classes.Timer import Timer # !Class Module! Track program's thread timing 

from Setup.SystemicFunctions import * # !Package! Systemic Functions
'''
Saves and retrieves the email and password from two `TextEditor` instances onto JSON.
Constructs the file path for an attachment then sends a PDF file to the default printer set up on the system.
Creates the path to the excel file. Adds input-specified data into the specified excel file
'''

from typing import List, Tuple # Code Readability 
from win32 import win32print # To check printer status and default
from tkinter import font # Global Font
import logging as log # Debugging and Information, Warning and Errors
import tkinter as tk # Builds off Interface and Program Functionality
import threading # Used to thread main background script

#______________________________________________________________ Index Script ______________________________________________________________ #

# Log Main Config #
log.basicConfig(level = log.INFO)

#_________________________________________________________________ Globals _________________________________________________________________ #

default_printer = win32print.GetDefaultPrinter() # Current Default Printer
excel_set = False

current_email = None
current_password = None

#__________________________________________________________________ Window __________________________________________________________________#

WINDOW = tk.Tk() # Main Window

WHEIGHT = 600
WWIDTH = 800

try:
    FONT = font.Font(family = os.path.join(__file__,'Font', 'Lexend-VariableFont_wght.tff'), size = 18)
except Exception as e:
    log.warn('Failed to load Lexend Font.')
    FONT = font.Font(family = 'Helvetica', size = 18)

container = tk.Frame(WINDOW)
container.pack(fill = 'both', expand = True)

#__________________________ Main Frames Construction __________________________#

FRAME_MAIN = tk.Frame(container)
FRAME_RUN = tk.Frame(container)
FRAME_SETUP = tk.Frame(container)
FRAME_MAIL = tk.Frame(container)
FRAME_PRINTER = tk.Frame(container)
FRAME_EXCEL = tk.Frame(container)

frames = [FRAME_MAIN, FRAME_RUN, FRAME_SETUP, FRAME_MAIL, FRAME_PRINTER, FRAME_EXCEL]

for frame in frames:
    frame.grid(row=0, column=0, sticky='nsew')

try:
    custom_font = font.Font(family = 'Lexend', size = 12)
    WINDOW.option_add('*Font', custom_font)
except Exception as e:
    log.error(f'Error loading font: {e}')

def set_window(window = WINDOW) -> None:
    window.title('Email Printer - Wet Designs')
    window.geometry(f'{str(WWIDTH)}x{str(WHEIGHT)}')
    window.configure(bg='lightblue')

    return

def create_editor(window, text, width, height, font) -> TextEditor:
    '''
    This function initializes a `TextEditor` object with the specified parameters\n
    and returns it. The `TextEditor` is a custom text editor widget with placeholder\n
    text functionality and event handling.
    '''
    editor = TextEditor(window, text, width, height, font)

    return editor

def handle_forget_widget(frame) -> None:
    '''
    Handles widgets (editors & labels) according to the frame.
    Manual Handling Function.
    '''
    if frame != FRAME_SETUP:
        email_editor.text_editor.place_forget()
        pw_editor.text_editor.place_forget()
        instructions_email_setup.place_forget()
    
    if frame != FRAME_PRINTER:
        default_printer_editor.text_editor.place_forget()
        printer_list.place_forget()
    
    if frame != FRAME_EXCEL:
        set_excel_editor.text_editor.place_forget()

    return 

def switch_frame(frame:tk.Frame) -> None:
    '''
    Main switching frame functions:

    Args:
        frame (tk.Frame): The target frame to switch onto.
    
    - Updates the global current frame variable.
    - Hides all of the program-existent buttons.
    - Depending on the frame input, it shows widgets accordingly.
    
    Calls the `handle_forget_widget` function to handle widgets' visibility.
    '''
    global current_frame

    current_frame = frame
    hide_all(all_frame_btns)
    frame.tkraise()
    log.info(f'Switched frame')
    bind_hover_effects()

    # Widget Handler #
    handle_forget_widget(current_frame)

    return

# Button Division Canvas #

MAIN_CANVAS = tk.Canvas(WINDOW, width=800, height=600)
MAIN_CANVAS.pack()

#__________________________________________________________________ Status __________________________________________________________________#

current_frame = FRAME_MAIN # Start out with the Main Frame as a baseline

status = 'Not Running'
running = False

def create_status_icon(window: tk.Tk) -> Union[tk.Canvas, int]:
    '''
    Creates the components necessary to build the status icon for global implementation.

    Args:
        window (tk.Tk): To be used as an input for the necessary Canvas object.
    '''

    icon_canvas = tk.Canvas(window, width = 50, height = 50, highlightthickness = 0)
    icon_canvas.place(relx = 1.0, rely = 0.0, anchor = 'ne')
    circle = icon_canvas.create_oval(15, 15, 35, 35, outline='black', fill='red')

    return icon_canvas, circle

def update_icon_color(icon_canvas:tk.Canvas, circle:int, color:tuple) -> None:
    '''
    Update the color of the status icon.
    
    Args:
        icon_canvas (tk.Canvas): To be used to be configured given the following two settings.
        circle (int): Modifies the radial size of the `icon_canvas` object.
        color (tuple): Modifies the color of the `icon_canvas` object.
    '''
    icon_canvas.itemconfig(circle, fill=color)

    return

def create_status_label(window:tk.Tk) -> tk.Label:
    '''
    Create a status label and position it in the top-right corner of the window
    '''
    status_label = tk.Label(window, text=f'Status: {status}', width=20, height=2)
    status_label.place(relx=0.95, rely=0.01, anchor='ne')  # Position in the top-right corner

    return status_label

status_icon, circle = create_status_icon(WINDOW)
status_label = create_status_label(WINDOW)

def update_status(new_status):
    '''
    Updates the status of the Status Widget, which includes the icon and the label.\n
    Denoted as `status_icon` and `status_label` global variables.
    '''
    global status

    status = new_status
    status_label.config(text=f'Status: {status}')
    if status == 'Running':
        update_icon_color(status_icon, circle, 'green')
    else:
        update_icon_color(status_icon, circle, 'red')

#_____________________________________________________________ Labels / Widgets _____________________________________________________________ #

# Timer #

timer_label = Timer(FRAME_RUN)

# Set Email Widgets #

password_setup_txt = 'IMPORTANT:\nEMAIL SETUP INSTRUCTIONS.\nPassword IS NOT the same password used for your email.\nProceed with the following link:\nhttps://myaccount.google.com/u/3/apppasswords?\nWithin the text box labeled "App name", please input "Python Automation Script".\nPlease use the given auto-generated code as a password to input onto this program.'
instructions_email_setup = tk.Label(WINDOW, text=password_setup_txt, width=65, height=8)

email_editor = create_editor(WINDOW, 'Email', 33, 1, FONT)
pw_editor = create_editor(WINDOW, 'Password', 33, 1, FONT)

# Set Printer Widgets #

def order_str_list(input_list:List[str]) -> str:
    '''
    Support function used the following global variable `printer_list`.\n
    Uses input list to space its elements in different lines for readability.

    Args:
        input_list (list): Any list or set of strings within it.
    '''
    result = 'Available Printers:\n\n'
    for element in input_list:
        result += element + '\n'
    return result

printer_list = tk.Label(WINDOW, text=order_str_list(list_printers()), width=45, height=15)

default_printer_editor = create_editor(WINDOW, 'Default Printer', 33, 1, FONT)

# Set Excel Widgets #

set_excel_editor = create_editor(WINDOW, 'Excel File Name', 33, 1, FONT)

#_________________________________________________________________ Handlers _________________________________________________________________# 

# Universal Handlers #

def handle_back_to_main() -> None:
    '''
    Handles the Click Event over the `back_to_main` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_MAIN`.\n
    Shows all of the designated main frame buttons to be used.
    '''
    log.info('Back Button Clicked! Back to Main')
    switch_frame(FRAME_MAIN)
    show_button_on_canvas(main_frame_btns)

#_____________________________ Main Frame Handlers _____________________________#

def handle_click_setup() -> None:
    '''
    Handles the Click Event over the `setup` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_SETUP`.\n
    Shows all of the designated setup frame buttons to be used.
    '''
    log.info('Set Up Button Clicked! Switch')
    switch_frame(FRAME_SETUP)
    show_button_on_canvas(setup_frame_btns)
    hide_button_on_canvas([(confirm_email_rect, confirm_email_text)]) # Only for Confirm Button

def handle_click_see_mail() -> None:
    '''
    Handles the Click Event over the `see_mail` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_MAIL`.\n
    Shows all of the designated email frame buttons to be used.
    '''
    log.info('See Mail Button Clicked! Switch')
    switch_frame(FRAME_MAIL)
    show_button_on_canvas(mail_frame_btns)

def handle_click_run() -> None:
    '''
    Handles the Click Event over the `run` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_RUN`.\n
    Shows all of the designated running script frame buttons to be used.
    '''
    log.info('Run Button Clicked! Switch')
    switch_frame(FRAME_RUN)
    show_button_on_canvas(run_frame_btns)

def handle_set_printer_menu() -> None:
    '''
    Handles the Click Event over the `set_printer` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_PRINTER`.\n
    Shows all of the designated printer setup frame buttons to be used.\n
    Additionally, it will call the `handle_set_printer`\n 
    as a sub-handler, as this sector is initialized within the `FRAME_SETUP` already and not `FRAME_MAIN`.
    '''
    log.info('Printer Setup Button Clicked! Switch')
    switch_frame(FRAME_SETUP)
    show_button_on_canvas(printer_frame_btns)

    handle_set_printer()

def handle_set_excel_menu() -> None:
    '''
    Handles the Click Event over the `set_excel` button.\n
    Calls the function, `switch_frame`, to go back to `FRAME_EXCEL`.\n
    Shows all of the designated printer setup frame buttons to be used.\n
    Additionally, it will call the `handle_set_excel_path`\n 
    as a sub-handler, as this sector is initialized within the `FRAME_SETUP` already and not `FRAME_MAIN`.
    '''
    log.info('Excel Setup Button Clicked! Switch')
    switch_frame(FRAME_EXCEL)
    show_button_on_canvas(excel_frame_btns)

    handle_set_excel_path()

# Run Frame - Handler #

stop_event = threading.Event()

def start_email_thread() -> None:
    '''
    Starts the thread connection to the main script. Mainly uses the `email_thread` global variable for initialization.
    '''
    global email_thread, running, status

    email_thread = threading.Thread(target = read_email_script, args = (running, stop_event))
    email_thread.start()

    check_email_thread()

    return

def stop_email_thread():
    '''
    Stops the thread connection to the main script. Mainly uses the `email_thread` global variable for termination.
    '''
    global stop_event

    if email_thread.is_alive():
        stop_event.set()
        email_thread.join()

    return

def check_email_thread() -> None:
    '''
    Checks the status of the thread connecting to the main script.
    '''
    global running, status

    if running and not email_thread.is_alive():
        running = False
        status = 'Not Running'
        update_status(status)
        log.info(f'Thread has stopped. Status: {status}')

    WINDOW.after(1000, check_email_thread)

    return

def handle_run_script() -> None:
    '''
    Handles the Click Event over the `Run` button.\n
    Checks for Excel File existence, Sys Printer is available. Dynamically\n
    displays warning messages if rules are not satisfied.\n
    Calls the functions:\n
    `update_status` for global status widget.\n
    `start_email_thread` to initialize the thread connection.\n
    '''
    global running
    global status

    invalid = False

    excel_sheet_abspath = os.path.join(os.getcwd(), 'Setup/ExcelSheet')

    if len(os.listdir(os.path.abspath(excel_sheet_abspath))) == 0: # Excel File exists within directory?
        log.info('Excel File Does not exist. Program may not continue')

        excel_not_exist_label = tk.Label(WINDOW, text='Excel File Does not exist. Program may not continue.', width = 45, height = 2)
        excel_not_exist_label.place(x = 200, y = 80)
        WINDOW.after(3000, excel_not_exist_label.destroy)
        invalid = True
    
    if not default_printer: # Printer is available for usage?
        log.info('Default Printer Not Set. Program may not continue.')

        printer_not_set_label = tk.Label(WINDOW, text='Default Printer Not Set. Program may not continue.', width=45, height=2)
        printer_not_set_label.place(x=200, y=130)
        WINDOW.after(3000, printer_not_set_label.destroy)
        invalid = True
    
    if invalid: # Invalid Requirements?
        return

    if running: # Is Main Script already running?
        log.info('Script is already running.')
        return

    timer_label.reset_timer() # Ensures script timer reset before usage

    running = True
    status = 'Running'

    timer_label.start_timer() # Starts script timer
    timer_label.timer_label.pack() # Shows script timer
    
    update_status(status) # Updates global status widget

    start_email_thread() # Starts thread connection to main script

    log.info(f'Timer, Status: {status}')

    return

def handle_stop_script() -> None:
    '''
    Handles the Click Event over the `Stop` button.\n
    Checks if script is already stopped.\n
    Calls the functions:\n
    `update_status` for global status widget.\n
    `stop_email_thread` to initialize the thread connection.\n
    '''
    global running
    global status

    if not running: # Attempt to terminate script. Is it already running?
        log.info(f'Status {status}, please run the script first')
        return

    running = False
    status = 'Not Running'

    timer_label.stop_timer() # Stops script timer
    timer_label.timer_label.pack_forget() # Makes script timer invisible after termination
    update_status(status) # Updates global status widget

    stop_email_thread() # Stops thread connection to main script

    log.info(f'Timer, Status: {status}')

    return

# See Mail Handler #

### For future implementation ###

#____________________________ Set Up Frame Handlers ____________________________#

# Set Printer - Handler #

def on_confirm_printer() -> None:
    '''
    Handles the Click Event over the `Confirm` button within the `FRAME_PRINT` frame.\n
    Gets the text representation of the user's input.\n
    Checks:\n
    If the specified printer was already set.\n
    If printer is contained within the Windows System.\n
    If neither of these cases are true.\n
    Dynamically displays a label accordingly. 
    '''
    global default_printer

    log.info('Confirmed!')

    default_printer = default_printer_editor.get_text() # Extract textual representation of user input

    if setup_printer_system(default_printer): # Is Printer not Already Set and is Existent?
        text = f"Successfully set '{default_printer}' as the default printer."
    elif setup_printer_system(default_printer) is None: # Is Printer Existent?
        text = f'Printer name {default_printer} not available in Windows printer devices'
    elif setup_printer_system(default_printer) == False: # Is Printer Already Set?
        text = f"The printer '{default_printer}' is already set as the default printer."

    info_label = tk.Label(WINDOW, text = text, width = 50, height = 2) # Create dynamic label
    info_label.place(x = 140, y = 150) # Place label

    WINDOW.after(5000, info_label.destroy) # Display label for 5 seconds (5000 ms)

    return

def handle_set_printer() -> None:
    '''
    Handles the Click Event over the `Set Printer` button within the `FRAME_SETUP` frame.\n
    Displays user input editor (`default_printer_editor`), and also places the\n
    global variable, `printer_list`, containing the label for all printers found within\n
    the Windows System.
    '''
    default_printer_editor.text_editor.place(x = 180, y = 100)
    printer_list.place(x = 280, y = 160)

    return

# Set Email - Handler #

def handle_set_credentials() -> None:
    '''
    Handles the Click Event over the `Set Email` button within the `FRAME_SETUP` frame.\n
    Displays user input editors (`email_editor` and `pw_editor`), and also places the\n
    global variable, `instructions_email_setup`, containing the label for necessary instructions\n
    to access the generated password for the user's account to be used by the program' API request.
    '''
    show_button_on_canvas([(confirm_email_rect, confirm_email_text)]) # Display confirmation button to user input
    instructions_email_setup.place(x = 205, y = 450)
    
    email_editor.text_editor.place(x = 180, y = 100)
    pw_editor.text_editor.place(x = 180, y = 150)
    instructions_email_setup.place(x = 205, y = 450)

    return

def on_confirm_click_creds(credentials_path = os.path.join(os.getcwd(), 'Setup/credentials.json')) -> None:
    '''
    Handles the Click Event over the `Confirm` button within the `FRAME_SETUP` frame.\n
    Gets the text representation of the user's input.\n
    Checks if the email input is valid to avoid possible issues with the main script.\n
    Dynamically displays a label accordingly. 
    '''
    global email_editor, pw_editor, current_email, current_password
    
    # Extract textual representation of user input #
    current_email = email_editor.get_text()
    current_password = pw_editor.get_text()

    if '@' not in current_email: # Is input email address valid?

        text = f'Invalid Email.'

    else:    

        text = f'Credentials Confirmed. Email: {current_email}, Password: {current_password}'
        save_credentials(email_editor, pw_editor, credentials_path) # Save Credentials to the JSON database

    confirmed_cred = tk.Label(WINDOW, text = text, width = 50, height = 2)
    confirmed_cred.place(x = 200, y = 200)

    WINDOW.after(3000, confirmed_cred.destroy) # Display message for 3 seconds (3000 ms)

    return

# Set Excel - Handler #

def handle_set_excel_path() -> None:
    
    set_excel_editor.text_editor.place(x = 180, y = 100)

    return

def on_confirm_click_excel() -> None:
    '''
    Handles the Click Event over the `Confirm` button within the `FRAME_EXCEL` frame.\n
    Gets the text representation of the user's input.\n
    Checks:\n
    If the excel file name is longer than 3 characters.\n
    If the excel file name is less than 20 characters.\n
    By calling the `mod_excel_file`, the function will check the type of modification done to the file.\n
        (Rename -> 'str', Creation -> 'str', NoChange -> None)\n
        - If the file name is the same as the one already set, the function will turn to a void function. Returning None.\n
        Will dynamically change the label message according to the type of modification\n

    Dynamically displays a label accordingly. 
    '''
    global excel_set

    excel_file_name = set_excel_editor.get_text() # Extract textual representation of user input

    if len(excel_file_name) <= 4: # Is the length of the user's desired file name greater than 3 characters long?
        log.warn('Invalid Excel File name')
        text = f'Invalid File Name: {excel_file_name}. Name must be longer than 3 characters.'

    elif len(excel_file_name) >= 21: # Is the length of the user's desired file name less than 21 characters long?
        log.warn('Invalid Excel File name')
        text = f'Invalid File Name: {excel_file_name}. Length of name must be less than 20 characters'

    else: # Conditions satisfied

        if not mod_excel_file(excel_file_name): # If no modification has been made to the file

            text = f'File Already named: {excel_file_name}.xlsx'

        else:

            log.info('Valid Excel File name')
            text = f'Excel File: {excel_file_name} Set'

            excel_set = os.listdir(excel_dir)[0] # Set Global Excel File Name

    # Display Dynamic Labels

    confirm_excel = tk.Label(WINDOW, text = text)
    confirm_excel.place(x = 200, y = 200)
    WINDOW.after(5000, confirm_excel.destroy)

    return

#__________________________________________________________________ Buttons __________________________________________________________________#

# Dimensions and Colors #

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
SEPARATION = 10

DEFAULT_COLOR = 'lightgrey'
HOVER_COLOR = 'gray'

def create_button(x:Union[int, float], y:Union[int, float], text:str, command) -> Tuple[int, int]:
    '''
    Creates the components necessary to create buttons.

    Args:
        x (int or float): X Position of where the desired button will be created in the screen.
        y (int or flat): Y Position of where the desired button will be created in the screen.
        text (str): Button Display text for user visualization.
        command (function): Command to be carried on in the event of the button click.

    Returns:
        A tuple of integers containing the class representation of the buttons, represented by integers.
    '''

    # Create Button Box
    rect = MAIN_CANVAS.create_rectangle(x, y, x + BUTTON_WIDTH, y + BUTTON_HEIGHT, outline = 'black', fill = 'lightgrey')
    # Create Button Text
    text_id = MAIN_CANVAS.create_text(x + BUTTON_WIDTH / 2, y + BUTTON_HEIGHT / 2, text = text, fill = 'black', font = (FONT, 14, 'bold'))
    
    # Hovering Button Bind
    MAIN_CANVAS.tag_bind(rect, '<Button-1>', lambda event: command())
    MAIN_CANVAS.tag_bind(text_id, '<Button-1>', lambda event: command())

    return rect, text_id

# Universal Button #

back_to_main_rect, back_to_main_text = create_button(70, 380, 'Back', command = handle_back_to_main)

# Main Frame Buttons #

setup_rect, setup_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Up', command = handle_click_setup)
see_mail_rect, see_mail_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'See Mail', command = handle_click_see_mail)
run_rect, run_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Run', command = handle_click_run)

main_frame_btns = [(setup_rect, setup_text), (see_mail_rect, see_mail_text), (run_rect, run_text)]

# Mail Frame Buttons #

'''For Future Implementation'''

mail_frame_btns = [(back_to_main_rect, back_to_main_text)]

# SetUp Frame Buttons #

confirm_email_rect, confirm_email_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 20, 'Confirm', command = on_confirm_click_creds)

set_printer_rect, set_printer_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Set Printer', command = handle_set_printer_menu)
set_credentials_rect, set_credentials_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Set Email', command = handle_set_credentials)
set_excel_rect, set_excel_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + 2 * (BUTTON_HEIGHT + SEPARATION), 'Set Excel', command = handle_set_excel_menu)

setup_frame_btns = [(back_to_main_rect, back_to_main_text), (set_printer_rect, set_printer_text),(set_credentials_rect, set_credentials_text),(set_excel_rect, set_excel_text), (confirm_email_rect, confirm_email_text)]

# Run Frame Buttons #

run_script_rect, run_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200, 'Run', command = handle_run_script)
stop_script_rect, stop_script_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 200 + BUTTON_HEIGHT + SEPARATION, 'Stop', command = handle_stop_script)

run_frame_btns = [(back_to_main_rect, back_to_main_text), (run_script_rect, run_script_text), (stop_script_rect, stop_script_text)]

# Printer Frame Buttons #

confirm_printer_rect, confirm_printer_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 20, 'Confirm', command = on_confirm_printer)

printer_frame_btns = [(back_to_main_rect, back_to_main_text), (confirm_printer_rect, confirm_printer_text)]

# Excel Frame Buttons #

confirm_excel_rect, confirm_excel_text = create_button(WWIDTH//2 - BUTTON_WIDTH//2, 20, 'Confirm', command = on_confirm_click_excel)

excel_frame_btns = [(back_to_main_rect, back_to_main_text), (confirm_excel_rect, confirm_excel_text)]

# All Frame Buttons #

all_frame_btns = [main_frame_btns, run_frame_btns, mail_frame_btns, setup_frame_btns, printer_frame_btns, excel_frame_btns]

# Hide / Show Buttons #

def hide_button_on_canvas(btns: List[Tuple[int, int]]) -> None:
    '''
    Hides all of the buttons given from the argument.
    '''

    for rect, text_id in btns:

        MAIN_CANVAS.itemconfig(rect, state = tk.HIDDEN)
        MAIN_CANVAS.itemconfig(text_id, state = tk.HIDDEN)
    
    return

def show_button_on_canvas(btns: List[Tuple[int, int]]) -> None:
    '''
    Shows all of the buttons given from the argument.
    '''
    for rect, text_id in btns:

        MAIN_CANVAS.itemconfig(rect, state = tk.NORMAL)
        MAIN_CANVAS.itemconfig(text_id, state = tk.NORMAL)

    return

def hide_all(frame_btns: List[List[Tuple[int, int]]]) -> None:
    '''
    Hides all of the buttons given from the argument.
    '''
    for btns in frame_btns:
        hide_button_on_canvas(btns)

    return

# Function Handle Hovering #

def on_enter(event) -> None:
    '''
    Mouse Event Hovering Over the button's boundary.
    '''
    try:
        item_id = MAIN_CANVAS.find_closest(event.x, event.y)[0]
        if MAIN_CANVAS.type(item_id) == 'rectangle':
            MAIN_CANVAS.itemconfig(item_id, fill=HOVER_COLOR)

    except Exception as e:
        log.warning(f'Error Occurred: {e}')

    return

def on_leave(event) -> None:
    '''
    Mouse Event Hovering Outside the button's boundary.
    '''

    try:
        item_id = MAIN_CANVAS.find_closest(event.x, event.y)[0]
        if MAIN_CANVAS.type(item_id) == 'rectangle':
            MAIN_CANVAS.itemconfig(item_id, fill=DEFAULT_COLOR)

    except Exception as e:
        log.warning(f'Error Occurred: {e}')
    
    return

def bind_hover_effects() -> None:
    '''
    Dictates the execution given the current frame.
    '''

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
    elif current_frame == FRAME_EXCEL:
        frame_buttons = excel_frame_btns

    try:
        for rect, text_id in frame_buttons:
            MAIN_CANVAS.tag_bind(rect, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(rect, '<Leave>', on_leave)
            MAIN_CANVAS.tag_bind(text_id, '<Enter>', on_enter)
            MAIN_CANVAS.tag_bind(text_id, '<Leave>', on_leave)
    except Exception as e:
        log.warn(f'Error: {e}')
    
    return

bind_hover_effects() # Will Continue to Check for Mouse Event for Hovering Color changes.