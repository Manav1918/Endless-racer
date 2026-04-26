import os
import pygame
from storage import load_data

class AudioManager:
    def __init__(self):
        self.audio_dir = os.path.join(os.path.dirname(__file__), "assets", "audio")
        self._voice_channel = None
        self._music_loaded  = False
        self._initialized   = False

    def init_mixer(self):
        """Called once after pygame.init() to safely start the mixer."""
        if not self._initialized:
            try:
                pygame.mixer.init(frequency=22050)
                self._initialized = True
            except Exception as e:
                print(f"[Audio] Mixer init failed: {e}")

    def _music_path(self):
        # Prefer WAV (generated), fallback to mp3
        for name in ("music.wav", "music.mp3"):
            p = os.path.join(self.audio_dir, name)
            if os.path.exists(p):
                return p
        return None

    # ── Voice-over ────────────────────────────────────────────
    def play_welcome_voice(self):
        self.init_mixer()
        path = os.path.join(self.audio_dir, "welcome.mp3")
        if not os.path.exists(path):
            return
        try:
            snd = pygame.mixer.Sound(path)
            self._voice_channel = snd.play()
        except Exception as e:
            print(f"[Audio] voice error: {e}")

    # ── Music ─────────────────────────────────────────────────
    def _load_music(self):
        self.init_mixer()
        path = self._music_path()
        if path is None:
            print("[Audio] No music file found in assets/audio/")
            return False
        try:
            pygame.mixer.music.load(path)
            self._music_loaded = True
            return True
        except Exception as e:
            print(f"[Audio] music load error: {e}")
            return False

    def play_menu_music(self):
        """Soft background music for menus (respects saved volume)."""
        self.init_mixer()
        if not self._music_loaded:
            if not self._load_music():
                return
        saved_vol = load_data().get("music_vol", 50) / 100 * 0.6  # menu = 60% of saved
        pygame.mixer.music.set_volume(max(0.0, min(1.0, saved_vol)))
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def play_game_music(self):
        """Full-volume racing music during gameplay (respects saved volume)."""
        self.init_mixer()
        if not self._music_loaded:
            if not self._load_music():
                return
        saved_vol = load_data().get("music_vol", 50) / 100
        pygame.mixer.music.set_volume(max(0.0, min(1.0, saved_vol)))
        pygame.mixer.music.play(-1)

    def pause_music(self):
        if self._initialized:
            pygame.mixer.music.pause()

    def resume_music(self):
        if self._initialized:
            pygame.mixer.music.unpause()

    def stop_music(self):
        if self._initialized:
            pygame.mixer.music.stop()
        self._music_loaded = False   # force reload next time

audio_manager = AudioManager()
