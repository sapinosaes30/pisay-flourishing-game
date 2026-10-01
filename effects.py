import math
import random
import pygame
from settings import GOLD, SUCCESS, WHITE


class Spark:
    def __init__(self, x, y, vx, vy, color, life=0.55, size=4):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = float(vx), float(vy)
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 360 * dt
        self.life -= dt

    def draw(self, surface, camera_x):
        if self.life <= 0:
            return
        scale = max(0.25, self.life / self.max_life)
        size = max(1, int(self.size * scale))
        pygame.draw.circle(surface, self.color, (int(self.x - camera_x), int(self.y)), size)


class Effects:
    def __init__(self):
        self.sparks = []
        self.toast = ""
        self.toast_timer = 0.0
        self.toast_kind = "success"

    def burst(self, x, y, color=GOLD, count=16, speed=125):
        count = min(count, 24)
        for i in range(count):
            angle = random.random() * math.tau
            force = random.uniform(speed * 0.55, speed)
            self.sparks.append(
                Spark(
                    x, y,
                    math.cos(angle) * force,
                    math.sin(angle) * force - 50,
                    color,
                    life=random.uniform(0.35, 0.75),
                    size=random.randint(2, 5),
                )
            )

    def notify(self, text, seconds=2.5, kind="success"):
        self.toast = text
        self.toast_timer = seconds
        self.toast_kind = kind

    def update(self, dt):
        for spark in self.sparks:
            spark.update(dt)
        self.sparks[:] = [spark for spark in self.sparks if spark.life > 0]
        self.toast_timer = max(0.0, self.toast_timer - dt)

    def draw_sparks(self, surface, camera_x):
        for spark in self.sparks:
            spark.draw(surface, camera_x)

    def toast_color(self):
        return SUCCESS if self.toast_kind == "success" else GOLD if self.toast_kind == "info" else WHITE
