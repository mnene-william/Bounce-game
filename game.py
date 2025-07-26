# Replace all SPAWN_ENEMY with Enemy_spawn

import pygame
import random

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_r,
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


GAME_SPEED = 5

GROUND_HEIGHT = 25
GROUND_WIDTH = SCREEN_WIDTH * 7

ground_rect = pygame.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), GROUND_WIDTH, GROUND_HEIGHT)

movement_on_x = 0

GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1

GAME_STATE_GAME_OVER = 2

current_game_state = GAME_STATE_MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce game")

def draw_menu_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)

    text = font.render("Bounce Game", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    instruction_text = font_small.render("Press SPACE to Start", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.blit(instruction_text, instruction_rect)

    pygame.display.flip()

def draw_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, (255, 0, 0))

    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    instruction_text = font_small.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(instruction_text, instruction_rect)

    pygame.display.flip()

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
        if self.change_in_y > 10:
            self.change_in_y = 10

    def jump(self):
        if self.on_the_ground:

            self.change_in_y = JUMP_STRENGTH
            self.on_the_ground = False

    def update(self, platforms_group):
        global movement_on_x
        global current_game_state

        self.gravity_force()
        self.rect.y += self.change_in_y


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
            if self.change_in_y > 0 and self.rect.bottom <= platform.rect.bottom + 5 and self.rect.centerx >= platform.rect.left and self.rect.centerx <= platform.rect.right:
                self.rect.bottom = platform.rect.top
                self.change_in_y = 0
                self.on_the_ground = True

        if self.rect.top > SCREEN_HEIGHT:
            current_game_state = GAME_STATE_GAME_OVER
            pygame.time.set_timer(Enemy_spawn, 0)



        collided_enemies = pygame.sprite.spritecollide(self, enemies, True)

        if collided_enemies:
            current_game_state = GAME_STATE_GAME_OVER

            pygame.time.set_timer(Enemy_spawn, 0)

    def left_movement(self):
        self.change_in_x = -PLAYER_SPEED

    def right_movement(self):
        self.change_in_x = PLAYER_SPEED

    def stop_movement(self):
        self.change_in_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Platform, self).__init__()
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
        super(Enemy, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0 , 0))
        self.rect = self.image.get_rect()

        self.world_x = x
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def update(self, movement_on_x):
        self.world_x -= self.speed
        self.rect.x = self.world_x + movement_on_x

        if self.rect.right < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

def generate_platforms(count):
    last_x = SCREEN_WIDTH
    if platforms:
        last_x = max(p.start_x + p.rect.width for p in platforms)

    for _ in range(count):
        x = last_x + random.randint(150, 300)
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
        width = random.randint(100, 250)
        height = 20

        new_platform = Platform(x, y, width, height)
        platforms.add(new_platform)
        
        all_sprites.add(new_platform)
        last_x = x + width

def game_reset():
    global movement_on_x
    global player

    movement_on_x = 0

    all_sprites.empty()
    platforms.empty()
    enemies.empty()

    player.rect.x = (SCREEN_WIDTH // 2) - (25 // 2)
    player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 75
    player.change_in_x = 0
    player.change_in_y = 0
    player.on_the_ground = False
    all_sprites.add(player)

    generate_platforms(15)

    pygame.time.set_timer(Enemy_spawn, 1500)

player = Player()

Enemy_spawn = pygame.USEREVENT + 1

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

            if current_game_state == GAME_STATE_MENU:
                if event.key == K_SPACE:
                    current_game_state = GAME_STATE_PLAYING
                    game_reset()
            elif current_game_state == GAME_STATE_PLAYING:
                if event.key == K_UP:
                    player.jump()


            elif current_game_state == GAME_STATE_GAME_OVER:
                if event.key == K_r:
                    current_game_state = GAME_STATE_PLAYING
                    game_reset()

        elif event.type == Enemy_spawn:

            if current_game_state == GAME_STATE_PLAYING:
                enemy_width = random.randint(25, 40)
                enemy_height = random.randint(25, 40)

                enemy_speed = random.randint(2, 4)

                spawn_x_world = SCREEN_WIDTH + random.randint(50, 200)
                spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - enemy_height

                if platforms and random.random() < 0.7:
                    random_platform = random.choice(platforms.sprites())

                    potential_platform_y = random_platform.rect.top - enemy_height
                    potential_platform_x_world = random_platform.start_x + random.randint(0, max(0, random_platform.rect.width - enemy_width))


                    if (potential_platform_x_world + movement_on_x > -enemy_width and
                        potential_platform_x_world + movement_on_x < SCREEN_WIDTH + random_platform.rect.width + 200):

                        spawn_x_world = potential_platform_x_world
                        spawn_y = potential_platform_y

                new_enemy = Enemy(spawn_x_world, spawn_y, enemy_width, enemy_height, enemy_speed)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


    if current_game_state == GAME_STATE_MENU:
        draw_menu_screen()


    elif current_game_state == GAME_STATE_PLAYING:

        movement_on_x -=GAME_SPEED

        player.update(platforms)
        

        for platform in platforms:
            platform.update(movement_on_x)

        for enemy in enemies:
            enemy.update(movement_on_x)

        for platform in platforms.copy():
            if platform.rect.right < 0:
                platform.kill()

        if len(platforms) < 10:
            generate_platforms(5)

        screen.fill((135, 206, 235))

        new_ground_rect = pygame.Rect(ground_start_x + movement_on_x, ground_rect.y, ground_rect.width, ground_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), new_ground_rect)

        all_sprites.draw(screen)
        pygame.display.flip()

    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_game_over_screen()

    clock.tick(FPS)

pygame.quit()
                
        



