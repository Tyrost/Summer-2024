import pygame

class Button:

    def __init__(self, x, y, width, height, text, font, fontColor, color, hover) -> None:
        self.x = x
        self.y = y

        self.box = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = color
        self.hover = hover
        self.font = font
        self.fontColor = fontColor

        self.clicked = False

    def draw(self, screen:pygame.Surface):
        cursor_position = pygame.mouse.get_pos()
        if self.box.collidepoint(cursor_position):
            pygame.draw.rect(surface=screen, color=self.hover, rect=self.box)#self.box)
        else:
            pygame.draw.rect(surface=screen, color=self.color, rect=self.box)

        text_surface = self.font.render(self.text, True, self.fontColor)
        text_rect = text_surface.get_rect(center=self.box.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event: pygame.event.Event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                if not self.clicked:
                    self.clicked = True
                    return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.box.collidepoint(pygame.mouse.get_pos()):
                self.clicked = False
        return False
        
       