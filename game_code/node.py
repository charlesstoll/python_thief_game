#!/bin/python3

import sys
import copy
import math

# creates a decision tree for searching the tree. The class passed in
# as the object for the root node needs to have a few functions:
# state1.get_options() -> return a list of all DOABLE options for how to move from this state
# state1.get_rating() -> gets the value (goodness) of the given state
# state1.get_cost(state2) -> gets the cost to move from state2 to state1
# state1.do_option(option) -> does the option move on the state
# state1.get_better_choice(r1, op1, r2, op2) -> returns the better rating, option pair
class Decision_Tree(object):
    def __init__(self, base_state):
        self.root_node = Node(copy.deepcopy(base_state), self)
        self.nodes_to_iterate = []
    
    def find_depth_first(self, depth, winning_val=0):
        self.recursive_find_depth_first(depth, winning_val)
        return root_node.best_move

    def recursive_find_depth_first(self, depth, winning_val=0):
        # recursive exit point. we just return the best thing we have found
        if len(self.nodes_to_iterate) == 0:
            return
        # if we got a winning move, just do that move
        if self.root_node.rating == winning_val:
            return
        # apparently we are not done so keep going
        next_node = self.nodes_to_iterate.pop(0)
        if next_node.depth == depth:
            return
        next_node.enumerate_nodes()
        # added some new nodes so get our best move
        next_node.update_self_and_tree_above()
        next_node.enumerate_nodes()
        self.nodes_to_iterate.extend(next_node.children)
        # keep going!!!
        self.recursive_find_depth_first(depth, winning_val)

class Node(object):
    def __init__(self, state, tree, path_to_here=[], depth=0, parent=None):
        self.state = state
        self.options = self.state.get_options()
        self.rating = self.state.get_rating()
        if not parent == None:
            # refers to the parent NODE. NOOOOOT the parent state
            self.parent = parent
        self.depth = depth
        self.path_to_here = path_to_here
        self.best_move = "err"
        self.cost_to_get_here = self.state.get_cost(self.parent.state)
        self.children = []

    def enumerate_nodes(self):
        # create all child nodes
        for option in self.options:
            next_state = copy.deepcopy(self.state)
            next_state.do_option(option)
            next_path = copy.deepcopy(self.path).append(option)
            new_node = Node(next_state, self.tree, next_path, self.depth + 1, self)
            self.children.append(new_node)

    def update_best_move(self):
        # we want to get rid of our rating because the game is moving on, we can't just pause
        self.rating = self.children[0].rating
        self.best_move = self.options[0]
        # look at all child nodes, update own rating to be the best one
        for move_num in len(self.children):
            (self.rating, self.best_move) = self.state.get_better_choice(self.rating, self.best_move, self.children[move_num].rating, self.options[move_num])
    
    def update_self_and_tree_above(self):
        #update our best move, then traverse up and do the same thing
        self.update_best_move()
        # exit if we are the root node
        if(self.parent == None):
            return
        # update the tree above if we are not
        self.parent.update_tree_above()

            
