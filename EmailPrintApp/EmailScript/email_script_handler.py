
from Setup.SystemicFunctions import *  # !Package! For `input_excel_data` & `print_pdf` Functions
from EmailScript.support import * # !Module! Imports Support  

from typing import Tuple
import logging as log
import email.message
import threading
import imaplib
import pdfkit
import email
import os
import time

#____________________________________________________________ Main Script Module ____________________________________________________________ #

def convert_html_to_pdf(html_content:str, pdf_file_path:str) -> None:
    '''
    Converts the given HTML content to a PDF file.
    '''
    try:
        
        pdfkit.from_string(html_content, pdf_file_path)
        log.info(f"PDF generated and saved at {pdf_file_path}")

    except Exception as e:
        log.warning(f"PDF generation failed: {e}")

    return

def decode_part(part:email.message.EmailMessage) -> str:
    '''
    Decodes the payload of an email message part into a string.\n
    The Function attempts to decode the payload message using 'utf-8'.\n
    If there is a failure, it then attempts 'iso-8859-1' then 'windows-1252'.
    '''
    try:

        return part.get_payload(decode=True).decode('utf-8')
    
    except UnicodeDecodeError:
        try:

            return part.get_payload(decode=True).decode('iso-8859-1')
        
        except UnicodeDecodeError:

            return part.get_payload(decode=True).decode('windows-1252')

def get_message_body_and_attachments(message:email.message.EmailMessage) -> Tuple[str, list]:
    '''
    Extracts the body text and attachments from an email message.
    '''
    body = ''
    attachments = []
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                filename = part.get_filename()
                
                if filename:
                    attachments.append((filename, part.get_payload(decode = True)))

            elif (content_type == "text/plain") and ("attachment" not in content_disposition):
                body += decode_part(part)
    else:
        body = decode_part(message)
    return body, attachments

if not os.path.isdir(attachments_dir):
    os.makedirs(attachments_dir)

#________________________________ Main Script ________________________________#

def read_email_script(running:bool, stop_event:threading.Event, callback = None) -> None:
    '''
    Monitors an email inbox for new messages and processes them.

    This function continuously checks for unseen emails in the inbox,\n
    processes them if they meet certain criteria, and handles attachments and \n
    specific data extraction. The function will stop monitoring when the\n
    `running` flag is set to `False` or when the `stop_event` is triggered.\n
    '''
    global error_count # Track Errors

    log.info('Starting...')
    while running and not stop_event.is_set(): # Stops when `running` variable is False, and when the Stop Threading Event is not set.
        try:
            status = 'Running'
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_address, password)
            mail.select(readonly = False)

            status, message_ids = mail.search(None, 'UNSEEN')

            if status != 'OK':
                log.info("No messages found!")
                mail.logout()
                continue

            for message_id in message_ids[0].split():
                status, message_data = mail.fetch(message_id, '(RFC822)')

                if status != 'OK':
                    log.warning(f"Failed to fetch message with ID {message_id}")
                    continue
                
                ### ESSENTIAL IMPLEMENTATION HERE ###

                actual_message = email.message_from_bytes(message_data[0][1])

                email_date = actual_message["Date"] # Get Date
                subject = actual_message["Subject"] # Get Email's Subject

                if ('New Order' in subject): # Only Execute Script if subject contains the string 'New Order'.

                    message_body, attachments = get_message_body_and_attachments(actual_message) # Get Data: Body and Attachments
                    create_json(emails_json, message_id, email_date, subject, message_body) # Create JSON to dump email details
                
                    for filename, content in attachments:
                        filepath = os.path.join(attachments_dir, filename)

                        with open(filepath, 'wb') as f:
                            f.write(content)

                        log.info(f"Attachment saved: {filepath}")

                        if attachments is not None:
                            print_pdf(attachments) # Prints PDF if attachment is existent
                    else:
                        data = find_data(message_body) # Finds data
                        input_excel_data(data) # Inputs data into Excel

                    log.info("=" * 50)

                    status, _ = mail.store(message_id, '+FLAGS', '\\Seen')

                    if status != 'OK':
                        log.warning(f"Failed to mark message with ID {message_id} as seen")

            mail.close()
            mail.logout()

        except ValueError as e:
            log.warning(e)
            log.warning('Email setup not yet set...')

            if callback:
                callback(None)
            return
        
        except Exception as e: # Possible Wrong Credentials Set. Includes Instructions for Troubleshooting.
            log.warning(f'An error occurred\nPerhaps it has to do with credentials.\nPlease navigate to MainMenu > SetUp > Set Email and read the instructions carefully.\n\nError:\n{e}\n\nRetrying in 30 seconds...\n')
            error_count += 1
            # If there are 3 errors, the program will end
            if error_count == 3:
                log.info('Ended...\n')
                if callback:
                    callback(None)
                return
            
            time.sleep(30)
            log.info('Running...\n')
    
    log.info('Connection Ended\n')
    return
