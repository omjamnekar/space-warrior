import pygame
import time
import random
from game.entities.meteor import Meteor
from game.settings import WIDTH, HEIGHT, FPS, FULLSCREEN
from game.assets import background,Assets, SPACE_DEFAULT ,fade_out_music
from game.systems.game_logic import Game
from game.senes.pause import PauseScreen
from game.systems.hexbar import StatusBars
from game.senes.home import HomeScreen
from game.ui.home.home import HomeInterface

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("SPACE WARRIOR")

# Darkened main background
darkened_background = pygame.Surface((WIDTH, HEIGHT))
darkened_background.blit(background, (0, 0))
darkened_background.set_alpha(180)




def main():
    """Main game loop"""
    pygame.init()
    global WIDTH, HEIGHT


    window_flags = pygame.RESIZABLE
    if FULLSCREEN:
        window_flags = pygame.FULLSCREEN
    window = pygame.display.set_mode((WIDTH, HEIGHT), window_flags)

    clock = pygame.time.Clock()

    home_screen = HomeScreen(window)
    start_screen = HomeInterface(window=window)
    home_screen.show()
    start_screen.show()
    # transition_to_main(window, home_screen)
    # transition_to_main(window,start_screen)
    status = StatusBars()
    game = Game(status=status, window=window)
    pause_screen = PauseScreen()
    running = True
    paused = False
    show_best_score = False
    # last_weapon_switch_time = 0
    # darkened_background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    while running:
        clock.tick(FPS)
        window.blit(background, (0, 0))
        events = pygame.event.get()  # Capture all events

        for event in events:

            if event.type == pygame.QUIT:
                game.save_best_score()
                running = False

            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Toggle fullscreen
                    if window.get_flags() & pygame.FULLSCREEN:
                        window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    else:
                        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                elif event.type == pygame.VIDEORESIZE:
                    WIDTH, HEIGHT = event.w, event.h
                    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                    darkened_background = pygame.transform.scale(background, (WIDTH, HEIGHT))

              
              
                if event.key == pygame.K_ESCAPE:
                    fade_in_pause_screen(window, pause_screen)  # Apply fade-in
                    pause_screen.toggle()
                    if(pause_screen.active):
                        SPACE_DEFAULT.set_volume(0.3)
                    else:
                        SPACE_DEFAULT.set_volume(1) 
                    

                if event.key == pygame.K_q:  
                    print("T key pressed!")  # Debuggings
                    game.player.switch_weapon() 
                
        
        if pause_screen.active:
            selected_option = pause_screen.update(events)  # Handle pause menu navigation

        
            if selected_option == "Resume":
                fade_out_music(SPACE_DEFAULT, 1.0) 
                pause_screen.toggle()  # Unpause
            elif selected_option == "Restart":
                fade_out_music(SPACE_DEFAULT, 0.0)
                SPACE_DEFAULT.stop()
                status.reset()
                game.restart(status)
                SPACE_DEFAULT.play()
                pause_screen.toggle()
            elif selected_option == "Home":
                fade_out_music(SPACE_DEFAULT, 0.0) 
                SPACE_DEFAULT.stop()
                home_screen.show()
                transition_to_main(window, home_screen)
                status.reset()
                game.restart(status)
                pause_screen.toggle()

            pause_screen.draw(window)  # Draw the pause menu
        else:
            SPACE_DEFAULT.set_volume(1)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and game.player.weapon_type == "plasma" and status.get_xp() > 0:
                game.player.shoot_plasma_continuous()
                status.decrease_xp(1)

            game.player.move(keys)
            game.player.update()

            if not game.game_over_screen:
                if random.randint(1, 50) == 1:
                    game.meteors.append(Meteor())
                game.update()
 

            game.draw(window)
            game.player.draw_weapon_switch_message(window)


            # Display Score
            score_text = Assets.PRESS_START_FONT.render(f"Score: {game.score}", True, (255, 255, 255))
            window.blit(score_text, (20, 20))


            if game.score >= game.best_score:
                game.best_score = game.score
                game.save_best_score()
                show_best_score = True

            if show_best_score:
                best_score_text = Assets.PRESS_START_FONT.render(f"Best Score: {game.best_score}", True, (255, 255, 0))
                best_score_x = (WIDTH - best_score_text.get_width()) // 2
                window.blit(best_score_text, (best_score_x, 20))

        pygame.display.update()

    pygame.quit()



def fade_in_pause_screen(window, pause_screen):
    """Fade in the pause screen when the game is paused"""
   
    alpha = 0  # Start fully transparent
    fade_speed = 10  # Adjust for smooth fading

    fade_surface = pygame.Surface((WIDTH, HEIGHT))  # Overlay
    fade_surface.fill((0, 0, 0))  # Black background

    while alpha < 180: 
        clock.tick(60)
        fade_surface.set_alpha(alpha)  # Increase opacity
        window.blit(darkened_background, (0, 0))  # Keep the game background
        window.blit(fade_surface, (0, 0)) 
        pause_screen.draw(window) 
        alpha += fade_speed  
        pygame.display.update()


def transition_to_main(window, home_screen):
    
    SPACE_DEFAULT.play(loops=-1)
    
    """Fade out the home screen while revealing the main background"""
    alpha = 255  
    fade_speed = 5  

    fade_surface = home_screen.bg.copy() 

    while alpha > 0:
        clock.tick(60)
        window.blit(background, (0, 0))  # Show main game background
        fade_surface.set_alpha(alpha)  # Reduce opacity
        window.blit(fade_surface, (0, 0))  # Draw fading home screen
        alpha -= fade_speed  # Decrease opacity
        pygame.display.update()




