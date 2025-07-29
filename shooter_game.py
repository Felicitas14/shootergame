from pygame import *
from time import time as timer
from random import randint

lost = 0
score = 0
rel_time = False
num_fire = 0
win_widht = 700
win_height = 500
jendela = display.set_mode((win_widht, win_height))
display.set_caption('pygame window')
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

rocket = 'rocket.png'
enemy = 'ufo.png'
background = transform.scale(image.load('galaxy.jpg'), (win_widht, win_height))
finish = False
run = True


font.init()
font1 = font.SysFont('Arial', 80) 
font2 = font.SysFont('Arial', 36) 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),( size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        jendela.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 50:
            self.rect.x += self.speed
    
    def fire(self):
        bullets = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullet.add(bullets)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

monster = sprite.Group()
for i in range (1, 6):
    monsters = Enemy(enemy, randint(80, win_widht - 80), -40, 80, 50 , randint(1, 3))
    monster.add(monsters)

pemain = Player(rocket, 100, 400, 50, 50, 10)
bullet = sprite.Group()
asteroids = sprite.Group()
for i in range (1, 3):
    asteroid = Enemy('asteroid.png', randint(80, win_widht - 80), -40, 80, 50 , randint(1, 3))
    asteroids.add(asteroid)
       
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1 
                    fire_sound.play()
                    pemain.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
        

    if not finish:
        jendela.blit(background,(0, 0))
        collides = sprite.groupcollide(monster, bullet, True, True)
        if score >= 10:
            finish = True
            menang = font1.render('YOU WIN!', True ,(0, 255, 0))
            jendela.blit(menang, (200, 200))
        if lost >= 3 or sprite.spritecollide(pemain, monster, False):
            finish = True
            kalah = font1.render('YOU LOSE!', True ,(255, 0, 0))
            jendela.blit(kalah, (200, 200))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                jendela.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        for c in collides:
            score += 1
            monsters = Enemy(enemy, randint(80, win_widht - 80), -40, 80, 50, randint(1, 3))
            monster.add(monsters)
        collide = sprite.spritecollide(pemain, monster, True)
        bullet.update()
        bullet.draw(jendela)
        text_lose = font2.render('Missed:' + str(lost), 1, (255, 255, 255))
        jendela.blit(text_lose, (10, 50))
        text_score = font2.render('skor:' + str(score), 1, (255, 255, 255))
        jendela.blit(text_score, (20, 100))
        asteroids.update()
        asteroids.draw(jendela)
        monster.update()
        monster.draw(jendela)
        pemain.update()
        pemain.reset()
        display.update()
    clock.tick(FPS)
        