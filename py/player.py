import pygame
from bullet import Bullet

class Player:
    def __init__(self, x, y, image, bullet_image, screen, windowWidth, delay):
        self.x = x
        self.y = y
        self.image = image
        self.bullet_image = bullet_image
        self.screen = screen
        self.windowWidth = windowWidth
        self.delay = delay
        self.bullet_count = 0
        self.last_bullet_time = 0

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.x > 0:
            self.x -= 3

    def move_right(self):
        if self.x < self.windowWidth - self.image.get_width():
            self.x += 3

    def fire_bullet(self, bullets):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_bullet_time > self.delay * 1000 and self.bullet_count > 0:
            self.last_bullet_time = current_time
            self.bullet_count -= 1
            bullets.append(Bullet(self.x, self.y, self.screen))
