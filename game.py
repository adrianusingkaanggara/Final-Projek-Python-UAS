import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'image')
snd_dir = path.join(path.dirname(__file__), 'sound')


WIDTH = 480
HEIGHT = 600
FPS = 60
Waktu_PowerUp = 10000  

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (115, 115, 115)

# initialize pygame and display window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AR VS Zeef Galaxy")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('KenVector Future', bold=True, italic=False)
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE) # pygame.font.render(text, antialias = True or False, color, background=None)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
def draw_shield_bar(surf, x, y, bar):
    if bar < 0:
        bar = 0
        
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (bar / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
   
     
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = memanggil objek yang diinginkan
        # self.image = pygame.Surface((50, 40)) # Surface membuat objek kotak
        # self.image.fill(GREEN) # mewarnai objek player
        self.image = pygame.transform.scale(player_img, (100, 100)) # mengubah skala objek
        self.image.set_colorkey(BLACK) # menghilangkan outline hitam
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100 # Membuat value Shield untuk nyawa
        self.shoot_delay = 100 # Muncul peluru dalam satuan ms
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3 # Set Nyawa bisa berapa aja
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.kekuatan = 1
        self.kekuatan_time = pygame.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        # Fungsi input keyboard
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        elif self.rect.left < 0:
            self.rect.left = 0

        elif self.rect.y < 0:
            self.rect.y = 0

        elif self.rect.y > HEIGHT:
            self.rect.y = HEIGHT
            
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        
        #Timeout for PowerUps  
        if self.kekuatan >= 2 and pygame.time.get_ticks() - self.kekuatan_time > Waktu_PowerUp:
            self.kekuatan -= 1
            self.kekuatan_time = pygame.time.get_ticks()
            
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.kekuatan == 1:
                peluru = Peluru(self.rect.centerx, self.rect.top)
                all_sprites.add(peluru)
                peluru_s.add(peluru)    
                suara_tembakan.play()
            if self.kekuatan >= 2:
                peluru1 = Peluru(self.rect.left, self.rect.centery)
                peluru2 = Peluru(self.rect.right, self.rect.centery)
                
                all_sprites.add(peluru1)
                all_sprites.add(peluru2)
                
                peluru_s.add(peluru1)
                peluru_s.add(peluru2)
                
                suara_tembakan.play()
            # if self.kekuatan >= 3:
            #     peluru3 = Peluru(self.rect.right, self.rect.centery)
            #     all_sprites.add(peluru3)
            #     peluru_s.add(peluru3)
                
        
    def hide(self):
        # Hide player sementara
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
        
    def menambah_kekuatan(self):
        self.kekuatan += 1
        self.kekuatan_time = pygame.time.get_ticks()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = memanggil objek yang diinginkan
        # self.image = pygame.Surface((50, 40)) # Surface membuat objek kotak
        # self.image.fill(RED) # mewarnai objek player
        self.image_orig = random.choice(meteor_img) # Memakai Objek Meteor.png
        self.image_orig.set_colorkey(BLACK) # Menghilangkan outline dari png
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, -200)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-8, 8)
        self.rot = 0 # Set Rotation
        self.rot_speed = random.randrange(-8, 8) # Rotation Speed
        self.last_update = pygame.time.get_ticks()
    
    # Fungsi Rotasi objek Mob
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            # self.image = pygame.transform.rotate(self.image_orig, self.rot)
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        
    def update(self):
        self.rotate() # Return Rotasi
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-8, 8)

class Musuh(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(musuh_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, -200)
        self.radius = int(self.rect.width * .85 / 2)
        self.speedy = random.randrange(1, 10)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy
        # Kill if kelewat dari screen
        if self.rect.top > HEIGHT:
            self.kill()
    


class Peluru(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10, 20))
        # self.image.fill(YELLOW)
        self.image = peluru_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
          
    def update(self):
        self.rect.y += self.speedy
        # Kill
        if self.rect.bottom < 0:
            self.kill()
           
class Ledakan(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = ledakan_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75 # Standard = 30, Normal = 60, Faster = 75
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(ledakan_anim[self.size]):
                self.kill()
            
            else:
                center = self.rect.center
                self.image = ledakan_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
    
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'lives'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        # Kill if kelewat dari screen
        if self.rect.top > HEIGHT:
            self.kill()


# Membuat Class Huruf Hijaiyah            
class Huruf_Hijaiyah(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.transform.scale(random.choice(hijaiyah_img), (100, 100)) # Untuk set ukuran image pada random image
        self.image = random.choice(hijaiyah_img)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
        
    def update(self):
        self.rect.y += self.speedy
        # Kill if kelewat dari screen
        if self.rect.top > HEIGHT:
            self.kill()

#     self.image = pygame.transform.scale(Surface, 100, 100)
#     self.image.rect = self.image.get_rect()



def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ARZeef Galaxy", 44, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "AR & Zeef @2020", 34, WIDTH / 2, HEIGHT / 2.9)
    draw_text(screen, "Key Arah untuk bergerak, Space untuk menembak", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Tekan tombol apa aja Untuk Mulai", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False                

# Load all Graphics
# Load Background
background = pygame.image.load(path.join(img_dir, "background/darkspace.png")).convert()
background_rect = background.get_rect()


player_img = pygame.image.load(path.join(img_dir, "character/playerShip2.gif")).convert() # Objek Player
player_mini_img = pygame.transform.scale(player_img, (25, 19)) # Objek Nyawa Player
player_mini_img.set_colorkey(BLACK)
# meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
meteor_img = []
meteor_list = ['meteor/meteorBrown_big1.png', 'meteor/meteorBrown_big2.png', 'meteor/meteorBrown_med1.png', 
               'meteor/meteorBrown_med3.png', 'meteor/meteorBrown_tiny1.png', 'meteor/meteorBrown_tiny2.png']
peluru_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
powerup_img = {}
powerup_img['shield'] = pygame.image.load(path.join(img_dir, 'powerup/shield_gold.png')).convert()
# powerup_img['shield_kecil']
powerup_img['gun'] = pygame.image.load(path.join(img_dir, 'powerup/bolt_gold.png')).convert()
powerup_img['lives'] = pygame.image.load(path.join(img_dir, 'powerup/pill_red.png')).convert()
hijaiyah_img = []
hijaiyah_list = ['hijaiyah/baa-01.png', 'hijaiyah/qaf-01.png', 'hijaiyah/tha-01.png', 'hijaiyah/dal.png', 'hijaiyah/jim.png']
musuh_img = []
musuh_list = ['musuh/enemyBlack1.png', 'musuh/enemyBlue1.png', 'musuh/enemyGreen1.png', 'musuh/enemyRed1.png',
            'musuh/enemyBlack2.png', 'musuh/enemyBlue2.png', 'musuh/enemyGreen2.png', 'musuh/enemyRed2.png',
            'musuh/enemyBlack3.png', 'musuh/enemyBlue3.png', 'musuh/enemyGreen3.png', 'musuh/enemyRed3.png',
            'musuh/enemyBlack4.png', 'musuh/enemyBlue4.png', 'musuh/enemyGreen4.png', 'musuh/enemyRed4.png',
            'musuh/enemyBlack5.png', 'musuh/enemyBlue5.png', 'musuh/enemyGreen5.png', 'musuh/enemyRed5.png',]
# musuh_list = ['musuh/enemyPlane.png', 'musuh/enemyPlane2.png']

for image in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_dir, image)).convert())
    
for image in hijaiyah_list:
    hijaiyah_img.append(pygame.image.load(path.join(img_dir, image)).convert())

for image in musuh_list:
    musuh_img.append(pygame.image.load(path.join(img_dir, image)).convert())
    

# for image in huruf_hijaiyah['qalqalah']:
#     huruf_hijaiyah.append(pygame.image.load(path.join(img_dir, image)).convert()) 

# Membuat efek ledakan
ledakan_anim = {}
ledakan_anim['besar'] = []
ledakan_anim['kecil'] = []
ledakan_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert() # Load Image ledakan Mob
    img.set_colorkey(BLACK)
    img_besar = pygame.transform.scale(img, (75, 75))
    ledakan_anim['besar'].append(img_besar)
    img_kecil = pygame.transform.scale(img,(32, 32))
    ledakan_anim['kecil'].append(img_kecil)   
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert() # Load Image ledakan Player
    img.set_colorkey(BLACK)
    ledakan_anim['player'].append(img)
    


 
# Load Game Suara
suara_tembakan = pygame.mixer.Sound(path.join(snd_dir, 'sfx_laser2.ogg'))
# suara = []
# for sound in ['mlehoy.wav']
suara_ledakan = []
for sound in ['Explosion3.wav', 'Explosion11.wav']:
    suara_ledakan.append(pygame.mixer.Sound(path.join(snd_dir, sound))) # Menambah suara Ledakan
suara_pickup = []
for sound in ['Pickup21.wav', 'Pickup27.wav', 'Pickup34.wav']:
    suara_pickup.append(pygame.mixer.Sound(path.join(snd_dir, sound))) # Menambah suara Pickup
# musik = pygame.mixer.music.load(path.join(snd_dir, 'file_music.wav')) # menyalakan musik

# All Collision Group ditaruh di game over screen
# # Collision            
# all_sprites = pygame.sprite.Group()
# mobs = pygame.sprite.Group()
# peluru_s = pygame.sprite.Group()
# powerups = pygame.sprite.Group()
# player = Player()
# all_sprites.add(player)
def newmob():
     m = Mob()
     all_sprites.add(m)
     mobs.add(m)

def newmusuh():
    m1 = Musuh()
    all_sprites.add(m1)
    musuh.add(m1)
    
# for i in range(8):
#     newmob()
# score = 0
# # pygame.mixer.music.play(loops=-1)
    

# Game Loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        peluru_s = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        huruf_hijaiyah = pygame.sprite.Group()
        player = Player()
        musuh = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(15):
            newmob()
        for i in range(1):
            newmusuh()
        score = 0
    # keep loop running at right speed
    clock.tick(FPS)
    # Proses Input (events)
    for event in pygame.event.get():
        # closing window
        if event.type == pygame.QUIT:
           running = False
           
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()
           
    # Update
    all_sprites.update()
    
    # Checking
    # check peluru mengenai mob
    hits = pygame.sprite.groupcollide(mobs, peluru_s, True, True, collided = None)
    for hit in hits:
        score += 1 * hit.radius #Kalkulasi Score
        random.choice(suara_ledakan).play()
        meledak = Ledakan(hit.rect.center, 'besar') # Memanggil Class Ledakan
        all_sprites.add(meledak)
        if random.random() > 0.5: # tingkat rare
            power = PowerUp(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
            
        elif random.random() > 0.5:
            hijaiyah = Huruf_Hijaiyah(hit.rect.center)
            all_sprites.add(hijaiyah)
            huruf_hijaiyah.add(hijaiyah)
        newmob()

    # check peluru mengenai musuh
    hits = pygame.sprite.groupcollide(musuh, peluru_s, True, True, collided = None)
    for hit in hits:
        score += 10 * hit.radius #Kalkulasi Score
        random.choice(suara_ledakan).play()
        meledak = Ledakan(hit.rect.center, 'besar') # Memanggil Class Ledakan
        all_sprites.add(meledak)
        newmusuh()
        
    # check untuk melihat if mob menembak player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        random.choice(suara_ledakan).play()
        meledak = Ledakan(hit.rect.center, 'kecil') # Memanggil Class Ledakan
        all_sprites.add(meledak)
        newmob()
        if player.shield <= 0:
            mati_meledak = Ledakan(player.rect.center, 'player') # Jika meledak sampe mati
            all_sprites.add(mati_meledak)
            player.hide()
            player.lives -= 1
            player.shield = 100
            # player.kill() # Mati

    # check untuk melihat if musuh menembak player
    hits = pygame.sprite.spritecollide(player, musuh, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        random.choice(suara_ledakan).play()
        meledak = Ledakan(hit.rect.center, 'kecil') # Memanggil Class Ledakan
        all_sprites.add(meledak)
        newmusuh()
        if player.shield <= 0:
            mati_meledak = Ledakan(player.rect.center, 'player') # Jika meledak sampe mati
            all_sprites.add(mati_meledak)
            player.hide()
            player.lives -= 1
            player.shield = 100
            # player.kill() # Mati
            
    # Check if player menembak powerups
    hits = pygame.sprite.spritecollide(player, powerups, True, collided = None)
    for hit in hits:
        random.choice(suara_pickup).play()
        # if hit.type == 'shield_kecil':
        #     player.shield += random.randrange(5, 10) 
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.menambah_kekuatan()
        if hit.type == 'lives':
            if player.lives < 3:
                player.lives += 1
            
        # # Huruf Hijaiyah akan membuat player mendapatkan powerup
        # if hit.type == 'qalqalah':
        #     player.menambah_kekuatan()
            
    # if player mati dan meledak
    if player.lives == 0 and not mati_meledak.alive():
        # running = False # Game akan berhenti
        game_over = True # Diganti jadi game over karena untuk menambah fitur game over
        
    
    # Check if player menembak Huruf Hijaiyah
    hits = pygame.sprite.spritecollide(player, huruf_hijaiyah, True, collided = None)        
    for hit in hits:
        random.choice(suara_pickup).play()
        score += 1000
        
        
        
    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # Flip display
    pygame.display.flip()
    
pygame.quit() 
