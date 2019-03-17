from node import *
from board import *

board = Board(board_size=4)
board.print_board()

board.print_state()

tree = Decision_Tree(board)
base_node = tree.root_node

print("================================= single root node print ======================")
base_node.print_node()
print("================================ enumerate node testing ======================")
base_node.enumerate_nodes()
print("************BASE NODE*******************")
base_node.print_node()
print("***********CHILDREN 1 *******************")
base_node.children[0].print_node()
print("***********CHILDREN 2 *******************")
base_node.children[1].print_node()
print("====================================enumerate child noe ========================")
base_node.children[1].enumerate_nodes()
base_node.children[1].print_node()
base_node.children[1].children[0].print_node()

print("================================== print node recursive test ======================")
base_node.print_node_recursive()

print("================================== update_best_move_test ==========================")
tree = Decision_Tree(board)
base_node = tree.root_node
base_node.enumerate_nodes()
base_node.print_node_and_children()
base_node.update_best_move()
base_node.print_node_and_children()

print("ONCE MORE WITH FEELING")
base_node = base_node.children[0]
base_node.enumerate_nodes()
base_node = base_node.children[0]
base_node.enumerate_nodes()
base_node.print_node_and_children()
base_node.update_best_move()
base_node.print_node_and_children()

print("============================== update_self_and_tree_above ==========================")

tree = Decision_Tree(board)
base_node = tree.root_node

base_node.print_node()
base_node.enumerate_nodes()
base_node.children[1].enumerate_nodes()
base_node.children[1].children[0].enumerate_nodes()
base_node.print_node_recursive()
base_node.children[1].children[0].children[0].update_tree_above()
base_node.print_node_recursive()

