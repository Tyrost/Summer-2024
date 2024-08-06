import subprocess
import os
import logging as log
import sys
from win32 import win32print,win32api
from pathlib import Path
relative_route = os.path.join(os.path.dirname(__file__), '..')
absolute_route= os.path.abspath(relative_route)
sys.path.append(absolute_route)
# import pygetwindow as gw
import time

WAITING_TIME = 100 # Seconds

def list_printers()->list:
    printers=win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    printer_names=list()
    for printer in printers:
        printer_names.append(printer[2])
    return printer_names
printers=list_printers()

def setup_printer_system(printer_names:list)->str:
    #TODO Select from the printer_names a printer_name, set the printer name and return the printer
    # - Select printer into variable    
    # Setting of default printer
    selected_printer="Brother MFC-J485DW Printer"
    win32print.SetDefaultPrinter(selected_printer)
    
    
    return selected_printer
    
    # try:
    #     command = ["control", "printers"]
    #     subprocess.Popen(command)

    #     log.info("Please select the default printer in the opened window.")
    #     time.sleep(WAITING_TIME)  

    #     window_titles = [w.title for w in gw.getWindowsWithTitle('Printers')]

    #     if not window_titles:
    #         log.error('Printer setup window is not open or has been closed.')
    #         return None

    #     # Wait for user to select the printer
    #     log.info("Please select the default printer in the opened window.")
    #     time.sleep(10)  # Adjust as needed

    #     # Get the default printer name
    #     printer_name = win32print.GetDefaultPrinter()
    #     if printer_name:
    #         return printer_name
    #     else:
    #         log.error('No default printer found.')
    #         return None
    # except subprocess.CalledProcessError as e:
    #     log.error(f'Failed to open printer setup page: {e}')
    #     return None
    # except Exception as e:
    #     log.error(f'Unexpected error: {e}')
    #     return None

def wait_for_printer_setup(timeout=60, interval=100):
    """Wait for the printer setup to complete within the specified timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        printer_name = setup_printer_system()
        if printer_name:
            return printer_name
        time.sleep(interval)
    return None

def set_printer_name():
    """Ensure the printer setup is complete and return the printer name if successful."""
    printer_name = wait_for_printer_setup()
    if printer_name:
        return printer_name
    else:
        log.error('Printer setup not completed within the timeout period.')
        raise NotImplementedError('Printer Not Set')
selected_printer=setup_printer_system(printers)
def get_attachment_filepath(file_name:str)->str:
    script_dir=Path(__file__).resolve().parent
    
    attachments_dir=script_dir.parents[1]/'EmailScript'/"attachments"
        
    file_path=attachments_dir/file_name
    
    
    rel_path=os.path.join(__file__,"..","..","..",'EmailScript',"attachments",file_name)
    abs_path=os.path.abspath(rel_path)
    
    if(os.path.isfile(abs_path)):
        return abs_path
    else:
        return "Error"

def print_pdf(file_name)->None:
    #IMPORTANT Operative system requires a pdf reader set by default (Adobe Reader ,Foxit reader, etc...)
    path_file=get_attachment_filepath(file_name)
    
    if(os.path.isfile(path_file)):
        win32api.ShellExecute(
            0,
            "print",
            path_file,
            f"/d'{win32print.GetDefaultPrinter()}'",
            ".",
            0
        )
    else:
        print("file does not exists")
    
    

filepath=get_attachment_filepath("invoice-4730.pdf")

print_pdf(filepath)
# def print_file(printer_name, file_path):
#     """Print the specified file to the given printer."""
#     if not os.path.exists(file_path):
#         log.error(f"Error: File not found: {file_path}")
#         return
#     try:
#         command = ["print", f'/D:{printer_name}', file_path]
#         subprocess.run(command, check=True)
#     except subprocess.CalledProcessError as e:
#         log.error(f'Failed to print the file: {e}')
#     except Exception as e:
#         log.error(f'Unexpected error: {e}')
        
# file_to_print = 'EmailScript/attachments/invoice-4730.pdf'

# def print_execution():
#     try:
#         printer_name = handle_set_printer()
#         if printer_name:
#             print_file(printer_name, file_to_print)
#     except NotImplementedError:
#         log.error('Printer setup failed, unable to print the file.')

