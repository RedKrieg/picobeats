class Ball:
    def __init__(self, lane_size, lane_coordinate, position=0, speed=1, width=1):
        self.lane_size = lane_size
        self.lane_coordinate = lane_coordinate
        self.position = position
        self.speed = speed
        self.width = width
        # hack to get subposition correctly set at start
        if position == lane_size - 1:
            self._subposition = (lane_size << 3) - 1
        else:
            self._subposition = position << 3

    def update(self):
        self._subposition += self.speed
        self.position = self._subposition >> 3
        # handle bounces
        if self.position >= self.lane_size:
            self.position = self.lane_size - 1
            self._subposition = (self.lane_size << 3) - 1
            self.speed *= -1
            return self.position
        if self.position < 0:
            self.position = 0
            self._subposition = 0
            self.speed *= -1
            return self.position

    def move(self, pos, speed=None):
        self.position = pos
        self._subposition = pos << 3
        if speed is not None:
            self.speed = speed

    def render(self, buf):
        # reduce lookups inside loops
        spd = self.speed
        lc = self.lane_coordinate
        pos = self.position
        sp = buf.set_pixel
        # render shifter
        rs = buf.render_count % 6
        if spd == 0:
            for y in range(self.width):
                sp(pos, lc+y, (255 >> rs, 0, 0))
            return
        direction = -spd // abs(spd)
        for y in range(self.width):
            for i in range(3):
                sp(pos + i*direction, lc+y, (255 >> i, 0, 0))
