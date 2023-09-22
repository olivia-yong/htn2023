import pygame
import random
import requests as req
from threading import Thread


from hand_landmarker import run, HAND_EVENT
from pyfont.font import Font

pygame.init()
pygame.font.init()

#########################################################
# CONSTANTS
BASE_URL = "https://htn-2023-backend.vercel.app"

# VARIABLES

# Colors
ORANGE = (227, 174, 59)
BLACK = (1, 1, 1)
WHITE = (255, 255, 255)
PINK = (255, 184, 230)
GREEN = (0, 164, 0)
PALE_GREEN = (219, 255, 132)
PURPLE = (130, 33, 139)

# Logo
LOGO = pygame.image.load("./ASSETS/logo.png")
pygame.display.set_icon(LOGO)

# Game screen
screen_width = 800
screen_height = 600
gamedis_width = 600
gamedis_height = 600
size = [gamedis_width, gamedis_height]

# Scoreboard
scoreboard_width = 200
scoreboard_height = 200

# Shop
shop_width = 200
shop_height = 600

score_font_type = pygame.font.SysFont(None, 36)

# Snake
pos_x = gamedis_width / 2 + scoreboard_width
pos_y = gamedis_height / 2
pos_x_change = 0
pos_y_change = 0
snake_icon_size = 10  # hey i need to edit this later but game breaks if u change it so don't change this
snake_List = []
snake_body_img = "./ASSETS/skin1_body.png"
snake_tail_img = "./ASSETS/skin1_tail.png"

# Apples
game_score = 0
foodx = (
    round(random.randrange(0, gamedis_width - 200 - snake_icon_size) / 10.0) * 10.0
    + scoreboard_width
    + 100
)
foody = (
    round(random.randrange(0, gamedis_height - 200 - snake_icon_size) / 10.0) * 10.0
    + 100
)
food_img = "./ASSETS/rock1.png"

# Speed
clock = pygame.time.Clock()
snake_speed = 10

game_over = False
window_over = False
game_on = False
camera_on = False

######################################################
# MAKE GAME SCREEN
gamedis = pygame.display.set_mode((800, 600))

game_area = pygame.Rect(200, 0, gamedis_width, gamedis_height)
scoreboard = pygame.Rect(0, 0, scoreboard_width, scoreboard_height)
shop = pygame.Rect(0, scoreboard_height, shop_width, shop_height)

pygame.display.set_caption("Snake Wave")

mike_font = Font(pygame.image.load("pyfont/font.png").convert())

##############################################################################################
# FUNCTIONS


# Increment score
def update_score(game_score):
    pygame.draw.rect(gamedis, PINK, scoreboard)
    score_text = f"Score - {game_score}"
    mike_font.render(
        gamedis,
        score_text,
        scoreboard_width / 2,
        scoreboard_height / 2,
        BLACK,
        12,
        style="center",
    )
    pygame.display.update()


# Grow snake
def update_snake(snake_List, pos_x, pos_y):
    # Draw snake
    cnt = 0
    for x in snake_List:
        if cnt % 2 == 0:
            snake_body = pygame.image.load(snake_body_img).convert()
        else:
            snake_body = pygame.image.load(snake_tail_img).convert()
        cnt += 1
        snake_body = pygame.transform.scale(
            snake_body, (snake_icon_size, snake_icon_size)
        )
        gamedis.blit(snake_body, (x[0], x[1]))
    pygame.display.update()


# Show food
def make_food(foodx, foody):
    food = pygame.image.load(food_img).convert()
    food = pygame.transform.scale(food, (snake_icon_size, snake_icon_size))
    gamedis.blit(food, (foodx, foody))
    pygame.display.update()


def make_lose_screen():
    global game_over
    global window_over
    pygame.mouse.set_visible(True)
    pygame.draw.rect(gamedis, BLACK, game_area)
    mike_font.render(
        gamedis,
        "YOU LOSE",
        gamedis_width / 2 + scoreboard_width,
        gamedis_height / 8,
        WHITE,
        18,
        style="center",
    )

    # Saving latest score
    res = req.post(
        BASE_URL + "/post_score",
        json={"username": username, "score": game_score},
        headers={"Content-Type": "application/json"},
    ).json()

    # Get personal highscore
    res = req.get(
        BASE_URL + "/personal_highscore",
        json={"username": username},
        headers={"Content-Type": "application/json"},
    ).json()
    highscore = res["data"]
    highscore_text = f"Personal Highscore - {highscore}"
    mike_font.render(
        gamedis,
        highscore_text,
        gamedis_width / 2 + scoreboard_width,
        gamedis_height / 8 + 50,
        WHITE,
        14,
        style="center",
    )

    # Making leaderboard
    res = req.get(BASE_URL + "/leaderboard").json()
    leaderboard = res["data"]
    board_w = 400
    board_h = 500
    board_pos_x = gamedis_width / 2 + scoreboard_width - board_w / 2
    board_pos_y = gamedis_height / 8 + 100
    pygame.draw.rect(gamedis, ORANGE, (board_pos_x, board_pos_y, board_w, board_h))
    text_y = board_pos_y + 30
    mike_font.render(
        gamedis,
        "Leaderboard",
        gamedis_width / 2 + scoreboard_width,
        text_y,
        WHITE,
        16,
        style="center",
    )

    # Extra spacing
    text_y += 10

    for score in leaderboard:
        text_y += 30
        score_text = pygame.font.SysFont(None, 27).render(
            f"{score[0]} - {score[1]}    {score[2][5:16]}", True, WHITE
        )
        text_rect = score_text.get_rect(center=(board_pos_x + board_w / 2, text_y))
        gamedis.blit(score_text, text_rect)

    # Making play again button
    button_w = 200
    button_h = 40
    button_pos_x = gamedis_width / 2 + scoreboard_width - button_w / 2
    button_pos_y = gamedis_height * 9 / 10
    pygame.draw.rect(gamedis, PURPLE, (button_pos_x, button_pos_y, button_w, button_h))
    mike_font.render(
        gamedis,
        "Play Again?",
        button_pos_x + button_w / 2,
        button_pos_y + button_h / 2,
        WHITE,
        12,
        style="center",
    )
    pygame.display.update()

    while window_over == False:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                window_over = True
                game_over = True
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    button_pos_x <= mouse[0] <= button_w + button_pos_x
                    and button_pos_y <= mouse[1] <= button_h + button_pos_y
                ):
                    print("BUTTON PRESSED HOORAY")
                    game_over = False
                    make_game_screen()
                    game_loop(game_over)
                    break


def make_intro_screen():
    global game_on
    gamedis.fill(GREEN)
    mike_font.render(
        gamedis,
        "Welcome to Snake Wave",
        screen_width / 2,
        100,
        WHITE,
        24,
        style="center",
    )

    # username and password input

    mike_font.render(
        gamedis,
        "Username ",
        screen_width / 2 - 150,
        200,
        WHITE,
        14,
        style="center",
    )

    mike_font.render(
        gamedis,
        "Password ",
        screen_width / 2 - 150,
        300,
        WHITE,
        14,
        style="center",
    )

    username_input_x = screen_width / 2 - 75
    username_input_y = 200 - (30 / 2)
    pygame.draw.rect(gamedis, WHITE, (username_input_x, username_input_y, 270, 30))

    password_input_x = username_input_x
    password_input_y = 300 - (30 / 2)
    pygame.draw.rect(gamedis, WHITE, (password_input_x, password_input_y, 270, 30))

    # login button
    login_x = screen_width / 2 - 50
    login_y = screen_height / 2 + 40
    pygame.draw.rect(
        gamedis, PURPLE, (screen_width / 2 - 50, screen_height / 2 + 40, 100, 40)
    )
    mike_font.render(
        gamedis,
        "Login",
        screen_width / 2,
        screen_height / 2 + 60,
        WHITE,
        12,
        style="center",
    )

    # register button
    register_x = screen_width / 2 - 62.5
    register_y = screen_height / 2 + 160
    pygame.draw.rect(
        gamedis, PURPLE, (screen_width / 2 - 62.5, screen_height / 2 + 160, 125, 40)
    )
    mike_font.render(
        gamedis,
        "Register",
        screen_width / 2,
        screen_height / 2 + 180,
        WHITE,
        12,
        style="center",
    )

    pygame.display.update()

    global username
    username = ""
    password = ""
    password_dis = ""
    username_input_active = False
    password_input_active = False
    while game_on == False:
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = True
                window_over = True
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                # Check if mouse is in input boxes
                if (
                    mouse[0] <= username_input_x + 270 and mouse[0] >= username_input_x
                ) and (
                    mouse[1] <= username_input_y + 30 and mouse[1] >= username_input_y
                ):
                    username_input_active = True
                    password_input_active = False
                    print("username input active")
                    continue

                if (
                    mouse[0] <= password_input_x + 270 and mouse[0] >= password_input_x
                ) and (
                    mouse[1] <= password_input_y + 30 and mouse[1] >= password_input_y
                ):
                    password_input_active = True
                    username_input_active = False
                    print("password input active")
                    continue

                if (
                    (login_x <= mouse[0] <= login_x + 100)
                    and (login_y <= mouse[1] <= login_y + 40)
                    and (username_input_active or password_input_active)
                ):
                    print("login button pressed")
                    username_input_active = False
                    password_input_active = False

                    res = req.post(
                        BASE_URL + "/login",
                        json={"username": username, "password": password},
                        headers={"Content-Type": "application/json"},
                    ).json()

                    if res["status"] == 1:
                        if res["message"] == "Incorrect password":
                            wrong_pass = pygame.font.SysFont(None, 25).render(
                                res["message"], True, PURPLE
                            )
                            text_rect = wrong_pass.get_rect(
                                center=(screen_width / 2, password_input_y - 20)
                            )
                            gamedis.blit(wrong_pass, text_rect)

                        elif res["message"] == "User does not exist":
                            no_user = pygame.font.SysFont(None, 25).render(
                                res["message"], True, PURPLE
                            )
                            text_rect = no_user.get_rect(
                                center=(screen_width / 2, username_input_y - 20)
                            )
                            gamedis.blit(no_user, text_rect)

                    if res["status"] == 0:
                        print(res["data"])
                        game_on = True
                        return True

                if (
                    (register_x <= mouse[0] <= register_x + 125)
                    and (register_y <= mouse[1] <= register_y + 40)
                    and (username_input_active or password_input_active)
                ):
                    print("register button pressed")
                    username_input_active = False
                    password_input_active = False

                    res = req.post(
                        BASE_URL + "/register",
                        json={"username": username, "password": password},
                        headers={"Content-Type": "application/json"},
                    ).json()

                    if res["status"] == 1:
                        if res["message"] == "Username already exists":
                            user_exists = pygame.font.SysFont(None, 25).render(
                                res["message"], True, PURPLE
                            )
                            text_rect = user_exists.get_rect(
                                center=(screen_width / 2, username_input_y - 20)
                            )
                            gamedis.blit(user_exists, text_rect)

                    if res["status"] == 0:
                        print(res["data"])
                        game_on = True
                        return True

            if event.type == pygame.KEYDOWN:
                if username_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

                if password_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                        password_dis = password_dis[:-1]
                    else:
                        password += event.unicode
                        if event.unicode:
                            password_dis += "*"

        if username_input_active:
            user_color = PINK
            pass_color = WHITE
        elif password_input_active:
            user_color = WHITE
            pass_color = PINK
        else:
            user_color = WHITE
            pass_color = WHITE

        pygame.draw.rect(
            gamedis, user_color, (username_input_x, username_input_y, 270, 30)
        )
        pygame.draw.rect(
            gamedis, pass_color, (password_input_x, password_input_y, 270, 30)
        )

        # Set username and password length limit
        if len(username) > 26:
            username = username[:26]
        if len(password) > 26:
            password = password[:26]
        if len(password_dis) > 26:
            password_dis = password_dis[:26]

        # Render inputted text
        username_input = pygame.font.SysFont(None, 25).render(username, True, BLACK)
        password_input = pygame.font.SysFont(None, 25).render(password_dis, True, BLACK)
        gamedis.blit(username_input, (username_input_x + 5, username_input_y + 5))
        gamedis.blit(password_input, (password_input_x + 5, password_input_y + 5))
        pygame.display.update()

    # game_on = True
    return False


def make_game_screen():
    global pos_x
    global pos_y
    global pos_x_change
    global pos_y_change
    global game_score
    global camera_on

    # Start hand landmarker background process
    if not camera_on:
        background_process = Thread(target=run)
        background_process.start()
        camera_on = True

    pygame.mouse.set_visible(False)

    # Make main playing area
    pygame.draw.rect(gamedis, BLACK, game_area)

    # Make scoreboard
    game_score = 0
    pygame.draw.rect(gamedis, PINK, scoreboard)
    score_text = f"Score - {game_score}"
    mike_font.render(
        gamedis,
        score_text,
        scoreboard_width / 2,
        scoreboard_height / 2,
        BLACK,
        12,
        style="center",
    )

    # Make shop
    update_shop()

    # Make initial snake
    pos_x = gamedis_width / 2 + scoreboard_width
    pos_y = gamedis_height / 2
    pos_x_change = 0
    pos_y_change = 0
    snake_head = pygame.image.load(snake_body_img).convert()
    snake_head = pygame.transform.scale(snake_head, (snake_icon_size, snake_icon_size))
    gamedis.blit(snake_head, (pos_x, pos_y))
    pygame.display.flip()


def update_shop():
    pygame.draw.rect(gamedis, PALE_GREEN, shop)

    # skin 1
    skin1_icon = pygame.image.load("./ASSETS/skin1_head.png").convert()
    skin1_icon = pygame.transform.scale(skin1_icon, (80, 80))
    gamedis.blit(skin1_icon, (10, scoreboard_height + 50))

    # rock 1
    rock1_icon = pygame.image.load("./ASSETS/rock1.png").convert()
    rock1_icon = pygame.transform.scale(rock1_icon, (80, 80))
    gamedis.blit(rock1_icon, ((10 + 80 + 15), scoreboard_height + 50))

    # skin 2
    skin2_icon_link = "./ASSETS/skin2_head_locked.jpg"
    skin2_icon = pygame.image.load(skin2_icon_link)
    skin2_icon = pygame.transform.scale(skin2_icon, (80, 80))
    gamedis.blit(skin2_icon, (10, scoreboard_height + 50 + 80 + 20))

    # rock 2
    rock2_icon_link = "./ASSETS/rock2_locked.jpg"
    rock2_icon = pygame.image.load(rock2_icon_link)
    rock2_icon = pygame.transform.scale(rock2_icon, (80, 80))
    gamedis.blit(rock2_icon, ((10 + 80 + 15), scoreboard_height + 50 + 80 + 20))

    # Select button
    pygame.draw.rect(
        gamedis, PURPLE, (10 + 20, scoreboard_height + 50 + 160 + 40, 140, 50)
    )
    mike_font.render(
        gamedis,
        "Select",
        10 + 20 + 70,
        scoreboard_height + 50 + 160 + 40 + 25,
        WHITE,
        12,
        style="center",
    )
    pygame.display.update()

    pygame.display.flip()


def game_loop(game_over):
    global pos_x
    global pos_y
    global pos_x_change
    global pos_y_change
    global foodx
    global foody
    global game_score
    while game_over == False:
        for event in pygame.event.get():
            """
            #RESIZE WINDOW BUTTONs
            if event.type == pysgame.VIDEORESIZE:
                gamedis_height = event.h
                gamedis_width = event.w
                size = [gamedis_width, gamedis_height]
                gamedis = pygame.display.set_mode(size, pygame.RESIZABLE)
            """
            # X BUTTON
            if event.type == pygame.QUIT:
                game_over = True
                return

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
                    game_score += 1
                    update_score(game_score)

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

        pos_x += pos_x_change
        pos_y += pos_y_change

        if (
            pos_x > (gamedis_width + scoreboard_width)
            or pos_x < scoreboard_width
            or pos_y > gamedis_height
            or pos_y < 0
        ):
            game_over = True
            print("Game is over! You hit a wall!")
            snake_List.clear()
            make_lose_screen()
            return

        # Updating snake head
        pygame.draw.rect(gamedis, BLACK, game_area)
        make_food(foodx, foody)
        snake_Head = []
        snake_Head.append(pos_x)
        snake_Head.append(pos_y)
        snake_List.append(snake_Head)

        if len(snake_List) > game_score + 1:
            del snake_List[0]

        update_snake(snake_List, pos_x, pos_y)

        # Did snake hit food?
        if pos_x == foodx and pos_y == foody:
            foodx = (
                round(random.randrange(0, gamedis_width - 200 - snake_icon_size) / 10.0)
                * 10.0
                + scoreboard_width
                + 100
            )
            foody = (
                round(
                    random.randrange(0, gamedis_height - 200 - snake_icon_size) / 10.0
                )
                * 10.0
                + 100
            )
            game_score += 1
            update_score(game_score)
            print("YEAH FOOD")

        # Check if snake hit itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True
                print("We hit uh ourselves")
                snake_List.clear()
                make_lose_screen()
                return

        pygame.display.flip()
        clock.tick(snake_speed)


logged_in = False
while game_on == False:
    logged_in = make_intro_screen()

if game_on and logged_in:
    make_game_screen()
    game_loop(game_over)


# Exiting the game
pygame.quit()
pygame.font.quit()
quit()
