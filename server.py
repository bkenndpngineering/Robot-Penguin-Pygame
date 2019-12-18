import pygame
from textures import *
from button import Button

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PENGUIN GAME SERVER')
clock = pygame.time.Clock()


def main():
    #b1 = Button("hello", (0, 0, 100, 50))
    card_resize_rect = (200, 300)
    left_card_resized = pygame.transform.scale(left_card, card_resize_rect)
    right_card_resized = pygame.transform.scale(right_card, card_resize_rect)
    down_card_resized = pygame.transform.scale(down_card, card_resize_rect)
    up_card_resized = pygame.transform.scale(up_card, card_resize_rect)

    offset_x = SCREEN_WIDTH / 8
    offset_y = SCREEN_HEIGHT / 8
    button_left_card = Button("", (SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_down_card = Button("", (2*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_up_card = Button("", (3*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_right_card = Button("", (4*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))

    prog_terminate = False
    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = True

        # background
        display.fill((0, 0, 0))

        # render buttons
        button_left_card.render(display)
        button_down_card.render(display)
        button_up_card.render(display)
        button_right_card.render(display)

        # render icons over the buttons
        display.blit(left_card_resized, (SCREEN_WIDTH/8+offset_x, offset_y))
        display.blit(down_card_resized, (2*SCREEN_WIDTH/8+offset_x, offset_y))
        display.blit(up_card_resized, (3*SCREEN_WIDTH/8+offset_x, offset_y))
        display.blit(right_card_resized, (4*SCREEN_WIDTH/8+offset_x, offset_y))

        # need send button
        # select button under images
        # undo button

        #

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

pygame.quit()
quit()