from collections import deque

class ScoreBoard:
    def __init__(self, loc_p1, loc_p2, width, height, thickness=2):
        self.locations = (loc_p1, loc_p2)
        self.width = width
        self.height = height
        self.thickness = thickness
        self.score = width//2 - 1
        self.render_flash = deque((), width)
        
    def update(self, player):
        if player:
            self.score += 1
            self.render_flash.append(self.width-1)
        else:
            self.score -= 1
            self.render_flash.append(0)
        if self.score == -1 or self.score == self.width-1:
            # reset score for now
            self.score = self.width//2 - 1

    def render(self, buf):
        # prevent lookups inside loops
        rf = self.render_flash
        sc = self.score
        sp = buf.set_pixel
        h = self.height
        t = self.thickness
        col = (63, 63, 63)
        fcol = (255, 255, 255)
        for i in range(t):
            for y in range(h):
                sp(sc+i, y, col)
        for i in range(len(rf)):
            x = rf.popleft()
            for y in range(h):
                sp(x, y, fcol)