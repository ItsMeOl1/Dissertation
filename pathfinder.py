from warnings import warn
import heapq  # used to create heap structures


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0  # how far from start
        self.h = 0  # using Pythagoras to find a heuristic
        self.f = 0  # final

    def __eq__(self, other):  # is this node equal to another
        return self.position == other.position

    def __lt__(self, other):  # less than
        return self.f < other.f

    def __gt__(self, other):  # greater than
        return self.f > other.f

    def set_Values(self, g, h):
        self.g = g
        self.h = h
        self.f = self.g + self.h


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end):

    # Create start and end node
    start_node = Node(None, start)
    start_node.set_Values(0, 0)
    end_node = Node(None, end)
    end_node.set_Values(0, 0)

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # What squares to search
    adjacent = ((0, -1), (0, 1), (-1, 0), (1, 0))

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node: # If found the goal
            return return_path(current_node)

        children = [] # Generate children

        for new_pos in adjacent:  # Adjacent squares
            # Get node position
            node_position = (
                current_node.position[0] + new_pos[0], current_node.position[1] + new_pos[1])

            # If in maze
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0: # Make sure nothing built there
                continue

            new_node = Node(current_node, node_position) # Create new node

            children.append(new_node)

        
        for child in children: # Loop through children
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0: # Child is on the closed list
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) **
                       2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            heapq.heappush(open_list, child) # Add the child to the open list

    return False # Couldn't find a path
