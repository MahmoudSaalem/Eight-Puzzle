import sys
import math
import timeit

if sys.platform == "win32":
    import psutil
else:
    import resource


class Frontier(object):
    def __init__(self, method="queue"):
        if method.lower() not in ["queue", "stack", "heap"]:
            raise Exception("Invalid frontier type")
        self.method = method
        self._frontier = []
        self._frontier_set = set()

    def push(self, val):
        if self.method.lower() == "heap":
            self._frontier.insert(0, val)
            self._frontier.sort(reverse=True, key=lambda tup: tup[0])
            self._frontier_set.add(val[1].config)
        else:
            self._frontier.append(val)
            self._frontier_set.add(val.config)

    def pop(self):
        if self.method.lower() == "stack":
            ret = self._frontier.pop()
        elif self.method.lower() == "queue":
            ret = self._frontier.pop(0)
        else:
            ret = self._frontier.pop()[1]
        self._frontier_set.remove(ret.config)
        return ret

    def update_key(self, val, cost):
        if self.method.lower == "heap":
            for i, elem in enumerate(self._frontier):
                if elem[1].config == val.config:
                    if cost < elem[0]:
                        self._frontier.pop(i)
                        self._frontier.append((cost, val))
                        self._frontier.sort(reverse=True, key=lambda tup: tup[0])
                    break

    def exists(self, val):
        return val.config in self._frontier_set


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


# GLOBAL VARIABLES
nodes_expanded = 0
max_depth = 0
running_time = 0


def write_output(state: PuzzleState):
    global running_time
    ram_usage = psutil.Process().memory_info().rss if sys.platform == "win32" else \
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    ram_usage = round(ram_usage / 1048576, 8)
    running_time = round(running_time, 8)
    path = path_to_goal(state)
    output = ""
    output += "Cost of path: " + str(state.cost) + "\n"
    output += "Nodes expanded: " + str(nodes_expanded) + "\n"
    output += "Search depth: " + str(state.cost) + "\n"
    output += "Max search depth: " + str(max_depth) + "\n"
    output += "Running time: " + str(running_time) + " sec\n"
    output += "Max RAM usage: " + str(ram_usage) + " MB\n"
    output += "Path to goal: " + str(path)
    f = open("output.txt", "w")
    f.write(output)
    f.close()
    print(output)
    return path


def path_to_goal(state: PuzzleState):
    path = []
    curr_state = state
    while curr_state.action != "Initial":
        path.append(curr_state.action)
        curr_state = curr_state.parent
    path.reverse()
    return path


def bfs_search(initial_state):
    """BFS search"""
    global nodes_expanded
    global max_depth
    frontier = Frontier("Queue")
    explored = set()
    frontier.push(initial_state)
    while frontier:
        state: PuzzleState = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            return state

        for neighbor in state.expand():
            if neighbor.config not in explored and not frontier.exists(neighbor):
                max_depth = max(max_depth, neighbor.cost)
                frontier.push(neighbor)
    return False


def dfs_search(initial_state):
    """DFS search"""
    global nodes_expanded
    global max_depth
    frontier = Frontier("Stack")
    explored = set()
    frontier.push(initial_state)
    while frontier:
        state: PuzzleState = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            return state

        for neighbor in state.reverse_expand():
            if neighbor.config not in explored and not frontier.exists(neighbor):
                max_depth = max(max_depth, neighbor.cost)
                frontier.push(neighbor)
    return False


def a_star_search(initial_state, cost_function):
    """A * search"""
    global nodes_expanded
    global max_depth
    frontier = Frontier("heap")
    explored = set()
    frontier.push((calculate_total_cost(initial_state, cost_function), initial_state))
    while frontier:
        state: PuzzleState = frontier.pop()
        explored.add(state.config)

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            return state

        for neighbour in state.expand():
            cost = calculate_total_cost(neighbour, cost_function)
            if neighbour.config not in explored and not frontier.exists(neighbour):
                max_depth = max(max_depth, neighbour.cost)
                frontier.push((cost, neighbour))
            elif frontier.exists(neighbour):
                frontier.update_key(neighbour, cost)
    return False


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


def solve(state, method):
    global running_time
    if method == "bfs":
        start = timeit.default_timer()
        solved_state = bfs_search(state)
        running_time = timeit.default_timer() - start
        return write_output(solved_state)
    elif method == "dfs":
        start = timeit.default_timer()
        solved_state = dfs_search(state)
        running_time = timeit.default_timer() - start
        return write_output(solved_state)
    elif method == "ast_man":
        start = timeit.default_timer()
        solved_state = a_star_search(state, calculate_manhattan_dist)
        running_time = timeit.default_timer() - start
        return write_output(solved_state)
    elif method == "ast_euc":
        start = timeit.default_timer()
        solved_state = a_star_search(state, calculate_euclidean_dist)
        running_time = timeit.default_timer() - start
        return write_output(solved_state)
    else:
        print("Enter valid command arguments !")


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
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    solve(hard_state, method)


if __name__ == '__main__':
    main()
