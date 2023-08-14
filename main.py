import pygame
import random
import math
from pygame import  mixer


#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))
RED =(255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

# Variables


# Title and Icons
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.jfif')
pygame.display.set_icon(icon)
#Back ground
background = pygame.image.load('background1.jfif')
background = pygame.transform.scale(background,(800,600))
#Background Sound
mixer.music.load('background.wav')
#mixer.music.play(-1)#-1 for play continously
#if you remove -1 it will play 


#Player
playerImg = pygame.image.load('player3.png')
playerX=370
playerY = 480
playerX_change=0
pv=5

#Enemy
S=28
enemyImg_original= pygame.image.load('enemy3.png')
enemyImg_original = pygame.transform.scale(enemyImg_original,(S,S))
enemyX= []
enemyY_change=[]
enemyX_change=[]
enemyY =[]
enemyImg =[]
num_of_enemies = 6
evx=1
evy=20
for i in range(num_of_enemies):
    enemyImg.append(enemyImg_original)
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyY_change.append(evy)
    enemyX_change.append(evx)


#Bullet
#ready = you can't see the bullet on the screen
#Fire - The bullet is currently moving
S=28
bulletImg = pygame.image. load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg,(S,S))
bulletX=0
bulletY = 480
bvx=1
bvy=10
bulletY_change=bvy
bulletX_change=bvx
bullet_state ="ready"

#Score
score_value =0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game over text
over_font = pygame.font.Font('freesansbold.ttf',256)

def draw_border():
    pygame.draw.line(screen,BLUE,(0,480),(800,480),1)


def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

    
def game_over_text():
    over_text = font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(300,250))
    
    
def player(x,y):
    if x<0:
        x=0
    if x >736:
        x=736
    screen.blit(playerImg,(x,y))
    
    
def enemy(x,y):
    if x<0:
        x=0
    elif x >736:
        x=736
    screen.blit(enemyImg[1],(x,y))
    
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y-26))
    
    
#collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2))+(math.pow((enemyY-bulletY),2)))
    if distance <27:
        return True
    else :return False
                         

#Game loop
running = True

while running :
    screen.fill(WHITE)
    
    screen.blit(background,(0,0))
    draw_border()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
         
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == pygame.K_LEFT:
             #   print("left")
                playerX_change = -pv
            if event.key == pygame.K_RIGHT:
              #  print("Right")
                playerX_change = pv
                
            if event.key == pygame.K_SPACE:
                bulletY = 480
                bullet_state = "ready"
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX                    
                    fire_bullet(bulletX,bulletY)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               # print("keystrokes has been released")
                playerX_change = 0
    #bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change

        

    #Enemy Movement
    for i in range(num_of_enemies):
        #Game over
        if enemyY[i]>480:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        
        if enemyX[i] <+0:
            enemyX_change[i] = evx
            enemyY [i] += enemyY_change[i]
        elif enemyX[i] >+750:
            enemyX_change[i] =-evx
            enemyY[i] += enemyY_change[i]
        
        
        enemyX[i] += enemyX_change[i]   
        enemy(enemyX[i],enemyY[i])
            
    
    #Collision 
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state="ready"
            collision =False
            score_value +=1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
    
    
    playerX += playerX_change        
    player(playerX,playerY)
    show_score(textX,textY)
    
    pygame.display.update()
    
pygame.quit()