import pygame
import random

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT
)


pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
GRAVITY = 1
PLAYER_SPEED = 4


JUMP_STRENGTH = -20

GROUND_HEIGHT = 25
GROUND_WIDTH = SCREEN_WIDTH * 7
ground_rect = pygame.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), GROUND_WIDTH, GROUND_HEIGHT)

movement_on_x = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Bounce game") 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.image = pygame.Surface((25, 75))
        self.image.fill((0, 0, 255)) 
        self.rect = self.image.get_rect()

        self.rect.x = (SCREEN_WIDTH // 2) - (25 // 2) 
        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 75

        self.change_in_x = 0
        self.change_in_y = 0
        self.on_the_ground = False

    
    def gravity_force(self):
        self.change_in_y += GRAVITY
    
    def jump(self):
        if self.on_the_ground:
            self.change_in_y = JUMP_STRENGTH
            self.on_the_ground = False

    

    def update(self, platforms_group):
        global movement_on_x
        
        self.gravity_force()

        self.rect.y += self.change_in_y

        if self.change_in_x > 0 and self.rect.right > SCREEN_WIDTH - 200:
            movement_on_x -= self.change_in_x
        elif self.change_in_x < 0 and self.rect.left < 200:
            movement_on_x -= self.change_in_x
        else:
            self.rect.x += self.change_in_x

        


        if self.rect.left < 0:
            self.rect.left = 0
            self.change_in_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.change_in_x = 0


        self.on_the_ground = False

        if self.rect.colliderect(ground_rect):
            if self.change_in_y > 0:

                self.rect.bottom = ground_rect.top
                self.change_in_y = 0
                self.on_the_ground = True


        on_the_platform_list = pygame.sprite.spritecollide(self, platforms_group, False)

        for platform in on_the_platform_list:

            if self.change_in_y > 0 and self.rect.bottom <= platform.rect.bottom :
                self.rect.bottom = platform.rect.top
                self.change_in_y = 0
                self.on_the_ground = True





    def left_movement(self):
        self.change_in_x = -PLAYER_SPEED

    def right_movement(self):
        self.change_in_x = PLAYER_SPEED

    def stop_movement(self):
        self.change_in_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):

        super(Platform, self). __init__()

        self.image = pygame.Surface((width, height))
        self.image.fill((150, 75, 0)) 

        self.rect = self.image.get_rect()

        self.rect.x = x 

        self.rect.y = y 

        self.start_x = x

    def update(self, movement_on_x):

        self.rect.x = self.start_x + movement_on_x


        
all_sprites = pygame.sprite.Group()

platforms = pygame.sprite.Group()

platform1 = Platform(100, SCREEN_HEIGHT - 100, 150, 20) 
platform2 = Platform(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 200, 200, 20) 
platform3 = Platform(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 300, 150, 20) 
platform4 = Platform(50, SCREEN_HEIGHT - 400, 100, 20)
platform5 = Platform(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 450, 100, 20)
platform6 = Platform(SCREEN_WIDTH + 100, SCREEN_HEIGHT - 150, 150, 20) 
platform7 = Platform(SCREEN_WIDTH + 300, SCREEN_HEIGHT - 250, 100, 20) 
platform8 = Platform(SCREEN_WIDTH + 500, SCREEN_HEIGHT - 350, 180, 20) 

platforms.add(platform1)
platforms.add(platform2)
platforms.add(platform3)
platforms.add(platform4)
platforms.add(platform5)
platforms.add(platform6)
platforms.add(platform7)
platforms.add(platform8)

for platform in platforms:
    all_sprites.add(platform)

player = Player()
all_sprites.add(player)

ground_start_x = ground_rect.x


clock = pygame.time.Clock()
FPS = 60






running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_LEFT:
                player.left_movement()

            elif event.key == K_RIGHT:
                player.right_movement()

            elif event.key == K_UP:
                player.jump()

        elif event.type == KEYUP:
            if event.key == K_LEFT and player.change_in_x < 0:
                player.stop_movement()
            elif event.key == K_RIGHT and player.change_in_x > 0:
                player.stop_movement()


        


    player.update(platforms)

    for platform in platforms:
        platform.update(movement_on_x)
    

    screen.fill((135, 206, 235)) 

    new_ground_rect = pygame.Rect(ground_start_x + movement_on_x, ground_rect.y, ground_rect.width, ground_rect.height)
     
    pygame.draw.rect(screen, (0, 255, 0), new_ground_rect)

    all_sprites.draw(screen)




    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
                
        



