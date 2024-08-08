import os
import logging as log
import sys
from win32 import win32print,win32api

# Thanks Uncle Angel for this module! :) #

relative_route = os.path.join(os.path.dirname(__file__), '..')
absolute_route= os.path.abspath(relative_route)
sys.path.append(absolute_route)

WAITING_TIME = 100 # Seconds

def list_printers()->list:
    """
    Get a list of available printers.

    Returns:
        list: A list of available printer names.
    """
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    
    printer_names = [printer[2] for printer in printers]

    return printer_names

def setup_printer_system(selected_printer:list)->str:
    '''
    Selects a printer to be the default for the program
    '''
    printers = list_printers()

    if selected_printer not in printers:
        raise None#ValueError('Printer name not available in Windows printer devices')
    
    current_default_printer = win32print.GetDefaultPrinter()

    if current_default_printer == selected_printer:
        return False#log.info(f"The printer '{selected_printer}' is already set as the default printer.")
        
    
    log.info(f'New Printer: {selected_printer} set!')
    win32print.SetDefaultPrinter(selected_printer)
    
    new_default_printer = win32print.GetDefaultPrinter()
    if new_default_printer == selected_printer:
        return new_default_printer

###################################################################################

def get_attachment_filepath(file_name:str)->str:

    rel_path = os.path.join(__file__,"..","..","..",'EmailScript',"attachments",file_name)
    abs_path = os.path.abspath(rel_path)
    
    if os.path.isfile(abs_path):
        return abs_path
    else:
        raise LookupError(f'Name of file: {file_name} not found...')

def print_pdf(file_name)->None:
    '''
    IMPORTANT Operative system requires a pdf reader set by default (Adobe Reader ,Foxit reader, etc...)
    '''
    
    path_file = get_attachment_filepath(file_name)
    
    if os.path.isfile(path_file):
        try:
            win32api.ShellExecute(
                0,
                "print",
                path_file,
                f"/d'{win32print.GetDefaultPrinter()}'",
                ".",
                0
            )
            return
        except win32api.error as e:
            pass
    else:
        raise LookupError(f'Value Type: {file_name} Not supported. File with given name not found.')

# def wait_for_printer_setup(selected_printer, timeout=60, interval=100):
#     """Wait for the printer setup to complete within the specified timeout."""
#     start_time = time.time()

#     log.info('Setting up Printer. Please wait....')

#     while time.time() - start_time < timeout:
#         printer_name = setup_printer_system(selected_printer)
#         if printer_name:
#             log.info('Printer information resolved!')
#             return printer_name
#         time.sleep(interval)

#     return None

# def set_printer_name(selected_printer):
#     """Ensure the printer setup is complete and return the printer name if successful."""
#     printer_name = wait_for_printer_setup(selected_printer)
#     if printer_name:
#         return printer_name
#     else:
#         log.error('Printer setup not completed within the timeout period.')
#         raise NotImplementedError('Printer Not Set')