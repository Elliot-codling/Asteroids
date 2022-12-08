#main asteroids game
#GAME CREATED BY ELLIOT CODLING

import os, time
from engine import game_engine_71222 as game_engine
from random import randint

try:
    import pygame   #import pygame
except ModuleNotFoundError:
    game_engine.update.pygame_debug()

pygame.font.init()      #initilise the font,
#DOES NOT WORK WITH PYGAME 2.0 ON RASPBERRY PI 
file_dir = os.getcwd() # get the current directory

#create window -------------------------------------------
w, h = 480, 600
window = game_engine.window.define("Asterods", w, h)

#variables
run = True
clock = pygame.time.Clock()
vel = 6

#lists
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
rocket = game_engine.properties_object("rocket", "{}/textures/spaceship.png".format(file_dir), ((w/2) - 96) + 50, 518, 96, 96, True)
display_sprite += [rocket]

#foreground
foreground = []
#text_foreground
text_foreground = []


#main code --------------------------------------------------------------------------------
def gameplay():
    global display
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        game_engine.player.left(rocket, vel, 10)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        game_engine.player.right(rocket, vel, w - 106)
        
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
                

while run:
    #keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    

    if keys[pygame.K_ESCAPE]:       #exit if esc key has been pressed
        run = False
    
    gameplay()
    game_engine.window.update(window, display, display_sprite, foreground, text_foreground, clock, 0)
    clock.tick(60)

pygame.quit()
print("Quiting...")