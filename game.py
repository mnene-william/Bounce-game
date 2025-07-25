import pygame
import random

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
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

GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_OVER = 2

current_game_state = GAME_STATE_MENU
ground_rect = pygame.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), GROUND_WIDTH, GROUND_HEIGHT)

movement_on_x = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Bounce game") 


def menu_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Bounce Game", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

def game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    small_font = pygame.font.Font(None, 36)
    instruction_text = small_font.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(instruction_text, instruction_rect)



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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super(Enemy, self). __init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0 , 0))
        self.rect = self.image.get_rect()

        self.initial_spawn_on_x = x
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self, movement_on_x):
        self.initial_spawn_on_x -= self.speed

        self.rect.x = self.initial_spawn_on_x + movement_on_x

        if self.rect.right < 0:
            self.kill()


        
all_sprites = pygame.sprite.Group()

platforms = pygame.sprite.Group()

enemies = pygame.sprite.Group()

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

enemy1 = Enemy(SCREEN_WIDTH + 200, (SCREEN_HEIGHT - GROUND_HEIGHT - 30), 30, 30, speed=3)
enemies.add(enemy1)
all_sprites.add(enemy1)

enemy2 = Enemy(platform6.start_x + 100,(platform6.rect.top - 30), 30, 30, speed=3)
enemies.add(enemy2)
all_sprites.add(enemy2)


player = Player()
all_sprites.add(player)

ground_start_x = ground_rect.x


clock = pygame.time.Clock()
FPS = 60


Enemy_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(Enemy_spawn, 1500)






running = True

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if current_game_state == GAME_STATE_MENU:
                if event.key == K_SPACE:
                    current_game_state == GAME_STATE_PLAYING

                    player.rect.x = (SCREEN_WIDTH // 2) - (25 // 2)
                    player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 75

                    player.change_in_x = 0
                    player.change_in_y = 0

                    movement_on_x = 0

                    platforms.empty()
                    enemies.empty()
                    
                    pygame.time.set_timer(Enemy_spawn, 1500)

            elif event.type == KEYUP and current_game_state == GAME_STATE_PLAYING:
                if event.key == K_LEFT and player.change_in_x < 0:
                    player.stop_movement()

                elif event.key == K_RIGHT and player.change_in_y > 0:
                    player.stop_movement()

            elif event.type == Enemy_spawn and current_game_state == GAME_STATE_PLAYING:
                enemy_width = random.randint(25, 40)
                enemy_height = random.randint(25, 40)
                enemy_speed = random.randint(2, 4)

                spawn_x = SCREEN_WIDTH + random.randint(50, 200)

                spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - enemy_height

                if platforms and random.random() < 0.7:
                    random_platform = random.choice(platforms.sprites())

                    random_platform_y = random_platform.rect.top - enemy_height

                    random_platform_x = random_platform.rect.top - enemy_height

                    if random_platform_x + movement_on_x > -enemy_width and random_platform_x + movement_on_x < SCREEN_WIDTH + random_platform.rect.width + 200:
                        spawn_x = random_platform_x

                        spawn_y = random_platform_y

                




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

        elif event.type == Enemy_spawn:
            enemy_width = random.randint(25, 40)
            enemy_height = random.randint(25, 40)
            enemy_speed = random.randint(2, 4)

            spawn_x = SCREEN_WIDTH + random.randint(50, 200)

            ground_spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - enemy_height

            platform_spawn_y = None

            if platforms:
                random_platform = random.choice(platforms.sprites())

                platform_spawn_y = random_platform.rect.top - enemy_height 
                platform_spawn_x = random_platform.start_x + random.randint(0, random_platform.rect.width - enemy_width)


                if random.random() < 0.7 and platforms:
                    new_enemy = Enemy(platform_spawn_x, platform_spawn_y, enemy_width, enemy_height, enemy_speed)
                else:
                    new_enemy = Enemy(spawn_x, ground_spawn_y, enemy_width, enemy_height, enemy_speed)


                enemies.add(new_enemy)
                all_sprites.add(new_enemy)




    player.update(platforms)

    for platform in platforms:
        platform.update(movement_on_x)


    for enemy in enemies:
        enemy.update(movement_on_x)
    

    screen.fill((135, 206, 235)) 

    new_ground_rect = pygame.Rect(ground_start_x + movement_on_x, ground_rect.y, ground_rect.width, ground_rect.height)
     
    pygame.draw.rect(screen, (0, 255, 0), new_ground_rect)

    all_sprites.draw(screen)




    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
                
        



