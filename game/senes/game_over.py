import pygame
import time
import math
import random

from game.settings import WIDTH, HEIGHT
from game.assets import Assets

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, int(self.y)), self.size)

class GameOverScreen:
    def __init__(self):
        self.fade_alpha = 0  # Fade-in effect reset
        self.pulse_timer = 0  # Timer for blinking "Press R"
        self.show_text = True  # Toggle blinking text
        self.restart_triggered = False  # Ensures restart happens once
        self.stars = [Star() for _ in range(100)]  # Generate stars for the background

    def show_game_over_screen(self, window, score, best_score):
        clock = pygame.time.Clock()
        game_font_large = Assets.TITLE_FONT
        game_font = Assets.PRESS_START_FONT
        start_time = time.time()

        explosion_sound = pygame.mixer.Sound("assets/sound/game_over/game_over.mp3")
        explosion_sound.play()  # Play sound when Game Over appears
        
        self.fade_alpha = 0  # Reset fade effect
        self.pulse_timer = 0  # Reset blinking timer
        self.restart_triggered = False  # Ensure restart is handled properly
        
        while True:
            clock.tick(60)
            elapsed_time = time.time() - start_time

            self.pulse_timer += 1
            if self.pulse_timer % 30 == 0:
                self.show_text = not self.show_text  # Toggle blinking effect

            # Update stars
            for star in self.stars:
                star.move()

            window.fill((0, 0, 0))  # Clear the screen
            for star in self.stars:
                star.draw(window)  # Draw stars

            if self.fade_alpha < 255:
                self.fade_alpha += 3  # Slower fade-in for a smooth effect

            # Ensure alpha doesn't exceed 255
            self.fade_alpha = min(self.fade_alpha, 255)

            # Apply the fade overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255 - self.fade_alpha))  # Reverse fade effect (from dark to visible)
            window.blit(overlay, (0, 0))

            game_over_y = HEIGHT // 4  # Position for "GAME OVER"
            text_spacing = 70  # Space between text elements
            restart_y = game_over_y + text_spacing * 5

            # Shadow effect for "GAME OVER"
            shadow_offset = 3
            shadow_game_over = game_font_large.render("GAME OVER", True, (50, 0, 0))
            window.blit(shadow_game_over, (WIDTH // 2 - shadow_game_over.get_width() // 2 + shadow_offset, game_over_y + shadow_offset))

            # Glowing Red "GAME OVER"
            glow_intensity = min(255, 100 + int(80 * abs(math.sin(elapsed_time * 2))))
            game_over_text = game_font_large.render("GAME OVER", True, (255, glow_intensity, glow_intensity))
            window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, game_over_y))

            # Score & Best Score
            score_y = game_over_y + text_spacing * 3
            best_score_y = game_over_y + text_spacing * 4

            score_text = game_font.render(f"Score: {score}", True, (255, 200, 200))
            best_score_text = game_font.render(f"Best Score: {best_score}", True, (255, 100, 100))

            window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, score_y))
            window.blit(best_score_text, (WIDTH // 2 - best_score_text.get_width() // 2, best_score_y))

            # Sci-fi style "Press R to Restart" button
            if self.show_text:
                restart_text = game_font.render("Press R to Restart", True, (255, 255, 255))
                pygame.draw.rect(window, (150, 0, 0), (WIDTH // 2 - restart_text.get_width() // 2 - 10, restart_y - 5, restart_text.get_width() + 20, restart_text.get_height() + 10), border_radius=5)
                window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, restart_y))

            pygame.display.update()

            # Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not self.restart_triggered:
                        self.restart_triggered = True  # Prevent multiple restarts
                        self.fade_alpha = 0  # Reset fade effect for next game
                        for i in range(10, -1, -1):  # Gradually reduce volume over 2 seconds
                            pygame.mixer.Sound.set_volume(explosion_sound, i / 20)
                            pygame.time.delay(50)  # Delay for 100ms
                        pygame.mixer.stop()  # Stop all currently playing sounds
                        return   # Exit function, restart game