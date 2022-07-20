import picounicorn

class Ball:
    def __init__(self, lane_size, lane_coordinate, position=0, speed=1, max_speed=8):
        self.lane_size = lane_size
        self.lane_coordinate = lane_coordinate
        self.position = position
        self.speed = speed
        self._subposition = position << 3

    def update(self):
        self._subposition += self.speed
        self.position = self._subposition >> 3
        if self.position >= self.lane_size:
            self.position = self.lane_size - 1
            self._subposition = self.position << 3
            self.speed *= -1
        if self.position < 0:
            self.position = 0
            self.speed *= -1

    def move(self, pos, speed=None):
        self.position = pos
        self._subposition = pos << 3
        if speed is not None:
            self.speed = speed

    def set_pixel(self, x, y, r, g, b):
        if x >= 0 and x < self.lane_size:
            picounicorn.set_pixel(x, y, r, g, b)

    def render(self):
        if self.speed == 0:
            self.set_pixel(self.position, self.lane_coordinate, 255, 0, 0)
            return
        direction = -self.speed // abs(self.speed)
        for i in range(4):
            self.set_pixel(self.position + i*direction, self.lane_coordinate, 255 >> i, 0, 0)
