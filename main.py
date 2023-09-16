import pygame

pygame.init()
pygame.font.init()

#########################################################
#VARIABLES
gamedis_width = 800
gamedis_height = 600
size = [gamedis_width, gamedis_height]

#scoreboard
scoreboard_width= 200
scoreboard_height = 600
orange = (227, 174, 59)
black = (0, 0, 0)
score_font_type = pygame.font.SysFont(None, 36)

#snake
snake_head_img = "./ASSETS/snake_head_test.png"
pos_x = gamedis_width / 2 + scoreboard_width / 2
pos_y = gamedis_height / 2
pos_x_change = 0
pos_y_change = 0


#apples
game_score = 0 

game_over = False

#speed
clock = pygame.time.Clock()
snake_speed = 50

######################################################
#MAKE GAME SCREEN
gamedis = pygame.display.set_mode(size)

#make scoreboard
pygame.draw.rect(gamedis, orange, pygame.Rect(0, 0, scoreboard_width, scoreboard_height))
#scoreboard_surface = pygame.Surface((scoreboard_width, scoreboard_height))
#scoreboard_surface.fill(orange)
score_display = score_font_type.render(f'Score: {game_score}', True, orange)
gamedis.blit(score_display, (30, 100))


#make initial snake
snake_head = pygame.image.load(snake_head_img).convert()
snake_head = pygame.transform.scale(snake_head, (10, 10))
gamedis.blit(snake_head, (pos_x, pos_y))

pygame.display.update()
pygame.display.set_caption("Snakes eat rocks")




#continuously run game until game_over = true (when game ends)
while not game_over:
    # Get all events
    gamedis.fill(black)
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
                score_display = score_font_type.render(f'Score: {game_score}', True, black) 
                gamedis.blit(score_display, (30, 100))
                pygame.display.update()
                        
    pos_x += pos_x_change
    pos_y += pos_y_change      

    #Updating Snake Head
    gamedis.blit(snake_head, (pos_x, pos_y))
    pygame.display.update()

    clock.tick(snake_speed)




#Exiting the Game
pygame.quit()
pygame.font.quit()
quit()