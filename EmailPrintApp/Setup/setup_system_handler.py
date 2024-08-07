import logging as log
import json
from Setup.SystemicFunctions.input_excel_orders import *
from Setup.SystemicFunctions.set_credentials import PlaceholderTextEditor
# from SystemicFunctions.setup_printer_system import *

# All Courtesy of ChatGPT :)

# def handle_set_printer():
#     printer_name = set_printer_name()
#     return printer_name

def credential_obj(window, text:list, x, y, width, height, font, current_frame, target_frame):
        
    email_editor = PlaceholderTextEditor(window, text[0], x, y[0], width, height, font)
    pw_editor = PlaceholderTextEditor(window, text[1], x, y[1], width, height, font)
    
    if current_frame != target_frame:
        email_editor.pack_forget()
        pw_editor.pack_forget()
    
    return email_editor, pw_editor
    
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



def handle_set_excel_path():
    pass
