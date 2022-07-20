import picounicorn

class Ball:
    def __init__(self, lane_size, lane_coordinate, position=0, speed=1):
        self.lane_size = lane_size
        self.lane_coordinate = lane_coordinate
        self.position = position
        self.speed = speed
        
    def move(self, pos=None, speed=None):
        if pos is None:
            self.position += self.speed
            if self.position >= self.lane_size:
                self.position = self.lane_size - 1
                self.speed *= -1
            if self.position < 0:
                self.position = 0
                self.speed *= -1
        else:
            self.position = pos
            if speed is not None:
                self.speed = speed
        
    def set_pixel(self, x, y, r, g, b):
        if x >= 0 and x < self.lane_size:
            picounicorn.set_pixel(x, y, r, g, b)
        
    def render(self):
        direction = -self.speed // abs(self.speed)
        for i in range(4):
            self.set_pixel(self.position + i*direction, self.lane_coordinate, 255 >> i, 0, 0)