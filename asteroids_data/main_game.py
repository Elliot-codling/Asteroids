#main asteroids game
#GAME CREATED BY ELLIOT CODLING
import os
from engine import game_engine_131222 as game_engine
from random import randint

try:
    import pygame   #import pygame
except ModuleNotFoundError:
    game_engine.update.pygame_debug()

pygame.font.init()      #initilise the font
pygame.mixer.init()         #initilise music

file_dir = os.getcwd() # get the current directory

#create window -------------------------------------------
w, h = 480, 600
window = game_engine.window.define("Asterods", w, h)

#variables
run = True
run_game = False
clock = pygame.time.Clock()
vel = 6
frames = 0
frames_wait = 145
sprite_speed = 2
score = 0
high_score = 0
enable_collisions = True
volume = 10
performance_mode = False

#load in textures
global background_stars_texture, rock_texture
background_stars_texture = pygame.image.load("{}/textures/background-stars.png".format(file_dir))
rock_texture = pygame.image.load("{}/textures/rock_brown.png".format(file_dir))
#display
display = []
#create background of stars
x = 0
y = -60
for _ in range(11):
    for _ in range(6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        background_stars = game_engine.properties_object("background_stars_{}{}".format(x, y), background_stars_texture, x, y, 80, 60, False)
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

#main menu --------------------------------------------------------
def init_main_menu():
    global foreground, text_foreground
    #create text
    start_text = game_engine.properties_text("start", "[ Start Game ]", "YELLOW", w, h, 45, True)
    options_text = game_engine.properties_text("start", "[ Options ]", "YELLOW", w, h + 80, 45, True)
    exit_text = game_engine.properties_text("start", "[ Exit Game ]", "YELLOW", w, h + 160, 45, True)
    #create boxes that are invisable
    start_button = game_engine.properties_object("start_button", "{}/textures/invisable_button.png".format(file_dir), start_text.x, start_text.y, start_text.texture.get_width(), start_text.texture.get_height(), not performance_mode)
    options_button = game_engine.properties_object("options_button", "{}/textures/invisable_button.png".format(file_dir), options_text.x, options_text.y, options_text.texture.get_width(), options_text.texture.get_height(), not performance_mode)
    exit_button = game_engine.properties_object("exit_button", "{}/textures/invisable_button.png".format(file_dir), exit_text.x, exit_text.y, exit_text.texture.get_width(), exit_text.texture.get_height(), not performance_mode)
    
    foreground += [start_button, options_button, exit_button]
    text_foreground += [start_text, options_text, exit_text]

def init_options_menu():
    global foreground, text_foreground
    #create text
    back_text = game_engine.properties_text("start", "[ Back ]", "YELLOW", w, h, 45, True)
    music_text = game_engine.properties_text("start", "[ Music  level: {} ]".format(volume), "YELLOW", w, h + 80, 45, True)
    volume_down_text = game_engine.properties_text("start", "[ - ]", "YELLOW", w - 60, h + 160, 45, True)
    volume_up_text = game_engine.properties_text("start", "[ + ]", "YELLOW", w + 60, h + 160, 45, True)
    performance_text = game_engine.properties_text("performance_text", "[ Performance mode: {} ]".format(performance_mode), "YELLOW", w, h + 240, 45, True)
    #create boxes that are invisable
    back_button = game_engine.properties_object("back_button", "{}/textures/invisable_button.png".format(file_dir), back_text.x, back_text.y, back_text.texture.get_width(), back_text.texture.get_height(), not performance_mode)
    volume_down_button = game_engine.properties_object("volume_down_button", "{}/textures/invisable_button.png".format(file_dir), volume_down_text.x, volume_down_text.y, volume_down_text.texture.get_width(), volume_down_text.texture.get_height(), not performance_mode)
    volume_up_button = game_engine.properties_object("volume_up_button", "{}/textures/invisable_button.png".format(file_dir), volume_up_text.x, volume_up_text.y, volume_up_text.texture.get_width(), volume_up_text.texture.get_height(), not performance_mode)
    performance_button = game_engine.properties_object("performance_button", "{}/textures/invisable_button.png".format(file_dir), performance_text.x, performance_text.y, performance_text.texture.get_width(), performance_text.texture.get_height(), not performance_mode)
    
    foreground += [back_button, volume_down_button, volume_up_button, performance_button]
    text_foreground += [back_text, music_text, volume_down_text, volume_up_text, performance_text]
    
def main_menu():
    global display_sprite, foreground, text_foreground
    global run_game, run, volume, performance_mode
    pygame.time.delay(100)
    if not pygame.mouse.get_pressed()[0]:
        pass
    #main start menu
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "start_button", foreground):
        #delete everything the init main menu started and start the game
        pygame.mixer.music.stop()
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        run_game = True

    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "options_button", foreground):
        #delete everything the init main menu started
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        init_options_menu()
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "exit_button", foreground):
        run = False
    #options menu
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "back_button", foreground):
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        init_main_menu()
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "volume_down_button", foreground):
        if volume > 0:
            volume -= 1
        pygame.mixer.music.set_volume(volume / 10)
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        init_options_menu()
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "volume_up_button", foreground):
        if volume < 10:
            volume += 1
        pygame.mixer.music.set_volume(volume / 10)
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        init_options_menu()    
    elif game_engine.mouse.collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], "performance_button", foreground):
        #flip the variable performance_mode and reset the screen
        performance_mode = not performance_mode
        foreground = []
        for _ in range(len(text_foreground) - 1):
            del text_foreground[1]
        init_options_menu()

        display_sprite = []
        reset_player()
        create_rocks()

#sub program -----------------------------------------------------------------------
def create_rocks():
    #spawn new enemy at the top of screen
    global display_sprite
    x = 10
    y = -90
    for index in range(1, 6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        rock = game_engine.properties_object("rock_{}{}".format(x, y), rock_texture, x, y, 80, 80, not performance_mode)
        #flip the background image
        rock_texture_new = pygame.transform.flip(rock.texture, horizontal, vertical)
        rock.texture = rock_texture_new
        
        display_sprite.insert(index, (rock))
        x += 90

    del_rock = randint(1, 5)
    del display_sprite[del_rock]

def update(window, display, display_sprite, foreground, text_foreground, clock):
    game_engine.window.update(window, display, display_sprite, foreground, text_foreground, clock, 0)
    
def reset_player():
    global display_sprite, rocket
    rocket = game_engine.properties_object("rocket", "{}/textures/spaceship.png".format(file_dir), (w/2) - 51 / 2, 518, 45, 51, not performance_mode)
    display_sprite += [rocket]

def game_over():
    global display_sprite, text_foreground
    global run_game, score, high_score, frames, frames_wait, sprite_speed
    if score > high_score:
        high_score = score
    #reset everything
    text_foreground = []
    display_sprite = []
    score, frames, frames_wait, sprite_speed = 0, 0, 145, 2
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
    game_engine.music.fade_out(volume / 10, 0, 0.1)
    init_main_menu()
    update(window, display, display_sprite, foreground, text_foreground, clock)

def update_score():
    global text_foreground
    score_text = game_engine.properties_text("score", "Score: {}    High score: {}".format(int(score), int(high_score)), "YELLOW", 20, 20, 30)
    text_foreground += [score_text]

def play_music():
    if pygame.mixer.music.get_busy():
        pass
    else:
        if run_game == False:
            pygame.mixer.music.load("{}/music/menu_start.ogg".format(file_dir))
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load("{}/music/gameplay.ogg".format(file_dir))
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
                
                background_stars = game_engine.properties_object("background_star", background_stars_texture, x, y, 80, 60, performance_mode)
                #flip the background image
                background_texture_new = pygame.transform.flip(background_stars.texture, horizontal, vertical)
                background_stars.texture = background_texture_new
                
                display.insert(index, (background_stars))
                del display[66]
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
        #update the text_foreground
        del text_foreground[0]
        update_score()

    #levels
    if score == 10:
        score += 5
        del text_foreground[0]
        update_score()
        sprite_speed, frames_wait, frames = 4, 90, 0
        level_text = game_engine.properties_text("level", "2X Speed!", "YELLOW", w, h, 100, True)
        text_foreground += [level_text]
        update(window, display, display_sprite, foreground, text_foreground, clock)
        pygame.time.delay(2000)
        del text_foreground[1]

    #move the rocks
    for index in range(1, len(display_sprite)):
        display_sprite[index].y += sprite_speed
    
        collision = game_engine.player.collisions(rocket, display_sprite, index)
        if collision != None and enable_collisions == True:
            game_over()
            break       

#initilise the start of the program
reset_player()          
create_rocks()  
update_score()
init_main_menu()
while run:
    #keyboard and exit button, main code -----------------------------
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:       #exit if esc key has been pressed
        run = False
    if keys[pygame.K_BACKSPACE]:
        game_over()

    play_music()
    if run_game:
        gameplay()
       
    else:
        main_menu()

    update(window, display, display_sprite, foreground, text_foreground, clock)
    clock.tick(60)   

pygame.quit()
print("Quiting...")