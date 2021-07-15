from pygame.image import load
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import loadSprite, getRandomVelocity, wrapPosition

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blitPosition = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blitPosition)

    def move(self, surface):
        self.position = wrapPosition(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.113
    BULLET_SPEED = 3

    def __init__(self, position, createBulletCallback):
        self.createBulletCallback = createBulletCallback
        #Makes copy of the UP vector
        self.direction = Vector2(UP)

        super().__init__(position, loadSprite("Spaceship"), Vector2(0))

    def accelerate(self):
        self.velocity += self.direction *self.ACCELERATION

    def rotate(self, clockwise = True):
            sign = 1 if clockwise else -1
            angle = self.MANEUVERABILITY * sign
            self.direction.rotate_ip(angle)

    def draw(self, surface):
            angle = self.direction.angle_to(UP)
            rotatedSurface = rotozoom(self.sprite, angle, 1.0)
            rotated_surface_size = Vector2(rotatedSurface.get_size())
            blitPosition = self.position - rotated_surface_size * .5
            surface.blit(rotatedSurface, blitPosition)
    
    def shoot(self):
        bulletVelocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bulletVelocity)
        self.createBulletCallback(bullet)

class Asteroid(GameObject):
    def __init__(self, position, createAsteroidCallback, size = 3):
        self.createAsteroidCallback = createAsteroidCallback
        self.size = size

        sizeToScale = {
            3: 1, 
            2: .75, 
            1: .5}

        scale = sizeToScale[size]
        sprite = rotozoom(loadSprite("Asteroid"), 0, scale)

        super().__init__(position, sprite, getRandomVelocity(1, 3))
    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(self.position, self.createAsteroidCallback, self.size - 1)
                self.createAsteroidCallback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, loadSprite("Bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
