import pygame
import random

TILE = 64

LOG_COLORS = [
    (139, 90, 43),
    (160, 110, 60),
    (120, 75, 35),
]


class Log:
    HEIGHT = 44
    MIN_WIDTH = 2
    MAX_WIDTH = 4

    def __init__(self, row: int, screen_width: int, speed: float, direction: int, initial: bool = False):
        self.row = row
        self.speed = speed * direction
        self.tile_width = random.randint(self.MIN_WIDTH, self.MAX_WIDTH)
        self.pixel_width = self.tile_width * TILE
        self.color = random.choice(LOG_COLORS)
        self.screen_width = screen_width

        if initial:
            # Spread initial logs across the visible area so the river looks populated immediately
            self.x = float(random.randint(-self.pixel_width, screen_width))
        elif direction == 1:
            self.x = float(-self.pixel_width - random.randint(0, 80))
        else:
            self.x = float(screen_width + random.randint(0, 80))

        self.y = row * TILE + (TILE - self.HEIGHT) // 2

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), self.y, self.pixel_width, self.HEIGHT)

    def update(self):
        self.x += self.speed

    def is_off_screen(self) -> bool:
        if self.speed > 0:
            return self.x > self.screen_width + 20
        return self.x + self.pixel_width < -20

    def draw(self, surface: pygame.Surface, cam_offset_y: int):
        draw_rect = pygame.Rect(int(self.x), self.y - cam_offset_y, self.pixel_width, self.HEIGHT)

        pygame.draw.rect(surface, self.color, draw_rect, border_radius=10)

        grain = (max(0, self.color[0] - 20), max(0, self.color[1] - 20), max(0, self.color[2] - 10))
        for i in range(1, self.tile_width):
            gx = int(self.x) + i * TILE
            gy1 = self.y - cam_offset_y + 6
            gy2 = self.y - cam_offset_y + self.HEIGHT - 6
            pygame.draw.line(surface, grain, (gx, gy1), (gx, gy2), 2)

        cap = (max(0, self.color[0] - 15), max(0, self.color[1] - 15), max(0, self.color[2] - 8))
        pygame.draw.rect(surface, cap, (int(self.x), self.y - cam_offset_y, 10, self.HEIGHT), border_radius=4)
        pygame.draw.rect(surface, cap,
                         (int(self.x) + self.pixel_width - 10, self.y - cam_offset_y, 10, self.HEIGHT),
                         border_radius=4)

        highlight = (min(255, self.color[0] + 30), min(255, self.color[1] + 20), min(255, self.color[2] + 10))
        pygame.draw.rect(surface, highlight,
                         (int(self.x) + 10, self.y - cam_offset_y + 5, self.pixel_width - 20, 7),
                         border_radius=4)


class LogRow:
    def __init__(self, row: int, screen_width: int, difficulty: float = 1.0):
        self.row = row
        self.screen_width = screen_width
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1.2, 2.5) * difficulty
        self.logs: list[Log] = []
        self.gap_timer = 0
        self.gap_interval = random.randint(60, 140)

        for _ in range(random.randint(2, 4)):
            self.logs.append(Log(row, screen_width, self.speed, self.direction, initial=True))

    def _spawn_log(self):
        self.logs.append(Log(self.row, self.screen_width, self.speed, self.direction))

    def update(self):
        for log in self.logs:
            log.update()
        self.logs = [lg for lg in self.logs if not lg.is_off_screen()]
        self.gap_timer += 1
        if self.gap_timer >= self.gap_interval:
            self._spawn_log()
            self.gap_timer = 0
            self.gap_interval = random.randint(60, 140)

    def draw(self, surface: pygame.Surface, cam_offset_y: int):
        for log in self.logs:
            log.draw(surface, cam_offset_y)

    def get_log_at(self, rect: pygame.Rect) -> Log | None:
        for log in self.logs:
            if log.rect.colliderect(rect):
                return log
        return None
