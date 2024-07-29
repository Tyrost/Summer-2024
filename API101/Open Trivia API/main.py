import pygame
from assets.components import *
from url_request import get_trivia, CROSS_MARK, CHECK_MARK
import logging as log

def quit_command_ex(event):
    
    if quit_confirm_yes.isclicked(event):
        log.info('Ending game...')

        return True

    if quit_confirm_no.isclicked(event):
        log.info('Action retracted, canceling quit...')
        quit_confirm_yes.visible = False
        quit_confirm_no.visible = False
        main_start_btn.visible = True
        main_quit_btn.visible = True

        return False

current_window = MAIN_MENU

def main():

    pygame.display.set_caption('Trivia Game')
    
    try:
        log.info(f'Main background image; Path: {main_img_path} loaded... OK {CHECK_MARK}')
    except FileNotFoundError:
        log.error(f'Main background image; Path: {main_img_path} failed to load... {CROSS_MARK}')
    
    quit_confirm_yes.visible = False
    quit_confirm_no.visible = False

    quit_flag = False

    running = True
    while running:

    ### Terminate Game Event ###

        for event in pygame.event.get(): # Event Manager (ESSENTIAL)
            if event.type == pygame.QUIT:
                running = False

    ### Main Image Filling ###

        screen_fill(main_img)

    ### Main Button Events ###

        if current_window == MAIN_MENU:

            main_start_btn.draw(screen)
            main_quit_btn.draw(screen)
            
            append_asset(main_start_btn, main_quit_btn)

            if main_start_btn.isclicked(event): # Start Game Button
                log.info(f'Start Button Clicked {CHECK_MARK}')
                current_window = CONFIG_MENU

                switch_window(1, master_asset_list)
                

            if main_quit_btn.isclicked(event): # Quit Game Event
                log.info(f'Quit Button Clicked {CHECK_MARK}')

                main_start_btn.undraw()
                main_quit_btn.undraw()
                del_asset([main_start_btn, main_quit_btn])

                quit_confirm_yes.visible = True
                quit_confirm_no.visible = True
                append_asset([quit_confirm_yes, quit_confirm_no])

                quit_flag = True
            
            # Draw buttons if attribute, visible = True, else return None and cotinue
            quit_confirm_yes.draw(screen)
            quit_confirm_no.draw(screen)
            append_asset([quit_confirm_yes, quit_confirm_no])
            
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
