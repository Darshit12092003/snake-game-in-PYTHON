import pygame
import random
import os

#initailizing pygame!
pygame.init()
pygame.mixer.init()# initailize the mixer for the game music!

# Creating Game Window 
window_height=500
window_width=800
gameWindow = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('My first python game')

# Background Images
bgimg = pygame.image.load('InGameBackground.jpg')
bgimg = pygame.transform.scale( bgimg, ( window_width, window_height ) ).convert_alpha() # convert alpha is used for smooth bliting of background image!
startimg = pygame.image.load('Snake.jpg')
startimg = pygame.transform.scale( startimg, (window_width,window_height) ).convert_alpha()
endimg = pygame.image.load('GameOver.jpg')
endimg = pygame.transform.scale ( endimg, (window_width,window_height) ).convert_alpha()

# Defining Game Colors
white = (255,255,255) # rgb format
red = (255,0,0) 
black = (0,0,0)
green = (0,190,0)


# clock
clock = pygame.time.Clock()

# font for score
font = pygame.font.SysFont(None,40)


# functions of the game!

def plot_snake(window,color,snake_list,snakesize):
    for x,y in snake_list:
        pygame.draw.rect(window,color,(x,y,snakesize,snakesize))
        
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text , (x,y))
    #here, second attribute is anti-aliasing!

def welcome():
    exit_game = False
    
    while not exit_game:
        
        gameWindow.fill(white)
        gameWindow.blit(startimg , (0,0))
        
        text_screen("Welcome to Snake Game!",black,100,210)
        text_screen("Press Spacebar to continue!",black,85,235)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    # # For Game Music
                    # pygame.mixer.music.load('InGameMusic.mp3')
                    # pygame.mixer.music.play()

                    gameloop()
                    
        pygame.display.update()
        clock.tick(30)
    pygame.quit()
    quit()

def gameloop():
    
    # Game Specific Variables
    game_over = False
    exit_game = False 
    score=0
    FPS = 60
    
    #defining snake attributes
    snake_x=55
    snake_y=55
    snake_size=10
    velocity_x=0
    velocity_y=0
    
    # defining variables for the increament in length of the snake
    snake_list = []
    snake_length = 1
    
    # defining food 
    food_x=random.randint(50,window_width-50) # here,we take range from 50 to width-50 for avoiding the collision of food with the 'score' displaying on the window!
    food_y=random.randint(50,window_height-50)
    food_size=10
    
    if(not os.path.exists("highscore.txt")): # if highscore file do not exist, it will create one!
        f=open('highscore.txt','w')
        f.write(str(0))
        f.close()
    f=open('highscore.txt','r')
    highscore=f.read()
    f.close()
    
    while not exit_game:
        
        if game_over:
            
            f=open('highscore.txt','w')
            f.write(str(highscore))
            f.close()
            
            # gameWindow.fill(white)
            gameWindow.blit(endimg, (0,0))
            text_screen("Game Over! Press Enter to Continue!",green,160,310)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                #print(event) to check how the pygame.event.get() is work!

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x += 4
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x -= 4
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y -= 4
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y += 4
                        velocity_x=0

            # assigning the velocity value to coordinates!
            snake_x = snake_x + velocity_x 
            snake_y = snake_y + velocity_y

            if abs(snake_x-food_x)<7 and abs(snake_y-food_y)<7:

                score+=10
                food_x=random.randint(50,window_width-50)
                food_y=random.randint(50,window_height-50)
                snake_length += 5

                # for food music 
                pygame.mixer.music.load('Food.mp3')
                pygame.mixer.music.play()

                if score > int(highscore):
                    highscore=score


            # gameWindow.fill(white)
            gameWindow.blit(bgimg , (0,0))

            text_screen(f"Score: {score}  Highscore: {highscore}",red,5,5)
            pygame.draw.rect(gameWindow,red,(food_x,food_y,food_size,food_size))


            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            
            if head in snake_list[:-1]: #if any cordinates of head in list excluding last element of the list then, game will be over!
#                 print(snake_list) to understand excactly!
                game_over = True
                pygame.mixer.music.load('Gameover.mp3')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>window_width or snake_y<0 or snake_y>window_height:
                game_over = True
                pygame.mixer.music.load('Gameover.mp3')
                pygame.mixer.music.play()
            

            plot_snake(gameWindow,black,snake_list,snake_size)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()
    
welcome()
# gameloop()