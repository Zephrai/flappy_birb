import pygame
class Player:
    def __init__(self, game, img: pygame.Surface):
        self.game = game
        self.x = 200
        self.y = 200
        self.vel_y = 0
        self.gravity = 0.02
        self.time = 1
        self.size = 30
        self.surf = img
        self.rotated = self.surf
        self.angle = 0
        self.alive = True

    def update(self, dt):
        self._collisions()
        self.vel_y += self.gravity * dt
        self.vel_y = min(20, self.vel_y)
        self.vel_y = max(-10, self.vel_y)
        self._rotate()
        self.y += self.vel_y
        self.time += dt

    def _add_score(self):
        self.game.score += 1
        self.game.counter_sound.play()

    def _collisions(self):
        hitbox = self.rotated.get_rect(topleft=(self.x, self.y))

        if hitbox.top >= self.game.HEIGHT or hitbox.bottom < 0:
            self.alive = False
        for pipe in self.game.pipes:
            if hitbox.colliderect(pipe.top_hitbox) or hitbox.colliderect(pipe.bot_hitbox):
                self.game.hit_sound.play()
                self.alive = False
            if self.x == pipe.x + pipe.size[0]:
                self._add_score()

    def _rotate(self):
        if self.vel_y >= 0:
            self.angle -= 2.0
            self.angle = max(self.angle, -25)
        if self.vel_y < 0:
            self.angle = 20
        
        self.rotated = pygame.transform.rotate(self.surf, self.angle)
        self.rotated_rect = self.rotated.get_rect(center=(self.x, self.y))
      

    def render(self):
        self.game.screen.blit(self.rotated, (self.x, self.y))
