import math
import pygame
from settings import MARKER_BLUE, MARKER_GOLD, MARKER_GREEN
from utils import distance, draw_text, font


class NPC:
    def __init__(self, name, x, y, color, dialogue, hair_color=(70, 55, 45), hair_style="short", role="Teacher", clothing_style="normal"):
        self.name = name
        self.x, self.y = x, y
        self.color = color
        self.dialogue = dialogue
        self.hair_color = hair_color
        self.hair_style = hair_style
        self.role = role
        self.clothing_style = clothing_style
        self.rect = pygame.Rect(x, y - 58, 42, 58)
        self.phase = 0.0
        self.marker_font = font(17, True)
        self.name_font = font(14, True)

    def update(self, dt):
        self.phase += dt * 2.4

    def near(self, player):
        return distance((self.x, self.y), (player.rect.centerx, player.rect.bottom)) < 105

    def draw_hair_back(self, surface, r):
        hair = self.hair_color
        if self.hair_style == "short":
            pygame.draw.ellipse(surface, hair, (r.x + 4, r.y - 4, 34, 25))
            pygame.draw.rect(surface, hair, (r.x + 4, r.y + 9, 5, 11), border_radius=2)
            pygame.draw.rect(surface, hair, (r.x + 33, r.y + 9, 5, 11), border_radius=2)
        else:
            pygame.draw.ellipse(surface, hair, (r.x + 7, r.y - 1, 28, 17))

    def draw_hair_front(self, surface, r):
        # Deliberately ends above the eye line so hair never overlays the face.
        hair = self.hair_color
        if self.hair_style == "short":
            pygame.draw.ellipse(surface, hair, (r.x + 7, r.y - 2, 28, 10))
        else:
            pygame.draw.ellipse(surface, hair, (r.x + 9, r.y, 24, 7))

    def draw(self, surface, camera_x, player, quest_state="none"):
        r = self.rect.move(-int(camera_x), 0)
        bob = int(1.5 * math.sin(self.phase))
        r.y += bob

        self.draw_hair_back(surface, r)
        pygame.draw.ellipse(surface, (241, 196, 156), (r.x + 8, r.y, 26, 23))

        # Face first; features remain readable even with the front hair cap.
        pygame.draw.circle(surface, (45, 45, 45), (r.x + 15, r.y + 10), 1)
        pygame.draw.circle(surface, (45, 45, 45), (r.x + 27, r.y + 10), 1)
        pygame.draw.line(surface, (102, 66, 60), (r.x + 17, r.y + 16), (r.x + 25, r.y + 16), 1)

        if self.name == "Ma'am Zen":
            pygame.draw.rect(surface, (222, 226, 232), (r.x + 10, r.y + 14, 22, 7), border_radius=3)
            pygame.draw.line(surface, (188, 194, 201), (r.x + 10, r.y + 17), (r.x + 6, r.y + 14), 1)
            pygame.draw.line(surface, (188, 194, 201), (r.x + 32, r.y + 17), (r.x + 36, r.y + 14), 1)

        self.draw_hair_front(surface, r)

        # Distinct bodies/wardrobes.
        if self.name == "Ma'am Eileen":
            pygame.draw.rect(surface, self.color, (r.x + 4, r.y + 20, 34, 22), border_radius=7)
            pygame.draw.polygon(surface, self.color,
                                [(r.x + 3, r.y + 35), (r.x + 39, r.y + 35), (r.x + 33, r.y + 50), (r.x + 9, r.y + 50)])
            pygame.draw.circle(surface, (255, 236, 214), (r.x + 12, r.y + 28), 3)
        elif self.name == "Ma'am Zen":
            pygame.draw.rect(surface, self.color, (r.x + 4, r.y + 20, 34, 29), border_radius=6)
            pygame.draw.rect(surface, (228, 233, 239), (r.x + 19, r.y + 21, 4, 25))
            pygame.draw.circle(surface, (176, 137, 89), (r.x + 29, r.y + 32), 3)
        else:
            pygame.draw.rect(surface, self.color, (r.x + 4, r.y + 20, 34, 29), border_radius=6)
            pygame.draw.line(surface, (245, 214, 92), (r.centerx, r.y + 25), (r.centerx, r.y + 44), 3)
            pygame.draw.line(surface, (26, 44, 72), (r.x + 7, r.y + 33), (r.x + 35, r.y + 33), 2)

        pygame.draw.rect(surface, (48, 55, 65), (r.x + 7, r.y + 48, 10, 8), border_radius=2)
        pygame.draw.rect(surface, (48, 55, 65), (r.x + 23, r.y + 48, 10, 8), border_radius=2)

        # Nameplate is restrained and only appears when the player is close.
        if self.near(player):
            name_img = self.name_font.render(self.name, True, (255, 255, 255))
            box = pygame.Rect(r.centerx - name_img.get_width() // 2 - 8, r.top - 36, name_img.get_width() + 16, 22)
            pygame.draw.rect(surface, (43, 61, 79), box, border_radius=8)
            surface.blit(name_img, (box.x + 8, box.y + 3))
            pygame.draw.circle(surface, MARKER_BLUE, (r.centerx, r.bottom + 12), 11)
            draw_text(surface, "E", (r.centerx - 4, r.bottom + 4), 12, (255, 255, 255), True)

        if quest_state in ("available", "ready"):
            symbol = "!" if quest_state == "available" else "?"
            color = MARKER_GOLD if quest_state == "available" else MARKER_GREEN
            bob2 = int(2 * math.sin(self.phase * 2.0))
            cx, cy = r.centerx, r.top - 20 + bob2
            pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 16)
            pygame.draw.circle(surface, color, (cx, cy), 12)
            img = self.marker_font.render(symbol, True, (255, 255, 255))
            surface.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2 - 1))
        elif quest_state == "active":
            cx, cy = r.centerx, r.top - 17
            pygame.draw.polygon(surface, MARKER_BLUE, [(cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)])
