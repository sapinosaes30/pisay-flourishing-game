from quests import Quest

q1 = Quest(
    quest_id="q1", title="Collect supplies", objective="Collect",
    giver="E", turn_in="E", target=3, progress_kind="school_supply",
    area="Study", next_step="next", reward_text="done", target_label="CLASS SUPPLY"
)
assert q1.accept()
assert not q1.collect("q2", "school_supply")
assert not q1.collect("q1", "research_note")
assert q1.collect("q1", "school_supply")
assert q1.collect("q1", "school_supply")
assert q1.collect("q1", "school_supply")
assert q1.state == Quest.READY
assert not q1.collect("q1", "school_supply")
assert not q1.can_turn_in("Zen")
assert q1.can_turn_in("E")
assert q1.complete()
assert not q1.complete()

q2 = Quest(
    quest_id="q2", title="Beacons", objective="Activate",
    giver="T", turn_in="T", target=3, progress_kind="checkpoint",
    area="Sky", next_step="next", reward_text="done", target_label="PRACTICE BEACON"
)
assert q2.accept()
assert not q2.activate_checkpoint("q2", 2)
assert q2.activate_checkpoint("q2", 1)
assert q2.activate_checkpoint("q2", 2)
assert q2.activate_checkpoint("q2", 3)
assert q2.state == Quest.READY
assert not q2.activate_checkpoint("q2", 4)
print("OK: exact quest binding, ordering, READY lock, and duplicate-completion prevention validated.")
