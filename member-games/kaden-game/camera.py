class Camera:
    def __init__(self, screen_height: int, target_frac: float = 0.62):
        self.screen_height = screen_height
        self.target_screen_y = int(screen_height * target_frac)
        self.offset_y: float = 0.0
        self._desired: float = 0.0
        self.lerp = 0.12

    def snap(self, player_world_y: int):
        self._desired = player_world_y - self.target_screen_y
        self.offset_y = self._desired

    def update(self, player_world_y: int):
        self._desired = player_world_y - self.target_screen_y
        self.offset_y += (self._desired - self.offset_y) * self.lerp

    def world_to_screen_y(self, world_y: float) -> int:
        return int(world_y - self.offset_y)
