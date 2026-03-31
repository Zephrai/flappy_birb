import pygame, sys
import math
from random import randint, choice
from Scripts.player import Player
from Scripts.pipe import Pipe, create_pipes
from Scripts.cloud import Cloud

import os, sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Flappy Birb')
        self.WIDTH = 800 
        self.HEIGHT = 800
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.Clock()
        
        try:
            self.player_img = pygame.transform.scale(pygame.image.load(resource_path('./data/assets/birb.png')).convert_alpha(), (75, 50))
            self.pipe_img = pygame.image.load(resource_path('./data/assets/pipe.png')).convert_alpha()
            self.cloud_img = pygame.image.load(resource_path('./data/assets/cloud.png')).convert_alpha()
            icon_surf = pygame.image.load(resource_path('./data/birb.ico')).convert_alpha()
            pygame.display.set_icon(icon_surf)
            self.player_img.set_colorkey((255, 255, 255))
            self.pipe_img.set_colorkey((255, 255, 255))
            self.cloud_img.set_colorkey((255, 255, 255))

            # sounds
            self.flap_sound = pygame.Sound(resource_path('./data/sounds/whoosh.wav'))
            self.hit_sound = pygame.Sound(resource_path('./data/sounds/hitsound.wav'))
            self.counter_sound = pygame.Sound(resource_path('./data/sounds/coin.wav'))
            self.flap_sound.set_volume(1.0)
            self.hit_sound.set_volume(0.20)
            self.counter_sound.set_volume(0.12)
        except Exception as e:
            self.player_img = None
            self.pipe_img = None
            self.cloud_img = None
            print('failed to load assets', e)

        self.player = Player(self, self.player_img)
        self.pipes: list[Pipe] = []
        self.clouds: list[Cloud] = []
        for _ in range(20):
            self.clouds.append(Cloud(self, self.cloud_img))
        
        def sort_by_z(cloud):
            return cloud.z
        self.clouds.sort(reverse=True, key=sort_by_z)
        self.cooldown = 100
        self.score = 0
        self.font = pygame.font.Font(size=80)
        self.game_over = False
        self.entities = [*self.clouds, *self.pipes]
    
    def death_screen(self):
        while not self.player.alive:
            self.screen.fill((20, 100, 140))
            for cloud in self.clouds:
                cloud.render()
            for entity in self.entities:
                entity.vel_x = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.alive = True

            self.player.render()
            for pipe in self.pipes:
                pipe.render()
            self.font.set_point_size(79)
            shadow = self.font.render(str(self.score), antialias=False, color=(0, 0, 0))
            self.font.set_point_size(75)
            text = self.font.render(str(self.score), antialias=False, color=(255, 255, 255))
           
            self.screen.blit(shadow, (self.WIDTH / 2 + 1, 50))
            self.screen.blit(text, (self.WIDTH / 2, 52))

    def reset(self):
        self.player = Player(self, self.player_img)
        self.clouds.clear()
        self.pipes.clear()
        self.entities.clear()
        for _ in range(20):
            self.clouds.append(Cloud(self, self.cloud_img))
        def sort_by_z(cloud):
            return cloud.z
        self.clouds.sort(reverse=True, key=sort_by_z)
        self.score = 0
        # flush the clock so delta time is reset
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            pygame.display.set_caption(f'{self.clock.get_fps():.1f}')
            dt = self.clock.get_time()
            self.screen.fill((20, 100, 140))
            for cloud in self.clouds:
                cloud.update()
                cloud.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.flap_sound.play()
                        self.player.vel_y -= 25
                        self.player.time = 0

            self.player.update(dt)
            self.player.render()

            create_pipes(self)
            for pipe in self.pipes:
                pipe.update()
                pipe.render()

            self.font.set_point_size(79)
            shadow = self.font.render(str(self.score), antialias=False, color=(0, 0, 0))
            self.font.set_point_size(75)
            text = self.font.render(str(self.score), antialias=False, color=(255, 255, 255))
           
            self.screen.blit(shadow, (self.WIDTH / 2 + 1, 50))
            self.screen.blit(text, (self.WIDTH / 2, 52))

            if self.player.alive == False:
                print(f'\033[36mYou died, final score:\033[0m \033[32m{self.score}\033[0m')
                self.death_screen()
                self.reset()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()