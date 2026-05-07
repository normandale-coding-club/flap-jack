"""Menu system for Crossy Road-style frog game."""

import pygame
import sys


class Menu:
    """Handles menu display and user interactions."""

    def __init__(self, screen_width, screen_height):
        """Initialize menu with screen dimensions."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_title = pygame.font.Font(None, 72)
        self.font_text = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.background_color = (34, 139, 34)  # Forest green

    def draw_main_menu(self, screen):
        """Draw the main menu screen."""
        screen.fill(self.background_color)

        # Title
        title = self.font_title.render("FROGGY CROSSER", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(title, title_rect)

        # Instructions
        instructions = [
            "Use ARROW KEYS to move the frog",
            "Cross the logs to reach the other side",
            "Don't get hit by moving logs!",
            "",
            "Press SPACE to START",
            "Press Q to QUIT",
        ]

        y_offset = 250
        for instruction in instructions:
            if instruction == "":
                y_offset += 30
                continue

            if "SPACE" in instruction or "QUIT" in instruction:
                text = self.font_small.render(instruction, True, (255, 255, 0))
            else:
                text = self.font_small.render(instruction, True, (255, 255, 255))

            text_rect = text.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 50

    def draw_pause_menu(self, screen):
        """Draw the pause menu overlay."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = self.font_title.render("PAUSED", True, (255, 215, 0))
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        screen.blit(pause_text, pause_rect)

        # Instructions
        resume_text = self.font_text.render("Press SPACE to Resume", True, (255, 255, 255))
        resume_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(resume_text, resume_rect)

        quit_text = self.font_text.render("Press Q to Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
        screen.blit(quit_text, quit_rect)

    def draw_game_over_menu(self, screen, score, high_score):
        """Draw the game over menu."""
        screen.fill(self.background_color)

        # Game Over text
        game_over_text = self.font_title.render("GAME OVER!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(game_over_text, game_over_rect)

        # Score
        score_text = self.font_text.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width // 2, 250))
        screen.blit(score_text, score_rect)

        # High Score
        high_score_text = self.font_text.render(f"Best: {high_score}", True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect(center=(self.screen_width // 2, 330))
        screen.blit(high_score_text, high_score_rect)

        # Instructions
        restart_text = self.font_small.render("Press SPACE to Play Again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, 450))
        screen.blit(restart_text, restart_rect)

        quit_text = self.font_small.render("Press Q to Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, 530))
        screen.blit(quit_text, quit_rect)

    def draw_hud(self, screen, score, level):
        """Draw heads-up display during gameplay."""
        font = pygame.font.Font(None, 36)

        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Level/Distance
        level_text = font.render(f"Distance: {level}", True, (255, 255, 255))
        screen.blit(level_text, (10, 50))

        # Controls hint
        controls = font.render("SPACE: Pause | Q: Quit", True, (200, 200, 200))
        screen.blit(controls, (self.screen_width - 400, 10))
