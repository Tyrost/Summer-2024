import pygame
from assets.components import *
from url_request import get_trivia, CROSS_MARK, CHECK_MARK
import logging as log

current_window = MAIN_MENU
window_assets = []
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
            log.info(master_asset_list)
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
            pass
        elif current_window == GAME_MENU:
            pass
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
        log.info(f'Start Button Clicked {CHECK_MARK}')
        current_window = CONFIG_MENU

        switch_window(window_assets, CONFIG_MENU) ### WORK IN PROGRESS ###
        
    if main_quit_btn.isclicked(event): # Quit Game Event
        log.info(f'Quit Button Clicked {CHECK_MARK}')

        make_invisible([main_start_btn, main_quit_btn])
        make_visible([quit_confirm_yes, quit_confirm_no])

        quit_flag = True
    
    if quit_flag and quit_command_ex(event):
        
        running = False

def hadle_config_window(event):
    pass

def handle_game_window(event):
    pass

if __name__ == '__main__':
    main()