import os
import pygame

# Initialize pygame and its modules
pygame.init()  # Ensure pygame is initialized
pygame.font.init()  # Ensure the font module is initialized

from game.settings import WIDTH, HEIGHT

# Load assets
background = pygame.image.load("./assets/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Darken background
dark_overlay = pygame.Surface((WIDTH, HEIGHT))  
dark_overlay.fill((0, 0, 0))  # Black overlay  
dark_overlay.set_alpha(100)  # Adjust darkness (increase for more darkness)
background.blit(dark_overlay, (0, 0))  # Apply the darkening effect

# ship_img = pygame.image.load("assets/ship_1.png")
laser_img = pygame.image.load("./assets/laser.png")
plasma_frame = plasma_frames = [
    pygame.transform.scale(
        pygame.transform.rotate(pygame.image.load(f"./assets/plasma/tile{i:03d}.png"), 90),
        (20, 30)
    )
    for i in range(5)
]

meteor_img = pygame.image.load("./assets/astroid/meteor.png")

# Scale assets
# ship_img = pygame.transform.scale(ship_img, (50, 50))
laser_img = pygame.transform.scale(laser_img, (10, 20))
meteor_img = pygame.transform.scale(meteor_img, (40, 40))



font_path = "./assets/font/PressStart2P.ttf"

# Check if the font file exists
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")

# Load fonts
game_font = pygame.font.Font(font_path, 14)
game_font_large = pygame.font.Font(font_path, 18)

# Load explosion animation frames
import pygame

# Load explosion animation frames
explosion_frames = [ pygame.transform.scale(pygame.image.load(f"./assets/destory/tile{i:03d}.png"),(320, 320)
    ) for i in range(8)]
ship_destroy_index = 0
play_destroy_animation = False
destroy_animation_time = 0

ship_destroy_frames = ship_destroy_frame = [
    pygame.transform.scale(
        pygame.image.load(f"./assets/ship-destroy/tile{i:03d}.png"),
         (220, 220)
    )
    for i in range(47)
]
ship_flight_frames = [
    pygame.image.load(f"./assets/spaceship/tile{i:03}.png") for i in range(16)
]

pygame.font.init()


class Assets:
    @staticmethod
    def load_fonts():
        Assets.TITLE_FONT = pygame.font.Font("./assets/font/KnightWarrior-w16n8.otf", 120)
        Assets.SUBHEADING_FONT = pygame.font.Font("./assets/font/VeniteAdoremus-rgRBA.ttf", 35)
        Assets.PRESS_START_FONT = pygame.font.Font("./assets/font/PressStart2P.ttf", 15)
        Assets.ROBUSSTART2P = pygame.font.Font("./assets/font/Robus-BWqOd.otf", 120)
        Assets.B04_11 = pygame.font.Font("./assets/font/04b_11.ttf", 11)
        Assets.KENVECTOR = pygame.font.Font("./assets/font/kenvector.ttf", 26)
        Assets.B04_11v =  pygame.font.Font("./assets/font/04b_11.ttf", 9)
        
# Initialize pygame mixer
pygame.mixer.init()

# Load sounds
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join("./assets", "sound", "explosions", "explosion-small.mp3"))
EXPLOSION_SOUND.set_volume(0.5)  # Adjust volume if neede



# Load sound effect for home screen
background_music = pygame.mixer.Sound('./assets/sound/theme-space/final-show.mp3')



# Load sounds
SPACE_DEFAULT = pygame.mixer.Sound(os.path.join("./assets", "sound", "theme-space", "space-default.mp3"))
SPACE_DEFAULT.set_volume(1)  # Adjust volume if needed

SELECT_OPTION = pygame.mixer.Sound(os.path.join("./assets", "sound", "selection", "select.wav"))
SELECT_OPTION.set_volume(2)  # Adjust volume if needed


SHIP_DESTROY =  pygame.mixer.Sound(os.path.join("./assets", "sound", "explosions", "space-ship.mp3"))
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

ROCK_COLLIED=  pygame.mixer.Sound(os.path.join("./assets", "sound", "collied", "rock-broke.mp3"))
ROCK_COLLIED.set_volume(1) 


RELOAD_WEAPON=  pygame.mixer.Sound(os.path.join("./assets", "sound", "leaser", "reload.mp3"))
RELOAD_WEAPON.set_volume(0.7) 

SWITCH_WEAPON = pygame.mixer.Sound(os.path.join("./assets", "sound", "leaser", "swing.mp3"))
SWITCH_WEAPON.set_volume(1) 


GAME_WIDTH, GAME_HEIGHT = 1280, 720
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

game_surface.blit(background, (0, 0))
# draw player, asteroids, etc. onto game_surface

BULLET_STORAGE=2000
BULLET=100





def load_animation_frames(folder_path):
    frames = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith(".png"):
            image = pygame.image.load(os.path.join(folder_path, file_name)).convert_alpha()
            frames.append(image)
    return frames

def  load_assets():
    walk_animations = {
        "down": load_animation_frames("./assets/character/main/walk/walk-front"),
        "up": load_animation_frames("./assets/character/main/walk/walk-backward"),
        "left": load_animation_frames("./assets/character/main/walk/walk-left"),
        "right": load_animation_frames("./assets/character/main/walk/walk-right"),
    }

    idle_animations = {
        "down": load_animation_frames("./assets/character/main/idle/idle-front"),
        "up": load_animation_frames("./assets/character/main/idle/idle-back"),
        "left": load_animation_frames("./assets/character/main/idle/idle-left"),
        "right": load_animation_frames("./assets/character/main/idle/idle-right"),
    }

    jump_animations = {
        "left": load_animation_frames("./assets/character/main/jump/jump-left"),
        "right":  load_animation_frames("./assets/character/main/jump/jump-right"),
        "up":  load_animation_frames("./assets/character/main/jump/jump-back"),      # or "back"
        "down":  load_animation_frames("./assets/character/main/jump/jump-front"),    
    }
    background = pygame.image.load("./back.jpg").convert()
    gun_image = pygame.image.load("./assets/accessories/guns/gun16.png").convert_alpha()
    gun_image = pygame.transform.scale(gun_image, (43, 23))  # Adjust the size as needed
    return walk_animations, idle_animations,jump_animations,background,gun_image


icon_image= pygame.image.load("./assets/character/main/idle/idle-front/idle00.png")


screen = pygame.display.set_mode((WIDTH, HEIGHT))

def load_image(path, size=None):
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size) if size else img
    else:
        print(f"[Warning] Missing image: {path}")
        surf = pygame.Surface(size if size else (50, 50))
        surf.fill((100, 100, 100))
        return surf
# Now load assets safely after display mode is set:
panel_image = load_image("./inventory/panel_one.png", (350, 600))
panel_two = load_image("./inventory/panel_two.png", (350, 600))
item_box_image = load_image("./inventory/itemBox.png", (68, 68))
button_image = load_image("./inventory/button.png", (75, 40))

button_image2 = load_image("./inventory/button.png", (75, 40))
money_icon = load_image("./assets/accessories/money.png", (30, 30))
selected_box =load_image("./inventory/selected.png", (68, 68))

upgrade_image =load_image("./inventory/upgrade.png", (20, 25))




menu_items = {
    "item1": {
        "normal": load_image("./inventory/menu/item1.png", (28, 28)),
        "selected": load_image("./inventory/menu/item1-selected.png", (28, 28)),
    },
    "item2": {
        "normal": load_image("./inventory/menu/item2.png", (28, 28)),
        "selected": load_image("./inventory/menu/item2-selected.png", (28, 28)),
    },
    "item3": {
        "normal": load_image("./inventory/menu/item3.png", (28,28)),
        "selected": load_image("./inventory/menu/item3-selected.png", (28, 28)),
    },
    "item4": {
        "normal": load_image("./inventory/menu/item4.png",(28, 28)),
        "selected": load_image("./inventory/menu/item4-selected.png", (28, 28)),
    },
}


import textwrap
import pygame

def render_multiline_text(
    screen, 
    text, 
    font, 
    color, 
    panel_rect, 
    start_y, 
    line_spacing=5, 
    max_width=None, 
    center=True
):
    """
    Renders multi-line text within a given panel with automatic wrapping and spacing.

    Args:
        screen (pygame.Surface): The surface to render on.
        text (str): The full text to render (can contain \n).
        font (pygame.font.Font): Font to render the text.
        color (tuple): Text color (R, G, B).
        panel_rect (pygame.Rect): Rect where text will be displayed.
        start_y (int): The starting y-coordinate.
        line_spacing (int, optional): Space between lines. Defaults to 5.
        max_width (int, optional): Wrap width. If None, uses panel_rect.width.
        center (bool, optional): If True, centers text horizontally. If False, aligns left.
    """
    lines = []
    max_width = max_width or panel_rect.width - 40  # add margin

    # Split into individual lines and wrap each line
    for line in text.split('\n'):
        wrapped = textwrap.wrap(line, width=100)  # Initial wrap by characters count
        # Now filter based on pixel width
        for wrapped_line in wrapped:
            # Shrink if necessary by measuring text pixel length
            words = wrapped_line.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + ("" if current_line == "" else " ") + word
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

    # Render each line
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        if center:
            x = panel_rect.left + (panel_rect.width - text_surface.get_width()) // 2
        else:
            x = panel_rect.left + 20  # left aligned with margin
        y = start_y + i * (text_surface.get_height() + line_spacing)
        screen.blit(text_surface, (x, y))


hand_icon = pygame.transform.rotate(load_image("./assets/accessories/guns/hands.png", (70,80)), -90)
gun_icon = load_image("./assets/accessories/guns/gun24.png" ,(150, 40))
knife_icon = load_image("./assets/accessories/guns/kniff.png",(150, 60))
hud_image =load_image("./assets/accessories/weapon-excess.png",(150, 40))


start_button_paths = [
    "assets/interface/buttons/play.png",
    "assets/interface/buttons/store.png",
    "assets/interface/buttons/option.png",
    "assets/interface/buttons/tutorial.png"
]


# start screen

home_arrow_img = pygame.image.load("../astroid-gpt/assets/interface/buttons/arrow.png").convert_alpha()
home_arrow_img = pygame.transform.scale(home_arrow_img, (30, 30))  

side_top_bar= pygame.image.load("assets/interface/home/sideTop.png")
side_top_bar = pygame.transform.scale(side_top_bar, (300, 60))  

left_bottom_bar  = pygame.image.load("assets/interface/home/bottom-left.png")
left_bottom_bar = pygame.transform.scale(left_bottom_bar, (350,100))  

middle_bar = pygame.image.load("assets/interface/home/middle-header.png")
middle_bar = pygame.transform.scale(middle_bar,(600,140))

middle_bar_text =pygame.image.load("assets/interface/home/start_game.png")
middle_bar_text = pygame.transform.scale(middle_bar_text,(400,50))

top_right =pygame.image.load("assets/interface/home/top-right.png")
top_right= pygame.transform.scale(top_right,(280,240))

big_spaceship = pygame.image.load("assets/interface/home/spaceship.png")
big_spaceship = pygame.transform.scale(big_spaceship,(240,240))

bottom_right = pygame.transform.flip(top_right, True, False)


SWITCH_BUTTON = pygame.mixer.Sound(os.path.join("assets", "sound", "selection", "3d.wav"))
SWITCH_BUTTON.set_volume(1) 


SELECT_BUTTON = pygame.mixer.Sound(os.path.join("assets", "sound", "selection", "level.mp3"))
SELECT_BUTTON.set_volume(1) 

primary_color=(24, 191, 196)



# store screen
store_panel = pygame.image.load("assets/interface/store/store_panel.png")
store_panel = pygame.transform.scale(store_panel,(340,640))

store_panel_flip =pygame.transform.flip(store_panel,True,False)

store_menu = [

    pygame.image.load("assets/interface/store/store_menu/nural.png"),
    pygame.image.load("assets/interface/store/store_menu/plasma.png"),
    pygame.image.load("assets/interface/store/store_menu/precision.png"),
    pygame.image.load("assets/interface/store/store_menu/research.png"),
    pygame.image.load("assets/interface/store/store_menu/shield.png"),
    pygame.image.load("assets/interface/store/store_menu/toxic.png")
]

store_menu_name =[
    "shield",
    "precision",
    "nural",
    "plasma",
    "toxic",
    "research"
]

for index, item in enumerate(store_menu):
    store_menu[index] = pygame.transform.scale(item, (35, 35))



shield_item = [
    pygame.transform.scale(
        pygame.image.load(f"assets/interface/store/shield/tile{i:03d}.png").convert_alpha(),
        (50, 50)  
    )
    for i in range(1, 32)
]



VISIBLE_ROWS = 4
ITEM_HEIGHT = 60  # including spacing
SCROLL_SPEED = 20
