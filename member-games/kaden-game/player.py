import pygame

TILE = 64


class Player:
    WIDTH = 48
    HEIGHT = 48

    def __init__(self, start_col: int, start_row: int):
        self.col = start_col
        self.row = start_row
        self.pixel_x = float(start_col * TILE + (TILE - self.WIDTH) // 2)
        self.pixel_y = float(start_row * TILE + (TILE - self.HEIGHT) // 2)
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.move_speed = 10
        self.alive = True
        self.on_log = False
        self.facing = "up"
        self.jump_frame = 0
        self.jump_total = 8
        self.best_row = start_row

    def handle_input(self, event: pygame.Event):
        if self.moving or not self.alive:
            return
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_UP, pygame.K_w):
            self._start_move(0, -1, "up")
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self._start_move(0, 1, "down")
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self._start_move(-1, 0, "left")
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self._start_move(1, 0, "right")

    def _start_move(self, dc: int, dr: int, facing: str):
        self.col += dc
        self.row += dr
        self.target_x += dc * TILE
        self.target_y += dr * TILE
        self.moving = True
        self.jump_frame = 0
        self.facing = facing

    def update(self):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist <= self.move_speed:
                self.pixel_x = self.target_x
                self.pixel_y = self.target_y
                self.moving = False
            else:
                ratio = self.move_speed / dist
                self.pixel_x += dx * ratio
                self.pixel_y += dy * ratio
            self.jump_frame = min(self.jump_frame + 1, self.jump_total)

        if self.row < self.best_row:
            self.best_row = self.row

    def ride_log(self, dx: float):
        self.pixel_x += dx
        self.target_x += dx
        self.col = round((self.pixel_x - (TILE - self.WIDTH) // 2) / TILE)

    def draw(self, surface: pygame.Surface, cam_offset_y: int):
        draw_x = int(self.pixel_x)
        draw_y = int(self.pixel_y) - cam_offset_y

        progress = self.jump_frame / max(self.jump_total, 1)
        arc = int(12 * 4 * progress * (1 - progress))

        body = pygame.Rect(draw_x, draw_y - arc, self.WIDTH, self.HEIGHT)

        pygame.draw.ellipse(surface, (34, 139, 34), body)
        pygame.draw.ellipse(surface, (50, 180, 50),
                            pygame.Rect(body.x + 8, body.y + 6, self.WIDTH - 22, self.HEIGHT // 3))

        eye_y = body.y + 10
        for ex in (body.x + 13, body.x + self.WIDTH - 13):
            pygame.draw.circle(surface, (255, 255, 255), (ex, eye_y), 7)

        px = {"up": 0, "down": 0, "left": -2, "right": 2}[self.facing]
        py = {"up": -2, "down": 2, "left": 0, "right": 0}[self.facing]
        for ex in (body.x + 13, body.x + self.WIDTH - 13):
            pygame.draw.circle(surface, (0, 0, 0), (ex + px, eye_y + py), 3)

        leg = (22, 110, 22)
        pygame.draw.rect(surface, leg, (body.x - 6, body.bottom - 18, 10, 16))
        pygame.draw.rect(surface, leg, (body.right - 4, body.bottom - 18, 10, 16))
        pygame.draw.rect(surface, leg, (body.x - 4, body.y + 14, 8, 10))
        pygame.draw.rect(surface, leg, (body.right - 4, body.y + 14, 8, 10))

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.pixel_x) + 6, int(self.pixel_y) + 6,
                           self.WIDTH - 12, self.HEIGHT - 12)
