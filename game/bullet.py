import pygame
from game.settings import BULLET_SPEED, HEIGHT, WIDTH  # ✅ Ensure WIDTH is imported

import pygame
from game.assets import  laser_img,plasma_frame
from game.settings import BULLET_SPEED, HEIGHT, WIDTH  


laser_sound = pygame.mixer.Sound("assets/sound/leaser/leaser.mp3")  
bullet_sound = pygame.mixer.Sound("assets/sound/leaser/bullet.wav")  


bullet_sound.set_volume(0.5) 
laser_sound.set_volume(0.7)  

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10 

        self.image = laser_img
        self.image = pygame.transform.scale(self.image, (20, 20))

        self.rect = self.image.get_rect(center=(self.x, self.y))
        bullet_sound.play()

    def move(self):
        self.y -= self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def off_screen(self):
        return self.y < 0 




class LeaserBullet:
    def __init__(self, x, y):
        self.frames = plasma_frame 
        self.speed = 15
        self.animation_index = 0
        self.animation_speed = 5
        self.animation_counter = 0
        self.rect = self.frames[0].get_rect(center=(x, y))
        laser_sound.play()  

    def move(self):
        self.rect.y -= self.speed
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.frames)

    def draw(self, window):
        current_frame = self.frames[self.animation_index]
        window.blit(current_frame, self.rect.topleft)

    def off_screen(self):
        return self.rect.bottom < 0