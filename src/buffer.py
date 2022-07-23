import gc
import micropython
import picounicorn
from font import font

# Tried to use bytearray for the buffer instead of a list of strings
# but I found that it was considerably slower due to the conversion
# from memoryview instance to three ints for colors

class Buffer:
    def __init__(self, width=None, height=None):
        self.width = width or picounicorn.get_width()
        self.height = height or picounicorn.get_height()
        self.buffer = []
        self.render_count = 0
        # build buffer in memory
        for x in range(self.width):
            self.buffer.append([])
            for y in range(self.height):
                self.buffer[x].append((0, 0, 0))

    @micropython.native
    def clear(self):
        # save a millisecond
        buf = self.buffer
        h = self.height
        for x in range(self.width):
            for y in range(h):
                buf[x][y] = (0, 0, 0)

    @micropython.native
    def blit(self, bitmap, color, x_off=0, y_off=0):
        sp = self.set_pixel
        for y, row in enumerate(bitmap):
            for x, bit in enumerate(row):
                if bit:
                    sp(x+x_off, y+y_off, color)

    @micropython.native
    def draw_char(self, char, color, x_off=0, y_off=0):
        self.blit(font[ord(char)], color, x_off, y_off)

    @micropython.native
    def set_pixel(self, x, y, color):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.buffer[x][y] = color

    @micropython.native
    def render(self):
        # save us having to look up self.* in the tight loop here (saves 1ms/frame)
        buf = self.buffer
        h = self.height
        sp = picounicorn.set_pixel
        for x in range(self.width):
            for y in range(h):
                sp(x, y, *buf[x][y])
        self.render_count += 1
        # this stabilizes slowdowns due to all the memory thrashing we do with this buffering method
        #gc.collect()
