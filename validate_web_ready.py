from pathlib import Path
import ast

root = Path(__file__).resolve().parent
required = [
    'main.py', 'game.py', 'world.py', 'island.py', 'player.py', 'npc.py',
    'quests.py', 'activities.py', 'quest_ui.py', 'dialogue.py', 'effects.py',
    'utils.py', 'settings.py', 'requirements.txt', 'README.txt',
    'BUILD_WEB.bat', 'WEB_BUILD_NOTES.md', 'validate_web_ready.py',
]
missing = [name for name in required if not (root / name).exists()]
if missing:
    raise SystemExit('Missing required web-ready files: ' + ', '.join(missing))

for py_file in root.glob('*.py'):
    ast.parse(py_file.read_text(encoding='utf-8'))

main = (root / 'main.py').read_text(encoding='utf-8')
game = (root / 'game.py').read_text(encoding='utf-8')
world = (root / 'world.py').read_text(encoding='utf-8')
settings = (root / 'settings.py').read_text(encoding='utf-8')
workflow = root / '.github' / 'workflows' / 'deploy-web.yml'

checks = [
    ('main imports asyncio', 'import asyncio' in main),
    ('main initializes display before game launch', 'pygame.display.set_mode' in main and 'await run_game_async(screen)' in main),
    ('game runner is async', 'async def run(self)' in game and 'async def run_game_async(screen)' in game),
    ('browser yield is present', 'await asyncio.sleep(0)' in game),
    ('continuous sky-gradient loop is present', 'for y in range(HEIGHT)' in world),
    ('V6.1 title is present', 'V6.1' in settings),
    ('web workflow exists', workflow.exists()),
]
failed = [label for label, ok in checks if not ok]
if failed:
    raise SystemExit('Web-ready validation failed: ' + '; '.join(failed))

print('OK: V6.1 web-ready files and Python syntax validated.')
for label, _ in checks:
    print('OK:', label)
