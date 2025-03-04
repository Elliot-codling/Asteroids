#main asteroids game
from engine import game_engine_240123 as engine
from random import randint; import os, pygame
pygame.font.init()      #initilise the font
file_dir = os.getcwd() # get the current directory
activate_music = engine.activate_music

#variables
run = True              #main game loop - if false stops the program
run_game = False                #runs the game - if false returns to the main menu
clock = pygame.time.Clock()
vel = 6             #speed of the player left and right
frames_wait = 145               # the amount of frames to wait until creating a new set of rocks 
wait = engine.frames + frames_wait                        #the future time of when the asteroids should be spawned in
sprite_speed = 2                #speed of the rocks to travel towards the player
score = 0               #current score
high_score = 0              #current high score
enable_collisions = True                #collsions
volume = 10             #volume of the game 
performance_mode = False                #performance mode - disables all transparencies
enable_vsync = True             #enables vsync

#create window -------------------------------------------
w, h = 480, 600
window = engine.window("Asterods", w, h, (0, 0, 0), pygame.SCALED, enable_vsync)

#load in textures - to always store them in ram
global background_stars_texture, rock_texture
background_stars_texture = pygame.image.load(f"{file_dir}/textures/background-stars.png")
rock_texture = pygame.image.load(f"{file_dir}/textures/rock_brown.png")
#display
display = []
#create background of stars
x = 0
y = -60
for _ in range(11):
    for _ in range(6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        background_stars = engine.properties_object(f"background_stars_{x}{y}", background_stars_texture, x, y, 80, 60, False)
        #flip the background image
        background_stars.texture = pygame.transform.flip(background_stars.texture, horizontal, vertical)
        
        display += [background_stars]
        x += 80
    y += 60
    x = 0

#display_sprite
display_sprite = []
#spaceship animation
playerAnimation = [pygame.image.load(f"{file_dir}/textures/spaceship.png"), pygame.image.load(f"{file_dir}/textures/spaceship_3.png"), pygame.image.load(f"{file_dir}/textures/spaceship_2.png")]
#foreground
foreground = []
#text_foreground
text_foreground = []
score_text = engine.properties_text("score", f"Score: {int(score)}    High score: {int(high_score)}", "YELLOW", 20, 20, 30)
text_foreground += [score_text]

#main menu --------------------------------------------------------
def delete_text():          #removes all of the invisable buttons and removed all of the text in index 1
    global foreground, text_foreground
    foreground = []
    for _ in range(len(text_foreground) - 1):
        del text_foreground[1]

def init_main_menu():               #creates all the text and all the invisable buttons
    global foreground, text_foreground
    #create text
    start_text = engine.properties_text("start", "[ Start Game ]", "YELLOW", w, h, 45, True)
    options_text = engine.properties_text("options", "[ Options ]", "YELLOW", w, h + 80, 45, True)
    exit_text = engine.properties_text("exit", "[ Exit Game ]", "YELLOW", w, h + 160, 45, True)
    #create boxes that are invisable
    start_button = engine.properties_object("start_button", f"{file_dir}/textures/invisable_button.png", start_text.x, start_text.y, start_text.texture.get_width(), start_text.texture.get_height(), not performance_mode)
    options_button = engine.properties_object("options_button", f"{file_dir}/textures/invisable_button.png", options_text.x, options_text.y, options_text.texture.get_width(), options_text.texture.get_height(), not performance_mode)
    exit_button = engine.properties_object("exit_button", f"{file_dir}/textures/invisable_button.png", exit_text.x, exit_text.y, exit_text.texture.get_width(), exit_text.texture.get_height(), not performance_mode)
    
    foreground += [start_button, options_button, exit_button]
    text_foreground += [start_text, options_text, exit_text]

def init_options_menu():            #creates all the text and all the invisable buttons
    global foreground, text_foreground
    #create text
    back_text = engine.properties_text("back", "[ Back ]", "YELLOW", w, h, 45, True)
    music_text = engine.properties_text("music", f"[ Music  level: {volume} ]", "YELLOW", w, h + 80, 45, True)
    volume_down_text = engine.properties_text("voldown", "[ - ]", "YELLOW", w - 60, h + 160, 45, True)
    volume_up_text = engine.properties_text("volup", "[ + ]", "YELLOW", w + 60, h + 160, 45, True)
    performance_text = engine.properties_text("performance_text", f"[ Performance mode: {performance_mode} ]", "YELLOW", w, h + 240, 45, True)

    #create boxes that are invisable
    back_button = engine.properties_object("back_button", f"{file_dir}/textures/invisable_button.png", back_text.x, back_text.y, back_text.texture.get_width(), back_text.texture.get_height(), not performance_mode)
    volume_down_button = engine.properties_object("volume_down_button", f"{file_dir}/textures/invisable_button.png", volume_down_text.x, volume_down_text.y, volume_down_text.texture.get_width(), volume_down_text.texture.get_height(), not performance_mode)
    volume_up_button = engine.properties_object("volume_up_button", f"{file_dir}/textures/invisable_button.png", volume_up_text.x, volume_up_text.y, volume_up_text.texture.get_width(), volume_up_text.texture.get_height(), not performance_mode)
    performance_button = engine.properties_object("performance_button", f"{file_dir}/textures/invisable_button.png", performance_text.x, performance_text.y, performance_text.texture.get_width(), performance_text.texture.get_height(), not performance_mode)

    print(len(foreground))
    foreground += [back_button, volume_down_button, volume_up_button, performance_button]
    text_foreground += [back_text, music_text, volume_down_text, volume_up_text, performance_text]
    
def main_menu():            #pauses for 100ms to stop multiple clicks, main menu works by checking for mouse collisions with the invisable boxes created
    global display_sprite, foreground, text_foreground
    global run_game, run, volume, performance_mode, enable_vsync
    pygame.time.delay(100)
    if not pygame.mouse.get_pressed()[0]:
        pass
    #main start menu
    elif engine.mouse.collision("start", foreground):
        #delete everything the init main menu started and start the game
        engine.music.stop()
        delete_text()
        run_game = True
    elif engine.mouse.collision("options_button", foreground):
        #delete everything the init main menu started
        delete_text()
        init_options_menu()
    elif engine.mouse.collision("exit_button", foreground):
        run = False

    #options menu
    elif engine.mouse.collision("back_button", foreground):
        delete_text()
        init_main_menu()
    elif engine.mouse.collision("volume_down_button", foreground):
        if volume > 0:
            volume -= 1
        pygame.mixer.music.set_volume(volume / 10)
        delete_text()
        init_options_menu()
    elif engine.mouse.collision("volume_up_button", foreground):
        if volume < 10:
            volume += 1
        pygame.mixer.music.set_volume(volume / 10)
        delete_text()
        init_options_menu()    
    elif engine.mouse.collision("performance_button", foreground):
        #flip the variable performance_mode and reset the screen
        performance_mode = not performance_mode
        delete_text()
        init_options_menu()

        display_sprite = []
        reset_player()
        create_rocks()

#sub program -----------------------------------------------------------------------
def create_rocks():             #create a new set of rocks above the screen and then randomly select one to be deleted
    #spawn new enemy at the top of screen
    global display_sprite
    x = 10
    y = -90
    for index in range(1, 6):
        horizontal = randint(0, 1)
        vertical = randint(0, 0)
        
        rock = engine.properties_object(f"rock_{x}{y}", rock_texture, x, y, 80, 80, not performance_mode)
        #flip the background image
        rock.texture = pygame.transform.flip(rock.texture, horizontal, vertical)
        
        display_sprite.insert(index, (rock))
        x += 90

    del_rock = randint(1, 5)
    del display_sprite[del_rock]

def update(window, display, display_sprite, foreground, text_foreground, clock):                #update to the screen
    engine.window.update(window, display, display_sprite, foreground, text_foreground)
    
def reset_player():                 #resets the player
    global display_sprite, rocket
    rocket = engine.properties_object("rocket", f"{file_dir}/textures/spaceship.png", (w/2) - 51 / 2, 518, 45, 51, not performance_mode)
    display_sprite += [rocket]

def game_over():                #set a new high score, reset all variables, tell the player that they lost before sending them back to the main menu
    global display_sprite, text_foreground
    global run_game, score, high_score, frames_wait, sprite_speed
    if score > high_score:
        high_score = score
    #reset everything
    delete_text()
    display_sprite = []
    score, frames_wait, sprite_speed = 0, 145, 2
    reset_player()
    text_foreground[0].texture = engine.properties_text.reload_text(f"Score: {int(score)}    High score: {int(high_score)}", "YELLOW", 30)   #update the text_foreground

    #lost text
    lost = engine.properties_text("lost_text", "You lost!", "YELLOW", w, h, 100, True)
    text_foreground += [lost]
    update(window, display, display_sprite, foreground, text_foreground, clock)
    pygame.time.delay(1000)
    
    del text_foreground[1]
    #stop the game and update the screen to its default text

    run_game = False
    engine.music.fade_out(volume / 10, 0, 0.1)
    init_main_menu()
    update(window, display, display_sprite, foreground, text_foreground, clock)

def play_music():               #plays music depending if the code is in the main menu or in the main game
    if pygame.mixer.music.get_busy():
        pass
    else:
        if run_game == False:
            pygame.mixer.music.load(f"{file_dir}/music/menu_start.ogg")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.load(f"{file_dir}/music/gameplay.ogg")
            pygame.mixer.music.play(-1)

#main code --------------------------------------------------------------------------------
def gameplay():
    global display, display_sprite, text_foreground     #global lists used
    global wait, frames_wait, score, high_score, sprite_speed   #global variables used
    #player movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        engine.object.left(rocket, vel, 10)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        engine.object.right(rocket, vel, w - rocket.width - 10)

    #player animation
    engine.object.animate(rocket, playerAnimation, 10)
    
    #create scrolling background
    for image in display:
        image.y += 1
        if display[0].y == 0:
            x = 0
            y = -60
            for index in range(6):
                horizontal = randint(0, 1)
                vertical = randint(0, 0)
                
                background_stars = engine.properties_object("background_star", background_stars_texture, x, y, 80, 60, performance_mode)
                #flip the background image
                background_stars.texture = pygame.transform.flip(background_stars.texture, horizontal, vertical)
                
                display.insert(index, (background_stars))
                del display[66]
                x += 80   
    
    #create new rocks if the amount of frames passed == future frame time
    if engine.frames >= wait:
        create_rocks()
        wait = engine.frames + frames_wait
    
    #delete the rocks that hit y coord 700
    if display_sprite[len(display_sprite) - 1].y >= 700:
        del display_sprite[len(display_sprite) - 1]
        score += 0.25
        text_foreground[0].texture = engine.properties_text.reload_text(f"Score: {int(score)}    High score: {int(high_score)}", "YELLOW", 30)   #update the text_foreground

    #levels
    if score == 10:
        score += 5
        text_foreground[0].texture = engine.properties_text.reload_text(f"Score: {int(score)}    High score: {int(high_score)}", "YELLOW", 30)       #update the score
        #set new variables and configurations
        sprite_speed, frames_wait, = 4, 90
        level_text = engine.properties_text("level", "2X Speed!", "YELLOW", w, h, 100, True)
        text_foreground += [level_text]
        update(window, display, display_sprite, foreground, text_foreground, clock)
        pygame.time.delay(2000)
        del text_foreground[1]

    #move the rocks
    for index in range(1, len(display_sprite)):
        display_sprite[index].y += sprite_speed
    
    #check for collisions
    if engine.object.collision_mask(rocket, display_sprite) and enable_collisions:
        game_over()

    engine.counter.update()            #update the frames passed
    print(engine.frames)

#initilise the start of the program
reset_player()          
create_rocks()  
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

    if activate_music:          #play music if an audio driver has been detected
        play_music()
    if run_game:            #run game or main menu depending if the player is alive
        gameplay()
    else:
        main_menu() 
    
    update(window, display, display_sprite, foreground, text_foreground, clock)
    clock.tick(60)   
pygame.quit()