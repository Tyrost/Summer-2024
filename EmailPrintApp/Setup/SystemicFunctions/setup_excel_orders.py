import os
import pandas as pd
import logging as log
import numpy as np
from typing import Union

excel_dir = 'Summer-2024/EmailPrintApp/Setup/ExcelSheet'

def mod_excel_file(name):

    excel_path = f'{excel_dir}/{name}.xlsx'

    if len(os.listdir(excel_dir)) == 0:
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
        return 'created'
    
    elif f'{name}.xlsx' == os.listdir(excel_dir)[0]:
        log.info(f'File Already named: {name}.xlsx')
        return
    
    else:
        log.info('Directory not empty. Modifying file.')
        old_file = os.listdir(excel_dir)[0]
        old_file_path = os.path.join(excel_dir, old_file)
        
        os.rename(old_file_path, excel_path)

        return 'rename'

def input_excel_data(data:Union[dict, list]):

    if isinstance(data, dict):
        if not data:
            raise ValueError("Input dictionary is empty.")
        new_data = np.array(list(data.values())).reshape(1, -1) 
    elif isinstance(data, list):
        if not data:
            raise ValueError("Input list is empty.")
        new_data = np.array(data)
        if new_data.ndim == 1:
            new_data = new_data.reshape(1, -1)
    
    print(new_data)
    print(len(new_data))

    excel_file = os.path.join(excel_dir, os.listdir(excel_dir)[0])
    excel_df = pd.read_excel(excel_file)
    new_row = pd.DataFrame(new_data, columns=excel_df.columns)

    updated_df = pd.concat([excel_df, new_row], ignore_index=True)

    updated_df.to_excel(excel_file, index=False)
    
    log.info('Excel Sheet Updated')
    return