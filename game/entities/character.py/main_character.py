import pygame 
import sys
import random 

from  assets import load_assets, WIDTH,HEIGHT,icon_image, hud_image, hand_icon, gun_icon, knife_icon
from systems.inventory import InventoryUI
from game.utils.data import items_data
from utils.heathbar import HealthBar
from utils.HUD import WeaponHUD

        

    


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_animations, idle_animations, jump_animation, gun_image):
        super().__init__()
        self.x, self.y = x, y
        self.walk_animations = walk_animations
        self.idle_animations = idle_animations
        self.direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 120
        self.idle_animation_speed = 300
        self.speed = 1.9
        self.image = self.idle_animations[self.direction][0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.is_moving = False
        self.is_jumping = False
        self.jump_frame = 0
        self.jump_timer = 0
        self.ground_y = y
        self.jump_animations = jump_animation
        self.jump_animatian_speed = 200
        self.jump_progress = 0.0
        self.jump_duration = 600
        self.jump_height = 20
        self.gun_image = gun_image
        self.health_bar = HealthBar(WIDTH - 30, 30, 100, 50, icon_image)
        self.weapon_hud = WeaponHUD(hud_image, [hand_icon, gun_icon, knife_icon])

        self.show_gun = False



    def update(self, keys, dt):
        moved = False
        move_x = 0
        move_y = 0
        if keys[pygame.K_q]:
            self.show_gun = not self.show_gun  # toggle instantly


        # Jump initiation
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.jump_frame = 0
            self.jump_timer = 0
            self.jump_progress = 0.0
            self.ground_y = self.y

        # Handle input for movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -self.speed
            self.direction = "left"
            moved = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = self.speed
            self.direction = "right"
            moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = self.speed
            self.direction = "down"
            moved = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -self.speed
            self.direction = "up"
            moved = True

        # In your draw loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.weapon_hud.switch_weapon(0)
                elif event.key == pygame.K_2:
                    self.weapon_hud.switch_weapon(1)
                elif event.key == pygame.K_3:
                    self.weapon_hud.switch_weapon(2)

        # Jump motion
        if self.is_jumping:
            self.jump_timer += dt
            self.jump_progress += dt / self.jump_duration

            if self.jump_progress > 1.0:
                self.jump_progress = 0
                self.is_jumping = False
                self.y = self.ground_y  # Reset to ground

            jump_offset = -self.jump_height * (4 * self.jump_progress * (1 - self.jump_progress))
            self.y = self.ground_y + jump_offset

            # You can still move horizontally and vertically during jump
            self.x += move_x
            self.y += move_y

            # Jump animation
            if self.jump_timer > self.jump_animatian_speed:
                self.jump_timer = 0
                self.jump_frame = (self.jump_frame + 1) % len(self.jump_animations[self.direction])
            self.image = self.jump_animations[self.direction][self.jump_frame]

        else:
            if moved:
                if not self.is_moving:
                    self.current_frame = 0
                    self.animation_timer = 0
                self.is_moving = True

                self.x += move_x
                self.y += move_y

                self.animation_timer += dt
                if self.animation_timer > self.animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.walk_animations[self.direction])
                self.image = self.walk_animations[self.direction][self.current_frame]

            else:
                if self.is_moving:
                    self.current_frame = 0
                    self.animation_timer = 0
                self.is_moving = False

                self.animation_timer += dt
                if self.animation_timer > self.idle_animation_speed:
                    self.animation_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.idle_animations[self.direction])
                self.image = self.idle_animations[self.direction][self.current_frame]

        self.rect.center = (self.x, self.y)




    def draw(self, screen, offset_x, offset_y):
        player_x = self.rect.x - offset_x
        player_y = self.rect.y - offset_y

        gun_pos = [player_x, player_y]
        flip_gun = False
        rotate_angle = 0
     
        self.weapon_hud.draw(screen)
        if self.direction == "right":
            gun_pos[0] += 15
            gun_pos[1] += 32
        elif self.direction == "left":
            gun_pos[0] += 6
            gun_pos[1] += 32
            flip_gun = True
        elif self.direction == "up":
            # Draw player first (no gun visible when facing up)
            screen.blit(self.image, (player_x, player_y))
            self.health_bar.draw(screen)
            return
        elif self.direction == "down":
            gun_pos[0] += 25
            gun_pos[1] += 20
            rotate_angle = -80
        
        # self.health_bar.draw(screen)

        # Flip and rotate gun image
        gun_image = pygame.transform.flip(self.gun_image, flip_gun, False)
        gun_image = pygame.transform.rotate(gun_image, rotate_angle)

        # If facing down, draw gun first (behind player)
       
       
        if self.direction == "down" and self.show_gun:
            screen.blit(gun_image, gun_pos)
            screen.blit(self.image, (player_x, player_y))
        else:
            # Otherwise, draw player first, then gun (in front)
            screen.blit(self.image, (player_x, player_y))
            if self.show_gun:
                # Add rotation effect if switching
              if self.show_gun:
                  screen.blit(gun_image, gun_pos)



def create_parallax_layer(width, height, star_count=200):
    parallax = pygame.Surface((width, height))
    parallax.fill((5, 5, 30))
    for _ in range(star_count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        pygame.draw.circle(parallax, (255, 255, 255), (x, y), 1)
    return parallax

def main():
    pygame.init()
    screen_width, screen_height = WIDTH, HEIGHT
    zoom_factor = 2

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Zoomed Scrolling World")
    pygame.display.set_icon(icon_image)

    zoom_surface = pygame.Surface((screen_width // zoom_factor, screen_height // zoom_factor))

    clock = pygame.time.Clock()

    walk_animations, idle_animations, jump_animations, background, gun_image = load_assets()
    bg_width, bg_height = background.get_size()
    parallax = create_parallax_layer(bg_width, bg_height, star_count=300)

    player = Player(bg_width // 2, bg_height // 2, walk_animations, idle_animations, jump_animations, gun_image)
    all_sprites = pygame.sprite.Group(player)
    
    inventory_ui = InventoryUI()

    inventory_open = False

    running = True
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()

        screen.fill((30, 30, 30))
       

        for event in pygame.event.get():
            inventory_ui.handle_event(event)
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                inventory_open = not inventory_open
                print(f"Inventory Open: {inventory_open}")

        if not inventory_open:
            player.update(keys, dt)

        # ✅ Calculate offset once
        offset_x = player.rect.centerx - (zoom_surface.get_width() // 2)
        offset_y = player.rect.centery - (zoom_surface.get_height() // 2)

        offset_x = max(0, min(offset_x, bg_width - zoom_surface.get_width()))
        offset_y = max(0, min(offset_y, bg_height - zoom_surface.get_height()))

        # ✅ Draw world on zoom_surface
        zoom_surface.blit(parallax, (-offset_x, -offset_y))
        zoom_surface.blit(background, (-offset_x, -offset_y))
        player.draw(zoom_surface, offset_x, offset_y)

        # ✅ Scale and draw on screen
        zoomed = pygame.transform.scale(zoom_surface, (screen_width, screen_height))
        screen.blit(zoomed, (0, 0))

       
        player.health_bar.draw(screen)

        if inventory_open:
            # Darken the background when inventory is open
            dark_overlay = pygame.Surface((screen_width, screen_height))
            dark_overlay.set_alpha(150)  # Adjust transparency (0-255)
            dark_overlay.fill((0, 0, 0))  # Black overlay
            screen.blit(dark_overlay, (0, 0))
            
            inventory_ui.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()






if __name__ == "__main__":
    main()



