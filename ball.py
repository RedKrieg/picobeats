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
        # handle bounces
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

    def render(self, buf):
        spd = self.speed
        lc = self.lane_coordinate
        pos = self.position
        if spd == 0:
            buf.set_pixel(pos, lc, (255, 0, 0))
            return
        direction = -spd // abs(spd)
        for i in range(4):
            buf.set_pixel(pos + i*direction, lc, (255 >> i, 0, 0))
