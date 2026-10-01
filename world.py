import math
import random
import pygame
from island import Island
from settings import WIDTH, HEIGHT, WORLD_WIDTH, SKY_TOP, SKY_MID, SKY_BOTTOM, SUN, SUN_GLOW, CLOUD, CLOUD_SHADOW, INK, GRASS_DARK, GRASS_LIGHT
from utils import draw_text, font


class World:
    def __init__(self):
        self.islands = [
            Island(80, 535, 760, 145, 1, "Home Hub"),
            Island(920, 500, 680, 150, 2, "Study Island"),
            Island(1730, 525, 500, 145, 3, "Kindness Trail"),
            Island(2360, 485, 760, 165, 4, "Kindness Garden"),
            Island(3260, 535, 780, 145, 5, "Sky Campus"),
        ]
        rng = random.Random(8)
        self.clouds = [(rng.randint(0, WORLD_WIDTH), rng.randint(72, 315), rng.randint(90, 170)) for _ in range(12)]
        self.sky_surface = self._build_sky_surface()
        self.cloud_surface = self._build_cloud_surface()
        self.sign_font = font(12, True)
        self.place_font = font(11, True)
        self._last_location = None

    def _build_sky_surface(self):
        # V6.1 uses one cached color per pixel row, avoiding the uncovered
        # row gaps that could appear between the old gradient bands.
        surface = pygame.Surface((WIDTH, HEIGHT)).convert()
        split_y = min(430, HEIGHT)
        for y in range(HEIGHT):
            if y <= split_y:
                t = y / max(1, split_y)
                top, bottom = SKY_TOP, SKY_MID
            else:
                t = (y - split_y) / max(1, HEIGHT - split_y - 1)
                top, bottom = SKY_MID, SKY_BOTTOM
            color = tuple(int((1 - t) * top[i] + t * bottom[i]) for i in range(3))
            pygame.draw.line(surface, color, (0, y), (WIDTH - 1, y))
        return surface

    def _build_cloud_surface(self):
        # A reusable cloud tile keeps per-frame drawing tiny.
        tile = pygame.Surface((190, 80), pygame.SRCALPHA)
        pygame.draw.ellipse(tile, CLOUD_SHADOW, (12, 28, 120, 28))
        pygame.draw.ellipse(tile, CLOUD, (24, 22, 72, 36))
        pygame.draw.ellipse(tile, CLOUD, (55, 8, 72, 50))
        pygame.draw.ellipse(tile, CLOUD, (92, 24, 70, 34))
        return tile

    def draw_sky(self, surface, camera_x):
        surface.blit(self.sky_surface, (0, 0))
        sun_x = 1040 - camera_x * 0.08
        pygame.draw.circle(surface, SUN_GLOW, (int(sun_x), 118), 68)
        pygame.draw.circle(surface, SUN, (int(sun_x), 118), 42)
        for x, y, w in self.clouds:
            sx = x - camera_x * 0.22
            if -w < sx < WIDTH + w:
                surface.blit(self.cloud_surface, (int(sx), y - 10))

    def draw(self, surface, camera_x):
        self.draw_sky(surface, camera_x)

        # Parallax islands and distant school silhouettes add depth without extra objects.
        for x, y, w in [(480, 392, 210), (1540, 360, 250), (2800, 350, 235), (3820, 392, 250)]:
            sx = x - camera_x * 0.5
            if -w < sx < WIDTH + w:
                pygame.draw.ellipse(surface, (118, 164, 180), (int(sx), y, w, 54))
                pygame.draw.polygon(surface, (91, 123, 142), [(int(sx + 25), y + 23), (int(sx + w * .8), y + 23), (int(sx + w * .64), y + 72), (int(sx + w * .36), y + 84)])

        for island in self.islands:
            island.draw(surface, camera_x)
        self.draw_landmarks(surface, camera_x)
        self.draw_route_cues(surface, camera_x)
        self.draw_signs(surface, camera_x)

    def draw_route_cues(self, surface, camera_x):
        # Small floating chevrons make the intended route obvious without cluttering the world.
        for gap_x, gap_y in ((850, 503), (1650, 515), (2295, 505), (3180, 510)):
            sx = int(gap_x - camera_x)
            if -120 < sx < WIDTH + 120:
                pygame.draw.circle(surface, (255, 255, 255), (sx, gap_y), 17)
                pygame.draw.circle(surface, (96, 130, 157), (sx, gap_y), 17, 2)
                pygame.draw.polygon(surface, (64, 112, 202), [(sx - 7, gap_y - 7), (sx + 5, gap_y), (sx - 7, gap_y + 7)])
                pygame.draw.polygon(surface, (64, 112, 202), [(sx + 1, gap_y - 7), (sx + 13, gap_y), (sx + 1, gap_y + 7)])

    def draw_signs(self, surface, camera_x):
        signs = [
            ("HOME HUB", 180, 486),
            ("STUDY ISLAND", 1070, 450),
            ("KINDNESS TRAIL", 1820, 478),
            ("KINDNESS GARDEN", 2495, 435),
            ("SKY CAMPUS", 3400, 486),
        ]
        for label, x, y in signs:
            sx = int(x - camera_x)
            if -200 < sx < WIDTH + 200:
                img = self.place_font.render(label, True, INK)
                box = pygame.Rect(sx - 10, y - 7, img.get_width() + 20, 24)
                pygame.draw.rect(surface, (255, 255, 255), box, border_radius=9)
                pygame.draw.rect(surface, (102, 132, 152), box, 1, border_radius=9)
                surface.blit(img, (box.x + 10, box.y + 5))

    def draw_landmarks(self, surface, camera_x):
        # Home Hub: spawn marker + small bench + flag.
        self._draw_flag(surface, camera_x, 225, 501, (64, 112, 202), "START")
        self._draw_bench(surface, camera_x, 335, 510)
        # Study Island: books and a board.
        self._draw_book_stack(surface, camera_x, 1010, 468, (81, 121, 196))
        self._draw_book_stack(surface, camera_x, 1380, 466, (121, 84, 166))
        self._draw_board(surface, camera_x, 1210, 455)
        # Kindness Trail: hearts / flowers make it visually different.
        for x in (1830, 1950, 2070):
            self._draw_flower(surface, camera_x, x, 505)
        # Garden: trees + flowers.
        for x in (2475, 2700, 2930):
            self._draw_tree(surface, camera_x, x, 468)
        for x in range(2520, 3041, 90):
            self._draw_flower(surface, camera_x, x, 458)
        # Sky Campus: a little technical training frame.
        for x in (3430, 3680, 3920):
            self._draw_flag(surface, camera_x, x, 497, (66, 164, 94), "")

    def _draw_flag(self, surface, camera_x, x, y, color, text):
        sx = int(x - camera_x)
        if sx < -60 or sx > WIDTH + 60:
            return
        pygame.draw.line(surface, (92, 77, 65), (sx, y), (sx, y - 40), 3)
        pygame.draw.polygon(surface, color, [(sx, y - 38), (sx + 25, y - 31), (sx, y - 25)])
        if text:
            draw_text(surface, text, (sx - 9, y + 4), 10, color, True)

    def _draw_bench(self, surface, camera_x, x, y):
        sx = int(x - camera_x)
        if -80 < sx < WIDTH + 80:
            pygame.draw.rect(surface, (106, 78, 56), (sx, y + 2, 58, 7), border_radius=3)
            pygame.draw.rect(surface, (91, 68, 51), (sx + 7, y + 9, 6, 14))
            pygame.draw.rect(surface, (91, 68, 51), (sx + 45, y + 9, 6, 14))

    def _draw_book_stack(self, surface, camera_x, x, y, color):
        sx = int(x - camera_x)
        if -90 < sx < WIDTH + 90:
            for i, w in enumerate((36, 30, 42)):
                yy = y - i * 8
                pygame.draw.rect(surface, color if i != 1 else (76, 155, 143), (sx, yy, w, 8), border_radius=2)
                pygame.draw.line(surface, (255, 255, 255), (sx + 5, yy + 2), (sx + w - 5, yy + 2), 1)

    def _draw_board(self, surface, camera_x, x, y):
        sx = int(x - camera_x)
        if -120 < sx < WIDTH + 120:
            pygame.draw.rect(surface, (97, 72, 56), (sx, y, 100, 62), border_radius=5)
            pygame.draw.rect(surface, (239, 245, 241), (sx + 8, y + 7, 84, 42), border_radius=3)
            pygame.draw.line(surface, (80, 110, 169), (sx + 20, y + 21), (sx + 65, y + 21), 2)
            pygame.draw.line(surface, (90, 150, 132), (sx + 20, y + 32), (sx + 75, y + 32), 2)

    def _draw_flower(self, surface, camera_x, x, y):
        sx = int(x - camera_x)
        if -40 < sx < WIDTH + 40:
            pygame.draw.line(surface, GRASS_DARK, (sx, y + 13), (sx, y + 1), 2)
            pygame.draw.circle(surface, (239, 111, 130), (sx - 4, y - 2), 4)
            pygame.draw.circle(surface, (255, 212, 90), (sx + 4, y - 2), 4)
            pygame.draw.circle(surface, (246, 241, 212), (sx, y), 3)

    def _draw_tree(self, surface, camera_x, x, y):
        sx = int(x - camera_x)
        if -70 < sx < WIDTH + 70:
            pygame.draw.rect(surface, (109, 77, 57), (sx - 6, y, 12, 34), border_radius=4)
            pygame.draw.circle(surface, (69, 150, 81), (sx, y - 2), 24)
            pygame.draw.circle(surface, (87, 169, 95), (sx - 18, y + 5), 18)
            pygame.draw.circle(surface, (82, 161, 90), (sx + 18, y + 6), 18)

    def current_location(self, x):
        for island in self.islands:
            if island.x <= x <= island.x + island.width:
                return island.name
        return "Open Sky"
