import asyncio
import math
import pygame
from settings import WIDTH, HEIGHT, FPS, INTERACT_DISTANCE, WORLD_WIDTH, INK, MUTED, LOCATION_BADGE, FALL_THRESHOLD, CAMERA_SMOOTH, MARKER_BLUE, MARKER_GOLD, SUCCESS, WARNING
from player import Player
from world import World
from npc import NPC
from dialogue import DialogueBox
from quests import Quest
from activities import Collectible, ActivityCheckpoint
from quest_ui import QuestUI
from effects import Effects
from utils import draw_text, font, distance, rounded_panel


class Game:
    def __init__(self, screen):
        # Display initialization stays in main.py; this constructor only receives the ready screen.
        self.screen = screen
        self.world = World()
        self.spawn_x, self.spawn_y = 260, 470
        self.player = Player(self.spawn_x, self.spawn_y)
        self.dialogue = DialogueBox()
        self.quest_ui = QuestUI()
        self.effects = Effects()
        self.running = True

        self.location = "Home Hub"
        self.previous_location = "Home Hub"
        self.camera_x = 0.0
        self.message = ""
        self.message_timer = 0.0
        self.message_surface = None
        self.message_box = None
        self.frame_count = 0

        self.npcs = [
            NPC(
                "Ma'am Eileen", 470, 535, (226, 132, 100),
                [
                    "Hello, darling! Welcome to our floating school.",
                    "May naiwan tayong classroom supplies sa Study Island. Can you help, darling?",
                    "Hanapin ang 3 supplies. Pag nahanap mo lahat, balik dito kay Ma'am Eileen, okay?",
                ],
                hair_color=(92, 55, 35), hair_style="short", role="Warm homeroom teacher", clothing_style="skirt",
            ),
            NPC(
                "Ma'am Zen", 1190, 500, (74, 82, 105),
                [
                    "Good. You are here.",
                    "I need three research notes from Study Island. They are marked clearly.",
                    "Read the information you recover. Return to me when all three are collected.",
                ],
                hair_color=(135, 135, 140), hair_style="short", role="Algebra / Research teacher",
            ),
            NPC(
                "Sir Tanoy", 1530, 500, (67, 112, 171),
                [
                    "Uy! Ready for a hands-on challenge?",
                    "Run the Sky Campus practice circuit. Hit Beacon 1, then 2, then 3.",
                    "Mess up? No drama. Try again. Learning by doing, remember?",
                ],
                hair_color=(135, 135, 140), hair_style="very_short", role="Hands-on learning teacher",
            ),
        ]

        self.quests = [
            Quest(
                quest_id="eileen_supplies",
                title="Ready, Darlings!",
                objective="Find 3 CLASSROOM SUPPLIES on Study Island.",
                giver="Ma'am Eileen", turn_in="Ma'am Eileen", target=3,
                progress_kind="school_supply", area="Study Island",
                next_step="Find the remaining CLASS SUPPLIES on Study Island.",
                reward_text="Ay, thank you, darling! The classroom is ready again. You really helped me out.",
                target_label="CLASS SUPPLY",
                destination_text="Study Island • classroom supplies",
            ),
            Quest(
                quest_id="zen_research",
                title="Research Relay",
                objective="Collect 3 RESEARCH NOTES on Study Island.",
                giver="Ma'am Zen", turn_in="Ma'am Zen", target=3,
                progress_kind="research_note", area="Study Island",
                next_step="Find the remaining RESEARCH NOTES on Study Island.",
                reward_text="All three notes are back. Good. Careful work matters in research.",
                prerequisite="eileen_supplies",
                target_label="RESEARCH NOTE",
                destination_text="Study Island • research notes",
            ),
            Quest(
                quest_id="tanoy_circuit",
                title="Hands-On Circuit",
                objective="Activate 3 PRACTICE BEACONS on Sky Campus, in order.",
                giver="Sir Tanoy", turn_in="Sir Tanoy", target=3,
                progress_kind="checkpoint", area="Sky Campus",
                next_step="Reach PRACTICE BEACON 1 on Sky Campus.",
                reward_text="Nice run! Three beacons, one lesson: keep trying until it works.",
                prerequisite="zen_research",
                target_label="PRACTICE BEACON",
                destination_text="Sky Campus • practice circuit",
            ),
        ]

        self.collectibles = [
            Collectible(1040, 446, "school_supply", "Supply 1", "Study Island", "eileen_supplies"),
            Collectible(1260, 444, "school_supply", "Supply 2", "Study Island", "eileen_supplies"),
            Collectible(1490, 442, "school_supply", "Supply 3", "Study Island", "eileen_supplies"),
            Collectible(1110, 410, "research_note", "Research 1", "Study Island", "zen_research"),
            Collectible(1340, 404, "research_note", "Research 2", "Study Island", "zen_research"),
            Collectible(1515, 402, "research_note", "Research 3", "Study Island", "zen_research"),
        ]

        self.checkpoints = [
            ActivityCheckpoint(1, 3450, 494, "Practice Beacon 1", "tanoy_circuit"),
            ActivityCheckpoint(2, 3700, 492, "Practice Beacon 2", "tanoy_circuit"),
            ActivityCheckpoint(3, 3940, 490, "Practice Beacon 3", "tanoy_circuit"),
        ]

        self.goal_locked = False
        self.set_message("Start at Home Hub: talk to Ma'am Eileen. Look for the gold !", 4)

    # ---------- Quest helpers ----------
    def current_quest(self):
        for quest in self.quests:
            if quest.state in (Quest.ACTIVE, Quest.READY):
                return quest
        return None

    def next_available_quest(self):
        for quest in self.quests:
            if quest.state == Quest.AVAILABLE and quest.is_unlocked(self.quests):
                return quest
        return None

    def quest_for_teacher(self, name):
        for quest in self.quests:
            if quest.giver == name:
                return quest
        return None

    def marker_state_for_teacher(self, name):
        quest = self.quest_for_teacher(name)
        if not quest or quest.state == Quest.COMPLETE:
            return "none"
        if quest.state == Quest.READY:
            return "ready"
        if quest.state == Quest.ACTIVE:
            return "active"
        if quest.state == Quest.AVAILABLE and quest.is_unlocked(self.quests) and self.current_quest() is None:
            return "available"
        return "none"

    def goal_text(self):
        quest = self.current_quest()
        if quest is None:
            next_quest = self.next_available_quest()
            return f"Talk to {next_quest.giver}." if next_quest else "Explore the floating islands and discover what is next."
        if quest.state == Quest.READY:
            return f"Return to {quest.turn_in}."
        return quest.next_step

    def target_point(self):
        quest = self.current_quest()
        if quest is None:
            nxt = self.next_available_quest()
            if nxt:
                teacher = next((n for n in self.npcs if n.name == nxt.giver), None)
                return (teacher.x, teacher.y) if teacher else (self.spawn_x, self.spawn_y)
            return None
        if quest.state == Quest.READY:
            teacher = next((n for n in self.npcs if n.name == quest.turn_in), None)
            return (teacher.x, teacher.y) if teacher else None
        if quest.progress_kind in ("school_supply", "research_note"):
            remaining = [c for c in self.collectibles if not c.taken and c.quest_id == quest.quest_id]
            if remaining:
                target = min(remaining, key=lambda c: abs(c.x - self.player.rect.centerx))
                return (target.x, target.y)
        if quest.progress_kind == "checkpoint":
            needed = quest.progress + 1
            cp = next((c for c in self.checkpoints if c.checkpoint_id == needed), None)
            if cp:
                return (cp.x, cp.y)
        return None

    # ---------- Interaction ----------
    def nearest_teacher(self):
        nearest, best = None, 9999
        for npc in self.npcs:
            d = distance((npc.x, npc.y), (self.player.rect.centerx, self.player.rect.bottom))
            if d < best and d < INTERACT_DISTANCE:
                nearest, best = npc, d
        return nearest

    def nearest_checkpoint(self):
        quest = self.current_quest()
        if not quest or quest.progress_kind != "checkpoint" or quest.state != Quest.ACTIVE:
            return None
        needed = quest.progress + 1
        cp = next((c for c in self.checkpoints if c.checkpoint_id == needed and c.near(self.player)), None)
        return cp

    def interact_with_teacher(self, teacher):
        ready = self.current_quest()
        if ready and ready.state == Quest.READY:
            if teacher.name == ready.turn_in:
                if ready.complete():
                    self.dialogue.start(teacher.name, [ready.reward_text, "Quest COMPLETE! Your next lesson is ready when you are."])
                    self.effects.burst(teacher.x, teacher.y - 48, SUCCESS, 22, 145)
                    self.effects.notify(f"{ready.title} COMPLETE! Next quest unlocked.", 3, "success")
                return
            self.dialogue.start(teacher.name, [f"Your finished quest is {ready.title}.", f"Return to {ready.turn_in} to turn it in."])
            return

        active = self.current_quest()
        if active and active.state == Quest.ACTIVE and teacher.name != active.giver:
            self.dialogue.start(teacher.name, [f"You're working on {active.title}.", active.next_step, f"Return to {active.turn_in} when you're done."])
            return

        quest = self.quest_for_teacher(teacher.name)
        if quest:
            if quest.state == Quest.AVAILABLE and quest.is_unlocked(self.quests):
                if quest.accept():
                    self.dialogue.start(teacher.name, [f"QUEST: {quest.title}", quest.objective, f"AREA: {quest.area}.", f"NEXT: {quest.next_step}", f"RETURN TO: {quest.turn_in}."])
                    self.effects.notify(f"Quest accepted: {quest.title}", 3, "info")
                return
            if quest.state == Quest.ACTIVE:
                self.dialogue.start(teacher.name, [f"{quest.title}", quest.objective, f"PROGRESS: {quest.progress_text}", quest.next_step])
                return
            if quest.state == Quest.COMPLETE:
                self.dialogue.start(teacher.name, teacher.dialogue + ["You already completed my quest. Keep exploring!"])
                return

        self.dialogue.start(teacher.name, teacher.dialogue)

    def handle_interaction(self):
        if self.dialogue.active:
            self.dialogue.advance()
            return
        teacher = self.nearest_teacher()
        if teacher:
            self.interact_with_teacher(teacher)
            return
        checkpoint = self.nearest_checkpoint()
        if checkpoint:
            quest = self.current_quest()
            if quest and quest.activate_checkpoint(checkpoint.quest_id, checkpoint.checkpoint_id):
                checkpoint.active = True
                self.effects.burst(checkpoint.x, checkpoint.y, SUCCESS, 18, 120)
                if quest.state == Quest.READY:
                    self.effects.notify("Objective complete! Return to Sir Tanoy.", 3.5, "success")
                else:
                    quest.next_step = f"Reach PRACTICE BEACON {quest.progress + 1} on Sky Campus."
                    self.effects.notify(f"Beacon {checkpoint.checkpoint_id} activated  •  {quest.progress}/{quest.target}", 2.5, "success")
            return
        self.effects.notify("Nothing to interact with here.", 1.5, "info")

    # ---------- Player / world ----------
    def set_message(self, text, seconds=3):
        self.message = text
        self.message_timer = seconds
        self.message_surface = font(18, True).render(text, True, INK)
        self.message_box = pygame.Rect(WIDTH // 2 - self.message_surface.get_width() // 2 - 18, 292, self.message_surface.get_width() + 36, 42)

    def respawn_player(self):
        self.player.x = float(self.spawn_x)
        self.player.y = float(self.spawn_y)
        self.player.rect.topleft = (self.spawn_x, self.spawn_y)
        self.player.vx = 0
        self.player.vy = 0
        self.player.on_ground = False
        self.camera_x = 0.0
        self.effects.burst(self.spawn_x, self.spawn_y + 10, MARKER_BLUE, 20, 110)
        self.effects.notify("You fell! Back to Home Hub.", 3, "info")

    def update(self, dt):
        self.frame_count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            # The jump is buffered from KEYDOWN as well; this path keeps held-jump natural.
            if self.frame_count % 6 == 0:
                self.player.request_jump()
        self.player.update(dt, keys, self.world.islands)

        if self.player.rect.top > FALL_THRESHOLD:
            self.respawn_player()

        self.location = self.world.current_location(self.player.rect.centerx)
        if self.location != self.previous_location:
            self.previous_location = self.location
            self.effects.notify(self.location, 1.8, "info")

        # Only update moving activity art. Draw culling happens in the draw pass.
        for collectible in self.collectibles:
            collectible.update(dt)
            if collectible.taken:
                continue
            if distance((collectible.x, collectible.y), (self.player.rect.centerx, self.player.rect.centery)) < 38:
                quest = self.current_quest()
                if quest and quest.state == Quest.ACTIVE and quest.collect(collectible.quest_id, collectible.kind):
                    collectible.taken = True
                    self.effects.burst(collectible.x, collectible.y, collectible.style["ring"], 16, 115)
                    if quest.state == Quest.READY:
                        self.effects.notify(f"Objective complete! Return to {quest.turn_in}.", 3.5, "success")
                    else:
                        self.effects.notify(f"{quest.target_label}: {quest.progress}/{quest.target}", 1.8, "success")

        for checkpoint in self.checkpoints:
            checkpoint.update(dt)
        for npc in self.npcs:
            npc.update(dt)
        self.effects.update(dt)
        self.message_timer = max(0.0, self.message_timer - dt)

        target = max(0, min(self.player.rect.centerx - WIDTH // 2, WORLD_WIDTH - WIDTH))
        self.camera_x += (target - self.camera_x) * min(1.0, dt * CAMERA_SMOOTH)

    # ---------- Drawing ----------
    def draw_top_ui(self):
        draw_text(self.screen, "PISAY FLOATING ISLANDS", (22, 17), 25, INK, True)
        badge = pygame.Rect(22, 49, 184, 28)
        pygame.draw.rect(self.screen, LOCATION_BADGE, badge, border_radius=10)
        draw_text(self.screen, self.location, (34, 56), 13, INK, True)
        draw_text(self.screen, "TAB / G  •  GUIDE", (225, 57), 13, MUTED, True)

        quest = self.current_quest()
        if quest:
            label = f"QUEST  {quest.progress}/{quest.target}"
            draw_text(self.screen, label, (390, 57), 12, SUCCESS if quest.state == quest.READY else ACCENT, True)

        if self.message_timer > 0 and self.message_surface is not None:
            box = self.message_box
            rounded_panel(self.screen, box, (255, 255, 255), ACCENT, 12, True, 2)
            self.screen.blit(self.message_surface, (box.x + 18, box.y + 11))

    def draw_target_arrow(self):
        point = self.target_point()
        if not point:
            return
        target_x, target_y = point
        target_screen_x = int(target_x - self.camera_x)
        direction = 1 if target_x >= self.player.rect.centerx else -1
        if 24 <= target_screen_x <= WIDTH - 24:
            pygame.draw.line(self.screen, MARKER_BLUE, (target_screen_x, 38), (target_screen_x, 65), 2)
            pygame.draw.polygon(self.screen, MARKER_BLUE, [(target_screen_x, 38), (target_screen_x - 7, 49), (target_screen_x + 7, 49)])
        else:
            edge = WIDTH - 25 if direction > 0 else 25
            pygame.draw.polygon(self.screen, MARKER_BLUE, [(edge + 13 * direction, 55), (edge - 8 * direction, 44), (edge - 8 * direction, 66)])

    def draw_kill_box(self):
        pygame.draw.rect(self.screen, (184, 67, 67), (0, HEIGHT - 12, WIDTH, 12))
        draw_text(self.screen, "FALL ZONE  •  RESPAWN at Home Hub", (WIDTH - 295, HEIGHT - 30), 11, (255, 255, 255), True)

    def draw(self):
        camera_x = int(self.camera_x)
        self.world.draw(self.screen, camera_x)

        quest = self.current_quest()
        for item in self.collectibles:
            highlighted = bool(quest and quest.state == Quest.ACTIVE and item.quest_id == quest.quest_id and not item.taken)
            item.draw(self.screen, camera_x, highlighted=highlighted, show_label=highlighted)

        needed_cp = quest.progress + 1 if quest and quest.progress_kind == "checkpoint" and quest.state == Quest.ACTIVE else None
        for cp in self.checkpoints:
            available = needed_cp == cp.checkpoint_id
            cp.draw(self.screen, camera_x, available=available)
            cp.draw_prompt(self.screen, camera_x, visible=available and cp.near(self.player))

        for npc in self.npcs:
            npc.draw(self.screen, camera_x, self.player, self.marker_state_for_teacher(npc.name))

        self.draw_target_arrow()
        self.player.draw(self.screen, camera_x)
        self.effects.draw_sparks(self.screen, camera_x)
        self.draw_top_ui()
        self.quest_ui.draw_tracker(self.screen, quest, self.location)
        self.quest_ui.draw_goal_banner(self.screen, self.goal_text())
        self.draw_kill_box()

        if self.effects.toast_timer > 0:
            img = font(15, True).render(self.effects.toast, True, INK)
            box = pygame.Rect(WIDTH // 2 - img.get_width() // 2 - 16, 348, img.get_width() + 32, 34)
            rounded_panel(self.screen, box, (255, 255, 255), ACCENT, 10, True, 2)
            self.screen.blit(img, (box.x + 16, box.y + 8))

        self.dialogue.draw(self.screen)
        if self.quest_ui.guide_open:
            self.quest_ui.draw_guide(self.screen, quest, self.location)
        pygame.display.flip()

    async def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = min(clock.tick(FPS) / 1000.0, 0.033)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_TAB, pygame.K_g) and not self.dialogue.active:
                        self.quest_ui.toggle_guide()
                    elif event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                        if event.key in (pygame.K_e, pygame.K_RETURN):
                            self.handle_interaction()
                        elif self.dialogue.active:
                            self.dialogue.advance()
                        else:
                            self.player.request_jump()
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        self.player.request_jump()
                    elif event.key == pygame.K_ESCAPE and self.quest_ui.guide_open:
                        self.quest_ui.toggle_guide()
            self.update(dt)
            self.draw()
            # Return control to the browser/pygbag event loop every frame.
            await asyncio.sleep(0)


async def run_game_async(screen):
    await Game(screen).run()


def run_game(screen):
    """Desktop compatibility wrapper for callers that still expect a sync entry point."""
    asyncio.run(run_game_async(screen))
