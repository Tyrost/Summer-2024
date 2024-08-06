import requests
from typing import Union

CHECK_MARK = '\033[32m\u2714\033[0m'
CROSS_MARK = '\033[31m\u2716\033[0m' 

category_cache = None

def check_amount(amount:Union[int, str])->bool:
    '''
    Guardian code function that returns a boolean value.
    Checks input, integer, to verify that it is the correct data type, and that the amount
    is not greater than 50.
    '''
    result = (isinstance(amount, str) or isinstance(amount, int)) # Checks that input is a string or an integer #
    if amount > 50: # Checks that amount is not greater than 50 #
        return False
    return result

def check_category(category:str)->tuple:
    global category_cache
    '''
    Guardian code function that returns a tuple value.
    Checks the string category for its data type and that it is included within the API's JSON response.
    Checks that response status code is not other than 200. For simplicity matters, it will create an raise an error
    alerting the type of status code.
    This function returns a tuple that holds the JSON response if needed later on,
    and it holds the boolean value checking existance within the response.
    '''
    # Check data type
    if not isinstance(category, int): 
        return False

    if category_cache is None:
        # Send API request
        response = requests.get('https://opentdb.com/api_category.php')
        
        # Checks that response code is only 200. Returns an error otherwise.
        if response.status_code != 200: 
            return f'Error {response.status_code}', False
        
        # Creastes the JSON representation of the http response
        category_cache = response.json()['trivia_categories']
    
    exists = any(cat['id'] == category for cat in category_cache)
    # Return JSON and boolean that checks for existance
    return category_cache, exists


def check_diff(diff:str)->bool:
    '''
    Simple function that returns a boolean based on the input string.
    Checks to see that the string is held in the options of `easy`, `medium` or `hard` 
    '''
    options = ['easy', 'medium', 'hard']
    
    return diff in options

def check_type(type:str)->bool:
    '''
    Simple function that returns a boolean based on the input string.
    Checks to see that the string is held in the options of `any`, `multiple` or `boolean` 
    '''
    choices = ['any', 'multiple', 'boolean']

    return type in choices
