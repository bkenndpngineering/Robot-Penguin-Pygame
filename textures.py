import pygame

background = pygame.image.load("assets/BGnew.jpg")
icon_jewel = pygame.image.load("assets/ICON_Jewel.jpg")
icon_seal =  pygame.image.load("assets/ICON_Bear.jpg")
icon_seal_blue = pygame.image.load("assets/ICON_Bear_Flash.jpg")
icon_obstacle = pygame.image.load("assets/ICON_Igloo.jpg")
icon_goal = pygame.image.load("assets/ICON_Goal.jpg")

icon_player_front = pygame.image.load("assets/ICON_Player.jpg")
icon_player_left = pygame.image.load("assets/ICON_Player_270.jpg")
icon_player_right = pygame.image.load("assets/ICON_Player_90.jpg")
icon_player_down = pygame.image.load("assets/ICON_Player_180.jpg")
icon_player_up = pygame.image.load("assets/ICON_Player_Up.jpg")

win_screen = pygame.image.load("assets/winner.jpg")
loose_screen = pygame.image.load("assets/loser.jpg")

left_card = pygame.image.load("assets/CARD_Left.jpg")
right_card = pygame.image.load("assets/CARD_Right.jpg")
down_card = pygame.image.load("assets/CARD_Down.jpg")
up_card = pygame.image.load("assets/CARD_Up.jpg")

pygame.font.init()
font_bold = pygame.font.Font("assets/Manjari-Bold.otf", 20)
font_regular = pygame.font.Font("assets/Manjari-Regular.otf", 20)
font_thin = pygame.font.Font("assets/Manjari-Thin.otf", 20)