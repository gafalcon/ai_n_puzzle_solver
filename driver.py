"""Implementation of an intelligent solver of the n-puzzle game """
import argparse
import resource
import time
import structs

SEARCH_STRUCT = {
    "bfs": structs.Queue,
    "dfs": structs.Stack,
    "ast": list,
    "queue": list
}

class State():
    """Represents a state of the game"""
    def __init__(self, board, is_array=True, father=None):
        "Represents a board state"
        if is_array:
            self.state = board
        else:
            board = [int(tile) for tile in board.split(",")]
            self.state = ((board[0], board[1], board[2]),
                          (board[3], board[4], board[5]),
                          (board[6], board[7], board[8]))
        self.father = father

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
            childs.append(self.swap_copy(x_0, y_0, x_0 - 1, y_0)) #up
        if x_0 < 2: #row is not last one
            childs.append(self.swap_copy(x_0, y_0, x_0 + 1, y_0)) #down
        if y_0 > 0: #col is not first one
            childs.append(self.swap_copy(x_0, y_0, x_0, y_0 - 1)) #left
        if y_0 < 2: #col is not last one
            childs.append(self.swap_copy(x_0, y_0, x_0, y_0 + 1)) #right

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

class Solver():
    """Solves the game"""
    def __init__(self, board, method):
        "docstring"
        self.init_state = State(board, False)
        self.search_method = method

        self.nodes_expanded = 0
        self.frontier_size = 0
        self.max_frontier_size = 0
        self.max_ram_usage = 0

    def search(self):
        """Finds answer"""
        frontier = SEARCH_STRUCT[self.search_method]([self.init_state])
        explored = structs.Stack()#[]#set()

        while not frontier.is_empty():
            state = frontier.pop()
            explored.add(state)

            print("State to explore")
            print(state)
            if state.is_goal_test():
                print("Goal test found!")
                self.frontier_size = frontier.size()
                return True

            self.nodes_expanded += 1
            for neighbor in state.get_childs(self.search_method):
                child_state = State(neighbor)
                if not frontier.contains(child_state) and not explored.contains(child_state):
                    frontier.add(child_state)
                    print("************* Child appended: \n",child_state)

            self.max_frontier_size = max(self.max_frontier_size, frontier.size())
            ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
            # print("Ram usage:", ram_usage)
            self.max_ram_usage = max(self.max_ram_usage, ram_usage)

        return False


    def begin_search(self):
        """Track memory and time consumption"""
        begin_time = time.process_time()
        self.search()
        elapsed_time = time.process_time() - begin_time
        print("path_to_goal:")
        print("cost_of_path:")
        print("nodes_expanded:", self.nodes_expanded)
        print("fringe_size:", self.frontier_size)
        print("max_fringe_size:", self.max_frontier_size)
        print("search_depth:")
        print("max_search_depth:")
        print("running_time:", elapsed_time)
        print("max_ram_usage:", self.max_ram_usage)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve the n-puzzle game")
    parser.add_argument('method', help="The search method to solve the puzzle",
                        type=str, choices=["bfs", "dfs", "ast", "ida"])
    parser.add_argument('board', help="The initial configuration of the board")
    args = parser.parse_args()
    Solver(args.board, args.method).begin_search()
