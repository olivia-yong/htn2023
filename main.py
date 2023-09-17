import pygame
import random
from threading import Thread

from hand_landmarker import run, HAND_EVENT

pygame.init()
pygame.font.init()

#########################################################
# VARIABLES

# colors
orange = (227, 174, 59)
black = (0, 0, 0)
white = (255, 255, 255)
pink = (255, 184, 230)

# game screen
gamedis_width = 600
gamedis_height = 600
size = [gamedis_width, gamedis_height]

# scoreboard
scoreboard_width = 200
scoreboard_height = 600

score_font_type = pygame.font.SysFont(None, 36)

#snake
pos_x = gamedis_width / 2 + scoreboard_width
pos_y = gamedis_height / 2
pos_x_change = 0
pos_y_change = 0
snake_icon_size = 10 #hey i need to edit this later but game breaks if u change it so don't change this
snake_List = []
snake_body_img = "./ASSETS/skin1_body.png"
snake_tail_img = "./ASSETS/skin1_tail.png"

# apples
game_score = 0
foodx = (
    round(random.randrange(0, gamedis_width - 200 - snake_icon_size) / 10.0) * 10.0
    + scoreboard_width + 100
)
foody = round(random.randrange(0, gamedis_height - 200 - snake_icon_size) / 10.0) * 10.0 + 100
food_img = "./ASSETS/rock1.png"

# speed
clock = pygame.time.Clock()
snake_speed = 10

game_over = False
window_over = False
game_on = True

######################################################
# MAKE GAME SCREEN
gamedis = pygame.display.set_mode((800, 600))

# make main playing area
game_area = pygame.Rect(200, 0, gamedis_width, gamedis_height)
pygame.draw.rect(gamedis, black, game_area)

# make scoreboard
scoreboard = pygame.Rect(0, 0, scoreboard_width, scoreboard_height)
pygame.draw.rect(gamedis, pink, scoreboard)
score_display = score_font_type.render(f"Score: {game_score}", True, black)
gamedis.blit(score_display, (30, 100))

#make initial snake
snake_head = pygame.image.load(snake_body_img).convert()
snake_head = pygame.transform.scale(snake_head, (snake_icon_size, snake_icon_size))
gamedis.blit(snake_head, (pos_x, pos_y))

pygame.display.flip()
pygame.display.set_caption("Snake wave")

background_process = Thread(target=run)
background_process.start()

##############################################################################################
# FUNCTIONS


# update score
def update_score(game_score):
    pygame.draw.rect(gamedis, pink, scoreboard)
    score_display = score_font_type.render(f"Score: {game_score}", True, black)
    gamedis.blit(score_display, (30, 100))
    pygame.display.update()


def update_snake(snake_List, pos_x, pos_y):
    #Draw Snake
    cnt = 0
    for x in snake_List:
        if(cnt % 2 == 0):    
            snake_body = pygame.image.load(snake_body_img).convert()    
        else :
            snake_body = pygame.image.load(snake_tail_img).convert()
        cnt += 1
        snake_body = pygame.transform.scale(snake_body, (snake_icon_size, snake_icon_size))
        gamedis.blit(snake_body, (x[0], x[1]))

    pygame.display.update()

def make_food(foodx, foody):
    food = pygame.image.load(food_img).convert()
    food = pygame.transform.scale(food, (snake_icon_size, snake_icon_size))
    gamedis.blit(food, (foodx, foody))
    pygame.display.update()


# continuously run game until game_over = true (when game ends)
while not window_over:
    # Get all event
    score_change = False
    for event in pygame.event.get():
        """
        #RESIZE WINDOW BUTTONs
        if event.type == pygame.VIDEORESIZE:
            gamedis_height = event.h
            gamedis_width = event.w
            size = [gamedis_width, gamedis_height]
            gamedis = pygame.display.set_mode(size, pygame.RESIZABLE)
        """
        # X BUTTON
        if event.type == pygame.QUIT:
            window_over = True
            exit

        # Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and pos_x_change == 0:
                pos_x_change = -snake_icon_size
                pos_y_change = 0
            elif event.key == pygame.K_RIGHT and pos_x_change == 0:
                pos_x_change = snake_icon_size
                pos_y_change = 0
            elif event.key == pygame.K_UP and pos_y_change == 0:
                pos_x_change = 0
                pos_y_change = -snake_icon_size
            elif event.key == pygame.K_DOWN and pos_y_change == 0:
                pos_x_change = 0
                pos_y_change = snake_icon_size
            elif event.key == pygame.K_1:
                score_change = True
                game_score += 1
                update_score(game_score)

        '''
        if event.type == HAND_EVENT:
            result = event.dict.get("result")
            if result == "L" and pos_x_change == 0:
                pos_x_change = -snake_icon_size
                pos_y_change = 0
            elif result == "R" and pos_x_change == 0:
                pos_x_change = snake_icon_size
                pos_y_change = 0
            elif result == "U" and pos_y_change == 0:
                pos_x_change = 0
                pos_y_change = -snake_icon_size
            elif result == "D" and pos_y_change == 0:
                pos_x_change = 0
                pos_y_change = snake_icon_size
        '''
    # Did snake hit wall?
    pos_x += pos_x_change
    pos_y += pos_y_change

    if (
        pos_x > (gamedis_width + scoreboard_width)
        or pos_x < scoreboard_width
        or pos_y > gamedis_height
        or pos_y < 0
    ):
        game_over = True
        

    # Updating Snake Head
    pygame.draw.rect(gamedis, black, game_area)
    make_food(foodx, foody)
    snake_Head = []
    snake_Head.append(pos_x)
    snake_Head.append(pos_y)
    snake_List.append(snake_Head)

    if len(snake_List) > game_score + 1:
        del snake_List[0]

    # Check if snake hit itself
    for x in snake_List[:-1]:
        if x == snake_Head:
            game_over = True

    update_snake(snake_List, pos_x, pos_y)

    # Did snake hit food?
    if pos_x == foodx and pos_y == foody:
        foodx = (
            round(random.randrange(0, gamedis_width - 200 - snake_icon_size) / 10.0) * 10.0
            + scoreboard_width + 100
        )
        foody = round(random.randrange(0, gamedis_height - 200 - snake_icon_size) / 10.0) * 10.0 + 100
        game_score += 1
        update_score(game_score)
        print("YEAHHHH FOOOB")

    clock.tick(snake_speed)


# You Lose XD
pygame.draw.rect(gamedis, black, game_area)
lose_text = score_font_type.render("RIP BOZO YOU LOSE", True, white)
gamedis.blit(lose_text, (gamedis_width / 2, gamedis_height / 2))
pygame.display.update()
pygame.time.wait(2000)

# Exiting the Game
pygame.quit()
pygame.font.quit()
quit()
