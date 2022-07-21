import picounicorn
import gc

class Buffer:
    def __init__(self, width=None, height=None):
        self.width = width or picounicorn.get_width()
        self.height = height or picounicorn.get_height()
        self.buffer = []
        # build buffer in memory
        for x in range(self.width):
            self.buffer.append([])
            for y in range(self.height):
                self.buffer[x].append((0, 0, 0))
        
    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.buffer[x][y] = (0, 0, 0)
                
    def set_pixel(self, x, y, color):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.buffer[x][y] = color
    
    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                picounicorn.set_pixel(x, y, *self.buffer[x][y])
        # this stabilizes slowdowns due to all the memory thrashing we do with this buffering method
        gc.collect()
