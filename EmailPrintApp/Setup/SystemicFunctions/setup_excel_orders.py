import os
import pandas as pd
import logging as log
import numpy as np
from typing import Union

excel_dir = os.path.abspath(os.path.join(os.getcwd(), 'Setup/ExcelSheet')) # Global Excel Directory

def mod_excel_file(name) -> Union[str, None]:
    '''
    Creates the Path to the file given the desired name for it.\n
    If the directory is empty, it will then proceed to create the brand new file.\n
    If a file exists within the global excel directory, check if the name is the same as the desired input name.\n

    Returns:
        The Status of the function's Modification as a string (None if no changes were made).
    '''
    excel_path = f'{excel_dir}/{name}.xlsx' # New Excel Path to the File

    if len(os.listdir(excel_dir)) == 0: # Checks if there is anything inside the directory
        log.info('Creating a brand new file')
        data = {
            'Date': [],
            'Order Number': [],
            'Customer Name': [],
            'Billing Address': [],
            'Contact': [],
            'Quantity': [],
            'Shipping Method': [],
            'Price': [],
            'Payment Method': []
        }

        order_df = pd.DataFrame(data)

        order_df.to_excel(excel_path, index=False)

        return 'created' # Status: Newly Created #
    
    elif f'{name}.xlsx' == os.listdir(excel_dir)[0]: # Checks if the name of the file attempting to add is the same one as the already existent one.
        log.info(f'File Already named: {name}.xlsx')

        return # Status: Unchanged #
    
    else:
        log.info('Directory not empty. Modifying file.') 
        old_file = os.listdir(excel_dir)[0]
        old_file_path = os.path.join(excel_dir, old_file)
        
        os.rename(old_file_path, excel_path) # Renames the file already existent within the directory.

        return 'rename' # Status: Renamed #

def input_excel_data(data:Union[dict, list]):
    '''
    Adds input-specified data into the specified excel file denoted from the `excel_path` local variable.
    '''
    if isinstance(data, dict): # Checks if data is in form of a dictionary.

        if not data:
            raise ValueError("Input dictionary is empty.")
        new_data = np.array(list(data.values())) # COnvert Data into Numpy Array

    elif isinstance(data, list): # Checks if data is in form of a list.

        if not data:
            raise ValueError("Input list is empty.")
        
        new_data = np.array(data)

    excel_path = os.path.join(excel_dir, os.listdir(excel_dir)[0]) # Crates Path
    excel_df = pd.read_excel(excel_path) # Creates Excel-formed DataFrame
    new_row = pd.DataFrame(new_data, columns = excel_df.columns) # Crates Row given the DataFrame

    updated_df = pd.concat([excel_df, new_row], ignore_index=True) # Updates Excel File

    updated_df.to_excel(excel_path, index=False) # Imports to Excel
    
    log.info('Excel Sheet Updated')

    return