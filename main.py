import asyncio
import pygame
from settings import WIDTH, HEIGHT, TITLE
from game import run_game_async


async def main():
    # Pygbag requires an async-aware entry loop for browser builds.
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    try:
        await run_game_async(screen)
    finally:
        pygame.quit()


asyncio.run(main())
