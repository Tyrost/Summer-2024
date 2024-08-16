
from typing import Union
import logging as log
import json
import os
import re
import time

#_______________________________________________________ Support Module (Main Script) _______________________________________________________#

error_count = 0

credentials_json = os.path.abspath(os.path.join(os.getcwd(), 'Setup/credentials.json')) # Absolute Path to User Credential Storage

attachments_dir = os.path.abspath(os.path.join(os.getcwd(), 'EmailScript/attachments')) # Absolute Path to Program's Attachment Directory

emails_json = os.path.abspath(os.path.join(os.getcwd(), 'EmailScript/emails.json')) # Absolute Path to Program's Email DB Directory

with open(credentials_json, 'r') as f: # Open Credentials
    data = json.load(f)

# Store Credentials

email_address = data['email']
password = data['password']

def load_json(path:str) -> Union[dict, list]:
    '''
    Loads JSON data from a given path.
    '''
    if os.path.exists(path): # Checks that JSON file is existent

        with open(path, 'r') as f:
            data = json.load(f)
            return data
    else:
        return [] # Generates an empty array to initialize storage, if empty.
    
def create_json(path:str, id:bytes, date:str, subject:str, body:str) -> None:
    '''
    This function loads an existing JSON file, appends the details of a new email\n
    to it, and then saves the updated data back to the file. The email details include\n
    the email ID, date, subject, and body.\n

    Args:
        path (str): The file path to the JSON file where email details are stored.
        id (bytes): The identifier of the email, which is decoded to a string.
        date (str): The date the email was received.
        subject (str): The subject line of the email.
        body (str): The body content of the email.
    '''
    data = load_json(path) # Load existent data
    e_mail = {
        'id': id.decode(),
        'date': date,
        'subject': subject,
        'body': body
    }
    data.append(e_mail)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    log.info('Added email to JSON')

#Thanks ChatGPT :)

def find_data(body: str) -> dict:
    '''
    This function parses the body of an email to extract specific details such as the date,\n
    order number, customer name, billing address, contact information, quantity, shipping\n
    method, price, and payment method. The extracted data is organized into a dictionary\n 
    and returned.
    '''
    # Define regex patterns for each piece of information

    patterns = {
        'Date': r'Date:\s*(.+?)\n',
        'Order Number': r'Order #(\d+)',
        'Customer Name': r'You’ve received the following order from (.+?):',
        'Billing Address': r'Billing address\s*(.+?)\n\s*(.+?)\n\s*(\d{6})\n\s*\(\+\d{2}\)\d{8}\s*<\+\d{10}>',
        'Quantity': r'Quantity:\s*(\d+)',
        'Shipping Method': r'Shipping:\s*(.+?)\n',
        'Price': r'Total:\s*\$([\d\.]+)',
        'Payment Method': r'Payment method:\s*(.+?)\n'
    }
    
    # Extract information using regex patterns

    extracted_info = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, body, re.DOTALL)
        if match:
            if key == 'Billing Address':
                extracted_info[key] = f"{match.group(1).strip()}\n{match.group(2).strip()}\n{match.group(3).strip()}"
            else:
                extracted_info[key] = match.group(1).strip()

    # Extract contact information separately
    contact_info_pattern = r'(<\+(\d{10})>)\s*(.+?)\n'
    contact_info_match = re.search(contact_info_pattern, body)
    if contact_info_match:
        extracted_info['Contact Info'] = contact_info_match.group(3).strip()

    # Apply extracted information into the resultant dictionary
    ordered_info = {
        'Date': extracted_info.get('Date'),
        'Order Number': extracted_info.get('Order Number'),
        'Customer Name': extracted_info.get('Customer Name'),
        'Billing Address': extracted_info.get('Billing Address'),
        'Contact': extracted_info.get('Contact Info'),
        'Quantity': extracted_info.get('Quantity'),
        'Shipping Method': extracted_info.get('Shipping Method'),
        'Price': extracted_info.get('Price'),
        'Payment Method': extracted_info.get('Payment Method'),
    }

    time.sleep(3)

    return ordered_info

