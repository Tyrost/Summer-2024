import pygame
from assets.components import *
from url_request import get_trivia, CROSS_MARK, CHECK_MARK
import logging as log

# def quit_command_ex(event):
    
#     if quit_confirm_yes.isclicked(event):
#         log.info('Ending game...')

#         return True

#     if quit_confirm_no.isclicked(event):
#         log.info('Action retracted, canceling...')
#         quit_confirm_yes.visible = False
#         quit_confirm_no.visible = False
#         main_start_btn.visible = True
#         main_quit_btn.visible = True

#         return False

current_window = MAIN_MENU



def main():
    global current_window
    global master_asset_list
    start_time = time.time()

    pygame.display.set_caption('Trivia Game')
    
    try:
        log.info(f'Main background image; Path: {main_img_path} loaded... OK {CHECK_MARK}')
    except FileNotFoundError:
        log.error(f'Main background image; Path: {main_img_path} failed to load... {CROSS_MARK}')

    quit_flag = False

    running = True
    while running:

        # TIME TRACKER
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= 1.0:
            log.info(master_asset_list)
            start_time = current_time

    ### Terminate Game Event ###

        for event in pygame.event.get(): # Event Manager (ESSENTIAL)
            if event.type == pygame.QUIT:
                running = False

    ### Main Image Filling ###

        screen_fill(main_img)

    ### Main Button Events ###

        if current_window == MAIN_MENU:
            

            # Draw any possible usable buttons within the **main menu** window. Not all will be visible as some Button's
            # visibility attributes are False
            draw_many([main_start_btn, main_quit_btn, quit_confirm_yes, quit_confirm_no], screen)
            # Start with visibility to quit confirmation buttons = False
            # rest of buttons are visible by default.
            make_invisible([quit_confirm_yes, quit_confirm_no])


            
            if main_start_btn.isclicked(event): # Start Game Button ### CONTINUE HERE
                log.info(f'Start Button Clicked {CHECK_MARK}')
                current_window = CONFIG_MENU

                switch_window(1, master_asset_list) ### NOT IMPLEMENTED ###
                

            if main_quit_btn.isclicked(event): # Quit Game Event
                log.info(f'Quit Button Clicked {CHECK_MARK}')

                make_invisible([main_start_btn, main_quit_btn])
                make_visible([quit_confirm_yes, quit_confirm_no])

                quit_flag = True
            
            # Draw buttons if attribute, visible = True, else return None and cotinue

            # append_asset([quit_confirm_yes, quit_confirm_no])
            
            if quit_flag:
                if quit_command_ex(event):
                    running = False

        elif current_window == CONFIG_MENU:
            pass
        elif current_window == GAME_MENU:
            pass
        pygame.display.update() # Update Changes

    pygame.quit()
    log.info('Game terminated.')

main()