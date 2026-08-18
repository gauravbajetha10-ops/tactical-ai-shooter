from wall import Wall
from enemy import EnemyBot

def get_level_data(level_num):
    
    if level_num == 1:
        walls = [
            Wall(260, 130, 200, 25), Wall(820, 130, 200, 25),
            Wall(260, 530, 200, 25), Wall(820, 530, 200, 25),
            Wall(520, 130, 25, 200), Wall(520, 400, 25, 200)
        ]
        enemies = [EnemyBot(130, 130, "ASSAULT")]

    elif level_num == 2:
        walls = [
            Wall(260, 130, 25, 450),
            Wall(980, 130, 25, 450),
            Wall(285, 340, 695, 25),
            Wall(620, 0, 25, 160),
            Wall(620, 550, 25, 170)
        ]
        enemies = [
            EnemyBot(100, 360, "ASSAULT"), 
            EnemyBot(1160, 360, "MELEE") 
        ]

    elif level_num == 3:
        walls = []
       
        for x in range(200, 1100, 260):
            for y in range(130, 600, 200):
                walls.append(Wall(x, y, 100, 100))
        
        enemies = [
            EnemyBot(100, 60, "ASSAULT"),
            EnemyBot(1160, 60, "ASSAULT"),
            EnemyBot(640, 360, "MELEE")
        ]

    elif level_num == 4:
        walls = [
            Wall(610, 220, 50, 260),
            Wall(500, 330, 270, 50),
            Wall(200, 160, 130, 25),
            Wall(200, 160, 25, 130),
            Wall(940, 160, 130, 25),
            Wall(1045, 160, 25, 130),
            Wall(200, 530, 130, 25),
            Wall(200, 425, 25, 130),
            Wall(940, 530, 130, 25),
            Wall(1045, 425, 25, 130),
        ]
        enemies = [
            EnemyBot(560, 360, "MELEE"),
            EnemyBot(560, 430, "SNIPER"),
            EnemyBot(100, 60, "ASSAULT")
        ]

    elif level_num == 5:
        walls = [
            Wall(0, 180, 460, 25), Wall(820, 180, 460, 25),
            Wall(0, 510, 460, 25), Wall(820, 510, 460, 25),
            Wall(620, 0, 25, 230), Wall(620, 490, 25, 230),
            Wall(260, 300, 130, 120), Wall(880, 300, 130, 120)
        ]
        enemies = [
            EnemyBot(100, 60, "SNIPER"), 
            EnemyBot(1160, 60, "SNIPER"),
            EnemyBot(640, 360, "MELEE"),
            EnemyBot(640, 360, "MELEE"),
            EnemyBot(960, 630, "ASSAULT")
        ]
        
    return walls, enemies