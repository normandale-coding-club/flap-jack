"""Main game coordinator for Crossy Road-style frog game."""

import pygame
import sys
from menu import Menu
from world import World


class Game:
    """Main game controller."""

    def __init__(self):
        """Initialize the game."""
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Froggy Crosser - Crossy Road Style")

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.menu = Menu(self.screen_width, self.screen_height)
        self.world = World(self.screen_width, self.screen_height)

        self.state = "menu"  # menu, playing, paused, game_over
        self.running = True
        self.input_cooldown = 0

    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

                if self.state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.start_game()

                elif self.state == "playing":
                    if event.key == pygame.K_SPACE:
                        self.state = "paused"

                elif self.state == "paused":
                    if event.key == pygame.K_SPACE:
                        self.state = "playing"

                elif self.state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.start_game()

    def handle_input(self):
        """Handle continuous input during gameplay."""
        if self.state == "playing":
            keys = pygame.key.get_pressed()

            # Input cooldown to prevent multiple jumps per frame
            if self.input_cooldown > 0:
                self.input_cooldown -= 1
                return

            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                if self.world.handle_input(keys):
                    self.input_cooldown = 10  # Prevent rapid input

    def start_game(self):
        """Start a new game."""
        self.world.reset()
        self.state = "playing"
        self.input_cooldown = 0

    def update(self):
        """Update game state."""
        if self.state == "playing":
            result = self.world.update()

            if result is False:
                # Frog fell in water
                self.state = "game_over"
            elif result == "win":
                # Frog reached goal
                self.state = "game_over"

    def draw(self):
        """Render the game."""
        if self.state == "menu":
            self.menu.draw_main_menu(self.screen)

        elif self.state == "playing":
            self.world.draw(self.screen)
            self.menu.draw_hud(self.screen, self.world.get_score(), self.world.get_score() // 10)

        elif self.state == "paused":
            self.world.draw(self.screen)
            self.menu.draw_hud(self.screen, self.world.get_score(), self.world.get_score() // 10)
            self.menu.draw_pause_menu(self.screen)

        elif self.state == "game_over":
            self.menu.draw_game_over_menu(
                self.screen,
                self.world.get_score(),
                self.world.get_high_score(),
            )

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
