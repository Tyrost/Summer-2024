from auxiliary import *
import logging  as log

log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = 'https://opentdb.com/api.php?'

def get_trivia(amount:int, category:int=None, diff:str=None, type:str=None):
    '''
    Initializes the http link to the API that will direct the program to the JSON containing trivia questions.
    It logs the configurations of desired type of gameplay.
    '''
    if not check_amount(amount):
        log.error(f'\n\n\nLog: Question amount request not satisfied... OK {CROSS_MARK}\n')
        raise ValueError('Amount of questions must not exceed 50')
    
    log.info(f'\n\n\nLog: Question amount request satisfied... OK {CHECK_MARK}')
    
    url = f'{BASE_URL}amount={str(amount)}'
    try:

        if category is not None: 
            if check_category(category)[1]:
                url += f'&category={category}'
                log.info('Log: Category set... Condtions satisfied.')
            else:
                log.warning(f'Category {category} not supported')
        else:
            log.info(f'Log: Category not set... Conditions satisfied. OK {CHECK_MARK}')
            
        if diff is not None:
            if check_diff(diff):
                url += f'&difficulty={diff}'
                log.info('Log: Difficulty set... Condtions satisfied.')
            else:
                log.warning(f'Difficulty {diff} not supported')
        else:
            log.info(f'Log: Difficulty not set... Conditions satisfied. OK {CHECK_MARK}')
        
        if type is not None:
            if check_type(type):
                url += f'&type={type}'
                log.info('Log: Type set... Condtions satisfied.')
            else:
                log.warning('Type of gameplay not supported!')
        else:
            log.info(f'Log: Type not set... Conditions satisfied. OK {CHECK_MARK}')
        
        return url
    
    except Exception as error:
        log.fatal(f'\n\n\nFatal error ocurred. The program may not continue.\n\n\n')
        print(f'There was an error when getting trivia information. Error:\n {error}')
        return
    
if __name__ =='__main__':
    print(get_trivia(20))