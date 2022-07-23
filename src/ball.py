import micropython

class Ball:
    def __init__(self, lane_size, lane_coordinate, position=0, speed=1, width=1):
        self.lane_size = lane_size
        self.lane_coordinate = lane_coordinate
        self.position = position
        self.speed = speed
        self.width = width
        self.color = (127, 255, 127)
        # hack to get subposition correctly set at start
        if position == lane_size - 1:
            self._subposition = (lane_size << 3) - 1
        else:
            self._subposition = position << 3

    def update(self):
        self.move_by(self.speed)
        # handle bounces
        l = self.position < 0
        r = self.position >= self.lane_size
        if r:
            self.position = self.lane_size - 1
            self._subposition = (self.lane_size << 3) - 1
        if l:
            self.position = 0
            self._subposition = 0
        if l or r:
            self.speed *= -1
            self.color = tuple(reversed(self.color))
            return self.position

    def move_by(self, value):
        self._subposition += value
        self.position = self._subposition >> 3

    @micropython.native
    def render(self, buf):
        # reduce lookups inside loops
        spd = self.speed
        lc = self.lane_coordinate
        pos = self.position
        sp = buf.set_pixel
        color = self.color
        # when speed is 0, shift color by 2 bits every 4 frames
        cs = ((buf.render_count >> 2 ) & 1) << 2
        if spd == 0:
            color = tuple(i >> cs for i in self.color)
            for y in range(self.width):
                sp(pos, lc+y, color)
            return
        direction = -spd // abs(spd)
        for y in range(self.width):
            for i in range(3):
                sp(pos + i*direction, lc+y, tuple(j>>i for j in color))
