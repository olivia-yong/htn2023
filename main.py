import pygame
pygame.init()


#CONSTANTS
size = [800, 600]

#make game screen
gamedis = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.update()
pygame.display.set_caption("Snake eat rocks")

#create boolean to determine game state
game_over = False


#continuously run game until game_over = true (when game ends)
while not game_over:
    # Get all events
    for event in pygame.event.get(): 

        #RESIZE WINDOW BUTTONs
        if event.type == pygame.VIDEORESIZE:
            gamedis = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        #X BUTTON
        if event.type == pygame.QUIT:
            game_over = True
        print(event)

#Exiting the Game
pygame.quit()
quit()