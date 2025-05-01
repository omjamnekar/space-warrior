import pygame
import sys
from game.entities.stars import Star
from game.settings import WIDTH, HEIGHT, PROGRESS, LEVEL, SPEED, CAPACITY_BULLET
from game.assets import (
    SPACE_DEFAULT, background, SELECT_BUTTON, SWITCH_BUTTON,
    start_button_paths, home_arrow_img, side_top_bar, left_bottom_bar,
    middle_bar, middle_bar_text, top_right, big_spaceship, bottom_right, primary_color,
    store_panel,store_panel_flip,store_menu,shield_item
)

pygame.init()


class HomeInterface:
    def __init__(self, window: pygame.display.set_mode):
        self.window = window
        
        # assets
        self.button_paths = start_button_paths
        self.arrow_img = home_arrow_img
        self.top_rigt_bar = side_top_bar
        self.bottom_left = left_bottom_bar
        self.middle_bar = middle_bar
        self.middle_bar_text = middle_bar_text
        self.top_right = top_right
        self.big_spaceship = big_spaceship
        self.bottom_right = bottom_right
        self.primary_color = primary_color

        self.bg = pygame.transform.scale(background, (WIDTH, HEIGHT))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        self.bg.blit(overlay, (0, 0))

        self.stars = [Star() for _ in range(100)]
        self.button_positions = [(100, 300 + i * 50) for i in range(len(self.button_paths))]
        self.buttons = []

        self.top_icons = [
            pygame.image.load("assets/interface/home/close.png"),
            pygame.image.load("assets/interface/home/music.png"),
            pygame.image.load("assets/interface/home/menu.png"),
        ]
        self.top_icons = [pygame.transform.scale(icon, (35, 35)) for icon in self.top_icons]
        self.top_icon_positions = [(20, 60), (80, 60), (140, 60)]

        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.running = True
        
        self.selected_item_index = None 

        # Animation state
        self.switched_index = 0
        self.selected_menu = "EQUIPPED"
        self.selected_index = 0
        self.fade_alpha = 0
        self.fade_speed = 5
        self.animated_progress = 0
        self.animated_level = 6.5
        self.bar_animation_speed = 5.5
        self.item_space =40
        self.menu_item_size =35
        self.menu_selected =0
        self.isEnter =False
        self.store_menu_icons = []
        self.scroll_offset = 0
        icon_size = 32
        start_x = WIDTH // 2 - 50  # adjust this based on your panel position
        y = 150  # vertical position of icons, adjust based on image

        for i in range(6):  # 6 icons
            rect = pygame.Rect(start_x + i * (icon_size + 10), y, icon_size, icon_size)
            self.store_menu_icons.append(rect)

        # Load buttons
        for path in self.button_paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (220, 35))
            img.set_alpha(0)
            self.buttons.append(img)

    def show(self):
        SWITCH_BUTTON.play()
        clock = pygame.time.Clock()

        # Start all elements with fade_alpha = 0
        self.fade_alpha = 0
        self.fade_speed = 5

        # Convert surfaces that need alpha handling
        self.bg.set_alpha(0)
        self.big_spaceship.set_alpha(0)
        self.middle_bar.set_alpha(0)
        self.middle_bar_text.set_alpha(0)
        self.top_right.set_alpha(0)
        self.bottom_right.set_alpha(0)
        self.bottom_left.set_alpha(0)
        self.top_rigt_bar.set_alpha(0)

        while self.running:
            clock.tick(60)
            
            #keys Handler
            self.key_Handler()                    

            # Increase fade-in alpha up to 255
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)

                # Apply alpha to UI assets
                self.bg.set_alpha(self.fade_alpha)
                self.top_rigt_bar.set_alpha(self.fade_alpha)
                self.bottom_left.set_alpha(self.fade_alpha)
                self.middle_bar.set_alpha(self.fade_alpha)
                self.middle_bar_text.set_alpha(self.fade_alpha)
                self.top_right.set_alpha(self.fade_alpha)
                self.big_spaceship.set_alpha(self.fade_alpha)
                self.bottom_right.set_alpha(self.fade_alpha)

                for btn in self.buttons:
                    btn.set_alpha(self.fade_alpha)

            # =============== DRAWING ==================
            self.window.blit(self.bg, (0, 0))

            for star in self.stars:
                star.move()
                star.draw(self.window)

            for i, btn in enumerate(self.buttons):
                x, y = self.button_positions[i]
                self.window.blit(btn, (x, y))
                if i == self.switched_index:
                    border_rect = pygame.Rect(x - 5, y - 5, btn.get_width() + 10, btn.get_height() + 10)
                    pygame.draw.rect(self.window, (255, 255, 255), border_rect, 3)

            self.window.blit(self.arrow_img, (self.button_positions[self.switched_index][0] - 40,
                                            self.button_positions[self.switched_index][1]))

            # Top bar & icons
            self.window.blit(self.top_rigt_bar, (0, 0))
            for i, icon in enumerate(self.top_icons):
                self.window.blit(icon, self.top_icon_positions[i])

            # Bottom left bar
            self.window.blit(self.bottom_left, (0, HEIGHT - 100))

            if self.switched_index ==0:
                self.start_Screen()
            elif self.switched_index == 1:
                self.store_screen()
            pygame.display.flip()
        pygame.quit()
        sys.exit()
    

    def startGame(self):
        for volume in range(10, -1, -1):
            pygame.mixer.music.set_volume(volume / 10)
            pygame.time.delay(150)
        pygame.mixer.music.fadeout(1500)
        pygame.mixer.music.stop()
        SPACE_DEFAULT.play()
        SPACE_DEFAULT.set_volume(1)


    def start_Screen(self):
       
                self.window.blit(self.middle_bar, ((WIDTH / 2) / 2 + 40, 10))
                self.window.blit(self.middle_bar_text, ((WIDTH / 2) / 2 + 140, 50))

                self.window.blit(self.top_right, (WIDTH - 300, 10))
                top_right_x = WIDTH - 260
                # Animate progress
                if self.animated_progress < PROGRESS:
                    self.animated_progress += self.bar_animation_speed
                    self.animated_progress = min(self.animated_progress, PROGRESS)

                # Animate level
                if self.animated_level < LEVEL:
                    self.animated_level += self.bar_animation_speed
                    self.animated_level = min(self.animated_level, LEVEL)
                self.draw_status_bar(top_right_x, 80, "progress", self.animated_progress, PROGRESS, 100)
                self.draw_status_bar(top_right_x, 160, "level", self.animated_level, LEVEL, 100)


                # Spaceship + bottom info
                self.window.blit(self.big_spaceship, (WIDTH - 300, HEIGHT / 2 - 110))
                self.window.blit(self.bottom_right, (WIDTH - 300, HEIGHT - 260))

                self.draw_perfomance_bar(WIDTH - 260, HEIGHT - 200, "SPEED", str(SPEED) + "KM/H", (WIDTH - 265, HEIGHT - 175))
                self.draw_perfomance_bar(WIDTH - 260, HEIGHT - 125, "CAPACITY", str(CAPACITY_BULLET) + " rounds",
                                        (WIDTH - 260, HEIGHT - 100))
    

    def draw_status_bar(self, x, y, label, animated_value, target_value, max_value):
        custom_font = pygame.font.Font("./assets/font/PressStart2P.ttf", 15)

        # numeric value 
        display_val = int(animated_value)
        text_surface = custom_font.render(f"{label}: {display_val}", True, (255, 255, 255))
        self.window.blit(text_surface, (x, y))

        #  background bar
        pygame.draw.rect(self.window, (225, 225, 225), (x, y + 25, 200, 10), border_radius=5)

      
        fill_width = int(200 * animated_value / max_value)
        pygame.draw.rect(self.window, self.primary_color, (x, y + 25, fill_width, 10), border_radius=5)


    def draw_perfomance_bar(self, x, y, label, value, position):
        width, height = position
        custom_font = pygame.font.Font("./assets/font/PressStart2P.ttf", 15)
        text_surface = custom_font.render(f"{label}", True, (255, 255, 255))
        self.window.blit(text_surface, (x, y))
        self.draw_container(f"{value}", (width, height), (200, 35))

    def draw_container(self, text, pos, size, bg_color=(0, 54, 91), text_color=(255, 255, 255), border_color=(255, 255, 255)):
        x, y = pos
        width, height = size
        border_radius = 15
        pygame.draw.rect(self.window, bg_color, (x, y, width, height), border_radius=border_radius)
        pygame.draw.rect(self.window, border_color, (x, y, width, height), width=2, border_radius=border_radius)

        font = pygame.font.SysFont('consolas', 18, bold=True)
        rendered_text = font.render(text, True, text_color)
        text_rect = rendered_text.get_rect(midleft=(x + 10, y + height // 2))
        self.window.blit(rendered_text, text_rect)



    def store_screen(self):
        # Draw panel
        self.window.blit(store_panel, (WIDTH / 2 - 120, 100))
        self.window.blit(store_panel_flip, (WIDTH / 2 + 235, 100))

    

        for index, rect in enumerate(self.store_menu_icons):
            icon = store_menu[index]

            if self.menu_selected == index:
               
                scaled_icon = pygame.transform.scale(icon, (38, 38))
                icon_pos = (rect.x - 3, rect.y - 3) 
            else:
                scaled_icon = pygame.transform.scale(icon, (32, 32))
                icon_pos = rect.topleft

            self.window.blit(scaled_icon, icon_pos)

        selected_rect = self.store_menu_icons[self.menu_selected]
        pygame.draw.rect(self.window, (255, 255, 255),
                        (selected_rect.x, selected_rect.bottom + 5, selected_rect.width +2, 3))

        self.menu_button("EQUIPPED", (WIDTH / 2 - 80, 220), isSelected=(self.selected_menu == "EQUIPPED"))
        self.menu_button("STORE", (WIDTH / 2 + 10, 220), isSelected=(self.selected_menu == "STORE"))

        underline_width = 100
        underline_height = 3
        underline_x = (WIDTH / 2 - 80) if self.selected_menu == "EQUIPPED" else (WIDTH / 2 + 10)
        underline_y = 240 
        pygame.draw.rect(self.window, (0, 255, 255), (underline_x, underline_y, underline_width, underline_height))
        pygame.draw.rect(self.window,(255,255,255), (WIDTH/2-80, 243, 270,2))
        
        # grid items
        self.draw_shield_grid(shield_item, WIDTH/2 -85, 250,4, 50)




   
    def draw_shield_grid(self, items, start_x, start_y, columns=4, spacing=10):
        item_size = 10  
        item_rects = []

        for i, image in enumerate(items):
            row = i // columns
            col = i % columns
            x = start_x + col * (item_size + spacing + 10)
            y = start_y + row * (item_size + spacing)

           
            if i == self.selected_item_index:
                pygame.draw.rect(self.window, (0, 255, 255), (x-2, y-2, 50, 50), width=2, border_radius=6)
                scaled_image = pygame.transform.scale(image, (image.get_width() - 4, image.get_height() -4))
                self.window.blit(scaled_image, (x, y))
                rect = pygame.Rect(x, y, item_size, item_size)
                item_rects.append(rect)

            else:
                self.window.blit(image, (x, y))
                rect = pygame.Rect(x, y, item_size, item_size)
                item_rects.append(rect)

       
        return item_rects



    def menu_button(self, label, pos, isSelected=False):
        x, y = pos
        font = pygame.font.Font("./assets/font/VeniteAdoremus-rgRBA.ttf", 16)
        text_surface = font.render(label, True, (0, 255, 255) if isSelected else (200, 200, 200))
        text_rect = text_surface.get_rect(center=(x + 50, y))
        self.window.blit(text_surface, text_rect)
        return text_rect
    

    def key_Handler(self):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                               self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # Left mouse click
                               print("clicked")
                               self.handle_mouse_click(event.pos)
                    elif event.type == pygame.KEYDOWN :
                            if event.key == pygame.K_DOWN:
                                self.switched_index = (self.switched_index + 1) % len(self.buttons)
                                SWITCH_BUTTON.play()
                            elif event.key == pygame.K_UP:
                                self.switched_index = (self.switched_index - 1) % len(self.buttons)
                                SWITCH_BUTTON.play()
                            elif event.key == pygame.K_RETURN:
                                SELECT_BUTTON.play()
                            
                        
    def handle_mouse_click(self, pos):
        mouse_x, mouse_y = pos
        item_rects = self.draw_shield_grid(shield_item, WIDTH / 2 - 85, 250, 4, 50)
        equipped_rect = self.menu_button("EQUIPPED", (WIDTH / 2 - 80, 220), isSelected=(self.selected_menu == "EQUIPPED"))
        store_rect = self.menu_button("STORE", (WIDTH / 2 + 10, 220), isSelected=(self.selected_menu == "STORE"))
        



       

        if equipped_rect.collidepoint(mouse_x, mouse_y):
            self.selected_menu = "EQUIPPED"
            SELECT_BUTTON.play()
            return
        elif store_rect.collidepoint(mouse_x, mouse_y):
            self.selected_menu = "STORE"
            SELECT_BUTTON.play()
            return

        if self.switched_index == 1: 
            for i, rect in enumerate(self.store_menu_icons):
                if rect.collidepoint(mouse_x, mouse_y):
                    self.selected_store_category = i
                    self.menu_selected = i
                    SELECT_BUTTON.play()
                    return

       
        for i, (x, y) in enumerate(self.button_positions):
            btn_rect = pygame.Rect(x, y, 220, 35)
            if btn_rect.collidepoint(mouse_x, mouse_y):
                self.switched_index = i
                SELECT_BUTTON.play()
                return
            

        if self.switched_index == 1:
            for index, item in enumerate(store_menu):
                x = (WIDTH / 2 - 50) + index * self.item_space
                y = 150
                item_rect = pygame.Rect(x, y, self.menu_item_size, self.menu_item_size)
                if item_rect.collidepoint(mouse_x, mouse_y):
                    self.menu_selected = index
                    SELECT_BUTTON.play()
                    return

        for idx, rect in enumerate(item_rects):
           
            moved_rect = rect.move(10, 10)
            padded_rect = moved_rect.inflate(40, 40)
           
            if padded_rect.collidepoint(pos):
                self.selected_item_index = idx
                SELECT_BUTTON.play()
                print(f"Clicked on shield item index: {idx}")
