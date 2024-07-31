import pygame
from assets.components import *
from url_request import get_trivia, CHECK_MARK
import logging as log

current_window = MAIN_MENU
quit_flag = False
running = True

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
            
            hadle_config_window(event)

        elif current_window == GAME_MENU:
            
            handle_game_window(event)

        pygame.display.update() # Update Changes

    pygame.quit()
    log.info('Game terminated.')

def handle_main_menu(event):
    global running
    global current_window
    global quit_flag

    window_assets = [main_start_btn, main_quit_btn, quit_confirm_yes, quit_confirm_no]
    # Draw any possible usable buttons within the main menu window
    draw_many(window_assets, screen)

    # Start with visibility to quit confirmation buttons = False
    if not quit_flag:
        make_invisible([quit_confirm_yes, quit_confirm_no])

    if main_start_btn.isclicked(event): # Start Game Button
        log.info(f'Start Button Clicked.')
        current_window = CONFIG_MENU

        switch_window(window_assets, CONFIG_MENU)
        make_visible(window_assets)
        quit_flag = False
        
    if main_quit_btn.isclicked(event): # Quit Game Event
        log.info(f'Quit Button Clicked.')

        make_invisible([main_start_btn, main_quit_btn])
        make_visible([quit_confirm_yes, quit_confirm_no])

        quit_flag = True
    
    if quit_flag and quit_command_ex(event): 
        running = False    

def hadle_config_window(event):
    global current_window

    window_asset = [back_main_btn]
    draw_many([back_main_btn], screen)

    if back_main_btn.isclicked(event):
        log.info('Back to main menu...')
        current_window = MAIN_MENU

        switch_window(window_asset, MAIN_MENU)
        make_visible(window_asset)

def handle_game_window(event):
    pass

if __name__ == '__main__':
    main()