import pygame
from textures import *

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PENGUIN GAME SERVER')
clock = pygame.time.Clock()

def text_objects(text, font, color=(0, 0, 0)):
    # pythonprogramming.net/displaying-text-pygame-screen/
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,font,rect,ic,ac):
    # pythonprogramming.net/pygame-button-function/
    mouse = pygame.mouse.get_pos()
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, ac, rect)
    else:
        pygame.draw.rect(display, ic, rect)

    textSurf, textRect = text_objects(msg, font)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    display.blit(textSurf, textRect)

def main():
    prog_terminate = False
    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = True

        display.fill((0, 0, 0))
        display.blit(down_card, (0,0))
        button("start",font_bold,(0,0,100,50), (255,255,0), (100,100,100))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()

pygame.quit()
quit()