import pygame
import random
from log import LogRow, TILE

ROW_GRASS = "grass"
ROW_RIVER = "river"
ROW_BANK = "bank"

GRASS_COLORS = [(86, 130, 3), (98, 145, 5), (75, 118, 2)]
BANK_COLORS = [(210, 180, 140), (195, 165, 125), (220, 190, 150)]
RIVER_COLORS = [(28, 107, 160), (30, 120, 175), (25, 95, 150)]
RIVER_DARK = (20, 85, 135)

STARTING_SAFE = 3
RIVER_LEN = 6
BANK_LEN = 2
CYCLE = BANK_LEN + RIVER_LEN


def _row_type(row: int) -> str:
    if row >= 0:
        return ROW_GRASS
    r = abs(row)
    if r <= STARTING_SAFE:
        return ROW_GRASS
    pos = (r - STARTING_SAFE - 1) % CYCLE
    return ROW_BANK if pos < BANK_LEN else ROW_RIVER


def _difficulty(row: int) -> float:
    return 1.0 + max(0, abs(row) - STARTING_SAFE) * 0.015


class WorldRow:
    def __init__(self, row_index: int, row_type: str, screen_width: int, difficulty: float = 1.0):
        self.row_index = row_index
        self.row_type = row_type
        self.screen_width = screen_width
        palette = GRASS_COLORS if row_type == ROW_GRASS else BANK_COLORS if row_type == ROW_BANK else RIVER_COLORS
        self.color = random.choice(palette)
        self.log_row: LogRow | None = LogRow(row_index, screen_width, difficulty) if row_type == ROW_RIVER else None

    def update(self):
        if self.log_row:
            self.log_row.update()

    def draw(self, surface: pygame.Surface, cam_offset_y: int, screen_width: int):
        y = self.row_index * TILE - cam_offset_y
        pygame.draw.rect(surface, self.color, (0, y, screen_width, TILE))

        if self.row_type == ROW_RIVER:
            for rx in range(0, screen_width, 48):
                pygame.draw.ellipse(surface, RIVER_DARK, (rx, y + TILE // 2 - 5, 32, 10))

        if self.row_type in (ROW_GRASS, ROW_BANK):
            tuft = (max(0, self.color[0] - 15), min(255, self.color[1] + 10), max(0, self.color[2] - 5))
            for tx in range(10, screen_width, 60):
                pygame.draw.circle(surface, tuft, (tx, y + TILE - 8), 5)

        if self.log_row:
            self.log_row.draw(surface, cam_offset_y)


class World:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rows: dict[int, WorldRow] = {}
        self.score = 0
        self._scored: set[int] = set()
        self._generate_around(0, 30)

    def _generate_around(self, center: int, half: int = 20):
        for r in range(center - half, center + half + 1):
            if r not in self.rows:
                self.rows[r] = WorldRow(r, _row_type(r), self.screen_width, _difficulty(r))

    def update(self, player):
        c = player.row
        self._generate_around(c, 25)

        for r in range(c - 20, c + 20):
            if r in self.rows:
                self.rows[r].update()

        stale = [r for r in self.rows if r > c + 40 or r < c - 40]
        for r in stale:
            del self.rows[r]

        self._check_player(player)
        if player.alive:
            self._update_score(player)

    def _check_player(self, player):
        row_data = self.rows.get(player.row)
        if row_data is None:
            return

        if row_data.row_type in (ROW_GRASS, ROW_BANK):
            player.on_log = False
            return

        if row_data.row_type == ROW_RIVER and not player.moving:
            log = row_data.log_row.get_log_at(player.rect) if row_data.log_row else None
            if log:
                player.on_log = True
                player.ride_log(log.speed)
                if player.pixel_x < -TILE or player.pixel_x > self.screen_width + TILE:
                    player.alive = False
            else:
                player.alive = False

    def _update_score(self, player):
        row = player.row
        if row < 0 and row not in self._scored:
            self._scored.add(row)
            self.score += 1

    def draw(self, surface: pygame.Surface, cam_offset_y: int, player_row: int):
        for r in range(player_row - 15, player_row + 16):
            row_data = self.rows.get(r)
            if row_data:
                row_data.draw(surface, cam_offset_y, self.screen_width)
