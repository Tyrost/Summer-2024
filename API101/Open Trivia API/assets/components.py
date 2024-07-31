import pygame
import logging as log
from assets.Button import Button
from typing import List
import time

pygame.init()
pygame.font.init()

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

def switch_window(stack, window) -> None:
    global master_asset_list
    global screen

    log.info(f'Window switched to `{window}`')
    
    undraw_many(stack)

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
GAME_IMG_PATH = 'API101/Open Trivia API/assets/game_background.jpg'

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


### Configuration Menu ###

back_main_btn = Button(180, 460, 150, 70, 'Back', FONT,(0,0,0), (250, 250, 250), (100,100,100))

### Support Functions ###

# Visibility / Tracking #

def make_visible(stack:List[Button])->None:

    for button in stack:
        if not isinstance(button, Button):
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        button.visible = True
    
    append_asset(stack)
    
def make_invisible(stack:List[Button])->None:
    
    for button in stack:
        if not isinstance(button, Button):
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        button.visible = False

    del_asset(stack)

def draw_many(stack:List[Button], screen)->None:

    for button in stack:
        if not isinstance(button, Button):
            raise TypeError(f'Type: {str(type(button))} not accepted. Stack must contain only button instances')
        if button.visible:
            button.draw(screen)
            append_asset([button])

def undraw_many(stack) -> None:
    for button in stack:
        if not isinstance(button, Button):
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