
from game.assets import Assets , HEIGHT,WIDTH

Assets.load_fonts()

class CopyRightText():
    
    def draw_copyright(self, window):
        # Copyright text settings
        text = "weebhub©2025"
        rendered_text = Assets.PRESS_START_FONT.render(text, True, (255, 255, 255))
        text_rect = rendered_text.get_rect()
        text_rect.bottomright = (WIDTH - 10, HEIGHT - 10)  # Position at bottom-right
        window.blit(rendered_text, text_rect)