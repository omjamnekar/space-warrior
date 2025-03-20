import pygame
import random
from game.assets import SPACE_DEFAULT, Assets, background
from game.settings import WIDTH, HEIGHT
from game.entities.stars import Star

# Colors
HEADING_COLOR = (22, 138, 173)
SUBHEADING_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
BOTTOM_TEXT_COLOR = (255, 255, 255)

Assets.load_fonts()
heading_font = Assets.TITLE_FONT
subheading_font = Assets.SUBHEADING_FONT
bottom_font = Assets.PRESS_START_FONT

# Initialize pygame mixer for sound effects and music


def render_text_with_shadow(text, font, color, shadow_offset=(3, 3)):
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, SHADOW_COLOR)
    return text_surface, shadow_surface, shadow_offset


class HomeScreen:
    def __init__(self, window):
        self.window = window    
        self.bg = pygame.transform.scale(background, (WIDTH, HEIGHT))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.bg.blit(overlay, (0, 0))
        pygame.mixer.init()

        # Load background music (replace with your file path)
        pygame.mixer.music.load('assets/sound/theme-space/hero.mp3')


        self.heading_text, self.heading_shadow, offset_h = render_text_with_shadow("SPACE WARRIOR", heading_font, HEADING_COLOR)
        self.subheading_text, self.subheading_shadow, offset_s = render_text_with_shadow("ADVENTURE TO REACH HOME", subheading_font, SUBHEADING_COLOR)
        self.bottom_text = bottom_font.render("Press ENTER to start", True, BOTTOM_TEXT_COLOR)

        self.heading_rect = self.heading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        self.subheading_rect = self.subheading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        self.bottom_rect = self.bottom_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        self.offset_h = offset_h
        self.offset_s = offset_s

        self.stars = [Star() for _ in range(100)]

        # Play background music with full volume
      

    def show(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(1.0)  # Ensure full volume
        pygame.mixer.music.play(loops=-1, start=0.0)  # Loops indefinitely
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Gradually lower the volume and stop the music in 1.5 seconds
                        for volume in range(10, -1, -1):  # Gradually reduce volume
                            pygame.mixer.music.set_volume(volume / 10)
                            pygame.time.delay(150)  # Delay to simulate gradual volume down
                        
                        pygame.mixer.music.fadeout(1500)  # Fade out over 1.5 seconds
                        pygame.mixer.music.stop()
                        SPACE_DEFAULT.play()
                        SPACE_DEFAULT.set_volume(1) 
                        return
            self.window.blit(self.bg, (0, 0))
            for star in self.stars:
                star.move()
                star.draw(self.window)
            self.window.blit(self.heading_shadow, self.heading_rect.move(self.offset_h))
            self.window.blit(self.heading_text, self.heading_rect)
            self.window.blit(self.subheading_shadow, self.subheading_rect.move(self.offset_s))
            self.window.blit(self.subheading_text, self.subheading_rect)
            self.window.blit(self.bottom_text, self.bottom_rect)
            pygame.display.update()
