import pygame
import sys
import os
from states import StateManager
from game_logic import WIDTH, HEIGHT

def capture_screens():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    manager = StateManager()
    
    os.makedirs("docs/screenshots", exist_ok=True)
    
    # 1. Capture Welcome Screen
    manager.update() # Get it started
    manager.draw(screen)
    pygame.display.flip()
    pygame.image.save(screen, "docs/screenshots/welcome.png")
    print("Captured welcome.png")
    
    # 2. Capture Main Menu
    manager.change_state("MainMenu")
    manager.update()
    manager.draw(screen)
    pygame.display.flip()
    pygame.image.save(screen, "docs/screenshots/main_menu.png")
    print("Captured main_menu.png")
    
    # 3. Capture Credits
    manager.change_state("Credits")
    manager.update()
    manager.draw(screen)
    pygame.display.flip()
    pygame.image.save(screen, "docs/screenshots/credits.png")
    print("Captured credits.png")
    
    # 4. Capture Settings
    manager.change_state("Settings")
    manager.update()
    manager.draw(screen)
    pygame.display.flip()
    pygame.image.save(screen, "docs/screenshots/settings.png")
    print("Captured settings.png")
    
    # 5. Capture Game
    manager.change_state("Game")
    # Update a few times to let objects spawn
    for _ in range(30):
        manager.update()
    manager.draw(screen)
    pygame.display.flip()
    pygame.image.save(screen, "docs/screenshots/gameplay.png")
    print("Captured gameplay.png")
    
    pygame.quit()

if __name__ == "__main__":
    capture_screens()
