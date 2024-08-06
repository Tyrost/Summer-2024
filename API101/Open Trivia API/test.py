from auxiliary import check_category

config = {
    'category': 9,
    'difficulty': 1,
    'type': 1,
    'amount': 5,
}

def find_category_name():
    category_stack = check_category(config['category'])[0]
    for cat in category_stack:
        if config['category'] == cat['id']:
            return cat['name']
        
def give_diff_name():
    if config['difficulty'] == 1:
        return 'Easy'
    if config['difficulty'] == 2:
        return 'Medium'
    if config['difficulty'] == 3:
        return 'Hard'

def give_type_name():
    if config['type'] == 1:
        return 'any'
    if config['type'] == 2:
        return 'Multiple Choice'
    if config['type'] == 3:
        return 'True or False'

def create_config_matrix():
    matrix = []
    matrix.append(['Category', find_category_name()]) # Category
    matrix.append(['Difficulty', give_diff_name()]) # Difficulty
    matrix.append(['Type', give_type_name()]) # Type
    matrix.append(['Amount', str(config['amount'])]) # Amount of Questions
    return matrix

config_matrix = create_config_matrix()

print(config_matrix)
[['idk', 'idk'], ['idk', 'idk2'], ['idk', 'idk3'], ['idk', 'idk4']]
[['Category', 'General Knowledge'], ['Difficulty', 'Easy'], ['Type', 'Any'], ['Amount', '5']]