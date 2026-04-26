import pygame
import random
import math
import os
from game_logic import GameLogic, WIDTH, HEIGHT, BLACK, WHITE, YELLOW
from audio_manager import audio_manager
from storage import load_data, save_data, save_settings

# ─────────────────────────────────────────────────────────────
# Colour palette
# ─────────────────────────────────────────────────────────────
BG_DARK   = (15, 15, 25)
GOLD      = (255, 215, 0)
ACCENT    = (70, 130, 220)
LIGHT     = (210, 220, 255)
BTN_BASE  = (30, 50, 90)
BTN_HOVER = (50, 90, 160)


# ─────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────
def draw_gradient_rect(screen, rect, top_col, bot_col, radius=10):
    surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        r = y / rect.height
        col = (int(top_col[0]+(bot_col[0]-top_col[0])*r),
               int(top_col[1]+(bot_col[1]-top_col[1])*r),
               int(top_col[2]+(bot_col[2]-top_col[2])*r), 255)
        pygame.draw.line(surf, col, (0, y), (rect.width, y))
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255,255,255,255), (0,0,rect.width,rect.height), border_radius=radius)
    surf.blit(mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(surf, rect.topleft)


class Button:
    def __init__(self, cx, y, w, h, text, action=None):
        self.rect   = pygame.Rect(cx - w//2, y, w, h)
        self.text   = text
        self.action = action
        self.hovered = False
        self.font   = pygame.font.SysFont("Arial", 26, bold=True)

    def draw(self, screen):
        top = BTN_HOVER if self.hovered else BTN_BASE
        bot = (80, 130, 220) if self.hovered else (20, 40, 80)
        draw_gradient_rect(screen, self.rect, top, bot, radius=14)
        pygame.draw.rect(screen, ACCENT if self.hovered else (60,80,140),
                         self.rect, width=2, border_radius=14)
        txt = self.font.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
        elif event.type == pygame.FINGERDOWN:
            pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
            if self.rect.collidepoint(pos) and self.action:
                self.action()


# ─────────────────────────────────────────────────────────────
# Star / particle for welcome screen
# ─────────────────────────────────────────────────────────────
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x   = random.randint(0, WIDTH)
        self.y   = random.randint(0, HEIGHT)
        self.spd = random.uniform(0.5, 3.0)
        self.r   = random.randint(1, 3)
        self.alpha = random.randint(80, 255)

    def update(self):
        self.y += self.spd
        if self.y > HEIGHT:
            self.reset()
            self.y = 0

    def draw(self, screen):
        s = pygame.Surface((self.r*2, self.r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, self.alpha), (self.r, self.r), self.r)
        screen.blit(s, (int(self.x) - self.r, int(self.y) - self.r))


# ─────────────────────────────────────────────────────────────
# Base state
# ─────────────────────────────────────────────────────────────
class State:
    def __init__(self, manager): self.mgr = manager
    def handle_events(self, events): pass
    def update(self): pass
    def draw(self, screen): pass


# ─────────────────────────────────────────────────────────────
# 1. Welcome / Splash screen
# ─────────────────────────────────────────────────────────────
class WelcomeScreen(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.stars  = [Star() for _ in range(120)]
        self.timer  = 0
        self.alpha  = 0
        self.logo_bounce = 0.0
        self.road_y = 0.0
        self.car_x  = -80.0
        self.font_big  = pygame.font.SysFont("Impact", 72)
        self.font_sub  = pygame.font.SysFont("Arial", 26, bold=True)
        self.done = False

    def update(self):
        self.timer += 1
        # Fade in logo
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 3)
        # Bounce effect
        self.logo_bounce = math.sin(self.timer * 0.05) * 8
        # Animated road
        self.road_y = (self.road_y + 6) % HEIGHT
        # Car drives across
        if self.timer > 60:
            self.car_x += 4
        for s in self.stars:
            s.update()
        # Auto-transition after ~4 s
        if self.timer > 240:
            self.mgr.change_state("MainMenu")

    def draw(self, screen):
        screen.fill(BG_DARK)
        for s in self.stars:
            s.draw(screen)

        # Animated road strip (preview)
        road_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(road_surf, (40,40,50,180), (WIDTH//2-150, 0, 300, HEIGHT))
        dash, gap = 50, 50
        off = int(self.road_y) % (dash+gap)
        for y0 in range(-dash+off, HEIGHT+dash, dash+gap):
            pygame.draw.rect(road_surf, (255,220,0,160), (WIDTH//2-3, y0, 6, dash))
        screen.blit(road_surf, (0,0))

        # Animated car silhouette
        if self.timer > 60:
            cx = int(self.car_x)
            car_rect = pygame.Rect(cx, HEIGHT//2+20, 60, 100)
            pygame.draw.rect(screen, (220,50,50), car_rect, border_radius=10)
            pygame.draw.ellipse(screen, (255,255,180), (cx+5, HEIGHT//2+25, 16, 10))
            pygame.draw.ellipse(screen, (255,255,180), (cx+39, HEIGHT//2+25, 16, 10))

        # Logo
        title_surf = self.font_big.render("ENDLESS RACER", True, GOLD)
        title_surf.set_alpha(self.alpha)
        ty = int(HEIGHT//3 + self.logo_bounce)
        screen.blit(title_surf, title_surf.get_rect(centerx=WIDTH//2, centery=ty))

        # Sub-text
        if self.timer > 80:
            sub = self.font_sub.render("Tap to Race!", True, LIGHT)
            sub.set_alpha(min(255, (self.timer - 80) * 5))
            screen.blit(sub, sub.get_rect(centerx=WIDTH//2, centery=HEIGHT//2+80))

    def handle_events(self, events):
        for e in events:
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.KEYDOWN):
                if self.timer > 60:
                    self.mgr.change_state("MainMenu")


# ─────────────────────────────────────────────────────────────
# 2. Main Menu
# ─────────────────────────────────────────────────────────────
class MainMenu(State):
    def __init__(self, manager, first_launch=False):
        super().__init__(manager)
        self.data   = load_data()
        self.stars  = [Star() for _ in range(80)]
        self.timer  = 0
        self.road_y = 0.0
        self.font_title = pygame.font.SysFont("Impact", 64)
        self.font_score = pygame.font.SysFont("Arial",  24)
        self.buttons = [
            Button(WIDTH//2, 300, 240, 52, "NEW GAME",  lambda: self.mgr.change_state("Game")),
            Button(WIDTH//2, 362, 240, 52, "CONTINUE",  lambda: self.mgr.change_state("Game", continue_game=True)),
            Button(WIDTH//2, 424, 240, 52, "SCORES",    lambda: self.mgr.change_state("Scores")),
            Button(WIDTH//2, 486, 240, 52, "SETTINGS",  lambda: self.mgr.change_state("Settings")),
            Button(WIDTH//2, 548, 240, 52, "CREDITS",   lambda: self.mgr.change_state("Credits")),
            Button(WIDTH//2, 610, 240, 52, "QUIT",      lambda: self.mgr.quit_game()),
        ]
        # Voice only on very first launch
        if first_launch:
            audio_manager.play_welcome_voice()
        # Soft menu music (restart only if not already playing)
        audio_manager.play_menu_music()

    def handle_events(self, events):
        for e in events:
            for b in self.buttons:
                b.handle_event(e)

    def update(self):
        self.timer  += 1
        self.road_y  = (self.road_y + 3) % HEIGHT
        for s in self.stars: s.update()

    def draw(self, screen):
        screen.fill(BG_DARK)
        for s in self.stars:
            s.draw(screen)

        # Scrolling road
        rs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(rs, (35,35,45,160), (WIDTH//2-150, 0, 300, HEIGHT))
        dash, gap = 50, 50
        off = int(self.road_y) % (dash+gap)
        for y0 in range(-dash+off, HEIGHT+dash, dash+gap):
            pygame.draw.rect(rs, (255,220,0,100), (WIDTH//2-3, y0, 6, dash))
        screen.blit(rs, (0,0))

        # Title with glow
        title = self.font_title.render("ENDLESS RACER", True, GOLD)
        glow_surf = self.font_title.render("ENDLESS RACER", True, (255,200,0))
        glow_surf.set_alpha(40 + int(30*math.sin(self.timer*0.05)))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            screen.blit(glow_surf, glow_surf.get_rect(centerx=WIDTH//2+dx, centery=160+dy))
        screen.blit(title, title.get_rect(centerx=WIDTH//2, centery=160))

        subtitle = self.font_score.render("– Endless Road Ahead –", True, LIGHT)
        screen.blit(subtitle, subtitle.get_rect(centerx=WIDTH//2, centery=220))

        for b in self.buttons:
            b.draw(screen)

        # Score panel
        panel = pygame.Surface((WIDTH-40, 70), pygame.SRCALPHA)
        panel.fill((255,255,255,15))
        screen.blit(panel, (20, HEIGHT - 90))
        pygame.draw.rect(screen, (60,80,140), (20, HEIGHT-90, WIDTH-40, 70), width=1, border_radius=8)
        bs  = self.font_score.render(f"🏆 Best: {int(self.data['best_score'])}", True, GOLD)
        ps  = self.font_score.render(f"⏱ Last: {int(self.data['previous_score'])}", True, LIGHT)
        screen.blit(bs, (40, HEIGHT-80))
        screen.blit(ps, (40, HEIGHT-52))


# ─────────────────────────────────────────────────────────────
# 3. Scores screen
# ─────────────────────────────────────────────────────────────
class ScoresScreen(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.data = load_data()
        self.font_t = pygame.font.SysFont("Impact", 52)
        self.font_n = pygame.font.SysFont("Arial", 28)
        self.back   = Button(WIDTH//2, HEIGHT-100, 200, 50, "◀  BACK",
                             lambda: self.mgr.change_state("MainMenu"))

    def handle_events(self, events):
        for e in events:
            self.back.handle_event(e)

    def draw(self, screen):
        screen.fill(BG_DARK)
        t = self.font_t.render("SCORES", True, GOLD)
        screen.blit(t, t.get_rect(centerx=WIDTH//2, centery=100))

        rows = [
            ("🏆  Best Score",     int(self.data["best_score"])),
            ("⏱  Previous Score", int(self.data["previous_score"])),
        ]
        for i, (label, val) in enumerate(rows):
            y = 220 + i * 100
            draw_gradient_rect(screen, pygame.Rect(40, y, WIDTH-80, 70), BTN_BASE, (20,40,80), 12)
            pygame.draw.rect(screen, ACCENT, (40, y, WIDTH-80, 70), width=2, border_radius=12)
            l  = self.font_n.render(label, True, LIGHT)
            vl = self.font_n.render(str(val), True, GOLD)
            screen.blit(l,  (60, y+10))
            screen.blit(vl, (60, y+40))

        self.back.draw(screen)


# ─────────────────────────────────────────────────────────────
# 4. Credits screen
# ─────────────────────────────────────────────────────────────
class CreditsScreen(State):
    LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "images", "logo.png")

    def __init__(self, manager):
        super().__init__(manager)
        self.timer  = 0
        self.stars  = [Star() for _ in range(60)]
        self.font_t = pygame.font.SysFont("Impact", 52)
        self.font_h = pygame.font.SysFont("Arial",  26, bold=True)
        self.font_n = pygame.font.SysFont("Arial",  22)
        self.back   = Button(WIDTH//2, HEIGHT - 90, 200, 50, "BACK",
                             lambda: self.mgr.change_state("MainMenu"))
        self.logo = None
        if os.path.exists(self.LOGO_PATH):
            try:
                img = pygame.image.load(self.LOGO_PATH).convert_alpha()
                self.logo = pygame.transform.smoothscale(img, (200, 200))
            except Exception as e:
                print(f"Logo load error: {e}")

    def handle_events(self, events):
        for e in events:
            self.back.handle_event(e)

    def update(self):
        self.timer += 1
        for s in self.stars:
            s.update()

    def draw(self, screen):
        screen.fill(BG_DARK)
        for s in self.stars:
            s.draw(screen)

        # Title
        t = self.font_t.render("CREDITS", True, GOLD)
        screen.blit(t, t.get_rect(centerx=WIDTH//2, centery=70))
        pygame.draw.line(screen, ACCENT, (40, 110), (WIDTH-40, 110), 2)

        # Static Logo
        logo_cy = 245
        if self.logo:
            screen.blit(self.logo, self.logo.get_rect(centerx=WIDTH//2, centery=logo_cy))
        else:
            pygame.draw.circle(screen, (30, 60, 120), (WIDTH//2, logo_cy), 90)
            pygame.draw.circle(screen, ACCENT,         (WIDTH//2, logo_cy), 90, width=3)
            fb = pygame.font.SysFont("Impact", 60)
            ct = fb.render("CID", True, (220, 50, 50))
            screen.blit(ct, ct.get_rect(center=(WIDTH//2, logo_cy)))

        # Info card
        panel_y = 370
        draw_gradient_rect(screen, pygame.Rect(30, panel_y, WIDTH-60, 175), BTN_BASE, (20,40,80), 16)
        pygame.draw.rect(screen, ACCENT, (30, panel_y, WIDTH-60, 175), width=2, border_radius=16)

        rows = [
            ("Developed by",            self.font_n, (180, 180, 200)),
            ("Pawan Kumar",             self.font_h, GOLD),
            ("",                        self.font_n, WHITE),
            ("CID – An Education Hub",  self.font_h, LIGHT),
            ("Keep Coding! Keep Learning!",   self.font_n, (180, 180, 200)),
        ]
        y_off = panel_y + 14
        for text, font, col in rows:
            if text:
                surf = font.render(text, True, col)
                screen.blit(surf, surf.get_rect(centerx=WIDTH//2, y=y_off))
            y_off += font.size("A")[1] + 5

        self.back.draw(screen)


# ─────────────────────────────────────────────────────────────
# 5. Settings screen
# ─────────────────────────────────────────────────────────────
class SettingsScreen(State):
    def __init__(self, manager):
        super().__init__(manager)
        # Load saved settings instead of hardcoding defaults
        data = load_data()
        self.music_vol = data.get("music_vol", 50)
        self.sfx_on    = data.get("sfx_on", True)

        self.font_t = pygame.font.SysFont("Impact", 52)
        self.font_n = pygame.font.SysFont("Arial",  24)
        self.back   = Button(WIDTH//2, HEIGHT-100, 200, 50, "BACK",
                             lambda: self.mgr.change_state("MainMenu"))
        self.vol_up = Button(WIDTH//2+80, 290, 60, 44, "+",
                             lambda: self._change_vol(10))
        self.vol_dn = Button(WIDTH//2-80, 290, 60, 44, "-",
                             lambda: self._change_vol(-10))
        self.sfx_btn = Button(WIDTH//2, 390, 220, 50, self._sfx_label(),
                              lambda: self._toggle_sfx())

    def _sfx_label(self):
        return "SFX: ON" if self.sfx_on else "SFX: OFF"

    def _change_vol(self, delta):
        self.music_vol = max(0, min(100, self.music_vol + delta))
        # Apply immediately so user hears the change
        pygame.mixer.music.set_volume(self.music_vol / 100)
        # Persist to disk right away
        save_settings(self.music_vol, self.sfx_on)

    def _toggle_sfx(self):
        self.sfx_on = not self.sfx_on
        self.sfx_btn.text = self._sfx_label()
        save_settings(self.music_vol, self.sfx_on)

    def handle_events(self, events):
        for e in events:
            self.back.handle_event(e)
            self.vol_up.handle_event(e)
            self.vol_dn.handle_event(e)
            self.sfx_btn.handle_event(e)

    def draw(self, screen):
        screen.fill(BG_DARK)
        t = self.font_t.render("SETTINGS", True, GOLD)
        screen.blit(t, t.get_rect(centerx=WIDTH//2, centery=100))

        # Volume bar
        vl = self.font_n.render(f"Music Volume: {self.music_vol}%", True, LIGHT)
        screen.blit(vl, vl.get_rect(centerx=WIDTH//2, centery=240))

        # Progress bar
        bar_x, bar_y, bar_w, bar_h = WIDTH//2 - 100, 262, 200, 12
        pygame.draw.rect(screen, (40, 50, 80), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill_w = int(bar_w * self.music_vol / 100)
        if fill_w > 0:
            pygame.draw.rect(screen, ACCENT, (bar_x, bar_y, fill_w, bar_h), border_radius=6)
        pygame.draw.rect(screen, LIGHT, (bar_x, bar_y, bar_w, bar_h), width=1, border_radius=6)

        self.vol_dn.draw(screen)
        self.vol_up.draw(screen)
        self.sfx_btn.draw(screen)
        self.back.draw(screen)


# ─────────────────────────────────────────────────────────────
# 5. Game state
# ─────────────────────────────────────────────────────────────
class GameState(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.game = GameLogic()
        # Start full-volume racing music
        audio_manager.play_game_music()

    def load_save(self, score, level):
        self.game.score = score
        self.game.level = level
        self.game.speed_multiplier = 1.0 + (level - 1) * 0.25

    def handle_events(self, events):
        self.game.handle_events(events)
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.mgr.change_state("Pause")

    def update(self):
        self.game.update()
        if self.game.is_game_over:
            data = load_data()
            best = max(data["best_score"], self.game.score)
            # Preserve settings when saving scores
            save_data(best, self.game.score,
                      music_vol=data.get("music_vol", 50),
                      sfx_on=data.get("sfx_on", True))
            self.mgr.change_state("GameOver", final_score=self.game.score, best=best)

    def draw(self, screen):
        self.game.draw(screen)


# ─────────────────────────────────────────────────────────────
# 6. Pause menu
# ─────────────────────────────────────────────────────────────
class PauseMenu(State):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_t  = pygame.font.SysFont("Impact", 72)
        self.buttons = [
            Button(WIDTH//2, 320, 240, 52, "▶  RESUME",      lambda: self.mgr.change_state("Game", resume=True)),
            Button(WIDTH//2, 390, 240, 52, "🏠  MAIN MENU",  lambda: self.mgr.change_state("MainMenu")),
            Button(WIDTH//2, 460, 240, 52, "🚪  QUIT GAME",  lambda: self.mgr.quit_game()),
        ]
        audio_manager.pause_music()

    def handle_events(self, events):
        for e in events:
            for b in self.buttons: b.handle_event(e)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.mgr.change_state("Game", resume=True)

    def draw(self, screen):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0,0,0,160))
        screen.blit(ov, (0,0))
        t = self.font_t.render("PAUSED", True, GOLD)
        screen.blit(t, t.get_rect(centerx=WIDTH//2, centery=200))
        for b in self.buttons: b.draw(screen)


# ─────────────────────────────────────────────────────────────
# 7. Game Over
# ─────────────────────────────────────────────────────────────
class GameOver(State):
    def __init__(self, manager, final_score=0, best=0):
        super().__init__(manager)
        self.final_score = final_score
        self.best        = best
        self.font_t  = pygame.font.SysFont("Impact", 64)
        self.font_n  = pygame.font.SysFont("Arial",  28)
        self.stars   = [Star() for _ in range(60)]
        self.timer   = 0
        self.buttons = [
            Button(WIDTH//2, 520, 220, 52, "🔄  PLAY AGAIN", lambda: self.mgr.change_state("Game")),
            Button(WIDTH//2, 590, 220, 52, "🏠  MENU",       lambda: self.mgr.change_state("MainMenu")),
        ]

    def update(self):
        self.timer += 1
        for s in self.stars: s.update()

    def handle_events(self, events):
        for e in events:
            for b in self.buttons: b.handle_event(e)

    def draw(self, screen):
        screen.fill((25, 5, 5))
        for s in self.stars: s.draw(screen)

        t = self.font_t.render("GAME OVER", True, (255, 80, 80))
        screen.blit(t, t.get_rect(centerx=WIDTH//2, centery=160))

        draw_gradient_rect(screen, pygame.Rect(40, 250, WIDTH-80, 220), (40,10,10), (20,5,5), 16)
        pygame.draw.rect(screen, (120,30,30), (40, 250, WIDTH-80, 220), width=2, border_radius=16)

        rows = [
            ("Your Score", int(self.final_score), LIGHT),
            ("Best Score", int(self.best),        GOLD),
        ]
        for i, (label, val, col) in enumerate(rows):
            y = 280 + i*80
            screen.blit(self.font_n.render(label, True, (180,180,180)), (70, y))
            screen.blit(self.font_n.render(str(val), True, col),        (70, y+32))

        for b in self.buttons: b.draw(screen)


# ─────────────────────────────────────────────────────────────
# State Manager
# ─────────────────────────────────────────────────────────────
class StateManager:
    def __init__(self):
        self._game_state  = None
        self._first_launch = True   # voice-over guard
        self.states = {
            "Welcome": WelcomeScreen(self),
            "Scores":  ScoresScreen(self),
            "Credits": CreditsScreen(self),
        }
        self._build_settings()  # always fresh so saved values load
        self._build_main_menu(first_launch=True)
        self.current_name  = "Welcome"
        self.current_state = self.states["Welcome"]

    def _build_main_menu(self, first_launch=False):
        self.states["MainMenu"] = MainMenu(self, first_launch=first_launch)

    def _build_settings(self):
        self.states["Settings"] = SettingsScreen(self)

    def change_state(self, name, resume=False, continue_game=False,
                     final_score=0, best=0):
        if name == "Game":
            if resume:
                audio_manager.resume_music()
                self.current_name  = "Game"
                self.current_state = self._game_state
                return
            gs = GameState(self)
            if continue_game:
                data  = load_data()
                score = data.get("previous_score", 0)
                level = max(1, int(score // 200))
                gs.load_save(score, level)
            self._game_state = gs
            self.states["Game"] = gs

        elif name == "Pause":
            self.states["Pause"] = PauseMenu(self)

        elif name == "GameOver":
            self.states["GameOver"] = GameOver(self, final_score=final_score, best=best)
            audio_manager.stop_music()

        elif name == "Settings":
            self._build_settings()  # reload saved values every time

        elif name == "Credits":
            self.states["Credits"] = CreditsScreen(self)

        elif name == "MainMenu":
            self._build_main_menu(first_launch=False)

        self.current_name  = name
        self.current_state = self.states[name]

    def quit_game(self):
        pygame.quit()
        import sys
        sys.exit()

    def handle_events(self, events):
        for e in events:
            # Handle Android hardware back button
            if e.type == pygame.KEYDOWN and e.key == pygame.K_AC_BACK:
                if self.current_name == "MainMenu":
                    self.quit_game()
                elif self.current_name == "Game":
                    self.change_state("Pause")
                else:
                    self.change_state("MainMenu")
        self.current_state.handle_events(events)

    def update(self):
        self.current_state.update()

    def draw(self, screen):
        # Draw paused game beneath pause overlay
        if self.current_name == "Pause" and self._game_state:
            self._game_state.draw(screen)
        self.current_state.draw(screen)
