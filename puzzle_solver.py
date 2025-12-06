"""
Puzzle 8 Solver - A* Algorithm Implementation

This module contains the core logic for solving the 8-puzzle using the A* algorithm
with Manhattan distance heuristic.
"""

from queue import PriorityQueue


def tuple_to_board(state):
    """Convierte una tupla a lista para uso interno si es necesario"""
    return [list(row) for row in state]


def board_to_tuple(board):
    """Convierte un tablero (lista) a tupla inmutable"""
    return tuple(tuple(row) for row in board)


def is_solvable(board):
    """Verifica si el tablero es resoluble contando inversiones"""
    flat_board = [num for row in board for num in row if num != 0]
    inversions = sum(
        1
        for i in range(len(flat_board) - 1)
        for j in range(i + 1, len(flat_board))
        if flat_board[i] > flat_board[j]
    )
    return inversions % 2 == 0


def find_zero(state):
    """Encuentra la posición del espacio vacío (0)"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None


def get_neighbors(state):
    """Genera todos los estados vecinos posibles (arriba, abajo, izquierda, derecha)"""
    neighbors = []
    board = tuple_to_board(state)
    i, j = find_zero(state)

    # Arriba
    if i > 0:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i - 1][j] = new_board[i - 1][j], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Abajo
    if i < 2:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i + 1][j] = new_board[i + 1][j], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Izquierda
    if j > 0:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i][j - 1] = new_board[i][j - 1], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    # Derecha
    if j < 2:
        new_board = [row[:] for row in board]
        new_board[i][j], new_board[i][j + 1] = new_board[i][j + 1], new_board[i][j]
        neighbors.append(board_to_tuple(new_board))

    return neighbors


def manhattan_distance(state, goal):
    """Calcula la distancia de Manhattan entre el estado actual y el objetivo"""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                num = state[i][j]
                for goal_i in range(3):
                    for goal_j in range(3):
                        if goal[goal_i][goal_j] == num:
                            distance += abs(i - goal_i) + abs(j - goal_j)
                            break
    return distance


def reconstruct_path(came_from, current):
    """Reconstruye el camino desde el inicio hasta el objetivo"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def a_star(start, goal):
    """
    Implementación del algoritmo A*

    Args:
        start: Estado inicial del tablero (tupla de tuplas)
        goal: Estado objetivo del tablero (tupla de tuplas)

    Returns:
        tuple: (path, nodes_explored, nodes_generated) o (None, nodes_explored, nodes_generated)
               - path: Lista de estados desde el inicio hasta el objetivo
               - nodes_explored: Número de nodos explorados
               - nodes_generated: Número total de nodos generados
    """
    if not is_solvable(start):
        return None, 0, 0

    counter = 0
    open_set = PriorityQueue()
    open_set.put((0, counter, start))
    counter += 1

    came_from = {}
    g_score = {start: 0}
    closed_set = set()

    nodes_generated = 1
    nodes_explored = 0

    while not open_set.empty():
        current_f, _, current = open_set.get()

        if current in closed_set:
            continue

        nodes_explored += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, nodes_explored, nodes_generated

        closed_set.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                h_score = manhattan_distance(neighbor, goal)
                f_score = tentative_g_score + h_score

                open_set.put((f_score, counter, neighbor))
                counter += 1
                nodes_generated += 1

    return None, nodes_explored, nodes_generated
