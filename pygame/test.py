# Game derived from tutorial template at https://realpython.com/pygame-a-primer/

# import the pygame module
import pygame

# import random for random numbers!
import random

# import pygame.locals for easier access to key coordinates
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
SKY = 400
JUMP_APEX = 50
CLOCK_TICK = 500
ENEMY_INTERVAL = 40
ENEMY_WIDTH = 20

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('jet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(bottom = SKY, left = 0)
        self.velocity = 0
    
    def update(self):
        self.rect.move_ip(0, self.velocity * -1)
        if self.rect.bottom <= SKY - JUMP_APEX:
            self.velocity = -1
        elif self.rect.bottom >= SKY:
            self.velocity = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(bottom = SKY, left = WIDTH)
        self.speed = 2

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# class Cloud(pygame.sprite.Sprite):
    # def __init__(self):
        # super(Cloud, self).__init__()
        # self.image = pygame.image.load('cloud.png').convert()
        # self.image.set_colorkey((0, 0, 0), RLEACCEL)
        # self.rect = self.image.get_rect(center=(
            # random.randint(820, 900), random.randint(0, HEIGHT))
        # )

    # def update(self):
        # self.rect.move_ip(-5, 0)
        # if self.rect.right < 0:
            # self.kill()

# initialize pygame
pygame.init()

# create the screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a custom event for adding a new enemy.
# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
# ADDCLOUD = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDCLOUD, 1000)

# create our 'player', right now he's just a rectangle
player = Player()

background_sky = pygame.Surface((WIDTH, SKY))
background_sky.fill((0,0,255))

background_ground = pygame.Surface((WIDTH, HEIGHT - SKY))
background_ground.fill((100,0,100))

enemies = pygame.sprite.Group()
#clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
time = 0
def playGame():
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE and player.rect.bottom == SKY:
                player.velocity = 1
        elif event.type == QUIT:
            running = False
        # elif event.type == ADDENEMY:
            # new_enemy = Enemy()
            # enemies.add(new_enemy)
            # all_sprites.add(new_enemy)
        # elif event.type == ADDCLOUD:
            # new_cloud = Cloud()
            # all_sprites.add(new_cloud)
            # clouds.add(new_cloud)
    time += 1
    if not time % (CLOCK_TICK * ENEMY_INTERVAL * ENEMY_WIDTH):
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
    if not time % CLOCK_TICK:
        screen.blit(background_sky, (0, 0))
        screen.blit(background_ground, (0, SKY))
#    pressed_keys = pygame.key.get_pressed()
        player.update()
        enemies.update()
#        clouds.update()
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()

        pygame.display.flip()