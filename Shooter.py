from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed  = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y <= win_height:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        global lost
        if self.rect.y <= win_height:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_height = 500
win_width = 700
window = display.set_mode((win_width,win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))

lost = 0
score = 0
goal = 10
max_lost = 10
life = 3

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))

player = Player('rocket.png', 5, win_height - 80, 80, 100, 4)
monster1 = Enemy('ufo2.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
monster2 = Enemy('ufo2.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
monster3 = Enemy('ufo2.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
monster4 = Enemy('ufo2.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
monster5 = Enemy('ufo2.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))

astro1 = Asteroid('asteroid.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
astro2 = Asteroid('asteroid.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))
astro3 = Asteroid('asteroid.png', randint(5, win_width - 5), 0, 80, 50, randint(2 , 5))

monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)

asteroids = sprite.Group()
asteroids.add(astro1)
asteroids.add(astro2)
asteroids.add(astro3)

bullets = sprite.Group()

img_bullet = "bullet.png"

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

game = True
finish = False

num_fire = 0
rel_time = False



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire<5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire = num_fire + 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
    
    if finish != True:
        window.blit(background, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        asteroids.draw(window)
        asteroids.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo2.png', randint(80, win_width - 80), -40, 80, 50, randint(2 , 5))
            monsters.add(monster)
            
        collides2 = sprite.spritecollide(player, monsters, False)
        for c in collides2:
            monster = Enemy('ufo2.png', randint(80, win_width - 80), -40, 80, 50, randint(2 , 5))
            monsters.add(monster)
        
        collides3 = sprite.spritecollide(player, asteroids, False)
        for c in collides3:
            astro = Asteroid('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(2 , 5))
            asteroids.add(astro)

        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1

        if life == 0 or lost > max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))

        display.update()
    
    time.delay(50)
