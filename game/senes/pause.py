import pygame
from game.settings import WIDTH, HEIGHT
from game.assets import Assets, SELECT_OPTION
from game.ui.copyright import CopyRightText

class PauseScreen:
    def __init__(self):
        self.active = False
        self.options = ["Resume", "Restart", "Home"]
        self.selected_index = 0  # Track selected option
        self.font = Assets.PRESS_START_FONT  # Sci-fi styled font
        self.title_font = Assets.TITLE_FONT  # Title font

    def toggle(self):
        self.active = not self.active

    @property
    def is_active(self):
        return self.active

    def draw(self, window):
        # Draw the overlay for the pause screen
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 10, 30))  # Sci-fi dark blue
        window.blit(overlay, (0, 0))

        # Draw the title
        title_text = self.title_font.render("Game Paused", True, (0, 255, 255))
        title_x = (WIDTH - title_text.get_width()) // 2
        window.blit(title_text, (title_x, 100))

        # Draw the copyright text at the bottom-right corner
        CopyRightText().draw_copyright(window)

        # Draw options
        for i, option in enumerate(self.options):
            is_selected = i == self.selected_index
            color = (255, 255, 255) if not is_selected else (0, 255, 255)
            text = self.font.render(option, True, color)

            # Draw button background
            button_rect = pygame.Rect((WIDTH // 2 - 100, 250 + i * 70, 200, 50))
            pygame.draw.rect(window, (50, 50, 100), button_rect, border_radius=10)
            if is_selected:
                pygame.draw.rect(window, (0, 255, 255), button_rect, 3, border_radius=10)

            # Center the text inside the button
            text_x = button_rect.x + (button_rect.width - text.get_width()) // 2
            text_y = button_rect.y + (button_rect.height - text.get_height()) // 2
            window.blit(text, (text_x, text_y))



    def handle_input(self, event):
        """Handles navigation and selection."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                SELECT_OPTION.play()
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                SELECT_OPTION.play()
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                SELECT_OPTION.play()
                return self.options[self.selected_index]  # Return selected option
        return None

    def update(self, events):
        """Updates selection based on player input."""
        for event in events:
            selected_option = self.handle_input(event)
            if selected_option:
                return selected_option  # Return if a selection is made
        return None
