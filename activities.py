import math
import random
import pygame
from settings import MARKER_BLUE, MARKER_GOLD, MARKER_GREEN, GOLD, PURPLE, TEAL, INK, WHITE
from utils import draw_centered_text, draw_text, font


ITEM_STYLES = {
    "school_supply": {
        "label": "CLASS SUPPLY",
        "full_name": "Classroom Supply",
        "color": (239, 164, 52),
        "ring": MARKER_GOLD,
    },
    "research_note": {
        "label": "RESEARCH NOTE",
        "full_name": "Research Note",
        "color": (103, 83, 182),
        "ring": PURPLE,
    },
}


class Collectible:
    def __init__(self, x, y, kind, item_id, label, area, quest_id):
        self.x, self.y = x, y
        self.kind = kind
        self.item_id = item_id
        self.label = label
        self.area = area
        self.quest_id = quest_id
        self.taken = False
        self.phase = random.random() * math.tau
        self.style = ITEM_STYLES[kind]
        self.small_font = font(11, True)

    def update(self, dt):
        self.phase += dt * 2.6

    def draw(self, surface, camera_x, highlighted=False, show_label=False):
        if self.taken:
            return
        x = int(self.x - camera_x)
        if x < -90 or x > surface.get_width() + 90:
            return
        yy = int(self.y + 4 * math.sin(self.phase))
        ring = self.style["ring"] if highlighted else self.style["color"]
        pygame.draw.circle(surface, (255, 255, 255), (x, yy), 21 if highlighted else 18)
        pygame.draw.circle(surface, ring, (x, yy), 21 if highlighted else 18, 3)

        if self.kind == "school_supply":
            # Oversized pencil-case icon + ruler strip = unmistakably a school supply.
            pygame.draw.rect(surface, (248, 221, 114), (x - 12, yy - 9, 24, 18), border_radius=4)
            pygame.draw.rect(surface, (224, 90, 72), (x - 12, yy - 9, 24, 5), border_radius=2)
            pygame.draw.line(surface, (76, 116, 194), (x - 7, yy - 2), (x + 7, yy + 10), 4)
            pygame.draw.polygon(surface, (223, 182, 135), [(x + 7, yy + 10), (x + 11, yy + 13), (x + 4, yy + 10)])
            pygame.draw.line(surface, (117, 128, 139), (x - 8, yy - 4), (x + 7, yy - 4), 1)
        elif self.kind == "research_note":
            paper = [(x - 11, yy - 13), (x + 7, yy - 13), (x + 11, yy - 8), (x + 11, yy + 13), (x - 11, yy + 13)]
            pygame.draw.polygon(surface, (246, 244, 232), paper)
            pygame.draw.polygon(surface, (210, 215, 228), [(x + 7, yy - 13), (x + 7, yy - 8), (x + 11, yy - 8)])
            pygame.draw.line(surface, PURPLE, (x - 6, yy - 7), (x + 6, yy - 7), 2)
            pygame.draw.line(surface, TEAL, (x - 6, yy - 1), (x + 6, yy - 1), 2)
            pygame.draw.line(surface, (82, 111, 174), (x - 6, yy + 5), (x + 6, yy + 5), 2)
            pygame.draw.line(surface, (214, 103, 133), (x + 7, yy - 5), (x + 7, yy + 7), 3)

        if highlighted or show_label:
            tag = self.style["label"]
            img = self.small_font.render(tag, True, INK)
            box = pygame.Rect(x - img.get_width() // 2 - 8, yy - 48, img.get_width() + 16, 22)
            pygame.draw.rect(surface, WHITE, box, border_radius=8)
            pygame.draw.rect(surface, ring, box, 2, border_radius=8)
            surface.blit(img, (box.x + 8, box.y + 4))


class ActivityCheckpoint:
    def __init__(self, checkpoint_id, x, y, name, quest_id):
        self.checkpoint_id = checkpoint_id
        self.x, self.y = x, y
        self.name = name
        self.quest_id = quest_id
        self.active = False
        self.phase = random.random() * math.tau
        self.label_font = font(12, True)

    def update(self, dt):
        self.phase += dt * 2.8

    def near(self, player, limit=105):
        return math.hypot(self.x - player.rect.centerx, self.y - player.rect.bottom) < limit

    def draw(self, surface, camera_x, available=False):
        x = int(self.x - camera_x)
        if x < -100 or x > surface.get_width() + 100:
            return
        y = int(self.y + 7 * math.sin(self.phase))
        ring = MARKER_GREEN if self.active else MARKER_GOLD if available else MARKER_BLUE

        pygame.draw.circle(surface, (34, 50, 67), (x, y + 10), 19)
        pygame.draw.circle(surface, ring, (x, y), 22, 4)
        pygame.draw.rect(surface, (92, 108, 124), (x - 10, y - 13, 20, 26), border_radius=4)
        pygame.draw.circle(surface, WHITE, (x, y - 4), 6)
        draw_centered_text(surface, str(self.checkpoint_id), (x, y - 4), 12, ring, True)

        label = f"{self.checkpoint_id}  {self.name}"
        img = self.label_font.render(label, True, INK)
        box = pygame.Rect(x - img.get_width() // 2 - 8, y - 56, img.get_width() + 16, 24)
        pygame.draw.rect(surface, WHITE, box, border_radius=8)
        pygame.draw.rect(surface, ring, box, 2, border_radius=8)
        surface.blit(img, (box.x + 8, box.y + 5))

        if available:
            pulse = int(25 + 8 * math.sin(self.phase * 2.0))
            pygame.draw.circle(surface, ring, (x, y), pulse, 1)

    def draw_prompt(self, surface, camera_x, visible=False):
        if not visible or self.active:
            return
        x = int(self.x - camera_x)
        if x < -180 or x > surface.get_width() + 180:
            return
        y = int(self.y - 41)
        img = font(13, True).render("E / ENTER  activate", True, INK)
        box = pygame.Rect(x - img.get_width() // 2 - 9, y - 13, img.get_width() + 18, 24)
        pygame.draw.rect(surface, WHITE, box, border_radius=8)
        pygame.draw.rect(surface, MARKER_GOLD, box, 2, border_radius=8)
        surface.blit(img, (box.x + 9, box.y + 4))
