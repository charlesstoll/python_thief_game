import sys
import math
sys.path.append("../communication/")
sys.path.append("../vision/")
from Robot_Class_Tracking import *
# used for ai and copying the game state
import copy
from node import *

debug = 1
pr_debug = 0

# this line needs to be changed to pass in the correct value of the camera index
cv_info = Robot_Track(0)

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

N = 0
E = 90
S = 180
W = 270
NE = 60
SE = 120
SW = 240
NW = 300

class Piece(object):
    def __init__(self, row, col, board, ip_address, name):
        self.row = row
        self.col = col
        self.board = board
        self.ip_address = ip_address
        self.direction = N #0 refers to pointing north
        if board.in_bounds(row, col):
            self.on_board = True
        else:
            self.on_board = False

    def __repr__(self):
        if self.on_board:
            return "( " + str(self.row) + " , " + str(self.col) + " )"
        else:
            return "Not on board"

    def turn(self, new_direction, send=0):
#        turn_amount = new_direction - self.direction
#        turn_amount = (turn_amount + 180) % 360 - 180
        command = 'none'
        if(new_direction == N):
            command = 'up'
        elif(new_direction == NE):
            command = 'right_up'
        elif(new_direction == SE):
            command = 'right_down'
        elif(new_direction == S):
            command = 'down'
        elif(new_direction == SW):
            command = 'left_down'
        elif(new_direction == NW):
            command = 'left_up'
        else:
            return
        if((debug == 0) and (send == 1)):
            print("i would have sent somethin out here but not anymore")
        self.direction = new_direction

    def place(self, row, col):
        if not self.board.is_occupied(row, col):
            self.row = row
            self.col = col
            self.on_board = True
            return True
        else:
            self.row = -1
            self.col = -1
            self.on_board = False
            return False

    # move in one direction 1 space. True/False return for success/failure
    def move(self, direction, send=0):
        # some sanity checks
        if not self.on_board:
            return False

        # first, get the space we want to get to 
        if direction == "stay":
            return True
        elif direction == "up":
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
        # NOTE: if the space we are moving into is oriented "up," then we 
        # are on a space that is oriented "down" so everything here looks a
        # little backwards but it is not
        print("CHECKING SEND HERE")
        if(send == 1 and debug == 0):
            print("sending--------------------------------------------------------------------")
            piece_name = self.board.char_order[self.board.next_to_move]
            cv_info.move_robot(piece_name, self.ip_address, next_space.row, next_space.col)

        return self.place(next_space.row, next_space.col)


class Thief(Piece):
    def __init__(self, row, col, board, ip_address, name):
        Piece.__init__(self, row, col, board, ip_address, name)

    def __repr__(self):
        return "Thief: " + Piece.__repr__(self)

class Policeman(Piece):
    def __init__(self, row, col, board, ip_address, name):
        Piece.__init__(self, row, col, board, ip_address, name)

    def __repr__(self):
        return "Policeman: " + Piece.__repr__(self)

ip_addr_p = ["192.168.137.4", "192.168.137.66"]
ip_addr_t = "192.168.137.7"

class Board(object):
    def __init__(self, board_size=4, space_width=100, num_police=2):
        
        # used for node-base ai. options are 'cooperative' or 'greedy'
        self.p1_strategy = "cooperative"
        self.p2_strategy = "cooperative"

        self.search_style = "depth_first"

        # create an array of spaces that we can use
        if(board_size <= 0):
            board_size = 4
        self.game_over = 0
        self.board_size = board_size
        self.space_array = []
        self.char_order = ['t','p1','p2']
        self.next_to_move = 0
        self.last_move = 'none'
        for row in range(board_size):
            tmp_row = []
            for col in range(row*2 + 1):
                tmp_space = Space(row, col, self, space_width)
                tmp_row.append(tmp_space)
            self.space_array.append(tmp_row)
        
        # now create some pieces and remember them in useful groupings
        self.all_pieces = []
        self.policemen = []
        for tmp in range(num_police):
            tmp = Policeman(self.board_size-1, tmp, self, ip_addr_p[tmp], 'p' + str(tmp + 1))
            self.policemen.append(tmp)
            self.all_pieces.append(tmp)
        self.thief = Thief(0,0, self, ip_addr_t, 't')
        self.all_pieces.append(self.thief)

    def increment_turn(self):
        self.next_to_move = (self.next_to_move + 1) % 3

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
        print("Waiting for " + self.get_current_piece_name() + " to make a move")
        
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
    
    def get_space_direction(self, row, col, direction):
        if direction == "down":
            return self.get_space_below(row, col)
        if direction == "up":
            return self.get_space_above(row, col)
        if direction == "left":
            return self.get_space_left(row, col)
        if direction == "right":
            return self.get_space_right(row, col)
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
        tmp = self.get_space_below(row, col)
        if tmp != None:
            neighbors.append(tmp)
        return neighbors

    # REAAAAAAAAAAALLY shitty inefficent function but our grid is small and we got gigahertz of power :D
    def get_distance_between_spaces(self, row1, col1, row2, col2, max_dist=10):
        distance = 0
        if (row1 == row2) and (col1 == col2):
            return distance
        current_layer = []
        next_layer = []
        current_layer.append(self.get_space(row1, col1))
        # just go for a bit and give up past 20
        while(distance <= max_dist):
            distance = distance + 1
            # get the next row of stuffs based on current layer
            for space in current_layer:
                next_layer.extend(self.get_neighbors(space.row, space.col))
            # now check all these to see if they match
            for space in next_layer:
                if (row2 == space.row) and (col2 == space.col):
                    return distance
            current_layer = next_layer
            next_layer = []
        print("found two spaces that were more than 10 distance apart")
        return max_dist + 1

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

    def get_piece(self, piece_name):
        if(piece_name == "p1"):
            return self.policemen[0]

        if(piece_name == "p2"):
            return self.policemen[1]
        
        if(piece_name == "t"):
            return self.thief

    def get_current_piece(self):
        return self.get_piece(self.char_order[self.next_to_move])

    def get_current_piece_name(self):
        return self.char_order[self.next_to_move]

    def p_to_t_dist(self, p_number):
        if p_number < 1 or p_number > 2:
            print("ERROR: p_to_t_dist trying to find distance to nonexistant Policeman")
        # get thief space
        row_t = self.thief.row
        col_t = self.thief.col
        # get p1 space
        row_p = self.policemen[p_number - 1].row
        col_p = self.policemen[p_number - 1].col
        # get dist(p, thief)
        p_t_dist = self.get_distance_between_spaces(row_t, col_t, row_p, col_p, 8)
        return p_t_dist
    
    def move_piece(self, piece_name, move, send=0):
        # last move is used for the ai so that it knows which move it is currently evaluating
        self.last_move = move
        if(piece_name == "p1"):
        # TODO: add the logic BEFORE the move so that if the policemen is next to the thief
        # on his turn, the game ends and doesn't need a move to get there
        # TODO: also change the "get rating" fxns so that they will return the dist - 1 as
        # the rating
            if self.p_to_t_dist(1) == 1:
                self.game_over = 1
            if self.policemen[0].move(move, send):
                return True
            # check if we couldn't move because of the thief
            space = self.get_space_direction(self.policemen[0].row, self.policemen[0].col, move)
            # we couldn't move because of no space
            if space == None:
                return False
            # we either hit a policeman or a thief so find out
            piece = self.get_piece_at_location(space.row, space.col)
            # if we hit a thief, the game is over and we can say that the turn was a success
            if type(piece) == Thief:
                self.game_over = 1
                return True
            # how did we get here???
            return False

        if(piece_name == "p2"):
            if self.p_to_t_dist(2) == 1:
                self.game_over = 1
            if self.policemen[1].move(move, send):
                return True
            # check if we couldn't move because of the thief
            space = self.get_space_direction(self.policemen[1].row, self.policemen[1].col, move)
            # we couldn't move because of no space
            if space == None:
                return False
            # we either hit a policeman or a thief so find out
            piece = self.get_piece_at_location(space.row, space.col)
            # if we hit a thief, the game is over and we can say that the turn was a success
            if type(piece) == Thief:
                self.game_over = 1
                return True
            # how did we get here???
            return False
        if(piece_name == "t"):
            return self.thief.move(move, send)

# AI section is here
    def cooperative_rating(self):
        # get dist(p1, thief)
        p1_t_dist = self.p_to_t_dist(1) 
        # get dist(p2, thief)
        p2_t_dist = self.p_to_t_dist(2) 
        # return dist(p1, thief) + dist(p2, thief)
        return p1_t_dist + p2_t_dist
        return math.sqrt((p1_t_dist * p1_t_dist) + (p2_t_dist * p2_t_dist)) - 1

    def p1_greedy_rating(self):
        # get thief space
        row_t = self.thief.row
        col_t = self.thief.col
        # get p1 space
        row_p1 = self.policemen[0].row
        col_p1 = self.policemen[0].col
        # get dist(p1, thief)
        p1_t_dist = self.get_distance_between_spaces(row_t, col_t, row_p1, col_p1, 8)
        # return dist(p1, thief)
        return p1_t_dist - 1

    def p2_greedy_rating(self):
        # get thief space
        row_t = self.thief.row
        col_t = self.thief.col
        # get p2 space
        row_p2 = self.policemen[1].row
        col_p2 = self.policemen[1].col
        # get dist(p2, thief)
        p2_t_dist = self.get_distance_between_spaces(row_t, col_t, row_p2, col_p2, 8)
        # return dist(p2, thief)
        return p2_t_dist -1
    
    # this funciton just calls the correct ai movement algorithm
    def ai_move(self, depth):
        search_style = self.search_style
        print("doing a search using a " + search_style + " style search")
        print("p1 is being " + self.p1_strategy + " and p2 is being " + self.p2_strategy)
        if(search_style == "depth_first"):
            tree = Decision_Tree(self)
            best_move = tree.find_depth_first(depth)
            print("***************************************BEST MOVE IS " + best_move)
            self.move_piece(self.char_order[self.next_to_move], best_move, send=1)
            print("I made a move!! " + self.char_order[self.next_to_move] +" went " + best_move)
        if(search_style == "breadth_first"):
            tree = Decision_Tree(self)
            best_move = tree.find_breadth_first(depth)
            print("BEST MOVE IS " + best_move)
            self.move_piece(self.char_order[self.next_to_move], best_move, send=1)
            print("I made a move!! " + self.char_order[self.next_to_move] +" went " + best_move)

        # functions for node-based ai stuffs
# state1.get_options() -> return a list of all DOABLE options for how to move from this state
    def get_options(self):
        curr_piece = self.get_current_piece()
        directions = ["down", "up", "left", "right"]
        doable_options = []
        # we can always just stay
        doable_options.append("stay")
        for option in directions:
            tmp_space = self.get_space_direction(curr_piece.row, curr_piece.col, option)
            if tmp_space == None:
                continue
            if self.is_occupied(tmp_space.row, tmp_space.col):
                continue
            doable_options.append(option)
        return doable_options

# state1.get_node_rating() -> gets the value (goodness) of the given state
    def get_node_rating(self):
        # find the t rating
        t_rating = self.cooperative_rating() 
        # find p1's rating
        p1_rating = 1000
        if self.p1_strategy == "cooperative":
            p1_rating = self.cooperative_rating()
        elif self.p1_strategy == "greedy":
            p1_rating = self.p1_greedy_rating()
        else:
            print("ERROR: bad strategy for p1")
        # find p2's rating
        p2_rating = 1000
        if self.p2_strategy == "cooperative":
            p2_rating = self.cooperative_rating()
        elif self.p2_strategy == "greedy":
            p2_rating = self.p2_greedy_rating()
        else:
            print("ERROR: bad strategy for p2")
        # store all ratings in the list and return it
        node_rating = []
        node_rating.append(t_rating)
        node_rating.append(p1_rating)
        node_rating.append(p2_rating)
        return node_rating

# state1.get_cost(state2) -> gets the cost to move from state2 to state1
#   # NOTE: this is not needed for our game or for node.py at the moment
# state1.do_option(option) -> does the option move on the state
    def do_option(self, option):
        curr_piece = self.get_current_piece_name()
        self.move_piece(curr_piece, option)
        self.increment_turn()

# state1.get_better_choice(r1, op1, r2, op2) -> returns the better rating, option pair
# NOTE: the logic here is dependant on what values you are saving during the get_node_rating fxn
    def get_better_choice(self, r1, op1, r2, op2):
        curr_piece = self.get_current_piece_name()
        # return max for thief
        if curr_piece == "t":
            if r1[0] > r2[0]:
                return (r1, op1)
            else:
                return (r2, op2)
        # return min for p1
        if curr_piece == "p1":
            if r1[1] < r2[1]:
                return (r1, op1)
            else:
                return (r2, op2)
        # return min for p2
        if curr_piece == "p2":
            if r1[2] < r2[2]:
                return (r1, op1)
            else:
                return (r2, op2)

# state1.should_exit_search(rating) -> returns true if this is a rating that is good enough to stop
    def should_exit_search(self, rating):
        curr_piece = self.get_current_piece_name()
        if curr_piece == "t":
            print("ERROR: we are being asked to choose a final move for the thief")
            return True
        if curr_piece == "p1":
            if rating[1] == 0:
                return True
            return False
        if curr_piece == "p2":
            if rating[2] == 0:
                return True
            return False
        print("ERROR: piece_name is not valid!!!")
        return True

    def print_state(self):
        self.print_board()
