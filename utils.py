import random
from pygame.image import load
from pygame.math import Vector2
from pygame import Color

def loadSprite(name, with_alpha=True):
    path = f"Assets/Sprites/{name}.png"
    loadedSprite = load(path)

    if with_alpha:
        return loadedSprite.convert_alpha()
    else:
        return loadedSprite.convert()

def getRandomPosition(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height())
    )

def getRandomVelocity(minSpeed, maxSpeed):
    speed = random.randint(minSpeed, maxSpeed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def wrapPosition(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def printText(surface, text, font, color = Color("tomato")):
    textSurface = font.render(text, True, color)

    rect = textSurface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(textSurface, rect)
