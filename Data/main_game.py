#GAME CREATED BY ELLIOT CODLING

import os, time   #import os
from Ele_Engine import game_engine_003 as game_engine     #import custom game engine
from random import randint      #import random
try:
    import pygame   #import pygame
except:
    game_engine.update.pygame_debug()

pygame.font.init()      #initilise the font,
#DOES NOT WORK WITH PYGAME 2.0 ON RASPBERRY PI 
file_dir = os.getcwd() # get the current directory

#define window ------------------------------------------------
w, h = 480, 600           #screen width and height

game_engine.update.define("Asteroids", w, h)            #define window with name and width and height
game_engine.player.left_border(10)      #to define where the left border is of the screen
game_engine.player.right_border(w - 106)    #to define where the right border is of the screen

#not required as the player cannot go up / down in this game
#game_engine.player.top_border(10)   #to define where the top border is of the screen
#game_engine.player.bottom_border(h - 106)    #to define where the bottom border is of the screen

#----------------------------------------------------------------

# define variables -----------------------------------------
#background
display = []        #define the array for background
background_stars = pygame.image.load("{}/Textures/background-stars.png".format(file_dir))
background_stars = pygame.transform.scale(background_stars, (80, 60))
background_stars = background_stars.convert()

#sprites
display_sprite =[]      #define the array for sprites, including the player
sprite = pygame.image.load("{}/Textures/spaceship.png".format(file_dir))
enemy_rock = pygame.image.load("{}/Textures/rock_brown.png".format(file_dir))
enemy_rock = pygame.transform.scale(enemy_rock, (80, 80))
#enemy_rock = enemy_rock.convert()          #do not use, removes transparency

#forground
#score
score = 0               #create variable score
high_score = 0          #create high score
foreground = []         #create the array for the foreground

#text_foreground
text_foreground = []
font = pygame.font.SysFont(None, 30)        #inisilise the font
score_text = font.render("Score: {}    High Score: {}".format(score, high_score), True, pygame.Color("YELLOW"))
text_foreground.insert(0, (score_text, [20, 20]))

#other stuff
clock = pygame.time.Clock()     #get the clock for pygame
frames = 0              #count how many frames have been made so know when to spawn enemy rocks
sprite_speed = 2        #set the speed of other sprites (rocks)
frame_wait = 120        #this sets how many frames will be drawn until new enemy spawns
gameplay = False           #set this to not immediately play the game
volume = 1          #set the volume level

#menu boolen / buttons for sub menu
menu_start = True           #display the start / home menu
options = False             #when to show options menu instead of other menus / sub menus

#creating background
x = 0
y = -60
for _ in range(11):
    for _ in range(6):
        horizontal = randint(0, 1)      #randomise horizontal flip
        vertical = randint(0, 1)        #randomise vertical flip
        #flip the background img
        background_stars = pygame.transform.flip(background_stars, horizontal, vertical)
        display += [(background_stars, [x, y])]   #put the image into the display array
        x += 80
    y += 60
    x = 0

#-----------------------------------------------------------

# player startup ----------------------------------------------------------------
def reset_player():
    global player_screenx, player_screeny, player_x, player_y, player_width, player_height, vel, display_sprite         #globalise the player pos
    player_screenx = ((w / 2) - 96) + 48   #define player screen x coords 
    player_screeny = 500      #define player screen y coords
    player_x = ((w / 2) - 96) + 78       #define player x coords
    player_y = 518        #define player y coords
    vel = 6     #define player velocity
    display_sprite = [(sprite, [player_screenx, player_screeny])]      #put player in display array for rendering

    #create new collision detection
    player_width = 36           #width
    player_height = 24          #height
reset_player()
# --------------------------------------------------------------------------------

# main menu ---------------------------------------------------------------------------------
def main_menu():
    global gameplay, run, volume, text_foreground, font
    global menu_start, options
    mx, my = pygame.mouse.get_pos()                 #get mouse pos
    click = False
    
    if pygame.mouse.get_pressed()[0]:               #check if left mouse button is clicked
        click = True

    if click == True:               #check if mouse left button is pressed
        if menu_start == True:
            if start_button.collidepoint((mx, my)):                 #check if the start button has been collided
                gameplay = True
                for _ in range(3):                      #delete the text for the main menu
                    del text_foreground[1]
                pygame.mixer.music.stop()               #stop the music

            elif options_button.collidepoint((mx, my)):
                for _ in range(3):
                    del text_foreground[1]
                reset_options(text_foreground)
                menu_start = False          #stop the menu main stuff
                options = True          #allow the options menu to work for buttons
                

            elif exit_button.collidepoint((mx, my)):
                run = False

        else:
            if options == True:                     #submenu options
                if back_button.collidepoint((mx, my)):                  #check for mouse over back button
                    options = False
                    menu_start = True

                    for _ in range(4):                  #delete "back", "music", "-", "+"
                        del text_foreground[1]

                    delay(150)
                    reset_screen(text_foreground)

                elif volume_down_button.collidepoint((mx, my)):
                    if volume <= 0.1:               #don't go below 0
                        pass
                    else:
                        volume -= 0.1                       #reduce volume  
                        pygame.mixer.music.set_volume(volume)       #set volume of the music
                        delay(150)
                        for _ in range(4):              #delete "back", "music", "-", "+"
                            del text_foreground[1]
                        reset_options(text_foreground)

                elif volume_up_button.collidepoint((mx, my)):
                    if volume >= 1:
                        pass
                    else:
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)       #set volume of the music
                        delay(150)                  #pause the code for 0.15 secs
                        for _ in range(4):
                            del text_foreground[1]
                            
                        reset_options(text_foreground)

# --------------------------------------------------------------------------------------------

# sub code ------------------------------------------------------------------------------------
def reset_options(text_foreground):
    #used so that the submenu options can be redrawn so that music can change on screen
    global font  
    global back_button, volume_down_button, volume_up_button
    back_txt = font.render("[ Back ]".format(volume), True, pygame.Color("YELLOW"))             #create the back button
    text_rect = back_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(back_txt, [text_rect[0], text_rect[1]])]
    back_button = pygame.Rect(text_rect[0], text_rect[1], text_rect[2], text_rect[3])
        
    music_txt = font.render("[ Music: {} ]".format(round(volume * 10, 1)), True, pygame.Color("YELLOW"))
    text_rect = music_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(music_txt, [text_rect[0], text_rect[1] + 40])]

    font = pygame.font.SysFont(None, 70)        #inisilise the font
    music_volume_down_txt = font.render("-", True, pygame.Color("YELLOW"))
    text_rect = music_volume_down_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(music_volume_down_txt, [text_rect[0] - 25, text_rect[1] + 80])]
    volume_down_button = pygame.Rect(text_rect[0] - 25, text_rect[1] + 80, text_rect[2], text_rect[3])
    
    music_volume_up_txt = font.render("+", True, pygame.Color("YELLOW"))
    text_rect = music_volume_up_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(music_volume_up_txt, [text_rect[0] + 25, text_rect[1] + 80])]
    volume_up_button = pygame.Rect(text_rect[0] + 25, text_rect[1] + 80, text_rect[2], text_rect[3])
    font = pygame.font.SysFont(None, 30)        #inisilise the font

def delay(time):            #delay the game by the variable time
    pygame.time.delay(time)

def add_score(points):              #add to the score of the variable points
    global score
    score += points         #add to score
    #score
    #only update the scoreboard when nessisary
    font = pygame.font.SysFont(None, 30)        #inisilise the font
    score_text = font.render("Score: {}    High Score: {}".format(score, high_score), True, pygame.Color("YELLOW"))            #state score at (20, 20)
    text_foreground.insert(0, (score_text, [20, 20]))            #insert this score img to index 0
    del text_foreground[1]                   #the current score will be moved to 1 so need to add this to delete it

def update(display, display_sprite, foreground, text_foreground, clock):                    #update the screen
    game_engine.update.window(display, display_sprite, foreground, text_foreground, clock)
    
def reset_screen(text_foreground):                          #reset the screen to the main menu
    start_txt = font.render("[ Start Game ]", True, pygame.Color("YELLOW"))
    text_rect = start_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(start_txt, [text_rect[0], text_rect[1]])]
    start_button = pygame.Rect(text_rect[0], text_rect[1], text_rect[2], text_rect[3])                  #create invisible buttons so that collide point can happen in main_menu

    options_txt = font.render("[ Options ]", True, pygame.Color("YELLOW"))
    text_rect = options_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(options_txt, [text_rect[0], text_rect[1] + 40])]
    options_button = pygame.Rect(text_rect[0], text_rect[1] + 40, text_rect[2], text_rect[3])

    exit_txt = font.render("[ Exit Game ]", True, pygame.Color("YELLOW"))
    text_rect = exit_txt.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground += [(exit_txt, [text_rect[0], text_rect[1] + 80])]
    exit_button = pygame.Rect(text_rect[0], text_rect[1] + 80, text_rect[2], text_rect[3])

    return start_button, options_button, exit_button

def game_over():
    #game over?
    global gameplay
    font = pygame.font.SysFont(None, 100)        #inisilise the font
    lost = font.render("You lost!", True, pygame.Color("YELLOW"))        #render the image for the text, 
    #this is required for pygame version less than 2.0
    text_rect = lost.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
    text_foreground.insert(1, (lost, [text_rect[0], text_rect[1]]))         #add the game over text to the text_foreground          
    
    update(display, display_sprite, foreground, text_foreground, clock)     #update the screen to show the "You Lost!"
    delay(500)             #stop the game for 0.5 secs

    del text_foreground[1]              #remove the "You Lost!"
    game_engine.music.fade_out(volume, 0, 0.1)           #fade the music
    reset_screen(text_foreground)                   #reset the screen to the title
    gameplay = False                    #stop playing the game
# ------------------------------------------------------------------------------------------------------------------------------------------------

# main game code loop ------------------------------------------------------------------------------------------------------------------------------

def main_game():                    
    global player_screenx, player_screeny, player_x, player_y, player_width, player_height, vel              #importing player variables
    global display_sprite, display, foreground, text_foreground              #globalise all screen arrays
    global background_stars, enemy_rock                    #globalise texture variables
    global score, high_score                     #scoring system
    global  frames, sprite_speed, frame_wait               #other stuff

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        # set out the players screen coords, as well as its x and y coords, including velocity
        player_screenx, player_x = game_engine.player.left(player_screenx, player_x, vel)
        display_sprite[0][1][0] = player_screenx

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_screenx, player_x = game_engine.player.right(player_screenx, player_x, vel)
        display_sprite[0][1][0] = player_screenx

    #this part is not needed for this program however is here if needed
    """
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_screeny, player_y = game_engine.player.up(player_screeny, player_y, vel)
        display_sprite[0][1][1] = player_screeny

    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_screeny, player_y = game_engine.player.down(player_screeny, player_y, vel)
        display_sprite[0][1][1] = player_screeny
    """
    #debug
    if keys[pygame.K_b]:
        game_engine.update.list_debug(display, display_sprite, foreground, text_foreground, clock)
    
    
    #create scrolling background
    length = len(display)       #find the length of the display array to find how many textures there are to change
    length = int(length)        #turn the str into int

    #v standing for variable
    for v in range(length):
        #find the coords
        #create new img when index 0, y == 0
        if display[0][1][1] >= 0:
            #print(True)
            x = 0
            y = -60             #create at y = -60, prevent 'jittering'
            for v in range(6):
                horizontal = randint(0, 1)      #randomise horizontal flip
                vertical = randint(0, 1)        #randomise vertical flip
                #flip the background img
                background_stars = pygame.transform.flip(background_stars, horizontal, vertical)

                display.insert(v, (background_stars, [x, y]))       #insert the img at the new index
                #everytime this completes a cycle the index increases by 1, this is why del [330] is a constant number as all the.
                #rest of the img get shifted by 1
                del display[66]        #delete the oldest index img
                x += 80

        else:
            display[v][1][1] += 1           #how much the background moves 

    #when to spawn new enemy at the top of the screen
    frames += 1                     #add frames by 1
    if frames >= frame_wait:               #wait for frames to be bigger than frame_wait
        x = 10              #set x coord
        for v in range(5):
            horizontal = randint(0, 1)      #randomise horizontal flip
            vertical = randint(0, 1)        #randomise vertical flip
            #flip the background img
            enemy_rock = pygame.transform.flip(enemy_rock, horizontal, vertical)
            display_sprite.insert(v + 1, (enemy_rock, [x, -90]))          #add new rock to display_sprite
            x += 90             #add the x coord by 90
            

        random_num = randint(1, 5)
        del display_sprite[random_num]
        frames = 0                  #reset frame variable

    #create enemy sprites on the screen in the display_sprite array
    length = len(display_sprite)
    length = int(length)
  
    #check to see if the player has collided with any rocks
    for v in range(1, length):
        collided_image = game_engine.player.collisions(player_x, player_y, player_width, player_height, display_sprite, v)
        collided_image = str(collided_image)            #change the collision to str
        enemy_rock_str = enemy_rock             #create new variable
        enemy_rock_str = str(enemy_rock_str)            #change to str
        if collided_image == enemy_rock_str:            #check if collided image is the enemy rock
            frame_wait = 120            #frame wait to default setting
            sprite_speed = 2            #set the default speed of rocks

            
            
            if score > high_score:                  #high score system
                high_score_array = [score]             #add score to the array
                high_score = high_score_array[0]                #make the high score == to the high score array

            score = 0               #score is 0
            add_score(0)
            game_over()
            reset_player()
            break

        else:
            display_sprite[v][1][1] += sprite_speed         #move the sprites by the sprite speed

    #check to see if the rocks are below the y value 700, this is to delete them and add score to player score
    for v in range(1, length):
        length = len(display_sprite)            #this is because as it deletes the sprites the array changes legnth so this is needed for no errors
        length = int(length)            #change to int

        if display_sprite[length - 1][1][1] > 700:              #check if the last sprite y is greater than 700
            del display_sprite[length - 1]                  #delete that sprite
            add_score(0.25)                     #add this per rock (4 rocks each, 4 * 0.25 = 1)

    
    #levels
    if score == 10:             #level 1 when score == 10
        add_score(5)              #give  player 5 points for getting 10 points
        sprite_speed = 4            #increase rock speed by 4
        frame_wait = 80             #create rocks every 80 frames
        
        font = pygame.font.SysFont(None, 100)        #inisilise the font
        level = font.render("2X Speed!", True, pygame.Color("WHITE"))        #render the image for the text, 
        #this is required for pygame version less than 2.0
        text_rect = level.get_rect(center=(w / 2, h / 2))             #do stuff to centre the text
        text_foreground.insert(1, (level, [text_rect[0], text_rect[1]]))         #insert 2x speed into text_foreground
        #delay_game = True               #delay the game
        update(display, display_sprite, foreground, text_foreground, clock)
        delay(2000)
        del text_foreground[1]
    
    
# -------------------------------------------------------

# music --------------------------------------------------------------------------
pygame.mixer.init()         #initilise music
def music():                #create the function

    if pygame.mixer.music.get_busy() == True:               #check if busy
        pass

    else:
        if gameplay == False:                  #if in menu play this track
            pygame.mixer.music.load("{}/Music/menu_start.ogg".format(file_dir))
            pygame.mixer.music.play(-1)

        elif gameplay == True:                 #else play this during gameplay
            pygame.mixer.music.load("{}/Music/gameplay.ogg".format(file_dir))
            pygame.mixer.music.play(-1)
# -------------------------------------------------------------------------------

#main game loop --------------------------------------------
run = True
start_button, options_button, exit_button = reset_screen(text_foreground)
while run:
    try:
        # keyboard and exit button, main code -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        music()
        if not gameplay:
            main_menu()     #start main_menu
            
        else:
            main_game()     #execute the main code

        #exit game
        if keys[pygame.K_ESCAPE]:
            run = False
        # ---------------------------------------------------------

        # update screen ----------------------------------------
        #game_engine.update.debug(True, player_x, player_y, player_width, player_height)
        update(display, display_sprite, foreground, text_foreground, clock)     #update the window
        clock.tick(60)  #limit to 60 fps

        #--------------------------------------------------------

    except FileNotFoundError:      #stop code if there is an error with pygame
        run  = False
        #pygame.error

# --------------------------------------
pygame.quit()