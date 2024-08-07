import json
import os

error_count = 0

credentials_json = 'EmailPrintApp/Setup/credentials.json'
#'Summer-2024/EmailPrintApp/Setup/credentials.json' Win
attachments_dir = 'EmailPrintApp/EmailScript/attachments'
#'Summer-2024/EmailPrintApp/EmailScript/attachments' Win
emails_json = 'EmailPrintApp/EmailScript/emails.json'
#'Summer-2024/EmailPrintApp/EmailScript/emails.json'

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