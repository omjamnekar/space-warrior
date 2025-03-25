import pygame
from game.settings import HEIGHT, MAX_HP, MAX_XP
from game.assets import game_font

class StatusBars:
    def __init__(self, max_hp=MAX_HP, max_xp=MAX_XP):
        self.hp = max_hp
        self.max_hp = max_hp
        self.xp = 0
        self.max_xp = max_xp

    def increase_xp(self, amount):
        self.xp = min(self.xp + amount, self.max_xp)
    
    def decrease_xp(self, amount):
        self.xp = max(0, self.xp - amount)  # also prevent going negative

    def decrease_hp(self, amount):
        self.hp = max(0, self.hp - amount)

    def reset(self):
        self.hp = self.max_hp
        self.xp = 0

    def get_xp(self):
        return self.xp

    def draw(self, window, player, width=200, height=15, margin=30, spacing=10, text_margin=5, font=game_font):
        x = window.get_width() - width - margin - 40
        hp_bar_y = margin
        xp_bar_y = hp_bar_y + height + spacing

        # HP BAR
        hp_fill_width = (self.hp / self.max_hp) * width
        hp_fill_x = x + (width - hp_fill_width)
        pygame.draw.rect(window, (200, 0, 0), (hp_fill_x, hp_bar_y, hp_fill_width, height))
        pygame.draw.rect(window, (255, 255, 255), (x, hp_bar_y, width, height), 3)

        # XP BAR
        xp_fill_width = int((self.xp / self.max_xp) * width)
        xp_fill_x = x + (width - xp_fill_width)
        xp_color = (255, 50, 50) if self.xp < 40 else (255, 165, 0) if self.xp < 80 else (255, 215, 0)

        if xp_fill_width > 0:
            pygame.draw.rect(window, xp_color, (xp_fill_x, xp_bar_y, xp_fill_width, height))
        pygame.draw.rect(window, (255, 255, 255), (x, xp_bar_y, width, height), 3)

        # Labels
        if font:
            shadow_hp = font.render("HP", True, (0, 0, 0))
            hp_text = font.render("HP", True, (255, 255, 255))
            shadow_xp = font.render("XP", True, (0, 0, 0))
            xp_text = font.render("XP", True, (255, 255, 255))

            text_x = x + width - text_margin + 10
            window.blit(shadow_hp, (text_x + 2, hp_bar_y + 2))
            window.blit(hp_text, (text_x, hp_bar_y))
            window.blit(shadow_xp, (text_x + 2, xp_bar_y + 2))
            window.blit(xp_text, (text_x, xp_bar_y))

        # ✅ Draw bullet ammo info BELOW XP bar
        bullet_text = font.render(f"Ammo: {player.current_bullets} / {player.bullet_storage}", True, (255, 255, 255))
        shadow_bullet = font.render(f"Ammo: {player.current_bullets} / {player.bullet_storage}", True, (0, 0, 0))
        bullet_y = xp_bar_y + height + spacing + 5
        window.blit(shadow_bullet, (x + 2, bullet_y + 2))
        window.blit(bullet_text, (x, bullet_y))
