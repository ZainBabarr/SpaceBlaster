# Add the moveVertically method in the Platform class
class Platform:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction = 1

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

    def moveSideways(self, windowWidth, speed, range):
        self.x += speed * self.direction
        if self.x < range or self.x + self.image.get_width() > windowWidth-range:
            self.direction *= -1

    def moveVertically(self, windowHeight, speed, range):
        self.y += speed * self.direction
        if self.y < 0 or self.y + self.image.get_height() > windowHeight:
            self.direction *= -1