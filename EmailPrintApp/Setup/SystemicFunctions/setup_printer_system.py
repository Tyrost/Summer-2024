import os
import logging as log
import sys
from win32 import win32print,win32api

#_________________________________________________________ Printer Setup _________________________________________________________#

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
        log.warn('Printer name not available in Windows printer devices')
        return None
    
    current_default_printer = win32print.GetDefaultPrinter()

    if current_default_printer == selected_printer:
        return False 
    
    log.info(f'New Printer: {selected_printer} set!')
    win32print.SetDefaultPrinter(selected_printer)
    
    new_default_printer = win32print.GetDefaultPrinter()
    if new_default_printer == selected_printer:
        return new_default_printer

#__________________________ Printing Execution / Parsing __________________________# 

def get_attachment_filepath(file_name:str)->str:
    '''
    This function constructs the file path for an attachment based on the\n
    provided file name using the current working directory. It then\n 
    checks if the file exists at the constructed path. If the file exists, the\n 
    absolute path is returned. Otherwise, an error is raised.
    '''
    rel_path = os.path.join(os.getcwd(), 'EmailScript', 'attachments', file_name)
    abs_path = os.path.abspath(rel_path)
    
    if os.path.isfile(abs_path):
        return abs_path
    else:
        raise LookupError(f'Name of file: {file_name} not found...')

def print_pdf(file_name)->None:
    '''
    This function sends a PDF file to the default printer set up on the system.\n
    `It requires the operating system to have a PDF reader (like Adobe Reader, Foxit Reader, etc.)`\n
    set as the default program for handling PDFs. The function locates the file using
    the `get_attachment_filepath` function, and if the file exists, it attempts to print 
    it using the Windows ShellExecute API.
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