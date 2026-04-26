import pygame
import random
import os

WIDTH = 480
HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
ROAD_COLOR = (45, 45, 55)

ROAD_LEFT = WIDTH // 2 - 150
ROAD_RIGHT = WIDTH // 2 + 150
ROAD_WIDTH = 300
LANE_W = ROAD_WIDTH // 3

ENVIRONMENTS = [
    {"name": "Mountain",   "sky_top": (70,130,180),  "sky_bot": (135,206,235), "ground": (120,120,130), "type": "mountain"},
    {"name": "Green Land", "sky_top": (100,180,255), "sky_bot": (150,220,255), "ground": (34,139,34),   "type": "grassland"},
    {"name": "Jungle",     "sky_top": (0,50,0),      "sky_bot": (10,80,10),    "ground": (0,80,0),      "type": "jungle"},
    {"name": "Desert",     "sky_top": (255,140,0),   "sky_bot": (255,200,100), "ground": (210,180,100), "type": "desert"},
]


class Decoration:
    def __init__(self, x, y, env_type):
        self.x = x
        self.y = y
        self.env_type = env_type

    def update(self, speed):
        self.y += speed

    def is_off_screen(self):
        return self.y > HEIGHT + 100

    def draw(self, screen):
        ix, iy = int(self.x), int(self.y)
        if self.env_type == "mountain":
            pygame.draw.circle(screen, (130, 130, 140), (ix, iy), 22)
            pygame.draw.circle(screen, (110, 110, 120), (ix - 10, iy), 14)
            # Waterfall strip
            pygame.draw.rect(screen, (100, 180, 255), (ix + 15, iy - 40, 5, 50))
        elif self.env_type == "grassland":
            pygame.draw.rect(screen, (101, 67, 33), (ix - 5, iy - 10, 10, 30))
            pygame.draw.circle(screen, (0, 120, 0), (ix, iy - 20), 22)
            pygame.draw.circle(screen, (0, 160, 0), (ix - 12, iy - 28), 14)
        elif self.env_type == "jungle":
            pygame.draw.rect(screen, (60, 30, 10), (ix - 5, iy - 20, 10, 45))
            pygame.draw.circle(screen, (0, 80, 0),  (ix, iy - 35), 28)
            pygame.draw.circle(screen, (0, 100, 0), (ix - 18, iy - 20), 18)
            pygame.draw.circle(screen, (10, 60, 0), (ix + 15, iy - 22), 16)
        elif self.env_type == "desert":
            pygame.draw.rect(screen, (0, 130, 60), (ix - 5, iy - 45, 10, 50))
            pygame.draw.rect(screen, (0, 130, 60), (ix - 22, iy - 28, 17, 8))
            pygame.draw.rect(screen, (0, 130, 60), (ix - 22, iy - 36, 8, 10))
            pygame.draw.rect(screen, (0, 130, 60), (ix + 5,  iy - 22, 17, 8))
            pygame.draw.rect(screen, (0, 130, 60), (ix + 14, iy - 32, 8, 12))


def _draw_car(surface, color, w, h):
    """Draw a polished top-down car procedurally."""
    dark  = (max(0,color[0]-70), max(0,color[1]-70), max(0,color[2]-70))
    light = (min(255,color[0]+60), min(255,color[1]+60), min(255,color[2]+60))

    # --- Body ---
    pygame.draw.rect(surface, color, (4, 4, w-8, h-8), border_radius=10)

    # --- Roof (darker centre panel) ---
    pygame.draw.rect(surface, dark, (9, 24, w-18, h-46), border_radius=8)

    # --- Racing stripe down the middle ---
    pygame.draw.rect(surface, light, (w//2-3, 6, 6, h-12))

    # --- Front windshield ---
    pygame.draw.rect(surface, (160, 220, 245), (9, 24, w-18, 16), border_radius=5)

    # --- Rear window ---
    pygame.draw.rect(surface, (160, 220, 245), (9, h-38, w-18, 13), border_radius=5)

    # --- Headlights ---
    pygame.draw.ellipse(surface, (255, 255, 170), (5,  6,  14, 9))
    pygame.draw.ellipse(surface, (255, 255, 170), (w-19, 6,  14, 9))

    # --- Tail-lights ---
    pygame.draw.ellipse(surface, (255, 30, 30), (5,  h-15, 14, 9))
    pygame.draw.ellipse(surface, (255, 30, 30), (w-19, h-15, 14, 9))

    # --- Wheels (with hub detail) ---
    WC, HC = (15, 15, 15), (70, 70, 70)
    for wx, wy in [(0, 10), (w-8, 10), (0, h-28), (w-8, h-28)]:
        pygame.draw.rect(surface, WC, (wx, wy, 8, 18), border_radius=3)
        pygame.draw.rect(surface, HC, (wx+2, wy+5, 4, 8), border_radius=2)


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, is_player=True):
        super().__init__()
        self.is_player = is_player
        self.w, self.h = 50, 90
        if is_player:
            color = (220, 50, 50)   # red
        else:
            color = (random.randint(40,210), random.randint(40,210), random.randint(40,210))
        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        _draw_car(self.image, color, self.w, self.h)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        if self.is_player:
            self.rect.x += self.speed_x
            self.rect.left  = max(self.rect.left,  ROAD_LEFT + 5)
            self.rect.right = min(self.rect.right, ROAD_RIGHT - 5)



class TouchControls:
    SIZE = 70
    MARGIN = 20

    def __init__(self):
        m = self.MARGIN
        s = self.SIZE
        self.left_rect  = pygame.Rect(m, HEIGHT - s - m, s, s)                    # bottom-left
        self.right_rect = pygame.Rect(WIDTH - s - m, HEIGHT - s - m, s, s)        # bottom-right
        self.left_pressed = self.right_pressed = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.left_rect.collidepoint(event.pos):  self.left_pressed  = True
            if self.right_rect.collidepoint(event.pos): self.right_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.left_rect.collidepoint(event.pos):  self.left_pressed  = False
            if self.right_rect.collidepoint(event.pos): self.right_pressed = False
        elif event.type == pygame.FINGERDOWN:
            pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
            if self.left_rect.collidepoint(pos):  self.left_pressed  = True
            if self.right_rect.collidepoint(pos): self.right_pressed = True
        elif event.type == pygame.FINGERUP:
            pos = (int(event.x * WIDTH), int(event.y * HEIGHT))
            if self.left_rect.collidepoint(pos):  self.left_pressed  = False
            if self.right_rect.collidepoint(pos): self.right_pressed = False

    def draw(self, screen):
        for rect, is_left, pressed in [
            (self.left_rect,  True,  self.left_pressed),
            (self.right_rect, False, self.right_pressed),
        ]:
            # Background bubble
            s = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
            alpha = 200 if pressed else 100
            bg_col = (80, 160, 255, alpha) if pressed else (255, 255, 255, alpha)
            pygame.draw.rect(s, bg_col, (0, 0, self.SIZE, self.SIZE), border_radius=14)
            pygame.draw.rect(s, (255, 255, 255, 180), (0, 0, self.SIZE, self.SIZE),
                             width=2, border_radius=14)
            screen.blit(s, rect.topleft)

            # Draw triangle arrow using polygon
            cx, cy = rect.centerx, rect.centery
            aw, ah = 22, 28   # arrow width and half-height
            if is_left:
                pts = [(cx + aw//2, cy - ah//2),
                       (cx + aw//2, cy + ah//2),
                       (cx - aw//2, cy)]
            else:
                pts = [(cx - aw//2, cy - ah//2),
                       (cx - aw//2, cy + ah//2),
                       (cx + aw//2, cy)]
            arrow_col = (255, 255, 255) if not pressed else (255, 220, 50)
            pygame.draw.polygon(screen, arrow_col, pts)



class GameLogic:
    def __init__(self):
        self.player = Car(WIDTH // 2, HEIGHT - 150, is_player=True)
        self.all_sprites = pygame.sprite.Group(self.player)
        self.enemies     = pygame.sprite.Group()

        self.score = 0.0
        self.level = 1
        self.speed_multiplier = 1.0
        self.road_y = 0.0
        self.is_game_over = False
        self.environment_idx = 0

        self.decorations = []
        self.dec_timer = 0

        self.touch = TouchControls()

        self.transition_alpha = 0
        self.transitioning = False
        self.transition_text = ""

    # ---------- helpers ----------
    def _spawn_enemy(self):
        x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 60)
        y = random.randint(-400, -80)
        enemy = Car(x, y, is_player=False)
        enemy.speed_y = random.uniform(3, 6)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def _spawn_decoration(self):
        env_type = ENVIRONMENTS[self.environment_idx]["type"]
        for x in [random.randint(5, ROAD_LEFT - 30), random.randint(ROAD_RIGHT + 10, WIDTH - 30)]:
            self.decorations.append(Decoration(x, random.randint(-100, -10), env_type))

    # ---------- event / update ----------
    def handle_events(self, events):
        for event in events:
            self.touch.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  self.player.speed_x = -8
                if event.key == pygame.K_RIGHT: self.player.speed_x =  8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT  and self.player.speed_x < 0: self.player.speed_x = 0
                if event.key == pygame.K_RIGHT and self.player.speed_x > 0: self.player.speed_x = 0

        spd = 8 * self.speed_multiplier
        keys = pygame.key.get_pressed()
        if self.touch.left_pressed  or keys[pygame.K_LEFT]:  self.player.speed_x = -spd
        elif self.touch.right_pressed or keys[pygame.K_RIGHT]: self.player.speed_x =  spd
        else:
            if not self.touch.left_pressed and not self.touch.right_pressed:
                if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    self.player.speed_x = 0

    def update(self):
        if self.is_game_over:
            return

        self.score += 0.15 * self.speed_multiplier

        # Level-up check
        new_level = 1 + int(self.score // 200)
        if new_level > self.level:
            self.level = new_level
            self.speed_multiplier = 1.0 + (self.level - 1) * 0.25
            new_env = (self.level - 1) % len(ENVIRONMENTS)
            if new_env != self.environment_idx:
                self.environment_idx = new_env
                self.decorations.clear()
                self.transition_alpha = 255
                self.transitioning = True
                self.transition_text = f"Entering {ENVIRONMENTS[new_env]['name']}!"

        if self.transitioning:
            self.transition_alpha = max(0, self.transition_alpha - 4)
            if self.transition_alpha == 0:
                self.transitioning = False

        self.road_y = (self.road_y + 10 * self.speed_multiplier) % HEIGHT

        self.all_sprites.update()

        scroll = 7 * self.speed_multiplier
        for enemy in list(self.enemies):
            enemy.rect.y += int(scroll)
            if enemy.rect.top > HEIGHT + 50:
                enemy.kill()
                self.score += 5

        self.dec_timer += 1
        if self.dec_timer >= 30:
            self.dec_timer = 0
            self._spawn_decoration()
        for d in self.decorations:
            d.update(scroll)
        self.decorations = [d for d in self.decorations if not d.is_off_screen()]

        max_enemies = 2 + self.level
        if len(self.enemies) < max_enemies and random.random() < 0.02 * self.speed_multiplier:
            self._spawn_enemy()

        hits = pygame.sprite.spritecollide(self.player, self.enemies, False,
                                           pygame.sprite.collide_rect_ratio(0.72))
        if hits:
            self.is_game_over = True

    # ---------- drawing ----------
    def _draw_bg(self, screen):
        env = ENVIRONMENTS[self.environment_idx]
        st, sb = env["sky_top"], env["sky_bot"]
        # Gradient sides
        for y in range(HEIGHT):
            r = float(y) / HEIGHT
            col = (int(st[0]+(sb[0]-st[0])*r), int(st[1]+(sb[1]-st[1])*r), int(st[2]+(sb[2]-st[2])*r))
            pygame.draw.line(screen, col, (0, y), (ROAD_LEFT, y))
            pygame.draw.line(screen, col, (ROAD_RIGHT, y), (WIDTH, y))

        # Environment-specific scenery on sides
        if env["type"] == "mountain":
            for mx, mh in [(80,200),(40,160),(420,220),(440,150)]:
                pts = [(mx-60, HEIGHT//2),(mx, HEIGHT//2-mh),(mx+60, HEIGHT//2)]
                pygame.draw.polygon(screen, (100,100,120), pts)
                sp = [(mx-20, HEIGHT//2-mh+40),(mx, HEIGHT//2-mh),(mx+20, HEIGHT//2-mh+40)]
                pygame.draw.polygon(screen, (235,240,255), sp)

    def _draw_road(self, screen):
        pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        pygame.draw.rect(screen, (240,240,240), (ROAD_LEFT, 0, 8, HEIGHT))
        pygame.draw.rect(screen, (240,240,240), (ROAD_RIGHT - 8, 0, 8, HEIGHT))
        dash, gap = 50, 50
        offset = int(self.road_y) % (dash + gap)
        for y0 in range(-dash + offset, HEIGHT + dash, dash + gap):
            pygame.draw.rect(screen, YELLOW, (ROAD_LEFT + LANE_W - 3, y0, 6, dash))
            pygame.draw.rect(screen, YELLOW, (ROAD_LEFT + LANE_W*2 - 3, y0, 6, dash))

    def draw(self, screen):
        self._draw_bg(screen)
        for d in self.decorations:
            d.draw(screen)
        self._draw_road(screen)
        self.all_sprites.draw(screen)
        self.touch.draw(screen)

        # HUD
        f36 = pygame.font.SysFont(None, 36)
        f28 = pygame.font.SysFont(None, 28)
        screen.blit(f36.render(f"Score: {int(self.score)}", True, WHITE), (10, 10))
        screen.blit(f28.render(f"Lv.{self.level}  |  {ENVIRONMENTS[self.environment_idx]['name']}", True, YELLOW), (10, 50))
        screen.blit(f28.render("ESC = Pause", True, (200,200,200)), (WIDTH - 130, 10))

        # Environment transition flash
        if self.transition_alpha > 0:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((255, 255, 255, self.transition_alpha))
            screen.blit(ov, (0, 0))
            if self.transition_alpha > 60:
                tf = pygame.font.SysFont(None, 48)
                ts = tf.render(self.transition_text, True, BLACK)
                screen.blit(ts, ts.get_rect(center=(WIDTH//2, HEIGHT//2)))
