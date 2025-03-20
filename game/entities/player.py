import pygame
from game.settings import WIDTH, HEIGHT  

from game.entities.bullet import Bullet, LeaserBullet
from game.assets import SWITCH_WEAPON, ship_destroy_frame, ship_flight_frames, Assets ,SHIP_DESTROY   # ✅ Import flight animation

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100  
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, 80, 80)
        
        # More precise hitbox for collisions
        self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 20, self.rect.height - 20)
        # ✅ Load Ship Flight Animation
        self.ship_frames = [pygame.transform.scale(frame, (80, 80)) for frame in ship_flight_frames]
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100  # Change frame every 100ms

        # ✅ Load Ship Destroy Animation
        self.ship_destroy_frames = ship_destroy_frame
        self.ship_destroy_index = 0
        self.play_destroy_animation = False
        self.destroy_animation_start_time = 0
        self.is_destroyed = False

        # Bullets and shooting control
        self.bullets = []
        self.shoot_delay = 10
        self.shoot_timer = 0
        self.last_plasma_shot_time = 0
        self.plasma_shoot_cooldown = 150  # Plasma continuous shooting cooldown (ms)

        # Weapons
        self.weapon_types = ["laser", "plasma"]
        self.weapon_index = 0
        self.weapon_type = self.weapon_types[self.weapon_index]
        
        # Weapon switch message
        self.weapon_switch_message = ""
        self.weapon_switch_message_start_time = 0
        self.weapon_message_duration = 3000  

    def switch_weapon(self):
        """Switch between laser and plasma weapons."""
        SWITCH_WEAPON.play()
        self.weapon_index = (self.weapon_index + 1) % len(self.weapon_types)
        self.weapon_type = self.weapon_types[self.weapon_index]
        self.weapon_switch_message = f"Weapon switched to: {self.weapon_type}"
        self.weapon_switch_message_start_time = pygame.time.get_ticks()
        
    


    def draw_weapon_switch_message(self, window):
        """Display weapon switch message on the bottom right of the screen for at least 2 seconds."""
        if self.weapon_switch_message:
            elapsed_time = pygame.time.get_ticks() - self.weapon_switch_message_start_time
            if elapsed_time < self.weapon_message_duration:  # Show message for 2 seconds (2000 ms)
                font = Assets.PRESS_START_FONT  # Use predefined font
                text_surface = font.render(self.weapon_switch_message, True, (255, 255, 0))  # Yellow color
                
                # Calculate position for bottom-right corner
                x_position = WIDTH - text_surface.get_width() - 20  # 20px padding from right
                y_position = HEIGHT - text_surface.get_height() - 20  # 20px padding from bottom
                
                window.blit(text_surface, (x_position, y_position))  # Draw text
            else:
                self.weapon_switch_message = ""  # Clear message after timeout


    def update(self):
        """Update player state (timers, bullets, animation)."""
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        self.update_bullets()


    def draw(self, window, offset=(0, 0)):
        """Draw player ship with animations, bullets, and destruction effects."""
        offset_x, offset_y = offset
        now = pygame.time.get_ticks()

        if self.play_destroy_animation:
            SHIP_DESTROY.play()
            current_time = pygame.time.get_ticks()

            if current_time - self.destroy_animation_start_time > 50:  # 50ms per frame
                self.destroy_animation_start_time = current_time
                if self.ship_destroy_index < len(self.ship_destroy_frames) - 1:
                    self.ship_destroy_index += 1
                else:
                    self.play_destroy_animation = False  # Stop animation when last frame is reached
                    self.is_destroyed = True  # ✅ Mark player as destroyed

            # Render destroy animation frame with offset
            frame = self.ship_destroy_frames[self.ship_destroy_index]
            frame_rect = frame.get_rect(center=self.hitbox.center)
            window.blit(frame, (frame_rect.x + offset_x, frame_rect.y + offset_y))

        else:
            # 🚀 Handle Flight Animation
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.ship_frames)

            # Draw the player with offset
            window.blit(self.ship_frames[self.current_frame], (self.rect.x + offset_x, self.rect.y + offset_y))

        # 🔫 Draw Bullets with offset
        for bullet in self.bullets:
            bullet.draw(window, offset=(offset_x, offset_y))



    def shoot(self):
        """Shoot based on current weapon type."""
        if self.play_destroy_animation or self.is_destroyed:
            return
        if self.shoot_timer == 0:
            if self.weapon_type == "plasma":
                bullet = LeaserBullet(self.rect.centerx, self.rect.top)
                self.bullets.append(bullet)
                print("⚡ Plasma bullet fired!")
            elif self.weapon_type == "laser":
                bullet = Bullet(self.rect.centerx, self.rect.top)
                self.bullets.append(bullet)
                print("🔫 Laser bullet fired!")
            self.shoot_timer = self.shoot_delay

    def shoot_plasma_continuous(self):
        """Continuous plasma shooting with cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_plasma_shot_time > self.plasma_shoot_cooldown:
            self.shoot()
            self.last_plasma_shot_time = current_time

    def update_bullets(self):
        """Move and remove off-screen bullets."""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)

    def move(self, keys):
        """Move player based on WASD keys."""
        if self.play_destroy_animation or self.is_destroyed:
            return

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        self.hitbox.x = self.rect.x + 10
        self.hitbox.y = self.rect.y + 10

    def start_destroy_animation(self):
        """Trigger ship destroy animation at collision."""
        if not self.play_destroy_animation:
            self.play_destroy_animation = True
            self.ship_destroy_index = 0

 