
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

BACKGROUND_IMAGE_1_PATH = 'Layer1.png'
BACKGROUND_IMAGE_1_SPEED = 0.1

BACKGROUND_IMAGE_2_PATH = 'Layer2.png'
BACKGROUND_IMAGE_2_SPEED = 0.3


BACKGROUND_IMAGE_3_PATH = 'Layer3.png'
BACKGROUND_IMAGE_3_SPEED = 0.5

BACKGROUND_IMAGE_4_PATH = 'Layer4.png'
BACKGROUND_IMAGE_4_SPEED = 0.7


PLAYER_SPRITE_PATH = 'mechaneko-sheet1-r1-alpha.png'

ENEMY_SPRITE_PATH = (318, 290, 41, 35)

GROUND_HEIGHT = 25
GROUND_WIDTH = SCREEN_WIDTH * 7

ground_rect = pygame.Rect(0, (SCREEN_HEIGHT - GROUND_HEIGHT), GROUND_WIDTH, GROUND_HEIGHT)

movement_on_x = 0

background_image_1_x = 0
background_image_2_x = 0
background_image_3_x = 0
background_image_4_x = 0

GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1

GAME_STATE_GAME_OVER = 2

GAME_STATE_WON = 3

score = 0
score_font = None

WIN_SCORE = 1000

collectibles_count = 0

current_game_state = GAME_STATE_MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce game")

bg_image_1 = None
bg_image_2 = None
bg_image_3 = None
bg_image_4 = None

player_sprite_sheet = None

enemy_sprite_image = None

BG_1_HEIGHT = 0
BG_2_HEIGHT = 0
BG_3_HEIGHT = 0
BG_4_HEIGHT = 0


try:

    bg_image_1 = pygame.image.load(BACKGROUND_IMAGE_1_PATH).convert_alpha()
    bg_image_2 = pygame.image.load(BACKGROUND_IMAGE_2_PATH).convert_alpha()
    bg_image_3 = pygame.image.load(BACKGROUND_IMAGE_3_PATH).convert_alpha()
    bg_image_4 = pygame.image.load(BACKGROUND_IMAGE_4_PATH).convert_alpha()

    player_sprite_sheet = pygame.image.load(PLAYER_SPRITE_PATH).convert_alpha()

    temp_enemy_image = player_sprite_sheet.subsurface(ENEMY_SPRITE_PATH)

    scale_factor = 2
    enemy_sprite_image = pygame.transform.scale(temp_enemy_image, (temp_enemy_image.get_width() * scale_factor, temp_enemy_image.get_height() * scale_factor))

    BG_1_HEIGHT = bg_image_1.get_height()
    BG_2_HEIGHT = bg_image_2.get_height()
    BG_3_HEIGHT = bg_image_3.get_height()
    BG_4_HEIGHT = bg_image_4.get_height()

    score_font = pygame.font.Font(None, 48)

except:
    print(f"Error loading background image")



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

    font_small = pygame.font.Font(None, 30)

    final_score_text = font_small.render(f"Final score: {score}", True, (255, 255, 0))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    screen.blit(final_score_text, final_score_rect)

    final_collectibles_text = font_small.render(f"Collectibles: {collectibles_count}", True, (255, 255, 255))
    final_collectibles_rect = final_collectibles_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(final_collectibles_text, final_collectibles_rect)

    instruction_text_restart = font_small.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    instruction_restart_rect = instruction_text_restart.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 70))
    screen.blit(instruction_text_restart, instruction_restart_rect)

    pygame.display.flip()


def draw_win_screen():
    screen.fill((0, 150, 0))
    font = pygame.font.Font(None, 70)
    text = font.render("YOU WIN!", True, (255, 255, 0))

    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2 - 50))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36)
    final_score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
    screen.blit(final_score_text, final_score_rect)

    final_collectibles_text = font_small.render(f"Collectibles: {collectibles_count}", True, (0, 255, 255))
    final_collectibles_rect = final_collectibles_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(final_collectibles_text, final_collectibles_rect)

    instruction_text_restart = font_small.render("Press R to Restart or ESC to Quit", True, (255, 255, 255))
    instruction_restart_rect = instruction_text_restart.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100))
    screen.blit(instruction_text_restart, instruction_restart_rect)

    pygame.display.flip()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        player_frame_rect = (164, 387, 38, 30)
        self.image = player_sprite_sheet.subsurface(player_frame_rect)


        scale_factor = 2

        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale_factor, self.image.get_height() * scale_factor))

        self.rect = self.image.get_rect()

        self.rect.x = (SCREEN_WIDTH // 2) - (self.rect.width // 2)

        self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT -self.rect.height

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

    def update(self, platforms_group, enemies_group, collectibles_group):
        global movement_on_x
        global current_game_state
        global score
        global collectibles_count

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



        collided_enemies = pygame.sprite.spritecollide(self, enemies_group, True)

        if collided_enemies:
            current_game_state = GAME_STATE_GAME_OVER

            pygame.time.set_timer(Enemy_spawn, 0)

        collected_items = pygame.sprite.spritecollide(self, collectibles_group, True)
        for item in collected_items:
            score +=10
            collectibles_count += 1

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
    def __init__(self, x, y, image, speed):
        super(Enemy, self).__init__()
        self.image = image
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


class Collectible(pygame.sprite.Sprite):
    def __init__ (self, x, y, size=15, color=(0, 255, 255)):
        super(Collectible, self). __init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect =  self.image.get_rect()

        self.world_x = x
        self.rect.x = x
        self.rect.y = y

        self.collected = False

    def update(self, movement_on_x):
        self.rect.x = self.world_x + movement_on_x

        if self.rect.right < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

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

        if random.random() < 0.6:
            collectible_x = x + random.randint(0, max(0, width - 15))
            collectible_y = y - 20

            new_collectible = Collectible(collectible_x, collectible_y) 

            collectibles.add(new_collectible)
            all_sprites.add(new_collectible)

def game_reset():
    global movement_on_x
    global player
    global score
    global collectibles_count

    movement_on_x = 0

    score = 0
    collectibles_count = 0

    all_sprites.empty()
    platforms.empty()
    enemies.empty()
    collectibles.empty()

    player.rect.x = (SCREEN_WIDTH // 2) - (player.rect.width // 2)
    player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - player.rect.height
    player.change_in_x = 0
    player.change_in_y = 0
    player.on_the_ground = False
    all_sprites.add(player)

    generate_platforms(20)

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


                enemy_speed = random.randint(2, 4)

                spawn_x_world = SCREEN_WIDTH + random.randint(50, 200)
                spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - enemy_sprite_image.get_height()

                if platforms and random.random() < 0.7:
                    random_platform = random.choice(platforms.sprites())

                    potential_platform_y = random_platform.rect.top - enemy_sprite_image.get_height()
                    potential_platform_x_world = random_platform.start_x + random.randint(0, max(0, random_platform.rect.width - enemy_sprite_image.get_width()))


                    if (potential_platform_x_world + movement_on_x < SCREEN_WIDTH + 100):

                        spawn_x_world = potential_platform_x_world
                        spawn_y = potential_platform_y

                new_enemy = Enemy(spawn_x_world, spawn_y, enemy_sprite_image, enemy_speed)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)


    if current_game_state == GAME_STATE_MENU:
        draw_menu_screen()


    elif current_game_state == GAME_STATE_PLAYING:

        movement_on_x -=GAME_SPEED

        score = abs(movement_on_x // 5)

        if score >=  WIN_SCORE:
            current_game_state = GAME_STATE_WON
            pygame.time.set_timer(Enemy_spawn, 0)

        background_image_1_x -=GAME_SPEED * BACKGROUND_IMAGE_1_SPEED
        background_image_2_x -=GAME_SPEED * BACKGROUND_IMAGE_2_SPEED
        background_image_3_x -=GAME_SPEED * BACKGROUND_IMAGE_3_SPEED
        background_image_4_x -=GAME_SPEED * BACKGROUND_IMAGE_4_SPEED
        

        player.update(platforms, enemies, collectibles)
        

        for platform in platforms:
            platform.update(movement_on_x)

        for enemy in enemies:
            enemy.update(movement_on_x)

        for collectible in collectibles:
            collectible.update(movement_on_x)

        for platform in platforms.copy():
            if platform.rect.right < 0:
                platform.kill()
        
        for enemy in enemies.copy():
            if enemy.rect.right < 0:
                enemy.kill()
        for collectible in collectibles.copy():
            if collectible.rect.right < 0:
                collectible.kill()

      

        if len(platforms) < 10:
            generate_platforms(5)

        if score >= WIN_SCORE:
            current_game_state = GAME_STATE_WON
            pygame.time.set_timer(Enemy_spawn, 0)

        if current_game_state == GAME_STATE_PLAYING:
            screen.fill((135, 206, 235))

        first_image =  int(background_image_1_x % bg_image_1.get_width())
        screen.blit(bg_image_1, (first_image, SCREEN_HEIGHT - BG_1_HEIGHT))

        if first_image > 0:
            screen.blit(bg_image_1, (first_image - bg_image_1.get_width(), SCREEN_HEIGHT - BG_1_HEIGHT))
        if first_image < SCREEN_WIDTH - bg_image_1.get_width():
            screen.blit(bg_image_1, (first_image + bg_image_1.get_width(), SCREEN_HEIGHT - BG_1_HEIGHT))


        second_image = int(background_image_2_x % bg_image_2.get_width())
        screen.blit(bg_image_2, (second_image, SCREEN_HEIGHT - BG_2_HEIGHT))
    
        if second_image > 0:
            screen.blit(bg_image_2, (second_image - bg_image_2.get_width(), SCREEN_HEIGHT - BG_2_HEIGHT))
        if second_image < SCREEN_WIDTH - bg_image_2.get_width():
            screen.blit(bg_image_2, (second_image + bg_image_2.get_width(), SCREEN_HEIGHT - BG_2_HEIGHT))

        third_image = int(background_image_3_x % bg_image_3.get_width())
        screen.blit(bg_image_3, (third_image, SCREEN_HEIGHT - BG_3_HEIGHT))

        if third_image > 0:
             screen.blit(bg_image_3, (third_image - bg_image_3.get_width(), SCREEN_HEIGHT - BG_3_HEIGHT))
        if third_image < SCREEN_WIDTH - bg_image_3.get_width():
            screen.blit(bg_image_3, (third_image + bg_image_3.get_width(), SCREEN_HEIGHT - BG_3_HEIGHT))

    
        fourth_image = int(background_image_4_x % bg_image_4.get_width())
        screen.blit(bg_image_4, (fourth_image, SCREEN_HEIGHT - BG_4_HEIGHT))

        if fourth_image > 0:
             screen.blit(bg_image_4, (fourth_image + bg_image_4.get_width(), SCREEN_HEIGHT - BG_4_HEIGHT))
        if fourth_image < SCREEN_WIDTH - bg_image_4.get_width():
            screen.blit(bg_image_4, (fourth_image + bg_image_4.get_width(), SCREEN_HEIGHT - BG_4_HEIGHT))

        

        new_ground_rect = pygame.Rect(ground_start_x + movement_on_x, ground_rect.y, ground_rect.width, ground_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), new_ground_rect)

        collectibles.draw(screen) 
        platforms.draw(screen) 
        enemies.draw(screen)

        all_sprites.draw(screen)

        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        collectibles_count_text = score_font.render(f"Collectibles: {collectibles_count}", True, (0, 255, 255))
        screen.blit(collectibles_count_text, (10, 50))

        pygame.display.flip()

    elif current_game_state == GAME_STATE_GAME_OVER:
        draw_game_over_screen()
    elif current_game_state == GAME_STATE_WON:
        draw_win_screen()

    clock.tick(FPS)

pygame.quit()
                
        



