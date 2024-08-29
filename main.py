import pygame
import math
import random
from pygame import mixer


## Initialize the pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # creating a game display of size 800 pixels x 600 pixels

##Background
background = pygame.image.load("background.png")
mixer.music.load("background.wav")
mixer.music.play(-1)

##Game Display
pygame.display.set_caption("SpaceInvader2")
icon = pygame.image.load("spaceship (1).png")
pygame.display.set_icon(icon)

##Player
playerImg = pygame.image.load("player.png")
# Coordinates of the player on the screen
playerX = 365  # horizontal coordinate
playerY = 520  # vertical coordinate
playerX_change = 0

##Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6  # Say there are 6 enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ufo.png"))
    # Coordinates of the player on the screen
    enemyX.append(random.randint(0, 735))  # horizontal coordinate
    enemyY.append(random.randint(50, 150))  # vertical coordinate
    enemyX_change.append(0.3)
    enemyY_change.append(40)

##Bullet
bulletImg = pygame.image.load("bullet (1).png")
# Coordinates of the player on the screen
bulletX = 0  # horizontal coordinate
bulletY = 480  # vertical coordinate
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"  # Ready state: no bullet fired, not visible; "fire": bullet fired, visible on screen

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)
textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("ZunScore: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit means to draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


##Player Dynamics


##Game Window
# the game window needs to keep open until closed
running = True  # using variable "running" to keep the window open
while running:
    # set color of the screen (RGB)
    screen.fill((0, 0, 0))  # choose any color by changing the values of RGB
    # background image
    screen.blit(background, (0, 0))
    # creating an event(keyboard/mouse press) in pygame
    for event in pygame.event.get():
        # pygame.quite implies cross is clicked, which changes running into False and the while loop breaks
        if event.type == pygame.QUIT:
            running = False

        # Keystroke right or left or not pressed
        if event.type == pygame.KEYDOWN:
            # print("A keystroke is pressed")
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                # print("Right arrow is pressed")
                playerX_change = +0.1
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("shoot.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # KEYUP means key released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystroke has been released")
                playerX_change = 0
    # Limiting boundaries for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movements
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                playerY = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0, 735)  # horizontal coordinate
            enemyY[i] = random.randint(50, 150)  # vertical coordinate
        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        # print(score)
        enemyX[i] = random.randint(0, 735)  # horizontal coordinate
        enemyY[i] = random.randint(50, 150)  # vertical coordinate

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # updating display every loop
