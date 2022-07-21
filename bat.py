import picounicorn

class Bat:
    def __init__(self, button, ball, voice, location_x, location_y, max_len=6):
        """
            [button] is a picounicorn button ID
            [ball] is an instance of ball.Ball
            [voice] is an instance of chirp.Chirper
            [location_x] and [location_y] are screen coordinates of the first pixel
            [max_len] is the maximum length of the bat
        """
        self.max_len = max_len
        self.length = 0
        self.button = button
        self.ball = ball
        self.voice = voice
        self.location_x = location_x
        self.location_y = location_y
        self.direction = 1 if location_x == 0 else -1
        self.color = (128, 128, 128)
        self.holding = False

    def update(self):
        """
            Checks for button input and updates bat state

            Returns True when a ball has been launched
        """
        if picounicorn.is_pressed(self.button):
            # short circuit when we're already holding a ball
            if self.holding:
                # only act on release
                return False
            # check for collision from ball movement last frame
            self.holding = self.ball.position == self.location_x + (self.length - 1) * self.direction
            # handle collision
            if self.holding:
                self.ball.speed = 0
                return False
            # don't extend past max length
            if self.length < self.max_len:
                # extend
                self.length +=1
                # check for collision after extending
                self.holding = self.ball.position == self.location_x + (self.length - 1) * self.direction
                # handle collision
                if self.holding:
                    self.ball.speed = 0
        else:
            if self.holding:
                self.ball.speed = (self.max_len - self.length + 1) * self.direction
                self.holding = False
                self.voice.play(25*self.max_len//abs(self.ball.speed))
                self.length -= 1
                return True
            if self.length > 0:
                self.length -= 1
        return False

    def render(self, buf):
        """Render the bat"""
        for i in range(self.location_x, self.location_x + self.length * self.direction, self.direction):
            buf.set_pixel(i, self.location_y, self.color)
