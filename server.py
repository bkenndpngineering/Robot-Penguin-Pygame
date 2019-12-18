import pygame
from textures import *
from button import Button
from clientPoll import gameServer

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PENGUIN GAME SERVER')
clock = pygame.time.Clock()

server = gameServer().run()

def main():
    # resize images
    card_resize_rect = (200, 300)
    left_card_resized = pygame.transform.scale(left_card, card_resize_rect)
    right_card_resized = pygame.transform.scale(right_card, card_resize_rect)
    down_card_resized = pygame.transform.scale(down_card, card_resize_rect)
    up_card_resized = pygame.transform.scale(up_card, card_resize_rect)
    # create buttons
    offset_x = SCREEN_WIDTH / 8
    offset_y = SCREEN_HEIGHT / 8
    button_left_card = Button("", (SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_down_card = Button("", (2*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_up_card = Button("", (3*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))
    button_right_card = Button("", (4*SCREEN_WIDTH/8+offset_x, offset_y, card_resize_rect[0], card_resize_rect[1]))

    button_width = 150
    button_height = 75
    button_reset = Button("RESET IT!", (0 * SCREEN_WIDTH/8+offset_x - button_width, offset_y * 2 + card_resize_rect[1], button_width, button_height))
    button_send = Button("SEND IT!", (5 * SCREEN_WIDTH/8+offset_x + card_resize_rect[0], offset_y * 2 + card_resize_rect[1], button_width, button_height))

    # create grid
    instruction_list = []

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

        # render grid, 6x1
        pygame.draw.rect(display, (255, 0, 0), (0 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)
        pygame.draw.rect(display, (255, 0, 0), (1 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)
        pygame.draw.rect(display, (255, 0, 0), (2 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)
        pygame.draw.rect(display, (255, 0, 0), (3 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)
        pygame.draw.rect(display, (255, 255, 255), (4 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)
        pygame.draw.rect(display, (255, 255, 255), (5 * SCREEN_WIDTH / 8 + offset_x, offset_y * 2 + card_resize_rect[1], card_resize_rect[0], card_resize_rect[1]), 3)

        # render utility buttons
        button_send.render(display)
        button_reset.render(display)

        # check button status
        if button_left_card.isPressed():
            print("left")
            if len(instruction_list) < 6:
                instruction_list.append("left")
            pygame.time.delay(250) # simple debouncing
            button_left_card.reset()

        if button_right_card.isPressed():
            print("right")
            if len(instruction_list) < 6:
                instruction_list.append("right")
            pygame.time.delay(250)  # simple debouncing
            button_right_card.reset()

        if button_down_card.isPressed():
            print("down")
            if len(instruction_list) < 6:
                instruction_list.append("down")
            pygame.time.delay(250)  # simple debouncing
            button_down_card.reset()

        if button_up_card.isPressed():
            print("up")
            if len(instruction_list) < 6:
                instruction_list.append("up")
            pygame.time.delay(250)  # simple debouncing
            button_up_card.reset()

        if button_reset.isPressed():
            instruction_list = []
            print("reset")
            pygame.time.delay(250)  # simple debouncing
            button_reset.reset()

        if button_send.isPressed():
            print("send")
            print(instruction_list)
            # need at least four moves to send, make things interesting
            if not len(instruction_list) >= 4:
                print("need at least four!")
            else:
                if server.client_ready:
                    print("sending...")
                    # send the instructions list then clear it
                    server.send(instruction_list)
                    instruction_list = []
                else:
                    print("client not ready")
            pygame.time.delay(250)  # simple debouncing
            button_send.reset()

        # render grid icons
        x = 0
        coordinate_x = x * SCREEN_WIDTH / 8 + offset_x
        coordinate_y = offset_y * 2 + card_resize_rect[1]
        for instruction in instruction_list:
            if instruction == "left":
                display.blit(left_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "right":
                display.blit(right_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "up":
                display.blit(up_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "down":
                display.blit(down_card_resized, (coordinate_x, coordinate_y))

            x += 1
            coordinate_x = x * SCREEN_WIDTH / 8 + offset_x

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()

pygame.quit()
server.stop()