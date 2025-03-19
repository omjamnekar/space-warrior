import pygame
from game.hexbar import StatusBars
from game.player import Player
from game.meteor import Meteor
from game.settings import WIDTH, HEIGHT
from game.assets import game_font, SPACE_DEFAULT,ROCK_COLLIED ,Assets
from game.game_over import GameOverScreen
from game.home import HomeScreen

import random

class Game:
    def __init__(self, status: StatusBars, window):
        self.hex_bar = status
        self.window = window
        self.player = Player()
        self.best_score = self.load_best_score()
        self.meteors = []
        self.running = True
        self.game_over_screen = False
        self.score = 0
        self.spawn_timer = 0
        self.spawn_delay = 30  # Frames until next meteor spawn
        self.game_ov_instance =GameOverScreen()
        self.running = False
        self.home= HomeScreen(window=self.window) 
        self.fonts =Assets.load_fonts()
    
        self.flash_alpha = 0  # Opacity for red flash
        self.shake_duration = 0  # Shake effect duration
        self.shake_intensity = 0  # How much the screen moves 
     
    def load_best_score(self):
        try:
            with open("best_score.txt", "r") as file:
                best_score = int(file.read().strip())
                print(f"📂 Loaded Best Score: {best_score}")
                return best_score
        except (FileNotFoundError, ValueError):
            return 0



    def save_best_score(self):
        try:
            with open("best_score.txt", "w") as file:
                file.write(str(self.best_score))
                file.flush()
        except Exception as e:
            print(f"Error Saving Best Score: {e}")

    def spawn_meteor(self):
        if self.spawn_timer <= 0:
            meteor_x = random.randint(0, WIDTH - 80)
            self.meteors.append(Meteor())
            self.spawn_timer = self.spawn_delay
        else:
            self.spawn_timer -= 1



    def check_collisions(self):
        bullets_to_remove = set()

        for meteor in self.meteors[:]:
            if meteor.off_screen():
                self.meteors.remove(meteor)
                continue

            if self.player.hitbox.colliderect(meteor.hitbox) and not meteor.exploding and  not  self.player.is_destroyed:
                 self.hex_bar.decrease_hp(30)
                 meteor.destroy()
                 if(self.hex_bar.hp> 10):
                    ROCK_COLLIED.play()
                 if self.hex_bar.hp<=0:
    
                    self.player.start_destroy_animation()
                    return 
            
            if self.player.play_destroy_animation and self.player.ship_destroy_index >= len(self.player.ship_destroy_frames):
                self.player.is_destroyed = True 
             
            if self.player.is_destroyed:
                self.game_over()  
                
            

            for bullet in self.player.bullets[:]:
                if bullet.rect.colliderect(meteor.hitbox) and not meteor.exploding:
                    bullets_to_remove.add(bullet)
                    meteor.destroy()
                    self.score += 10
                    self.hex_bar.increase_xp(10)

                    if self.score > self.best_score:
                        self.best_score = self.score
                        self.save_best_score()
                        print(f"🎯 New Best Score: {self.best_score}")

        self.player.bullets = [bullet for bullet in self.player.bullets if bullet not in bullets_to_remove]
        self.meteors = [meteor for meteor in self.meteors if meteor.exploding or meteor.rect.y < HEIGHT]

    def game_over(self):
        
        SPACE_DEFAULT.set_volume(0.1)
        SPACE_DEFAULT.stop()
        
        self.save_best_score()
        self.game_over_screen = True
        self.running = False  # Stop the game loop
          

    def restart(self, originstatus: StatusBars):
        self.__init__(status=originstatus, window=self.window)
        
        self.game_over_screen = False  
        self.running = True

    def update(self):
        if self.game_over_screen:
            return  # Stop updates when game is over

        self.spawn_meteor()
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.update()

        if keys[pygame.K_SPACE]:
            if self.player.weapon_type == "laser":
                self.player.shoot()
            elif self.player.weapon_type == "plasma" and self.hex_bar.xp>0:
                self.player.shoot_plasma_continuous()
            if self.player.weapon_type == "plasma" and self.hex_bar.xp== 0:
                self.xp_empty()


        for meteor in self.meteors:
            meteor.move()

        self.check_collisions()
        self.meteors = [meteor for meteor in self.meteors if meteor.draw(self.window)]


    def xp_empty(self):
        if self.hex_bar.xp==0:
            font = Assets.PRESS_START_FONT  # Use a default font with size 36
            text = font.render("XP is empty", True, (255, 0, 0))  # Red color
            text_rect = text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 50))  # Position near the bottom-right, slightly upwards
            self.window.blit(text, text_rect)
           

    def draw(self, window):
       

        self.player.draw(window)
              
        if self.game_over_screen and not self.running:  
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            for alpha in range(0, 255, 5):  # Gradually increase alpha for fade-in effect
                fade_surface.set_alpha(alpha)
                self.window.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)  # Delay to control the speed of the fade-in transition
           
            self.game_ov_instance.show_game_over_screen(window=self.window, best_score=self.best_score, score=self.score)
            self.running = False  
            self.game_over_screen = False  
            self.hex_bar.reset()
            self.restart(self.hex_bar)
            
            home_screen = HomeScreen(window)  
            home_screen.show() 
            return  # Stop further rendering
        for meteor in self.meteors[:]:
            if not meteor.draw(window):
                self.meteors.remove(meteor)

        self.hex_bar.draw(window)



    def show_score(self, window):
        score_text = game_font.render(f"Score: {self.score}", True, (255, 255, 255))
        best_score_text = game_font.render(f"Best: {self.best_score}", True, (255, 215, 0))
        window.blit(score_text, (10, 10))
        window.blit(best_score_text, (10, 40))

    
        