import pygame
from textures import font_bold, font_regular, font_thin

class Button():
    def __init__(self, text, rect, inact_color=(255,0,0), act_color=(0,255,0), font=font_regular, text_color=(0, 0, 0)):
        self.text = text
        self.rect = rect
        self.inactive_color = inact_color
        self.active_color = act_color
        self.font = font
        self.text_color = text_color

        self.pressed = False

    def reset(self):
        self.pressed = False

    def isPressed(self):
        return self.pressed

    def render(self, display):
        # doubles as an update function
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = ((self.rect[0]+(self.rect[2]/2)), (self.rect[1]+(self.rect[3]/2)))

        if self.rect[0]+self.rect[2] > mouse[0] > self.rect[0] and self.rect[1]+self.rect[3] > mouse[1] > self.rect[1] and click[0] == 1:
            self.pressed = True

        if self.pressed:
            pygame.draw.rect(display, self.inactive_color, self.rect)
        else:
            pygame.draw.rect(display, self.active_color, self.rect)

        display.blit(text_surface, text_rect)