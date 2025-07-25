import pygame
import random

from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_r, # For restart
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

movement_on_x = 0 # This will control the camera/world shift

# Game States
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2 # Renamed for clarity and consistency

# Initial game state
current_game_state = GAME_STATE_MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce game") 

# --- Game State Drawing Functions ---
def draw_menu_screen(): # Renamed to draw_menu_screen for consistency
    screen.fill((0, 0, 0)) # Black background for menu
    font = pygame.font.Font(None, 74) # Using None for default system font
    text = font.render("Bounce Game", True, (255, 255, 255)) # White text
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36) # Using None for default system font
    instruction_text = font_small.render("Press SPACE to Start", True, (255, 255, 255)) # Added instruction text
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(instruction_text, instruction_rect)

    pygame.display.flip()

def draw_game_over_screen(): # Renamed to draw_game_over_screen for consistency
    screen.fill((0, 0, 0)) # Black background
    font = pygame.font.Font(None, 74) # Using None for default system font
    text = font.render("GAME OVER", True, (255, 0, 0)) # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    screen.blit(text, text_rect)

    font_small = pygame.font.Font(None, 36) # Using None for default system font
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
        global current_game_state # Needed to change game state on game over
        
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
            # Only allow landing on top of platform
            if self.change_in_y > 0 and self.rect.bottom <= platform.rect.bottom + 5 and self.rect.centerx >= platform.rect.left and self.rect.centerx <= platform.rect.right: 
                self.rect.bottom = platform.rect.top
                self.change_in_y = 0
                self.on_the_ground = True
        
        # Game Over condition (Player falls off screen) - Correctly placed outside platform loop
        if self.rect.top > SCREEN_HEIGHT:
            current_game_state = GAME_STATE_GAME_OVER
            pygame.time.set_timer(SPAWN_ENEMY, 0) # Stop spawning enemies when game is over
    
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
        self.start_x = x # Original world X position

    def update(self, movement_on_x_arg):
        self.rect.x = self.start_x + movement_on_x_arg


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

    def update(self, movement_on_x_arg):
        self.world_x -= self.speed 
        self.rect.x = self.world_x + movement_on_x_arg

        if self.rect.right < 0:
            self.kill()

        
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# --- Automated Platform Generation Function ---
def generate_platforms(count):
    last_x = SCREEN_WIDTH # Start generating from the right edge of the screen
    # If there are existing platforms, find the rightmost one to continue generation
    if platforms:
        last_x = max(p.start_x + p.rect.width for p in platforms) # Get world_x of rightmost platform's end

    for _ in range(count):
        x = last_x + random.randint(150, 300) 
        y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - GROUND_HEIGHT - 50) 
        width = random.randint(100, 250) 
        height = 20 

        new_platform = Platform(x, y, width, height)
        platforms.add(new_platform)
        all_sprites.add(new_platform) # Corrected: adding new_platform, not the platforms group
        last_x = x + width 

# --- Game Reset Function ---
def game_reset(): # Renamed to game_reset for consistency
    global movement_on_x # Need to modify the global variable
    global player # Ensure player object is accessible globally for reset

    movement_on_x = 0

    # Clear all existing sprites from their groups
    all_sprites.empty()
    platforms.empty()
    enemies.empty()

    # Re-initialize player position and state
    player.rect.x = (SCREEN_WIDTH // 2) - (25 // 2)
    player.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - 75
    player.change_in_x = 0
    player.change_in_y = 0
    player.on_the_ground = False # Reset on_the_ground state
    all_sprites.add(player) # Add player back to all_sprites

    # Regenerate platforms
    generate_platforms(15) # Generate an initial set of platforms (15 is a good starting number)

    # Reset enemy timer to start spawning again
    pygame.time.set_timer(SPAWN_ENEMY, 1500)


# Initialize player (needed before game_reset can add it to all_sprites)
player = Player() 

# Define SPAWN_ENEMY custom event
SPAWN_ENEMY = pygame.USEREVENT + 1 

# Initial game setup - calls game_reset to set up the initial state
# This ensures that when the game starts, it's in a clean, playable state if PLAYING is the default
# But since we start at MENU, game_reset is called by pressing SPACE
# game_reset() # This line should be commented out or removed, as game_reset is called by menu transition


ground_start_x = ground_rect.x # Store the initial world X position of the ground


clock = pygame.time.Clock()
FPS = 60


# --- The Game Loop ---
running = True

while running:

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            # Handle KEYDOWN events based on current game state
            if current_game_state == GAME_STATE_MENU:
                if event.key == K_SPACE:
                    current_game_state = GAME_STATE_PLAYING # Assignment
                    game_reset() # Call game_reset to prepare for playing
            elif current_game_state == GAME_STATE_PLAYING:
                if event.key == K_LEFT:
                    player.left_movement()
                elif event.key == K_RIGHT:
                    player.right_movement()
                elif event.key == K_UP:
                    player.jump()
            elif current_game_state == GAME_STATE_GAME_OVER:
                if event.key == K_r: # 'R' to restart (using K_r from locals)
                    current_game_state = GAME_STATE_PLAYING # Assignment
                    game_reset() # Call game_reset to prepare for playing

        # Handle KEYUP events (separate from KEYDOWN)
        elif event.type == KEYUP:
            if current_game_state == GAME_STATE_PLAYING: 
                if event.key == K_LEFT and player.change_in_x < 0:
                    player.stop_movement()
                elif event.key == K_RIGHT and player.change_in_x > 0: # Corrected player.change_in_x
                    player.stop_movement()
        
        # Handle SPAWN_ENEMY custom event (separate from KEYDOWN/KEYUP)
        elif event.type == SPAWN_ENEMY:
            if current_game_state == GAME_STATE_PLAYING:
                enemy_width = random.randint(25, 40)
                enemy_height = random.randint(25, 40)
                enemy_speed = random.randint(2, 4)

                # Default spawn position (ground)
                spawn_x_world = SCREEN_WIDTH + random.randint(50, 200) 
                spawn_y = SCREEN_HEIGHT - GROUND_HEIGHT - enemy_height
                
                # Decide if we try to spawn on a platform
                if platforms and random.random() < 0.7: # 70% chance to try platform spawn
                    random_platform = random.choice(platforms.sprites()) 
                    
                    potential_platform_y = random_platform.rect.top - enemy_height
                    # Corrected X calculation for enemy on platform
                    potential_platform_x_world = random_platform.start_x + random.randint(0, max(0, random_platform.rect.width - enemy_width)) # Ensure width is positive
                    
                    # Ensure spawn is not too far off-screen
                    if (potential_platform_x_world + movement_on_x > -enemy_width and 
                        potential_platform_x_world + movement_on_x < SCREEN_WIDTH + random_platform.rect.width + 200):
                        
                        spawn_x_world = potential_platform_x_world
                        spawn_y = potential_platform_y
                
                new_enemy = Enemy(spawn_x_world, spawn_y, enemy_width, enemy_height, enemy_speed)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    # --- Game State Updates and Drawing (outside the event loop, once per frame) ---
    if current_game_state == GAME_STATE_MENU:
        draw_menu_screen() 
    elif current_game_state == GAME_STATE_PLAYING:
        # Update game elements
        player.update(platforms)

        # Update all platforms and enemies, applying camera movement
        for platform in platforms:
            platform.update(movement_on_x)

        for enemy in enemies:
            enemy.update(movement_on_x)

        # Cleanup off-screen platforms
        for platform in platforms.copy(): 
            if platform.rect.right < 0: 
                platform.kill() 
        
        # Generate new platforms if needed
        if len(platforms) < 10: 
            generate_platforms(5) 

        # Drawing for PLAYING state
        screen.fill((135, 206, 235)) # Sky Blue

        # Draw ground (updated with camera movement)
        new_ground_rect = pygame.Rect(ground_start_x + movement_on_x, ground_rect.y, ground_rect.width, ground_rect.height)
        pygame.draw.rect(screen, (0, 255, 0), new_ground_rect) # Green

        # Draw all sprites (player, platforms, enemies)
        all_sprites.draw(screen) 
        pygame.display.flip()

    elif current_game_state == GAME_STATE_GAME_OVER: # Corrected state name
        draw_game_over_screen() 

    # Control frame rate
    clock.tick(FPS) 

pygame.quit()
                
        



