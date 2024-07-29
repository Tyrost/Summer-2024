import pygame
import logging as log
from assets.Button import Button
from typing import List

pygame.init()
pygame.font.init()

WWIDTH = 900 # Window Width
WHEIGHT = 600 # Window Height

FONT = pygame.font.Font('API101/Open Trivia API/assets/Lexend-Regular.ttf', 18) # Main Font

screen = pygame.display.set_mode((WWIDTH, WHEIGHT))

master_asset_list = []

### WINDOWS ###

MAIN_MENU = 'main_menu'
CONFIG_MENU = 'config menu'
GAME_MENU = 'game menu'

def switch_window(window, asset_list:List[Button] = master_asset_list):

    for element in asset_list:
        if isinstance(Button, element):
            element.undraw()
    return

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

main_img_path = 'API101/Open Trivia API/assets/main_background.jpg' # Main Image Path
main_img = load_image(main_img_path, (WWIDTH, WHEIGHT)) # pygame Image Object

def screen_fill(img):
    
    try:
        if not img:
            screen.fill((25, 80, 62))
        else:
            screen.blit(img, (0, 0))
    except pygame.error:
        log.warning('display Surface quit')
    return

def append_asset(asset:list)->list:
    global master_asset_list

    for element in asset:
        master_asset_list.append(element)

    return master_asset_list

def del_asset(asset:list)->None:
    
    for i in range(len(asset)):
        for j in master_asset_list:
            if j == asset[i]:
                master_asset_list.pop(i)
    return master_asset_list

### Button Components ###

MAIN_BTN_WIDTH = 150
MAIN_BTN_HEIGHT = 70

# Main Menu
main_start_btn = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2, WHEIGHT/2 - 50, 150, 70, 'Start', FONT, (0,0,0), (250, 250, 250), (100,100,100))
main_quit_btn = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2, WHEIGHT/2 + 50, 150, 70, 'Quit', FONT, (0,0,0), (250, 250, 250), (100,100,100))

# Quit Game Options
quit_confirm_yes = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2 - 220, WHEIGHT/2 + 50, 150, 70, 'Yes', FONT, (0,0,0), (250, 250, 250), (100,100,100))
quit_confirm_no = Button(WWIDTH/2 - MAIN_BTN_WIDTH/2 + 220, WHEIGHT/2 + 50, 150, 70, 'No', FONT, (0,0,0), (250, 250, 250), (100,100,100))