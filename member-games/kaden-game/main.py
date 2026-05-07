import pygame
import sys
from player import Player, TILE
from world import World
from camera import Camera
from menu import draw_menu, draw_hud, draw_game_over

WIDTH = 640
HEIGHT = 640
FPS = 60
TITLE = "Frog Leap"

START_COL = WIDTH // (2 * TILE)
START_ROW = 3


def run_game(screen: pygame.Surface, clock: pygame.time.Clock, high_score: int) -> int:
    player = Player(START_COL, START_ROW)
    world = World(WIDTH, HEIGHT)
    camera = Camera(HEIGHT)
    camera.snap(int(player.pixel_y))

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return max(world.score, high_score)
                if game_over and event.key == pygame.K_RETURN:
                    return max(world.score, high_score)
            if not game_over:
                player.handle_input(event)

        if not game_over:
            player.update()
            world.update(player)
            camera.update(int(player.pixel_y))
            if not player.alive:
                game_over = True

        screen.fill((0, 0, 0))
        world.draw(screen, int(camera.offset_y), player.row)
        player.draw(screen, int(camera.offset_y))
        draw_hud(screen, world.score, high_score)

        if game_over:
            draw_game_over(screen, world.score, max(world.score, high_score))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    high_score = 0

    while True:
        in_menu = True
        while in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        in_menu = False
            screen.fill((0, 0, 0))
            draw_menu(screen, high_score)
            pygame.display.flip()
            clock.tick(FPS)

        result = run_game(screen, clock, high_score)
        high_score = max(high_score, result)


if __name__ == "__main__":
    main()
