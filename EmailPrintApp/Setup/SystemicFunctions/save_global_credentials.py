from components.Classes.TextEditor import TextEditor
import logging as log
import json

def save_credentials(email_editor:TextEditor, pw_editor:TextEditor, credentials_path:str):
    '''
    This function retrieves the email and password from two `TextEditor` instances\n 
    and saves them as a dictionary to a JSON file at the specified path. If an error\n 
    occurs during the file write operation, it logs a warning and saves `None` values\n 
    for both the email and password instead.
    '''
    email = email_editor.get_text()
    password = pw_editor.get_text()
    
    new_credentials = {'email': email, 'password': password}
    
    try:
        with open(credentials_path, 'w') as f:
            json.dump(new_credentials, f, indent = 2)

    except Exception as e:
        log.warning(f'There was an error: {e}')
        with open(credentials_path, 'w') as f:
            json.dump({'email': None, 'password': None}, f, indent = 2)
    
    return email, password