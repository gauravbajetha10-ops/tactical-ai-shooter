# Tactical AI - 2D Stealth Campaign

A top-down tactical stealth shooter built entirely in Python using the Pygame library. This project focuses on advanced enemy AI, dynamic line-of-sight mechanics, and object-oriented architecture.

## 🎯 Project Overview
Instead of standard enemies that blindly walk toward the player, this game features intelligent bots controlled by a **Finite State Machine (FSM)**. Enemies dynamically switch between patrolling, investigating last known player locations, and engaging in combat based on mathematical line-of-sight calculations.

## ✨ Key Technical Features
* **Finite State Machine AI:** Enemies operate on three distinct states:
  * *Patrol:* Generates random movement vectors to guard their territory.
  * *Chase:* Activates when the player enters their detection radius and line-of-sight.
  * *Investigate:* If the player breaks line-of-sight by hiding behind a wall, the AI remembers their last known coordinates and navigates there to search.
* **Dynamic Line-of-Sight & Fog of War:** Utilizes geometric clipline checks to ensure enemies cannot see or shoot through walls. An alpha-channel Fog of War system visually restricts the player's vision, forcing tactical use of cover.
* **Persistent Leaderboard:** Implements local JSON data storage to track, sort, and save the fastest campaign completion times across multiple play sessions.
* **Level Progression & Scaling:** Features 5 uniquely designed levels optimized for a 16:9 (1280x720) aspect ratio with seamless fullscreen scaling. 
* **Object-Oriented Architecture:** The codebase is heavily modularized (separated into Player, Enemy, Wall, and Bullet classes) for clean execution and easy scalability.

## ⚙️ Installation & Setup
To run this game locally on your machine, you will need Python 3 and the Pygame library installed.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gauravbajetha10-ops/tactical-ai-shooter.git](https://github.com/gauravbajetha10-ops/tactical-ai-shooter.git)
   cd tactical-ai-shooter
Install the required dependencies:Bashpip install pygame
Run the game:Bashpython main.py
🎮 ControlsActionKeybindingMoveW, A, S, DAim / ShootMouse / Left ClickReloadRPausePToggle FullscreenFMenu ConfirmENTER or SPACEQuit GameESC📁 Project Structuremain.py: The core game loop, event handling, and UI rendering.player.py: Manages player input, collision resolution, weapons, and auto-healing.enemy.py: Contains the AI bot logic, FSM state updates, and tracking math.bullet.py: Calculates geometric trajectories (angles/velocities) for projectiles.wall.py: Generates static environmental hitboxes.levels.py: Stores the coordinate arrays to procedurally build each of the 5 arenas.settings.py: Centralized configuration for game variables, colors, and resolution.👤 AuthorDeveloped by Gaurav Bajetha/gauravbajetha10-ops as an exploration of Python game development and Artificial Intelligence logic.
