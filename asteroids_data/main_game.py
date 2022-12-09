#main asteroids game
#GAME CREATED BY ELLIOT CODLING
import os, time
from engine import game_engine_71222 as game_engine
from random import randint

try:
    import pygame   #import pygame
except ModuleNotFoundError:
    game_engine.update.pygame_debug()

pygame.font.init()      #initilise the font
pygame.mixer.init()         #initilise music
#DOES NOT WORK WITH PYGAME 2.0 ON RASPBERRY PI 
file_dir = os.getcwd() # get the current directory

#create window -------------------------------------------
w, h = 480, 600
window = game_engine.window.define("Asterods", w, h)

#variables
run = True
run_game = True
clock = pygame.time.Clock()
vel = 6
frames = 0
frames_wait = 120
sprite_speed = 2
score = 0
high_score = 0
enable_collisions = True
#display
display = []


#create background of stars
x = 0
y = -60
for _ in range(11):
    for _ in range(6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        background_stars = game_engine.properties_object("background_stars_{}{}".format(x, y), "{}/textures/background-stars.png".format(file_dir), x, y, 80, 60, False)
        #flip the background image
        background_texture_new = pygame.transform.flip(background_stars.texture, horizontal, vertical)
        background_stars.texture = background_texture_new
        
        display += [background_stars]
        x += 80
    y += 60
    x = 0

#display_sprite
display_sprite = []
#foreground
foreground = []
#text_foreground
text_foreground = []

#sub program -----------------------------------------------------------------------
def create_rocks():
    #spawn new enemy at the top of screen
    global display_sprite
    x = 10
    y = -90
    for index in range(1, 6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        rock = game_engine.properties_object("rock_{}{}".format(x, y), "{}/textures/rock_brown.png".format(file_dir), x, y, 80, 80, True)
        #flip the background image
        rock_texture_new = pygame.transform.flip(rock.texture, horizontal, vertical)
        rock.texture = rock_texture_new
        
        display_sprite.insert(index, (rock))
        x += 90

    del_rock = randint(1, 5)
    del display_sprite[del_rock]
    #frames = 0
def update(window, display, display_sprite, foreground, text_foreground, clock):
    game_engine.window.update(window, display, display_sprite, foreground, text_foreground, clock, 0)
    
def reset_player():
    global display_sprite, rocket
    rocket = game_engine.properties_object("rocket", "{}/textures/spaceship.png".format(file_dir), (w/2) - 51 / 2, 518, 45, 51, False)
    display_sprite += [rocket]

def game_over():
    global display_sprite, text_foreground
    global run_game, score, frames
    
    #reset everything
    text_foreground = []
    display_sprite = []
    score, frames = 0, 0
    reset_player()
    create_rocks()  
    update_score()

    #lost text
    lost = game_engine.properties_text("lost_text", "You lost!", "YELLOW", w, h, 100, True)
    text_foreground += [lost]
    update(window, display, display_sprite, foreground, text_foreground, clock)
    pygame.time.delay(1000)
    del text_foreground[1]
    #stop the game and update the screen to its default text

    run_game = False
    update(window, display, display_sprite, foreground, text_foreground, clock)

def update_score():
    global text_foreground
    score_text = game_engine.properties_text("score", "Score: {}    High score: {}".format(score, high_score), "YELLOW", 20, 20, 30)
    text_foreground += [score_text]

def play_music():
    if pygame.mixer.music.get_busy():
        pass
    else:
        if gameplay == False:
            pygame.mixer.music.load("{}/Music/menu_start.ogg".format(file_dir))
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load("{}/Music/gameplay.ogg".format(file_dir))
            pygame.mixer.music.play(-1)

#main code --------------------------------------------------------------------------------
def gameplay():
    global display, display_sprite, text_foreground     #global lists used
    global frames, frames_wait, score, high_score, sprite_speed   #global variables used
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        game_engine.player.left(rocket, vel, 10)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        game_engine.player.right(rocket, vel, w - rocket.width - 10)
        
    #create scrolling background
    for image in display:
        if display[0].y == 0:
            x = 0
            y = -60
            for index in range(6):
                horizontal = randint(0, 1)
                vertical = randint(0, 0)
                
                background_stars = game_engine.properties_object("background_stars_{}{}".format(x, y), "{}/textures/background-stars.png".format(file_dir), x, y, 80, 60, False)
                #flip the background image
                background_texture_new = pygame.transform.flip(background_stars.texture, horizontal, vertical)
                background_stars.texture = background_texture_new
                
                display.insert(index, (background_stars))
                del display[len(display) - 1]
                x += 80
 
                
        else:
            image.y += 1

    #create new rocks if the amount of frames passed == frames to wait for
    frames += 1
    if frames >= frames_wait:
        create_rocks()
        frames = 0
    
    #delete the rocks that hit y coord 700
    if display_sprite[len(display_sprite) - 1].y >= 700:
        del display_sprite[len(display_sprite) - 1]
        score += 0.25

    #move the rocks
    for index in range(1, len(display_sprite)):
        display_sprite[index].y += sprite_speed
    
        collision = game_engine.player.collisions(rocket, display_sprite, index)
        if collision != None and enable_collisions == True:
            if score > high_score:
                high_score = score

            game_over()
            break   
        
    #update the text_foreground
    del text_foreground[0]
    update_score()

    #levels
    if score == 10:
        score += 5
        del text_foreground[0]
        update_score()
        sprite_speed, frames_wait = 4, 80
        level_text = game_engine.properties_text("level", "2X Speed!", "YELLOW", w, h, 100, True)
        text_foreground += [level_text]
        update(window, display, display_sprite, foreground, text_foreground, clock)
        pygame.time.delay(2000)
        del text_foreground[1]

reset_player()          
create_rocks()  
update_score()
while run:
    #keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:       #exit if esc key has been pressed
        run = False
    if keys[pygame.K_f]:
        run_game = True
    play_music()
    if run_game:
        gameplay()

    update(window, display, display_sprite, foreground, text_foreground, clock)
    clock.tick(60)

pygame.quit()
print("Quiting...")