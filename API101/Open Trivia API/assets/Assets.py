import pygame
from typing import List, Tuple, Union

class Button:

    def __init__(self, x:int, y:int, width:int, height:int, text:str, font:pygame.font.Font, fontColor:tuple, color:tuple, hover:tuple, c_hover=True) -> None:
        self.x = x
        self.y = y

        self.box = pygame.Rect(x,y,width,height)
        self.text = text
        self.hover = hover
        self.color = color
        self.font = font
        self.fontColor = fontColor

        self.clicked = False
        self.visible = True

        self.c_hover = c_hover
    
    def __repr__(self) -> str:
        return f'<R{self.text}>'

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
        if self.box.collidepoint(cursor_position) and self.c_hover:
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

# Courtesy of ChatGPT :)
class TriangleButton:

    def __init__(self, vertices:List[Tuple[float]], label:str, color:tuple, hover:tuple) -> None:

        self.vertices = vertices

        self.label = label
        self.color = color
        self.current_color = color
        self.hover = hover

        self.clicked = False
        self.visible = True

    def __repr__(self) -> str:
        return f'<T{self.label}>'
    
    def get_center(self) -> Tuple[int, int]:
        x = (self.vertices[0][0] + self.vertices[1][0] + self.vertices[2][0]) // 3
        y = (self.vertices[0][1] + self.vertices[1][1] + self.vertices[2][1]) // 3
        return (x, y)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            if self.is_hovered(event.pos):
                self.current_color = self.hover
            else:
                self.current_color = self.color

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos):
                return True
        return False

    def is_hovered(self, mouse_pos: Tuple[int, int]) -> bool:
        return self.is_point_in_triangle(mouse_pos, self.vertices[0], self.vertices[1], self.vertices[2])

    def is_point_in_triangle(self, pt: Tuple[int, int], v1: Tuple[int, int], v2: Tuple[int, int], v3: Tuple[int, int]) -> bool:
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign(pt, v1, v2) < 0.0
        b2 = sign(pt, v2, v3) < 0.0
        b3 = sign(pt, v3, v1) < 0.0

        return ((b1 == b2) and (b2 == b3))
    
    def draw(self, screen: pygame.Surface) -> None:
        if not self.visible:
            return
        
        pygame.draw.polygon(screen, self.current_color, self.vertices)
    
    def undraw(self) -> None:
        self.visible = False

    def isclicked(self, event):
        if not self.visible:
            return
        try:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.clicked:
                self.clicked = True
                mouse_pos = pygame.mouse.get_pos()
                return self.is_point_in_triangle(mouse_pos, self.vertices[0], self.vertices[1], self.vertices[2])
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
            else:
                return False
        except Exception as e:
            print(f'Error in button click handling: {e}')
        return False
    
# Courtesy of ChatGPT :)
class Table:
    def __init__(self, surface: pygame.Surface, position: Tuple[int, int], font: pygame.font.Font, fontColor: Tuple[int, int, int], text:List[List[str]], cell_padding: int = 5):
        # """
        # Initializes the TextTable with a surface, position, font, color, and cell padding.

        # Parameters:
        #     surface (pygame.Surface): The surface to draw the table on.
        #     position (Tuple[int, int]): The top-left position where the table starts.
        #     font (pygame.font.Font): The font used to render the text.
        #     color (Tuple[int, int, int]): The color of the text.
        #     cell_padding (int): The padding around the text in each cell.
        # """
        self.surface = surface
        self.position = position
        self.font = font
        self.fontColor = fontColor
        self.cell_padding = cell_padding
        self.text = text

        self.visible = True

    def draw(self, screen = None) -> None:
        """
        Draws a table of text on the Pygame surface.

        Parameters:
            data (List[List[str]]): The data to be displayed in the table. Each sublist represents a row.
        """
        if not self.visible:
            return 
        
        x, y = self.position
        for row in self.text:
            max_height = 0
            row_surfaces = []
            for cell in row:
                text_surface = self.font.render(cell, True, self.fontColor)
                row_surfaces.append(text_surface)
                max_height = max(max_height, text_surface.get_height())
            for i, cell_surface in enumerate(row_surfaces):
                self.surface.blit(cell_surface, (x + i * (cell_surface.get_width() + self.cell_padding), y))
            y += max_height + self.cell_padding

    def undraw(self):
        self.visible = False