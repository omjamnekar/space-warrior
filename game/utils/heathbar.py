import pygame
from assets import WIDTH
import math


class HealthBar:
    def __init__(self, x, y, full_health, full_xp, icon_image):
        self.x, self.y = x, y
        self.full_health = full_health
        self.full_xp = full_xp
        self.current_health = full_health
        self.current_xp = full_xp

        self.icon_image = pygame.transform.scale(icon_image, (60, 60))  
        self.health_color = (0, 255, 0) 
        self.xp_color = (0, 150, 255)  
        self.border_color = (255, 255, 255)  

        self.bar_width = 250  
        self.health_height = 15  
        self.xp_height = 8  
        self.spacing = 2  

    def draw(self, screen):
        # Set the right margin offset
        right_margin = 20
        bar_x = WIDTH - self.bar_width - right_margin-30
        bar_y = self.y + 10  
        icon_x = WIDTH - 60 - right_margin  # Place icon just at the right edge

        health_ratio = self.current_health / self.full_health
        current_health_width = int(self.bar_width * health_ratio)

        xp_ratio = self.current_xp / self.full_xp
        current_xp_width = int(self.bar_width * xp_ratio)

        # Angled health bar
        cut_angle_rad = math.radians(50)
        offset_health = math.tan(cut_angle_rad) * self.health_height
        offset_xp = math.tan(cut_angle_rad) * self.xp_height

        health_bar_points = [
            (bar_x + offset_health, bar_y),
            (bar_x + current_health_width, bar_y),
            (bar_x + current_health_width, bar_y + self.health_height),
            (bar_x, bar_y + self.health_height)
        ]
        pygame.draw.polygon(screen, self.health_color, health_bar_points)
        pygame.draw.polygon(screen, self.border_color, health_bar_points, 1)

        xp_bar_y = bar_y + self.health_height + self.spacing
        xp_bar_points = [
            (bar_x + offset_xp, xp_bar_y),
            (bar_x + current_xp_width, xp_bar_y),
            (bar_x + current_xp_width, xp_bar_y + self.xp_height),
            (bar_x, xp_bar_y + self.xp_height)
        ]
        pygame.draw.polygon(screen, self.xp_color, xp_bar_points)
        pygame.draw.polygon(screen, self.border_color, xp_bar_points, 1)

        # Draw icon on the right
        screen.blit(self.icon_image, (icon_x, self.y - 10))

