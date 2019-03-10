import sys
import math
sys.path.append("../communication/")
import client
# used for ai and copying the game state
import copy

debug = 1
pr_debug = 0

# search_styles : depth_first breadth_first test
search_style = "depth_first"
# ai_function : cooperative greedy
ai_function = "cooperative"

state_list = []

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
    def __init__(self, row, col, board, ip_address):
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

    def turn(self, new_direction):
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
        if(debug == 0):
            client.send(self.ip_address, command)
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
    def move(self, direction):
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
        if(next_space.orientation == "up"):
            if(direction == "up"):
                self.turn(N)
            if(direction == "left"):
                self.turn(SW)
            if(direction == "right"):
                self.turn(SE)
        if(next_space.orientation == "down"):
            if(direction == "down"):
                self.turn(S)
            if(direction == "left"):
                self.turn(NW)
            if(direction == "right"):
                self.turn(NE)
 
        return self.place(next_space.row, next_space.col)


class Thief(Piece):
    def __init__(self, row, col, board, ip_address):
        Piece.__init__(self, row, col, board, ip_address)

    def __repr__(self):
        return "Thief: " + Piece.__repr__(self)

class Policeman(Piece):
    def __init__(self, row, col, board, ip_address):
        Piece.__init__(self, row, col, board, ip_address)

    def __repr__(self):
        return "Policeman: " + Piece.__repr__(self)

ip_addr_p = ["127.0.0.1", "127.0.0.1"]
ip_addr_t = "127.0.0.1"

class Board(object):
    def __init__(self, board_size=4, space_width=100, num_police=2):
        
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
            tmp = Policeman(self.board_size-1, tmp, self, ip_addr_p[tmp])
            self.policemen.append(tmp)
            self.all_pieces.append(tmp)
        self.thief = Thief(0,0, self, ip_addr_t)
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

    def move_piece(self, piece_name, move):
        # last move is used for the ai so that it knows which move it is currently evaluating
        self.last_move = move
        if(piece_name == "p1"):
            if self.policemen[0].move(move):
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
            if self.policemen[1].move(move):
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
            return self.thief.move(move)


# AI section is here
    def cooperative_rating(self):
        # get thief space
        row_t = self.thief.row
        col_t = self.thief.col
        # get p1 space
        row_p1 = self.policemen[0].row
        col_p1 = self.policemen[0].col
        # get p2 space
        row_p2 = self.policemen[1].row
        col_p2 = self.policemen[1].col
        # get dist(p1, thief)
        p1_t_dist = self.get_distance_between_spaces(row_t, col_t, row_p1, col_p1, 8)
        # get dist(p2, thief)
        p2_t_dist = self.get_distance_between_spaces(row_t, col_t, row_p2, col_p2, 8)
        # return dist(p1, thief) + dist(p2, thief)
        if(p1_t_dist == 0):
            return 0
        if(p2_t_dist == 0):
            return 0
        return p1_t_dist + p2_t_dist
        return math.sqrt((p1_t_dist * p1_t_dist) + (p2_t_dist * p2_t_dist))

    def get_rating(self):
        #TODO: add some stuff here to make it always use the "cooperative" when guessing what the thief will do
        if(ai_function == "cooperative"):
            return self.cooperative_rating()
        if(ai_function == "greedy"):
            return self.greedy_rating()

    # this funciton just calls the correct ai movement algorithm
    def ai_move(self, depth):
        if(search_style == "test"):
            self.ai_move_test(self.char_order[self.next_to_move])
        if(search_style == "depth_first"):
            print("doing depth_first searching")
            self.ai_move_depth_first(depth)
        if(search_style == "breadth_first"):
            print("doing breadth_first searching")

    def ai_move_test(self, piece_name):
        if(self.move_piece(piece_name, 'right')):
            print("I made a move!! I went right")
            return
        if(self.move_piece(piece_name, 'up')):
            print("I made a move!! I went up")
            return
        if(self.move_piece(piece_name, 'left')):
            print("I made a move!! I went left")
            return
        if(self.move_piece(piece_name, 'down')):
            print("I made a move!! I went down")
            return
        self.move_piece(piece_name, 'stay')
        print("I made a move!! I just stayed still")
    
    # define this algorithm just sets up anything that needs to be done BEFORE/AFTER recursion
    def ai_move_depth_first(self, depth):
        root = copy.copy(self)
        move, rating = root.get_best_move_depth_first(depth)
        self.move_piece(self.char_order[self.next_to_move], move)
        print("I made a move!! " + self.char_order[self.next_to_move] +" went " + move)

    # does the recursion
    def get_best_move_depth_first(start_point, depth):
        max_depth = 9
        # exit if we found a game over state or if we hit recursion bottom
        rating = start_point.get_rating()
        #print("my rating is: " + str(rating))
        if(rating == 0 or depth == 0):
            #print("RECURSION EXIT POINT =====================================")
            return ('none', rating)
        
        # not exiting, so we must be recursing!!!!! so we should set that shit up...
        # first, copy the game 4 times (we have 4 possible moves)
        op_stay = copy.deepcopy(start_point)
        op_left = copy.deepcopy(start_point)
        op_right = copy.deepcopy(start_point)
        op_updown = copy.deepcopy(start_point)
        
        # now, do recursion on each new state and remember the max/min values for decision making
        maximum = -1
        minimum = 1000
        best_max_move = 'none'
        best_min_move = 'none'

        tmp_move = 'none'
        tmp_score = 0
        curr_piece = start_point.get_current_piece()
        #print("starting recursion at depth: " + str(depth) + "==================================")
        if(op_stay.move_piece(start_point.char_order[start_point.next_to_move], 'stay')):
            op_stay.increment_turn()
            if(depth > 1 and pr_debug):
                print(((max_depth-depth) * '  ') + "If " + start_point.char_order[start_point.next_to_move] + " goes stay")
            tmp_move, tmp_score = op_stay.get_best_move_depth_first(depth - 1)
            if(tmp_score <= minimum):
                best_min_move = 'stay'
                minimum = tmp_score
            if(tmp_score >= maximum):
                best_max_move = 'stay'
                maximum = tmp_score
 
        if(op_left.move_piece(start_point.char_order[start_point.next_to_move], 'left')):
            op_left.increment_turn()
            if(depth > 1 and pr_debug):
                print(((max_depth-depth) * '  ') + "If " + start_point.char_order[start_point.next_to_move] + " goes left")
            tmp_move, tmp_score = op_left.get_best_move_depth_first(depth - 1)
            if(tmp_score <= minimum):
                best_min_move = 'left'
                minimum = tmp_score
            if(tmp_score >= maximum):
                best_max_move = 'left'
                maximum = tmp_score
        
        if(op_right.move_piece(start_point.char_order[start_point.next_to_move], 'right')):
            op_right.increment_turn()
            if(depth > 1 and pr_debug):
                print(((max_depth-depth) * '  ') + "If " + start_point.char_order[start_point.next_to_move] + " goes right")
            tmp_move, tmp_score = op_right.get_best_move_depth_first(depth - 1)
            if(tmp_score <= minimum):
                best_min_move = 'right'
                minimum = tmp_score
            if(tmp_score >= maximum):
                best_max_move = 'right'
                maximum = tmp_score
        if(start_point.get_space(curr_piece.row, curr_piece.col).orientation == 'up'):
            if(op_updown.move_piece(start_point.char_order[start_point.next_to_move], 'down')):
                op_updown.increment_turn()
                if(depth > 1 and pr_debug):
                    print(((max_depth-depth) * '  ') + "If " + start_point.char_order[start_point.next_to_move] + " goes down")
                tmp_move, tmp_score = op_updown.get_best_move_depth_first(depth - 1)
                if(tmp_score <= minimum):
                    best_min_move = 'down'
                    minimum = tmp_score
                if(tmp_score >= maximum):
                    best_max_move = 'down'
                    maximum = tmp_score
        else:
            if(op_updown.move_piece(start_point.char_order[start_point.next_to_move], 'up')):
                op_updown.increment_turn()
                if(depth > 1 and pr_debug):
                    print(((max_depth-depth) * '  ') + "If " + start_point.char_order[start_point.next_to_move] + " goes up")
                tmp_move, tmp_score = op_updown.get_best_move_depth_first(depth - 1)
                if(tmp_score <= minimum):
                    best_min_move = 'up'
                    minimum = tmp_score
                if(tmp_score >= maximum):
                    best_max_move = 'up'
                    maximum = tmp_score

        # now, we return the best move that we found
        if(start_point.char_order[start_point.next_to_move] == 't'):
            if(depth > 1 and pr_debug):
                print(((max_depth-depth) * '  ') + "figuring out the thief's move, it would go: " + best_max_move)
            return (best_max_move, maximum)
        else:
            if(depth > 1 and pr_debug):
                print(((max_depth-depth) * '  ') + "figure out " + start_point.char_order[start_point.next_to_move] + "'s turn. it would go: " + best_min_move)
            return (best_min_move, minimum)
