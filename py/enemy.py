import math, time

#enemy.py
class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 5

    def update_position(self):
        self.y += (math.sin(time.time() * 5) * 0.5)

    def move_sideways(self, screen_width, speed, barrier):
        self.x += self.direction * speed
        if self.x <= barrier or self.x + self.image.get_width() >= screen_width-barrier:
            self.direction *= -1

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def check_collision(self, bullet_x, bullet_y):
        return (bullet_y - 3 <= int(self.y) + 40 <= bullet_y + 3) and (self.x - 5 <= bullet_x <= self.x + 5)