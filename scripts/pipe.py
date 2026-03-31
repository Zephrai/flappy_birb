
import pygame
from random import randint

class Pipe:
    def __init__(self, game, img):
        self.game = game
        self.x = self.game.WIDTH
        self.y = 0
        self.size = [80, randint(-400, -10)]
        self.vel_x = -5
        self.pipe_gap = 70
        self.top_surf = pygame.transform.flip(img, False, True)
        self.bot_surf = img
        self.top_hitbox = None
        self.bot_hitbox = None
        
    def update(self):
        self.x += self.vel_x
        if self.x + self.size[0] <= 0:
            self.game.pipes.pop() 
        self._hitboxes()
    
    def _hitboxes(self):
        # Top pipe hitbox
        self.top_hitbox = self.top_surf.get_rect(topleft=(self.x, self.size[1]))
        # Bottom pipe hitbox
        self.bot_hitbox = self.bot_surf.get_rect(topleft=(self.x, self.game.HEIGHT + self.size[1] - self.pipe_gap))

    def render(self):
        # top pipe
        self.game.screen.blit(self.top_surf, (self.x, self.size[1], *self.top_surf.get_rect().size))
        # bottom pipe
        self.game.screen.blit(self.bot_surf, (self.x, self.game.HEIGHT + self.size[1] - self.pipe_gap, *self.top_surf.get_rect().size))

def create_pipes(game):
    game.cooldown -= 1
    if game.cooldown <= 0:
        game.pipes.reverse()
        game.pipes.append(Pipe(game, game.pipe_img))
        game.pipes.reverse()
        game.cooldown = 100
