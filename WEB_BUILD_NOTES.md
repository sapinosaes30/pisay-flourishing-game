# PISAY FLOATING ISLANDS — V6.1 WEB-READY

## Goal

The intended player experience is:

**open one link -> browser loads the game -> play**

The browser route is **Python + pygame-ce + pygbag**. A JavaScript rewrite is not part of this milestone.

## Local Windows test

From this folder:

```text
py -m pip install -r requirements.txt
py -m pip install --user --upgrade pygbag==0.9.4
py -m pygbag .
```

Open the local URL printed by pygbag.

For a release build (the package is currently pinned to pygbag 0.9.4):

```text
py -m pygbag --build --title "PISAY FLOATING ISLANDS" .
```

The expected static output is under `build/web`.

## Browser verification checklist

Do not call this finished until a real browser test confirms:

- game starts and remains responsive
- keyboard input works
- A/D or arrows move
- W/Up/Space jumps
- E/Enter interacts and advances dialogue
- TAB/G opens the guide and ESC closes it
- collisions and platform traversal work
- Eileen quest collects only classroom supplies
- Zen quest collects only research notes
- Tanoy beacons require order 1 -> 2 -> 3
- wrong quest items/checkpoints do not advance progress
- completed quests cannot be completed again
- falling respawns at Home Hub
- teacher visuals remain readable
- no black sky stripes appear
- target arrow and quest UI remain readable
- browser does not freeze or crash

## Current limitation

This package has been made browser-ready in code and packaging structure, but the current container does not have pygame-ce or pygbag installed, so a genuine graphical browser build/playtest cannot be claimed from this environment.
