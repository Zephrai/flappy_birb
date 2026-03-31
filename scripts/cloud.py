import pygame
from random import randint

class Cloud:
    def __init__(self, game, img: pygame.Surface):
        self.game = game
        self.x = randint(0, self.game.WIDTH)
        self.y = randint(0, self.game.HEIGHT)
        self.z = randint(1, 3)
        self.surf = img
        self.rect = self.surf.get_rect().size
        self.size = [*self.rect]
        self.vel_x = 0
        self._parallax()
    
    def update(self):
        self.x += self.vel_x
        if self.x + self.size[0] <= 0:
            self.x = self.game.WIDTH
        
    def _parallax(self):
        if self.z == 1:
            self.surf = pygame.transform.scale2x(self.surf)
            self.vel_x = -3
        elif self.z == 2:
            self.surf = pygame.transform.scale_by(self.surf, 0.8)
            self.vel_x = -2
        elif self.z == 3:
            self.surf = pygame.transform.scale_by(self.surf, 0.4)
            self.vel_x = -1

        self.rect = self.surf.get_rect().size
        self.size = [*self.rect]

    def render(self):
        self.game.screen.blit(self.surf, (self.x, self.y, *self.surf.get_rect().size))
