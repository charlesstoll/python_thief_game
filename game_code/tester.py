import board as gc

my_board = gc.Board(board_size=3)

my_board.print_board()

space_list = my_board.get_space_list()
for space in space_list:
   print("---for space " + str(space) + " -------------------")
   left = space.get_left_neighbor()
   right = space.get_right_neighbor()
   above = space.get_above_neighbor()
   below = space.get_below_neighbor()
   print("left: " + str(left))
   print("right: " + str(right))
   print("above: " + str(above))
   print("below: " + str(below))
