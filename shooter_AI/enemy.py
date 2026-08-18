import pygame
import math
import random
from settings import *
from bullet import Bullet

class EnemyBot:
    
    def __init__(self, x, y, bot_type="ASSAULT"):
        self.x = x
        self.y = y
        self.bot_type = bot_type
        self.radius = 15
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        
       
        self.state = "PATROL" 
        self.max_health = 100
        self.health = 100
        self.is_visible_to_player = False
        
        
        if self.bot_type == "ASSAULT":
            self.speed = 2 
            self.health = 100 
            self.detection_radius = 300
            self.fire_rate = 800 
            self.alert_color = ENEMY_ASSAULT
            
        elif self.bot_type == "SNIPER":
            self.speed = 1        
            self.health = 75      
            self.detection_radius = 600 
            self.fire_rate = 2000 
            self.alert_color = ENEMY_SNIPER
            
        elif self.bot_type == "MELEE":
            self.speed = 6.2      
            self.health = 150     
            self.detection_radius = 250
            self.fire_rate = 1000 
            self.alert_color = ENEMY_MELEE
            
       
        self.last_shot_time = 0
        self.last_known_x = None
        self.last_known_y = None
        
       
        self.wander_dx = random.uniform(-1, 1)
        self.wander_dy = random.uniform(-1, 1)
        self.wander_timer = 0
        self.wander_interval = 2000 

    def update(self, player, enemy_bullet_list, walls):
       
        if self.health <= 0: return 

        
        dist = math.hypot(player.x - self.x, player.y - self.y)
        has_line_of_sight = True

       
        for wall in walls:
            if wall.rect.clipline((self.x, self.y), (player.x, player.y)):
                has_line_of_sight = False
                break 

        
        if has_line_of_sight and dist <= player.vision_radius:
            self.is_visible_to_player = True
        else:
            self.is_visible_to_player = False

       
        can_see_player = dist < self.detection_radius and has_line_of_sight and player.health > 0

        if can_see_player:
            self.state = "CHASE"
            self.last_known_x = player.x
            self.last_known_y = player.y
        elif self.last_known_x is not None:
            self.state = "INVESTIGATE"
        else:
            self.state = "PATROL"

        
        dx, dy = 0, 0
        current_time = pygame.time.get_ticks()

        if self.state == "CHASE":
           
            target_dist = math.hypot(player.x - self.x, player.y - self.y)
            if target_dist > 0: dx, dy = (player.x - self.x) / target_dist, (player.y - self.y) / target_dist
            
        elif self.state == "INVESTIGATE":
            
            target_dist = math.hypot(self.last_known_x - self.x, self.last_known_y - self.y)
            if target_dist < 5:
                
                self.last_known_x, self.last_known_y = None, None
                self.state = "PATROL"
            elif target_dist > 0: 
                dx, dy = (self.last_known_x - self.x) / target_dist, (self.last_known_y - self.y) / target_dist
                
        elif self.state == "PATROL":
            
            if current_time - self.wander_timer > self.wander_interval:
                self.wander_dx = random.uniform(-1, 1)
                self.wander_dy = random.uniform(-1, 1)
                
                w_dist = math.hypot(self.wander_dx, self.wander_dy)
                if w_dist > 0: self.wander_dx /= w_dist; self.wander_dy /= w_dist
                
                self.wander_timer = current_time
                self.wander_interval = random.randint(1500, 4000) 
            dx, dy = self.wander_dx * 0.5, self.wander_dy * 0.5

        
        self.rect.x += dx * self.speed
        hit_wall = False 
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                hit_wall = True
                if dx > 0: self.rect.right = wall.rect.left
                if dx < 0: self.rect.left = wall.rect.right
        if self.rect.left < 0 or self.rect.right > WIDTH: hit_wall = True
        self.x = self.rect.centerx

        
        self.rect.y += dy * self.speed
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                hit_wall = True
                if dy > 0: self.rect.bottom = wall.rect.top
                if dy < 0: self.rect.top = wall.rect.bottom
        if self.rect.top < 0 or self.rect.bottom > HEIGHT: hit_wall = True
        self.y = self.rect.centery

        
        if hit_wall:
            if self.state == "PATROL":
                self.wander_timer = 0 
            elif self.state == "INVESTIGATE":
                self.last_known_x, self.last_known_y = None, None
                self.state = "PATROL"

        
        if self.state == "CHASE":
            if self.bot_type != "MELEE":
                if current_time - self.last_shot_time > self.fire_rate:
                    bullet_speed = 15 if self.bot_type == "SNIPER" else 10
                    new_bullet = Bullet(self.x, self.y, player.x, player.y, ENEMY_BULLET_COLOR, speed=bullet_speed)
                    enemy_bullet_list.append(new_bullet)
                    self.last_shot_time = current_time 
            else:
                
                if dist < self.radius + player.radius:
                    if current_time - self.last_shot_time > self.fire_rate:
                        player.health -= 20
                        self.last_shot_time = current_time

    def draw(self, surface):
        
        if self.health > 0 and self.is_visible_to_player:
            if self.state == "CHASE": color = self.alert_color 
            elif self.state == "INVESTIGATE": color = (255, 165, 0) 
            else: color = ENEMY_IDLE 
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)

    def draw_health_bar(self, surface):
       
        ratio = self.health / self.max_health
        if ratio < 0: ratio = 0

        bar_width = self.rect.width  
        bar_height = 5               
        x = self.rect.x
        y = self.rect.y - 10         

        background_rect = pygame.Rect(x, y, bar_width, bar_height)
        foreground_rect = pygame.Rect(x, y, bar_width * ratio, bar_height)

        pygame.draw.rect(surface, (255, 0, 0), background_rect) 
        pygame.draw.rect(surface, (0, 255, 0), foreground_rect)