import pygame
import math
import json  
import os   
from settings import *
from player import Player
from bullet import Bullet
from levels import get_level_data


leaderboard_file = "leaderboard.json"
player_name = ""
level_times = [] 
level_start_time = 0
game_state = "START_MENU"


def load_leaderboard():

    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as f:
            return json.load(f)
    return []

def save_score(name, times):
   
    board = load_leaderboard()
    total = round(sum(times), 2) 
    
    player_found = False
    for entry in board:
        if entry["name"] == name:
            player_found = True
            
            if total < entry["total"]:
                entry["times"] = times
                entry["total"] = total
            break
            
    if not player_found:
        board.append({"name": name, "times": times, "total": total})
    
    board = sorted(board, key=lambda x: x["total"])
    
    with open(leaderboard_file, "w") as f:
        json.dump(board, f)


pygame.init()
display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

is_fullscreen = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tactical AI - Full Campaign")
clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 24, bold=True) 
large_font = pygame.font.SysFont("Arial", 72, bold=True)

current_level = 1
MAX_LEVELS = 5

player = None
enemies = []
walls = []
player_bullets = []
enemy_bullets = []

def load_level(level_num):
    
    global player, enemies, walls, player_bullets, enemy_bullets, game_state
    player = Player(50, 550) 
    
    
    player.vision_radius = 200 - (level_num * 25) 
    
    
    if level_num >= 3:
        player.is_auto = True
        player.fire_rate = 150 
        player.max_ammo = 30   
        player.ammo = 30
    elif level_num == 2:
        player.is_auto = True
        player.fire_rate = 400 

    player_bullets = [] 
    enemy_bullets = [] 
    game_state = "PLAYING"
    walls, enemies = get_level_data(level_num)



running = True

while running:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            
            
            if game_state == "START_MENU":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_state = "NAME_INPUT"
                    player_name = "" 
                    
            
            elif game_state == "NAME_INPUT":
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    board = load_leaderboard()
                   
                    name_exists = any(entry['name'] == player_name for entry in board)
                    
                    if name_exists:
                        game_state = "PROFILE_EXISTS" 
                    else:
                        game_state = "PLAYING"
                        current_level = 1
                        level_times = [] 
                        load_level(current_level)
                        level_start_time = pygame.time.get_ticks() 

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1] 
                else:
                    if len(player_name) < 10: 
                        player_name += event.unicode
                        
            
            elif game_state == "PROFILE_EXISTS":
                if event.key == pygame.K_RETURN:
                    game_state = "PLAYING"
                    current_level = 1
                    level_times = [] 
                    load_level(current_level)
                    level_start_time = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    game_state = "NAME_INPUT"
                    player_name = ""

            
            if event.key == pygame.K_p:
                if game_state == "PLAYING":
                    game_state = "PAUSED"
                elif game_state == "PAUSED":
                    game_state = "PLAYING"

           
            if event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            
            
            elif event.key == pygame.K_ESCAPE:
                running = False 

            
            if game_state == "GAME_OVER":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    load_level(current_level)
                    level_start_time = pygame.time.get_ticks() 
                elif event.key == pygame.K_ESCAPE:
                    game_state = "START_MENU" 

            elif game_state == "LEVEL_TRANSITION":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    current_level += 1
                    load_level(current_level)
                    level_start_time = pygame.time.get_ticks() 

            elif game_state == "VICTORY":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    game_state = "START_MENU" 

          
            if game_state == "PLAYING" and player:
                if event.key == pygame.K_r:
                    player.reload()

       
        if game_state == "PLAYING" and player and not player.is_auto:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if player.ammo > 0 and not player.is_reloading:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_bullet = Bullet(player.x, player.y, mouse_x, mouse_y, PLAYER_BULLET_COLOR)
                    player_bullets.append(new_bullet)
                    player.ammo -= 1
                elif player.ammo <= 0:
                    player.reload()

   
    if game_state == "PLAYING" and player:
        mouse_buttons = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()

       
        if mouse_buttons[0] and player.is_auto:
            if current_time - player.last_shot_time > player.fire_rate:
                if player.ammo > 0 and not player.is_reloading:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_bullet = Bullet(player.x, player.y, mouse_x, mouse_y, PLAYER_BULLET_COLOR)
                    player_bullets.append(new_bullet)
                    player.ammo -= 1
                    player.last_shot_time = current_time
                elif player.ammo <= 0:
                    player.reload()

        
        player_is_seen = False
        for enemy in enemies:
            if enemy.state == "CHASE":
                player_is_seen = True
                break 
                
        player.update_timers(player_is_seen)
        player.move(walls)
        
        for enemy in enemies:
            enemy.update(player, enemy_bullets, walls)

        
        all_bullets = [(player_bullets, True), (enemy_bullets, False)]
        for bullet_list, is_player_bullet in all_bullets:
            for bullet in bullet_list[:]:
                bullet.update()
                bullet_rect = pygame.Rect(bullet.x-bullet.radius, bullet.y-bullet.radius, bullet.radius*2, bullet.radius*2)
                
               
                hit_wall = False
                for wall in walls:
                    if bullet_rect.colliderect(wall.rect):
                        bullet_list.remove(bullet)
                        hit_wall = True
                        break
                if hit_wall: continue

                
                if is_player_bullet:
                    for enemy in enemies[:]: 
                        dist = math.hypot(enemy.x - bullet.x, enemy.y - bullet.y)
                        if dist < enemy.radius + bullet.radius:
                            enemy.health -= 25 
                            
                            enemy.x += bullet.dx * 2 
                            enemy.y += bullet.dy * 2
                            enemy.rect.center = (enemy.x, enemy.y)
                            
                            if bullet in bullet_list: bullet_list.remove(bullet)
                            if enemy.health <= 0: enemies.remove(enemy)
                            break 
                elif player.health > 0:
                    dist = math.hypot(player.x - bullet.x, player.y - bullet.y)
                    if dist < player.radius + bullet.radius:
                        player.health -= 10 
                        bullet_list.remove(bullet)

       
        if player.health <= 0:
            game_state = "GAME_OVER"
        elif len(enemies) == 0:
            time_taken = (pygame.time.get_ticks() - level_start_time) / 1000.0
            level_times.append(round(time_taken, 2))
            
            if current_level < MAX_LEVELS:
                game_state = "LEVEL_TRANSITION"
            else:
                game_state = "VICTORY"
                save_score(player_name, level_times)

   
    screen.fill(BG_COLOR)
    for wall in walls: wall.draw(screen)
    for bullet in player_bullets + enemy_bullets: bullet.draw(screen)
    for enemy in enemies: enemy.draw(screen) 
    if player: player.draw(screen)
    
   
    if game_state == "PLAYING" and player:
        fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fog.fill((0, 0, 0, 245)) 

       
        light_radius = player.vision_radius
        light_surf = pygame.Surface((light_radius * 2, light_radius * 2), pygame.SRCALPHA)
        
        step_size = 15 
        for radius in range(light_radius, 0, -step_size):
            strength = int(255 - (radius / light_radius) * 255)
            pygame.draw.circle(light_surf, (255, 255, 255, strength), (light_radius, light_radius), radius)
            
        
        fog.blit(light_surf, (int(player.x) - light_radius, int(player.y) - light_radius), special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(fog, (0, 0))

    
    if player:
        h_txt = font.render(f"Health: {max(0, int(player.health))}", True, UI_TEXT_COLOR)
        a_txt = font.render("RELOADING..." if player.is_reloading else f"Ammo: {player.ammo}/{player.max_ammo}", True, UI_TEXT_COLOR)
        lvl_txt = font.render(f"Level {current_level} - Enemies: {len(enemies)}", True, (255, 100, 100))
        screen.blit(h_txt, (10, 10))
        screen.blit(a_txt, (10, 40))
        screen.blit(lvl_txt, (WIDTH - 250, 10))


    
    if game_state != "PLAYING":
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0,0))
        
        if game_state == "GAME_OVER":
            title_text = large_font.render("GAME OVER", True, (255, 50, 50))
            sub_msg = "Press SPACE to Retry | ESC for Menu" 
            
        elif game_state == "LEVEL_TRANSITION":
            title_text = large_font.render(f"LEVEL {current_level} CLEARED", True, (100, 200, 255))
            sub_msg = "Press SPACE or ENTER for Next Level"
            
        elif game_state == "VICTORY":
            title_text = large_font.render("CAMPAIGN CLEARED!", True, (50, 255, 50))
            sub_msg = "Press SPACE to View Leaderboard"

        elif game_state == "PAUSED":
            title_text = large_font.render("PAUSED", True, (255, 255, 255))
            sub_msg = "Press P to Resume"

        elif game_state == "START_MENU":
            title_text = large_font.render("TACTICAL AI", True, (100, 200, 255))
            sub_msg = "Press SPACE to Start | ESC to Quit"
            
            
            board = load_leaderboard()
            y_offset = HEIGHT // 2 + 80
            lb_title = font.render("--- TOP AGENTS ---", True, (255, 215, 0))
            screen.blit(lb_title, (WIDTH//2 - lb_title.get_width()//2, y_offset))
            
            for i, entry in enumerate(board[:5]):
                txt = f"{i+1}. {entry['name']} - Total: {entry['total']}s"
                score_text = font.render(txt, True, (200, 200, 200))
                screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, y_offset + 30 + (i * 30)))

        elif game_state == "NAME_INPUT":
            title_text = large_font.render("ENTER AGENT NAME", True, (255, 255, 255))
            sub_msg = f"> {player_name}_ <" 
            
            instruct = font.render("Press ENTER to Begin", True, (150, 150, 150))
            screen.blit(instruct, (WIDTH//2 - instruct.get_width()//2, HEIGHT//2 + 100))

        elif game_state == "PROFILE_EXISTS":
            title_text = large_font.render("AGENT PROFILE FOUND", True, (255, 200, 50))
            sub_msg = f"Press ENTER to play as {player_name} | ESC to cancel"
            
           
            board = load_leaderboard()
            best_time = 0
            for entry in board:
                if entry['name'] == player_name:
                    best_time = entry['total']
                    
            best_txt = font.render(f"Previous Best Time: {best_time}s", True, (150, 255, 150))
            screen.blit(best_txt, (WIDTH//2 - best_txt.get_width()//2, HEIGHT//2 + 100))

       
        sub_text = font.render(sub_msg, True, (255, 255, 255))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2 + 50))
        
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()