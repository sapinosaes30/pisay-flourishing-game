import math
import random
import pygame
from settings import GRASS, GRASS_DARK, GRASS_LIGHT, SOIL, SOIL_DARK, SOIL_LIGHT, STONE, STONE_DARK


class Island:
    def __init__(self, x, y, width, height=150, seed=1, name="Island"):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.name = name
        rng = random.Random(seed)
        self.top_points = []
        segments = 12
        for i in range(segments + 1):
            px = x + width * i / segments
            wobble = rng.randint(-6, 7) if 0 < i < segments else 0
            self.top_points.append((int(px), int(y + wobble)))

        self.body_points = [
            (x + width, y + 20),
            (x + width - 38, y + height - 20),
            (x + width * 0.66, y + height - 2),
            (x + width * 0.42, y + height + 14),
            (x + width * 0.17, y + height - 15),
            (x, y + 25),
        ]
        self.rng = rng
        self.surface = self._build_surface()

    def _build_surface(self):
        surface = pygame.Surface((self.width + 8, self.height + 30), pygame.SRCALPHA)
        ox, oy = self.x, self.y
        top = [(px - ox + 2, py - oy + 10) for px, py in self.top_points]
        body = [(px - ox + 2, py - oy + 10) for px, py in self.body_points]

        pygame.draw.polygon(surface, SOIL_DARK, body)
        inner = [(px, py - 4) for px, py in body]
        pygame.draw.polygon(surface, SOIL, inner)

        # Warm rock bands for depth.
        pygame.draw.lines(surface, SOIL_LIGHT, False,
                          [(x1, y1 + 28) for x1, y1 in body[:4]], 3)
        pygame.draw.lines(surface, (119, 79, 61), False,
                          [(x1, y1 + 54) for x1, y1 in body[1:5]], 2)

        pygame.draw.polygon(surface, GRASS_DARK,
                            [(px, py + 3) for px, py in top])
        pygame.draw.polygon(surface, GRASS, top)
        pygame.draw.lines(surface, GRASS_LIGHT, False, top, 2)

        # Tiny rock flecks are cheap because the art is generated once.
        for _ in range(max(7, self.width // 90)):
            rx = self.rng.randint(18, max(19, self.width - 24))
            ry = self.rng.randint(65, max(66, self.height - 14))
            col = STONE if _ % 2 else STONE_DARK
            pygame.draw.circle(surface, col, (rx, ry), self.rng.randint(2, 4))

        # Grass tufts.
        for _ in range(max(5, self.width // 150)):
            gx = self.rng.randint(18, max(19, self.width - 18))
            gy = self.rng.randint(14, 28)
            pygame.draw.line(surface, GRASS_DARK, (gx, gy + 8), (gx - 3, gy), 2)
            pygame.draw.line(surface, GRASS_DARK, (gx, gy + 8), (gx + 3, gy + 1), 2)
        return surface

    def surface_y(self, world_x):
        if self.width <= 0:
            return self.y
        t = max(0.0, min(1.0, (world_x - self.x) / self.width))
        # Match the stylized wobble visually while keeping the collision surface simple.
        return self.y + 7 * math.sin(t * 8.0)

    def collide(self, player_rect, old_bottom):
        if player_rect.right <= self.x or player_rect.left >= self.x + self.width:
            return False
        surface_y = self.surface_y(player_rect.centerx)
        return old_bottom <= surface_y + 10 and player_rect.bottom >= surface_y

    def draw(self, surface, camera_x):
        sx = int(self.x - camera_x)
        if sx > surface.get_width() + 10 or sx + self.width < -10:
            return
        surface.blit(self.surface, (sx, int(self.y - 10)))
