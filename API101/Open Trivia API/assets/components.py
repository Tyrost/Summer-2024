import pygame
import logging as log
from assets.Assets import Button, TriangleButton, Table
from typing import List, Union
from auxiliary import check_category

pygame.init()
pygame.font.init()

display_window_message = ''

### Master Asset Tracker ###

master_asset_list = set()

def append_asset(stack:list)->list:
    global master_asset_list
    if isinstance(stack, list):
        master_asset_list.update(stack)
    else:
        master_asset_list.add(stack)


def del_asset(stack:list)->None: 
    global master_asset_list
    if isinstance(stack, list):
        master_asset_list.difference_update(stack)
    else:
        master_asset_list.discard(stack)

### WINDOWS ###

MAIN_MENU = 'main_menu'
CONFIG_MENU = 'config menu'
GAME_MENU = 'game menu'

WWIDTH = 900 # Window Width
WHEIGHT = 600 # Window Height

screen = pygame.display.set_mode((WWIDTH, WHEIGHT))

def switch_window(stack:List[Union[Button, TriangleButton, Table]], window) -> None:
    '''
    When switching windows this functions undraws all of the passed stack elements.
    Also makes the items visible in case of window switch-back.
    '''
    global master_asset_list
    global screen

    log.info(f'Window switched to `{window}`')
    
    undraw_many(stack)
    make_visible(stack)

def get_current_image(window):

    if window == MAIN_MENU:
        return main_img
    elif window == CONFIG_MENU:
        return config_img
    elif window == GAME_MENU:
        return game_img

# GLOBAL / DEFAULT FONT # 

FONT = pygame.font.Font('API101/Open Trivia API/assets/Lexend-Regular.ttf', 18) # Main Font

### Load Image Components ###

def load_image(path:str, scaling:tuple) -> pygame.Surface:
    '''
    Relative path
    '''
    try:
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, scaling)
        return image

    except Exception as e:
        log.warning(f'Error while loading image execution. Error: {e}')
        return None

MAIN_IMG_PATH = 'API101/Open Trivia API/assets/main_background.jpg' # Main Image Path
CONFIG_IMG_PATH = 'API101/Open Trivia API/assets/config_background.png' # Config Image Path
GAME_IMG_PATH = 'API101/Open Trivia API/assets/game_background.jpg' # Game Image Path

# pygame Image Objects
try:
    main_img = load_image(MAIN_IMG_PATH, (WWIDTH, WHEIGHT)) 
    config_img = load_image(CONFIG_IMG_PATH, (WWIDTH, WHEIGHT))
    game_img = load_image(GAME_IMG_PATH, (WWIDTH, WHEIGHT))
except Exception:
    log.warning('Could not load one or more background images.')

def screen_fill(img):
    
    try:
        if not img:
            screen.fill((25, 80, 62))
        else:
            screen.blit(img, (0, 0))
    except pygame.error:
        log.warning('display Surface quit')
    return

### Button Components ###

MAIN_BTN_WIDTH = 150
MAIN_BTN_HEIGHT = 70

### Main Menu ###
main_start_btn = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2, WHEIGHT/2 - 50, 150, 70, 'Start', FONT, (0,0,0), (250, 250, 250), (100,100,100))
main_quit_btn = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2, WHEIGHT/2 + 50, 150, 70, 'Quit', FONT, (0,0,0), (250, 250, 250), (100,100,100))

# Quit Game Options
quit_confirm_yes = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2 - 120, WHEIGHT/2, 150, 70, 'Yes', FONT, (0,0,0), (250, 250, 250), (100,100,100))
quit_confirm_no = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2 + 120, WHEIGHT/2, 150, 70, 'No', FONT, (0,0,0), (250, 250, 250), (100,100,100))

MAIN_WINDOW_ASSETS = [main_start_btn, main_quit_btn, quit_confirm_yes, quit_confirm_no]

### Configuration Menu ###

config = {
    'category': 1,
    'difficulty': 1,
    'type': 1,
    'amount': 5,
}

category_dict = check_category(config['category'])[0]['trivia_categories']['id'][config['category']]

config_matrix = [['Category', category_dict]]

back_main_btn = Button(180, 460, 150, 70, 'Back', FONT,(0,0,0), (250, 250, 250), (100,100,100))

#vvv +90 pixels padding from last button vvv#

# Category # 0 
category_left = TriangleButton([(WWIDTH - 320, 130), (WWIDTH - 320, 200), (WWIDTH - 370, 165)], 'Left Category', (250, 250, 250), (100,100,100))
category_btn = Button(WWIDTH - 310, 130, 150, 70, 'Category', FONT,(0,0,0), (250, 250, 250), (100,100,100), c_hover=False)
category_right = TriangleButton([(WWIDTH - 150, 130), (WWIDTH - 150, 200), (WWIDTH - 100, 165)], 'Right Category', (250, 250, 250), (100,100,100))

# Difficulty # 1
difficulty_left = TriangleButton([(WWIDTH - 320, 130 + 90), (WWIDTH - 320, 200 + 90), (WWIDTH - 370, 165 + 90)], 'Left Difficulty', (250, 250, 250), (100,100,100))
difficulty_btn = Button(WWIDTH - 310, 130 + 90, 150, 70, 'Difficulty', FONT,(0,0,0), (250, 250, 250), (100,100,100), c_hover=False)
difficulty_right = TriangleButton([(WWIDTH - 150, 130 + 90), (WWIDTH - 150, 200 + 90), (WWIDTH - 100, 165 + 90)], 'Right Difficulty', (250, 250, 250), (100,100,100))

# Type # 2
type_left = TriangleButton([(WWIDTH - 320, 130 + 90 * 2), (WWIDTH - 320, 200 + 90 * 2), (WWIDTH - 370, 165 + 90 * 2)], 'Left Type', (250, 250, 250), (100,100,100))
type_btn = Button(WWIDTH - 310, 130 + 90 * 2, 150, 70, 'Type', FONT,(0,0,0), (250, 250, 250), (100,100,100), c_hover=False)
type_right = TriangleButton([(WWIDTH - 150, 130 + 90 * 2), (WWIDTH - 150, 200 + 90 * 2), (WWIDTH - 100, 165 + 90 * 2)], 'Right Type', (250, 250, 250), (100,100,100))

# Amount of Q's # 3
number_left = TriangleButton([(WWIDTH - 320, 130 + 90 * 3), (WWIDTH - 320, 200 + 90 * 3), (WWIDTH - 370, 165 + 90 * 3)], 'Left Amount', (250, 250, 250), (100,100,100))
number_btn = Button(WWIDTH - 310, 130 + 90 * 3, 150, 70, 'Amount', FONT,(0,0,0), (250, 250, 250), (100,100,100), c_hover=False)
number_right = TriangleButton([(WWIDTH - 150, 130 + 90 * 3), (WWIDTH - 150, 200 + 90 * 3), (WWIDTH - 100, 165 + 90 * 3)], 'Right Amount', (250, 250, 250), (100,100,100))

config_table = Table(screen, (200, 150), FONT, (0, 0, 0), config_matrix, 3)

CONFIG_WINDOW_ASSETS = [back_main_btn, category_btn, category_left, category_right, difficulty_btn, difficulty_left, difficulty_right, type_btn, type_left, type_right ,number_btn, number_left, number_right, config_table]

### Support Functions ###

# Visibility / Tracking #

def make_visible(stack:List[Button])->None:

    for button in stack:
        if type(button) not in [Button, TriangleButton, Table]:
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        button.visible = True
    
    append_asset(stack)
    
def make_invisible(stack:List[Button])->None:
    
    for button in stack:
        if type(button) not in [Button, TriangleButton, Table]:
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        button.visible = False

    del_asset(stack)

def draw_many(stack:List[Union[Button, TriangleButton, Table]], screen)->None:

    for button in stack:
        if type(button) not in [Button, TriangleButton, Table]:
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        if button.visible:
            button.draw(screen)
            append_asset([button])

def undraw_many(stack:List[Union[Button, TriangleButton, Table]]) -> None:
    for button in stack:
        if type(button) not in [Button, TriangleButton, Table]:
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        if button.visible:
            button.undraw()
            del_asset([button])

# Quitting #

def quit_command_ex(event):

    if quit_confirm_yes.isclicked(event):
        log.info('Ending game...')
        return True
    
    if quit_confirm_no.isclicked(event):
        log.info('Action retracted, canceling...')
        make_visible([main_start_btn, main_quit_btn])
        make_invisible([quit_confirm_yes, quit_confirm_no])
        return False