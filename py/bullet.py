import pygame

class Bullet:
    def __init__(self, x, y, dis):
        self.x = x + 35  # Adjusting the x-coordinate to be the center of the character
        self.y = y
        self.dis = dis
        self.speed = 5
        self.radius = 6
        self.color = (255, 255, 0)  # Yellow color for the bullet
        self.border_color = (0, 0, 0)  # Black color for the border
        self.direction = 1

    def move(self):
        self.y -= self.direction * self.speed

    def setDirection(self, direction):
        self.direction = direction

    def draw(self):
        # Draw the bullet
        pygame.draw.circle(self.dis, self.color, (self.x, self.y), self.radius)
        # Draw bullet border
        pygame.draw.circle(self.dis, self.border_color, (self.x, self.y), self.radius + 3, 3)

    def is_off_screen(self):
        return self.y < 0 or self.y > 600 or self.x < 0 or self.x > 450  # Check for off-screen status

    def check_enemy_collision(self, enemy):
        bullet_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
        return bullet_rect.colliderect(enemy_rect)

    def check_platform_collision(self, platform):
        bullet_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        platform_rect = pygame.Rect(platform.x, platform.y, platform.image.get_width(), platform.image.get_height())
        return bullet_rect.colliderect(platform_rect)
