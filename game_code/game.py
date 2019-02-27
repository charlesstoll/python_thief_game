import sys
from board import *

using_ai = 0
exit = 0
print("Welcome to the Thief game! The only game where police try to catch bad guys!")
while(exit != 1):
    '''
    if(input("Would you like to start a new game? y/n  ") != "y"):
        print("Goodbye!")
        sys.exit()
    board_size = int(input("What size of board would you like?  "))
    board = Board(board_size=board_size)
    if(input("Would you like to play against the ai? y/n  ") == "y"):
        using_ai = 1
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
    tmp_char_order = []
    if(input("Would you like to choose character order? y/n  ") == "y"):
        tmp_char_order.append(input("Who goes first? t/p1/p2  "))
        tmp_char_order.append(input("Who goes second? t/p1/p2  "))
        tmp_char_order.append(input("Who goes third? t/p1/p2  "))
        board.char_order = tmp_char_order
    '''
    using_ai = 1
    board= Board(board_size = 4)
    while(board.game_over == 0):
        board.print_board()
        if(using_ai == 1 and (not board.char_order[board.next_to_move] == "t")):
            print("THE AI IS MOVING NOW----------------------------------------------")
            board.ai_move(6)
            board.increment_turn()
            continue
        print("What would " + board.char_order[board.next_to_move] + " like to do?")
        moved = 0
        while(moved == 0):
            move = input("move up/down/left/right/stay: ")
            if(move == "stay"):
                moved = 1
            else:
                if(board.move_piece(board.char_order[board.next_to_move], move)):
                    moved = 1
            if(moved == 1):
                board.increment_turn()
    print("**************************************************************************")
    print("**************************************************************************")
    print("******CONGRATULATIONS!!! YOU CAUGHT THE STUPID THIEF!*********************")
    print("**************************************************************************")
    print("**************************************************************************")
