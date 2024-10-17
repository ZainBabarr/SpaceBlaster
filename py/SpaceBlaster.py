import math
import time
import pygame
from enemy import Enemy
from greenEnemy import GreenEnemy
from bullet import Bullet
from player import Player
from gamePlatform import Platform

# Setting up game
pygame.init()

# Setting up window
windowWidth = 450
windowHeight = 600

dis = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Space Blaster")

# Setting up game
clock = pygame.time.Clock()
gameSpeed = 100
running = True

screen = "home"
delay = 1.1
levelStarted = True
level = 0
enemies = []
greenEnemies = []
bullets = []
platforms = []
gameStartTime = 0  # Time when the game starts
gameStarted = False  # Flag to check if the game has just started
tries = 1

# Colors
brown = (196, 179, 149)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
gray = (224, 224, 224)

# Initialize player
charX = windowWidth / 2 - 30
charY = 520
charImage = pygame.image.load("images/jet.png").convert_alpha()
charImage = pygame.transform.scale(charImage, (70, 70))
bulletImage = pygame.image.load("images/bullet.png").convert_alpha()
bulletImage = pygame.transform.scale(bulletImage, (35, 45))

player = Player(charX, charY, charImage, bulletImage, dis, windowWidth, delay)

# Images
background = pygame.image.load("images/background.png").convert_alpha()
logo = pygame.image.load("images/logo.png").convert_alpha()
logo = pygame.transform.scale(logo, (350, 300))
count = pygame.image.load("images/bullet count.png").convert_alpha()
count = pygame.transform.scale(count, (80, 50))
countLevel = pygame.image.load("images/bullet count.png").convert_alpha()
countLevel = pygame.transform.scale(countLevel, (140, 50))
blueEnemyImg = pygame.image.load("images/blue enemy.png").convert_alpha()
blueEnemyImg = pygame.transform.scale(blueEnemyImg, (55, 55))
greenEnemyImg = pygame.image.load("images/green enemy.png").convert_alpha()  # Corrected the image name
greenEnemyImg = pygame.transform.scale(greenEnemyImg, (55, 55))
platform_image = pygame.image.load("images/platform.png").convert_alpha()
platform_image = pygame.transform.scale(platform_image, (90, 45))

# Music + SFX
winSound = pygame.mixer.Sound("sound/win.wav")
loseSound = pygame.mixer.Sound("sound/lose.wav")
killSound = pygame.mixer.Sound("sound/kill.mp3")
killSound.set_volume(0.09)
barrierSound = pygame.mixer.Sound("sound/bonk.wav")
barrierSound.set_volume(0.7)

# Fonts
font = pygame.font.Font('fonts/font.otf', 200)
smallFont = pygame.font.Font('fonts/font.otf', 45)
pixelFont = pygame.font.Font('fonts/Minecraft.ttf', 30)
pressToPlay = pixelFont.render("[Space To Play]", True, white)

# Start button position
startY = 210

# Start Display
def startPage():
    global startY, pressToPlay, screen

    dis.blit(background, (0, 0))
    dis.blit(logo, (55, 100))
    dis.blit(pressToPlay, (114, startY+150))

    # Move the text
    startY = 210 + (math.sin(time.time() * 5) * 5)


# Game page
def gamePage():
    global level, levelStarted, enemies, bullets, gameStartTime, gameStarted, platforms, greenEnemies, screen, tries

    dis.blit(background, (0, 0))

    if not gameStarted:
        gameStartTime = pygame.time.get_ticks()
        gameStarted = True

    if level == 0:
        levelZero()
    elif level == 1:
        levelOne()
    elif level == 2:
        levelTwo()
    elif level == 3:
        levelThree()
    elif level == 4:
        levelFour()
    elif level == 5:
        levelFive()
    elif level == 6:
        levelSix()
    elif level == 7:
        levelSeven()
    elif level == 8:
        levelEight()
    elif level == 9:
        levelNine()
    elif level == 10:
        screen = "end"

    # Draw player
    player.draw()

    # Draw bullet count
    bulletCountDisplay = smallFont.render(str(player.bullet_count), True, black)
    dis.blit(count, (10, 10))
    dis.blit(bulletImage, (10, 12))
    dis.blit(bulletCountDisplay, (53, 11))

    # Draw level count
    levelDisplay = smallFont.render(str(level), True, black)
    dis.blit(countLevel, (300, 10))
    dis.blit(levelDisplay, (410, 10))
    dis.blit(smallFont.render("Level", True, black), (310, 10))

    # User controls (left, right, and space for firing bullets)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_left()
    elif keys[pygame.K_d]:
        player.move_right()
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - gameStartTime > 500:
        player.fire_bullet(bullets)

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()

        if bullet.is_off_screen():
            bullets.remove(bullet)

            # Check if player has no bullets left and there are still enemies
            if player.bullet_count == 0 and enemies:
                loseSound.play()
                tries += 1
                resetLevel()
                return
        else:
            for enemy in enemies[:]:
                if bullet.check_enemy_collision(enemy):
                    if isinstance(enemy, GreenEnemy):
                        loseSound.play()
                        tries += 1
                        resetLevel()  # Reset the level if a green enemy is hit
                        return
                    enemies.remove(enemy)
                    killSound.play()
                    bullets.remove(bullet)  # Remove the bullet if it hits an enemy

                    if player.bullet_count == 0 and enemies:
                        loseSound.play()
                        tries += 1
                        resetLevel()
                        return
                    break

            for greenEnemy in greenEnemies[:]:
                if bullet.check_enemy_collision(greenEnemy):
                    loseSound.play()
                    tries += 1
                    resetLevel()
                    return
            for platform in platforms[:]:
                if bullet.check_platform_collision(platform):
                    barrierSound.play()
                    bullet.setDirection(-bullet.direction)
                    break  # Break the platform collision checking loop after a hit

    # Draw enemies and platforms
    for enemy in enemies[:]:
        enemy.draw(dis)

    for greenEnemy in greenEnemies[:]:
        greenEnemy.draw(dis)

    for platform in platforms[:]:
        platform.draw(dis)
    
    # Update the display
    pygame.display.update()


# LEVELS
def levelZero():
    global levelStarted, level, enemies

    # Start Level
    if levelStarted:
        player.bullet_count = 1
        enemies = [Enemy(200, 80, blueEnemyImg)]
        levelStarted = False

    for enemy in enemies:
        enemy.update_position()

    if not enemies:
        resetLevel()
        winSound.play()
        level += 1

def levelOne():
    global levelStarted, level, enemies

    if levelStarted:
        player.bullet_count = 2
        enemies = [Enemy(100, 80, blueEnemyImg), Enemy(300, 80, blueEnemyImg)]
        levelStarted = False

    for enemy in enemies:
        enemy.update_position()

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelTwo():
    global levelStarted, level, enemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 1
        enemies = [Enemy(200, 80, blueEnemyImg)]
        platforms = [Platform(220, 140, platform_image)]
        levelStarted = False

    for platform in platforms:
        platform.moveSideways(windowWidth, 3, 40)

    for enemy in enemies:
        enemy.update_position()

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelThree():
    global levelStarted, level, enemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 1
        enemies = [Enemy(203, 410, blueEnemyImg)]
        platforms = [Platform(185, 80, platform_image), Platform(185, 450, platform_image)]
        levelStarted = False

    platforms[1].moveSideways(windowWidth, 1.5, 41)

    for enemy in enemies:
        enemy.move_sideways(windowWidth, 1.5, 58)

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelFour():
    global levelStarted, level, enemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 2
        enemies = [Enemy(100, 100, blueEnemyImg), Enemy(300, 100, blueEnemyImg)]
        platforms = [Platform(100, 200, platform_image), Platform(250, 400, platform_image)]
        levelStarted = False

    platforms[0].moveSideways(windowWidth, 2, 60)
    platforms[1].moveSideways(windowWidth, 0.3, 60)

    for enemy in enemies:
        enemy.move_sideways(windowWidth, 2, 40)
        enemy.update_position()

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelFive():
    global levelStarted, level, enemies, platforms, greenEnemies, platform_image

    if levelStarted:
        player.bullet_count = 1
        enemies = [Enemy(200, 100, blueEnemyImg)]
        greenEnemies = [GreenEnemy(200, 200, greenEnemyImg)]
        levelStarted = False

    for greenEnemy in greenEnemies:
        greenEnemy.move_sideways(windowWidth, 1.5, 80)

    for enemy in enemies:
        enemy.update_position()

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelSix():
    global levelStarted, level, enemies, greenEnemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 2
        enemies = [Enemy(200, 260, blueEnemyImg), Enemy(300, 90, blueEnemyImg)]
        greenEnemies = [GreenEnemy(100, 350, greenEnemyImg), GreenEnemy(300, 170, greenEnemyImg)]
        levelStarted = False

    for enemy in enemies:
        enemy.move_sideways(windowWidth, 1.2, 80)
        enemy.update_position()
        
    
    for greenEnemy in greenEnemies:
        greenEnemy.move_sideways(windowWidth, 2.0, 80)
        greenEnemy.update_position()

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelSeven():
    global levelStarted, level, enemies, platforms, greenEnemies, platform_image

    if levelStarted:
        player.bullet_count = 2
        enemies = [Enemy(100, 70, blueEnemyImg), Enemy(300, 70, blueEnemyImg)]
        greenEnemies = [GreenEnemy(100, 350, greenEnemyImg)]
        platforms = [Platform(80, 100, platform_image), Platform(280, 100, platform_image)]
        levelStarted = False

    for enemy in enemies:
        
        enemy.update_position()

    for greenEnemy in greenEnemies:
        greenEnemy.move_sideways(windowWidth, 2.5, 80)
        greenEnemy.update_position()

    platforms[0].moveVertically(windowWidth, 1.5, 100)
    platforms[1].moveVertically(windowWidth, 1.5, 100)

    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelEight():
    global levelStarted, level, enemies, greenEnemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 2
        enemies = [
            Enemy(150, 100, blueEnemyImg),
            Enemy(300, 400, blueEnemyImg)
        ]
        greenEnemies = [
            GreenEnemy(200, 200, greenEnemyImg),
            GreenEnemy(200, 400, greenEnemyImg)
        ]
        platforms = [
            Platform(0, 450, platform_image),
            Platform(360, 450, platform_image)
        ]
        levelStarted = False

    for enemy in enemies:
        if enemy.y < 300:
            enemy.move_sideways(windowWidth, 2, 0)  # Top enemies move slower
        else:
            enemy.move_sideways(windowWidth, 3, 70)  # Bottom enemies move faster
        enemy.update_position()

    for greenEnemy in greenEnemies:
        if greenEnemy.y < 300:
            greenEnemy.move_sideways(windowWidth, 1.2, 80)  # Top green enemies move slower
        else:
            greenEnemy.move_sideways(windowWidth, 2.5, 100)  # Bottom green enemies move faster
        greenEnemy.update_position()

    platforms[0].moveVertically(windowHeight, 2, 80)
    platforms[1].moveVertically(windowHeight, 1.5, 100)

    # Check if all enemies are defeated to reset level
    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

def levelNine():
    global levelStarted, level, enemies, greenEnemies, platforms, platform_image

    if levelStarted:
        player.bullet_count = 4
        enemies = [
            Enemy(150, 100, blueEnemyImg),
            Enemy(250, 100, blueEnemyImg),
            Enemy(100, 400, blueEnemyImg)
        ]
        greenEnemies = [
            GreenEnemy(200, 250, greenEnemyImg),
            GreenEnemy(200, 450, greenEnemyImg)
        ]
        platforms = [
            Platform(100, 150, platform_image),
            Platform(150, 350, platform_image)
        ]
        levelStarted = False

    for enemy in enemies:
        if enemy.y < 300:
            enemy.move_sideways(windowWidth, 2, 80)  # Top enemies move slower
        else:
            enemy.move_sideways(windowWidth, 2, 60)  # Bottom enemies move faster
        enemy.update_position()

    for greenEnemy in greenEnemies:
        if greenEnemy.y < 300:
            greenEnemy.move_sideways(windowWidth, 1, 100)  # Top green enemies move slower
        else:
            greenEnemy.move_sideways(windowWidth, 2, 80)  # Bottom green enemies move faster
        greenEnemy.update_position()

    platforms[0].moveSideways(windowWidth, 3.5, 0)
    platforms[1].moveSideways(windowWidth, 1.5, 100)

    # Check if all enemies are defeated to reset level
    if not enemies:
        winSound.play()
        resetLevel()
        level += 1

# Reset the level
def resetLevel():
    global levelStarted, enemies, greenEnemies, bullets, platforms
    levelStarted = True
    enemies = []
    greenEnemies = []
    bullets = []
    platforms = []

def endPage():
    global Tries, Congratulations, startY
    Congratulations = smallFont.render("You Finished the Game!", True, white)
    Tries = smallFont.render("Attempts: " + str(tries), True, white)

    # Buttons
    dis.blit(Tries, (135, startY+300))
    dis.blit(Congratulations, (40, startY+250))

    # Move the text
    startY = (math.sin(time.time() * 5) * 5)

# Main loop
while running:
    global endStartTime

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and screen == "home":
            screen = "game"
            winSound.play()

    # Check the current screen state
    if screen == "home":
        startPage()

    # Check if the game has started
    if screen == "game":
        gamePage()

    # Check if the game has ended
    if screen == "end":
        dis.blit(background, (0,0))
        endPage()

    pygame.display.update()
    clock.tick(gameSpeed)

pygame.quit()

