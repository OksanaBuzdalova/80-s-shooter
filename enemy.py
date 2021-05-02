from random import randint
from base import GameSprite


class Enemy(GameSprite):
    def update(self, game):
        width, height = self.window.get_size()
        if self.rect.y <= height:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
            game.lost += 1


class Asteroid(GameSprite):
    def update(self):
        width, height = self.window.get_size()
        if self.rect.y <= height:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
