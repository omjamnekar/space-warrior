import pygame
from game.settings import HEIGHT,MAX_HP,MAX_XP
from game.assets import game_font

class StatusBars:
    def __init__(self, max_hp=MAX_HP, max_xp=MAX_XP):
        self.hp = max_hp
        self.max_hp = max_hp
        self.xp = 0
        self.max_xp = max_xp

    def increase_xp(self, amount):
        self.xp = min(self.xp + amount, self.max_xp)  # Prevent overfill
    
    
    def decrease_xp(self, amount):
        self.xp = min(self.xp - amount, self.max_xp)  # Prevent overfill

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)  # Prevent negative HP

    def reset(self):
        self.hp = self.max_hp
        self.xp = 0


    def get_xp(self):
        return self.xp

    def draw(self, window, width=200, height=15, margin=30, spacing=10, text_margin=5, font=game_font):
        # Position bars slightly left from the top-right corner
        x = window.get_width() - width - margin -40 # Shift bars left
        hp_bar_y = margin  # HP at the top
        xp_bar_y = hp_bar_y + height + spacing  # XP below HP

        # **HP Bar (Red)**
        hp_fill_width = (self.hp / self.max_hp) * width
        hp_fill_x = x + (width - hp_fill_width)  # Start filling from the right
        pygame.draw.rect(window, (200, 0, 0), (hp_fill_x, hp_bar_y, hp_fill_width, height))
        pygame.draw.rect(window, (255, 255, 255), (x, hp_bar_y, width, height), 3)

        # **XP Bar (Gradient) - Filling from Right to Left**
        xp_fill_width = int((self.xp / self.max_xp) * width)  # Convert to int for safety
        xp_fill_x = x + (width - xp_fill_width)  # Start fill from the right side



        if self.xp < 40:
            xp_color = (255, 50, 50)  # Red
        elif self.xp < 80:
            xp_color = (255, 165, 0)  # Orange
        else:
            xp_color = (255, 215, 0)  # Gold

        if xp_fill_width > 0:  # Prevent drawing if width is 0
            pygame.draw.rect(window, xp_color, (xp_fill_x, xp_bar_y, xp_fill_width, height))  # XP fill
        pygame.draw.rect(window, (255, 255, 255), (x, xp_bar_y, width, height), 3)  # XP border

        # **Labels on the right side of bars with extra margin**
        if font:
            hp_text = font.render("HP", True, (255, 255, 255))  # White HP text
            xp_text = font.render("XP", True, (255, 255, 255))  # White XP text
            shadow_hp = font.render("HP", True, (0, 0, 0))  # Black shadow for HP
            shadow_xp = font.render("XP", True, (0, 0, 0))  # Black shadow for XP

            text_x = x + width - text_margin +10 # Shift text slightly left

            window.blit(shadow_hp, (text_x + 2, hp_bar_y + 2))
            window.blit(hp_text, (text_x, hp_bar_y))  # HP label

            window.blit(shadow_xp, (text_x + 2, xp_bar_y + 2))
            window.blit(xp_text, (text_x, xp_bar_y))  # XP label
