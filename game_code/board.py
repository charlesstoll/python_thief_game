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

    # this should be readable for boards up to size 6 (no double digit cols)
    def __repr__(self):
        piece = self.board.get_piece_at_location(self.row, self.col)
        if type(piece) is Thief:
            rep = "t"
        elif type(piece) is Policeman:
            rep = "p"
        else:
            rep = " "
        if self.orientation == "up":
            return "/" + str(self.row) + "," + str(self.col) + rep + "\\"
        else:
            return "\\" + str(self.row) + "," +  str(self.col) + rep + "/"
    
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

class Piece(object):
    def __init__(self, row, col, board):
        self.row = row
        self.col = col
        self.board = board
        if board.in_bounds(row, col):
            self.on_board = True
        else:
            self.on_board = False

    def __repr__(self):
        if self.on_board:
            return "( " + str(self.row) + " , " + str(self.col) + " )"
        else:
            return "Not on board"


    def place(self, row, col):
        if not self.board.is_occupied(row, col):
            self.row = row
            self.col = col
            self.on_board = True
        else:
            self.row = -1
            self.col = -1
            self.on_board = False

    # move in one direction 1 space. True/False return for success/failure
    def move(self, direction):
        # some sanity checks
        if not self.on_board:
           return False

        # first, get the space we want to get to 
        if direction == "up":
            next_space = self.board.get_space_above(self.row, self.col)
        elif direction == "down":
            next_space = self.board.get_space_below(self.row, self.col)
        elif direction == "left":
            next_space = self.board.get_space_left(self.row, self.col)
        elif direction == "right":
            next_space = self.board.get_space_right(self.row, self.col)
        else:
            next_space = None
        # now do some safety/sanity checks
        if next_space == None:
            return False
        if self.board.is_occupied(next_space.row, next_space.col):
            return False
        
        # try to place and return
        return self.place(next_space.row, next_space.col)


class Thief(Piece):
    def __init__(self, row, col, board):
        Piece.__init__(self, row, col, board)

    def __repr__(self):
        return "Thief: " + Piece.__repr__(self)

class Policeman(Piece):
    def __init__(self, row, col, board):
        Piece.__init__(self, row, col, board)

    def __repr__(self):
        return "Policeman: " + Piece.__repr__(self)

class Board(object):
    def __init__(self, board_size=4, space_width=100, num_police=2):
        
        # create an array of spaces that we can use
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
        
        # now create some pieces and remember them in useful groupings
        self.all_pieces = []
        self.policemen = []
        for tmp in range(num_police):
            tmp = Policeman(self.board_size-1, tmp, self)
            self.policemen.append(tmp)
            self.all_pieces.append(tmp)
        self.thief = Thief(0,0, self)
        self.all_pieces.append(self.thief)

    def get_space_list(self):
        space_list = []
        for tmp_row in self.space_array:
            for tmp_space in tmp_row:
                space_list.append(tmp_space)
        return space_list
            
    def print_board(self):
        for row in range(self.board_size):
            for empty_col in range(self.board_size - row - 1):
                sys.stdout.write("        ")
            print(self.space_array[row])
        
        for piece in self.all_pieces:
            print(piece)

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

    # returns the space at row, col
    def get_space(self, row, col):
        if self.in_bounds(row, col):
            return self.space_array[row][col]
        return None

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

    # find out if there is already something in a space
    def is_occupied(self, row, col):
        if not self.in_bounds(row, col):
            # not great to say that it is occupied since it is not a space
            # but whatever... if it is an issue we can fix it them
            return True
        for piece in self.all_pieces:
            if piece.row == row and piece.col == col:
                return True
        return False

    # find out what piece is on a square
    def get_piece_at_location(self, row, col):
        if not self.is_occupied(row, col):
            return None
        for piece in self.all_pieces:
            if piece.row == row and piece.col == col:
                return piece
        return None
