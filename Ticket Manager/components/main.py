from auxiliar import *
from Ticket import Ticket
from datetime import datetime

pathFile = './tickets.json'

### MAIN ###

def main(command=None):
    if not command:
        print('')
        command = input('Select Command:\n').strip().lower()
    
    if command == 'c':
        create_user_input()
    elif command == 'r':
        read_user_input()
    elif command == 'cm':
        comment_user_input()
    elif command == 'rp':
        reply_user_input()
    elif command == 'd':
        delete_user_input()
    else:
        print('Command not supported... Please use the -h, --help banner for support.')
        
    print('')
    return

### TASK FUNCTIONS ###

def create(name, message):
    id = create_id()
    while id_exists(id):
        new_id = create_id()
    
    try:
        id = new_id
    except UnboundLocalError:
        id = id
        
    data = Ticket(name, str(datetime.now()), message, id=id)
    data.create_ticket()
    id_jsonify(id)
    
    print(f'Ticket has been successfully created!\nYour ID is {id}')
    return

def read(id:str):
    if not read_find_id(id):
        return
    data = read_find_id(id)
    print('\n*** Customer ***\n')
    padding('Name:', data['name'], 50)
    padding('User ID:', data['id'], 50)
    padding('Time Created:', data['time'], 50)
    print('Message:\n')
    print(control_str_len(data['message'], 50))
    return

def comment(id:str, comment:str):
    comment_post(id, comment)
    print('Comment has successfully been entered.\n')
    
    return
        
def reply(name:str, id:str, txt:str):
    
    user_reply = Ticket(name, str(datetime.now()), txt)

    data = read_data(pathFile)
    
    for post in data:
    
        if post['id'] == id:
            post['reply'].append(user_reply.reply_func())
            break
    

    with open (pathFile, 'w') as f:
        json.dump(data, f, indent=2)
        
    
    print('Reply Sent.')
    
    return

def delete(id:str):
    
    data = read_data(pathFile)
    new_data = []
    
    for post in data:
        
        if post['id'] != id:
            new_data.append(post)

    with open (pathFile, 'w') as f:
        json.dump(new_data, f, indent=2)
        
    return
  
### CHECK MISFITTING ID ###          

def check_id(id):
    if not read_find_id(id):
        if len(id) < 6:
            print('ID must be six characters long')
            return False
        return False
    return True
            
### INPUT INTERACTION FUNCTIONS ###

def create_user_input():
    name = input('What is your name?\n')
    print('')
    msg = input('What is your issue?\n')
    if not check_string(msg):
        return
    print('')
    create(name, msg)
    
    return
    
def read_user_input():
    id = input('Please select ticket by ID:\n')
    if not check_id(id):
        return
    read(id)
    
    return

def comment_user_input():
    id = input('Please select ticket by ID to commment on:\n')
    if not check_id(id):
        return
    
    cmt = input('Please enter your comment on this post.\n')
    comment(id, cmt)
    
    return
    
def reply_user_input():
    user_name = input('What is your name?\n')
    print('')
    id = input('Please select ticket by ID to reply:\n')
    
    if not check_id(id):
        return
    
    print('')
    
    msg = input('Please enter your reply on this post.\n')
    print('')
    reply(user_name, id, msg)
    
    return

def delete_user_input():
    
    id = input('Please select ticket by ID to delete:\n')
    print('')
    
    if not check_id(id):
        return
    
    if warn_delete():
        delete(id)
    
    return


if __name__ == '__main__' :
    main() 
