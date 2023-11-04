import random

class MACHINE():
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = score
        self.drawn_lines = drawn_lines
        self.whole_lines = whole_lines
        self.whole_points = whole_points
        self.location = location

    def find_best_selection(self):
        return random.choice(self.whole_lines)

    
