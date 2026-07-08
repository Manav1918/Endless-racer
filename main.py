import pygame
import sys
import traceback
from states import StateManager
from game_logic import WIDTH, HEIGHT
from storage import get_save_path


def write_crash_log(exc):
    log_path = get_save_path("crash_log.txt")
    details = f"{exc}\n{traceback.format_exc()}"
    print(details)
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(details)
    except Exception as log_exc:
        print(f"Unable to write crash log: {log_exc}")

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
        write_crash_log(e)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
