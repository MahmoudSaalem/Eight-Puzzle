import queue as Q
import time
import sys
import math
if sys.platform == "win32":
    import psutil
    # print("psutil", psutil.Process().memory_info().rss)
else:
    import resource
    # print("resource", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


# The Class that Represents the Puzzle

class PuzzleState(object):
    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != 9 or len(config) != 9:
            raise Exception("the length of config is not correct!")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)
            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
        return self.children


def write_output():
    pass


def bfs_search(initial_state):
    """BFS search"""

    pass


def dfs_search(initial_state):
    """DFS search"""

    pass


def a_star_search(initial_state):
    """A * search"""

    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""

    pass


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""

    pass


def test_goal(puzzle_state: PuzzleState):
    """test the state is the goal state or not"""
    goal_state = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    return puzzle_state.config == goal_state


def get_arg(param_index, default=None):
    """
    Gets a command line argument by index (note: index starts from 1)
    If the argument is not supplies, it tries to use a default value.
    If a default value isn't supplied, an error message is printed
    and terminates the program.
    """
    try:
        return sys.argv[param_index]
    except IndexError as e:
        if default:
            return default
        else:
            print(e)
            print(
                f"[FATAL] The command-line argument #[{param_index}] is missing")
            exit(-1)    # Program execution failed.


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    method = get_arg(1, "bfs").lower()
    begin_state = get_arg(2, "1,0,2,3,4,5,6,7,8").split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    if method == "bfs":
        bfs_search(hard_state)
    elif method == "dfs":
        dfs_search(hard_state)
    elif method == "ast":
        a_star_search(hard_state)
    else:
        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()
