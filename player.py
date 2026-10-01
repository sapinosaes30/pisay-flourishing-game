import pygame
from settings import GRAVITY, PLAYER_SPEED, JUMP_SPEED, WORLD_WIDTH, COYOTE_TIME, JUMP_BUFFER_TIME
from utils import clamp


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 34, 54)
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1
        self.coyote_timer = 0.0
        self.jump_buffer = 0.0
        self.anim = 0.0
        self.was_on_ground = False

    def request_jump(self):
        self.jump_buffer = JUMP_BUFFER_TIME

    def update(self, dt, keys, islands):
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        direction = int(right) - int(left)

        target_vx = direction * PLAYER_SPEED
        accel = 1800 if direction else 2100
        if self.vx < target_vx:
            self.vx = min(target_vx, self.vx + accel * dt)
        elif self.vx > target_vx:
            self.vx = max(target_vx, self.vx - accel * dt)

        if direction:
            self.facing = 1 if direction > 0 else -1
            self.anim += dt * (9.0 if self.on_ground else 4.0)
        else:
            self.anim += dt * 2.5

        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)
        self.jump_buffer = max(0.0, self.jump_buffer - dt)

        if self.jump_buffer > 0 and (self.on_ground or self.coyote_timer > 0):
            self.vy = JUMP_SPEED
            self.on_ground = False
            self.coyote_timer = 0.0
            self.jump_buffer = 0.0

        old_bottom = self.y + self.rect.height
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        self.was_on_ground = self.on_ground
        self.on_ground = False

        if self.vy >= 0:
            for island in islands:
                if island.collide(self.rect, old_bottom):
                    surface_y = island.surface_y(self.rect.centerx)
                    self.rect.bottom = int(surface_y)
                    self.y = float(self.rect.y)
                    self.vy = 0.0
                    self.on_ground = True
                    break

        self.x = clamp(self.x, 0, WORLD_WIDTH - self.rect.width)
        self.rect.x = round(self.x)

    def draw(self, surface, camera_x):
        r = self.rect.move(-int(camera_x), 0)
        # Soft ground shadow.
        if self.on_ground:
            pygame.draw.ellipse(surface, (66, 87, 102), (r.x + 2, r.bottom - 3, 30, 7))

        bob = int(1 if self.on_ground and abs(self.vx) > 50 else 0)
        body_y = r.y + 18 + bob
        head_y = r.y + bob
        leg_phase = int(self.anim) % 2 if abs(self.vx) > 50 and self.on_ground else 0

        # Hair / cap.
        pygame.draw.ellipse(surface, (57, 70, 88), (r.x + 6, head_y - 2, 22, 10))
        pygame.draw.ellipse(surface, (241, 196, 156), (r.x + 7, head_y, 20, 21))
        eye_x = r.x + (19 if self.facing > 0 else 12)
        pygame.draw.circle(surface, (31, 43, 56), (eye_x, head_y + 8), 2)
        pygame.draw.line(surface, (80, 52, 44), (r.x + 13, head_y + 15), (r.x + 21, head_y + 15), 1)

        # Shirt and tiny school badge.
        pygame.draw.rect(surface, (64, 112, 202), (r.x + 5, body_y, 24, 27), border_radius=7)
        pygame.draw.rect(surface, (244, 196, 70), (r.x + 10, body_y + 6, 7, 7), border_radius=2)

        leg_offset = 2 if leg_phase else -1
        pygame.draw.rect(surface, (44, 54, 68), (r.x + 6, r.y + 44 + leg_offset, 9, 10), border_radius=3)
        pygame.draw.rect(surface, (44, 54, 68), (r.x + 19, r.y + 44 - leg_offset, 9, 10), border_radius=3)
