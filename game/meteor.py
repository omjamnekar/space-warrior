import pygame
import random
from game.assets import meteor_img, explosion_frames ,EXPLOSION_SOUND 
from game.settings import WIDTH, HEIGHT, METEOR_MIN_SPEED, METEOR_MAX_SPEED


class Meteor:
    def __init__(self):
        # ✅ Create irregular sizes by random scaling
        scale_factor = random.uniform(0.5, 1.5)  # Irregular scale from 50% to 150%
        self.image = pygame.transform.scale(
            meteor_img,
            (int(meteor_img.get_width() * scale_factor), int(meteor_img.get_height() * scale_factor))
        )

        self.x = random.randint(0, WIDTH - self.image.get_width())
        self.y = -40  # Start above the screen
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(
            self.rect.x + self.width * 0.15, 
            self.rect.y + self.height * 0.15, 
            self.width * 0.7, 
            self.height * 0.7
        )  

        self.speed = random.randint(METEOR_MIN_SPEED, METEOR_MAX_SPEED)

        self.exploding = False
        self.explosion_index = 0  
        self.scaled_explosions = [
            pygame.transform.scale(img, (int(self.width * 1.8), int(self.height * 1.8)))
            for img in explosion_frames
        ]

    def move(self):
        if not self.exploding:
            self.rect.y += self.speed
            self.hitbox.y += self.speed  

    def off_screen(self):
        return self.rect.y > HEIGHT        

    def destroy(self):
         if not self.exploding:
            EXPLOSION_SOUND.play()  # Play explosion sound
            self.exploding = True
            self.explosion_index = 0  

    def draw(self, window):
        if self.exploding:
            if self.explosion_index < len(self.scaled_explosions):
                explosion_img = self.scaled_explosions[self.explosion_index]
                explosion_x = self.rect.centerx - explosion_img.get_width() // 1
                explosion_y = self.rect.centery - explosion_img.get_height() // 1
                window.blit(explosion_img, (explosion_x, explosion_y))
                self.explosion_index += 1  
                return True  
            else:
                return False  
        else:
            window.blit(self.image, (self.rect.x, self.rect.y))
            return True  