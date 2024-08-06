import pygame
from assets.components import *
from url_request import get_trivia, CHECK_MARK
import logging as log
import time

current_window = MAIN_MENU
quit_flag = False
running = True

config_matrix = create_config_matrix()
config_table = Table(screen, (200, 150), FONT, (0, 0, 0), config_matrix, 4)

def update_config(new_config):
    global config
    global config_matrix

    config.update(new_config)
    config_matrix = create_config_matrix()
    config_table.text = config_matrix

def main():
    global current_window
    global master_asset_list
    global running
    global quit_flag

    start_time = time.time()

    pygame.display.set_caption('Trivia Game')

    while running:

        current_img = get_current_image(current_window)

    # TIME TRACKER
    
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= 1.5:
            log.info(config_matrix) # Test goes HERE!
            start_time = current_time
        
    ### Terminate Game Event ###

        for event in pygame.event.get(): # Event Manager (ESSENTIAL)
            if event.type == pygame.QUIT:
                running = False

    ### Main Image Filling ###

        screen_fill(current_img)

    ### Main Button Events ###

        if current_window == MAIN_MENU:

            handle_main_menu(event)

        elif current_window == CONFIG_MENU:
            
            handle_config_window(event)

        elif current_window == GAME_MENU:
            
            handle_game_window(event)

        pygame.display.update() # Update Changes

    pygame.quit()
    log.info('Game terminated.')

def handle_main_menu(event):
    global running
    global current_window
    global quit_flag
    global MAIN_WINDOW_ASSETS

    # Draw any possible usable buttons within the main menu window
    draw_many(MAIN_WINDOW_ASSETS, screen)

    # Start with visibility to quit confirmation buttons = False
    if not quit_flag:
        make_invisible([quit_confirm_yes, quit_confirm_no])

    if main_start_btn.isclicked(event): # Start Game Button
        log.info(f'Start Button Clicked.')
        current_window = CONFIG_MENU

        switch_window(MAIN_WINDOW_ASSETS, CONFIG_MENU)
        quit_flag = False
        
    if main_quit_btn.isclicked(event): # Quit Game Event
        log.info(f'Quit Button Clicked.')

        make_invisible([main_start_btn, main_quit_btn])
        make_visible([quit_confirm_yes, quit_confirm_no])

        quit_flag = True
    
    if quit_flag and quit_command_ex(event): 
        running = False    

def handle_config_window(event):
    global config
    global current_window
    global display_window_message
    global CONFIG_WINDOW_ASSETS

    draw_many(CONFIG_WINDOW_ASSETS, screen)

    if back_main_btn.isclicked(event):
        log.info('Back to main menu...')
        current_window = MAIN_MENU

        switch_window(CONFIG_WINDOW_ASSETS, MAIN_MENU)

    if category_left.isclicked(event):
        if config['category'] > 9:
            update_config({'category': config['category'] - 1}) 
            log.info('TButton LEFT: -1')
        else:
            config['category'] = 32
        return

    if category_right.isclicked(event):
        if config['category'] < 32:
            update_config({'category': config['category'] + 1})#config['category'] + 1
            log.info('TButton RIGHT: +1')        
        else:
            update_config({'category': 9})#config['category'] = 9
        return
    
    if difficulty_left.isclicked(event):
        if config['difficulty'] > 1:
            update_config({'difficulty': config['difficulty'] - 1})#config['difficulty'] - 1
            log.info('TButton LEFT: -1')
        else:
            update_config({'difficulty': 3})#config['difficulty'] = 3
        return

    if difficulty_right.isclicked(event):
        if config['difficulty'] < 3:
            update_config({'difficulty': config['difficulty'] + 1})#config['difficulty'] += 1
            log.info('TButton RIGHT: +1')
        else:
            update_config({'difficulty': 1})#config['difficulty'] = 1

    if type_left.isclicked(event):
        if config['type'] > 1:
            update_config({'type': config['type'] - 1})#config['type'] -= 1
            log.info('TButton LEFT: -1')        
        else:
            update_config({'type': 3})#config['type'] = 3
        return

    if type_right.isclicked(event):
        if config['type'] < 3:
            update_config({'type': config['type'] + 1})#config['type'] += 1
            log.info('TButton RIGHT: +1')        
        else:
            update_config({'type': 1})#config['type'] = 1
        return        

    if number_left.isclicked(event):
        if config['amount'] > 5:
            update_config({'amount': config['amount'] - 5})#config['amount'] - 5
            log.info('TButton LEFT: -5')        
        else:
            update_config({'amount': 50})#config['amount'] = 50
        return

    if number_right.isclicked(event):
        if config['amount'] < 50:
            update_config({'amount': config['amount'] + 5})#config['amount'] + 5
            log.info('TButton RIGHT: +5')        
        else:
            update_config({'amount': 5})#config['amount'] = 5
        return

def handle_game_window(event):
    pass

if __name__ == '__main__':
    main()