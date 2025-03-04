#main asteroids game
#v1.2, running on PiEngine 8.1
import PiEngine as engine
import pygame
from random import randint

#variables
file_dir = engine.directory()
clock = pygame.time.Clock()
counter = engine.counter()
vel = 6
rockSpeed = 2
score = 0
high_score = 0
volume = 10
runGame = False
enable_vsync = True
performance_mode = False
display = []
frames_wait = 145
wait = counter.frames + frames_wait

w, h = 480, 600
window = engine.window("Asteroids", w, h, (0, 0, 0), pygame.SCALED, enable_vsync)
#0 -> Background stars
#1 -> player
#2 -> Invisable buttons
#3 -> text
#4 -> rocks
def initPlayer():
    global player
    player = engine.properties_object("player", f"{file_dir}/textures/spaceship.png", (w/2) - 51 / 2, 518, 45, 51, not performance_mode, 1)

initPlayer()
display += [player]
#preloaded textures
backgroundStarTexture = pygame.image.load(f"{file_dir}/textures/background-stars.png")
rockTexture = pygame.image.load(f"{file_dir}/textures/rock_brown.png")
#spaceship animation
playerAnimation = [pygame.image.load(f"{file_dir}/textures/spaceship.png"), pygame.image.load(f"{file_dir}/textures/spaceship_3.png"), pygame.image.load(f"{file_dir}/textures/spaceship_2.png")]

#sub routines ----------------------------------------------------------------------
#create background
x = 0
y = -60
for _ in range(11):
    for _ in range(8):
        horizontal = randint(0, 1)
        vertical = randint(0, 1)

        background_stars = engine.properties_object("backgroundStar", backgroundStarTexture, x, y, 60, 60, False)
        rotatedTexture = pygame.transform.flip(background_stars.texture, horizontal, vertical)
        background_stars.reload_texture(rotatedTexture, rotatedTexture.get_width(), rotatedTexture.get_height())

        display += [background_stars]
        x += 60
    y += 60
    x = 0

#create rocks
def create_rocks():
    global display
    x = 10
    y = -80
    deletedRock = randint(1, 5)
    for index in range(1, 6):
        if index == deletedRock:
            x += 90
            continue
        horizontal = randint(0, 1)
        vertical = randint(0, 1)

        rock = engine.properties_object("asteroid", rockTexture, x, y, 80, 80, not performance_mode, 4)
        rotatedTexture = pygame.transform.flip(rock.texture, horizontal, vertical)
        rock.reload_texture(rotatedTexture, rotatedTexture.get_width(), rotatedTexture.get_height(), not performance_mode)

        display += [rock]
        x += 90

def update(display):
    window.update(display)

def deleteText():
    global display
    display = window.delete_layer(display, 3)

def initMainMenu():
    global display, performance_mode
    start_text = engine.properties_text("start", "[ Start Game ]", "YELLOW", w, h, 45, True, 3)
    options_text = engine.properties_text("option", "[ Options ]", "YELLOW", w, h + 80, 45, True, 3)
    exit_text = engine.properties_text("exit", "[ Exit Game ]", "YELLOW", w, h + 160, 45, True, 3)
    #create boxes that are invisable
    start_button = engine.properties_object("start_button", f"{file_dir}/textures/invisable_button.png", start_text.x, start_text.y, start_text.texture.get_width(), start_text.texture.get_height(), not performance_mode, 2)
    options_button = engine.properties_object("options_button", f"{file_dir}/textures/invisable_button.png", options_text.x, options_text.y, options_text.texture.get_width(), options_text.texture.get_height(), not performance_mode, 2)
    exit_button = engine.properties_object("exit_button", f"{file_dir}/textures/invisable_button.png", exit_text.x, exit_text.y, exit_text.texture.get_width(), exit_text.texture.get_height(), not performance_mode, 2)
    
    display += [start_button, options_button, exit_button, start_text, options_text, exit_text]

def initOptionsMenu():
    global display, performance_mode
    back_text = engine.properties_text("back", "[ Back ]", "YELLOW", w, h, 45, True, 3)
    music_text = engine.properties_text("music", f"[ Music  level: {volume} ]", "YELLOW", w, h + 80, 45, True, 3)
    volume_down_text = engine.properties_text("volDown", "[ - ]", "YELLOW", w - 60, h + 160, 45, True, 3)
    volume_up_text = engine.properties_text("volUp", "[ + ]", "YELLOW", w + 60, h + 160, 45, True, 3)
    performance_text = engine.properties_text("performance_text", f"[ Performance mode: {performance_mode} ]", "YELLOW", w, h + 240, 45, True, 3)

    #create boxes that are invisable
    back_button = engine.properties_object("back_button", f"{file_dir}/textures/invisable_button.png", back_text.x, back_text.y, back_text.texture.get_width(), back_text.texture.get_height(), not performance_mode, 2)
    volume_down_button = engine.properties_object("volume_down_button", f"{file_dir}/textures/invisable_button.png", volume_down_text.x, volume_down_text.y, volume_down_text.texture.get_width(), volume_down_text.texture.get_height(), not performance_mode, 2)
    volume_up_button = engine.properties_object("volume_up_button", f"{file_dir}/textures/invisable_button.png", volume_up_text.x, volume_up_text.y, volume_up_text.texture.get_width(), volume_up_text.texture.get_height(), not performance_mode, 2)
    performance_button = engine.properties_object("performance_button", f"{file_dir}/textures/invisable_button.png", performance_text.x, performance_text.y, performance_text.texture.get_width(), performance_text.texture.get_height(), not performance_mode, 2)

    display += [back_text, music_text, volume_down_text, volume_up_text, performance_text]
    display += [back_button, volume_down_button, volume_up_button, performance_button]

def mainMenu():
    global runGame, volume, performance_mode, display
    pygame.time.delay(100)
    if not pygame.mouse.get_pressed()[0]:
        pass
    #main start menu
    elif engine.mouse.collision("start_button", display):
        #delete everything the init main menu started and start the game
        #engine.music.stop()
        deleteText()
        display = window.delete_layer(display, 2)
        runGame = True
    elif engine.mouse.collision("options_button", display):
        #delete everything the init main menu started
        deleteText()
        display = window.delete_layer(display, 2)
        initOptionsMenu()
    elif engine.mouse.collision("exit_button", display):
        display = window.setRunStatus(False)

    #options menu
    elif engine.mouse.collision("back_button", display):
        deleteText()
        display = window.delete_layer(display, 2)
        initMainMenu()
        
    elif engine.mouse.collision("volume_down_button", display):
        if volume > 0:
            volume -= 1
        pygame.mixer.music.set_volume(volume / 10)
        deleteText()
        initOptionsMenu()

    elif engine.mouse.collision("volume_up_button", display):
        if volume < 10:
            volume += 1
        pygame.mixer.music.set_volume(volume / 10)
        deleteText()
        initOptionsMenu() 

    elif engine.mouse.collision("performance_button", display):
        #flip the variable performance_mode and reset the screen
        performance_mode = not performance_mode
        deleteText()
        display = window.delete_layer(display, 2)
        display = window.delete_layer(display, 1)
        initPlayer()
        display += [player]
        initOptionsMenu()

def gameOver():
    global score, high_score, frames_wait, rockSpeed, display, runGame
    if score > high_score:
        high_score = score
    deleteText()
    display = window.delete_layer(display, 4)
    score, frames_wait, rockSpeed = 0, 145, 2

    lost = engine.properties_text("lostText", "You Lost!", "YELLOW", w, h, 100, True, 3)
    display += [lost]
    update(display)
    pygame.time.delay(1000)

    display.remove(lost)
    runGame = False

    initMainMenu()
    update(display)



def gameplay(events, keys):
    global display, wait, score
    #player movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.left(vel, 10)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.right(vel, w - player.width - 10)

    #player animation
    engine.object.animate(player, playerAnimation, 10, counter, 0, 0, not performance_mode)
    counter.update()

    #scrolling background and move rocks
    for item in display:
        if item.layer != 0:
            pass
        else:
            item.y += 1
            if item.y >= h:
                item.y = -60

        if item.layer == 4:
            item.y += rockSpeed
            if item.y >= 700:
                engine.appendForDeletion(item)
                score += 0.25

    #delete rocks that require to be deleted
    display = engine.deleteItems(display)
        
    #create new rocks
    if counter.frames >= wait:
        create_rocks()
        wait = counter.frames + frames_wait

    if player.collision_mask(display, [4]):
        gameOver()

    
initMainMenu()
while window.isRunning():
    events, keys = engine.event.update(window)
    if keys[pygame.K_ESCAPE]:
        window.setRunStatus(False)
    
    clock.tick(60)
    if runGame:
        gameplay(events, keys)
    else:
        mainMenu()

    update(display)
pygame.quit()