import queue as Q
import time
import sys
import math
import heapq

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

    def reverse_expand(self):
        """expand the node"""
        # add child nodes in order of reverse-UDLR
        if len(self.children) == 0:
            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)
        return self.children


def write_output():
    pass


def bfs_search(initial_state):
    """BFS search"""
    frontier = []
    explored = set()
    frontier.append(initial_state)
    while frontier:
        state: PuzzleState = frontier.pop(0)
        explored.add(state.config)

        if test_goal(state):
            print(state.cost)
            return state.display()

        for neighbor in state.expand():
            if neighbor.config not in explored and neighbor not in frontier:
                frontier.append(neighbor)
    return False


def dfs_search(initial_state):
    """DFS search"""
    frontier = []
    explored = set()
    frontier.append(initial_state)
    while frontier:
        state: PuzzleState = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            print(state.cost)
            return state.display()

        for neighbor in state.reverse_expand():
            if neighbor.config not in explored and neighbor not in frontier:
                frontier.append(neighbor)
    return False


def a_star_search(initial_state, cost_function):
    """A * search"""
    frontier = []
    explored = set()
    frontier.append((calculate_total_cost(initial_state, cost_function), initial_state))
    while frontier:
        state: PuzzleState = frontier.pop()[1]
        explored.add(state.config)

        if test_goal(state):
            print(state.cost)
            return state.display()

        for neighbour in state.expand():
            cost = calculate_total_cost(neighbour, calculate_manhattan_dist)
            if neighbour.config not in explored and not in_priority_queue(frontier, neighbour):
                frontier.append((cost, neighbour))
                frontier.sort(reverse=True, key=lambda tup: tup[0])
            elif in_priority_queue(frontier, neighbour):
                update_queue_key(frontier, neighbour, cost)
    return False


def in_priority_queue(frontier, val):
    for elem in frontier:
        if elem[1].config == val.config:
            return True
    return False


def update_queue_key(frontier, val, cost):
    for i, elem in enumerate(frontier):
        if elem[1].config == val.config:
            if cost < elem[0]:
                frontier.pop(i)
                frontier.append((cost, val))
                frontier.sort(reverse=True, key=lambda tup: tup[0])
            break


def calculate_total_cost(state, cost_function):
    """calculate the total estimated cost of a state"""
    cost = 0
    for idx, value in enumerate(state.config):
        if value == 0:
            continue
        cost += cost_function(idx, value, state.n)
    return cost + state.cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    goal_x = value // n
    goal_y = value % n
    curr_x = idx // n
    curr_y = idx % n
    return abs(goal_x - curr_x) + abs(goal_y - curr_y)


def calculate_euclidean_dist(idx, value, n):
    """calculate the euclidean distance of a tile"""
    goal_x = value // n
    goal_y = value % n
    curr_x = idx // n
    curr_y = idx % n
    return math.sqrt(pow(goal_x - curr_x, 2) + pow(goal_y - curr_y, 2))


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
            exit(-1)  # Program execution failed.


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    method = get_arg(1, "ast_man").lower()
    begin_state = get_arg(2, "8,6,4,2,1,3,5,7,0").split(",")
    # begin_state= "1,0,2,3,4,5,6,7,8".split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    hard_state.display()
    # print("After DFS:")
    # dfs_search(hard_state)
    if method == "bfs":
        bfs_search(hard_state)
    elif method == "dfs":
        dfs_search(hard_state)
    elif method == "ast_man":
        a_star_search(hard_state, calculate_manhattan_dist)
    elif method == "ast_euc":
        a_star_search(hard_state, calculate_euclidean_dist)
    else:
        print("Enter valid command arguments !")


if __name__ == '__main__':
    main()
