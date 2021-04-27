from pygame import sprite, transform, image


class GameSprite(sprite.Sprite):
    def __init__(self, window, img_path, sprite_x, sprite_y, size_x, size_y, player_speed):
        super().__init__()
        self.window = window
        self.image = transform.scale(image.load(img_path), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))
