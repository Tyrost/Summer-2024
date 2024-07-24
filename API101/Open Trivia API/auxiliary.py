import requests
from colorama import Fore, Style, init

CHECK_MARK = '\033[32m\u2714\033[0m'  # Check mark
CROSS_MARK = '\033[31m\u2716\033[0m'  # Cross mark

def check_amount(amount):
    result = (isinstance(amount, str) or isinstance(amount, int))
    if amount > 50:
        result = False
    return result

def check_category(category:str):
    
    categories_json = requests.get('https://opentdb.com/api_category.php')

    if categories_json.status_code != 200:
        return f'Error {categories_json.status_code}', False
    
    response = categories_json.json()['trivia_categories']
    
    return response, any(cat['id'] == category for cat in response)

def check_diff(diff):
    options = ['easy', 'medium', 'hard']

    return diff in options

def check_type(type):
    choices = ['any', 'multiple', 'boolean']

    return type in choices
