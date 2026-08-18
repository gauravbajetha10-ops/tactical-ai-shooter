import pygame
import math

class Bullet:
    
    def __init__(self, x, y, target_x, target_y, color, speed=10):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 4
        self.color = color
        
        angle = math.atan2(target_y - y, target_x - x)
         
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
       
        self.x += self.dx
        self.y += self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)