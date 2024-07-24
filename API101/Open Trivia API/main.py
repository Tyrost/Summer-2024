import pygame
from url_request import get_trivia, CROSS_MARK, CHECK_MARK
import logging as log

if __name__ == '__main__':
    
    WWIDTH = 900
    WHEIGHT = 600
    
    pygame.init()
    screen = pygame.display.set_mode((WWIDTH, WHEIGHT))
    pygame.display.set_caption('Trivia Game')

    #url = get_trivia(amount=10, category=9, diff='easy', type='multiple')

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
                running = False

        if not main_img:
            screen.fill((25, 80, 62))
        else:
            screen.blit(main_img, (0, 0)) 

        pygame.display.update()

    pygame.quit()
