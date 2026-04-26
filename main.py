import pygame
import sys
from states import StateManager
from game_logic import WIDTH, HEIGHT

def main():
    pygame.init()
    # Safely initialize the audio manager after pygame.init()
    from audio_manager import audio_manager
    audio_manager.init_mixer()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Endless Racer")
    clock = pygame.time.Clock()

    manager = StateManager()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        manager.handle_events(events)
        manager.update()
        manager.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
