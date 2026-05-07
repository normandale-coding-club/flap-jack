"""World management for Crossy Road-style frog game."""

import pygame
import random


class Frog(pygame.sprite.Sprite):
    """The player-controlled frog."""

    def __init__(self, x, y, size=40):
        """Initialize the frog sprite."""
        super().__init__()
        self.size = size
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 200, 0))  # Green frog
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0
        self.falling = False
        self.gravity = 0.5
        self.jump_speed = 15

    def jump(self, direction):
        """Make the frog jump in a direction (0: up, 1: down, 2: left, 3: right)."""
        if direction == 0:  # Up
            self.rect.y -= self.size
        elif direction == 1:  # Down
            self.rect.y += self.size
        elif direction == 2:  # Left
            self.rect.x -= self.size
        elif direction == 3:  # Right
            self.rect.x += self.size

    def apply_gravity(self, ground_level):
        """Apply gravity to frog when falling."""
        if self.rect.y < ground_level:
            self.falling = True
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
        else:
            self.falling = False
            self.vel_y = 0
            self.rect.y = ground_level

    def draw_frog(self, surface):
        """Draw frog with eyes for better visuals."""
        # Body
        pygame.draw.circle(surface, (0, 200, 0), self.rect.center, self.size // 2)

        # Eyes
        eye_offset = self.size // 6
        eye_pos_left = (
            self.rect.centerx - eye_offset,
            self.rect.centery - eye_offset,
        )
        eye_pos_right = (
            self.rect.centerx + eye_offset,
            self.rect.centery - eye_offset,
        )
        pygame.draw.circle(surface, (255, 255, 255), eye_pos_left, 4)
        pygame.draw.circle(surface, (255, 255, 255), eye_pos_right, 4)
        pygame.draw.circle(surface, (0, 0, 0), eye_pos_left, 2)
        pygame.draw.circle(surface, (0, 0, 0), eye_pos_right, 2)


class Log(pygame.sprite.Sprite):
    """A moving log that can collide with the frog."""

    def __init__(self, x, y, width, height, speed, direction=1):
        """
        Initialize a log.

        Args:
            x: Initial x position
            y: Initial y position
            width: Log width
            height: Log height
            speed: Movement speed
            direction: 1 for right, -1 for left
        """
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((139, 69, 19))  # Brown log color
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = direction
        self.screen_width = 800  # Will be set by world

    def update(self):
        """Move the log."""
        self.rect.x += self.speed * self.direction

        # Wrap around screen
        if self.direction == 1 and self.rect.left > self.screen_width:
            self.rect.right = 0
        elif self.direction == -1 and self.rect.right < 0:
            self.rect.left = self.screen_width

    def draw_log(self, surface):
        """Draw log with texture details."""
        # Main log
        pygame.draw.rect(surface, (139, 69, 19), self.rect)

        # Add some texture rings
        for i in range(2, self.rect.width, 40):
            pygame.draw.line(
                surface, (101, 50, 15), (self.rect.x + i, self.rect.y), (self.rect.x + i, self.rect.bottom), 2
            )


class River:
    """Manages the river with multiple lanes of logs."""

    def __init__(self, screen_width, screen_height):
        """Initialize the river."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.logs = pygame.sprite.Group()
        self.lanes = []
        self.create_lanes()

    def create_lanes(self):
        """Create log lanes for the river."""
        # Create 5 lanes with logs
        num_lanes = 5
        lane_height = self.screen_height // (num_lanes + 2)
        log_height = 20

        for lane_idx in range(num_lanes):
            # Calculate y position for this lane
            y = 150 + lane_idx * lane_height

            # Randomize log properties per lane
            log_width = random.randint(80, 150)
            speed = random.uniform(2, 5)
            direction = 1 if lane_idx % 2 == 0 else -1
            gap = random.randint(100, 150)

            # Create multiple logs for this lane
            num_logs = (self.screen_width + gap * 2) // (log_width + gap) + 1
            for log_idx in range(num_logs):
                x = log_idx * (log_width + gap)
                log = Log(x, y, log_width, log_height, speed, direction)
                log.screen_width = self.screen_width
                self.logs.add(log)

            self.lanes.append({"y": y, "speed": speed, "direction": direction})

    def update(self):
        """Update all logs in the river."""
        self.logs.update()

    def check_collision(self, frog):
        """
        Check if frog is on a log or in water.

        Returns:
            (is_safe, velocity_x)
        """
        # Check if frog is in river area
        if frog.rect.y < 150 or frog.rect.y > 150 + len(self.lanes) * (self.screen_height // (len(self.lanes) + 2)):
            return True, 0  # Not in river area, safe

        # Check collision with logs
        collided_logs = pygame.sprite.spritecollide(frog, self.logs, False)
        if collided_logs:
            # Frog is on a log, move with it
            log = collided_logs[0]
            return True, log.speed * log.direction

        # Frog is in water without a log
        return False, 0

    def draw(self, surface):
        """Draw all logs and river."""
        # Draw water background
        water_rect = pygame.Rect(0, 150, self.screen_width, 200)
        pygame.draw.rect(surface, (30, 144, 255), water_rect)  # Dodger blue

        # Draw logs with custom styling
        for log in self.logs:
            log.draw_log(surface)


class World:
    """Main world manager handling all game interactions."""

    def __init__(self, screen_width, screen_height):
        """Initialize the world."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frog = None
        self.river = None
        self.score = 0
        self.high_score = 0
        self.reset()

    def reset(self):
        """Reset the game world for a new game."""
        # Frog starts at bottom center
        self.frog = Frog(self.screen_width // 2, self.screen_height - 50)
        self.river = River(self.screen_width, self.screen_height)
        self.score = 0

    def handle_input(self, keys):
        """Handle keyboard input for frog movement."""
        if keys[pygame.K_UP]:
            old_y = self.frog.rect.y
            self.frog.jump(0)  # Up
            if self.frog.rect.y < 100:
                self.frog.rect.y = old_y
            # Increase score for moving up
            if old_y > self.frog.rect.y:
                self.score += 10
            return True
        elif keys[pygame.K_DOWN]:
            old_y = self.frog.rect.y
            self.frog.jump(1)  # Down
            if self.frog.rect.y > self.screen_height - 50:
                self.frog.rect.y = old_y
            return True
        elif keys[pygame.K_LEFT]:
            self.frog.jump(2)  # Left
            if self.frog.rect.x < 20:
                self.frog.rect.x = 20
            return True
        elif keys[pygame.K_RIGHT]:
            self.frog.jump(3)  # Right
            if self.frog.rect.x > self.screen_width - 20:
                self.frog.rect.x = self.screen_width - 20
            return True
        return False

    def update(self):
        """Update world state."""
        self.river.update()

        # Check collision with logs
        is_safe, velocity_x = self.river.check_collision(self.frog)

        if not is_safe:
            # Frog in water, game over
            return False

        # Move frog with log if on one
        self.frog.rect.x += velocity_x

        # Keep frog in bounds horizontally
        self.frog.rect.x = max(20, min(self.screen_width - 20, self.frog.rect.x))

        # Check if frog reached the goal
        if self.frog.rect.y < 120:
            self.score += 100  # Bonus for reaching goal
            if self.score > self.high_score:
                self.high_score = self.score
            return "win"

        return True

    def draw(self, surface):
        """Draw all world elements."""
        # Draw grass background
        surface.fill((34, 139, 34))  # Forest green

        # Draw river
        self.river.draw(surface)

        # Draw goal area
        goal_rect = pygame.Rect(0, 100, self.screen_width, 50)
        pygame.draw.rect(surface, (100, 200, 255), goal_rect)  # Light blue
        pygame.draw.rect(surface, (0, 100, 200), goal_rect, 3)

        # Draw frog
        self.frog.draw_frog(surface)

    def get_score(self):
        """Get the current score."""
        return self.score

    def get_high_score(self):
        """Get the high score."""
        return self.high_score
