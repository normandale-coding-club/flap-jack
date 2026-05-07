import pygame
import physics

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

physObjList = []
player = physics.physObj(True, 40, (255, 20, 20), pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), pygame.Vector2(0,0), 1, )
physObjList.append(player)
ropelength = 300
ropeNum = 2000
i = 0
while i < ropeNum:
    ropeObj = physics.physObj(False, 1, (0, 0, 0), pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), pygame.Vector2(0,0), 1)
    ropeObj.ropey = ropelength - (i*ropelength/ropeNum)
    physObjList.append(ropeObj)
    i += 1

def physics():
    mouse_pos = pygame.mouse.get_pos()
    for phy in physObjList:
        phy.velocity += pygame.Vector2(0, 3000) * dt
        if hasattr(phy, 'ropey'):
            rope = pygame.Vector2(phy.pos - mouse_pos)
            if rope.length() > phy.ropey:
                phy.velocity -= rope
            if rope.length() > phy.ropey:
                phy.pos = mouse_pos + (rope.normalize() * phy.ropey)
    rope = pygame.Vector2(player.pos - mouse_pos)
    if rope.length() > 300:
        player.velocity -= rope
    if rope.length() > 300:
        player.pos = mouse_pos + (rope.normalize() * 300)
    for phy in physObjList:
        phy.velocity *= 1 - (.8 * dt)
        phy.pos += phy.velocity * dt

def render():
    screen.fill((50, 190, 255))
    for phys in physObjList:
        pygame.draw.circle(screen, phys.color, phys.pos, phys.size)
    pygame.display.flip()
    pass

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    physics()
    render()

pygame.quit()