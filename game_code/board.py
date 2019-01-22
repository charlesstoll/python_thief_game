

class Space(object):
    def __init__(self, row, col, board, space_width=100):
        self.space_width = space_width
        self.row = row
        self.col = col
        self.board = board
        # figure out if we are pointing up or down. it will be useful....
        if col % 2 == 0:
            self.orientation = "up"
        else:
            self.orientation = "down"
        # init the array. needs to be filled at a later time though
        self.neighbors = []

    # this should be readable for boards up to size 6 (no double digit cols)
    def __str__(self):
        if self.orientation == "up":
            return "|" + str(self.row) + str(self.col) + " up |"
        else:
            return "|" + str(self.row) + str(self.col) + "down|"
    
    def get_neighbors(self):
        self.neighbors.append(self.board.get_neighbors(self.row, self.col))

class Thief(object):
    def __init__(self, location, board):
        self.location = location
        self.board = board

class Policeman(object):
    def __init__(self, location, board):
        self.location = location
        self.board = board

class Board(object):
    def __init__(self, board_size=4, space_width=100, num_police=2):
        
        #create an array of spaces that we can use
        if(board_size <= 0):
            board_size = 4
        self.board_size = board_size
        self.space_array = []
        for row in range(board_size):
            tmp_row = []
            for col in range(row+1):
                print("adding row " + str(row) + " and col " + str(col))
                tmp_space = Space(row, col, self, space_width)
                tmp_row.append(tmp_space)
            self.space_array.append(tmp_row)
    
    def print_board(self):
        for i in range(self.board_size):
            print(self.space_array[i])

    # returns true if the given row, col are on the edge of the board
    def is_an_edge(self, row, col):
        #left edge of triangle
        if col == 0:
            return True
        #bottom of triangle
        if (row == self.board_size - 1) and (col % 2 == 0):
            return True
        #right of triangle
        if (col == (row * 2)):
            return True
        return False

    # returns true if the given row, col are in the board
    def in_bounds(self, row, col):
        if row < 0 or row > self.board_size - 1:
            return False
        if col < 0 or col > row * 2:
            return False
        return True

    # returns the space above, otherwise returns None
    def get_space_above(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if (row - 1 >= 0) and (col - 1 >= 0):
            return self.space_array(row - 1, col - 1)
        return None
    
    # returns the space to the left, otherwise returns None
    def get_space_left(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if col >= 0:
            return self.space_array(row, col - 1)
        return None

    # returns the space to the right, otherwise returns None
    def get_space_right(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if col < row * 2:
            return self.space_array(row, col + 1)
        return None
    
    # returns a list of neighbors. len > 0 and len <= 3
    def get_neighbors(self, row, col):
        neighbors = []
        tmp = self.get_space_above(row, col)
        if tmp != None:
            neighbors.append(tmp)
        tmp = self.get_space_left(row, col)
        if tmp != None:
            neighbors.append(tmp)
        tmp = self.get_space_right(row, col)
        if tmp != None:
            neighbors.append(tmp)
        return neighbors
