import pygame

class Button:

    def __init__(self, x:int, y:int, width:int, height:int, text:str, font:pygame.font.Font, fontColor:tuple, color:tuple, hover:tuple) -> None:
        self.x = x
        self.y = y

        self.box = pygame.Rect(x,y,width,height)
        self.text = text
        self.color = color
        self.hover = hover
        self.font = font
        self.fontColor = fontColor

        self.clicked = False
        self.visible = True
    
    def __repr__(self) -> str:
        return f'<{self.text}>'

    def undraw(self)->None:
        self.visible = False

    def draw(self, screen:pygame.Surface) -> None:
        '''
        Draws the button box and checks for cursor events:
        If cursor hover over the button box, it will change color from its default color.
        '''
        if not self.visible:
            return
        
        cursor_position = pygame.mouse.get_pos()
        if self.box.collidepoint(cursor_position):
            pygame.draw.rect(surface=screen, color=self.hover, rect=self.box)
        else:
            pygame.draw.rect(surface=screen, color=self.color, rect=self.box)

        text_surface = self.font.render(self.text, True, self.fontColor)
        text_rect = text_surface.get_rect(center=self.box.center)
        screen.blit(text_surface, text_rect)

    def isclicked(self, event: pygame.event.Event) -> bool:
        '''
        Checks the event in which the mouse's button is down within the box's boundry.
        '''
        if not self.visible:
            return False

        try:
            if event.type == pygame.MOUSEBUTTONDOWN and self.box.collidepoint(event.pos) and not self.clicked:
                self.clicked = True
                return True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
            return False

        except pygame.error as e:
            print(f'Error in button click handling: {e}')
        return False