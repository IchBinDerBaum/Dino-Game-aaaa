import pygame
import random
import os
from sys import exit
dir = os.path.dirname("trex_images/")

bgmusic = os.path.join(dir, "background_music.ogg")
gameovermusic = os.path.join(dir, "GAMEOVER.wav")
jump3sound = os.path.join(dir, "jump_sound3.wav")
jump4sound = os.path.join(dir, "jump_sound4.wav")
dinopic = os.path.join(dir, "dino.png")
dino1pic = os.path.join(dir, "dino1.png")
dino2pic = os.path.join(dir, "dino2.png")
groundpic = os.path.join(dir, "ground.png")
cactus1pic = os.path.join(dir, "cactus1.png")
cactus2pic = os.path.join(dir, "cactus2.png")
cactus3pic = os.path.join(dir, "cactus3.png")
bird1pic = os.path.join(dir, "bird1.png")
bird2pic = os.path.join(dir, "bird2.png")

pygame.init()
HEIGHT = 300
WIDTH = 900
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (115, 215, 255)
GRAY = (80, 80, 80)
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("t-rex jump")
clock = pygame.time.Clock()
score = 0
trigger = False
pygame.mixer.init()
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.load(bgmusic)
pygame.mixer.music.play(-1)
game_over_sound = pygame.mixer.Sound(gameovermusic)

# fontname = pygame.font.match_font("ARCADECLASSIC.TTF")


jump3 = pygame.mixer.Sound(jump3sound)
jump4 = pygame.mixer.Sound(jump4sound)
jump_sounds = (jump3, jump4)

aaa = os.path.join(dir, "ARCADECLASSIC.TTF")


def gettext(message, color, x, y, size):
    font = pygame.font.Font(aaa, size)
    text = font.render(message, True, color)
    place = text.get_rect(center=(x, y))
    sc.blit(text, place)


def gameover():
    game_over_sound.set_volume(0.05)
    game_over_sound.play(0)
    pygame.mixer.music.stop()
    sc.fill(RED)
    gettext("GAME OVER", LIGHTBLUE, WIDTH // 2, HEIGHT // 2, 96)
    gettext(f"{score}", WHITE, WIDTH // 2, HEIGHT // 2 + 60, 50)
    pygame.display.flip()
    playing = True
    while playing:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                playing = False
                pygame.quit()
                exit()


class Trex(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(dinopic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (88, 94))
        self.rect = self.image.get_rect()
        self.image1 = pygame.image.load(dino1pic).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (88, 94))
        self.image2 = pygame.image.load(dino2pic).convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (88, 94))
        self.images = [self.image, self.image1, self.image2]

        self.rect.x = 10
        self.height = HEIGHT - 10 - self.rect.height
        self.rect.y = self.height
        self.jumping = False
        self.jumpspeed = 13
        self.runcounter = 0

    def draw(self):
        sc.blit(self.image, self.rect)

    def update(self):
        if keys[pygame.K_SPACE] and self.rect.y == self.height:
            js = random.choice(jump_sounds)
            js.set_volume(0.01)
            js.play(0)
            self.jumping = True
        if self.jumping:
            self.rect.y -= self.jumpspeed
            self.jumpspeed -= 0.6
            self.image = self.images[0]
            self.runcounter = 0
        else:
            if self.runcounter < 5:
                self.image = self.images[1]
            else:
                self.image = self.images[2]
            if self.runcounter > 10:
                self.runcounter = 0
            self.runcounter += 1
        if self.rect.y > self.height:
            self.rect.y = self.height
            self.jumping = False
            self.jumpspeed = 13


class Ground:
    def __init__(self):
        self.image = pygame.image.load(groundpic).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT
        self.image1 = pygame.image.load(groundpic).convert_alpha()
        self.rect1 = self.image.get_rect()
        self.rect1.bottom = HEIGHT

        self.rect1.left = self.rect.right
        self.speed = 6

    def draw(self):
        sc.blit(self.image, self.rect)
        sc.blit(self.image1, self.rect1)

    def update(self):
        self.rect.x -= self.speed
        self.rect1.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = self.rect1.right
        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image1 = pygame.image.load(cactus1pic).convert_alpha()
        self.image2 = pygame.image.load(cactus2pic).convert_alpha()
        self.image3 = pygame.image.load(cactus3pic).convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (40, 70))
        self.image2 = pygame.transform.scale(self.image2, (40, 70))
        self.image3 = pygame.transform.scale(self.image3, (40, 70))
        self.image = random.choice((self.image1, self.image2, self.image3))
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - 10
        self.rect.x = WIDTH + self.rect.width + random.randrange(10, 50)
        self.speed = 6

    def draw(self):
        sc.blit(self.image, self.rect)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class Pterodactyl(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 6
        self.image = pygame.image.load(bird1pic).convert_alpha()
        self.image1 = pygame.image.load(bird2pic).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 50))
        self.image1 = pygame.transform.scale(self.image1, (70, 50))
        self.rect = self.image.get_rect()
        self.images = [self.image, self.image1]
        self.rect.y = HEIGHT - random.choice([80, 200])
        self.run_counter = 0
        self.rect.x = WIDTH + self.rect.width + random.randrange(40, 100)

    def draw(self):
        sc.blit(self.image, self.rect)

    def update(self):
        self.rect.x -= self.speed

        if self.run_counter < 15:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        if self.run_counter > 30:
            self.run_counter = 0
        self.run_counter += 1

        if self.rect.right < 0:
            self.kill()


pterodactylPhaseTrigger = False
maxCacti = 8
pterodactylCounter = 0

cacti = pygame.sprite.Group()
add_cacti = pygame.USEREVENT + 1
pygame.time.set_timer(add_cacti, random.randrange(800, 1500))
add_pterodactyl = pygame.USEREVENT + 2
pygame.time.set_timer(add_pterodactyl, random.randrange(1000, 1500))
pterodactiles = pygame.sprite.Group()
ground = Ground()
trex = Trex()
allsprites = pygame.sprite.Group()
allsprites.add(trex)
play = True
music_trigger = True
while play:
    clock.tick(FPS)

    if random.randrange(1, 10000) > 9992 and score > 1000:
        pterodactylPhaseTrigger = True
        maxCacti = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

        if event.type == add_cacti and len(cacti) < maxCacti and len(pterodactiles) == 0:
            cactus = Cactus()
            allsprites.add(cactus)
            cacti.add(cactus)
            pygame.time.set_timer(add_cacti, random.randrange(800, 1500))

        if event.type == add_pterodactyl and len(pterodactiles) < 5 and pterodactylPhaseTrigger:
            pterodactyl = Pterodactyl()
            allsprites.add(pterodactyl)
            pterodactiles.add(pterodactyl)
            pterodactylCounter += 1
            pygame.time.set_timer(add_pterodactyl, random.randrange(1000, 1500))
            if pterodactylCounter > 10:
                pterodactylPhaseTrigger = False
                maxCacti = 8
                pterodactylCounter = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                trigger = True
            if event.key == pygame.K_RETURN:
                if music_trigger:
                    pygame.mixer.music.pause()
                    music_trigger = False
                if not music_trigger:
                    pygame.mixer.music.unpause()
                    music_trigger = True

    keys = pygame.key.get_pressed()
    sc.fill(LIGHTBLUE)
    allsprites.draw(sc)
    ground.draw()
    pygame.mixer.music.pause()
    if trigger:
        pygame.mixer.music.unpause()
        sc.fill(LIGHTBLUE)
        ground.update()
        ground.draw()
        allsprites.draw(sc)
        allsprites.update()
        score += 1
        gettext(f"{score}", GRAY, WIDTH - 40, 30, 30)

    if pygame.sprite.spritecollideany(trex, cacti):
        gameover()
    if pygame.sprite.spritecollideany(trex, pterodactiles):
        gameover()
    pygame.display.flip()
pygame.quit()

