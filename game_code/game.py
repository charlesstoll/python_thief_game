import sys
from board import *

exit = 0
print("Welcome to the Thief game! The only game where police try to catch bad guys!")
while(exit != 1):
    if(input("Would you like to start a new game? y/n  ") != "y"):
        print("Goodbye!")
        sys.exit()
    board_size = int(input("What size of board would you like?  "))
    board = Board(board_size=board_size)
    if(input("Would you like to choose your own starting positions? y/n  ") == "y"):
        print("Which row and column would you like the Thief to start in?")
        t_row = int(input("row:  "))
        t_col = int(input("col:  "))
        print("Which row and column would you like Policeman 1 to start in?")
        p1_row = int(input("row:  "))
        p1_col = int(input("col:  "))
        print("Which row and column would you like Policeman 2 to start in?")
        p2_row = int(input("row:  "))
        p2_col = int(input("col:  "))
        board.thief.place(t_row, t_col)
        board.policemen[0].place(p1_row, p1_col)
        board.policemen[1].place(p2_row, p2_col)
    char_order = []
    next_to_move = 0
    if(input("Would you like to choose character order? y/n  ") == "y"):
        char_order.append(input("Who goes first? t/p1/p2  "))
        char_order.append(input("Who goes second? t/p1/p2  "))
        char_order.append(input("Who goes third? t/p1/p2  "))
    else:
        char_order.append("t")
        char_order.append("p1")
        char_order.append("p2")
    while(board.game_over == 0):
        board.print_board()
        print("What would " + char_order[next_to_move] + " like to do?")
        moved = 0
        while(moved == 0):
            move = input("move up/down/left/right/stay: ")
            if(move == "stay"):
                moved = 1
            else:
                if(board.move_piece(char_order[next_to_move], move)):
                    moved = 1
            if(moved == 1):
                next_to_move = (next_to_move + 1) % 3
    print("**************************************************************************")
    print("**************************************************************************")
    print("******CONGRATULATIONS!!! YOU CAUGHT THE STUPID THIEF!*********************")
    print("**************************************************************************")
    print("**************************************************************************")
