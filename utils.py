import math
import pygame

_FONT_CACHE = {}
_TEXT_CACHE = {}
_TEXT_CACHE_LIMIT = 3072


def clamp(value, low, high):
    return max(low, min(high, value))


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def font(size, bold=False):
    key = (size, bold)
    cached = _FONT_CACHE.get(key)
    if cached is None:
        cached = pygame.font.SysFont("segoeui", size, bold=bold)
        _FONT_CACHE[key] = cached
    return cached


def text_surface(text, size=24, color=(31, 43, 56), bold=False):
    key = (text, size, bold, color)
    img = _TEXT_CACHE.get(key)
    if img is None:
        img = font(size, bold).render(text, True, color)
        if len(_TEXT_CACHE) >= _TEXT_CACHE_LIMIT:
            _TEXT_CACHE.pop(next(iter(_TEXT_CACHE)))
        _TEXT_CACHE[key] = img
    return img


def draw_text(surface, text, pos, size=24, color=(31, 43, 56), bold=False):
    img = text_surface(text, size, color, bold)
    surface.blit(img, pos)
    return img


def rounded_panel(surface, rect, fill, border, radius=14, shadow=True, border_width=2):
    if shadow:
        pygame.draw.rect(surface, (30, 48, 66), rect.move(4, 5), border_radius=radius)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    if border_width:
        pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)


def wrap_text(text, font_obj, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else line + " " + word
        if font_obj.size(test)[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_centered_text(surface, text, center, size=20, color=(31,43,56), bold=False):
    img = text_surface(text, size, color, bold)
    surface.blit(img, (center[0] - img.get_width() // 2, center[1] - img.get_height() // 2))
    return img
