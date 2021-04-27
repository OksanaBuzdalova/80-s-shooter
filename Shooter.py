from typing import NoReturn
from pygame import *
from random import randint
from time import time as timer
from constants import *
from enemy import Enemy, Asteroid
from player import Player


class Game:
    def __init__(self, width=WINDOW_WIDTH,
                 height=WINDOW_HEIGHT,
                 monsters_count=5,
                 asteroids_count=3,
                 goal=10,
                 max_lost=10,
                 life_count=3):
        self.width = width
        self.height = height

        # Display
        self.window = display.set_mode((width, height))
        display.set_caption("Шутер")
        self.background = transform.scale(image.load(BACKGROUND_IMG_PATH), (width, height))

        # Fonts and final messages
        font.init()
        self.final_message_font = font.SysFont('Arial', 36)
        self.params_font = font.SysFont('Arial', 36)
        self.win = self.final_message_font.render('YOU WIN', True, (255, 255, 255))
        self.lose = self.final_message_font.render('YOU LOSE', True, (180, 0, 0))

        # Sprites
        self.player = Player(self.window, PLAYER_IMG_PATH, 5, height - 80, 80, 100, 4)
        self.monsters = sprite.Group(
            *(Enemy(self.window, MONSTER_IMG_PATH, randint(5, width - 5), 0, 80, 50, randint(2, 5)) for _ in
              range(monsters_count)))
        self.asteroids = sprite.Group(
            *(Asteroid(self.window, ASTEROID_IMG_PATH, randint(5, width - 5), 0, 80, 50, randint(2, 5)) for _ in
              range(asteroids_count)))

        # Music
        mixer.init()
        mixer.music.load(SPACE_MUSIC)
        mixer.music.play()
        self.fire_sound = mixer.Sound(FIRE_MUSIC)

        # Base game vars
        self.game = True
        self.rel_time = False
        self.finish = False
        self.goal = goal
        self.max_lost = max_lost
        self.life_count = life_count
        self.num_fire = 0
        self.score = 0
        self.lost = 0

    def update(self):
        self.player.reset()
        self.player.update()

        self.monsters.draw(self.window)
        self.monsters.update(self)

        self.asteroids.draw(self.window)
        self.asteroids.update()

    def handle_events(self):
        for e in event.get():
            if e.type == QUIT:
                self.game = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if self.num_fire < 5 and not self.rel_time:
                        self.fire_sound.play()
                        self.player.fire()
                        self.num_fire += 1
                    if self.num_fire >= 5 and not self.rel_time:
                        self.rel_time = True
                        self.last_time = timer()

    def run(self) -> NoReturn:
        while self.game:
            self.handle_events()
            if self.finish:
                time.delay(50)
                continue
            self.window.blit(self.background, (0, 0))
            self.update()
            if self.rel_time:
                now_time = timer()

                if now_time - self.last_time < 3:
                    reload = self.params_font.render('Wait, reload...', True, (150, 0, 0))
                    self.window.blit(reload, (260, 460))
                else:
                    self.num_fire = 0
                    self.rel_time = False

            for _ in sprite.groupcollide(self.monsters, self.player.bullets, True, True):
                self.score += 1
                self.monsters.add(Enemy(self.window, MONSTER_IMG_PATH, randint(80, self.width - 80), -40, 80, 50, randint(2, 5)))

            for _ in sprite.spritecollide(self.player, self.monsters, False):
                self.monsters.add(Enemy(self.window, MONSTER_IMG_PATH, randint(80, self.width - 80), -40, 80, 50, randint(2, 5)))

            for _ in sprite.spritecollide(self.player, self.asteroids, False):
                self.asteroids.add(Asteroid(self.window, ASTEROID_IMG_PATH, randint(80, self.width - 80), -40, 80, 50, randint(2, 5)))

            if sprite.spritecollide(self.player, self.monsters, False) or sprite.spritecollide(self.player, self.asteroids, False):
                sprite.spritecollide(self.player, self.monsters, True)
                sprite.spritecollide(self.player, self.asteroids, True)
                self.life_count -= 1

            if not self.life_count or self.lost > self.max_lost:
                self.finish = True
                self.window.blit(self.lose, (200, 200))

            if self.score >= self.goal:
                self.finish = True
                self.window.blit(self.win, (200, 200))

            text = self.params_font.render("Счет: " + str(self.score), True, (255, 255, 255))
            self.window.blit(text, (10, 20))

            text_lose = self.params_font.render("Пропущено: " + str(self.lost), True, (255, 255, 255))
            self.window.blit(text_lose, (10, 50))

            text_life = self.params_font.render(str(self.life_count), True, (0, 150, 0))
            self.window.blit(text_life, (650, 10))

            display.update()
            time.delay(50)


if __name__ == '__main__':
    Game().run()
