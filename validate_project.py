from pathlib import Path
import ast

root = Path(__file__).resolve().parent
required = [
    'main.py', 'game.py', 'world.py', 'island.py', 'player.py', 'npc.py',
    'quests.py', 'activities.py', 'quest_ui.py', 'dialogue.py', 'effects.py',
    'utils.py', 'settings.py', 'requirements.txt', 'README.txt'
]
missing = [f for f in required if not (root / f).exists()]
if missing:
    raise SystemExit('Missing: ' + ', '.join(missing))

for py in root.glob('*.py'):
    if py.name.startswith('validate_'):
        continue
    ast.parse(py.read_text(encoding='utf-8'))

game = (root / 'game.py').read_text(encoding='utf-8')
readme = (root / 'README.txt').read_text(encoding='utf-8')
if game.count('NPC(') != 3:
    raise SystemExit('Expected exactly three teacher declarations.')
if 'Sir Lando' in game:
    raise SystemExit('Sir Lando must not be declared in the current game.')
for forbidden in ['virtue meter', 'morality score', 'Kindness points', 'alignment system', 'XP system']:
    if forbidden in game:
        raise SystemExit(f'Forbidden system appears in code: {forbidden}')
if 'pygame.display.set_mode' not in (root / 'main.py').read_text(encoding='utf-8'):
    raise SystemExit('Display setup missing from main.py')
if 'await run_game_async(screen)' not in (root / 'main.py').read_text(encoding='utf-8'):
    raise SystemExit('Async game launch missing from main.py')
print('OK: V6.1 project files and Python syntax validated.')
print('OK: exactly three teachers; Lando is not declared.')
print('OK: display initialization stays in main.py.')
print('OK: async browser entry flow is present.')
print('OK: modular quest/UI/world/effects files present.')
