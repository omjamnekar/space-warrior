import pygame

class WeaponHUD:
    def __init__(self,hud_image, weapons):

        self.hud_image = hud_image
        self.hud_rect = self.hud_image.get_rect()
        self.margin = 20
        self.weapons = weapons  # list of weapon icons (pygame surfaces)
        self.current_weapon_index = 0
        self.switch_cooldown = 300  # in milliseconds
        self.last_switch_time = 0
        
    def draw(self,screen):
        screen_width, screen_height = screen.get_size()
        
        # Position HUD in bottom-right corner
        hud_x = screen_width - self.hud_rect.width - self.margin 
        hud_y = screen_height - self.hud_rect.height - self.margin 
        screen.blit(self.hud_image, (hud_x, hud_y))

        # Draw current weapon icon inside that HUD shape
        current_weapon_icon = self.weapons[self.current_weapon_index]
        weapon_rect = current_weapon_icon.get_rect(center=self.hud_rect.center)
     

        # Offset the icon position according to HUD position
        weapon_rect.centerx = hud_x + self.hud_rect.width // 1.5
        weapon_rect.centery = hud_y + self.hud_rect.height // 1.5

        screen.blit(current_weapon_icon, weapon_rect)

    def switch_weapon(self, index):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_switch_time > self.switch_cooldown:
            if 0 <= index < len(self.weapons):
                self.current_weapon_index = index
                self.last_switch_time = current_time
