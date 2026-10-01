import pygame
from settings import WIDTH, HEIGHT, PANEL, PANEL_SOFT, ACCENT, ACCENT_DARK, INK, MUTED, SUCCESS, GOLD, WARNING
from utils import draw_text, font, wrap_text, rounded_panel


class QuestUI:
    def __init__(self):
        self.guide_open = False
        self.title_font = font(19, True)
        self.body_font = font(15)
        self.body_bold = font(15, True)
        self.section_font = font(11, True)
        self.guide_title_font = font(28, True)
        self.guide_body = font(14)
        self.guide_body_bold = font(15, True)
        self.guide_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.guide_overlay.fill((13, 26, 40, 165))

    def toggle_guide(self):
        self.guide_open = not self.guide_open

    def draw_tracker(self, surface, quest, location):
        panel = pygame.Rect(WIDTH - 392, 14, 365, 342)
        rounded_panel(surface, panel, PANEL, ACCENT, 17, True, 2)
        draw_text(surface, "CURRENT QUEST", (panel.x + 17, panel.y + 13), 12, ACCENT, True)

        if not quest:
            draw_text(surface, "No active quest", (panel.x + 17, panel.y + 50), 20, INK, True)
            draw_text(surface, "Look for the teacher with !", (panel.x + 17, panel.y + 82), 15, MUTED)
            draw_text(surface, "Your next quest will unlock there.", (panel.x + 17, panel.y + 104), 15, MUTED)
            return

        draw_text(surface, quest.title, (panel.x + 17, panel.y + 43), 20, INK, True)
        state_label = {
            quest.ACTIVE: "IN PROGRESS",
            quest.READY: "READY TO TURN IN",
            quest.COMPLETE: "COMPLETE",
            quest.AVAILABLE: "AVAILABLE",
        }[quest.state]
        state_color = SUCCESS if quest.state == quest.READY else ACCENT
        badge = pygame.Rect(panel.right - 141, panel.y + 13, 124, 23)
        pygame.draw.rect(surface, PANEL_SOFT, badge, border_radius=9)
        draw_text(surface, state_label, (badge.x + 8, badge.y + 5), 9, state_color, True)

        draw_text(surface, "OBJECTIVE", (panel.x + 17, panel.y + 76), 10, ACCENT, True)
        lines = wrap_text(quest.compact_objective(), self.body_font, panel.width - 34)
        for i, line in enumerate(lines[:2]):
            draw_text(surface, line, (panel.x + 17, panel.y + 92 + i * 19), 15, INK)

        y = panel.y + 138
        draw_text(surface, "PROGRESS", (panel.x + 17, y), 10, ACCENT, True)
        draw_text(surface, quest.progress_text, (panel.x + 90, y - 2), 16, SUCCESS if quest.state == quest.READY else INK, True)

        # Progress pips make the numbers readable even from a distance.
        for i in range(quest.target):
            cx = panel.x + 165 + i * 24
            pygame.draw.circle(surface, SUCCESS if i < quest.progress else (205, 216, 226), (cx, y + 7), 6)

        draw_text(surface, "AREA", (panel.x + 17, y + 29), 10, ACCENT, True)
        draw_text(surface, quest.area, (panel.x + 62, y + 27), 14, INK, True)

        draw_text(surface, "TARGET", (panel.x + 17, y + 54), 10, ACCENT, True)
        draw_text(surface, quest.target_label, (panel.x + 65, y + 52), 13, INK, True)

        draw_text(surface, "NEXT STEP", (panel.x + 17, y + 80), 10, ACCENT, True)
        step = f"Return to {quest.turn_in}." if quest.state == quest.READY else quest.next_step
        step_lines = wrap_text(step, self.body_bold, panel.width - 34)
        for i, line in enumerate(step_lines[:2]):
            draw_text(surface, line, (panel.x + 17, y + 96 + i * 17), 14, INK, True)

        draw_text(surface, "RETURN TO", (panel.x + 17, y + 130), 10, ACCENT, True)
        draw_text(surface, quest.turn_in, (panel.x + 91, y + 128), 14, INK, True)

    def draw_goal_banner(self, surface, text):
        panel = pygame.Rect(20, 92, 455, 70)
        rounded_panel(surface, panel, PANEL, ACCENT, 14, True, 2)
        draw_text(surface, "WHAT DO I DO NOW?", (panel.x + 14, panel.y + 9), 11, ACCENT_DARK, True)
        lines = wrap_text(text, font(16, True), panel.width - 28)
        for i, line in enumerate(lines[:2]):
            draw_text(surface, line, (panel.x + 14, panel.y + 29 + i * 18), 16, INK, True)

    def draw_guide(self, surface, current_quest, location):
        surface.blit(self.guide_overlay, (0, 0))
        panel = pygame.Rect(105, 42, WIDTH - 210, HEIGHT - 84)
        rounded_panel(surface, panel, PANEL, ACCENT, 21, True, 3)
        draw_text(surface, "HOW TO PLAY", (panel.x + 28, panel.y + 22), 28, ACCENT_DARK, True)
        draw_text(surface, "TAB / G  •  close", (panel.right - 150, panel.y + 28), 13, MUTED, True)

        left = panel.x + 30
        mid = panel.x + 405
        right = panel.x + 700
        y = panel.y + 79

        draw_text(surface, "MOVE", (left, y), 16, INK, True)
        draw_text(surface, "A / D or Arrow Keys  =  move", (left, y + 28), 14, INK)
        draw_text(surface, "W / Up / Space  =  jump", (left, y + 49), 14, INK)

        draw_text(surface, "INTERACT", (left, y + 89), 16, INK, True)
        draw_text(surface, "E / Enter  =  talk / interact", (left, y + 117), 14, INK)
        draw_text(surface, "TAB / G  =  open this guide", (left, y + 138), 14, INK)

        draw_text(surface, "YOUR GOAL", (mid, y), 16, INK, True)
        goal = "Explore the floating islands, talk to teachers, complete quests, and discover new areas."
        for i, line in enumerate(wrap_text(goal, self.guide_body, 275)):
            draw_text(surface, line, (mid, y + 28 + i * 19), 14, INK)

        draw_text(surface, "QUEST FLOW", (mid, y + 99), 16, INK, True)
        steps = [
            "1. Find the teacher with !.",
            "2. Accept the quest.",
            "3. Follow AREA + NEXT STEP.",
            "4. Finish the objective.",
            "5. Return to the listed teacher.",
        ]
        for i, step in enumerate(steps):
            draw_text(surface, step, (mid, y + 127 + i * 20), 13, INK)

        draw_text(surface, "MARKERS", (right, y), 16, INK, True)
        markers = [
            ("!", GOLD, "New quest"),
            ("?", SUCCESS, "Quest ready to turn in"),
            ("◆", ACCENT, "Current quest giver"),
            ("●", ACCENT, "Quest target / destination"),
        ]
        for i, (symbol, color, label) in enumerate(markers):
            cy = y + 31 + i * 28
            pygame.draw.circle(surface, color, (right + 8, cy), 10)
            draw_text(surface, symbol, (right + 2, cy - 8), 13, (255, 255, 255), True)
            draw_text(surface, label, (right + 26, cy - 7), 13, INK)

        bottom = panel.bottom - 127
        pygame.draw.line(surface, (208, 219, 229), (panel.x + 28, bottom - 16), (panel.right - 28, bottom - 16), 1)
        draw_text(surface, "CURRENT LOCATION", (left, bottom), 10, MUTED, True)
        draw_text(surface, location, (left, bottom + 22), 17, INK, True)
        draw_text(surface, "CURRENT QUEST", (mid, bottom), 10, MUTED, True)
        draw_text(surface, current_quest.title if current_quest else "Talk to a teacher with !.", (mid, bottom + 22), 15, INK, True)
        if current_quest:
            current = f"Return to {current_quest.turn_in}." if current_quest.state == current_quest.READY else current_quest.next_step
            draw_text(surface, current, (mid, bottom + 46), 13, MUTED)

        warn = pygame.Rect(panel.x + 28, panel.bottom - 54, panel.width - 56, 29)
        pygame.draw.rect(surface, (255, 247, 236), warn, border_radius=9)
        draw_text(surface, "IMPORTANT: Falling off an island respawns you at Home Hub.", (warn.x + 12, warn.y + 7), 12, WARNING, True)
