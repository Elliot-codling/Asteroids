# Mainscript which is where the game runs
import core as system
import random
from enum import Enum

# === Variables ===
performanceMode = False
global counter, score
counter = 0
score = 0

# Game state
class gameState(Enum):
    GAMEPLAYING = 0
    MAINMENU = 1

# Layers
class layer(Enum):
    ROCKS = 0
    PLAYER = 1
    BACKGROUND = 2

# Rocks
rockTex = system.loadImage("assets/textures/rock_brown.png")
rockSpeed = 2

# Player
playerSpeed = 6
player = system.spriteObject("player", "assets/textures/spaceship.png", system.vector2f(0, 0), system.vector2i(15 * 3, 17 * 3), not performanceMode, layer.PLAYER.value)

backgroundMusicTrack = [f"{system.directoryPath()}/assets/music/menu_start.ogg", f"{system.directoryPath()}/assets/music/gameplay.ogg"]
backgroundMusic = system.music(backgroundMusicTrack, 0)


# === Move rocks ===
def moveRocks(window: system.window, object: system.spriteObject):
    global score

    if object.getID() != "rock":
        return
    
    # TODO: Removing the rocks while in a for loop will skip the next rock and therefore it will skip an increment position
    if object.getPosition().y >= 600:
        score += 0.25
        window.popFromQueue(object)
        return
    
    object.incrementPosition(system.vector2f(0, rockSpeed))
    

# === Scroll background ===
def scrollBackgroundObject(object: system.spriteObject):
    if object.getID() != "bg":
        return
    
    if object.getPosition().y >= 600:
        object.setPosition(system.vector2f(object.getPosition().x, -object.getSize().y))

    object.incrementPosition(system.vector2f(0, 1))

# === Player movement ===
def playerMovement(window: system.window):
    # Move the player
    if (window.getKey("a") or window.getKey("LEFT")) and player.leftBorder(player.getPosition(), 0):
        player.incrementPosition(system.vector2f(-playerSpeed, 0))

    if (window.getKey("d") or window.getKey("RIGHT")) and player.rightBorder(player.getPosition() + player.getSize(), 480):
        player.incrementPosition(system.vector2f(playerSpeed, 0))

    # Move the play back a little so that the sprite does not go off the screen
    if not player.leftBorder(player.getPosition(), 0):
        player.setPosition(system.vector2f(0, player.getPosition().y))
    if not player.rightBorder(player.getPosition() + player.getSize(), 480):
        player.setPosition(system.vector2f(480 - player.getSize().x, player.getPosition().y))


# === Create rocks ===
def createRocks(window: system.window):
    # Randomly select an index of which rock will not be spawned
    indexToContinue = random.randint(0, 4)
    # Iterate 5 times, however one of the interations will not create a rock
    for x in range(0, 5):
        if x == indexToContinue:
            continue
        
        # Create rock and add to queue
        rock = system.spriteObject("rock", rockTex, system.vector2f((x * 95) + 10, -80), system.vector2i(80, 80), not performanceMode, layer.ROCKS.value)
        window.pushToQueue(rock)






# === Main runtime events ===

# Runs only once
def start(window: system.window) -> None:
    #window.setTargetFramerate(60)
    
    # Create background
    backgroundStarTex = system.loadImage("assets/textures/background-stars.png")

    for y in range(11):
        for x in range(8):
            angle = random.choice([0, 90, 180, 270])

            backgroundStar = system.spriteObject("bg", backgroundStarTex, system.vector2f(x * 60, y * 60), system.vector2i(60, 60), False, layer.BACKGROUND.value)
            backgroundStar.setAngle(angle)
            window.pushToQueue(backgroundStar)
    
    # Player
    player.setPosition(system.vector2f((480 / 2) - (player.getSize().x / 2), 500))
    window.pushToQueue(player)

# Runs every frame
def update(window: system.window) -> None:
    window.renderObjects()

# Runs at 60fps (16.666... ms)
def fixedUpdate(window: system.window, deltaTime: float) -> None:
    global counter
    window.updateEvents()

    # End the program
    if window.getEvent("QUIT") or window.getKey("ESCAPE"):
        window.stopRunning()

    # Move player
    playerMovement(window)

    # Music
    backgroundMusic.playLoop()

    # Scroll background and move the rocks down
    queue = window.getQueue()
    for object in queue[:]:
        scrollBackgroundObject(object)
        moveRocks(window, object)

    # Create new rocks every 145 frames
    if counter % 145 == 0:
        createRocks(window)
        counter = 0
    counter += 1
    
    # Check if the player rect box lies within a rock
    collidedRock = player.collideBoxByID(window.getQueue(), "rock")
    hitRock = False
    if collidedRock != None:
        hitRock = player.collideMaskByObject(collidedRock)

    if hitRock:
        system.printDebugInfo(f"Game over, score: {score}")

    if window.getEvent("KEYDOWN") and window.getKey("f"):
        system.printDebugInfo(window.getFramerate())

   
# Runs once at the end
def end() -> None:
    pass

