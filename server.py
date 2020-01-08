import pygame
from textures import *
from button import Button
from clientPoll import gameServer

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('PENGUIN GAME SERVER')
clock = pygame.time.Clock()

server = gameServer().run()

def start_screen():
    button_width = 100
    button_height = 50

    #bottom right, hidden exit button
    button_hidden = Button("", (SCREEN_WIDTH - button_width, SCREEN_HEIGHT - button_height, button_width, button_height), inact_color=(0,0,0), act_color=(0,0,0))   # background color must be same as button color

    button_diff_easy = Button("Easy", (0, 0 * button_height, button_width, button_height))
    button_diff_med = Button("Medium", (0, 1 * button_height, button_width, button_height))
    button_diff_hard = Button("Hard", (0, 2 * button_height, button_width, button_height))

    difficulty = None

    prog_terminate = False
    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = True

        button_diff_easy.render(display)
        button_diff_med.render(display)
        button_diff_hard.render(display)
        button_hidden.render(display)
        instruction_list = []

        if button_diff_easy.isPressed():
            print("difficulty 1")
            difficulty = 1
            instruction_list.append("1")
            prog_terminate = True

        elif button_diff_med.isPressed():
            print("difficulty 2")
            difficulty = 2
            instruction_list.append("2")
            prog_terminate = True

        elif button_diff_hard.isPressed():
            print("difficulty 3")
            difficulty = 3
            instruction_list.append("3")
            prog_terminate = True

        elif button_hidden.isPressed():
            print("hidden button. exit")
            difficulty = None
            prog_terminate = True

        pygame.display.update()
        clock.tick(60)

    #return difficulty # do something with client
    if difficulty:
        if server.client_ready:
            print("sending...")
            # send the instructions list then clear it
            server.send(instruction_list)
            instruction_list = []
        else:
            print("client not ready")
        return True
    else:
        return False

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

    # bottom right, hidden exit button
    button_hidden = Button("",
                           (SCREEN_WIDTH - button_width, SCREEN_HEIGHT - button_height, button_width, button_height),
                           inact_color=(0, 0, 0), act_color=(0, 0, 0))  # background color must be same as button color

    # create grid
    instruction_list = []

    prog_terminate = 0
    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = 2

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
        button_hidden.render(display)

        if button_hidden.isPressed():
            print("hidden button. exit")
            prog_terminate = 2

        # check button status
        elif button_left_card.isPressed():
            print("rotateLeft")
            if len(instruction_list) < 6:
                instruction_list.append("rotateLeft")
            pygame.time.delay(250) # simple debouncing
            button_left_card.reset()

        elif button_right_card.isPressed():
            print("rotateRight")
            if len(instruction_list) < 6:
                instruction_list.append("rotateRight")
            pygame.time.delay(250)  # simple debouncing
            button_right_card.reset()

        elif button_down_card.isPressed():
            print("backwards")
            if len(instruction_list) < 6:
                instruction_list.append("backwards")
            pygame.time.delay(250)  # simple debouncing
            button_down_card.reset()

        elif button_up_card.isPressed():
            print("forwards")
            if len(instruction_list) < 6:
                instruction_list.append("forwards")
            pygame.time.delay(250)  # simple debouncing
            button_up_card.reset()

        elif button_reset.isPressed():
            instruction_list = []
            print("reset")
            pygame.time.delay(250)  # simple debouncing
            button_reset.reset()

        elif button_send.isPressed():
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
            if instruction == "rotateLeft":
                display.blit(left_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "rotateRight":
                display.blit(right_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "forwards":
                display.blit(up_card_resized, (coordinate_x, coordinate_y))

            elif instruction == "backwards":
                display.blit(down_card_resized, (coordinate_x, coordinate_y))

            x += 1
            coordinate_x = x * SCREEN_WIDTH / 8 + offset_x

        if server.restart:
            prog_terminate = 1
            server.restart = False

        pygame.display.update()
        clock.tick(60)

    return prog_terminate

if __name__ == "__main__":
    while 1:
        state = start_screen()
        if state == False:
            break
        state = main()
        if state == 2:
            break

pygame.quit()
server.stop()