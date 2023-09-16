import pygame

pygame.init()
pygame.font.init()

#########################################################
#VARIABLES

#colors
orange = (227, 174, 59)
black = (0, 0, 0)
white = (255, 255, 255)

#game screen
gamedis_width = 600
gamedis_height = 600
size = [gamedis_width, gamedis_height]

#scoreboard
scoreboard_width = 200
scoreboard_height = 600

score_font_type = pygame.font.SysFont(None, 36)

#snake
snake_head_img = "./ASSETS/snake_head_test.png"
pos_x = gamedis_width / 2
pos_y = gamedis_height / 2
pos_x_change = 0
pos_y_change = 0


#apples
game_score = 0
game_over = False

#speed
clock = pygame.time.Clock()
snake_speed = 30

######################################################
#MAKE GAME SCREEN
gamedis = pygame.display.set_mode((800, 600))

#make main playing area
game_area = pygame.Rect(200, 0, gamedis_width, gamedis_height)
pygame.draw.rect(gamedis, black, game_area)

#make scoreboard
scoreboard = pygame.Rect(0, 0, scoreboard_width, scoreboard_height)
pygame.draw.rect(gamedis, orange, scoreboard)
score_display = score_font_type.render(f'Score: {game_score}', True, black)
gamedis.blit(score_display, (30, 100))

#make initial snake
snake_head = pygame.image.load(snake_head_img).convert()
snake_head = pygame.transform.scale(snake_head, (10, 10))
gamedis.blit(snake_head, (pos_x, pos_y))

pygame.display.flip()
pygame.display.set_caption("Snakes eat rocks")


#continuously run game until game_over = true (when game ends)
while not game_over:
    # Get all event
    score_change = False
    for event in pygame.event.get(): 
        '''
        #RESIZE WINDOW BUTTONs
        if event.type == pygame.VIDEORESIZE:
            gamedis_height = event.h
            gamedis_width = event.w
            size = [gamedis_width, gamedis_height]
            gamedis = pygame.display.set_mode(size, pygame.RESIZABLE)
        '''
        #X BUTTON
        if event.type == pygame.QUIT:
            game_over = True

        #Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pos_x_change = -10
                pos_y_change = 0
            elif event.key == pygame.K_RIGHT:
                pos_x_change = 10
                pos_y_change = 0
            elif event.key == pygame.K_UP:
                pos_x_change = 0
                pos_y_change = -10
            elif event.key == pygame.K_DOWN:
                pos_x_change = 0
                pos_y_change = 10
            elif event.key == pygame.K_1:
                score_change = True
                game_score += 1
                pygame.draw.rect(gamedis, orange, scoreboard)
                score_display = score_font_type.render(f'Score: {game_score}', True, black) 
                gamedis.blit(score_display, (30, 100))
                pygame.display.update()

    #Did snake hit wall?
    pos_x += pos_x_change
    pos_y += pos_y_change      

    if pos_x > (gamedis_width + scoreboard_width) or pos_x < scoreboard_width or pos_y > gamedis_height or pos_y < 0:
        game_over = True
        break

    #Updating Snake Head
    pygame.draw.rect(gamedis, black, game_area)
    gamedis.blit(snake_head, (pos_x, pos_y))
    pygame.display.update()

    clock.tick(snake_speed)


# You Lose XD
pygame.draw.rect(gamedis, black,game_area)
lose_text = score_font_type.render("RIP BOZO YOU LOSE", True, white)
gamedis.blit(lose_text, (gamedis_width/2, gamedis_height/2))
pygame.display.update()
pygame.time.wait(2000)

#Exiting the Game
pygame.quit()
pygame.font.quit()
quit()