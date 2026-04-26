import pygame
import sys
from states import StateManager
from game_logic import WIDTH, HEIGHT

def main():
    # Crash logging for Android debugging
    try:
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
    except Exception as e:
        # Write crash log to a place where we can hopefully see it
        import traceback
        with open("crash_log.txt", "w") as f:
            f.write(str(e) + "\n")
            f.write(traceback.format_exc())
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
