class Quest:
    AVAILABLE = "available"
    ACTIVE = "active"
    READY = "ready"
    COMPLETE = "complete"

    def __init__(self, quest_id, title, objective, giver, turn_in, target, progress_kind, area, next_step, reward_text, prerequisite=None, target_label="QUEST TARGET", destination_text=""):
        self.quest_id = quest_id
        self.title = title
        self.objective = objective
        self.giver = giver
        self.turn_in = turn_in
        self.target = target
        self.progress_kind = progress_kind
        self.area = area
        self.next_step = next_step
        self.reward_text = reward_text
        self.prerequisite = prerequisite
        self.target_label = target_label
        self.destination_text = destination_text
        self.progress = 0
        self.state = self.AVAILABLE

    @property
    def accepted(self):
        return self.state in (self.ACTIVE, self.READY, self.COMPLETE)

    @property
    def completed(self):
        return self.state == self.COMPLETE

    @property
    def progress_text(self):
        return f"{self.progress} / {self.target}"

    def is_unlocked(self, quests):
        if not self.prerequisite:
            return True
        return any(q.quest_id == self.prerequisite and q.state == self.COMPLETE for q in quests)

    def accept(self):
        if self.state != self.AVAILABLE:
            return False
        self.state = self.ACTIVE
        return True

    def collect(self, quest_id, kind):
        # Exact quest binding prevents unrelated objects from ever counting.
        if self.state != self.ACTIVE or quest_id != self.quest_id or kind != self.progress_kind:
            return False
        self.progress = min(self.target, self.progress + 1)
        if self.progress >= self.target:
            self.state = self.READY
        return True

    def activate_checkpoint(self, quest_id, checkpoint_id):
        if self.state != self.ACTIVE or self.progress_kind != "checkpoint":
            return False
        if quest_id != self.quest_id or checkpoint_id != self.progress + 1:
            return False
        self.progress += 1
        if self.progress >= self.target:
            self.progress = self.target
            self.state = self.READY
        return True

    def can_turn_in(self, teacher_name):
        return self.state == self.READY and teacher_name == self.turn_in

    def complete(self):
        if self.state != self.READY:
            return False
        self.state = self.COMPLETE
        return True

    def status_text(self):
        if self.state == self.AVAILABLE:
            return "Available"
        if self.state == self.ACTIVE:
            return f"{self.progress_text} • {self.next_step}"
        if self.state == self.READY:
            return f"Objective complete! Return to {self.turn_in}."
        return "Completed"

    def compact_objective(self):
        if self.progress_kind == "checkpoint":
            return f"Activate {self.target} practice beacons in order."
        return self.objective
