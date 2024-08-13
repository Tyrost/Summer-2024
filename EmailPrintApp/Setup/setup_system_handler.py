import logging as log
import json

from Setup.SystemicFunctions import *

# Printer #

# def handle_set_printer(selected_printer, file_name):
#     setup_printer_system(selected_printer)
#     print_pdf(file_name)
#     return

# Credentials #

def create_editor(window, text, width, height, font)->PlaceholderTextEditor:
        
    editor = PlaceholderTextEditor(window, text, width, height, font)

    return editor
    
def save_credentials(email_editor:PlaceholderTextEditor, pw_editor:PlaceholderTextEditor, credentials_path:str):
    
    email = email_editor.get_text()
    password = pw_editor.get_text()
    
    new_credentials = {'email': email, 'password': password}
    
    try:
        with open(credentials_path, 'w') as f:
            json.dump(new_credentials, f, indent=2)
    except Exception as e:
        log.warning(f'There was an error: {e}')
        with open(credentials_path, 'w') as f:
            json.dump({'email': None, 'password': None}, f, indent=2)
    
    return email, password

# Excel #

def handle_set_excel_path():
    pass
