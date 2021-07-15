import pygame
from pygame.constants import KEYDOWN

from utils import loadSprite, getRandomPosition, printText
from Models import Spaceship, Asteroid

class spaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800,600))
        self.background = loadSprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroid  = []
        self.bullet = []
        self.spaceship = Spaceship((400, 300), self.bullet.append)

        for _ in range(2):
            while True:
                position = getRandomPosition(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break
            
            self.asteroid.append(Asteroid(position, self.asteroid.append))

    def mainLoop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def getGameObjects(self):
        gameObjects = [*self.asteroid, *self.bullet]

        if self.spaceship:
            gameObjects.append(self.spaceship)

        return gameObjects

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Asteroids")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()


        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise = True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise = False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()

    def _process_game_logic(self):
        for gameObject in self.getGameObjects():
            gameObject.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroid:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "YOU LOSE!"
                    break

        for bullet in self.bullet[:]:
            for asteroid in self.asteroid[:]:
                if asteroid.collides_with(bullet):
                    self.asteroid.remove(asteroid)
                    self.bullet.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullet[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullet.remove(bullet)

        if not self.asteroid and self.spaceship:
            self.message = "YOU WIN!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for gameObject in self.getGameObjects():
            gameObject.draw(self.screen)

        if self.message:
            printText(self.screen, self.message, self.font)

        pygame.display.flip()
        self.clock.tick(144)