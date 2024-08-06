from EmailScript.support import *
import imaplib
import email
import os
import time

def decode_part(part):
    try:
        return part.get_payload(decode=True).decode('utf-8')
    except UnicodeDecodeError:
        try:
            return part.get_payload(decode=True).decode('iso-8859-1')
        except UnicodeDecodeError:
            return part.get_payload(decode=True).decode('windows-1252')

def get_message_body_and_attachments(message):
    body = ''
    attachments = []
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    attachments.append((filename, part.get_payload(decode=True)))
            elif (content_type == "text/plain") and ("attachment" not in content_disposition):
                body += decode_part(part)
    else:
        body = decode_part(message)
    return body, attachments

if not os.path.isdir(attachments_dir):
    os.makedirs(attachments_dir)

def read_email_script(running, stop_event):
    '''
    Searches for UNSEEN emails only
    '''
    global error_count

    print('Starting...')
    while running and not stop_event.is_set():
        try:
            status = 'Running'
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(email_adress, password)
            mail.select(readonly=False)

            status, message_ids = mail.search(None, 'UNSEEN')

            if status != 'OK':
                print("No messages found!")
                mail.logout()
                continue

            for message_id in message_ids[0].split():
                status, message_data = mail.fetch(message_id, '(RFC822)')
                if status != 'OK':
                    print(f"Failed to fetch message with ID {message_id}")
                    continue

                actual_message = email.message_from_bytes(message_data[0][1])

                email_date = actual_message["Date"]
                subject = actual_message["Subject"]
                message_body, attachments = get_message_body_and_attachments(actual_message)
                
                create_json(emails_json, message_id, email_date, subject, message_body)

                for filename, content in attachments:
                    filepath = os.path.join(attachments_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"Attachment saved: {filepath}")

                print("=" * 50)

                status, _ = mail.store(message_id, '+FLAGS', '\\Seen')
                if status != 'OK':
                    print(f"Failed to mark message with ID {message_id} as seen")

            mail.close()
            mail.logout()

        except Exception as e:
            print(f'An error occurred:\n{e}')
            error_count += 1
            if error_count == 3:
                return
            time.sleep(60)
            print('Running...')
    
    print('Connection Ended')
