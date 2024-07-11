from random import randint, choice
import json
import os

pathFile = './id.json'
alphabet = 'A C D E F G H I J K L M N O P Q R S T U V W X Y Z'

def padding(str1, str2, space):
    
    between_spc = space - len(str1) - len(str2)
    
    print(str1 + ' '*between_spc + str2)
    return


description = ('Manager for ticketing system to assist clients with IT related problems. \
    options include creating a ticket, reading a ticket, commenting, replying, resolving and deleting' )

def help():
    pad = 30
    print(
    '*** TICKETING OPTIONS ***')
    padding('Create Ticket', 'C', pad) 
    padding('Read Ticket', 'RD', pad)
    padding('Comment Ticket', 'CM', pad)
    padding('Reply Ticket', 'R', pad)
    padding('Resolve/Clear Ticket', 'L', pad)
    return

def control_str_len(string:str, max_len:int):
    lines = []
    current_line = ''
    
    for i, char in enumerate(string):
        if char.isspace():
            if len(current_line) + len(char) <= max_len:
                current_line += char
            else:
                lines.append(current_line.strip())
                current_line = ''
        else:
            if len(current_line) + len(char) <= max_len:
                current_line += char
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = char
    
    if current_line:
        lines.append(current_line.strip())
    
    return '\n'.join(lines)
            
def file_exists(path)->bool:
    return os.path.exists(path)

def create_id():
    id = ''
    for i in range(6):
        chance = randint (0, 2)
        if chance != 2:
            id += str(randint(0, 9))
        else:
            id += choice(alphabet.split(' '))
    return id

def read_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

### ID DB ###

def id_jsonify(id)->None:
    if not file_exists(pathFile):
        id_dict = {
            'id': [id]
        }
        with open (pathFile, 'w') as f:
            json.dump(id_dict, f, indent=2)
    else:
        with open (pathFile, 'r') as f:
            data = json.load(f)
        data['id'].append(id)
        with open (pathFile, 'w') as f:
            json.dump(data, f, indent=2)
            
def id_exists(id) ->bool:
    if not file_exists(pathFile):
        return False
    with open (pathFile, 'r') as f:
        data = json.load(f)
        
    for id_element in data['id']:
        if id == id_element:
            return True
        
    return False

def read_find_id(id:str):
    ticket_file_path = './tickets.json'
    if file_exists(ticket_file_path):
        data = read_data(ticket_file_path)

        for i in range(len(data)):
            if data[i]['id'] == id:
                data = data[i]
                return data
        print('No ID found...\n')
        return False
    else:
        print('File does not exist')
        return
    
def comment_post(id:str, comment):
    
    try:
        
        data = read_data('./tickets.json')
    
    except FileNotFoundError:
        
        print('File does not exist. Please initialize before commenting.\n')
        print('')
        return
    
    if read_find_id(id) is None:
        
        return
    
    for post in data:
        
        if post['id'] == id:
            
            post['comment'] = comment
            break
    
    with open('./tickets.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    return   
        
def warn_delete():
    
    option = input('Are you sure you would like to remove this ticket? (y/n)\n')
    print('\n')
    
    if option == 'y':
        print('Ticket Deleted...\n')
        return True
    
    else:
        print('Deletion Canceled.\n')
        return False

def check_string(s):
    if len(s) < 10:
        print('Not a valid message.')
        return False
    return True