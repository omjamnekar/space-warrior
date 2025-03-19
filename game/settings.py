import os

# Game Constants
WIDTH, HEIGHT = 1300, 850
FPS = 60

MAX_HP=500
MAX_XP=500

# Colors (RGBA format for overlays)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OVERLAY_COLOR = (0, 0, 0, 150)  # Semi-transparent black

# Player & Game Speeds
PLAYER_SPEED = 5
BULLET_SPEED = 7
METEOR_SPEED = 3

# Meteor Speed Range
METEOR_MIN_SPEED = 2  # ✅ Add this
METEOR_MAX_SPEED = 5  # ✅ Add this

# Best Score Handling
BEST_SCORE_FILE = "best_score.txt"

def load_best_score():
    """Load the best score from a file, return 0 if the file does not exist or is invalid."""
    try:
        with open(BEST_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Default score if file is missing or invalid

def save_best_score(score):
    """Save the best score to a file."""
    with open(BEST_SCORE_FILE, "w") as file:
        file.write(str(score))

