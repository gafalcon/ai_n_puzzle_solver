"""Implementation of an intelligent solver of the n-puzzle game """
import argparse
import resource
import time
import structs

SEARCH_STRUCT = {
    "bfs": structs.Queue,
    "dfs": structs.Stack,
    "ast": structs.Heap,
    "ida": structs.Heap
}
def h(state):
    """heuristic for state"""
    return structs.sum_manhattan_distance(state.state)
def f(state):
    """Total cost for state"""
    return h(state) + state.depth

class State():
    """Represents a state of the game"""
    def __init__(self, board, is_array=True, parent=None, action=None):
        "Represents a board state"
        if is_array:
            self.state = board
        else:
            board = [int(tile) for tile in board.split(",")]
            self.state = ((board[0], board[1], board[2]),
                          (board[3], board[4], board[5]),
                          (board[6], board[7], board[8]))
        self.parent = parent
        self.action = action
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    def find_empty_space(self):
        """Finds location of empty tile"""
        for i, elem in enumerate(self.state):
            if 0 in elem:
                return (i, elem.index(0))

    def swap_copy(self, x_1, y_1, x_2, y_2):
        """Creates a copy of state with values at (x1,y1) and (x2,y2) swapped"""
        child = [list(row) for row in self.state]
        child[x_1][y_1], child[x_2][y_2] = child[x_2][y_2], child[x_1][y_1]
        return (tuple(child[0]), tuple(child[1]), tuple(child[2]))


    def is_goal_test(self):
        """Checks if state is goal state"""
        return self.state == ((0, 1, 2), (3, 4, 5), (6, 7, 8))

    def get_childs(self, method=None):
        """Finds all possible next states"""
        childs = []
        x_0, y_0 = self.find_empty_space()
        if x_0 > 0: #row is not first one
            childs.append(State(self.swap_copy(x_0, y_0, x_0 - 1, y_0), parent=self, action="Up"))
        if x_0 < 2: #row is not last one
            childs.append(State(self.swap_copy(x_0, y_0, x_0 + 1, y_0), parent=self, action="Down"))
        if y_0 > 0: #col is not first one
            childs.append(State(self.swap_copy(x_0, y_0, x_0, y_0 - 1), parent=self, action="Left"))
        if y_0 < 2: #col is not last one
            childs.append(State(self.swap_copy(x_0, y_0, x_0, y_0 + 1), parent=self, action="Right"))

        if method == "dfs":
            childs.reverse()
        return childs

    def __eq__(self, other):
        return self.state == other.state

    def __str__(self):
        return "{}{}{}\n{}{}{}\n{}{}{}".format(
            self.state[0][0], self.state[0][1], self.state[0][2],
            self.state[1][0], self.state[1][1], self.state[1][2],
            self.state[2][0], self.state[2][1], self.state[2][2],
        )

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.state.__lt__(other.state)

class Solver():
    """Solves the game"""
    def __init__(self, board, method):
        "docstring"
        self.init_state = State(board, False)
        self.search_method = method
        self.bound = 0
        self.nodes_expanded = 0
        self.frontier_size = 0
        self.max_frontier_size = 0
        self.max_ram_usage = 0
        self.max_search_depth = 0

    def search(self):
        """Finds answer"""
        frontier = SEARCH_STRUCT[self.search_method]([self.init_state])
        frontier_set = set()
        explored = set()
        # depth = self.init_state.depth
        while not frontier.is_empty():
            state = frontier.pop()
            explored.add(state.state)

            if state.is_goal_test():
                self.frontier_size = frontier.size()
                return state

            self.nodes_expanded += 1

            if self.search_method == "ida":
                cost = f(state)
                if cost > self.bound:
                    self.bound = cost
                    return

            for child_state in state.get_childs(self.search_method):
                if not child_state.state in frontier_set and not child_state.state in explored:
                    self.max_search_depth = max(self.max_search_depth, child_state.depth)
                    frontier.add(child_state)
                    frontier_set.add(child_state.state)

            self.max_frontier_size = max(self.max_frontier_size, frontier.size())
            ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            self.max_ram_usage = max(self.max_ram_usage, ram_usage)


    def get_actions(self, last_state):
        """prints path from initial state to goal"""
        state = last_state
        actions = []
        while not state is None:
            if state.action:
                actions.append(state.action)
            state = state.parent
        actions.reverse()
        return actions

    def begin_search(self):
        """Track memory and time consumption"""
        begin_time = time.process_time()
        # last_state = self.search()
        last_state = None
        if self.search_method == "ida":
            self.bound = h(self.init_state)
            while True:
                last_state = self.search()
                if last_state:
                    break
        else:
            last_state = self.search()

        actions = self.get_actions(last_state)
        elapsed_time = time.process_time() - begin_time
        print("path_to_goal:", actions)
        print("cost_of_path:", len(actions))
        print("nodes_expanded:", self.nodes_expanded)
        print("fringe_size:", self.frontier_size)
        print("max_fringe_size:", self.max_frontier_size)
        print("search_depth:", last_state.depth)
        print("max_search_depth:", self.max_search_depth)
        print("running_time:", elapsed_time)
        print("max_ram_usage:", self.max_ram_usage)
        # with open("output.txt", "w") as output_file:
        #     output_file.write("path_to_goal: {}\n".format(actions))
        #     output_file.write("cost_of_path: {}\n".format(len(actions)))
        #     output_file.write("nodes_expanded: {}\n".format(self.nodes_expanded))
        #     output_file.write("fringe_size: {}\n".format(self.frontier_size))
        #     output_file.write("max_fringe_size: {}\n".format(self.max_frontier_size))
        #     output_file.write("search_depth: {}\n".format(last_state.depth))
        #     output_file.write("max_search_depth: {}\n".format(self.max_search_depth))
        #     output_file.write("running_time: {}\n".format(elapsed_time))
        #     output_file.write("max_ram_usage: {}\n".format(self.max_ram_usage))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the n-puzzle game")
    parser.add_argument('method', help="The search method to solve the puzzle",
                        type=str, choices=["bfs", "dfs", "ast", "ida"])
    parser.add_argument('board', help="The initial configuration of the board")
    args = parser.parse_args()
    Solver(args.board, args.method).begin_search()
