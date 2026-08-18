import pygame

class Wall:
    """Represents a static environmental obstacle that blocks movement and vision."""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (80, 80, 100) 

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)