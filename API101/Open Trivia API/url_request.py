from auxiliary import *

base_url = 'https://opentdb.com/api.php?'

def get_trivia(amount:int, category:int=None, diff:str=None, type:str=None):
    if not check_amount(amount):
        print('Amount of questions must not exceed an amount of 50!')
        return
    
    url = f'{base_url}amount={str(amount)}'
    try:

        if category is not None: 
            if check_category(category)[1]:
                url += f'&category={category}'
            else:
                print(f'Category {category} not supported')
            
        if diff is not None:
            if check_diff(diff):
                url += f'&difficulty={diff}'
            else:
                print(f'Difficulty {diff} not supported')
        
        if type is not None:
            if check_type(type):
                url += f'&type={type}'
            else:
                print('Type of gameplay not supported!')
        
        return url
    
    except Exception as error:
        print(f'There was an error when getting trivia information. Error: {error}')
        return
    
if __name__ =='__main__':
    pass