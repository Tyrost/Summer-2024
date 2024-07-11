import json
import os

pathFile = './tickets.json'

def file_exists(path)->bool:
    return os.path.exists(path)

class Ticket:
    
    name:str
    ID:str
    Time:str
    Message:str
    Comment:None
    Reply:None
    
    def __init__(self, name, time, message, id = None) -> None: 
        self.name = name
        self.id = id
        self.time = time
        self.msg = message
        self.comment = None
        self.reply = []
    
    def _get_all_json(self):
        if file_exists(pathFile):
            with open(pathFile, 'r') as f:
                data = json.load(f)
                return data
        else:
            print('File cannot be read. File does not eixist.')

    def _jsonify(self) -> None:
        try:
            tkt = {
                'name': self.name,
                'time': self.time,
                'message': self.msg,
                'comment': self.comment,
                'reply': self.reply
            }
            if self.id is not None:
                tkt['id'] = self.id
                
            if not (file_exists(pathFile)): 
            ### IF PATH DOES NOT YET EXIST ###
                init_list = []
                init_list.append(tkt)
                with open(pathFile, 'w') as f:
                    json.dump(init_list, f, indent=2)
           
            else:       
            ### IF PATH ALREADY EXISTS ###
                data:list = self._get_all_json()
                data.append(tkt)
                with open(pathFile, 'w') as f:
                    json.dump(data, f, indent=2)
                          
        except Exception as error:
            print(f'There was an error when dumping json. Error: {error}') 
                                   
    def create_ticket(self) -> None:
        self._jsonify()
        return

    def comment_ticket(self, comment) -> None:
        self.comment = comment
    
    def reply_func(self) -> None:
        if not file_exists(pathFile):
            raise FileExistsError ('File does not exist')
        
        tkt_reply = {
            'name': self.name,
            'time': self.time,
            'message': self.msg,
        }
        
        return tkt_reply
        
        
if __name__ == '__main__':  
    pass

