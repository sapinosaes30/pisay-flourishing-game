PISAY FLOATING ISLANDS — V6.1 WEB-READY

Python + pygame-ce floating-island platformer.

V6.1 focus:
- cleaner, deeper floating-island graphics
- improved player movement and animation
- fixed teacher hair layering (hair does not cover faces/eyes)
- exactly three teachers
- more distinct teacher outfits and personalities
- guided, sequential quests with exact quest binding
- stronger quest item silhouettes and labels
- clear quest tracker with progress pips
- WHAT DO I DO NOW? guidance
- target arrow toward the next objective
- visual collection / beacon activation effects
- improved beginner guide
- preserved fall zone + Home Hub respawn
- preserved modular structure + display initialization in main.py

TEACHERS
1. Ma'am Eileen — warm, caring, mostly Tagalog, "darling/darlings", short brown hair.
2. Ma'am Zen — serious, knowledgeable, strict but caring, research/algebra personality, short grey hair.
3. Sir Tanoy — fun, hands-on, humorous, relaxed but somewhat strict, very short grey hair.
Sir Lando is not present.

QUESTS
1. Ready, Darlings! — Ma'am Eileen
   Find 3 CLASSROOM SUPPLIES on Study Island and return to Ma'am Eileen.
2. Research Relay — Ma'am Zen
   Collect 3 RESEARCH NOTES on Study Island and return to Ma'am Zen.
3. Hands-On Circuit — Sir Tanoy
   Activate practice beacons 1, 2, and 3 on Sky Campus in order, then return to Sir Tanoy.

Quest states:
AVAILABLE -> ACTIVE -> READY -> COMPLETE
Quest progress requires BOTH the correct quest id AND correct item/activity type.

CONTROLS
A / D or Arrow Keys = move
W / Up / Space = jump
E / Enter = interact / advance dialogue
TAB / G = guide
ESC = close guide

INSTALL / RUN
py -m pip install -r requirements.txt
py main.py


WEB BUILD
Preferred browser route: pygame-ce + pygbag.
The game loop is async-aware and yields with await asyncio.sleep(0) every frame.

Local browser test:
py -m pip install --user --upgrade pygbag
py -m pygbag .
Then open the local address reported by pygbag.

Production build:
py -m pygbag --build --title "PISAY FLOATING ISLANDS" .
Output: build\web

A real browser playtest is still required before calling the web release complete.
