from auxiliary import check_category
from pprint import pprint
import logging as log

config = {
    'category': 11,
    'difficulty': 1,
    'type': 1,
    'amount': 5,
}

### WORK IN PROGRESS ###

# Getting Category Information Given the JSON's API response with ID as a key to access category name #

if check_category(config['category'])[1]:
    log.info('Category not available')
category_dict = check_category(config['category'])[0]#['id'][config['category']]

# config_matrix = [['Category', category_dict]]

# print(config_matrix)
pprint(category_dict)