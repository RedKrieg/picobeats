import ball
import bat
import micropython
import picounicorn
import scoreboard
import time

class Game:
    def __init__(self, voices, buttons, lanes, buf, colors, framerate=60):
        self.balls = []
        self.bats = []
        for i, l in enumerate(lanes):
            self.balls.append(ball.Ball(buf.width,
                                        l,
                                        position=(buf.width - 1) if i%2 else 0,
                                        speed=-1 if i%2 else 1,
                                        width=2,
                                        ))
            for player in range(2):
                self.bats.append(bat.Bat(buttons[player][i],
                                    self.balls[i],
                                    voices[i],
                                    (buf.width - 1) if player else 0,
                                    l,
                                    width=2,
                                    team_color=colors[player]
                                    ))
        self.sb = scoreboard.ScoreBoard(0, buf.width - 1, buf.width, buf.height)
        self.buf = buf
        self.framerate = framerate
        self.ticks_per_frame = 1000 // framerate # rough, but err faster than slower

    @micropython.native
    def play(self):
        winner = None
        buf = self.buf
        while winner is None:
            start = time.ticks_ms()
            # update bat before ball to allow for hits
            for bt in self.bats:
                bt.update()
            for bl in self.balls:
                point=bl.update()
                if point is not None:
                    winner = self.sb.update(point)

            # start rendering
            buf.clear()
            self.sb.render(buf)
            for bt in self.bats:
                bt.render(buf)
            for bl in self.balls:
                bl.render(buf)

            # write to led array
            buf.render()

            # wait for next frame
            end = time.ticks_ms()
            wait_for = self.ticks_per_frame + time.ticks_diff(start, end)
            print(f"Waiting for {wait_for:>3} ms")
            time.sleep_ms(wait_for)

        return winner
