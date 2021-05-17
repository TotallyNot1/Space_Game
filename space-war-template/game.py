# Imports
import pygame
import random


# Window settings
WIDTH = 1300
HEIGHT = 700
TITLE = "AETHER PRIMORDIAL"
FPS = 60

# Game Stages
START = 0
PLAYING = 1
LOSE = 2
WIN = 3

# Create window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (152, 7, 7)
BLUE = (7, 26, 152)
ORANGE =(152, 46, 7)
YELLOW = (152, 104, 7)
GREEN = (21, 152, 7)
PURPLE = (55, 7, 152)
PINK = (152, 7, 99)



# Load fonts
title_font = pygame.font.Font('assets/fonts/recharge bd.ttf', 80)
default_font = pygame.font.Font(None, 40)

# Load images
background = pygame.image.load('assets/images/Background1.png').convert_alpha()
ship_img = pygame.image.load('assets/images/Player_Ship.png').convert_alpha()
Xship_img = pygame.image.load('assets/images/Player_ShipX.png').convert_alpha()
Zship_img = pygame.image.load('assets/images/Player_ShipZ.png').convert_alpha()
starship_img = pygame.image.load('assets/images/Player_Ship(Star).gif').convert_alpha()
strength_powerup_img = pygame.image.load('assets/images/Strength_power_up.gif').convert_alpha()
laser_img = pygame.image.load('assets/images/Blue_Laser.gif').convert_alpha()
bomb_img = pygame.image.load('assets/images/Red_Laser.gif').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemy_ship.png').convert_alpha()
enemy2_img = pygame.image.load('assets/images/enemy_ship2.png').convert_alpha()
enemy3_img = pygame.image.load('assets/images/speed_enemy.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/Shield_Powerup.png').convert_alpha()
custom_powerup_img = pygame.image.load('assets/images/Custom_Power-up.gif').convert_alpha()
Phi_Boss_img = pygame.image.load('assets/images/Phi.png').convert_alpha()
Sigma_Boss_img = pygame.image.load('assets/images/Sigma (Final Boss).png').convert_alpha()
# Load sounds
laser_snd = pygame.mixer.Sound('assets/sounds/laser.ogg')
explosion_snd = pygame.mixer.Sound('assets/sounds/explosion.ogg')

# Music
start_music = 'assets/music/theme.wav'
stage_theme = 'assets/music/main_theme.wav'
Boss_theme = 'assets/music/Bosstheme.wav'
stage_theme2 = 'assets/music/main_theme2.wav'
Victory_theme = 'assets/music/Victory.wav'

# Game classes
class Ship(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5
        self.shield = 4
        self.max_shield = 6
        self.shot_limit = 5
        
    def move_left(self):
        self.rect.x -= self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
            
    def move_right(self):
        self.rect.x += self.speed

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
    def move_down(self):
        self.rect.y += self.speed

        if self.rect.bottom > 1000:
            self.rect.bottom = 1000

    def move_up(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 600:
            self.rect.bottom = 600


        
    def shoot(self):
        if len(lasers) < self.shot_limit:
           x = self.rect.centerx
           y = self.rect.top

           lasers.add( Laser(x, y, laser_img) )
            
           laser_snd.play()

    def check_bombs(self):
        hits = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hits:
            self.shield -= 1

            if self.shield <= 0:
                self.kill()
                explosion_snd.play()
                
    def check_powerups(self):
        hits = pygame.sprite.spritecollide(self, powerups, True)

        for hit in hits:
            hit.apply(self)
            
                       
    def update(self):
       self.check_bombs()
       self.check_powerups()
        
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 5
        
    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
            

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
class ShieldPowerup(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y

        self.speed = 2

    def apply(self, ship):
        if ship.shield ==3:
            ship.shield += 1
        else:
            ship.shield = 3
            
        player.score += 5
        
    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image, shield, value):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        
        self.shield = shield
        self.value = value
        
    def drop_bomb(self):
        x = self.rect.centerx 
        y = self.rect.bottom
        bombs.add(Bomb(x, y, bomb_img)) 
        laser_snd.play()
        
    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
          self.shield -= 1

        if self.shield <= 0:
            self.kill()
            explosion_snd.play()
            player.score += self.value
            
class Boss(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image, shield, value):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        
        self.shield = shield
        self.value = value
        
    def drop_bomb(self):
        x = self.rect.centerx 
        y = self.rect.bottom
        bombs.add(Bomb(x, y, bomb_img)) 
        laser_snd.play()
        
    def update(self):
        hits = pygame.sprite.spritecollide(self, lasers, True)

        for laser in hits:
          self.shield -= 1

        if self.shield <= 0:
            self.kill()
            explosion_snd.play()
            player.score += self.value
            
class Fleet (pygame.sprite.Group):

    def __init__(self, *sprites):
        super().__init__(*sprites)

        self.speed = 2
        self.bomb_rate = 1
        
    def move(self):
        reverse = False
        
        for sprite in self.sprites():
            sprite.rect.x += self.speed

            if sprite.rect.right > WIDTH or sprite.rect.left < 0:
                reverse = True

        if reverse:
            self.speed *= -1
            
    def select_bomber(self):
        sprites = self.sprites()

        if len(sprites) > 0:
            r = random.randrange(0, 120)
            
            if r < self.bomb_rate + 0.75 *player.level:
                bomber = random.choice(sprites)
                bomber.drop_bomb()
        
    def update(self, *args):
        super().update(*args)

        self.move()

        if len(player) > 0:
            
            self.select_bomber()
        

# Setup
def new_game():
    global ship, player
    
    start_x = WIDTH / 2
    start_y = HEIGHT - 100
    ship = Ship(start_x, start_y, ship_img)
    
    player = pygame.sprite.GroupSingle(ship)
    player.score = 0
    player.level = 1

    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)
    
def start_level():
    global enemies, lasers, bombs, powerups
    if player.level == 1:
        e1 = Enemy(450, 40, enemy_img, 5, 10)
        e2 = Enemy(650, 40, enemy_img, 5, 10)
        e3 = Enemy(850, 40, enemy_img, 5, 10)
        e4 = Enemy(250, 90, enemy_img, 5, 10)
        e5 = Enemy(1000, 90, enemy_img, 5, 10)
        e6 = Enemy(550, 90, enemy_img, 5, 10)
        e7 = Enemy(750, 90, enemy_img, 5, 10)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7)
    elif player.level == 2:
        e1 = Enemy(450, 40, enemy_img, 5, 10)
        e2 = Enemy(650, 40, enemy_img, 5, 10)
        e3 = Enemy(850, 40, enemy_img, 5, 10)
        e4 = Enemy(550, 80, enemy2_img, 7, 20)
        e5 = Enemy(750, 80, enemy2_img, 7, 20)
        e6 = Enemy(900, 120, enemy2_img, 7, 20)
        e7 = Enemy(300, 80, enemy2_img, 7, 20)
        e8 = Enemy(460, 120, enemy2_img, 7, 20)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8)
    elif player.level == 3:
        e1 = Enemy(450, 40, enemy2_img, 5, 20)
        e2 = Enemy(650, 40, enemy2_img, 5, 20)
        e3 = Enemy(850, 40, enemy2_img, 5, 20)
        e4 = Enemy(750, 120, enemy2_img, 7, 20)
        e5 = Enemy(950, 120, enemy2_img, 7, 20)
        e6 = Enemy(300, 80, enemy2_img, 7, 20)
        e7 = Enemy(460, 120, enemy2_img, 7, 20)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7)
    elif player.level == 4:
        e1 = Enemy(450, 80, enemy2_img, 5, 20)
        e2 = Enemy(650, 80, enemy2_img, 5, 20)
        e3 = Enemy(850, 80, enemy2_img, 5, 20)
        e4 = Enemy(550, 80, enemy2_img, 7, 20)
        e5 = Enemy(750, 80, enemy2_img, 7, 20)
        e6 = Enemy(550, 200, enemy2_img, 7, 20)
        e7 = Enemy(250, 200, enemy2_img, 7, 20)
        e8 = Enemy(550, 80, enemy2_img, 7, 20)
        e9 = Enemy(950, 200, enemy2_img, 7, 20)
        e10 = Enemy(350, 80, enemy2_img, 7, 20)
        enemies = Fleet(e1, e2, e3, e4, e5, e6, e7, e8, e9, e10)
    elif player.level == 5:
        e1 = Enemy(450, 150, Phi_Boss_img, 15, 200)
        enemies = Fleet(e1)
    elif player.level == 6:
        e1 = Enemy(250,200, enemy2_img, 7, 20)
        e2 = Enemy(650, 100, enemy2_img, 7, 20)
        e3 = Enemy(850, 100, enemy3_img, 5, 20)
        e4 = Enemy(500, 200, enemy2_img, 7, 20)
        e5 = Enemy(750, 200, enemy2_img, 7, 20)
        enemies = Fleet(e1, e2, e3, e4, e5)
    elif player.level == 7:
        e1 = Enemy(450, 80, enemy2_img, 7, 10)
        e2 = Enemy(650, 80, enemy2_img, 7, 10)
        e3 = Enemy(850, 80, enemy2_img, 7, 10)
        e4 = Enemy(250, 120, enemy3_img, 5, 10)
        e5 = Enemy(1000, 120, enemy3_img, 5, 10)
        e6 = Enemy(550, 120, enemy2_img, 7, 10)
        e7 = Enemy(750, 120, enemy2_img, 7, 10)
        enemies = Fleet(e1, e2, e3, e4, e5)
    elif player.level == 8:
        e1 = Enemy(250, 90, enemy2_img, 7, 20)
        e2 = Enemy(650, 120, enemy3_img, 5, 20)
        e3 = Enemy(750, 120, enemy2_img, 7, 20)
        e4 = Enemy(100, 80, enemy3_img, 5, 20)
        e5 = Enemy(900, 120, enemy3_img, 5, 20)
        enemies = Fleet(e1, e2, e3, e4, e5)
    elif player.level == 9:
        e1 = Enemy(400, 80, enemy2_img, 7, 20)
        e2 = Enemy(400, 300, enemy2_img, 7, 20)
        e3 = Enemy(800, 80, enemy2_img, 7, 20)
        e4 = Enemy(800, 300, enemy2_img, 7, 20)
        e5 = Enemy(700, 80, enemy2_img, 7, 20)
        e6 = Enemy(550, 300, enemy3_img, 5, 10)
        e7 = Enemy(700, 300, enemy3_img, 5, 10)
        e8 = Enemy(550, 300, enemy3_img, 5, 10)
        e9 = Enemy(900, 300, enemy2_img, 7, 10)
        e10 = Enemy(900, 80, enemy3_img, 5, 10)
        enemies = Fleet(e1, e2, e3, e4, e5, e7, e8, e9, e10)
    elif player.level == 10:
        e1 = Enemy(450, 200, Sigma_Boss_img, 30, 200)
        enemies = Fleet(e1)
    
    
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
    x = random.randint(HEIGHT, WIDTH)
    y = random.randint (-3000, -1000)
    p1 = ShieldPowerup(x, y, powerup_img)

    powerups = pygame.sprite.Group(p1)
        
def display_stats():
    score_text = default_font.render("Score: " + str(player.score), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.left = 20
    screen.blit(score_text, rect)

    level_text = default_font.render("Level :" + str(player.level), True, WHITE)
    rect = score_text.get_rect()
    rect.top = 20
    rect.left = WIDTH - 120
    screen.blit(level_text, rect)
    
def display_shield():
        pygame.draw.rect(screen,RED,[16,HEIGHT -49, 288, 33])
        if ship.shield == 1:
                pygame.draw.rect(screen,YELLOW,[20,HEIGHT -45, 93.33 , 25])
        elif ship.shield == 2:
                pygame.draw.rect(screen,ORANGE,[20,HEIGHT -45, 186.66, 25])
        elif ship.shield == 3:
                pygame.draw.rect(screen,GREEN,[20,HEIGHT -45, 280, 25])
        elif ship.shield == 4:
                pygame.draw.rect(screen,PINK,[20,HEIGHT -45, 280, 25])
        elif ship.shield >= 5:
                pygame.draw.rect(screen,PURPLE,[20,HEIGHT -45, 280, 25])

def start_screen():
    
    title_text = title_font.render(TITLE, True, WHITE)
    rect = title_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.bottom = HEIGHT // 2 - 15
    screen.blit(title_text, rect)

    sub_text = default_font.render("Press any key to start", True, WHITE)
    rect = sub_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.top = HEIGHT // 2 + 15
    screen.blit(sub_text, rect)
    
def lose_screen():
    lose_text = default_font.render("Game Over", True, WHITE)
    rect = lose_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.centery = HEIGHT // 2
    screen.blit(lose_text, rect)

def win_screen():
    win_text = default_font.render("You Win!", True, WHITE)
    rect = win_text.get_rect()
    rect.centerx = WIDTH // 2
    rect.centery = HEIGHT // 2
    screen.blit(win_text, rect)

def play_music(file, loops):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops)

    if player.level == 5 and 10:
        play_music(Boss_theme, -1)
    elif player.level >=6:
        play_music(stage_theme2)
        
    
# Game loop
new_game()
start_level()
stage = START

running = True

while running:
    # Input handling
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                
            if stage == START:
                stage = PLAYING
                pygame.mixer.music.load(stage_theme)
                pygame.mixer.music.play(-1)
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            elif stage == LOSE or stage == WIN:
                if event.key == pygame.K_r:
                    new_game()
                    start_level()
                    stage = START
            if stage == WIN:
                play_music(Victory_theme, -1)
                
    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        elif pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()
    
    # Game logic
    if stage != START:
        lasers.update()
        bombs.update()
        enemies.update()
        player.update()
        powerups.update()
    
    if len(enemies) == 0:
        if player.level == 10:
            stage = WIN
        else:
            player.level += 1
            start_level()
    elif len(player) == 0:
        stage = LOSE
        
    # Drawing code
    screen.fill(BLACK)
    screen.blit(background, [20, 0,])
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    powerups.draw(screen)
    display_stats()
    display_shield()
    if stage == START:
        start_screen()
    elif stage == LOSE:
        lose_screen()
    elif stage == WIN:
        win_screen()
        
    # Update screen
    pygame.display.update()


    
    # Limit refresh rate of game loop 
    clock.tick(FPS)


# Close window and quit
pygame.quit()
