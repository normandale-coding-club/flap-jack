import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (20, 80, 20)
LIGHT_GREEN = (80, 180, 80)
GOLD = (255, 215, 0)
RED = (220, 50, 50)
GRAY = (180, 180, 180)
RIVER_BLUE = (28, 107, 160)


def _draw_background(surface: pygame.Surface):
    w, h = surface.get_size()
    surface.fill(DARK_GREEN)
    pygame.draw.rect(surface, RIVER_BLUE, (0, h // 2 - 55, w, 110))
    for rx in range(0, w, 48):
        pygame.draw.ellipse(surface, (20, 85, 135), (rx, h // 2 - 10, 32, 20))


def _draw_frog(surface: pygame.Surface, cx: int, cy: int, size: int = 56):
    r = pygame.Rect(cx - size // 2, cy - size // 2, size, size)
    pygame.draw.ellipse(surface, LIGHT_GREEN, r)
    for ex in (r.x + 14, r.right - 14):
        pygame.draw.circle(surface, WHITE, (ex, r.y + 14), 10)
        pygame.draw.circle(surface, BLACK, (ex + 1, r.y + 14), 5)
    pygame.draw.arc(surface, BLACK, (r.x + 14, r.centery, size - 28, 18), 3.14, 0, 3)


def draw_menu(surface: pygame.Surface, high_score: int):
    w, h = surface.get_size()
    _draw_background(surface)

    font_big = pygame.font.SysFont("Arial", 62, bold=True)
    font_med = pygame.font.SysFont("Arial", 30)
    font_sm = pygame.font.SysFont("Arial", 22)

    title = font_big.render("FROG LEAP", True, GOLD)
    surface.blit(title, title.get_rect(center=(w // 2, h // 2 - 170)))

    _draw_frog(surface, w // 2, h // 2 - 55, 70)

    prompt = font_med.render("Press  ENTER  to Play", True, WHITE)
    surface.blit(prompt, prompt.get_rect(center=(w // 2, h // 2 + 60)))

    hints = ["Arrow Keys / WASD — Move", "ESC — Quit"]
    for i, hint in enumerate(hints):
        t = font_sm.render(hint, True, GRAY)
        surface.blit(t, t.get_rect(center=(w // 2, h // 2 + 115 + i * 28)))

    if high_score > 0:
        hs = font_med.render(f"Best: {high_score}", True, GOLD)
        surface.blit(hs, hs.get_rect(center=(w // 2, h // 2 + 200)))


def draw_hud(surface: pygame.Surface, score: int, high_score: int):
    font = pygame.font.SysFont("Arial", 28, bold=True)

    bar = pygame.Surface((surface.get_width(), 44), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 130))
    surface.blit(bar, (0, 0))

    sc = font.render(f"Score: {score}", True, WHITE)
    hs = font.render(f"Best: {high_score}", True, GOLD)
    surface.blit(sc, (12, 8))
    surface.blit(hs, (surface.get_width() - hs.get_width() - 12, 8))


def draw_game_over(surface: pygame.Surface, score: int, high_score: int):
    w, h = surface.get_size()

    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    font_big = pygame.font.SysFont("Arial", 54, bold=True)
    font_med = pygame.font.SysFont("Arial", 32)
    font_sm = pygame.font.SysFont("Arial", 24)

    go = font_big.render("GAME OVER", True, RED)
    sc = font_med.render(f"Score: {score}", True, WHITE)
    hs = font_med.render(f"Best:  {high_score}", True, GOLD)
    ret = font_sm.render("ENTER to play again  |  ESC to quit", True, GRAY)

    surface.blit(go, go.get_rect(center=(w // 2, h // 2 - 80)))
    surface.blit(sc, sc.get_rect(center=(w // 2, h // 2)))
    surface.blit(hs, hs.get_rect(center=(w // 2, h // 2 + 44)))
    surface.blit(ret, ret.get_rect(center=(w // 2, h // 2 + 110)))
