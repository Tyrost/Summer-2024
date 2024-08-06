import subprocess
import os
import logging as log
from win32 import win32print
import pygetwindow as gw
import time

WAITING_TIME = 100 # Seconds

def setup_printer_system():
    try:
        command = ["control", "printers"]
        subprocess.Popen(command)

        log.info("Please select the default printer in the opened window.")
        time.sleep(WAITING_TIME)  

        window_titles = [w.title for w in gw.getWindowsWithTitle('Printers')]

        if not window_titles:
            log.error('Printer setup window is not open or has been closed.')
            return None

        # Wait for user to select the printer
        log.info("Please select the default printer in the opened window.")
        time.sleep(10)  # Adjust as needed

        # Get the default printer name
        printer_name = win32print.GetDefaultPrinter()
        if printer_name:
            return printer_name
        else:
            log.error('No default printer found.')
            return None
    except subprocess.CalledProcessError as e:
        log.error(f'Failed to open printer setup page: {e}')
        return None
    except Exception as e:
        log.error(f'Unexpected error: {e}')
        return None
    
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