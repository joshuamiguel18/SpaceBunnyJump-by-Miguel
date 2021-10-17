import pygame
import os
import random


# Initialize game
pygame.init()
pygame.mixer.init()
# Game dimension
WIDTH = 400
HEIGHT = 600
# Framerate
clock = pygame.time.Clock()
FPS = 60
# Game environment
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Bunny Jump')
# Game variable
GRAVITY = 0.5
MAX_PLATFORM = 10
SCROLL = 10
scroll_bg = 0
game_over = False
score = 0 
WHITE = ((255,255,255))
high_score = 0
fade = 0
# Font 
game_font = pygame.font.SysFont("Times New Roman", 25)
small_font = pygame.font.SysFont("Times New Roman", 20)

# load Sound
defeat = pygame.mixer.Sound("Videogame Lose Sound Effect HD _ No Copyright.wav")

# Load images
bg = pygame.image.load(os.path.join('assets','space.gif'))
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT)).convert_alpha()
bunny_image = pygame.transform.scale(pygame.image.load(os.path.join('assets','cute-rabbit-astronaut-carrot-rocket-260nw-1862661304-removebg-preview.png')),(50,50)).convert_alpha()
platform_image = pygame.image.load(os.path.join('assets','platform.jpg')).convert_alpha()

if os.path.exists('highscore.txt'):
    with open('highscore.txt', 'r') as file:
        high_score = int(file.read())


class Player():
    def __init__(self, x, y):
        self.image = bunny_image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel_y = 0
    def movement(self):
        scroll = 0
        dy = 0
        global score
        button = pygame.key.get_pressed()
        if button[pygame.K_a] and self.rect.left - 10 > 0:
            self.rect.x -= 10
        if button[pygame.K_d] and self.rect.right < WIDTH - 10:
            self.rect.x += 10
        self.vel_y += GRAVITY
        dy += self.vel_y
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, 40,50):
                if self.rect.bottom < platform.rect.centery:                   
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = -15
        if self.rect.top <= SCROLL:
            if self.vel_y < 0:
                scroll = -dy
                score += 1
        self.rect.y += dy + scroll
        return scroll
    def draw(self):
        screen.blit(self.image, self.rect)
        

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image,(width,8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > HEIGHT:
            self.kill()
platform_group = pygame.sprite.Group()

# Create Platform
platform = Platform(WIDTH//2-50, 500, 100)
platform_group.add(platform)

def draw_bg_move(scroll_bg):
    screen.blit(bg, (0,scroll_bg))
    screen.blit(bg, (0,-600+scroll_bg))
def draw_text(text, font, x, y, color):
    text = font.render(text,1,color)
    screen.blit(text,(x,y))   

# Entities
player = Player(WIDTH//2,HEIGHT-200)
pygame.mixer.music.load("Original Tetris theme (Tetris Soundtrack).wav")
pygame.mixer.music.play(-1)


# Main loop
run = True
while run:
    # Clock Frame
    clock.tick(FPS)
    
    if game_over == False:
        # BG music
        
        # Movement
        scroll = player.movement()
        scroll_bg += scroll
        if scroll_bg > 600:
            scroll_bg = 0
        if len(platform_group) < MAX_PLATFORM:
            py = platform.rect.y - random.randint(50,120)
            pw = random.randint(30,60)
            px = random.randint(0,WIDTH-pw)
            platform = Platform(px,py,pw)
            
            platform_group.add(platform)
        
        draw_bg_move(scroll_bg)
        
        # Update of platform
        platform_group.update(scroll)
        # Draw entities
        player.draw()
        platform_group.draw(screen)
        draw_text(f'Score: {int(score)}', game_font,20,20,WHITE)
        if player.rect.top > HEIGHT:
            game_over = True
    else:
        
        pygame.mixer.music.stop()
        if fade < WIDTH:
            fade += 10
            pygame.draw.rect(screen,(0,0,0),(0, 0,fade,HEIGHT//2))
            pygame.draw.rect(screen,(0,0,0),(WIDTH - fade, HEIGHT//2,WIDTH, HEIGHT//2))
            pygame.mixer.Sound.play(defeat)   
        else:
            if score > high_score:
                high_score = score
                with open('highscore.txt', 'w') as file:
                    file.write(str(high_score))
            draw_text('You fell :<', game_font, WIDTH//2-50, 250, WHITE)
            draw_text('Press space to retry :>', game_font,WIDTH//2-100,300,WHITE)
            draw_text(f'Final Score: {int(score)}', game_font,WIDTH//2-73,275,WHITE)
            draw_text(f'High Score: {int(high_score)}', game_font,WIDTH//2-78,405,WHITE)
            draw_text('by Miguel Toribio :-)',small_font,WIDTH//2-85,525,WHITE)
            draw_text('Space Bunny Jump',small_font,WIDTH//2-75,500,WHITE)
            button = pygame.key.get_pressed()
            if button[pygame.K_SPACE]:
                pygame.mixer.music.load("Original Tetris theme (Tetris Soundtrack).wav")
                pygame.mixer.music.play(-1)
                defeat.stop()
                fade = 0
                game_over = False
                score = 0
                player.rect.center = (WIDTH//2,HEIGHT-150)
                platform_group.empty()
                platform = Platform(WIDTH//2-50, 500, 100)
                platform_group.add(platform)
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            if score > high_score:
                high_score = score
                with open('highscore.txt', 'w') as file:
                    file.write(str(high_score))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    pygame.display.update()
pygame.quit()