

class Space(object):
    def __init__(self, space_width=100):
        self.space_width = space_width
        # this could be "none" "thief" or "police"
        self.occupied_by = "none"

class Board(object):
    def __init__(self, board_size=4, space_width=100, num_police=2):

