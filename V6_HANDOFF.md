# PISAY FLOATING ISLANDS — V6 HANDOFF

## Version
V6 POLISHED

## What changed
V6 is a major quality pass over V5.1. The game remains a modular Python + pygame-ce project and does not overwrite older versions.

## Core rules preserved
- Exactly 3 teachers: Ma'am Eileen, Ma'am Zen, Sir Tanoy.
- Sir Lando is removed.
- No virtue meters, morality points, alignment, or virtue-only XP.
- Bottom fall zone remains.
- Falling off the world respawns the player at Home Hub.
- Display initialization remains in `main.py` before `run_game(screen)`.

## Teacher visuals
- Ma'am Eileen: short brown hair.
- Ma'am Zen: short grey hair + mask.
- Sir Tanoy: very short grey hair.
- Hair is split into BACK and FRONT layers; the front cap stops above the eye line.

## Quest structure
1. `eileen_supplies` — Ready, Darlings!
   - Find 3 classroom supplies on Study Island.
   - Exact item binding: quest id + `school_supply`.
2. `zen_research` — Research Relay
   - Collect 3 research notes on Study Island.
   - Exact item binding: quest id + `research_note`.
   - Unlocks after Eileen is COMPLETE.
3. `tanoy_circuit` — Hands-On Circuit
   - Activate practice beacons 1 → 2 → 3 on Sky Campus.
   - Exact checkpoint quest id + ordered checkpoint id.
   - Unlocks after Zen is COMPLETE.

## UI
- Current quest panel on right.
- WHAT DO I DO NOW? panel on left.
- progress pips
- state badge
- target arrow to nearest relevant target / return teacher
- TAB / G beginner guide
- visual markers: ! available, ? ready, diamond active

## Visual polish
- cached multi-band sky
- sun + parallax clouds
- richer island layers with rock flecks + grass tufts
- themed landmarks per island
- improved player animation
- distinct teacher outfits
- collection / beacon spark effects
- clearer item silhouettes

## Performance
Static sky, cloud tile, island art, fonts, and repeated text are cached. Draw calls for world objects remain culled by camera bounds. Effects are capped at small burst sizes.

## Validation
- `py validate_project.py`
- `py validate_quest_logic.py`

The execution environment used to build this project does not include network access for installing pygame-ce, so a real graphical run was not possible during packaging. Python syntax and quest-state logic were validated locally.
