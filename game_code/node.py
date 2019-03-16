#!/bin/python3

import sys
import copy
import math

# creates a decision tree for searching the tree. The class passed in
# as the object for the root node needs to have a few functions:
# state1.get_options() -> return a list of all DOABLE options for how to move from this state
# state1.get_node_rating() -> gets a list of all player's rating of the state (order is left to state implementation)
# state1.do_option(option) -> does the option move on the state
# state1.get_better_choice(r1, op1, r2, op2) -> returns the better rating, option pair
# state1.print_state() -> prints out the state
# state1.should_exit_search(rating) -> returns true if this is a rating that is good enough to stop
#                                      our search on
class Decision_Tree(object):
    def __init__(self, base_state):
        self.root_node = Node(copy.deepcopy(base_state), self)
        self.nodes_to_iterate = []
    
    def find_depth_first(self, depth):
        self.nodes_to_iterate.append(self.root_node)
        self.recursive_find_depth_first(depth)
        return self.root_node.best_move

    def recursive_find_depth_first(self, depth):
        # recursive exit point. we just return the best thing we have found
        if len(self.nodes_to_iterate) == 0:
            return
        # if we got a winning move, just do that move
        if self.root_node.state.should_exit_search(self.root_node.rating):
            return
        # apparently we are not done so keep going
        next_node = self.nodes_to_iterate.pop(0)
        if next_node.depth == depth:
            return
        next_node.enumerate_nodes()
        # added some new nodes so get our best move
        next_node.update_self_and_tree_above()
        self.nodes_to_iterate.extend(next_node.children)
        # keep going!!!
        self.recursive_find_depth_first(depth)

class Node(object):
    def __init__(self, state, tree, depth=0, parent=None):
        self.state = state
        self.tree = tree
        self.options = self.state.get_options()
        self.rating = self.state.get_node_rating()
        self.parent = parent
        self.depth = depth
        self.best_move = "err"
        self.children = []
    
    def print_node(self):
        print(("     " * self.depth) + "Node being printed ==================================")
        self.state.print_state()
        print(("     " * self.depth) + "options: " + str(self.options))
        print(("     " * self.depth) + "rating: " + str(self.rating))
        print(("     " * self.depth) + "depth: " + str(self.depth))
        print(("     " * self.depth) + "best_move: " + str(self.best_move))
        print(("     " * self.depth) + "number of children: " + str(len(self.children)))

    def print_node_and_children(self):
        self.print_node()
        for node in self.children:
            node.print_node()
    
    def print_node_recursive(self):
        self.print_node()
        for node in self.children:
            node.print_node_recursive()

    def enumerate_nodes(self):
        # create all child nodes
        for option in self.options:
            next_state = copy.deepcopy(self.state)
            next_state.do_option(option)
            new_node = Node(next_state, self.tree, self.depth + 1, self)
            self.children.append(new_node)

    def update_best_move(self):
        # if we are a leaf node, just return since there are no moves after us
        if len(self.children) == 0:
            return
        # we want to get rid of our rating because the game is moving on, we can't just pause
        self.rating = self.children[0].rating
        self.best_move = self.options[0]
        # look at all child nodes, update own rating to be the best one
        for move_num in range(len(self.children)):
            (self.rating, self.best_move) = self.state.get_better_choice(self.rating, self.best_move, self.children[move_num].rating, self.options[move_num])
   
    def update_self_and_tree_above(self):
        #update our best move, then traverse up and do the same thing
        self.update_best_move()
        # exit if we are the root node
        if(self.parent == None):
            return
        self.parent.update_self_and_tree_above()
            
