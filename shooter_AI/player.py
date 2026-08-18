import pygame
from settings import *

class Player:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 15
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        
        self.health = 100 
        self.vision_radius = 1000
         
       
        self.max_ammo = 10
        self.ammo = self.max_ammo
        self.is_reloading = False
        self.reload_time = 1500
        self.reload_start = 0

        
        self.is_auto = False
        self.fire_rate = 300 
        self.last_shot_time = 0

        
        self.last_seen_time = 0
        self.heal_delay = 2000 
        self.heal_rate = 0.5   

    def update_timers(self, is_seen):
        
        current_time = pygame.time.get_ticks()
        
       
        if self.is_reloading:
            if current_time - self.reload_start >= self.reload_time:
                self.ammo = self.max_ammo
                self.is_reloading = False

        
        if is_seen:
            self.last_seen_time = current_time 
        else:
            
            if current_time - self.last_seen_time > self.heal_delay:
                if self.health < 100 and self.health > 0:
                    self.health += self.heal_rate
                    if self.health > 100: self.health = 100

    def reload(self):
        
        if not self.is_reloading and self.ammo < self.max_ammo:
            self.is_reloading = True
            self.reload_start = pygame.time.get_ticks()

    def move(self, walls):
        
        if self.health <= 0: return 
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_s]: dy = self.speed
        if keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_d]: dx = self.speed

        
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: self.rect.right = wall.rect.left
                if dx < 0: self.rect.left = wall.rect.right
        
        if self.rect.left > WIDTH: self.rect.right = 0
        elif self.rect.right < 0: self.rect.left = WIDTH
        self.x = self.rect.centerx

       
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0: self.rect.bottom = wall.rect.top
                if dy < 0: self.rect.top = wall.rect.bottom
        
        if self.rect.top > HEIGHT: self.rect.bottom = 0
        elif self.rect.bottom < 0: self.rect.top = HEIGHT
        self.y = self.rect.centery

    def draw(self, surface):
      
        if self.health > 0:
            pygame.draw.circle(surface, PLAYER_COLOR, (int(self.x), int(self.y)), self.radius)
        else:
            pygame.draw.circle(surface, (50, 50, 50), (int(self.x), int(self.y)), self.radius)