import json
import os
import re
import time
from pprint import pprint

error_count = 0

credentials_json = 'Summer-2024/EmailPrintApp/Setup/credentials.json'
#'EmailPrintApp/Setup/credentials.json' Mac
attachments_dir = 'Summer-2024/EmailPrintApp/EmailScript/attachments'
#'EmailPrintApp/EmailScript/attachments' Mac
emails_json = 'Summer-2024/EmailPrintApp/EmailScript/emails.json'
#'EmailPrintApp/EmailScript/emails.json' Mac

with open(credentials_json, 'r') as f:
    data = json.load(f)

email_adress = data['email']
password = data['password']

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            return data
    else:
        return []
    
def create_json(path, id, date, subject, body):

    data = load_json(path)
    e_mail = {
        'id': id.decode(),
        'date': date,
        'subject': subject,
        'body': body
    }
    data.append(e_mail)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print('Added email to JSON')

#Thanks ChatGPT :)
def find_data(body: str):
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
    
    extracted_info = {}
    
    for key, pattern in patterns.items():
        match = re.search(pattern, body, re.DOTALL)
        if match:
            if key == 'Billing Address':
                extracted_info[key] = f"{match.group(1).strip()}\n{match.group(2).strip()}\n{match.group(3).strip()}"
            else:
                extracted_info[key] = match.group(1).strip()

    contact_info_pattern = r'(<\+(\d{10})>)\s*(.+?)\n'
    contact_info_match = re.search(contact_info_pattern, body)
    if contact_info_match:
        extracted_info['Contact Info'] = contact_info_match.group(3).strip()

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

