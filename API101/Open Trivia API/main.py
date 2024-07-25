import pygame
from assets.button import Button
from url_request import get_trivia, CROSS_MARK, CHECK_MARK
import logging as log

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    WWIDTH = 900
    WHEIGHT = 600
    FONT = pygame.font.Font('API101/Open Trivia API/assets/Lexend-Regular.ttf', 32)

    screen = pygame.display.set_mode((WWIDTH, WHEIGHT))
    pygame.display.set_caption('Trivia Game')

    button = Button(WWIDTH/2 - 50, WHEIGHT/2 - 50, 150, 70, 'Hello World!', FONT, (0,0,0), (250, 250, 250), (100,100,100))

    main_img_path = 'API101/Open Trivia API/assets/main_background.jpg'
    
    try:
        main_img = pygame.image.load(main_img_path)
        main_img = pygame.transform.scale(main_img, (WWIDTH, WHEIGHT))
        log.info(f'Main background image; Path: {main_img_path} loaded... OK {CHECK_MARK}')
        
    except FileNotFoundError:
        log.error(f'Main background image; Path: {main_img_path} failed to load... {CROSS_MARK}')
        main_img = None
    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                log.info('Game terminated.')
                running = False

###################################################
        try:
            if not main_img:
                screen.fill((25, 80, 62))
            else:
                screen.blit(main_img, (0, 0))
        except pygame.error:
            log.warning('display Surface quit')

###################################################

        button.draw(screen)

        if button.is_clicked(event):
            log.info(f'BUTTON CLICKED! {CHECK_MARK}')

####################################################
        pygame.display.update()

    pygame.quit()
