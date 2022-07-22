import time

class Scroller:
    def __init__(self, buf, framerate=60, char_width=5):
        self.buf = buf
        self.ticks_per_frame = 1000 // framerate # rough, but err faster than slower
        self.char_width = char_width
        
    def scroll(self, text, color):
        # characters are up to 5 pixels wide, add one for spacing
        cw = self.char_width
        text_width = len(text)*cw

        buf = self.buf
        w = self.buf.width

        for i in range(text_width + w):
            start = time.ticks_ms()
            buf.clear()
            for j, c in enumerate(text):
                buf.draw_char(c, color, x_off=w-i+j*cw)
            buf.render()

            # wait for next frame
            end = time.ticks_ms()
            wait_for = self.ticks_per_frame + time.ticks_diff(start, end)
            print(f"Waiting for {wait_for:>3} ms")
            time.sleep_ms(wait_for)
