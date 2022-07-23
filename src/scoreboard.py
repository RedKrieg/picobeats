import micropython
from collections import deque

class ScoreBoard:
    def __init__(self, loc_p1, loc_p2, width, height, thickness=2):
        self.locations = (loc_p1, loc_p2)
        self.width = width
        self.height = height
        self.thickness = thickness
        self.score = width//2 - 1
        self.render_flash = deque((), width)
        self.near_win = False

    @micropython.native
    def update(self, player):
        rf = self.render_flash
        if player:
            self.score += 1
        else:
            self.score -= 1
        if self.score == -1:
            winner = 0
        elif self.score == self.width - 1:
            winner = self.score
        else:
            winner = None
        # used in renderer later to flash score bar
        self.near_win = self.score == 0 or self.score == self.width - 2
        if winner is not None:
            # reset score
            self.score = self.width//2 - 1
            # flash screen on victory
            for i in range(self.width):
                rf.append(i)
            return winner # let game engine handle the rest
        rf.append(player)

    @micropython.native
    def render(self, buf):
        # prevent name lookups inside loops for performance
        rf = self.render_flash
        sc = self.score
        sp = buf.set_pixel
        h = self.height
        t = self.thickness
        col = (63, 63, 63)
        # flash scoreboard high and low eight frames at a time
        if self.near_win and (buf.render_count >> 3) % 2:
            col = (32, 32, 32)
        fcol = (255, 255, 255)
        for i in range(t):
            for y in range(h):
                sp(sc+i, y, col)
        for i in range(len(rf)):
            x = rf.popleft()
            for y in range(h):
                sp(x, y, fcol)
