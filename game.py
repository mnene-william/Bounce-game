import pygame

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


JUMP_STRENGTH = -16

GROUND_HEIGHT = 25
ground_rect = pygame.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), SCREEN_WIDTH, GROUND_HEIGHT)

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

    

    def update(self):
        
        self.gravity_force()

        self.rect.y += self.change_in_y

        self.rect.x += self.change_in_x


        if self.rect.left < 0:
            self.rect.left = 0
            self.change_in_x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.change_in_x = 0

        if self.rect.colliderect(ground_rect):
            if self.change_in_y > 0:

                self.rect.bottom = ground_rect.top
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

        super(Platform)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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

    all_sprites.update()
            

    screen.fill((135, 206, 235)) 
     
    pygame.draw.rect(screen, (0, 255, 0), ground_rect)

    all_sprites.draw(screen)




    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
                
        



