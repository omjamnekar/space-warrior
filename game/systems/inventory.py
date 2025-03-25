import pygame
import os

from game.utils.data import items_data
from utils.data import render_multiline_text, Assets,upgrade_image, WIDTH, HEIGHT,menu_items,button_image2, selected_box, money_icon, panel_image, panel_two, button_image, item_box_image

class InventoryUI:
    def __init__(self, position=(WIDTH // 2, HEIGHT // 2)):
        Assets.load_fonts()
        self.position = position
        self.selected_index = 0
        self.item_data = items_data
        self.money_icon = money_icon
      
        # Load UI assets
        self.panel_image = panel_image
        self.item_box_image = item_box_image
        self.button_image = button_image
        self.button_image2 =button_image2
        self.panel_two = panel_two
        self.selection_box_image = selected_box
        self.menu_items = menu_items
        self.selected_menu_index = 0
        self.font_large = Assets.KENVECTOR
        self.font_small =Assets.B04_11
        self.font_very_small= Assets.B04_11v


        # Pre-load all item icons from item_data
        for item in self.item_data:
            item["icon"] = self.load_image(item["icon"], (56, 56))



    def draw_stat_bar(self, screen, x, y, width, height, value, max_value, color, bg_color=(50, 50, 50), border_color=(255, 255, 255)):
        # Ensure value is within the range of 0 to max_value
        value = max(0, min(value, max_value))
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
        bar_width = int((value / max_value) * width)
        pygame.draw.rect(screen, color, (x, y, bar_width, height))
        # pygame.draw.rect(screen, border_color, (x, y, width, height), 2)


    def load_image(self, path, size=None):
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size) if size else img
        else:
            print(f"[Warning] Missing image: {path}")
            surf = pygame.Surface(size if size else (50, 50))
            surf.fill((100, 100, 100))
            return surf

    def draw(self, screen, player_money=0):
        # Draw main panels
        panel_rect = self.panel_image.get_rect(topleft=(20, HEIGHT // 2 - self.panel_image.get_height() // 2))
        panel_two_rect = self.panel_two.get_rect(topleft=(panel_rect.right, panel_rect.top))
        screen.blit(self.panel_image, panel_rect.topleft)
        screen.blit(self.panel_two, panel_two_rect.topleft)

        # Draw menu items (icons at top of panel one)
        menu_margin_x = 30
        menu_margin_y = 30
        menu_spacing = 10
        menu_start_x = panel_rect.left + menu_margin_x
        menu_start_y = panel_rect.top + menu_margin_y
        for idx, (key, item) in enumerate(self.menu_items.items()):
            icon = item["selected"] if idx == self.selected_menu_index else item["normal"]
            x = menu_start_x + idx * (icon.get_width() + menu_spacing)
            screen.blit(icon, (x, menu_start_y))

        # Draw player money
        icon_margin = 20
        money_icon_pos = (panel_rect.right - self.money_icon.get_width() - icon_margin, panel_rect.top + icon_margin)
        screen.blit(self.money_icon, money_icon_pos)
        money_font = pygame.font.Font(None, 36)
        money_text = money_font.render(str(player_money), True, (255, 255, 0))
        money_text_pos = (money_icon_pos[0] - money_text.get_width() - 10, money_icon_pos[1] + 5)
        screen.blit(money_text, money_text_pos)

        # Draw items grid in panel one
        items_per_row = 4
        item_spacing = 80
        grid_width = (items_per_row - 1) * item_spacing + self.item_box_image.get_width()
        start_x = panel_rect.left + (panel_rect.width - grid_width) // 2
        start_y = panel_rect.top + 80
        for i, item in enumerate(self.item_data):
            x = start_x + (i % items_per_row) * item_spacing
            y = start_y + (i // items_per_row) * item_spacing
            screen.blit(self.item_box_image, (x, y))

            # Draw item icon centered
            icon_w, icon_h = item["icon"].get_size()
            box_w, box_h = self.item_box_image.get_size()
            icon_x = x + (box_w - icon_w) // 2
            icon_y = y + (box_h - icon_h) // 2
            screen.blit(item["icon"], (icon_x, icon_y))



            # Draw selection box if selected
            if i == self.selected_index:
                screen.blit(self.selection_box_image, (x, y))
        
                    # Draw quantity if more than one
            if item["upgrade"] >= 0:
                qty_text = self.font_small.render(str(item["upgrade"]), True, (255, 215, 0))
                screen.blit(qty_text, (x + 52, y + 52))

        # Draw selected item panel (panel two)
        if self.item_data:
            selected_item = self.item_data[self.selected_index]
            self.selected_item_image = selected_item["icon"]

            # Draw heading for selected item
            heading_text = self.font_large.render(selected_item["name"], True, (255, 215, 0))
            heading_x = panel_two_rect.left + (panel_two_rect.width - heading_text.get_width()) // 2
            heading_y = panel_two_rect.top + 30
            screen.blit(heading_text, (heading_x, heading_y))
                    
            desc_text = selected_item.get("desc", "")
            desc_start_y = heading_y + heading_text.get_height() + 150

            render_multiline_text(
                screen=screen,
                text=desc_text,
                font=self.font_small,
                color=(210, 180, 140),  # Changed color to skin-tone brown
                panel_rect=panel_two_rect,
                start_y=desc_start_y,
                line_spacing=8,
                max_width=panel_two_rect.width - 40,
                center=True
            )
                        # Assuming selected_item is your current item dictionary
            damage = selected_item.get("damage", 0)
            defense = selected_item.get("defense", 0)
            energy_consumption = selected_item.get("energy_consumption", 0)

            bar_start_y = desc_start_y + (len(desc_text.split('\n')) * (self.font_small.get_height() + 8)) + 50

            bar_width = panel_two_rect.width - 100
            bar_height = 10
            bar_x = panel_two_rect.left + 25

            # Labels and bars
            labels = [("Damage", damage, 100, (200, 50, 50)),
                    ("Defense", defense, 100, (50, 200, 50)),
                    ("Energy", energy_consumption, 100, (50, 150, 200))]

            for i, (label, value, max_val, color) in enumerate(labels):
                label_surface = self.font_small.render(f"{label}: {value}", True, (255, 255, 255))
                label_x = panel_two_rect.left + 25  # Align with the left side of the panel
                label_y = bar_start_y + i * (bar_height + 25)  # Reduced gap between bars
                screen.blit(label_surface, (label_x, label_y))

                bar_y = label_y + label_surface.get_height() + 2  # Reduced gap between label and bar
                self.draw_stat_bar(screen, bar_x, bar_y, bar_width, bar_height, value, max_val, color)

            # Draw selected item image below heading
        if self.selected_item_image:
            # Define your desired size (e.g., double the current size)
            new_width = int(self.selected_item_image.get_width() * 1.7)
            new_height = int(self.selected_item_image.get_height() * 1.7)

            # Scale the image
            scaled_item_image = pygame.transform.smoothscale(self.selected_item_image, (new_width, new_height))

            # Recalculate positions based on the scaled size
            selected_item_x = panel_two_rect.centerx - (new_width // 1.7)
            selected_item_margin_bottom = self.button_image.get_height()
            selected_item_y = panel_two_rect.bottom - selected_item_margin_bottom - new_height

            # Draw the scaled image
            screen.blit(scaled_item_image, (selected_item_x, selected_item_y))



        # Show energy consumption fragment below the main heading
        if self.item_data:
            selected_item = self.item_data[self.selected_index]
            upgrade_cost = selected_item.get("upgrade_Cost", 0)

            # Draw money icon
            cost_icon_x = panel_two_rect.left + 30  # Align to the left with a margin
            cost_icon_y = heading_y + heading_text.get_height() + 25  # Add margin below the heading
            screen.blit(self.money_icon, (cost_icon_x, cost_icon_y))

            # Draw upgrade cost text
            cost_text = self.font_small.render(f"{upgrade_cost}", True, (255, 255, 255))
            cost_text_x = cost_icon_x + self.money_icon.get_width() + 10  # Add spacing after the icon
            cost_text_y = cost_icon_y + (self.money_icon.get_height() - cost_text.get_height()) // 2  # Center text vertically
            screen.blit(cost_text, (cost_text_x, cost_text_y))

        

        # Add Upgrade button
        button_margin_bottom = 50  # Define button_margin_bottom before using it
        button3_x = panel_two_rect.right - self.button_image.get_width() - 30  # Position at the right side of energy
        button3_y = cost_text_y - 10  # Slightly move it upwards

        # Get mouse position and button state
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Check if Upgrade button is clicked
        is_button3_hovered = pygame.Rect(button3_x, button3_y, self.button_image.get_width(), self.button_image.get_height()).collidepoint(mouse_pos)
        is_button3_clicked = is_button3_hovered and mouse_pressed[0]

        # Animate Upgrade button click by moving it slightly down on the y-axis
        button3_y_offset = 5 if is_button3_clicked else 0

        # Increase the width of the Upgrade button box
        button3_width = self.button_image.get_width() + 25  # Add extra width
        button3_height = self.button_image.get_height()
        button3_x_center = button3_x + self.button_image.get_width() // 2
        button3_x = button3_x_center - button3_width // 2  # Adjust x to center the new width

        
        # Draw energy consumption below the upgrade cost section
        selected_item = self.item_data[self.selected_index]
        energy_consumption = selected_item.get("energy_consumption", 0)
        energy_text_label = self.font_small.render("Energy:", True, (255, 255, 255))
        energy_text_value = self.font_small.render(f"{energy_consumption}", True, (255, 0, 0))  # Value in red
        energy_x = cost_text_x - 35  # Align with the upgrade cost text
        energy_y = cost_text_y + cost_text.get_height() + 40  # Add margin below the upgrade cost
        screen.blit(energy_text_label, (energy_x, energy_y))
        screen.blit(energy_text_value, (energy_x + energy_text_label.get_width() + 5, energy_y))  # Position value next to label

        # Draw rarity attribute to the right of energy consumption
        rarity = selected_item.get("rarity", "Unknown")
        rarity_text_label = self.font_very_small.render("State:", True, (255, 255, 255))
        rarity_text_value = self.font_very_small.render(rarity, True, (173, 216, 240))  # Light blue color for value
        rarity_x = energy_x + 120  # Adjusted position to stay within panel two
        rarity_y = energy_y  # Align vertically with energy consumption
        screen.blit(rarity_text_label, (rarity_x, rarity_y))
        screen.blit(rarity_text_value, (rarity_x + rarity_text_label.get_width() + 5, rarity_y))  # Position value next to label
        # Draw Upgrade button with animation
        scaled_button_image = pygame.transform.scale(self.button_image, (button3_width, button3_height))
        screen.blit(scaled_button_image, (button3_x, button3_y + button3_y_offset))

        # Draw text on Upgrade button
        upgrade_text_color = (255, 255, 0) if is_button3_clicked else (255, 255, 255)
        upgrade_text = self.font_small.render("Upgrade", True, upgrade_text_color)
        upgrade_text_rect = upgrade_text.get_rect(center=(button3_x + button3_width // 2, button3_y + button3_height // 2 + button3_y_offset))
        screen.blit(upgrade_text, upgrade_text_rect)

        # Draw upgrade image to the left of the Upgrade button
        upgrade_image_x = button3_x - upgrade_image.get_width() - 10  # Position to the left with a margin
        upgrade_image_y = button3_y + (button3_height - upgrade_image.get_height()) // 2  # Center vertically
        screen.blit(upgrade_image, (upgrade_image_x, upgrade_image_y))

        # Check if the upgrade image is clicked
        upgrade_image_rect = pygame.Rect(upgrade_image_x, upgrade_image_y, upgrade_image.get_width(), upgrade_image.get_height())
        if upgrade_image_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
            # Display an option panel for upgrade details
            option_panel_width = 320
            option_panel_height = 220
            option_panel_x = upgrade_image_x - option_panel_width - 15  # Position to the left of the upgrade image
            option_panel_y = upgrade_image_y - (option_panel_height // 2)  # Center vertically with the upgrade image

            # Draw the option panel background with rounded corners
            option_panel_rect = pygame.Rect(option_panel_x, option_panel_y, option_panel_width, option_panel_height)
            pygame.draw.rect(screen, (0, 0, 0), option_panel_rect, border_radius=10)  # Dark gray background
            pygame.draw.rect(screen, (200, 200, 200), option_panel_rect, 2, border_radius=10)  # Light border

            # Add text to the option panel
            option_text = [
                ("Upgrade Details:", (255, 215, 0)),  # Gold for the title
                (f"Cost: {selected_item.get('upgrade_Cost', 0)}", (255, 255, 255)),  # White for details
                (f"Damage Boost: +{selected_item.get('damage', +20)}", (200, 50, 50)),  # Red for damage
                (f"Defense Boost: +{selected_item.get('defense_boost', +10)}", (50, 200, 50)),  # Green for defense
                (f"Energy Efficiency: +{selected_item.get('energy_efficiency', 0)}", (50, 150, 200))  # Blue for energy
            ]

            text_y = option_panel_y + 20
            for line, color in option_text:
                text_surface = self.font_small.render(line, True, color)
                screen.blit(text_surface, (option_panel_x + 15, text_y))
                text_y += text_surface.get_height() + 10



        button_margin_bottom = 20
        button_x = panel_two_rect.centerx - (self.button_image.get_width() // 2 + 115)
        button_y = panel_two_rect.bottom - self.button_image.get_height() - button_margin_bottom
        button2_x = panel_two_rect.centerx - (self.button_image2.get_width() // 2 - 115)
        button2_y = panel_two_rect.bottom - self.button_image2.get_height() - button_margin_bottom


        # Button 1 (Equip)
        is_button1_hovered = pygame.Rect(button_x, button_y, self.button_image.get_width(), self.button_image.get_height()).collidepoint(mouse_pos)
        is_button1_clicked = is_button1_hovered and mouse_pressed[0]

        # Button 2 (Drop)s
        is_button2_hovered = pygame.Rect(button2_x, button2_y, self.button_image2.get_width(), self.button_image2.get_height()).collidepoint(mouse_pos)
        is_button2_clicked = is_button2_hovered and mouse_pressed[0]

        # Animate button click by moving it slightly down on the y-axis
        button1_y_offset = 5 if is_button1_clicked else 0
        button2_y_offset = 5 if is_button2_clicked else 0

        # Draw buttons with animation
        screen.blit(self.button_image, (button_x, button_y + button1_y_offset))
        screen.blit(self.button_image2, (button2_x, button2_y + button2_y_offset))

        # Draw text on buttons
        equip_text_color = (255, 255, 0) if is_button1_clicked else (255, 255, 255)
        drop_text_color = (255, 255, 0) if is_button2_clicked else (255, 255, 255)

        equip_text = self.font_small.render("Equip", True, equip_text_color)
        drop_text = self.font_small.render("Drop", True, drop_text_color)

        equip_text_rect = equip_text.get_rect(center=(button_x + self.button_image.get_width() // 2, button_y + self.button_image.get_height() // 2 + button1_y_offset))
        drop_text_rect = drop_text.get_rect(center=(button2_x + self.button_image2.get_width() // 2, button2_y + self.button_image2.get_height() // 2 + button2_y_offset))

        # Show equipped status below the bars
        selected_item = self.item_data[self.selected_index]  # Ensure the selected item is updated
        equipped_status = selected_item.get("is_equiped", False)
        equipped_text = self.font_small.render("Equipped:", True, (255, 255, 255))
        status_color = (0, 255, 0) if equipped_status else (255, 0, 0)  # Green for Yes, Red for No
        status_text = self.font_small.render("Yes" if equipped_status else "No", True, status_color)

        left_margin = 25  # Adjusted margin from the left
        equipped_text_rect = equipped_text.get_rect(midleft=(panel_two_rect.left + left_margin, bar_start_y + len(labels) * (bar_height + 25) + 20))
        status_text_rect = status_text.get_rect(midleft=(panel_two_rect.left + left_margin, bar_start_y + len(labels) * (bar_height + 25) + 40))

        screen.blit(equipped_text, equipped_text_rect)
        screen.blit(status_text, status_text_rect)

        screen.blit(equip_text, equip_text_rect)
        screen.blit(drop_text, drop_text_rect)




    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.item_data)
            elif event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.item_data)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 4) % len(self.item_data)
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 4) % len(self.item_data)
            elif event.key == pygame.K_a:
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_items)
                self.selected_index = 0  # Reset item selection on menu switch
            elif event.key == pygame.K_d:
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_items)
                self.selected_index = 0  # Reset item selection on menu switch

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Check if clicking on menu icons
            panel_rect = self.panel_image.get_rect(topleft=(20, HEIGHT // 2 - self.panel_image.get_height() // 2))
            menu_margin_x = 30
            menu_margin_y = 30
            menu_spacing = 10
            menu_start_x = panel_rect.left + menu_margin_x
            menu_start_y = panel_rect.top + menu_margin_y

            for idx, (key, item) in enumerate(self.menu_items.items()):
                icon = item["normal"]
                icon_rect = icon.get_rect(topleft=(menu_start_x + idx * (icon.get_width() + menu_spacing), menu_start_y))
                if icon_rect.collidepoint(mouse_pos):
                    self.selected_menu_index = idx
                    self.selected_index = 0  # ✅ Reset item selection on menu click

            # Check for click on items
            items_per_row = 4
            item_spacing = 80
            grid_width = (items_per_row - 1) * item_spacing + self.item_box_image.get_width()
            start_x = panel_rect.left + (panel_rect.width - grid_width) // 2
            start_y = panel_rect.top + 80

            for i, item in enumerate(self.item_data):
                x = start_x + (i % items_per_row) * item_spacing
                y = start_y + (i // items_per_row) * item_spacing
                box_rect = self.item_box_image.get_rect(topleft=(x, y))
                if box_rect.collidepoint(mouse_pos):
                    self.selected_index = i  # ✅ Select item on click
