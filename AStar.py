SIZE = 9
START_SYMBOL = 'P'
END_SYMBOL = 'G'

# Define colors value for print colored text in terminal
COLOR_RED = '\33[91m'
COLOR_GRAY = '\33[90m'
COLOR_BLUE = '\33[94m'


# In this function, we first convert the input to a list, then we convert it to a list containing integer values
def save_matrix_as_list(matrix_file_inp):
    #  convert to list
    lines = []
    while True:
        line = matrix_file_inp.readline()
        if line == '':
            break  # end of file
        if "\n" in line:
            line = line[0:len(line) - 1]
        line = line.split()
        lines.append(line)
    # convert to integer list
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != START_SYMBOL and lines[i][j] != END_SYMBOL:
                lines[i][j] = int(lines[i][j])
    return lines


# this method calculate heuristic value of input node
def heuristic(current_row, current_col, end_x_inp, end_y_inp):
    return abs(end_x_inp - current_row) + abs(end_y_inp - current_col)


# this method calculate cost of given node (f = g + h)
def path_cost_calc(current_cost, heuristic_of_node):
    return current_cost + heuristic_of_node


# this method searches for input -char- and returns coordinates of it in given matrix
# we use this method for find coordinates of START_SYMBOL and END_SYMBOL in given matrix
def search_char(matrix_inp, char):
    for row in range(len(matrix_inp)):
        for col in range(len(matrix_inp[row])):
            if matrix_inp[row][col] == char:
                return row, col


# in this method we search for valid neighbors of current node(cells in the matrix whose value is not one)
def find_children(game_board, cell_row, cell_col):
    children = []
    if cell_row > 0:
        if (game_board[cell_row - 1][cell_col] == 0 or game_board[cell_row - 1][cell_col] == END_SYMBOL or
                game_board[cell_row - 1][cell_col] == START_SYMBOL):
            children.append((cell_row - 1, cell_col))
    if cell_row < SIZE:
        if (game_board[cell_row + 1][cell_col] == 0 or game_board[cell_row + 1][cell_col] == END_SYMBOL
                or game_board[cell_row + 1][cell_col] == START_SYMBOL):
            children.append((cell_row + 1, cell_col))
    if cell_col > 0:
        if (game_board[cell_row][cell_col - 1] == 0 or game_board[cell_row][cell_col - 1] == END_SYMBOL or
                game_board[cell_row][cell_col - 1] == START_SYMBOL):
            children.append((cell_row, cell_col - 1))
    if cell_col < SIZE:
        if (game_board[cell_row][cell_col + 1] == 0 or game_board[cell_row][cell_col + 1] == END_SYMBOL
                or game_board[cell_row][cell_col + 1] == START_SYMBOL):
            children.append((cell_row, cell_col + 1))
    return children


# this method create next level of search graph
def create_next_level_of_graph(children, current_node, visited, graph, end_x, end_y):
    for child in children:
        next_cost = current_node[2] + 1
        if child in visited:
            continue
        graph.append((child, [current_node[0]] + current_node[1], next_cost,
                      heuristic(child[0], child[1], end_x, end_y)))


# this method used for sorting and create queue
def comparison(current_node):
    return path_cost_calc(current_node[2], current_node[3])


# A method to check that we have reached the goal?
def objective_test(matrix, current_row, current_col):
    if matrix[current_row][current_col] == END_SYMBOL:
        return True
    return False


# We reverse the list Because we want the path from beginning to end
def return_path(path_from_end_to_start):
    path_from_end_to_start.reverse()
    path_from_start_to_end = path_from_end_to_start
    return path_from_start_to_end


# The main method that performs the A*
# and returns the result in the form of a list that contains the path from start to finish
def a_star(matrix, start_x, start_y, end_x, end_y):
    # Create graph and add root node
    # Every node in this graph is [coordinates of point in matrix, current path, current cost, heuristic of node]
    graph = [((start_x, start_y), [], 0, heuristic(start_x, start_y, end_x, end_y))]

    # We need a visited set Because our search is a graph search
    # This set of nodes that have been observed so far keeps cost up to this cell
    visited = {}

    while True:
        # The node with the lowest value of the function F
        current_node = graph.pop(0)
        # graph search
        if current_node[0] in visited:
            continue

        # Coordinates of current node in matrix
        current_row, current_col = current_node[0]

        # If this cell is end cell (check objective test when a node is selected)
        if objective_test(matrix, current_row, current_col):
            return return_path([current_node[0]] + current_node[1])

        # add current node to visited set
        visited[current_node[0]] = True
        # find all neighbors of current cell which contains ZERO or END_SYMBOL
        children = find_children(matrix, current_row, current_col)
        # Create next level of graph and sort nodes based on F function
        create_next_level_of_graph(children, current_node, visited, graph, end_x, end_y)
        graph.sort(key=comparison)


# This method print Game board
# Color of path is red!
def print_path(matrix, a_star_path, start_x, start_y, end_x, end_y):
    for i in range(SIZE + 2):
        for j in range(39):
            print(COLOR_GRAY + "-" + COLOR_GRAY, end="")
        print()
        if i == SIZE + 1:
            break
        for j in range(len(matrix[i])):
            if (i, j) == (start_x, start_y):
                print(COLOR_RED + START_SYMBOL + COLOR_RED, end="")
                print(COLOR_GRAY + " | " + COLOR_GRAY, end="")
            elif (i, j) == (end_x, end_y):
                print(COLOR_RED + END_SYMBOL + COLOR_RED, end="")
                print(COLOR_GRAY + " | " + COLOR_GRAY, end="")
            elif (i, j) in a_star_path:
                print(COLOR_RED + "*" + COLOR_RED, end="")
                print(COLOR_GRAY + " | " + COLOR_GRAY, end="")
            else:
                print(COLOR_GRAY + str(matrix[i][j]) + COLOR_GRAY, end=" | ")

        print()
    print()


def solve():
    matrix_file = open("matrix.txt", "r")
    matrix = save_matrix_as_list(matrix_file)
    # Find the starting cell coordinates
    start_x, start_y = search_char(matrix, START_SYMBOL)
    # Find the end cell coordinates
    end_x, end_y = search_char(matrix, END_SYMBOL)

    a_star_path = a_star(matrix, start_x, start_y, end_x, end_y)
    print_path(matrix, a_star_path, start_x, start_y, end_x, end_y)

    print(COLOR_BLUE + str(a_star_path) + COLOR_BLUE)


solve()
