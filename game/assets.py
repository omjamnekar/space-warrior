import os
import pygame

# Initialize pygame and its modules
pygame.init()  # Ensure pygame is initialized
pygame.font.init()  # Ensure the font module is initialized

from game.settings import WIDTH, HEIGHT

# Load assets
background = pygame.image.load("assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Darken background
dark_overlay = pygame.Surface((WIDTH, HEIGHT))  
dark_overlay.fill((0, 0, 0))  # Black overlay  
dark_overlay.set_alpha(100)  # Adjust darkness (increase for more darkness)
background.blit(dark_overlay, (0, 0))  # Apply the darkening effect

# ship_img = pygame.image.load("assets/ship_1.png")
laser_img = pygame.image.load("assets/laser.png")
plasma_frame = plasma_frames = [
    pygame.transform.scale(
        pygame.transform.rotate(pygame.image.load(f"assets/plasma/tile{i:03d}.png"), 90),
        (20, 30)
    )
    for i in range(5)
]

meteor_img = pygame.image.load("assets/astroid/meteor.png")

# Scale assets
# ship_img = pygame.transform.scale(ship_img, (50, 50))
laser_img = pygame.transform.scale(laser_img, (10, 20))
meteor_img = pygame.transform.scale(meteor_img, (40, 40))



font_path = "assets/font/PressStart2P.ttf"

# Check if the font file exists
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

# Load fonts
game_font = pygame.font.Font(font_path, 14)
game_font_large = pygame.font.Font(font_path, 18)

# Load explosion animation frames
import pygame

# Load explosion animation frames
explosion_frames = [ pygame.transform.scale(pygame.image.load(f"assets/destory/tile{i:03d}.png"),(320, 320)
    ) for i in range(8)]
ship_destroy_index = 0
play_destroy_animation = False
destroy_animation_time = 0

ship_destroy_frames = ship_destroy_frame = [
    pygame.transform.scale(
        pygame.image.load(f"assets/ship-destroy/tile{i:03d}.png"),
         (220, 220)
    )
    for i in range(47)
]
ship_flight_frames = [
    pygame.image.load(f"assets/spaceship/tile{i:03}.png") for i in range(16)
]

pygame.font.init()


class Assets:
    @staticmethod
    def load_fonts():
        Assets.TITLE_FONT = pygame.font.Font("assets/font/KnightWarrior-w16n8.otf", 120)
        Assets.SUBHEADING_FONT = pygame.font.Font("assets/font/VeniteAdoremus-rgRBA.ttf", 35)
        Assets.PRESS_START_FONT = pygame.font.Font("assets/font/PressStart2P.ttf", 15)
        Assets.ROBUSSTART2P = pygame.font.Font("assets/font/Robus-BWqOd.otf", 120)

# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("assets", "sound", "explosions", "explosion-small.mp3"))
EXPLOSION_SOUND.set_volume(0.5)  # Adjust volume if neede



# Load sound effect for home screen
background_music = pygame.mixer.Sound('assets/sound/theme-space/final-show.mp3')



# Load sounds
SPACE_DEFAULT = pygame.mixer.Sound(os.path.join("assets","sound","theme-space","space-default.mp3"))
SPACE_DEFAULT.set_volume(1)  # Adjust volume if neede
SELECT_OPTION = pygame.mixer.Sound(os.path.join("assets", "sound", "selection", "select.wav"))
SELECT_OPTION.set_volume(2)  # Adjust volume if needed


SHIP_DESTROY =  pygame.mixer.Sound(os.path.join("assets", "sound", "explosions", "space-ship.mp3"))
SHIP_DESTROY.set_volume(1) 


def fade_out_music(music, target_volume, fade_speed=0.05):
    """Gradually fade out the music to the target volume"""
    current_volume = music.get_volume()
    
    # Fade out until the target volume is reached
    while current_volume > target_volume:
        current_volume -= fade_speed  # Decrease volume gradually
        if current_volume < target_volume:
            current_volume = target_volume  # Ensure it doesn't go below target
        music.set_volume(current_volume)  # Apply the new volume
        pygame.time.wait(50)  # Wait a bit before adjusting again to create smooth effect

ROCK_COLLIED=  pygame.mixer.Sound(os.path.join("assets", "sound", "collied", "rock-broke.mp3"))
ROCK_COLLIED.set_volume(1) 


SWITCH_WEAPON=  pygame.mixer.Sound(os.path.join("assets", "sound", "leaser", "reload.mp3"))
SWITCH_WEAPON.set_volume(1) 


GAME_WIDTH, GAME_HEIGHT = 1280, 720
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

game_surface.blit(background, (0, 0))
# draw player, asteroids, etc. onto game_surface
