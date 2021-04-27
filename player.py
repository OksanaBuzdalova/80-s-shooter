from pygame import key, K_LEFT, K_RIGHT
from pygame.sprite import Group

from base import GameSprite
from constants import BULLET_IMG_PATH


class Player(GameSprite):
    def __init__(self, window, img_path, sprite_x, sprite_y, size_x, size_y, player_speed):
        super().__init__(window, img_path, sprite_x, sprite_y, size_x, size_y, player_speed)
        self.size_x = size_x
        self.bullets = Group()

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < self.window.get_size()[0] - self.size_x:
            self.rect.x += self.speed

        # Update bullets
        self.bullets.draw(self.window)
        self.bullets.update()

    def fire(self):
        bullet = Bullet(self.window, BULLET_IMG_PATH, self.rect.centerx, self.rect.top, 15, 20, -15)
        self.bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
