import sys

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
    def __repr__(self):
        if self.orientation == "up":
            return "/" + str(self.row) + "," + str(self.col) + "\\"
        else:
            return "\\" + str(self.row) + "," +  str(self.col) + "/"
    
    def print_neighbors(self):
        print("left: " + str(self.board.get_space_left(self)))    
        print("right: " + str(self.board.get_space_right(self)))    
        print("up: " + str(self.board.get_space_up(self)))    
        print("down: " + str(self.board.get_space_down(self)))    

    def get_left_neighbor(self):
        return self.board.get_space_left(self.row, self.col)

    def get_right_neighbor(self):
        return self.board.get_space_right(self.row, self.col)

    def get_above_neighbor(self):
        return self.board.get_space_above(self.row, self.col)

    def get_below_neighbor(self):
        return self.board.get_space_below(self.row, self.col)

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
            for col in range(row*2 + 1):
                print("adding row " + str(row) + " and col " + str(col))
                tmp_space = Space(row, col, self, space_width)
                tmp_row.append(tmp_space)
            self.space_array.append(tmp_row)

    def get_space_list(self):
        space_list = []
        for tmp_row in self.space_array:
            for tmp_space in tmp_row:
                space_list.append(tmp_space)
        return space_list
            
    def print_board(self):
        for row in range(self.board_size):
            for empty_col in range(self.board_size - row - 1):
                sys.stdout.write("       ")
            print(self.space_array[row])

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
        if self.space_array[row][col].orientation == "up":
            return None
        if not self.in_bounds(row - 1, col - 1):
            return None
        return self.space_array[row - 1][col - 1]
    
    # returns the space below, otherwise returns None
    def get_space_below(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if self.space_array[row][col].orientation == "down":
            return None
        if not self.in_bounds(row + 1, col + 1):
            return None
        return self.space_array[row + 1][col + 1]
    
    # returns the space to the left, otherwise returns None
    def get_space_left(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if not self.in_bounds(row, col - 1):
            return None
        return self.space_array[row][col - 1]

    # returns the space to the right, otherwise returns None
    def get_space_right(self, row, col):
        if not self.in_bounds(row, col):
            return None
        if not self.in_bounds(row, col + 1):
            return None
        return self.space_array[row][col + 1]
    
    # returns a list of neighbors. len > 0 and len <= 3
    def get_neighbors(self, row, col):
        tmp = self.get_space_above(row, col)
        if tmp != None:
            neighbors.append(tmp)
        tmp = self.get_space_left(row, col)
        if tmp != None:
            neighbors.append(tmp)
        tmp = self.get_space_right(row, col)
        if tmp != None:
            neighbors.append(tmp)
        tmp = self.get_space_below(row, col)
        if tmp != None:
            neighbors.append(tmp)
        return neighbors
