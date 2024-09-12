import pygame
# utils/helpers.py
def clamp(value, minimum, maximum):
    """
    Clamp a value within a specified range.
    """
    return max(minimum, min(value, maximum))

def load_image(image_path):
    """
    Load an image from a file.
    """
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print(f"Error loading image: {image_path}")
        raise SystemExit(e)
