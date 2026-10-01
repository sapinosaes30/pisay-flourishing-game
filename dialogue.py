import pygame
from settings import ACCENT, PANEL, INK, MUTED
from utils import font, wrap_text, rounded_panel


class DialogueBox:
    def __init__(self):
        self.active = False
        self.name = ""
        self.lines = []
        self.index = 0
        self.title_font = font(24, True)
        self.body_font = font(19)
        self.hint_font = font(13, True)

    def start(self, name, text):
        self.name = name
        self.lines = text if isinstance(text, list) else [text]
        self.index = 0
        self.active = True

    def advance(self):
        if not self.active:
            return
        self.index += 1
        if self.index >= len(self.lines):
            self.active = False

    def draw(self, surface):
        if not self.active:
            return
        panel = pygame.Rect(55, 490, surface.get_width() - 110, 180)
        rounded_panel(surface, panel, PANEL, ACCENT, 18, True, 3)

        pygame.draw.rect(surface, ACCENT, (panel.x + 18, panel.y + 17, 7, 76), border_radius=4)
        surface.blit(self.title_font.render(self.name, True, ACCENT), (panel.x + 36, panel.y + 16))

        body_x = panel.x + 36
        body_y = panel.y + 58
        lines = wrap_text(self.lines[self.index], self.body_font, panel.width - 72)
        for i, line in enumerate(lines[:4]):
            surface.blit(self.body_font.render(line, True, INK), (body_x, body_y + i * 26))

        page = f"{self.index + 1}/{len(self.lines)}"
        surface.blit(self.hint_font.render(page, True, MUTED), (panel.x + 24, panel.bottom - 29))
        hint = "E / ENTER / SPACE  •  continue"
        hint_img = self.hint_font.render(hint, True, MUTED)
        surface.blit(hint_img, (panel.right - hint_img.get_width() - 22, panel.bottom - 29))
